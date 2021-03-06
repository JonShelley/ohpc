#----------------------------------------------------------------------------bh-
# This RPM .spec file is part of the Performance Peak project.
#
# It may have been modified from the default version supplied by the underlying
# release package (if available) in order to apply patches, perform customized
# build/install configurations, and supply additional files to support
# desired integration conventions.
#
#----------------------------------------------------------------------------eh-

%define compiler_family intel
%{!?PROJ_DELIM: %define PROJ_DELIM %{nil}}

Summary:   Intel(R) MPI Library for Linux* OS
Name:      intel-mpi%{PROJ_DELIM}
Version:   5.1.0.069
Source0:   intel-impi-fsp-%{version}.tar.gz
Source1:   FSP_macros
Release:   1
License:   Intel
URL:       https://software.intel.com/en-us/intel-mpi-library
Group:     fsp/mpi-families
BuildArch: x86_64
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
AutoReq:   no
#AutoReqProv: no

Requires:  prun%{PROJ_DELIM}

%define pstudio_ver 2016.0.069

%include %{_sourcedir}/FSP_macros

%define __spec_install_post /usr/lib/rpm/brp-strip-comment-note /bin/true
%define __spec_install_post /usr/lib/rpm/brp-compress /bin/true
%define __spec_install_post /usr/lib/rpm/brp-strip /bin/true

#!BuildIgnore: post-build-checks rpmlint-Factory
%define debug_package %{nil}

%define package_target %{FSP_COMPILERS}/intel

%description

FSP collection of the Intel(R) MPI toolchain.

%prep

%build

%install

%{__mkdir} -p %{buildroot}/
cd %{buildroot}
%{__tar} xfz %{SOURCE0}
cd -

# Create extra bin dir with soft links that can be use to use Intel
# toolchain with standard front-end names like mpicc, mpif90, etc)


%{__mkdir}  %{buildroot}/%{package_target}/compilers_and_libraries_%{pstudio_ver}/linux/mpi/intel64/bin_fsp
cd %{buildroot}/%{package_target}/compilers_and_libraries_%{pstudio_ver}/linux/mpi/intel64/bin_fsp
ln -s ../bin/mpiicc   mpicc
ln -s ../bin/mpiifort mpif90
ln -s ../bin/mpiifort mpif77
ln -s ../bin/mpiicpc  mpicxx

# Intel MPI has support for both the Intel and GNU
# toolchains. Therefore, we create a gnu and intel modulefile here.

# FSP module file for Intel compiler toolchain
%{__mkdir} -p %{buildroot}/%{FSP_MODULEDEPS}/intel/impi
%{__cat} << EOF > %{buildroot}/%{FSP_MODULEDEPS}/intel/impi/%{version}
#%Module1.0#####################################################################
proc ModulesHelp { } {

puts stderr " "
puts stderr "This module loads the Intel MPI environment"
puts stderr " "
puts stderr "mpiifort     (Fortran source)"
puts stderr "mpiicc       (C   source)"
puts stderr "mpiicpc      (C++ source)"
puts stderr " "
puts stderr "Version %{version}"
puts stderr " "

}

module-whatis "Name: Intel MPI"
module-whatis "Version: %{version}"
module-whatis "Category: library, runtime support"
module-whatis "Description: Intel MPI Library (C/C++/Fortran for x86_64)"
module-whatis "URL: http://software.intel.com/en-us/articles/intel-mpi-library/"

set     version                 %{version}

setenv          I_MPI_ROOT      %{package_target}/compilers_and_libraries_%{pstudio_ver}/linux/mpi
setenv          MPI_DIR         %{package_target}/compilers_and_libraries_%{pstudio_ver}/linux/mpi/intel64
prepend-path    PATH            %{package_target}/compilers_and_libraries_%{pstudio_ver}/linux/mpi/intel64/bin
prepend-path    MANPATH         %{package_target}/compilers_and_libraries_%{pstudio_ver}/linux/mpi/man
prepend-path    LD_LIBRARY_PATH %{package_target}/compilers_and_libraries_%{pstudio_ver}/linux/mpi/intel64/lib

prepend-path    MODULEPATH      %{FSP_MODULEDEPS}/intel-impi

# Prefer bin_fsp to allow developers to use standard mpicc, mpif90,
# etc to access Intel toolchain.

prepend-path    PATH            %{package_target}/compilers_and_libraries_%{pstudio_ver}/linux/mpi/intel64/bin_fsp


family "MPI"
EOF

%{__cat} << EOF > %{buildroot}/%{FSP_MODULEDEPS}/intel/impi/.version.%{version}
#%Module1.0#####################################################################
set     ModulesVersion      "%{version}"
EOF

# FSP module file for GNU compiler toolchain
mkdir -p %{buildroot}/%{FSP_MODULEDEPS}/gnu/impi
%{__cat} << EOF > %{buildroot}/%{FSP_MODULEDEPS}/gnu/impi/%{version}
#%Module1.0#####################################################################
proc ModulesHelp { } {

puts stderr " "
puts stderr "This module loads the Intel MPI environment for use with the GNU"
puts stderr "compiler toolchain"
puts stderr " "
puts stderr "mpif90       (Fortran source)"
puts stderr "mpicc        (C   source)"
puts stderr "mpicxx       (C++ source)"
puts stderr " "
puts stderr "Version %{version}"
puts stderr " "

}

module-whatis "Name: Intel MPI"
module-whatis "Version: %{version}"
module-whatis "Category: library, runtime support"
module-whatis "Description: Intel MPI Library (C/C++/Fortran for x86_64)"
module-whatis "URL: http://software.intel.com/en-us/articles/intel-mpi-library/"

set     version                 %{version}

setenv          I_MPI_ROOT      %{package_target}/compilers_and_libraries_%{pstudio_ver}/linux/mpi
prepend-path    PATH            %{package_target}/compilers_and_libraries_%{pstudio_ver}/linux/mpi/intel64/bin
prepend-path    MANPATH         %{package_target}/compilers_and_libraries_%{pstudio_ver}/linux/mpi/man
prepend-path    LD_LIBRARY_PATH %{package_target}/compilers_and_libraries_%{pstudio_ver}/linux/mpi/intel64/lib

prepend-path    MODULEPATH      %{FSP_MODULEDEPS}/gnu-impi

family "MPI"
EOF

%{__cat} << EOF > %{buildroot}/%{FSP_MODULEDEPS}/gnu/impi/.version.%{version}
#%Module1.0#####################################################################
set     ModulesVersion      "%{version}"
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{FSP_HOME}

%changelog

