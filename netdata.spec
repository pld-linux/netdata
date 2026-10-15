#
# Conditional build:
%bcond_without	cups		# CUPS plugin
%bcond_without	freeipmi	# freeipmi plugin
%bcond_without	go		# Go plugins (go.d, scripts.d, nd-mcp)
%bcond_without	mongodb		# MongoDB exporter
%bcond_without	nfacct		# nfacct plugin
%bcond_without	xenstat		# xenstat plugin

%define		sqlite_src_ver	3530400

Summary:	Linux real time performance monitoring
Summary(pl.UTF-8):	Monitorowanie wydajności Linuksa w czasie rzeczywistym
Name:		netdata
Version:	2.12.1
Release:	0.1
License:	GPL v3+
Group:		Applications/System
#Source0Download: https://github.com/netdata/netdata/releases
Source0:	https://github.com/netdata/netdata/releases/download/v%{version}/%{name}-v%{version}.tar.gz
# Source0-md5:	45331671be9cdf4eb02f29da14884c7e
# vendored Go modules; regenerate with:
#  cd %%{name}-v%%{version}
#  for d in src/go src/collectors/cgroups.plugin/cgroup-name src/web/mcp/bridges/stdio-golang; do (cd $d && go mod vendor); done
#  tar cJf ../%%{name}-vendor-%%{version}.tar.xz src/go/vendor src/web/mcp/bridges/stdio-golang/vendor
Source1:	%{name}-vendor-%{version}.tar.xz
# Source1-md5:	233b147f970ef182ccc521001dccc7c1
# only ext/recover is used, it is not part of libsqlite3
Source2:	https://www.sqlite.org/2026/sqlite-src-%{sqlite_src_ver}.zip
# Source2-md5:	718613520b678b8754427ed2b01d12d3
Source3:	%{name}.conf
Source4:	%{name}.init
Patch0:		%{name}-system-libs.patch
URL:		https://www.netdata.cloud/
BuildRequires:	cmake >= 3.16.0
%{?with_cups:BuildRequires:	cups-devel}
BuildRequires:	curl-devel >= 7.21
%{?with_freeipmi:BuildRequires:	freeipmi-devel}
%{?with_go:BuildRequires:	golang >= 1.27}
BuildRequires:	json-c-devel >= 0.14
BuildRequires:	judy-devel
BuildRequires:	libbacktrace-devel
BuildRequires:	libbrotli-devel
BuildRequires:	libcap-devel
BuildRequires:	libmnl-devel
%{?with_nfacct:BuildRequires:	libnetfilter_acct-devel}
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	libuuid-devel
BuildRequires:	libuv-devel
BuildRequires:	lm_sensors-devel
BuildRequires:	lz4-devel >= 1.7.1
%{?with_mongodb:BuildRequires:	mongo-c-driver-devel >= 1.7}
BuildRequires:	ninja
BuildRequires:	openssl-devel
BuildRequires:	pcre2-8-devel
BuildRequires:	pkgconfig
BuildRequires:	protobuf
BuildRequires:	protobuf-devel
BuildRequires:	rpmbuild(macros) >= 1.742
BuildRequires:	snappy-devel
BuildRequires:	sqlite3-devel
BuildRequires:	systemd-devel
BuildRequires:	unzip
%{?with_xenstat:BuildRequires:	xen-devel}
BuildRequires:	yaml-devel
BuildRequires:	zlib-devel
BuildRequires:	zstd-devel
Provides:	group(netdata)
Provides:	user(netdata)
Requires(post,preun):	/sbin/chkconfig
Requires(post,preun,postun):	systemd-units >= 38
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	rc-scripts
Requires:	systemd-units >= 38
Suggests:	%{name}-charts
%{?with_go:Suggests:	%{name}-go}
Suggests:	%{name}-python
Obsoletes:	netdata-nodejs < 2
%{?with_go:ExclusiveArch:	%go_arches}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
netdata is the fastest way to visualize metrics. It is a resource
efficient, highly optimized system for collecting and visualizing any
type of realtime timeseries data, from CPU usage, disk activity, SQL
queries, API calls, web site visitors, etc.

netdata tries to visualize the truth of now, in its greatest detail,
so that you can get insights of what is happening now and what just
happened, on your systems and applications.

%description -l pl.UTF-8
netdata to najszybszy sposób wizualizacji metryk. Jest to wydajny pod
względem zużycia zasobów, znacząco zoptymalizowany system do zbierania
i wizualizacji dowolnego rodzaju danych zbieranych w linii czasu
rzeczywistego - np. wykorzystania CPU, aktywności dysku, zapytań SQL,
wywołań API, odwiedzających stronę WWW.

