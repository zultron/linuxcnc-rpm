# disable realtime varieties here
%global _without_posix 0
%global _without_rt_preempt 0
%global _without_xenomai 0
%global _without_xenomai_kernel 0
# disabling until we have a reasonable RTAI kernel
%global _without_rtai_kernel 1

# list kernel package versions here
%global xenomai_kpkg_version 3.5.7-6.xenomai.el6
%global rtai_kpkg_version 2.6.38.8-5.el6.rtai

# quicker build with no docs
%global _without_docs 1

# pre-release settings
%global _gitrel    20130905git05ed2b1
%global _pre       ubc3

# threading system settings
%if %{_without_posix}
%global configure_args_posix --without-posix
%endif

%if %{_without_rt_preempt}
%global configure_args_rt_preempt --without-rt-preempt
%endif

%if %{_without_xenomai}
%global configure_args_xenomai --without-xenomai
%global _with_xenomai 1
%endif

%if %{_without_xenomai_kernel}
%global configure_args_xenomai_kernel --without-xenomai-kernel
%else
# The wildcard is a hack to include the 'buildid' component in
# xenomai_kver, not present in the pkg version but present in $(uname
# -r).  See https://github.com/zultron/kernel-xenomai-rpm/issues/1
%define xenomai_kver %(basename \\\
	%{_usrsrc}/kernels/%{xenomai_kpkg_version}*.%{_target_cpu})
%global configure_args_xenomai_kernel \\\
	--with-xenomai-kernel-sources=%{_usrsrc}/kernels/%{xenomai_kver}
%global _with_xenomai 1
%endif

%if %{_without_rtai_kernel}
%global configure_args_rtai_kernel --without-rtai-kernel
%else
# Same wildcard hack.
%define rtai_kver %(basename \\\
	%{_usrsrc}/kernels/%{rtai_kpkg_version}*.%{_target_cpu})
%global configure_args_rtai_kernel \\\
	--with-rtai-kernel-sources=%{_usrsrc}/kernels/%{rtai_kver}
%endif


Name:           linuxcnc
Version:        2.6.0
Release:        0.5%{?_pre:.%{_pre}}%{?dist}
Summary:        A software system for computer control of machine tools

License:        GPLv2
Group:          Applications/Engineering
URL:            http://www.linuxcnc.org
Source0:        %{name}-%{version}%{?_gitrel:.%{_gitrel}}.tar.bz2

BuildRequires:  gcc-c++
BuildRequires:  gtk2-devel
BuildRequires:  libgnomeprintui22-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libGLU-devel
BuildRequires:  tcl-devel
BuildRequires:  tk-devel
BuildRequires:  bwidget
BuildRequires:  libXaw-devel
BuildRequires:  python-mtTkinter
BuildRequires:  boost-devel
BuildRequires:  pth-devel
BuildRequires:  libmodbus-devel
BuildRequires:  blt-devel
BuildRequires:  readline-devel
BuildRequires:  gettext
BuildRequires:  python-devel
BuildRequires:  python-lxml
BuildRequires:	libudev-devel
# for building docs
%if ! %{_without_docs}
BuildRequires:  lyx
BuildRequires:  source-highlight
BuildRequires:  ImageMagick
BuildRequires:  dvipng
BuildRequires:  dblatex
BuildRequires:  asciidoc >= 8.5
%endif
#
# Flavor-specific BRs
#
# All Xenomai flavors need library headers
%if 0%{?_with_xenomai}
BuildRequires:  xenomai-devel
%endif
# Xenomai kthreads need kernel headers
%if ! %{_without_xenomai_kernel}
BuildRequires:  kernel-xenomai-devel == %{xenomai_kpkg_version}
%endif
#
# RTAI kthreads need kernel and library headers
%if ! %{_without_rtai_kernel}
BuildRequires:	kernel-rtai-devel == %{rtai_kpkg_version}
BuildRequires:  rtai-devel
%endif

