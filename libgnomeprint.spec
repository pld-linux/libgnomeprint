## this could go, it's really just so we notice if the soname changes
%define sover 0

%define glib2_base_version 1.3.13
#%define glib2_version %{glib2_base_version}.90
%define glib2_version %{glib2_base_version}
%define libxml2_version 2.4.12
%define libart_lgpl_version 2.3.8
%define libbonobo_version 1.110.0
%define freetype_version 2.0.3

Summary:	Printing library for GNOME
Name:		libgnomeprint
Version:	1.110.0
Release:	1
License:	LGPL
Group:		Libraries
Group(de):	Libraries
Group(es):	Bibliotecas
Group(fr):	Librairies
Group(pl):	Biblioteki
Group(pt_BR):	Bibliotecas
Group(ru):	Библиотеки
Group(uk):	Б╕бл╕отеки
Source0:	ftp://ftp.gnome.org/pub/gnome/pre-gnome2/sources/%{name}/%{name}-%{version}.tar.bz2
# Bug fix patches
# remove libexec breakage
#Patch3:	%{name}-1.105.0.90-libexec.patch
PreReq:		urw-fonts
PreReq:		ghostscript
PreReq:		ghostscript-fonts
PreReq:		libxml
PreReq:		perl
PreReq:		XFree86
PreReq:		libgnomeprint = %{PACKAGE_VERSION}

BuildPrereq:	glib2-devel >= %{glib2_version}
BuildPrereq:	libxml2-devel >= %{libxml2_version}
BuildPrereq:	libart_lgpl-devel >= %{libart_lgpl_version}
BuildPrereq:	libbonobo-devel >= %{libbonobo_version}
BuildPrereq:	freetype >= %{freetype_version}
BuildPrereq:	automake14
URL:		http://www.gnome.org/
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

%package devel
Summary:	Libraries and include files for developing GNOME applications
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(es):	Desarrollo/Bibliotecas
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Group(pt_BR):	Desenvolvimento/Bibliotecas
Group(ru):	Разработка/Библиотеки
Group(uk):	Розробка/Б╕бл╕отеки

Requires:	%{name} = %{PACKAGE_VERSION}
Requires:	libgnomeprint = %{PACKAGE_VERSION}

Requires:	glib2-devel >= %{glib2_version}
Requires:	libxml2-devel >= %{libxml2_version}
Requires:	libart_lgpl-devel >= %{libart_lgpl_version}
Requires:	libbonobo-devel >= %{libbonobo_version}
Requires:	freetype >= %{freetype_version}

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

%prep
%setup -q
#%patch3 -p1 -b .libexec

%build
automake -a -c
%configure \
	--disable-font-install
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install $RPM_BUILD_ROOT%{_sysconfdir}/gnome/fonts

# It would probably be cleaner to use install DESTDIR=$RPM_BUILD_ROOT
# instead of %%makeinstall with this hack.
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	FONTMAPDIR_STATIC=$RPM_BUILD_ROOT%{_datadir}/gnome/libgnomeprint-2.0/fonts

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post 
## we could pass --dynamic here to install to /etc instead
## but I think it makes more sense to have this not be a config 
## file, then people make their changes in /etc if they want
libgnomeprint-2.0-font-install                                          \
       --aliases=%{_datadir}/gnome-print/fonts/adobe-urw.font           \
       --target=%{_sysconfdir}/gnome/fonts/libgnomeprint-rpm.fontmap    \
       --recursive --static                                            \
       %{_datadir}/fonts/default/Type1                                  \
       /usr/X11R6/lib/X11/fonts/Type1

/sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README installer/README.*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%{_libdir}/gnome-print-2.0
%{_libdir}/pkgconfig/*
%{_datadir}/gnome-print-2.0
%{_datadir}/gnome/libgnomeprint-2.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%attr(755,root,root) %{_libdir}/lib*.la
%{_libdir}/*.a
%{_includedir}/*