%package charts
Summary:	netdata charts plugin
Summary(pl.UTF-8):	Wtyczka do wykresów dla netdata
Group:		Applications/System
URL:		https://learn.netdata.cloud/docs/collecting-metrics/
Requires:	%{name} = %{version}-%{release}
Requires:	bash >= 4
BuildArch:	noarch

%description charts
Charts.d is BaSH script that allows you to write simple scripts for
collecting data.

It has been designed so that the actual script that will do data
collection will be permanently in memory, collecting data with as
little overheads as possible (i.e. initialize once, repeatedly collect
values with minimal overhead).

Charts.d looks for scripts in charts.d. The scripts should have the
filename suffix: .chart.sh.

%description charts -l pl.UTF-8
Charts.d to skrypt Basha pozwalający na pisanie prostych skryptów do
zbierania danych.

Jest zaprojektowany tak, że właściwy skrypt zbierający dane jest
trzymany cały czas w pamięci, zbierając dane z możliwie małym narzutem
(z pojedynczą inicjacją, regularnie zbierając wartości).

Charts.d wyszukuje skrypty w katalogu charts.d. Skrypty powinny mieć
rozszerzenie nazwy pliku: .chart.sh.

%package cups
Summary:	netdata CUPS plugin
Summary(pl.UTF-8):	Wtyczka CUPS dla netdata
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}

%description cups
netdata plugin collecting metrics from CUPS print server.

%description cups -l pl.UTF-8
Wtyczka netdata zbierająca metryki z serwera wydruku CUPS.

%package freeipmi
Summary:	netdata FreeIPMI plugin
Summary(pl.UTF-8):	Wtyczka FreeIPMI dla netdata
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}

%description freeipmi
netdata plugin collecting IPMI sensor metrics using FreeIPMI.

%description freeipmi -l pl.UTF-8
Wtyczka netdata zbierająca metryki czujników IPMI przy użyciu
FreeIPMI.

%package go
Summary:	netdata Go plugins
Summary(pl.UTF-8):	Wtyczki netdata napisane w Go
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}

%description go
go.d.plugin and scripts.d.plugin for netdata - data collectors
written in Go for a large number of applications and services.

%description go -l pl.UTF-8
go.d.plugin i scripts.d.plugin dla netdata - moduły zbierające dane
napisane w Go dla dużej liczby aplikacji i usług.

%package nfacct
Summary:	netdata nfacct plugin
Summary(pl.UTF-8):	Wtyczka nfacct dla netdata
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}

%description nfacct
netdata plugin collecting netfilter accounting and conntrack metrics.

%description nfacct -l pl.UTF-8
Wtyczka netdata zbierająca metryki rozliczania netfiltra i conntracka.

%package python
Summary:	netdata Python plugins
Summary(pl.UTF-8):	Wtyczki Pythona dla netdata
Group:		Applications/System
URL:		https://learn.netdata.cloud/docs/collecting-metrics/
Requires:	%{name} = %{version}-%{release}
Requires:	python3
BuildArch:	noarch

%description python
Netdata Python plugins.

%description python -l pl.UTF-8
Wtyczki Pythona dla netdata.

%package xenstat
Summary:	netdata xenstat plugin
Summary(pl.UTF-8):	Wtyczka xenstat dla netdata
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}

%description xenstat
netdata plugin collecting metrics from the Xen hypervisor.

%description xenstat -l pl.UTF-8
Wtyczka netdata zbierająca metryki z hipernadzorcy Xen.

%prep
%setup -q -n %{name}-v%{version} -a1 -a2
%patch -P0 -p1

