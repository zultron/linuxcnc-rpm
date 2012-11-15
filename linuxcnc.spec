# select the realtime variety here
%global _with_rtai 0
%global _with_rt_preempt 0
%global _with_xenomai_kernel 1
%global _with_xenomai_user 0
%global _with_simulator 0

# quicker build with no docs
%global _with_docs 0

# pre-release settings
%global _gitrel    20121112gite024e61
%global _pre       0

# threading system settings
%if 0%{?_with_rt_preempt}
%global with_threads --with-threads=rt-preempt-user
%global kernel_pkg kernel-rt
%global reltag rt_preempt
%endif
%if 0%{?_with_xenomai_kernel}
%global with_threads --with-threads=xenomai-kernel
%global kernel_pkg kernel-xenomai
%global reltag xeno_kernel
%global kversion_hardcoded 2.6.38.8-3.el6.xenomai
%global _with_xenomai 1
%endif
%if 0%{?_with_xenomai_user}
%global with_threads --with-threads=xenomai-user
%global kernel_pkg kernel-xenomai
%global reltag xeno_user
%global _with_xenomai 1
%endif
%if 0%{?_with_simulator}
%global with_threads --enable-simulator
%global reltag simulator
%endif

# release configuration
%global _prerel %{?_pre:.pre%{_pre}}%{?_gitrel:.%{_gitrel}}
%global _subrel %{?reltag:.%{reltag}}%{?_prerel}
%global _relsuffix %{_subrel}%{dist}

# kernel version computation
#
# kversion can be passed in from the commandline...
%if 0%{!?kversion:1}
# ...and if not, then discover it
%if 0%{?kversion_hardcoded:1}
# threads systems that build kernel modules need the kernel version
# hardcoded so that mock knows in advance what kernel package to
# install
%define kversion %{kversion_hardcoded}
%else # ! kversion_hardcoded
# threads systems that run in userland can use any installed version
# of the needed RT kernel
%define kversion %(rpm -q --qf='%%{version}-%%{release}\\n' \\\
	%{kernel_pkg}-devel | tail -1)
%endif # kversion_hardcoded
%endif # kversion undefined

# thread system ./configure settings
%define kversion_arch %{kversion}.%{_target_cpu}
%global rt_opts %{with_threads} \\\
        --with-kernel=%{kversion_arch} \\\
        --with-kernel-headers=%{_usrsrc}/kernels/%{kversion_arch}


Name:           linuxcnc
Version:        2.6.0
Release:        0.4%{?_relsuffix}
Summary:        A software system for computer control of machine tools

License:        GPLv2
Group:          Applications/Engineering
URL:            http://www.linuxcnc.org
# git://git.mah.priv.at/emc2-dev.git rtos-integration-preview1 branch
Source0:        %{name}-%{version}%{?_prerel}.tar.bz2

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
# for building docs
BuildRequires:  lyx
BuildRequires:  source-highlight
BuildRequires:  ImageMagick
BuildRequires:  dvipng
BuildRequires:  dblatex
BuildRequires:  asciidoc >= 8.5
#
# any of the following?
#BuildRequires:  dietlibc-devel glibc-static
#
# kernel pkg BRs
%if 0%{?kversion_hardcoded:1}
BuildRequires:  %{kernel_pkg}-devel == %{kversion}
%else
BuildRequires:  %{kernel_pkg}-devel
%endif
#
# thread-specific BRs
%if 0%{?_with_xenomai}
BuildRequires:  xenomai-devel
%endif # _with_xenomai


Requires:       bwidget
Requires:       blt
Requires:       python-mtTkinter
#
# kernel pkg Requires:
%if 0%{?kversion_hardcoded:1}
Requires:       %{kernel_pkg} == %{kversion}
%else
Requires:       %{kernel_pkg}
%endif
#
# thread-specific Requires:
%if 0%{?_with_xenomai}
Requires:       xenomai
%endif # _with_xenomai


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


%prep
%setup -q

%build
cd src
./autogen.sh
%configure  %{rt_opts} \
%if 0%{_with_docs}
            --enable-build-documentation \
%endif
            --with-tkConfig=%{_libdir}/tkConfig.sh \
            --with-tclConfig=%{_libdir}/tclConfig.sh
make %{?_smp_mflags} BUILD_VERBOSE=1

%install
rm -rf $RPM_BUILD_ROOT
cd src
make -e install DESTDIR=$RPM_BUILD_ROOT \
     DIR='install -d -m 0755' FILE='install -m 0644' \
     EXE='install -m 0755' SETUID='install -m 0755'
# put the init file in the right place
mkdir $RPM_BUILD_ROOT/etc/rc.d
mv $RPM_BUILD_ROOT/etc/init.d $RPM_BUILD_ROOT%{_initddir}
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
%attr(0755,-,-) %{_initddir}/realtime
%{_sysconfdir}/linuxcnc
%{_datadir}/X11/app-defaults/*
# /usr/bin/linuxcnc_module_helper must be setuid root; others not
%if 0%{?kversion_hardcoded:1}
%attr(04755,-,-) %{_bindir}/linuxcnc_module_helper
%endif # _with_xenomai_kernel
%attr(0755,-,-) %{_bindir}/[0-9a-km-z]*
%attr(0755,-,-) %{_bindir}/linuxcnc
%attr(0755,-,-) %{_bindir}/linuxcnc[a-z]*
%attr(0755,-,-) %{_bindir}/latency*
/linuxcnc
%{python_sitelib}/*
%{_exec_prefix}/lib/tcltk/linuxcnc
%attr(0775,-,-) %{_libdir}/*.so*
%{_datadir}/axis
%{_datadir}/glade3
%{_datadir}/gtksourceview-2.0
%{_datadir}/linuxcnc
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

%changelog
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
