Summary: 	H2O - The optimized HTTP/1, HTTP/2 server
Name: 		h2o
Version: 	1.4.2
Release: 	1%{?dist}
License: 	MIT
Group:		System Environment/Daemons
Source: 	https://github.com/h2o/h2o/archive/v%{version}.tar.gz
Url: 		https://h2o.github.io/
BuildRoot:  	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	cmake, openssl-devel, gcc-c++
Requires:	perl-Server-Starter, openssl

%if 0%{?fedora} >= 21
BuildRequires: systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
%endif

Source1: 	h2o.conf
Source2: 	index.html
Source3: 	h2o.service

%description
H2O is a very fast HTTP server written in C. It can also be used as a library.

%prep
%setup -q

%build
%cmake -DWITH_BUNDLED_SSL=on .
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

install -p -d -m 0755 %{buildroot}/etc/h2o
install -p -d -m 0755 %{buildroot}/var/log/h2o
install -p -d -m 0755 %{buildroot}/var/www
install -p -d -m 0755 %{buildroot}/var/run/h2o
install -p -d -m 0755 %{buildroot}/etc/systemd/system

install -p -m 0644 %{SOURCE1} %{buildroot}/etc/h2o/h2o.conf
install -p -m 0644 %{SOURCE2} %{buildroot}/var/www/index.html
install -p -m 0644 %{SOURCE3} %{buildroot}/etc/systemd/system/h2o.service

%check
ctest -V %{?_smp_mflags}

%if 0%{?fedora} >= 21
%post
%systemd_post h2o.service

%preun
%systemd_preun h2o.service

%postun
%systemd_postun_with_restart h2o.service
%endif

%files
%defattr(-,root,root)
%config(noreplace) /etc/h2o/h2o.conf
%config(noreplace) /var/www/index.html
%{_bindir}/h2o
/usr/share/h2o/fetch-ocsp-response
/usr/share/h2o/start_server
/etc/systemd/system/h2o.service
%attr(755,nobody,nobody) %dir /var/log/h2o
%attr(755,nobody,nobody) %dir /var/run/h2o
%dir /var/www
%doc /usr/share/doc/h2o
/usr/share/h2o
/usr/include/h2o.h
/usr/include/h2o
/usr/lib/libh2o-evloop.so

%changelog
* Sat Aug 15 2015 Martin Hagstrom <marhag87@gmail.com> 1.4.2-1
- Update to 1.4.2
* Wed May 20 2015 Arnoud Vermeer <a.vermeer@freshway.biz> 1.2.0-1
- new package built with tito
