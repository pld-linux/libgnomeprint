Summary:	Printing library for GNOME
Summary(pl):	Biblioteka drukowania dla GNOME
Name:		libgnomeprint
Version:	1.112.0
Release:	1
License:	LGPL
Group:		Libraries
Source0:	ftp://ftp.gnome.org/pub/gnome/pre-gnome2/sources/%{name}/%{name}-%{version}.tar.bz2
URL:		http://www.gnome.org/
PreReq:		ghostscript-fonts-std
BuildRequires:	glib2-devel >= 2.0.1
BuildRequires:	libxml2-devel >= 2.4.7
BuildRequires:	libart_lgpl-devel
BuildRequires:	libbonobo-devel >= 1.110
BuildRequires:	freetype-devel
BuildRequires:	pango-devel >= 1.0.0
BuildRequires:	automake
BuildRequires:	autoconf
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         _prefix         /usr/X11R6
%define         _mandir         %{_prefix}/man
%define         _sysconfdir     /etc/X11/GNOME2

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
Requires:	libxml2-devel >= 2.4.7
Requires:	libart_lgpl-devel
Requires:	libbonobo-devel

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
libtoolize --copy --force
aclocal
autoconf
automake -a -c -f
%configure \
	--disable-font-install
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/gnome/fonts

# It would probably be cleaner to use install DESTDIR=$RPM_BUILD_ROOT
# instead of %%makeinstall with this hack.
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	FONTMAPDIR_STATIC=%{_datadir}/gnome/libgnomeprint-2.0/fonts

gzip -9nf AUTHORS ChangeLog NEWS README installer/README.*

%find_lang %{name}-2.0

%clean
rm -rf $RPM_BUILD_ROOT

%post
## we could pass --dynamic here to install to /etc instead
## but I think it makes more sense to have this not be a config
## file, then people make their changes in /etc if they want
%{_bindir}/libgnomeprint-2.0-font-install \
       --aliases=%{_datadir}/gnome-print/fonts/adobe-urw.font \
       --target=%{_sysconfdir}/gnome/fonts/libgnomeprint-rpm.fontmap \
       --recursive --static \
       %{_datadir}/fonts/Type1
/sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}-2.0.lang
%defattr(644,root,root,755)
%doc *.gz */*.gz
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%{_libdir}/gnome-print-*
%{_libdir}/pkgconfig/*
%{_datadir}/gnome-print-*
%{_datadir}/gnome/libgnomeprint-*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%attr(755,root,root) %{_libdir}/lib*.la
%{_includedir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