Requires:       bwidget
Requires:       blt
Requires:       python-mtTkinter


%description

LinuxCNC (the Enhanced Machine Control) is a software system for
computer control of machine tools such as milling machines and lathes.

This version is from Michael Haberler's preview that integrates RTAI,
RT_PREEMPT, Xenomai-kernel, Xenomai-User and Simulator


%package devel
Group: Development/Libraries
Summary: Devel package for %{name}
Requires: %{name} = %{version}

%description devel
Development headers and libs for the %{name} package

%package doc
Group:          Documentation
Summary:        Documentation for %{name}

%description doc

Documentation files for the %{name} package


%if ! %{_without_posix}
%package	flavor-posix
Summary:	LinuxCNC modules for the POSIX flavor
Provides:	linuxcnc-flavor
Provides:	linuxcnc-flavor-posix
Requires:	linuxcnc == %{version}

%description	flavor-posix

This package provides the RT modules for the LinuxCNC POSIX flavor.

This flavor has no RT capabilities and is for simulation and non-RT
applications only.  It requires no special kernel.

%endif

%if ! %{_without_rt_preempt}
%package	flavor-rt-preempt
Summary:	LinuxCNC modules for the RT_PREEMPT flavor
Provides:	linuxcnc-flavor
Provides:	linuxcnc-flavor-rt-preempt
Requires:	linuxcnc == %{version}
Requires:	kernel-rt

%description	flavor-rt-preempt

This package provides the RT modules for the LinuxCNC RT_PREEMPT flavor.

It requires a kernel with the RT_PREEMPT patch.

%endif

%if ! %{_without_xenomai}
%package	flavor-xenomai
Summary:	LinuxCNC modules for the Xenomai flavor
Provides:	linuxcnc-flavor
Provides:	linuxcnc-flavor-xenomai
Requires:	linuxcnc == %{version}
Requires:	kernel-xenomai
Requires:	xenomai

%description	flavor-xenomai

This package provides the RT modules for the LinuxCNC Xenomai flavor.

It requires a kernel with the Xenomai patch.

%endif

%if ! %{_without_xenomai_kernel}
%package	flavor-xenomai-kernel
Summary:	LinuxCNC modules for the Xenomai kernel threads flavor
Provides:	linuxcnc-flavor
Provides:	linuxcnc-flavor-xenomai-kernel
Requires:	linuxcnc == %{version}
Requires:	kernel-xenomai == %{xenomai_kpkg_version}
Requires:	xenomai

%description	flavor-xenomai-kernel

This package provides the RT kernel modules for the LinuxCNC Xenomai
kernel-threads flavor.

It requires the Xenomai kernel package, version %{xenomai_kpkg_version}.

%endif

%if ! %{_without_rtai_kernel}
%package	flavor-rtai-kernel
Summary:	LinuxCNC modules for the RTAI kernel threads flavor
Provides:	linuxcnc-flavor
Provides:	linuxcnc-flavor-rtai-kernel
Requires:	linuxcnc == %{version}
Requires:	kernel-rtai == %{rtai_kpkg_version}
Requires:	rtai

%description	flavor-rtai-kernel

This package provides the RT kernel modules for the LinuxCNC RTAI
kernel-threads flavor.

It requires the RTAI kernel package, version %{rtai_kpkg_version}.

%endif


%prep
%setup -q


%build
cd src
./autogen.sh
%configure \
    %{?configure_args_posix} \
    %{?configure_args_rt_preempt} \
    %{?configure_args_xenomai} \
    %{?configure_args_xenomai_kernel} \
    %{?configure_args_rtai_kernel} \
%if ! 0%{_without_docs}
    --enable-build-documentation \
%endif
    --with-tkConfig=%{_libdir}/tkConfig.sh \
    --with-tclConfig=%{_libdir}/tclConfig.sh
make %{?_smp_mflags} V=1


