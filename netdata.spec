#
# Conditional build:
%bcond_without	systemd		# systemd
%bcond_with	nfacct		# build with nfacct plugin

Summary:	Linux real time system monitoring, over the web
Name:		netdata
Version:	1.0.0
Release:	0.4
License:	GPL v3+
Group:		Applications/System
Source0:	https://github.com/firehol/netdata/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	53a432f8849da6bd49b0853dd79551c5
Source1:	%{name}.conf
URL:		http://netdata.firehol.org/
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_nfacct:BuildRequires:	libmnl-devel}
%{?with_nfacct:BuildRequires:	libnetfilter_acct-devel}
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.202
BuildRequires:	zlib-devel
Provides:	group(netdata)
Provides:	user(netdata)
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
netdata is the fastest way to visualize metrics. It is a resource
efficient, highly optimized system for collecting and visualizing any
type of realtime timeseries data, from CPU usage, disk activity, SQL
queries, API calls, web site visitors, etc.

netdata tries to visualize the truth of now, in its greatest detail,
so that you can get insights of what is happening now and what just
happened, on your systems and applications.

%prep
%setup -q

%build
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-zlib \
	--with-math \
	%{__enable_disable nfacct plugin-nfacct} \
	--with-user=netdata
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/%{name}.conf

%{__rm} $RPM_BUILD_ROOT/var/{cache,log}/netdata/.keep

install -d $RPM_BUILD_ROOT%{systemdunitdir}
cp -p system/netdata-systemd $RPM_BUILD_ROOT%{systemdunitdir}/netdata.service

%pre
%groupadd -g 329 netdata
%useradd -u 329 -g netdata -c netdata -s /sbin/nologin -d / netdata

%postun
if [ "$1" = "0" ]; then
	%userremove netdata
	%groupremove netdata
fi

%if 0
%post
%systemd_post netdata.service

%preun
%systemd_preun netdata.service

%postun
%systemd_postun_with_restart netdata.service
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/*.conf
%attr(755,root,root) %{_sbindir}/%{name}
%{_datadir}/%{name}
%dir %{_libexecdir}/%{name}
%{systemdunitdir}/netdata.service
%attr(755,netdata,netdata) %dir %{_localstatedir}/cache/%{name}
%attr(755,netdata,netdata) %dir %{_localstatedir}/log/%{name}

%defattr(-,root,root,-)
%{_libexecdir}/%{name}/charts.d
%{_libexecdir}/%{name}/node.d
%{_libexecdir}/%{name}/plugins.d
