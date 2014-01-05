Summary:	Instant messaging program
Name:		pidgin
Version:	2.10.7
Release:	1
License:	GPL
Group:		Applications/Communications
Source0:	http://downloads.sourceforge.net/pidgin/%{name}-%{version}.tar.bz2
# Source0-md5:	ea88976b9952e80b702b030489f94393
Patch0:		%{name}-nolibs.patch
Patch1:		%{name}-desktop.patch
Patch2:		%{name}-dbus-dir.patch
URL:		http://www.pidgin.im/
BuildRequires:	NetworkManager-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	avahi-glib-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	gettext-autopoint
#BuildRequires:	gstreamer010-plugins-base-devel
#BuildRequires:	farstream-devel
BuildRequires:	gettext-devel
BuildRequires:	gstreamer-devel
BuildRequires:	gtk+-devel
BuildRequires:	gtkspell-devel
BuildRequires:	libtool
BuildRequires:	ncurses-ext-devel
BuildRequires:	pkg-config
BuildRequires:	xorg-libXScrnSaver-devel
Requires(post,postun):	hicolor-icon-theme
Requires:	libpurple = %{version}-%{release}
Suggests:	avahi
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Pidgin allows you to talk to anyone using AOL's Instant Messenger
service (you can sign up at http://www.aim.aol.com). It uses the TOC
version of the AOL protocol, so your buddy list is stored on AOL's
servers and can be retrieved from anywhere. It contains many of the
same features as AOL's IM client while at the same time incorporating
many new features. Pidgin also contains a multiple connection feature
which consists of protocol plugins. These plugins allow you to use
Pidgin to connect to other chat services such as Yahoo!, ICQ, MSN,
Jabber, Napster, Zephyr, IRC and Gadu-Gadu.

%package -n finch
Summary:	Pidgin console UI
Group:		Applications/Communications
Epoch:		1
Requires:	finch-libs = %{version}-%{release}

%description -n finch
Pidgin console UI.

%package -n libpurple
Summary:	Pidgin client library
Group:		Libraries

%description -n libpurple
Pidgin client library.

%package -n finch-libs
Summary:	Pidgin console client library
Group:		Libraries

%description -n finch-libs
Pidgin console client library.

%package -n libpurple-devel
Summary:	Development files for Pidgin client library
Group:		Development/Libraries
Requires:	libpurple = %{version}-%{release}

%description -n libpurple-devel
Development files for Pidgin.

%package -n finch-devel
Summary:	Development files for Pidgin client library
Group:		Development/Libraries
Requires:	libpurple-devel = %{version}-%{release}
Requires:	finch-libs = %{version}-%{release}
Requires:	ncurses-devel

%description -n finch-devel
Development files for Pidgin.

%package plugin-evolution
Summary:	Plugin for Ximian Evolution integration
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description plugin-evolution
Provides integration with Evolution.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4macros
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	--disable-gevolution	\
	--disable-gstreamer	\
	--disable-meanwhile	\
	--disable-perl		\
	--disable-schemas-install	\
	--disable-silent-rules	\
	--disable-tcl		\
	--disable-tk		\
	--disable-vv		\
	--enable-dbus		\
	--with-static-prpls=bonjour,irc,jabber		\
	--with-system-ssl-certs=/etc/certs
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT{%{_bindir}/purple-client-example,%{_libdir}/purple-2/dbus-example.*}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/{finch,gnt,pidgin,purple-2}/*.la
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/{ca@valencia,mhr,my_MM,ms_MY,ps,sr@latin}

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor

%postun
%update_icon_cache hicolor

%post	-n libpurple -p /usr/sbin/ldconfig
%postun	-n libpurple -p /usr/sbin/ldconfig

%post	-n finch-libs -p /usr/sbin/ldconfig
%postun	-n finch-libs -p /usr/sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README* HACKING
%attr(755,root,root) %{_bindir}/pidgin
%attr(755,root,root) %{_bindir}/purple-remote
%attr(755,root,root) %{_bindir}/purple-send
%attr(755,root,root) %{_bindir}/purple-send-async
%attr(755,root,root) %{_bindir}/purple-url-handler
%dir %{_libdir}/pidgin
%attr(755,root,root) %{_libdir}/pidgin/*.so
%dir %{_libdir}/purple-2
%attr(755,root,root) %{_libdir}/purple-2/*.so
%{_datadir}/sounds/purple
%{_desktopdir}/pidgin.desktop
%{_pixmapsdir}/pidgin
%{_iconsdir}/hicolor/*/apps/pidgin.*
%{_mandir}/man?/*

%files -n finch
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/finch
%attr(755,root,root) %{_libdir}/finch/*.so
%attr(755,root,root) %{_libdir}/gnt/*.so
%dir %{_libdir}/finch
%dir %{_libdir}/gnt

%files -n libpurple
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libpurple-client.so.0
%attr(755,root,root) %ghost %{_libdir}/libpurple.so.0
%attr(755,root,root) %{_libdir}/libpurple-client.so.*.*.*
%attr(755,root,root) %{_libdir}/libpurple.so.*.*.*

%files -n finch-libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libgnt.so.0
%attr(755,root,root) %{_libdir}/libgnt.so.*.*.*

%files -n libpurple-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpurple-client.so
%attr(755,root,root) %{_libdir}/libpurple.so
%{_aclocaldir}/purple.m4
%{_includedir}/pidgin
%{_includedir}/libpurple
%{_pkgconfigdir}/pidgin.pc
%{_pkgconfigdir}/purple.pc

%files -n finch-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgnt.so
%{_includedir}/finch
%{_includedir}/gnt
%{_pkgconfigdir}/finch.pc
%{_pkgconfigdir}/gnt.pc