%build
export GOCACHE=$(pwd)/.go-cache
export GOFLAGS="-mod=vendor -trimpath"
export GOTOOLCHAIN=local
export GOPROXY=off
%{?__jobs:export GOMAXPROCS=%{__jobs}}
# the local dashboard is closed source and downloaded at build time;
# ML needs dlib, which is not packaged; OTEL/NetFlow need vendored Rust crates;
# eBPF downloads prebuilt BPF objects and a libbpf fork
%cmake -B build -G Ninja \
	-DCMAKE_INSTALL_PREFIX=/ \
	-DENABLE_BUNDLED_JSONC=OFF \
	-DENABLE_BUNDLED_PROTOBUF=OFF \
	-DENABLE_BUNDLED_YAML=OFF \
	-DENABLE_DASHBOARD=OFF \
	-DENABLE_DBENGINE=ON \
	%{cmake_on_off mongodb ENABLE_EXPORTER_MONGODB} \
	-DENABLE_EXPORTER_PROMETHEUS_REMOTE_WRITE=ON \
	-DENABLE_JEMALLOC=OFF \
	-DENABLE_LIBBACKTRACE=ON \
	-DENABLE_MIMALLOC=OFF \
	-DENABLE_ML=OFF \
	-DENABLE_NETDATA_JOURNAL_FILE_READER=OFF \
	-DENABLE_PLUGIN_APPS=ON \
	-DENABLE_PLUGIN_CGROUP_NETWORK=ON \
	-DENABLE_PLUGIN_CHARTS=ON \
	%{cmake_on_off cups ENABLE_PLUGIN_CUPS} \
	-DENABLE_PLUGIN_DEBUGFS=ON \
	-DENABLE_PLUGIN_EBPF=OFF \
	%{cmake_on_off freeipmi ENABLE_PLUGIN_FREEIPMI} \
	%{cmake_on_off go ENABLE_PLUGIN_GO} \
	%{cmake_on_off go ENABLE_ND_MCP} \
	%{cmake_on_off go ENABLE_PLUGIN_SCRIPTS} \
	%{cmake_on_off go ENABLE_CGROUP_NAME} \
	-DENABLE_PLUGIN_IBM=OFF \
	-DENABLE_PLUGIN_LOCAL_LISTENERS=ON \
	-DENABLE_PLUGIN_NETFLOW=OFF \
	-DENABLE_PLUGIN_NETWORK_VIEWER=ON \
	%{cmake_on_off nfacct ENABLE_PLUGIN_NFACCT} \
	-DENABLE_PLUGIN_OTEL=OFF \
	-DENABLE_PLUGIN_PERF=ON \
	-DENABLE_PLUGIN_PYTHON=ON \
	-DENABLE_PLUGIN_SLABINFO=ON \
	-DENABLE_PLUGIN_STATSD=OFF \
	-DENABLE_PLUGIN_SYSTEMD_JOURNAL=ON \
	-DENABLE_PLUGIN_SYSTEMD_UNITS=ON \
	%{cmake_on_off xenstat ENABLE_PLUGIN_XENSTAT} \
	-DENABLE_SENTRY=OFF \
	-DENABLE_WEBRTC=OFF \
	-DNETDATA_SQLITE_RECOVER_SOURCE_DIR=$(pwd)/sqlite-src-%{sqlite_src_ver}/ext/recover \
	-DUSE_MOLD=OFF

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT
export GOCACHE=$(pwd)/.go-cache
export GOFLAGS="-mod=vendor -trimpath"
export GOTOOLCHAIN=local
export GOPROXY=off
%{?__jobs:export GOMAXPROCS=%{__jobs}}
%ninja_install -C build

%{__sed} -i -e '1s,^#!/usr/bin/env bash$,#!/bin/bash,' -e '1s,^#!/usr/bin/env sh$,#!/bin/sh,' \
	$RPM_BUILD_ROOT%{_sysconfdir}/%{name}/edit-config \
	$RPM_BUILD_ROOT%{_libexecdir}/%{name}/plugins.d/{alarm-notify.sh,anonymous-statistics.sh,cgroup-network-helper.sh,charts.d.dryrun-helper.sh,charts.d.plugin,get-kubernetes-labels.sh,ioping.plugin,python.d.plugin,system-info.sh,tc-qos-helper.sh}

install -d $RPM_BUILD_ROOT{/etc/{rc.d/init.d,systemd},%{systemdunitdir},%{systemdtmpfilesdir}}
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/%{name}.conf
install -p %{SOURCE4} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
cp -p build/system/systemd/netdata.service $RPM_BUILD_ROOT%{systemdunitdir}/%{name}.service
%{__sed} -e 's,^d /run/,d /var/run/,' build/system/systemd/tmpfiles/netdata.conf > $RPM_BUILD_ROOT%{systemdtmpfilesdir}/%{name}.conf
# LogNamespace=netdata in netdata.service
cp -p system/systemd/journald@netdata.conf $RPM_BUILD_ROOT/etc/systemd/journald@netdata.conf

