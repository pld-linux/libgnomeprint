# TODO:
# add support to IBM OMNI drivers
Summary:	Printing library for GNOME
Summary(pl):	Biblioteka drukowania dla GNOME
Name:		libgnomeprint
Version:	2.1.2
Release:	1
License:	LGPL
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/gnome/sources/%{name}/2.1/%{name}-%{version}.tar.bz2
URL:		http://www.gnome.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bonobo-activation-devel >= 2.1.0
BuildRequires:	freetype-devel >= 2.0.0
BuildRequires:	glib2-devel >= 2.1.3
BuildRequires:	libart_lgpl-devel >= 2.3.7
BuildRequires:	libbonobo-devel >= 2.1.0
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 2.4.22
BuildRequires:	pango-devel >= 1.1.4
BuildRequires:	rpm-build >= 4.1-8.2
Requires:	bonobo-activation >= 2.1.0
PreReq:		ghostscript-fonts-std
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
Requires:	%{name} = %{version}
Requires:	glib2-devel >= 2.0.1
Requires:	gtk-doc-common
Requires:	libxml2-devel >= 2.4.7
Requires:	libart_lgpl-devel
Requires:	libbonobo-devel >= 1.110

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
Requires:	%{name}-devel = %{version}

%description static
Static version of libgnomeprint library.

%description static -l pl
Statyczna wersja biblioteki libgnomeprint.

%prep
%setup -q

%build
#%{__libtoolize}
#%{__aclocal}
#%{__autoconf}
#%{__automake}
%configure \
	--disable-font-install \
	--with-html-dir=%{_gtkdocdir} \
	--enable-gtk-doc
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/gnome/libgnomeprint-2.0/fonts

# It would probably be cleaner to use install DESTDIR=$RPM_BUILD_ROOT
# instead of %%makeinstall with this hack.
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	pkgconfigdir=%{_pkgconfigdir} \
	HTML_DIR=%{_gtkdocdir}

%find_lang %{name}-2.2

%clean
rm -rf $RPM_BUILD_ROOT

%post
## we could pass --dynamic here to install to /etc instead
## but I think it makes more sense to have this not be a config
## file, then people make their changes in /etc if they want
%{_bindir}/libgnomeprint-2.0-font-install \
       --aliases=%{_datadir}/libgnomeprint-2.0/fonts/adobe-urw.font \
       --recursive --static \
       %{_fontsdir}
/sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}-2.2.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
#%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%dir %{_libdir}/%{name}/*
%dir %{_libdir}/%{name}/*/*
%attr(755,root,root) %{_libdir}/%{name}/*/*/*.so*
%{_libdir}/%{name}/*/*/*.la
%attr(755,root,root) %{_libdir}/%{name}/*/*/*/*.so*
%{_libdir}/%{name}/*/*/*/*.la
%{_datadir}/gnome-print-*
#%{_datadir}/gnome/libgnomeprint-*
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
%{_libdir}/%{name}/*/*/*.a
%{_libdir}/%{name}/*/*/*/*.a
