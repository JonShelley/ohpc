#----------------------------------------------------------------------------bh-
# This RPM .spec file is part of the Performance Peak project.
#
# It may have been modified from the default version supplied by the underlying
# release package (if available) in order to apply patches, perform customized
# build/install configurations, and supply additional files to support
# desired integration conventions.
#
#----------------------------------------------------------------------------eh-


#-fsp-header-comp-begin----------------------------------------------

%include %{_sourcedir}/FSP_macros

# FSP convention: the default assumes the gnu toolchain and openmpi
# MPI family; however, these can be overridden by specifing the
# compiler_family and mpi_family variables via rpmbuild or other
# mechanisms.

%{!?compiler_family: %define compiler_family gnu}
%{!?mpi_family:      %define mpi_family openmpi}
%{!?PROJ_DELIM:      %define PROJ_DELIM %{nil}}

# Compiler dependencies 

# Note: this package is slightly non-standard in that we always use
# gnu compilers undernead in order to support call-site demangling

BuildRequires: lmod%{PROJ_DELIM}
BuildRequires: gnu-compilers%{PROJ_DELIM}
Requires:      gnu-compilers%{PROJ_DELIM}

# MPI dependencies
%if %{mpi_family} == impi
BuildRequires: intel-mpi-devel%{PROJ_DELIM}
Requires:      intel-mpi-devel%{PROJ_DELIM}
%endif
%if %{mpi_family} == mvapich2
BuildRequires: mvapich2-gnu%{PROJ_DELIM}
Requires:      mvapich2-gnu%{PROJ_DELIM}
%endif
%if %{mpi_family} == openmpi
BuildRequires: openmpi-gnu%{PROJ_DELIM}
Requires:      openmpi-gnu%{PROJ_DELIM}
%endif

#-fsp-header-comp-end------------------------------------------------

# Base package name
%define pname mpiP
%define PNAME %(echo %{pname} | tr [a-z] [A-Z])

Summary:   mpiP: a lightweight profiling library for MPI applications.
Name:      %{pname}-%{compiler_family}-%{mpi_family}%{PROJ_DELIM}
Version:   3.4.1
Release:   1
License:   GPLv2+
Group:     fsp/perf-tools
URL:       http://mpip.sourceforge.net/
Source0:   %{pname}-%{version}.tar.gz
Source1:   FSP_macros
Source2:   FSP_setup_compiler
Source3:   FSP_setup_mpi
BuildRoot: %{_tmppath}/%{pname}-%{version}-%{release}-root
DocDir:    %{FSP_PUB}/doc/contrib

BuildRequires: binutils-devel
BuildRequires: python

%define debug_package %{nil}

# Default library install path
%define install_path %{FSP_LIBS}/%{compiler_family}/%{mpi_family}/%{pname}/%version

%description 

mpiP is a lightweight profiling library for MPI applications. Because
it only collects statistical information about MPI functions, mpiP
generates considerably less overhead and much less data than tracing
tools. All the information captured by mpiP is task-local. It only
uses communication during report generation, typically at the end of
the experiment, to merge results from all of the tasks into one output
file.

%prep

%setup -q -n %{pname}-%{version}

%build

# FSP compiler/mpi designation

# note: in order to support call-site demangling, we compile mpiP with gnu
export FSP_COMPILER_FAMILY=gnu
export FSP_MPI_FAMILY=%{mpi_family}
. %{_sourcedir}/FSP_setup_compiler
. %{_sourcedir}/FSP_setup_mpi

CC=mpicc
CXX=mpicxx
FC=mpif90



./configure --prefix=%{install_path} --enable-demangling --disable-libunwind || cat config.log

%install

# FSP compiler designation

# note: in order to support call-site demangling, we compile mpiP with gnu
export FSP_COMPILER_FAMILY=gnu
export FSP_MPI_FAMILY=%{mpi_family}
. %{_sourcedir}/FSP_setup_compiler
. %{_sourcedir}/FSP_setup_mpi

make %{?_smp_mflags} 
make DESTDIR=$RPM_BUILD_ROOT install

# FSP module file
%{__mkdir} -p %{buildroot}%{FSP_MODULEDEPS}/%{compiler_family}-%{mpi_family}/%{pname}
%{__cat} << EOF > %{buildroot}/%{FSP_MODULEDEPS}/%{compiler_family}-%{mpi_family}/%{pname}/%{version}
#%Module1.0#####################################################################

proc ModulesHelp { } {

puts stderr " "
puts stderr "This module loads the %{pname} library built with the %{compiler_family} compiler"
puts stderr "toolchain and the %{mpi_family} MPI stack."
puts stderr "\nVersion %{version}\n"

}
module-whatis "Name: %{pname} built with %{compiler_family} compiler and %{mpi_family} MPI"
module-whatis "Version: %{version}"
module-whatis "Category: Profiling library"
module-whatis "Description: %{summary}"
module-whatis "URL %{url}"

set     version			    %{version}

prepend-path	LD_LIBRARY_PATH	    %{install_path}/lib

setenv          %{PNAME}_DIR        %{install_path}
setenv          %{PNAME}_LIB        %{install_path}/lib

EOF

%{__cat} << EOF > %{buildroot}/%{FSP_MODULEDEPS}/%{compiler_family}-%{mpi_family}/%{pname}/.version.%{version}
#%Module1.0#####################################################################
##
## version file for %{pname}-%{version}
##
set     ModulesVersion      "%{version}"
EOF

%{__mkdir} -p $RPM_BUILD_ROOT/%{_docdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{FSP_HOME}
%{FSP_PUB}
%doc ChangeLog doc/PORTING.txt doc/README doc/UserGuide.txt