# self-updater, uninstaller and service files for other init systems
%{__rm} $RPM_BUILD_ROOT%{_libexecdir}/%{name}/{install-service.sh,netdata-updater.sh}
%{__rm} $RPM_BUILD_ROOT%{_prefix}/lib/%{name}/conf.d/netdata-updater.conf
%{__rm} -r $RPM_BUILD_ROOT%{_prefix}/lib/%{name}/system

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 329 netdata
%useradd -u 329 -g netdata -c netdata -s /sbin/nologin -d / netdata

%post
/sbin/chkconfig --add netdata
%service netdata restart
%systemd_post netdata.service

%preun
if [ "$1" = "0" ]; then
	%service -q netdata stop
	/sbin/chkconfig --del netdata
fi
%systemd_preun netdata.service

%postun
if [ "$1" = "0" ]; then
	%userremove netdata
	%groupremove netdata
fi
%systemd_reload

%files
%defattr(644,root,root,755)
%doc README.md
%dir %{_sysconfdir}/%{name}
%attr(755,root,root) %{_sysconfdir}/%{name}/edit-config
%{_sysconfdir}/%{name}/.install-type
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/netdata.conf
%dir %{_sysconfdir}/%{name}/custom-plugins.d
%dir %{_sysconfdir}/%{name}/health.d
%dir %{_sysconfdir}/%{name}/ssl
%dir %{_sysconfdir}/%{name}/statsd.d
%config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/systemd/journald@netdata.conf
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%{systemdunitdir}/%{name}.service
%{systemdtmpfilesdir}/%{name}.conf
%attr(755,root,root) %{_sbindir}/log2journal
%attr(755,root,root) %{_sbindir}/nd-run
%attr(755,root,root) %{_sbindir}/netdata
%attr(755,root,root) %{_sbindir}/netdata-claim.sh
%attr(755,root,root) %{_sbindir}/netdata-support-bundle
%attr(755,root,root) %{_sbindir}/netdatacli
%attr(755,root,root) %{_sbindir}/systemd-cat-native
%dir %{_prefix}/lib/%{name}
%dir %{_prefix}/lib/%{name}/conf.d
%{_prefix}/lib/%{name}/conf.d/apps_groups.conf
%{_prefix}/lib/%{name}/conf.d/exporting.conf
%{_prefix}/lib/%{name}/conf.d/health_alarm_notify.conf
%{_prefix}/lib/%{name}/conf.d/health_email_recipients.conf
%{_prefix}/lib/%{name}/conf.d/ioping.conf
%{_prefix}/lib/%{name}/conf.d/netdata.conf
%{_prefix}/lib/%{name}/conf.d/sensors3.conf
%{_prefix}/lib/%{name}/conf.d/stream.conf
%{_prefix}/lib/%{name}/conf.d/health.d
%{_prefix}/lib/%{name}/conf.d/log2journal.d
%{_prefix}/lib/%{name}/conf.d/schema.d
%{_prefix}/lib/%{name}/conf.d/statsd.d
%{_prefix}/lib/%{name}/conf.d/vnodes
%dir %{_libexecdir}/%{name}
%dir %{_libexecdir}/%{name}/plugins.d
%attr(755,root,root) %{_libexecdir}/%{name}/plugins.d/alarm-notify.sh
%attr(755,root,root) %{_libexecdir}/%{name}/plugins.d/anonymous-statistics.sh
%attr(755,root,root) %{_libexecdir}/%{name}/plugins.d/cgroup-network-helper.sh
%attr(755,root,root) %{_libexecdir}/%{name}/plugins.d/get-kubernetes-labels.sh
%attr(755,root,root) %{_libexecdir}/%{name}/plugins.d/ioping.plugin
%{_libexecdir}/%{name}/plugins.d/loopsleepms.sh.inc
%attr(755,root,root) %{_libexecdir}/%{name}/plugins.d/system-info.sh
%attr(755,root,root) %{_libexecdir}/%{name}/plugins.d/systemd-units.plugin
%attr(755,root,root) %{_libexecdir}/%{name}/plugins.d/tc-qos-helper.sh
%if %{with go}
%attr(755,root,root) %{_libexecdir}/%{name}/plugins.d/cgroup-name
%endif
# setns() into cgroups and running cgroup-network-helper.sh as root
%attr(4750,root,netdata) %{_libexecdir}/%{name}/plugins.d/cgroup-network
# finding processes listening on local sockets
%attr(4750,root,netdata) %{_libexecdir}/%{name}/plugins.d/local-listeners
# running a fixed set of privileged commands for collectors
%attr(4750,root,netdata) %{_libexecdir}/%{name}/plugins.d/ndsudo
%caps(cap_dac_read_search,cap_sys_ptrace=ep) %attr(750,root,netdata) %{_libexecdir}/%{name}/plugins.d/apps.plugin
%caps(cap_dac_read_search,cap_audit_control=ep) %attr(750,root,netdata) %{_libexecdir}/%{name}/plugins.d/debugfs.plugin
%caps(cap_sys_admin,cap_sys_ptrace,cap_dac_read_search=ep) %attr(750,root,netdata) %{_libexecdir}/%{name}/plugins.d/network-viewer.plugin
%caps(cap_perfmon=ep) %attr(750,root,netdata) %{_libexecdir}/%{name}/plugins.d/perf.plugin
%caps(cap_dac_read_search=ep) %attr(750,root,netdata) %{_libexecdir}/%{name}/plugins.d/slabinfo.plugin
%caps(cap_dac_read_search=ep) %attr(750,root,netdata) %{_libexecdir}/%{name}/plugins.d/systemd-journal.plugin
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/build-info-cmake-cache.gz
%{_datadir}/%{name}/web
%attr(770,netdata,netdata) %dir /var/cache/%{name}
%attr(770,netdata,netdata) %dir /var/lib/%{name}
%attr(770,netdata,netdata) %dir /var/lib/%{name}/cloud.d
%attr(770,netdata,netdata) %dir /var/lib/%{name}/registry
%attr(755,netdata,root) %dir /var/log/%{name}
%attr(775,root,netdata) %dir /var/run/%{name}