%install
rm -rf $RPM_BUILD_ROOT
cd src
make -e install DESTDIR=$RPM_BUILD_ROOT \
     DIR='install -d -m 0755' FILE='install -m 0644' \
     EXE='install -m 0755' SETUID='install -m 0755'
# put the docs in the right place
mv $RPM_BUILD_ROOT/usr/share/doc/linuxcnc \
   $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
# put X11 app-defaults where the rest of them live
mv $RPM_BUILD_ROOT%{_sysconfdir}/X11 $RPM_BUILD_ROOT%{_datadir}/

# Set the module(s) to be executable, so that they will be stripped
# when packaged.
find %{buildroot} -type f -name \*.ko -exec %{__chmod} u+x \{\} \;

%files
%defattr(-,root,root)
%{_sysconfdir}/linuxcnc
%{_datadir}/X11/app-defaults/*
# /usr/bin/linuxcnc_module_helper must be setuid root; others not
%if 0%{?kversion_hardcoded:1}
%attr(04755,-,-) %{_bindir}/linuxcnc_module_helper
%endif # _without_xenomai_kernel
%attr(0755,-,-) %{_bindir}/[0-9a-km-z]*
%attr(0755,-,-) %{_bindir}/linuxcnc
%attr(0755,-,-) %{_bindir}/linuxcnc[a-z]*
%attr(0755,-,-) %{_bindir}/latency*
%{python_sitearch}/*
%{_exec_prefix}/lib/tcltk/linuxcnc
%attr(0775,-,-) %{_libdir}/*.so*
%attr(0775,-,-) %{_libexecdir}/linuxcnc/flavor
%attr(0775,-,-) %{_libexecdir}/linuxcnc/inivar
%attr(0775,-,-) %{_libexecdir}/linuxcnc/linuxcnc_module_helper
%attr(0775,-,-) %{_libexecdir}/linuxcnc/pci_read
%attr(0775,-,-) %{_libexecdir}/linuxcnc/pci_write
%attr(0775,-,-) %{_libexecdir}/linuxcnc/rtapi_msgd
%{_datadir}/axis
%{_datadir}/glade3
%{_datadir}/gtksourceview-2.0
%{_datadir}/linuxcnc
%{_datadir}/gscreen
%lang(de) %{_datadir}/locale/de/LC_MESSAGES/linuxcnc.mo
%lang(es) %{_datadir}/locale/es/LC_MESSAGES/linuxcnc.mo
%lang(fi) %{_datadir}/locale/fi/LC_MESSAGES/linuxcnc.mo
%lang(fr) %{_datadir}/locale/fr/LC_MESSAGES/linuxcnc.mo
%lang(hu) %{_datadir}/locale/hu/LC_MESSAGES/linuxcnc.mo
%lang(it) %{_datadir}/locale/it/LC_MESSAGES/linuxcnc.mo
%lang(ja) %{_datadir}/locale/ja/LC_MESSAGES/linuxcnc.mo
%lang(pl) %{_datadir}/locale/pl/LC_MESSAGES/linuxcnc.mo
%lang(pt_BR) %{_datadir}/locale/pt_BR/LC_MESSAGES/linuxcnc.mo
%lang(ro) %{_datadir}/locale/ro/LC_MESSAGES/linuxcnc.mo
%lang(ru) %{_datadir}/locale/ru/LC_MESSAGES/linuxcnc.mo
%lang(sk) %{_datadir}/locale/sk/LC_MESSAGES/linuxcnc.mo
%lang(sr) %{_datadir}/locale/sr/LC_MESSAGES/linuxcnc.mo
%lang(sv) %{_datadir}/locale/sv/LC_MESSAGES/linuxcnc.mo
%lang(zh_CN) %{_datadir}/locale/zh_CN/LC_MESSAGES/linuxcnc.mo
%lang(zh_HK) %{_datadir}/locale/zh_HK/LC_MESSAGES/linuxcnc.mo
%lang(zh_TW) %{_datadir}/locale/zh_TW/LC_MESSAGES/linuxcnc.mo
%doc %{_mandir}/man[19]/*

%files devel
%defattr(-,root,root)
%{_includedir}/linuxcnc
%{_libdir}/liblinuxcnc.a
%doc %{_mandir}/man3/*

%files doc
%defattr(-,root,root)
%{_docdir}/%{name}-%{version}

%if ! %{_without_posix}
%files	flavor-posix
%attr(0755,-,-) %{_libexecdir}/linuxcnc/rtapi_app_posix
%{_libdir}/linuxcnc/posix
%{_libdir}/linuxcnc/ulapi-posix.so
%endif

%if ! %{_without_rt_preempt}
%files	flavor-rt-preempt
%attr(0755,-,-) %{_libexecdir}/linuxcnc/rtapi_app_rt-preempt
%{_libdir}/linuxcnc/rt-preempt
%{_libdir}/linuxcnc/ulapi-rt-preempt.so
%endif

%if ! %{_without_xenomai}
%files	flavor-xenomai
%attr(0755,-,-) %{_libexecdir}/linuxcnc/rtapi_app_xenomai
%{_libdir}/linuxcnc/xenomai
%{_libdir}/linuxcnc/ulapi-xenomai.so
%endif

%if ! %{_without_xenomai_kernel}
%files	flavor-xenomai-kernel
/lib/modules/%{xenomai_kver}
%{_libdir}/linuxcnc/ulapi-xenomai-kernel.so
%endif

%if ! %{_without_rtai_kernel}
%files	flavor-rtai-kernel
/lib/modules/%{rtai_ksrc}
%{_libdir}/linuxcnc/ulapi-rtai-kernel.so
%endif


%changelog
* Thu Sep  5 2013 John Morris <john@zultron.com> - 2.6.0-0.5.ubc3
- Update to 2.6.0-20130905git05ed2b1
- Refactor for Universal Build (universal-build-candidate-3)
- Build all flavors by default, with one kernel source per kthread flavor
- Break out flavor binaries into subpackages
- Disable RTAI build until we have RTAI packages
- Refactor macro system

* Mon Nov 12 2012 John Morris <john@zultron.com> - 2.6.0-0.4.pre0
- Update to 2.6.0-20121112gite024e61
-   Fix for Xenomai recommended kernel option
- Add preempt-rt support
- Generalize kernel package/version logic for various threads systems
  - Each thread system-specific section defines some config variables
  - Resulting logic is much simpler and easier to read
- Fix incorrect %defattr statements
- Bump xenomai kversion release
- Add thread system info in release tag
- Base kernel package version on -devel pkg, not kernel package
- Remove BR: kernel; should only need kernel-devel

* Fri Nov  9 2012 John Morris <john@zultron.com> - 2.6.0-0.3.pre0
- Update to 2.6.0-20121109git894f2cf
-   Fixes to compiler math options for xenomai
-   Fixes to kernel module symbol sharing
- Enable verbose builds
- Option to disable building docs for a quick build
- linuxcnc-module-helper setuid root
- rpmlint cleanups:  tabs, perms

* Mon Nov  6 2012 John Morris <john@zultron.com> - 2.6.0-0.2.pre0
- Update to Haberler's 2.6.0.pre0-20121106git98e9566 with
  multiple RT systems support
- Add configuration code for xenomai, based on Zultron kernel-xenomai RPM
- Update %%files section for xenomai and LinuxCNC updates
- BR formatting

* Sun May  6 2012  <john@zultron.com> - 2.6.0-0.1.pre0
- Updated to newest git:
  - Forward-port of Michael Buesch's patches
  - Fixes to the hal stacksize, no more crash!
  - Install shared libs mode 0755 for /usr/lib/rpm/rpmdeps

* Wed Apr 25 2012  <john@zultron.com> - 2.5.0.1-1
- Initial RPM version
