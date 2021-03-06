#
# spec file for package libconfuse0
#
# Copyright (c) 2011 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

%include %{_sourcedir}/FSP_macros
%{!?PROJ_DELIM:      %define PROJ_DELIM      %{nil}}

Name:           libconfuse0
Version:        2.7
Release:        1
License:        LGPL-2.1+
Group:          Development/Libraries/C and C++
DocDir:         %{FSP_PUB}/doc/contrib
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  gcc-c++ gettext-devel libtool pkgconfig
%if 0%{?suse_version} > 1020
BuildRequires:  check-devel
Recommends:     %{name}-lang
%else
BuildRequires:  check
%endif
%define pkg_name confuse
%define debug_package %{nil}
#
URL:            http://www.nongnu.org/confuse/
# taken from    http://download.savannah.gnu.org/releases/confuse/%{pkg_name}-%{version}.tar.gz
Source:         %{pkg_name}-%{version}.tar.gz
#
Summary:        A configuration file parser library

%description
libConfuse is a configuration file parser library, licensed under the
terms of the LGPL, and written in C. It supports sections and (lists
of) values (strings, integers, floats, booleans or other sections), as
well as some other features (such as single/double-quoted strings,
environment variable expansion, functions and nested include
statements). It makes it very easy to add configuration file capability
to a program using a simple API.

The goal of libConfuse is not to be the configuration file parser
library with a gazillion of features. Instead, it aims to be easy to
use and quick to integrate with your code. libConfuse was called libcfg
before, but was changed to not confuse with other similar libraries.

%package -n libconfuse-devel
Group:          Development/Libraries/C and C++
Requires:       %{name} = %{version}
Summary:        The development files for libconfuse

%description -n libconfuse-devel
libConfuse is a configuration file parser library, licensed under the
terms of the LGPL, and written in C. It supports sections and (lists
of) values (strings, integers, floats, booleans or other sections), as
well as some other features (such as single/double-quoted strings,
environment variable expansion, functions and nested include
statements). It makes it very easy to add configuration file capability
to a program using a simple API.

The goal of libConfuse is not to be the configuration file parser
library with a gazillion of features. Instead, it aims to be easy to
use and quick to integrate with your code. libConfuse was called libcfg
before, but was changed to not confuse with other similar libraries.

This package holds the development files for libconfuse.

%lang_package
%prep
%setup -q -n %{pkg_name}-%{version}

%build
autoreconf -fi
%configure --enable-shared --disable-static
%{__make} %{?_smp_mflags}

%install
%makeinstall
%find_lang %{pkg_name}
%{__install} -Dd %{buildroot}%{_mandir}
%{__cp} -Rv doc/man/man3/ %{buildroot}%{_mandir}
# clean up examples
%{__make} -C examples clean
rm -rf examples/.deps/ examples/Makefile*
%{__mkdir_p} ${RPM_BUILD_ROOT}/%{_docdir}

%post   -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/libconfuse.so.0.0.0
%{_libdir}/libconfuse.so.0

%files -n libconfuse-devel
%defattr(-,root,root,-)
%{_libdir}/libconfuse.so
%{_libdir}/libconfuse.la
%{_libdir}/pkgconfig/libconfuse.pc
%{_includedir}/confuse.h
%{_mandir}/man3/*.3*
%{_datadir}/
%doc NEWS
%doc README
%doc AUTHORS
%doc doc/html/ doc/tutorial-html/ examples/
%{FSP_PUB}
%{FSP_HOME}


%changelog
