#
# Conditional build:
%bcond_without	freeipmi	# freeipmi plugin
%bcond_without	nfacct		# nfacct plugin

Summary:	Linux real time performance monitoring
Summary(pl.UTF-8):	Monitorowanie wydajności Linuksa w czasie rzeczywistym
Name:		netdata
Version:	1.8.0
Release:	1
License:	GPL v3+
Group:		Applications/System
#Source0Download: https://github.com/firehol/netdata/releases
Source0:	https://github.com/firehol/netdata/releases/download/v%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	4058c3acdda1af5968e7dc636ba322e2
Source1:	%{name}.conf
Source2:	%{name}.init
Patch0:		nodejs.patch
URL:		http://netdata.firehol.org/
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake
%{?with_freeipmi:BuildRequires:	freeipmi-devel}
BuildRequires:	libcap-devel
%{?with_nfacct:BuildRequires:	libmnl-devel}
%{?with_nfacct:BuildRequires:	libnetfilter_acct-devel}
BuildRequires:	libuuid-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.647
BuildRequires:	zlib-devel
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
Suggests:	%{name}-charts
Suggests:	%{name}-nodejs
Suggests:	%{name}-python
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_prefix}/lib

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
URL:		https://github.com/firehol/netdata/wiki/General-Info---charts.d
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

%package nodejs
Summary:	netdata node.js plugins
Summary(pl.UTF-8):	Wtyczki node.js dla netdata
Group:		Applications/System
URL:		https://github.com/firehol/netdata/wiki/General-Info---node.d
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description nodejs
node.d.plugin is a netdata plugin that provides an abstraction layer
to allow easy and quick development of data collectors in node.js. It
also manages all its data collectors (placed in node.d) using a single
instance of node, thus lowering the memory footprint of data
collection.

%description nodejs -l pl.UTF-8
Wtyczka node.d zapewnia warstwę abstrakcji, pozwalającą na łatwe i
szybkie tworzenie modułów zbierających dane w node.js. Zarządza też
wszystkimi modułami zbierającymi dane (umieszczonymi w node.d) przy
użyciu prostej instancji węzła, obniżając narzut pamięciowy zbierania
danych.

%package python
Summary:	netdata Python plugins
Summary(pl.UTF-8):	Wtyczki Pythona dla netdata
Group:		Applications/System
URL:		https://github.com/firehol/netdata/wiki/How-to-write-new-module
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description python
Netdata Python plugins.

%description python -l pl.UTF-8
Wtyczki Pythona dla netdata.

%prep
%setup -q
%patch0 -p1

%build
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--libdir=%{_libexecdir} \
	%{__enable_disable freeipmi plugin-freeipmi} \
	%{__enable_disable nfacct plugin-nfacct} \
	--with-math \
	--with-zlib \
	--with-user=netdata
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT/var/{cache,lib,log}/netdata/.keep
%{__rm} $RPM_BUILD_ROOT/var/lib/netdata/registry/.keep

install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,%{systemdunitdir},%{_localstatedir}/lib/%{name}/registry}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/%{name}.conf
install -p %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
cp -p system/netdata.service $RPM_BUILD_ROOT%{systemdunitdir}/%{name}.service

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
%doc ChangeLog LICENSE.md LICENSE-REDISTRIBUTED.md README.md
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/apps_groups.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/netdata.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/fping.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/health_alarm_notify.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/health_email_recipients.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/stream.conf
%dir %{_sysconfdir}/%{name}/health.d
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/health.d/*.conf
%attr(754,root,root) /etc/rc.d/init.d/netdata
%attr(755,root,root) %{_sbindir}/%{name}
%dir %{_datadir}/%{name}
%dir %{_libexecdir}/%{name}
%{systemdunitdir}/netdata.service
%attr(755,netdata,netdata) %dir %{_localstatedir}/cache/%{name}
%attr(755,netdata,netdata) %dir %{_localstatedir}/log/%{name}
%attr(755,netdata,netdata) %dir %{_localstatedir}/lib/%{name}
%attr(755,netdata,netdata) %dir %{_localstatedir}/lib/%{name}/registry

%defattr(-,root,root,-)
%{_libexecdir}/%{name}/plugins.d
# subpackages
%exclude %{_libexecdir}/%{name}/plugins.d/node.d.plugin
%exclude %{_libexecdir}/%{name}/plugins.d/charts.d*

%defattr(-,root,netdata,-)
%{_datadir}/%{name}/web

%files charts
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/charts.d.conf
%dir %{_sysconfdir}/%{name}/charts.d
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/charts.d/*.conf
%attr(755,root,root) %{_libexecdir}/%{name}/plugins.d/charts.d*
%dir %{_libexecdir}/%{name}/charts.d
%{_libexecdir}/%{name}/charts.d/README.md
%attr(755,root,root) %{_libexecdir}/%{name}/charts.d/*.chart.sh

%files nodejs
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/node.d.conf
%dir %{_sysconfdir}/%{name}/node.d
%attr(755,root,root) %{_libexecdir}/%{name}/plugins.d/node.d.plugin
%dir %{_libexecdir}/%{name}/node.d
%{_libexecdir}/%{name}/node.d/README.md
%{_libexecdir}/%{name}/node.d/node_modules
%attr(755,root,root) %{_libexecdir}/%{name}/node.d/*.node.js

%files python
%defattr(644,root,root,755)
%dir %{_sysconfdir}/%{name}/python.d
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/python.d.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/python.d/*.conf
%dir %{_libexecdir}/%{name}/python.d
%{_libexecdir}/%{name}/python.d/README.md
%attr(755,root,root) %{_libexecdir}/%{name}/python.d/*.chart.py

# XXX system packages
%{_libexecdir}/%{name}/python.d/python-modules-installer.sh
%dir %{_libexecdir}/%{name}/python.d/python_modules
%{_libexecdir}/%{name}/python.d/python_modules/*.py
%{_libexecdir}/%{name}/python.d/python_modules/pyyaml2
%{_libexecdir}/%{name}/python.d/python_modules/pyyaml3
%{_libexecdir}/%{name}/python.d/python_modules/urllib3
