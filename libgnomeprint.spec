## this could go, it's really just so we notice if the soname changes
%define sover 0

%define glib2_base_version 1.3.13
#%define glib2_version %{glib2_base_version}.90
%define glib2_version %{glib2_base_version}
%define libxml2_version 2.4.12
%define libart_lgpl_version 2.3.8
%define libbonobo_version 1.110.0
%define freetype_version 2.0.3

Summary: Printing library for GNOME.
Name:		libgnomeprint
Version: 	1.110.0
Release:	1
License:	LGPL
Group: System Environment/Base
Source: 	ftp://ftp.gnome.org/pub/GNOME/sources/unstable/%{name}/%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

PreReq:	urw-fonts
PreReq:	ghostscript
PreReq:	ghostscript-fonts
PreReq:	libxml
PreReq: perl
PreReq: XFree86
PreReq: libgnomeprint = %{PACKAGE_VERSION}

BuildPrereq: glib2-devel >= %{glib2_version}
BuildPrereq: libxml2-devel >= %{libxml2_version}
BuildPrereq: libart_lgpl-devel >= %{libart_lgpl_version}
BuildPrereq: libbonobo-devel >= %{libbonobo_version}
BuildPrereq: freetype >= %{freetype_version}
BuildPrereq: automake14


# Bug fix patches
# remove libexec breakage
Patch3: libgnomeprint-1.105.0.90-libexec.patch

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
Summary: Libraries and include files for developing GNOME applications.
Group: Development/Libraries

Requires: %{name} = %{PACKAGE_VERSION}
Requires: libgnomeprint = %{PACKAGE_VERSION}

Requires: glib2-devel >= %{glib2_version}
Requires: libxml2-devel >= %{libxml2_version}
Requires: libart_lgpl-devel >= %{libart_lgpl_version}
Requires: libbonobo-devel >= %{libbonobo_version}
Requires: freetype >= %{freetype_version}

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
%setup -q -n %{name}-%{version}

%patch3 -p1 -b .libexec

%build

## ensure that --nodeps doesn't mess things up (configure.in also
## checks this in theory, but in principle the RPM and configure.in
## could require different versions, and a double check is nice
## anyhow)
if ! pkg-config --atleast-version=%{glib2_base_version} glib-2.0; then 
  echo "glib2-devel does not meet the build requirements"
  exit 1
fi


automake-1.4

%configure --disable-font-install
make

%install
rm -rf $RPM_BUILD_ROOT

# It would probably be cleaner to use install DESTDIR=$RPM_BUILD_ROOT
# instead of %%makeinstall with this hack.
%makeinstall FONTMAPDIR_STATIC=$RPM_BUILD_ROOT/usr/share/gnome/libgnomeprint-2.0/fonts
./mkinstalldirs $RPM_BUILD_ROOT/%{_sysconfdir}/gnome/fonts

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
%defattr(-, root, root)

