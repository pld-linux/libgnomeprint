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
Summary(pl):	Biblioteka drukowania dla GNOME
Name:		libgnomeprint
Version:	1.110.0
Release:	1
License:	LGPL
Group:		Libraries
Group(cs):	Knihovny
Group(da):	Biblioteker
Group(de):	Bibliotheken
Group(es):	Bibliotecas
Group(fr):	Librairies
Group(is):	Agerasˆfn
Group(it):	Librerie
Group(ja):	•È•§•÷•È•Í
Group(no):	Biblioteker
Group(pl):	Biblioteki
Group(pt):	Bibliotecas
Group(pt_BR):	Bibliotecas
Group(ru):	‚…¬Ã…œ‘≈À…
Group(sl):	Knjiænice
Group(sv):	Bibliotek
Group(uk):	‚¶¬Ã¶œ‘≈À…
Source0:	ftp://ftp.gnome.org/pub/gnome/pre-gnome2/sources/%{name}/%{name}-%{version}.tar.bz2
# Bug fix patches
# remove libexec breakage
#Patch3:	%{name}-1.105.0.90-libexec.patch
URL:		http://www.gnome.org/
PreReq:		ghostscript-fonts-std
PreReq:		libxml
PreReq:		perl
PreReq:		XFree86
PreReq:		/sbin/ldconfig
BuildRequires:	glib2-devel >= %{glib2_version}
BuildRequires:	libxml2-devel >= %{libxml2_version}
BuildRequires:	libart_lgpl-devel >= %{libart_lgpl_version}
BuildRequires:	libbonobo-devel >= %{libbonobo_version}
BuildRequires:	freetype >= %{freetype_version}
BuildRequires:	automake
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
dla uøytkownika aplikacji i narzÍdzi do uøytku w po≥±czeniu z zarz±dc±
okien X Window System. Pakiet libgnomeprint zawiera biblioteki
niezbÍdne aplikacjom GNOME do drukowania.

%package devel
Summary:	Include files for libgnomeprint
Summary(pl):	Pliki nag≥Ûwkowe libgnomeprint
Group:		Development/Libraries
Group(cs):	V˝vojovÈ prost¯edky/Knihovny
Group(da):	Udvikling/Biblioteker
Group(de):	Entwicklung/Bibliotheken
Group(es):	Desarrollo/Bibliotecas
Group(fr):	Development/Librairies
Group(is):	ﬁrÛunartÛl/Agerasˆfn
Group(it):	Sviluppo/Librerie
Group(ja):	≥´»Ø/•È•§•÷•È•Í
Group(no):	Utvikling/Bibliotek
Group(pl):	Programowanie/Biblioteki
Group(pt_BR):	Desenvolvimento/Bibliotecas
Group(pt):	Desenvolvimento/Bibliotecas
Group(ru):	Ú¡⁄“¡¬œ‘À¡/‚…¬Ã…œ‘≈À…
Group(sl):	Razvoj/Knjiænice
Group(sv):	Utveckling/Bibliotek
Group(uk):	Úœ⁄“œ¬À¡/‚¶¬Ã¶œ‘≈À…
Requires:	%{name} = %{version}
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

%description devel -l pl
Pliki nag≥Ûwkowe niezbÍdne do kompilacji aplikacji uøywaj±cych
biblioteki drukowania GNOME.

%package static
Summary:	Static libgnomeprint library
Summary(pl):	Statyczna biblioteka libgnomeprint
Group:		Development/Libraries
Group(cs):	V˝vojovÈ prost¯edky/Knihovny
Group(da):	Udvikling/Biblioteker
Group(de):	Entwicklung/Bibliotheken
Group(es):	Desarrollo/Bibliotecas
Group(fr):	Development/Librairies
Group(is):	ﬁrÛunartÛl/Agerasˆfn
Group(it):	Sviluppo/Librerie
Group(ja):	≥´»Ø/•È•§•÷•È•Í
Group(no):	Utvikling/Bibliotek
Group(pl):	Programowanie/Biblioteki
Group(pt_BR):	Desenvolvimento/Bibliotecas
Group(pt):	Desenvolvimento/Bibliotecas
Group(ru):	Ú¡⁄“¡¬œ‘À¡/‚…¬Ã…œ‘≈À…
Group(sl):	Razvoj/Knjiænice
Group(sv):	Utveckling/Bibliotek
Group(uk):	Úœ⁄“œ¬À¡/‚¶¬Ã¶œ‘≈À…
Requires:	%{name}-devel = %{version}

%description static
Static version of libgnomeprint library.

%description static -l pl
Statyczna wersja biblioteki libgnomeprint.

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

gzip -9nf AUTHORS ChangeLog NEWS README installer/README.*

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
       %{_fontsdir}/Type1
/sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS.gz ChangeLog.gz NEWS.gz README.gz installer/README.*.gz
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
%{_includedir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
