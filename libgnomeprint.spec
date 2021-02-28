#
# Conditional build:
%bcond_with	apidocs	# enable gtk-doc
%bcond_without	papi	# PAPI printing support

Summary:	Printing library for GNOME
Summary(pl.UTF-8):	Biblioteka drukowania dla GNOME
Name:		libgnomeprint
Version:	2.18.8
Release:	9
License:	LGPL v2+
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/libgnomeprint/2.18/%{name}-%{version}.tar.bz2
# Source0-md5:	63b05ffb5386e131487c6af30f4c56ac
Patch0:		%{name}-includes.patch
Patch1:		%{name}-papi.patch
Patch2:		bison3.patch
URL:		http://www.gnome.org/
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake >= 1:1.7.2
BuildRequires:	bison
BuildRequires:	cups-devel >= 1:1.1.20
%{?with_apidocs:BuildRequires:	docbook-dtd412-xml}
BuildRequires:	flex
BuildRequires:	freetype-devel >= 2.1.3
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.14.1
BuildRequires:	gnome-common >= 2.20.0
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.8}
BuildRequires:	intltool >= 0.36.2
BuildRequires:	libart_lgpl-devel >= 2.3.19
BuildRequires:	libgnomecups-devel >= 0.2.2
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 1:2.6.30
BuildRequires:	pango-devel >= 1:1.18.3
%{?with_papi:BuildRequires:	papi-devel}
BuildRequires:	pkgconfig
BuildRequires:	popt-devel
BuildRequires:	rpmbuild(macros) >= 1.197
BuildRequires:	zlib-devel
Requires:	fonts-Type1-urw
Requires:	glib2 >= 1:2.14.1
Requires:	libart_lgpl >= 2.3.19
Requires:	libxml2 >= 1:2.6.30
Requires:	pango >= 1:1.18.3
# sr@Latn vs. sr@latin
Conflicts:	glibc-misc < 6:2.7
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

%description -l pl.UTF-8
GNOME (GNU Network Object Model Environment) jest zestawem przyjaznych
dla użytkownika aplikacji i narzędzi do użytku w połączeniu z zarządcą
okien X Window System. Pakiet libgnomeprint zawiera biblioteki
niezbędne aplikacjom GNOME do drukowania.

%package devel
Summary:	Include files for libgnomeprint
Summary(pl.UTF-8):	Pliki nagłówkowe libgnomeprint
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.14.1
Requires:	libart_lgpl-devel >= 2.3.19
Requires:	libxml2-devel >= 1:2.6.30
Requires:	pango-devel >= 1:1.18.3

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

%description devel -l pl.UTF-8
Pliki nagłówkowe niezbędne do kompilacji aplikacji używających
biblioteki drukowania GNOME.

%package static
Summary:	Static libgnomeprint library
Summary(pl.UTF-8):	Statyczna biblioteka libgnomeprint
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static version of libgnomeprint library.

%description static -l pl.UTF-8
Statyczna wersja biblioteki libgnomeprint.

%package apidocs
Summary:	libgnomeprint API documentation
Summary(pl.UTF-8):	Dokumentacja API libgnomeprint
Group:		Documentation
Requires:	gtk-doc-common
BuildArch:	noarch

%description apidocs
libgnomeprint API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API libgnomeprint.

%package cups
Summary:	CUPS module for libgnomeprint
Summary(pl.UTF-8):	Moduł CUPS dla libgnomeprint
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	cups >= 1:1.1.20
Requires:	libgnomecups >= 0.2.2

%description cups
CUPS module for libgnomeprint.

%description cups -l pl.UTF-8
Moduł CUPS dla libgnomeprint.

%package papi
Summary:	PAPI module for libgnomeprint
Summary(pl.UTF-8):	Moduł PAPI dla libgnomeprint
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libgnomecups >= 0.2.2
Requires:	papi

%description papi
PAPI module for libgnomeprint.

%description papi -l pl.UTF-8
Moduł PAPI dla libgnomeprint.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
CPPFLAGS="%{rpmcppflags}%{?with_papi: -I/usr/include/papi}"
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-font-install \
	--enable-gtk-doc%{!?with_apidocs:=no} \
	--with-cups \
	--with-html-dir=%{_gtkdocdir} \
	%{!?with_papi:--without-papi}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/gnome/libgnomeprint-2.0/fonts

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	pkgconfigdir=%{_pkgconfigdir} \
	HTML_DIR=%{_gtkdocdir}

# no static modules and *.la files - shut up check-files
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/*/modules/{*.{a,la},transports/*.{a,la},filters/*.{a,la}}

%find_lang %{name}-2.2

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}-2.2.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_libdir}/libgnomeprint-2-2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgnomeprint-2-2.so.0
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/%{version}
%dir %{_libdir}/%{name}/%{version}/modules
%dir %{_libdir}/%{name}/%{version}/modules/filters
%dir %{_libdir}/%{name}/%{version}/modules/transports
%attr(755,root,root) %{_libdir}/%{name}/%{version}/modules/filters/libgnomeprint-clip.so
%attr(755,root,root) %{_libdir}/%{name}/%{version}/modules/filters/libgnomeprint-draft.so
%attr(755,root,root) %{_libdir}/%{name}/%{version}/modules/filters/libgnomeprint-frgba.so
%attr(755,root,root) %{_libdir}/%{name}/%{version}/modules/filters/libgnomeprint-multipage.so
%attr(755,root,root) %{_libdir}/%{name}/%{version}/modules/filters/libgnomeprint-position.so
%attr(755,root,root) %{_libdir}/%{name}/%{version}/modules/filters/libgnomeprint-reorder.so
%attr(755,root,root) %{_libdir}/%{name}/%{version}/modules/filters/libgnomeprint-reverse.so
%attr(755,root,root) %{_libdir}/%{name}/%{version}/modules/filters/libgnomeprint-rotate.so
%attr(755,root,root) %{_libdir}/%{name}/%{version}/modules/filters/libgnomeprint-select.so
%attr(755,root,root) %{_libdir}/%{name}/%{version}/modules/filters/libgnomeprint-zoom.so
%attr(755,root,root) %{_libdir}/%{name}/%{version}/modules/transports/libgnomeprint-custom.so
%attr(755,root,root) %{_libdir}/%{name}/%{version}/modules/transports/libgnomeprint-file.so
%attr(755,root,root) %{_libdir}/%{name}/%{version}/modules/transports/libgnomeprint-lpr.so
%attr(755,root,root) %{_libdir}/%{name}/%{version}/modules/libgnomeprintlpd.so
%{_datadir}/libgnomeprint
# for now it's the only package that uses /etc/gnome
%dir %{_sysconfdir}/gnome
%dir %{_sysconfdir}/gnome/libgnomeprint-2.0
%dir %{_sysconfdir}/gnome/libgnomeprint-2.0/fonts

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libgnomeprint
%endif

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgnomeprint-2-2.so
%{_libdir}/libgnomeprint-2-2.la
%{_includedir}/libgnomeprint-2.2
%{_pkgconfigdir}/libgnomeprint-2.2.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libgnomeprint-2-2.a

%files cups
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/%{version}/modules/libgnomeprintcups.so

%files papi
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/%{version}/modules/libgnomeprintpapi.so
