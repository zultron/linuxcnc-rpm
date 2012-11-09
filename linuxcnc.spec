# select the realtime variety here
%global _with_rtai 0
%global _with_rt_preempt 0
%global _with_xenomai_kernel 1
%global _with_xenomai_user 0
%global _with_simulator 0

%global _gitrel    20121109gita0a0322
%global _pre       0
%global _subrel    %{?_pre:.pre%{_pre}}%{?_gitrel:.%{_gitrel}}

%if 0%{?_with_rtai}
%global rt_opts --with-threads=rtai
%endif
%if 0%{?_with_rt_preempt 0}
%global rt_opts --with-threads=rt-preempt-user
%endif
%if 0%{?_with_xenomai_kernel 0}
%global xenomai_type xenomai-kernel
%global _with_xenomai 1
%endif
%if 0%{?_with_xenomai_user 0}
%global xenomai_type xenomai-user
%global _with_xenomai 1
%endif
%if 0%{?_with_simulator 0}
%global rt_opts --enable-simulator
%endif

%if 0%{?_with_xenomai}
# If kversion isn't defined on the rpmbuild line, find the
# version of the newest instelled xenomai kernel
%if ! 0%{?xenomai_kversion}
%global xenomai_kversion 2.6.38.8-2.xenomai.el6
%endif # !?xenomai_kversion
%global rt_opts --with-threads=%{xenomai_type} \\\
	--with-kernel=%{xenomai_kversion}.%{_target_cpu} \\\
	--with-kernel-headers=%{_usrsrc}/kernels/%{xenomai_kversion}.%{_target_cpu}
%endif # ?_with_xenomai


Name:		linuxcnc
Version:	2.6.0
Release:	0.3%{?_subrel}%{?dist}
Summary:	a software system for computer control of machine tools

License:	GPL/LGPL
Group:		Applications/Engineering
URL:		http://www.linuxcnc.org
# git://git.mah.priv.at/emc2-dev.git rtos-integration-preview1 branch
Source0:	%{name}-%{version}%{?_subrel}.tar.bz2

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
BuildRequires:  lyx
BuildRequires:  pth-devel
BuildRequires:  libmodbus-devel
BuildRequires:  blt-devel
BuildRequires:  readline-devel
BuildRequires:  source-highlight
BuildRequires:  ImageMagick
BuildRequires:  dvipng
BuildRequires:  gettext
BuildRequires:  python-devel
BuildRequires:  dblatex
BuildRequires:  asciidoc >= 8.5
BuildRequires:  python-lxml
#
# any of the following?
#BuildRequires:  dietlibc-devel glibc-static

Requires:       bwidget
Requires:       blt

# xenomai 
%if 0%{?_with_xenomai}
BuildRequires:  kernel-xenomai == %{xenomai_kversion}
BuildRequires:  kernel-xenomai-devel
BuildRequires:  xenomai-devel

Requires:  kernel-xenomai == %{xenomai_kversion}
Requires:  xenomai
%else
BuildRequires:  kernel-devel
%endif

%description

LinuxCNC (the Enhanced Machine Control) is a software system for
computer control of machine tools such as milling machines and lathes.

This version is from Michael Haberler's preview that integrates RTAI,
RT_PREEMPT, Xenomai-kernel, Xenomai-User and Simulator

%package devel
Group: Development/Libraries/C and C++
Summary: Devel package for %{name}
Requires: %{name} = %{version}

%description devel
Development headers and libs for the %{name} package

%package doc
Group:		Documentation
Summary:	Documentation for %{name}

%description doc

Documentation files for the %{name} package

%prep
%setup -q

%build
cd src
./autogen.sh
%configure  %{rt_opts} \
	    --with-tkConfig=%{_libdir}/tkConfig.sh \
	    --with-tclConfig=%{_libdir}/tclConfig.sh \
	    --enable-build-documentation
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
%attr(0755,-,-) %{_initddir}/realtime
%{_sysconfdir}/linuxcnc
%config %{_datadir}/X11/app-defaults/*
%{_bindir}/*
/linuxcnc
%{python_sitelib}/*
%{_prefix}/lib/tcltk/linuxcnc
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
%{_includedir}/linuxcnc
%{_libdir}/liblinuxcnc.a
%doc %{_mandir}/man3/*

%files doc
%{_docdir}/%{name}-%{version}

%changelog
* Fri Nov  9 2012 John Morris <john@zultron.com> - 2.6.0-0.3.pre0
- Update to 2.6.0-20121109gita0a0322
-   Fixes to compiler math options for xenomai
- Enable verbose builds

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





