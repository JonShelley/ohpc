#----------------------------------------------------------------------------bh-
# This RPM .spec file is part of the Performance Peak project.
#
# It may have been modified from the default version supplied by the underlying
# release package (if available) in order to apply patches, perform customized
# build/install configurations, and supply additional files to support
# desired integration conventions.
#
#----------------------------------------------------------------------------eh-

# MVAPICH2 MPI stack that is dependent on compiler toolchain

%define with_slurm 0
%define with_psm 0

#-fsp-header-comp-begin----------------------------------------------

# FSP convention: the default assumes the gnu compiler family;
# however, this can be overridden by specifing the compiler_family
# variable via rpmbuild or other mechanisms.

%{!?compiler_family: %define compiler_family gnu}
%{!?PROJ_DELIM:      %define PROJ_DELIM   %{nil}}

# Compiler dependencies
BuildRequires: lmod%{PROJ_DELIM}
%if %{compiler_family} == gnu
BuildRequires: gnu-compilers%{PROJ_DELIM}
Requires:      gnu-compilers%{PROJ_DELIM}
%endif
%if %{compiler_family} == intel
BuildRequires: gcc-c++ intel-compilers-devel%{PROJ_DELIM}
Requires:      gcc-c++ intel-compilers-devel%{PROJ_DELIM}
%if 0%{FSP_BUILD}
BuildRequires: intel_licenses
%endif
%endif

#-fsp-header-comp-end------------------------------------------------

%if 0%{with_slurm}
BuildRequires: slurm-devel%{PROJ_DELIM} slurm%{PROJ_DELIM}
%endif

%if %{with_psm}
BuildRequires:  infinipath-psm infinipath-psm-devel
%endif

%include %{_sourcedir}/FSP_macros

# Base package name
%define pname mvapich2

Summary:   OSU MVAPICH2 MPI implementation
Name:      %{pname}-%{compiler_family}%{PROJ_DELIM}
Version:   2.1
Release:   1
License:   BSD
Group:     fsp/mpi-families
URL:       http://mvapich.cse.ohio-state.edu/overview/mvapich2/
DocDir:    %{FSP_PUB}/doc/contrib
Source0:   %{pname}-%{version}.tar.gz
Source1:   FSP_macros
Source2:   FSP_setup_compiler
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%define debug_package %{nil}

%if 0%{?sles_version} || 0%{?suse_version}
Buildrequires: ofed 
%endif
%if 0%{?rhel_version} || 0%{?centos_version}
Buildrequires: rdma
%endif

Requires: prun%{PROJ_DELIM}

BuildRequires: bison
BuildRequires: libibmad-devel libibverbs-devel

# Default library install path
%define install_path %{FSP_MPI_STACKS}/%{name}/%version

%description 

MVAPICH2 is a high performance MPI-2 implementation (with initial
support for MPI-3) for InfiniBand, 10GigE/iWARP and RoCE.  MVAPICH2
provides underlying support for several interfaces (such as OFA-IB,
OFA-iWARP, OFA-RoCE, PSM, Shared Memory, and TCP) for portability
across multiple networks.

%prep

%setup -q -n %{pname}-%{version}

%build

# FSP compiler designation
export FSP_COMPILER_FAMILY=%{compiler_family}
. %{_sourcedir}/FSP_setup_compiler

./configure --prefix=%{install_path} \
	    --enable-cxx \
	    --enable-g=dbg \
            --with-device=ch3:mrail \
%if %{with_psm}
            --with-device=ch3:psm \
%endif
%if 0%{with_slurm}
            --with-pm=no --with-pmi=slurm \
%endif
	    --enable-fast=O3 || cat config.log

%install

# FSP compiler designation
export FSP_COMPILER_FAMILY=%{compiler_family}
. %{_sourcedir}/FSP_setup_compiler

#make %{?_smp_mflags} DESTDIR=$RPM_BUILD_ROOT install

# 06/04/15 - karl.w.schulz@intel.com; run serial build for fortran deps
make DESTDIR=$RPM_BUILD_ROOT install

# Remove .la files detected by rpm

rm $RPM_BUILD_ROOT/%{install_path}/lib/*.la


# FSP module file
%{__mkdir_p} %{buildroot}/%{FSP_MODULEDEPS}/%{compiler_family}/%{pname}
%{__cat} << EOF > %{buildroot}/%{FSP_MODULEDEPS}/%{compiler_family}/%{pname}/%{version}
#%Module1.0#####################################################################

proc ModulesHelp { } {

puts stderr " "
puts stderr "This module loads the %{pname} library built with the %{compiler_family} toolchain."
puts stderr "\nVersion %{version}\n"

}
module-whatis "Name: %{pname} built with %{compiler_family} toolchain"
module-whatis "Version: %{version}"
module-whatis "Category: runtime library"
module-whatis "Description: %{summary}"
module-whatis "URL: %{url}"

set     version			    %{version}

prepend-path    PATH                %{install_path}/bin
prepend-path    MANPATH             %{install_path}/man
prepend-path	LD_LIBRARY_PATH	    %{install_path}/lib
prepend-path    MODULEPATH          %{FSP_MODULEDEPS}/%{compiler_family}-%{pname}
prepend-path    MPI_DIR             %{install_path}
prepend-path    PKG_CONFIG_PATH     %{install_path}/lib/pkgconfig

family "MPI"
EOF

%{__cat} << EOF > %{buildroot}/%{FSP_MODULEDEPS}/%{compiler_family}/%{pname}/.version.%{version}
#%Module1.0#####################################################################
##
## version file for %{pname}-%{version}
##
set     ModulesVersion      "%{version}"
EOF

%{__mkdir_p} ${RPM_BUILD_ROOT}/%{_docdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig || exit 1

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{FSP_HOME}
%doc README.envvar
%doc COPYRIGHT
%doc CHANGELOG
%doc CHANGES
%doc README


%changelog
* Tue Aug  5 2014  <karl.w.schulz@intel.com> - 
- Initial build.