%files charts
%defattr(644,root,root,755)
%dir %{_sysconfdir}/%{name}/charts.d
%{_prefix}/lib/%{name}/conf.d/charts.d.conf
%{_prefix}/lib/%{name}/conf.d/charts.d
%attr(755,root,root) %{_libexecdir}/%{name}/plugins.d/charts.d.dryrun-helper.sh
%attr(755,root,root) %{_libexecdir}/%{name}/plugins.d/charts.d.plugin
%dir %{_libexecdir}/%{name}/charts.d
%attr(755,root,root) %{_libexecdir}/%{name}/charts.d/*.chart.sh

%if %{with cups}
%files cups
%defattr(644,root,root,755)
%attr(755,root,root) %{_libexecdir}/%{name}/plugins.d/cups.plugin
%endif

%if %{with freeipmi}
%files freeipmi
%defattr(644,root,root,755)
%attr(4750,root,netdata) %{_libexecdir}/%{name}/plugins.d/freeipmi.plugin
%endif

%if %{with go}
%files go
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/nd-mcp
%dir %{_sysconfdir}/%{name}/go.d
%{_prefix}/lib/%{name}/conf.d/go.d.conf
%{_prefix}/lib/%{name}/conf.d/go.d
%{_prefix}/lib/%{name}/conf.d/scripts.d.conf
%{_prefix}/lib/%{name}/conf.d/scripts.d
# CAP_NET_ADMIN for WireGuard, CAP_NET_RAW for ping, CAP_NET_BIND_SERVICE for SNMP traps on UDP/162
%caps(cap_dac_read_search,cap_net_admin,cap_net_raw,cap_net_bind_service=eip) %attr(750,root,netdata) %{_libexecdir}/%{name}/plugins.d/go.d.plugin
%attr(755,root,root) %{_libexecdir}/%{name}/plugins.d/scripts.d.plugin
%attr(755,root,root) %{_libexecdir}/%{name}/plugins.d/snmp-trap-profile-gen
%endif

%if %{with nfacct}
%files nfacct
%defattr(644,root,root,755)
%attr(4750,root,netdata) %{_libexecdir}/%{name}/plugins.d/nfacct.plugin
%endif

%files python
%defattr(644,root,root,755)
%dir %{_sysconfdir}/%{name}/python.d
%{_prefix}/lib/%{name}/conf.d/python.d.conf
%{_prefix}/lib/%{name}/conf.d/python.d
%attr(755,root,root) %{_libexecdir}/%{name}/plugins.d/python.d.plugin
%dir %{_libexecdir}/%{name}/python.d
%attr(755,root,root) %{_libexecdir}/%{name}/python.d/*.chart.py
# XXX system packages
%{_libexecdir}/%{name}/python.d/python_modules

%if %{with xenstat}
%files xenstat
%defattr(644,root,root,755)
%attr(4750,root,netdata) %{_libexecdir}/%{name}/plugins.d/xenstat.plugin
%endif
