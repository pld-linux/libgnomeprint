Summary:	Printing library for GNOME
Summary(pl):	Biblioteka drukowania dla GNOME
Name:		libgnomeprint
Version:	2.12.1
Release:	3
License:	LGPL v2+
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/gnome/sources/libgnomeprint/2.12/%{name}-%{version}.tar.bz2
# Source0-md5:	ea729d4968fe2169c84efb12ace5f6cc
URL:		http://www.gnome.org/
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake >= 1:1.7.2
BuildRequires:	cups-devel >= 1:1.1.20
BuildRequires:	freetype-devel >= 2.1.3
BuildRequires:	glib2-devel >= 1:2.11.2
BuildRequires:	gnome-common >= 2.8.0
BuildRequires:	gtk-doc >= 1.4
BuildRequires:	libart_lgpl-devel >= 2.3.17
BuildRequires:	libgnomecups-devel >= 0.2.2
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 2.6.25
BuildRequires:	pango-devel >= 1:1.13.1
BuildRequires:	pkgconfig
BuildRequires:	popt-devel
BuildRequires:	rpmbuild(macros) >= 1.197
Requires:	ghostscript-fonts-std
Requires:	pango >= 1:1.13.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNOME (GNU Network Object Model Environment) is a user-friendly set of
applications and desktop tools to be used in conjunction with a window
manager for the X Window System. The gnome-print package contains
libraries and fonts needed by GNOME applications for printing.

You should install the gnome-print package if you intend to use any of
the GNOME applications that can print. If you would like to develop
GNOME applications that can print you will also need to install the
gnome-print devel package.

%description -l pl
GNOME (GNU Network Object Model Environment) jest zestawem przyjaznych
dla u¿ytkownika aplikacji i narzêdzi do u¿ytku w po³±czeniu z zarz±dc±
okien X Window System. Pakiet libgnomeprint zawiera biblioteki
niezbêdne aplikacjom GNOME do drukowania.

%package devel
Summary:	Include files for libgnomeprint
Summary(pl):	Pliki nag³ówkowe libgnomeprint
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.11.2
Requires:	gtk-doc-common
Requires:	libart_lgpl-devel >= 2.3.17
Requires:	libxml2-devel >= 2.6.25
Requires:	pango-devel >= 1:1.13.1

%description devel
GNOME (GNU Network Object Model Environment) is a user-friendly set of
applications and desktop tools to be used in conjunction with a window
manager for the X Window System. The gnome-print-devel package
includes the libraries and include files needed for developing
applications that use the GNOME printing capabilities.

You should install the gnome-print-devel package if you would like to
develop GNOME applications that will use the GNOME print capabilities.
You do not need to install the gnome-print-devel package if you just
want to use the GNOME desktop environment.

%description devel -l pl
Pliki nag³ówkowe niezbêdne do kompilacji aplikacji u¿ywaj±cych
biblioteki drukowania GNOME.

%package static
Summary:	Static libgnomeprint library
Summary(pl):	Statyczna biblioteka libgnomeprint
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static version of libgnomeprint library.

%description static -l pl
Statyczna wersja biblioteki libgnomeprint.

%package cups
Summary:	CUPS module for libgnomeprint
Summary(pl):	Modu³ CUPS dla libgnomeprint
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description cups
CUPS module for libgnomeprint.

%description static -l pl
Modu³ CUPS dla libgnomeprint.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--disable-font-install \
	--with-html-dir=%{_gtkdocdir} \
	--enable-gtk-doc \
	--with-cups
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/gnome/libgnomeprint-2.0/fonts

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	pkgconfigdir=%{_pkgconfigdir} \
	HTML_DIR=%{_gtkdocdir}

# no static modules and *.la files - shut up check-files
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/*/modules/{*.{a,la},transports/*.{a,la},filters/*.{a,la}}

rm -r $RPM_BUILD_ROOT%{_datadir}/locale/no

%find_lang %{name}-2.2

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}-2.2.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/*
%dir %{_libdir}/%{name}/*/modules
%dir %{_libdir}/%{name}/*/modules/filters
%dir %{_libdir}/%{name}/*/modules/transports
%attr(755,root,root) %{_libdir}/%{name}/*/modules/filters/*.so*
%attr(755,root,root) %{_libdir}/%{name}/*/modules/libgnomeprintlpd.so
%attr(755,root,root) %{_libdir}/%{name}/*/modules/transports/*.so*
%{_datadir}/libgnomeprint
# for now it's the only package that uses /etc/gnome
%dir %{_sysconfdir}/gnome
%{_sysconfdir}/gnome/libgnomeprint-*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/*
%{_pkgconfigdir}/*.pc
%{_gtkdocdir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a

%files cups
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/*/modules/libgnomeprintcups.so
