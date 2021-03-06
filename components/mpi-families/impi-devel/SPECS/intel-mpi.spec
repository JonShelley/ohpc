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
Name:      intel-mpi-devel%{PROJ_DELIM}
Version:   5.1.0.069
Source0:   intel-impi-devel-fsp-%{version}.tar.gz
Source1:   FSP_macros
Release:   1
License:   Intel
URL:       https://software.intel.com/en-us/intel-mpi-library
Group:     fsp/mpi-families
BuildArch: x86_64
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
AutoReq:   no
#AutoReqProv: no

%include %{_sourcedir}/FSP_macros

%define __spec_install_post /usr/lib/rpm/brp-strip-comment-note /bin/true
%define __spec_install_post /usr/lib/rpm/brp-compress /bin/true
%define __spec_install_post /usr/lib/rpm/brp-strip /bin/true

requires: intel-mpi%{PROJ_DELIM}

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

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{FSP_HOME}

%changelog