%doc AUTHORS COPYING ChangeLog NEWS README installer/README.*
%{_bindir}/*
%{_libdir}/gnome-print-2.0
%{_libdir}/pkgconfig/*
%{_libdir}/lib*.so.%{sover}
%{_libdir}/lib*.so.%{sover}.*
%{_datadir}/gnome-print-2.0
%{_datadir}/gnome/libgnomeprint-2.0

%files devel
%defattr(-, root, root)

%{_libdir}/lib*.so
%{_libdir}/*.a
%{_includedir}/*

%changelog
* Wed Jan 30 2002 Owen Taylor <otaylor@redhat.com>
- Version 1.110.0

* Tue Jan 22 2002 Havoc Pennington <hp@redhat.com>
- automake14

* Mon Jan  7 2002 Havoc Pennington <hp@redhat.com>
- 1.109.0.90 snap
- remove .options patch which is upstream
- remove .nofontmaps patch, upstream uses sysconfdir sometimes now
  and has --disable-font-install configure option
- remove .fontmapdir, now fixed upstream

* Tue Nov 27 2001 Havoc Pennington <hp@redhat.com>
- rebuild due to build system fuckup

* Tue Nov 27 2001 Havoc Pennington <hp@redhat.com>
- cvs snap 1.106.0.90, glib 1.3.11

* Sun Oct 28 2001 Havoc Pennington <hp@redhat.com>
- new cvs snap, rebuild for glib 1.3.10, remove bogus gtk dep

* Tue Oct  9 2001 Havoc Pennington <hp@redhat.com>
- remove epoch screwup

* Mon Oct  8 2001 Havoc Pennington <hp@redhat.com>
- libgnomeprint package based on the gnome-print package

* Mon Oct  8 2001 Havoc Pennington <hp@redhat.com>
- use 0.30 tarball

* Sat Sep 22 2001 Havoc Pennington <hp@redhat.com>
- new cvs snap, with headers moved

* Wed Aug 15 2001 Owen Taylor <otaylor@redhat.com>
- Back out freetype change, for now, until we can get it in upstream.
- Move gnome-print/<ver>/profiles back to datadir, and remove the %config.
  Making them %config doesn't seem compatible with locating them
  in gnome-print/<ver>.

* Mon Aug 13 2001 Akira TAGOH <tagoh@redhat.com> 0.29-5
- no replace profiles.

* Mon Aug 13 2001 Akira TAGOH <tagoh@redhat.com> 0.29-4
- Move profiles directory to /etc/gnome-print/<ver>/profiles/

* Mon Aug 13 2001 Akira TAGOH <tagoh@redhat.com> 0.29-3
- Add freetype support patch. (Bug#50360)

* Sat Jul 21 2001 Owen Taylor <otaylor@redhat.com>
- Add missing directory

* Fri Jul 20 2001 Owen Taylor <otaylor@redhat.com>
- Upgrade to 0.29
- Don't install run-gnome-font-install (#48466), run gnome-font-install directly.
- Add BuildPrereq and make -devel package require gdk-pixbuf-devel
- Make libgnomeprint package require gnome-print package; otherwise
  packages requiring libgnomeprint might not get a runtime environment
- Add Prereq on ghostscript, since run-gnome-font-install parses output of 'gs -h'

* Mon Jul 16 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Kill output from run-gnome-font-install
- s/Copyright/License/
- Add post/postun scripts for the libgnomeprint subpackage

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Fri Apr 20 2001 Jonathan Blandford <jrb@redhat.com>
- new version (0.28)

* Thu Mar 01 2001 Owen Taylor <otaylor@redhat.com>
- Rebuild for GTK+-1.2.9 include paths

* Fri Feb 23 2001 Trond Eivind Glomsrød <teg@redhat.com>
- langify
- patch it to compile (didn't include locale.h when needed)
- use %%{_tmppath}

* Fri Feb 23 2001 Akira TAGOH <tagoh@redhat.com>
- Fixed font problem for Japanese.
- Fixed library dependency on VFlib (Bug#28331)

* Wed Feb 21 2001 Philipp Knirsch <pknirsch@redhat.de>
- Fixed bugzilla bug #27417, simple specfile %post fix.

* Sun Feb 18 2001 Akira TAGOH <tagoh@redhat.com>
- Fixed PostScript broken.
- Added autoheader,automake,autoconf stuff.

* Thu Feb 08 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add libtoolize to make porting to new archs easy

* Tue Feb 06 2001 Akira TAGOH <tagoh@redhat.com>
- Updated Japanese patch for Gnumeric.
  Created dummy .afm.

* Mon Feb 05 2001 Akira TAGOH <tagoh@redhat.com>
- Fixed gdk_fontset_load().
- Added Japanese patch for Gnumeric.

* Fri Feb 02 2001 Akira TAGOH <tagoh@redhat.com>
- Added Japanese patch.
  Fixed Print and Preview with Japanese.

* Fri Dec 29 2000 Matt Wilson <msw@redhat.com>
- 0.25

* Sat Aug 19 2000 Preston Brown <pbrown@redhat.com>
- added "|| true" to %%post so that if font-install screws up we don't get a
  bad exit status.  gnome-font-install expects that the directory specified by
  HOME env. var is writable, but it isn't always if you install with 'sudo'
  or the equivalent.  bad. bad. bad.

* Fri Aug 11 2000 Jonathan Blandford <jrb@redhat.com>
- Up Epoch and release

* Fri Jul 14 2000 Matt Wilson <msw@redhat.com>
- redirect %%post script output to /dev/null

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Thu Jun 29 2000 Owen Taylor <otaylor@redhat.com>
- Spec file fixes
