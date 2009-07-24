Summary: High-performance and highly configurable free RADIUS server
Name: freeradius
Version: 2.1.6
Release: 5%{?dist}
License: GPLv2+ and LGPLv2+
Group: System Environment/Daemons
URL: http://www.freeradius.org/

Source0: ftp://ftp.freeradius.org/pub/radius/freeradius-server-%{version}.tar.bz2
Source100: freeradius-radiusd-init
Source102: freeradius-logrotate
Source103: freeradius-pam-conf

Obsoletes: freeradius-dialupadmin >= 2.0 freeradius-dialupadmin-ldap >= 2.0
Obsoletes: freeradius-dialupadmin-mysql >= 2.0 freeradius-dialupadmin-postgresql >= 2.0

%define docdir %{_docdir}/freeradius-%{version}

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: autoconf
BuildRequires: gdbm-devel
BuildRequires: libtool
BuildRequires: libtool-ltdl-devel
BuildRequires: openssl-devel
BuildRequires: pam-devel
BuildRequires: zlib-devel
BuildRequires: net-snmp-devel
BuildRequires: net-snmp-utils
BuildRequires: readline-devel

Requires(pre): shadow-utils glibc-common
Requires(post): /sbin/ldconfig /sbin/chkconfig
Requires(postun): /sbin/ldconfig
Requires(preun): /sbin/chkconfig

%description
The FreeRADIUS Server Project is a high performance and highly configurable 
GPL'd free RADIUS server. The server is similar in some respects to 
Livingston's 2.0 server.  While FreeRADIUS started as a variant of the 
Cistron RADIUS server, they don't share a lot in common any more. It now has 
many more features than Cistron or Livingston, and is much more configurable.

FreeRADIUS is an Internet authentication daemon, which implements the RADIUS 
protocol, as defined in RFC 2865 (and others). It allows Network Access 
Servers (NAS boxes) to perform authentication for dial-up users. There are 
also RADIUS clients available for Web servers, firewalls, Unix logins, and 
more.  Using RADIUS allows authentication and authorization for a network to 
be centralized, and minimizes the amount of re-configuration which has to be 
done when adding or deleting new users.

%package libs
Group: System Environment/Daemons
Summary: FreeRADIUS shared libraries

%description libs
The FreeRADIUS shared library

%package utils
Group: System Environment/Daemons
Summary: FreeRADIUS utilities
Requires: %{name}-libs = %{version}-%{release}

%description utils
The FreeRADIUS server has a number of features found in other servers,
and additional features not found in any other server. Rather than
doing a feature by feature comparison, we will simply list the features
of the server, and let you decide if they satisfy your needs.

Support for RFC and VSA Attributes Additional server configuration
attributes Selecting a particular configuration Authentication methods

%package devel
Group: Development/Libraries
Summary: FreeRADIUS Development Files
Requires: %{name}-libs = %{version}-%{release}

%description devel
These are the static libraries for the FreeRADIUS package.


%package ldap
Summary: LDAP support for freeradius
Group: System Environment/Daemons
Requires: %{name}-libs = %{version}-%{release}
BuildRequires: openldap-devel

%description ldap
This plugin provides the LDAP support for the FreeRADIUS server project.

%package krb5
Summary: Kerberos 5 support for freeradius
Group: System Environment/Daemons
Requires: %{name}-libs = %{version}-%{release}
BuildRequires: krb5-devel

%description krb5
This plugin provides the Kerberos 5 support for the FreeRADIUS server project.

%package perl
Summary: Perl support for freeradius
Group: System Environment/Daemons
Requires: %{name}-libs = %{version}-%{release}
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
%if 0%{?fedora}
BuildRequires: perl-devel
%else
BuildRequires: perl
%endif
BuildRequires: perl(ExtUtils::Embed)

%description perl
This plugin provides the Perl support for the FreeRADIUS server project.

%package python
Summary: Python support for freeradius
Group: System Environment/Daemons
Requires: %{name}-libs = %{version}-%{release}
BuildRequires: python-devel

%description python
This plugin provides the Python support for the FreeRADIUS server project.

%package mysql
Summary: MySQL support for freeradius
Group: System Environment/Daemons
Requires: %{name}-libs = %{version}-%{release}
BuildRequires: mysql-devel

%description mysql
This plugin provides the MySQL support for the FreeRADIUS server project.

%package postgresql
Summary: postgresql support for freeradius
Group: System Environment/Daemons
Requires: %{name}-libs = %{version}-%{release}
BuildRequires: postgresql-devel

%description postgresql
This plugin provides the postgresql support for the FreeRADIUS server project.

%package unixODBC
Summary: unixODBC support for freeradius
Group: System Environment/Daemons
Requires: %{name}-libs = %{version}-%{release}
BuildRequires: unixODBC-devel

%description unixODBC
This plugin provides the unixODBC support for the FreeRADIUS server project.


%prep
%setup -q -n freeradius-server-%{version}

%build
%ifarch s390 s390x
export CFLAGS="$RPM_OPT_FLAGS -fPIC"
%else
export CFLAGS="$RPM_OPT_FLAGS -fpic"
%endif

%configure \
        --libdir=%{_libdir}/freeradius \
        --with-system-libtool \
        --disable-ltdl-install \
        --with-gnu-ld \
        --with-threads \
        --with-thread-pool \
        --with-docdir=%{docdir} \
        --with-rlm-sql_postgresql-include-dir=/usr/include/pgsql \
        --with-rlm-sql-postgresql-lib-dir=%{_libdir} \
        --with-rlm-sql_mysql-include-dir=/usr/include/mysql \
        --with-mysql-lib-dir=%{_libdir}/mysql \
        --with-unixodbc-lib-dir=%{_libdir} \
        --with-rlm-dbm-lib-dir=%{_libdir} \
        --with-rlm-krb5-include-dir=/usr/kerberos/include \
        --without-rlm_eap_ikev2 \
        --without-rlm_sql_iodbc \
        --without-rlm_sql_firebird \
        --without-rlm_sql_db2 \
        --without-rlm_sql_oracle

%if "%{_lib}" == "lib64"
perl -pi -e 's:sys_lib_search_path_spec=.*:sys_lib_search_path_spec="/lib64 /usr/lib64 /usr/local/lib64":' libtool
%endif

make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/var/run/radiusd
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/{logrotate.d,pam.d,rc.d/init.d}
mkdir -p $RPM_BUILD_ROOT/var/lib/radiusd
# fix for bad libtool bug - can not rebuild dependent libs and bins
#FIXME export LD_LIBRARY_PATH=$RPM_BUILD_ROOT/%{_libdir}
make install R=$RPM_BUILD_ROOT
# modify default configuration
RADDB=$RPM_BUILD_ROOT%{_sysconfdir}/raddb
perl -i -pe 's/^#user =.*$/user = radiusd/'   $RADDB/radiusd.conf
perl -i -pe 's/^#group =.*$/group = radiusd/' $RADDB/radiusd.conf
#ldconfig -n $RPM_BUILD_ROOT/usr/lib/freeradius
# logs
mkdir -p $RPM_BUILD_ROOT/var/log/radius/radacct
touch $RPM_BUILD_ROOT/var/log/radius/{radutmp,radius.log}

install -m 755 %{SOURCE100} $RPM_BUILD_ROOT/%{_initrddir}/radiusd
install -m 644 %{SOURCE102} $RPM_BUILD_ROOT/%{_sysconfdir}/logrotate.d/radiusd
install -m 644 %{SOURCE103} $RPM_BUILD_ROOT/%{_sysconfdir}/pam.d/radiusd

# remove unneeded stuff
rm -rf doc/00-OLD
rm -f $RPM_BUILD_ROOT/usr/sbin/rc.radiusd
rm -rf $RPM_BUILD_ROOT/%{_libdir}/freeradius/*.a
rm -rf $RPM_BUILD_ROOT/%{_libdir}/freeradius/*.la
rm -rf $RPM_BUILD_ROOT/%{_sysconfdir}/raddb/sql/mssql
rm -rf $RPM_BUILD_ROOT/%{_sysconfdir}/raddb/sql/oracle
rm -rf $RPM_BUILD_ROOT/%{_datadir}/dialup_admin/sql/oracle
rm -rf $RPM_BUILD_ROOT/%{_datadir}/dialup_admin/lib/sql/oracle
rm -rf $RPM_BUILD_ROOT/%{_datadir}/dialup_admin/lib/sql/drivers/oracle

# remove unsupported config files
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/raddb/experimental.conf

# install doc files omitted by standard install
for f in COPYRIGHT CREDITS INSTALL LICENSE README; do
    cp $f $RPM_BUILD_ROOT/%{docdir}
done

# add Red Hat specific documentation
cat >> $RPM_BUILD_ROOT/%{docdir}/REDHAT << EOF

Red Hat, RHEL, Fedora, and CentOS specific information can be found on the
FreeRADIUS Wiki in the Red Hat FAQ.

http://wiki.freeradius.org/Red_Hat_FAQ

Please reference that document.

EOF

%clean
rm -rf $RPM_BUILD_ROOT



# Make sure our user/group is present prior to any package or subpackage installation
%pre
getent group  radiusd >/dev/null || /usr/sbin/groupadd -r -g 95 radiusd
getent passwd radiusd >/dev/null || /usr/sbin/useradd  -r -g radiusd -u 95 -c "radiusd user" -s /sbin/nologin radiusd > /dev/null 2>&1
exit 0

%pre devel
getent group  radiusd >/dev/null || /usr/sbin/groupadd -r -g 95 radiusd
getent passwd radiusd >/dev/null || /usr/sbin/useradd  -r -g radiusd -u 95 -c "radiusd user" -s /sbin/nologin radiusd > /dev/null 2>&1
exit 0

%pre krb5
getent group  radiusd >/dev/null || /usr/sbin/groupadd -r -g 95 radiusd
getent passwd radiusd >/dev/null || /usr/sbin/useradd  -r -g radiusd -u 95 -c "radiusd user" -s /sbin/nologin radiusd > /dev/null 2>&1
exit 0

%pre ldap
getent group  radiusd >/dev/null || /usr/sbin/groupadd -r -g 95 radiusd
getent passwd radiusd >/dev/null || /usr/sbin/useradd  -r -g radiusd -u 95 -c "radiusd user" -s /sbin/nologin radiusd > /dev/null 2>&1
exit 0

%pre libs
getent group  radiusd >/dev/null || /usr/sbin/groupadd -r -g 95 radiusd
getent passwd radiusd >/dev/null || /usr/sbin/useradd  -r -g radiusd -u 95 -c "radiusd user" -s /sbin/nologin radiusd > /dev/null 2>&1
exit 0

%pre mysql
getent group  radiusd >/dev/null || /usr/sbin/groupadd -r -g 95 radiusd
getent passwd radiusd >/dev/null || /usr/sbin/useradd  -r -g radiusd -u 95 -c "radiusd user" -s /sbin/nologin radiusd > /dev/null 2>&1
exit 0

%pre perl
getent group  radiusd >/dev/null || /usr/sbin/groupadd -r -g 95 radiusd
getent passwd radiusd >/dev/null || /usr/sbin/useradd  -r -g radiusd -u 95 -c "radiusd user" -s /sbin/nologin radiusd > /dev/null 2>&1
exit 0

%pre postgresql
getent group  radiusd >/dev/null || /usr/sbin/groupadd -r -g 95 radiusd
getent passwd radiusd >/dev/null || /usr/sbin/useradd  -r -g radiusd -u 95 -c "radiusd user" -s /sbin/nologin radiusd > /dev/null 2>&1
exit 0

%pre python
getent group  radiusd >/dev/null || /usr/sbin/groupadd -r -g 95 radiusd
getent passwd radiusd >/dev/null || /usr/sbin/useradd  -r -g radiusd -u 95 -c "radiusd user" -s /sbin/nologin radiusd > /dev/null 2>&1
exit 0

%pre unixODBC
getent group  radiusd >/dev/null || /usr/sbin/groupadd -r -g 95 radiusd
getent passwd radiusd >/dev/null || /usr/sbin/useradd  -r -g radiusd -u 95 -c "radiusd user" -s /sbin/nologin radiusd > /dev/null 2>&1
exit 0

%pre utils
getent group  radiusd >/dev/null || /usr/sbin/groupadd -r -g 95 radiusd
getent passwd radiusd >/dev/null || /usr/sbin/useradd  -r -g radiusd -u 95 -c "radiusd user" -s /sbin/nologin radiusd > /dev/null 2>&1
exit 0




%post
/sbin/ldconfig
if [ $1 = 1 ]; then
  /sbin/chkconfig --add radiusd
fi

%preun
if [ $1 = 0 ]; then
  /sbin/service radiusd stop > /dev/null 2>&1
  /sbin/chkconfig --del radiusd
fi


%postun
if [ $1 -ge 1 ]; then
  /sbin/service radiusd condrestart >/dev/null 2>&1 || :
fi
/sbin/ldconfig


%files
%defattr(-,root,root)
%doc %{docdir}/
%config(noreplace) %{_sysconfdir}/pam.d/radiusd
%config(noreplace) %{_sysconfdir}/logrotate.d/radiusd
%config(noreplace) %{_initrddir}/radiusd
%dir %attr(755,radiusd,radiusd) /var/lib/radiusd
# configs
%dir %attr(755,root,radiusd) /etc/raddb
%defattr(-,root,radiusd)
%attr(644,root,radiusd) %config(noreplace) /etc/raddb/dictionary
%config(noreplace) /etc/raddb/acct_users
%config(noreplace) /etc/raddb/attrs
%config(noreplace) /etc/raddb/attrs.access_reject
%config(noreplace) /etc/raddb/attrs.accounting_response
%config(noreplace) /etc/raddb/attrs.pre-proxy
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/clients.conf
%config(noreplace) /etc/raddb/hints
%config(noreplace) /etc/raddb/huntgroups
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/sqlippool.conf
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/preproxy_users
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/proxy.conf
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/radiusd.conf
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/sql.conf
%dir %attr(750,root,radiusd) /etc/raddb/sql
#%attr(640,root,radiusd) %config(noreplace) /etc/raddb/sql/oracle/*
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/users
%dir %attr(770,root,radiusd) /etc/raddb/certs
/etc/raddb/certs/Makefile
/etc/raddb/certs/README
/etc/raddb/certs/xpextensions
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/certs/*.cnf
%attr(750,root,radiusd) /etc/raddb/certs/bootstrap
%dir %attr(750,root,radiusd) /etc/raddb/sites-available
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/sites-available/*
%dir %attr(750,root,radiusd) /etc/raddb/sites-enabled
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/sites-enabled/*
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/eap.conf
%attr(640,root,radiusd) /etc/raddb/example.pl
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/policy.conf
/etc/raddb/policy.txt
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/templates.conf
%dir %attr(750,root,radiusd) /etc/raddb/modules
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/modules/acct_unique
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/modules/always
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/modules/attr_filter
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/modules/attr_rewrite
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/modules/chap
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/modules/checkval
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/modules/counter
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/modules/detail
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/modules/detail.example.com
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/modules/detail.log
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/modules/digest
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/modules/echo
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/modules/etc_group
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/modules/exec
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/modules/expiration
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/modules/expr
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/modules/files
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/modules/inner-eap
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/modules/ippool
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/modules/logintime
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/modules/linelog
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/modules/mac2ip
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/modules/mac2vlan
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/modules/mschap
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/modules/otp
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/modules/pam
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/modules/pap
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/modules/perl
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/modules/passwd
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/modules/policy
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/modules/preprocess
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/modules/radutmp
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/modules/realm
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/modules/smbpasswd
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/modules/smsotp
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/modules/sql_log
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/modules/sqlcounter_expire_on_login
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/modules/sradutmp
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/modules/unix
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/modules/wimax
%dir %attr(700,radiusd,radiusd) /var/run/radiusd/
# binaries
%defattr(-,root,root)
/usr/sbin/checkrad
/usr/sbin/raddebug
/usr/sbin/radiusd
/usr/sbin/radwatch
/usr/sbin/radmin
# man-pages
%doc %{_mandir}/man1/*
%doc %{_mandir}/man5/*
%doc %{_mandir}/man8/*
# dictionaries
%dir %attr(755,root,root) /usr/share/freeradius
/usr/share/freeradius/*
# logs
%dir %attr(700,radiusd,radiusd) /var/log/radius/
%dir %attr(700,radiusd,radiusd) /var/log/radius/radacct/
%attr(644,radiusd,radiusd) /var/log/radius/radutmp
%config(noreplace) %attr(600,radiusd,radiusd) /var/log/radius/radius.log
# RADIUS Loadable Modules
%dir %attr(755,root,root) %{_libdir}/freeradius
#%attr(755,root,root) %{_libdir}/freeradius/rlm_*.so*
#%{_libdir}/freeradius/rlm_acctlog*.so
%{_libdir}/freeradius/rlm_acct_unique.so
%{_libdir}/freeradius/rlm_acct_unique-%{version}.so
%{_libdir}/freeradius/rlm_acctlog.so
%{_libdir}/freeradius/rlm_acctlog-%{version}.so
%{_libdir}/freeradius/rlm_always.so
%{_libdir}/freeradius/rlm_always-%{version}.so
%{_libdir}/freeradius/rlm_attr_filter.so
%{_libdir}/freeradius/rlm_attr_filter-%{version}.so
%{_libdir}/freeradius/rlm_attr_rewrite.so
%{_libdir}/freeradius/rlm_attr_rewrite-%{version}.so
%{_libdir}/freeradius/rlm_chap.so
%{_libdir}/freeradius/rlm_chap-%{version}.so
%{_libdir}/freeradius/rlm_checkval.so
%{_libdir}/freeradius/rlm_checkval-%{version}.so
%{_libdir}/freeradius/rlm_copy_packet.so
%{_libdir}/freeradius/rlm_copy_packet-%{version}.so
%{_libdir}/freeradius/rlm_counter.so
%{_libdir}/freeradius/rlm_counter-%{version}.so
%{_libdir}/freeradius/rlm_dbm.so
%{_libdir}/freeradius/rlm_dbm-%{version}.so
%{_libdir}/freeradius/rlm_detail.so
%{_libdir}/freeradius/rlm_detail-%{version}.so
%{_libdir}/freeradius/rlm_digest.so
%{_libdir}/freeradius/rlm_digest-%{version}.so
%{_libdir}/freeradius/rlm_dynamic_clients.so
%{_libdir}/freeradius/rlm_dynamic_clients-%{version}.so
%{_libdir}/freeradius/rlm_eap.so
%{_libdir}/freeradius/rlm_eap-%{version}.so
%{_libdir}/freeradius/rlm_eap_gtc.so
%{_libdir}/freeradius/rlm_eap_gtc-%{version}.so
%{_libdir}/freeradius/rlm_eap_leap.so
%{_libdir}/freeradius/rlm_eap_leap-%{version}.so
%{_libdir}/freeradius/rlm_eap_md5.so
%{_libdir}/freeradius/rlm_eap_md5-%{version}.so
%{_libdir}/freeradius/rlm_eap_mschapv2.so
%{_libdir}/freeradius/rlm_eap_mschapv2-%{version}.so
%{_libdir}/freeradius/rlm_eap_peap.so
%{_libdir}/freeradius/rlm_eap_peap-%{version}.so
%{_libdir}/freeradius/rlm_eap_sim.so
%{_libdir}/freeradius/rlm_eap_sim-%{version}.so
%{_libdir}/freeradius/rlm_eap_tls.so
%{_libdir}/freeradius/rlm_eap_tls-%{version}.so
%{_libdir}/freeradius/rlm_eap_ttls.so
%{_libdir}/freeradius/rlm_eap_ttls-%{version}.so
%{_libdir}/freeradius/rlm_exec.so
%{_libdir}/freeradius/rlm_exec-%{version}.so
%{_libdir}/freeradius/rlm_expiration.so
%{_libdir}/freeradius/rlm_expiration-%{version}.so
%{_libdir}/freeradius/rlm_expr.so
%{_libdir}/freeradius/rlm_expr-%{version}.so
%{_libdir}/freeradius/rlm_fastusers.so
%{_libdir}/freeradius/rlm_fastusers-%{version}.so
%{_libdir}/freeradius/rlm_files.so
%{_libdir}/freeradius/rlm_files-%{version}.so
%{_libdir}/freeradius/rlm_ippool.so
%{_libdir}/freeradius/rlm_ippool-%{version}.so
%{_libdir}/freeradius/rlm_linelog.so
%{_libdir}/freeradius/rlm_linelog-%{version}.so
%{_libdir}/freeradius/rlm_logintime.so
%{_libdir}/freeradius/rlm_logintime-%{version}.so
%{_libdir}/freeradius/rlm_mschap.so
%{_libdir}/freeradius/rlm_mschap-%{version}.so
%{_libdir}/freeradius/rlm_otp.so
%{_libdir}/freeradius/rlm_otp-%{version}.so
%{_libdir}/freeradius/rlm_pam.so
%{_libdir}/freeradius/rlm_pam-%{version}.so
%{_libdir}/freeradius/rlm_pap.so
%{_libdir}/freeradius/rlm_pap-%{version}.so
%{_libdir}/freeradius/rlm_passwd.so
%{_libdir}/freeradius/rlm_passwd-%{version}.so
%{_libdir}/freeradius/rlm_policy.so
%{_libdir}/freeradius/rlm_policy-%{version}.so
%{_libdir}/freeradius/rlm_preprocess.so
%{_libdir}/freeradius/rlm_preprocess-%{version}.so
%{_libdir}/freeradius/rlm_radutmp.so
%{_libdir}/freeradius/rlm_radutmp-%{version}.so
%{_libdir}/freeradius/rlm_realm.so
%{_libdir}/freeradius/rlm_realm-%{version}.so
%{_libdir}/freeradius/rlm_sql.so
%{_libdir}/freeradius/rlm_sql-%{version}.so
%{_libdir}/freeradius/rlm_sql_log.so
%{_libdir}/freeradius/rlm_sql_log-%{version}.so
%{_libdir}/freeradius/rlm_sqlcounter.so
%{_libdir}/freeradius/rlm_sqlcounter-%{version}.so
%{_libdir}/freeradius/rlm_sqlippool.so
%{_libdir}/freeradius/rlm_sqlippool-%{version}.so
%{_libdir}/freeradius/rlm_unix.so
%{_libdir}/freeradius/rlm_unix-%{version}.so

%files utils
%defattr(-,root,root)
/usr/bin/*

%files libs
# RADIU shared libs
%defattr(-,root,root)
%attr(755,root,root) %{_libdir}/freeradius/lib*.so*

%files devel
%defattr(-,root,root)
#%attr(644,root,root) %{_libdir}/freeradius/*.a
#%attr(644,root,root) %{_libdir}/freeradius/*.la
%dir %attr(755,radiusd,radiusd) /usr/include/freeradius
%attr(644,root,root) /usr/include/freeradius/*.h

%files krb5
%defattr(-,root,root)
%{_libdir}/freeradius/rlm_krb5.so
%{_libdir}/freeradius/rlm_krb5-%{version}.so
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/modules/krb5

%files perl
%defattr(-,root,root)
%{_libdir}/freeradius/rlm_perl.so
%{_libdir}/freeradius/rlm_perl-%{version}.so

%files python
%defattr(-,root,root)
%{_libdir}/freeradius/rlm_python.so
%{_libdir}/freeradius/rlm_python-%{version}.so

%files mysql
%defattr(-,root,root)
%dir %attr(750,root,radiusd) /etc/raddb/sql/mysql
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/sql/mysql/*
%{_libdir}/freeradius/rlm_sql_mysql.so
%{_libdir}/freeradius/rlm_sql_mysql-%{version}.so

%files postgresql
%defattr(-,root,root)
%dir %attr(750,root,radiusd) /etc/raddb/sql/postgresql
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/sql/postgresql/*
%{_libdir}/freeradius/rlm_sql_postgresql.so
%{_libdir}/freeradius/rlm_sql_postgresql-%{version}.so

%files ldap
%defattr(-,root,root)
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/ldap.attrmap
%{_libdir}/freeradius/rlm_ldap.so
%{_libdir}/freeradius/rlm_ldap-%{version}.so
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/modules/ldap

%files unixODBC
%defattr(-,root,root)
%{_libdir}/freeradius/rlm_sql_unixodbc.so
%{_libdir}/freeradius/rlm_sql_unixodbc-%{version}.so

%changelog
* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 10 2009 John Dennis <jdennis@redhat.com> - 2.1.6-4
- install COPYRIGHT CREDITS INSTALL LICENSE README into docdir

* Tue Jun 23 2009 John Dennis <jdennis@redhat.com> - 2.1.6-3
- resolves bug #507571 freeradius packages do not check for user/group existence

* Tue Jun  2 2009 John Dennis <jdennis@redhat.com> - 2.1.6-2
- make /etc/raddb/sites-available/* be config(noreplace)

* Mon May 18 2009 John Dennis <jdennis@redhat.com> - 2.1.6-1
  - update to latest upstream release, from upstream Changelog:
    Feature improvements
      * radclient exits with 0 on successful (accept / ack), and 1
        otherwise (no response / reject)
      * Added support for %%{sql:UPDATE ..}, and insert/delete
        Patch from Arran Cudbard-Bell
      * Added sample "do not respond" policy.  See raddb/policy.conf
        and raddb/sites-available/do_not_respond
      * Cleanups to Suse spec file from Norbert Wegener
      * New VSAs for Juniper from Bjorn Mork
      * Include more RFC dictionaries in the default install
      * More documentation for the WiMAX module
      * Added "chase_referrals" and "rebind" configuration to rlm_ldap.
        This helps with Active Directory.  See raddb/modules/ldap
      * Don't load pre/post-proxy if proxying is disabled.
      * Added %%{md5:...}, which returns MD5 hash in hex.
      * Added configurable "retry_interval" and "poll_interval"
        for "detail" listeners.
      * Added "delete_mppe_keys" configuration option to rlm_wimax.
        Apparently some WiMAX clients misbehave when they see those keys.
      * Added experimental rlm_ruby from
        http://github.com/Antti/freeradius-server/tree/master
      * Add Tunnel attributes to ldap.attrmap
      * Enable virtual servers to be reloaded on HUP.  For now, only
        the "authorize", "authenticate", etc. processing sections are
        reloaded.  Clients and "listen" sections are NOT reloaded.
      * Updated "radwatch" script to be more robust.  See scripts/radwatch
      * Added certificate compatibility notes in raddb/certs/README,
        for compatibility with different operating systems. (i.e. Windows)
      * Permit multiple "-e" in radmin.
      * Add support for originating CoA-Request and Disconnect-Request.
        See raddb/sites-available/originate-coa.
      * Added "lifetime" and "max_queries" to raddb/sql.conf.
        This helps address the problem of hung SQL sockets.
      * Allow packets to be injected via radmin.  See "inject help"
        in radmin.
      * Answer VMPS reconfirmation request.  Patch from Hermann Lauer.
      * Sample logrotate script in scripts/logrotate.freeradius
      * Add configurable poll interval for "detail" listeners
      * New "raddebug" command.  This prints debugging information from
        a running server.  See "man raddebug.
      * Add "require_message_authenticator" configuration to home_server
        configuration.  This makes the server add Message-Authenticator
        to all outgoing Access-Request packets.
      * Added smsotp module, as contributed by Siemens.
      * Enabled the administration socket in the default install.
        See raddb/sites-available/control-socket, and "man radmin"
      * Handle duplicate clients, such as with replicated or
        load-balanced SQL servers and "readclients = yes"

    Bug fixes
      * Minor changes to allow building without VQP.
      * Minor fixes from John Center
      * Fixed raddebug example
      * Don't crash when deleting attributes via unlang
      * Be friendlier to very fast clients
      * Updated the "detail" listener so that it only polls once,
        and not many times in a row, leaking memory each time...
      * Update comparison for Packet-Src-IP-Address (etc.) so that
        the operators other than '==' work.
      * Did autoconf magic to work around weird libtool bug
      * Make rlm_perl keep tags for tagged attributes in more situations
      * Update UID checking for radmin
      * Added "include_length" field for TTLS.  It's needed for RFC
        compliance, but not (apparently) for interoperability.
      * Clean up control sockets when they are closed, so that we don't
        leak memory.
      * Define SUN_LEN for systems that don't have it.
      * Correct some boundary conditions in the conditional checker ("if")
        in "unlang".  Bug noted by Arran Cudbard-Bell.
      * Work around minor building issues in gmake.  This should only
        have affected developers.
      * Change how we manage unprivileged user/group, so that we do not
        create control sockets owned by root.
      * Fixed more minor issues found by Coverity.
      * Allow raddb/certs/bootstrap to run when there is no "make"
        command installed.
      * In radiusd.conf, run_dir depends on the name of the program,
        and isn't hard-coded to "..../radiusd"
      * Check for EOF in more places in the "detail" file reader.
      * Added Freeswitch dictionary.
      * Chop ethernet frames in VMPS, rather than droppping packets.
      * Fix EAP-TLS bug.  Patch from Arnaud Ebalard
      * Don't lose string for regex-compares in the "users" file.
      * Expose more functions in rlm_sql to rlm_sqlippool, which 
        helps on systems where RTLD_GLOBAL is off.
      * Fix typos in MySQL schemas for ippools.
      * Remove macro that was causing build issues on some platforms.
      * Fixed issues with dead home servers.  Bug noted by Chris Moules.
      * Fixed "access after free" with some dynamic clients.

- fix packaging bug, some directories missing execute permission
  /etc/raddb/dictionary now readable by all.

* Tue Feb 24 2009 John Dennis <jdennis@redhat.com> - 2.1.3-4
- fix type usage in unixodbc to match new type usage in unixodbc API

* Thu Feb 19 2009 John Dennis <jdennis@redhat.com> - 2.1.3-3
- add pointer to Red Hat documentation in docdir

* Sat Jan 24 2009 Caolán McNamara <caolanm@redhat.com> - 2.1.3-2
- rebuild for dependencies

* Thu Dec  4 2008 John Dennis <jdennis@redhat.com> - 2.1.3-1
- upgrade to latest upstream release, upstream summary follows:
  The focus of this release is stability.
  Feature Improvements:
    * Allow running with "user=radiusd" and binding to secure sockets.
    * Start sending Status-Server "are you alive" messages earlier, which
      helps with proxying multiple realms to a home server.
    * Removed thread pool code from rlm_perl.  It's not necessary.
    * Added example Perl configuration to raddb/modules/perl
    * Force OpenSSL to support certificates with SHA256. This seems to be
      necessary for WiMAX certs.
  Bug fixes:
    * Fix Debian patch to allow it to build.
    * Fix potential NULL dereference in debugging mode on certain
      platforms for TTLS and PEAP inner tunnels.
    * Fix uninitialized memory in handling of vendor definitions
    * Fix parsing of quoted (but non-string) attributes in the "users" file.
    * Initialize uknown NAS IP to 255.255.255.255, rather than 0.0.0.0
    * use SUN_LEN in control socket, to avoid truncation on some platforms.
    * Correct internal handling of "debug condition" to prevent it from
      being over-written.
    * Check return code of regcomp in "unlang", so that invalid regular
      expressions are caught rather than mishandled.
    * Make rlm_sql use <ltdl.h>.  Addresses bug #610.
    * Document list "type = status" better.  Closes bug #580.
    * Set "default days" for certificates, because OpenSSL won't do it.
      This closes bug #615.
    * Reference correct list in example raddb/modules/ldap. Closes #596.
    * Increase default schema size for Acct-Session-Id to 64. Closes #540.
    * Fix use of temporary files in dialup-admin.  Closes #605 and
      addresses CVE-2008-4474.
    * Addressed a number of minor issues found by Coverity.
    * Added DHCP option 150 to the dictionary.  Closes #618.

* Wed Dec  3 2008 John Dennis <jdennis@redhat.com> - 2.1.1-8
- add --with-system-libtool to configure as a workaround for
undefined reference to lt__PROGRAM__LTX_preloaded_symbols

* Mon Dec  1 2008 John Dennis <jdennis@redhat.com> - 2.1.1-7
- add obsoletes tag for dialupadmin subpackages which were removed

* Mon Dec  1 2008 John Dennis <jdennis@redhat.com> - 2.1.1-7
- add readline-devel BuildRequires

* Sun Nov 30 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.1.1-4
- Rebuild for Python 2.6

* Fri Nov 21 2008 John Dennis <jdennis@redhat.com> - 2.1.1-3
- make spec file buildable on RHEL5.2 by making perl-devel a fedora only dependency.
- remove diaupadmin packages, it's not well supported and there are problems with it.

* Fri Sep 26 2008 John Dennis <jdennis@redhat.com> - 2.1.1-1
- Resolves: bug #464119 bootstrap code could not create initial certs in /etc/raddb/certs because
  permissions were 750, radiusd running as euid radiusd could not write there, permissions now 770

* Thu Sep 25 2008 John Dennis <jdennis@redhat.com> - 2.1.1-1
- upgrade to new upstream 2.1.1 release

* Wed Jul 30 2008 John Dennis <jdennis@redhat.com> - 2.0.5-2
- Resolves: bug #453761: FreeRADIUS %%post should not include chown -R
  specify file attributes for /etc/raddb/ldap.attrmap
  fix consistent use of tabs/spaces (rpmlint warning)

* Mon Jun  9 2008 John Dennis <jdennis@redhat.com> - 2.0.5-1
- upgrade to latest upstream, see Changelog for details,
  upstream now has more complete fix for bug #447545, local patch removed

* Wed May 28 2008 John Dennis <jdennis@redhat.com> - 2.0.4-1
- upgrade to latest upstream, see Changelog for details
- resolves: bug #447545: freeradius missing /etc/raddb/sites-available/inner-tunnel

* Fri May 16 2008  <jdennis@redhat.com> - 2.0.3-3
- # Temporary fix for bug #446864, turn off optimization

* Fri Apr 18 2008 John Dennis <jdennis@redhat.com> - 2.0.3-2
- remove support for radrelay, it's different now
- turn off default inclusion of SQL config files in radiusd.conf since SQL
  is an optional RPM install
- remove mssql config files

* Thu Apr 17 2008 John Dennis <jdennis@redhat.com> - 2.0.3-1
- Upgrade to current upstream 2.0.3 release
- Many thanks to Enrico Scholz for his spec file suggestions incorporated here
- Resolve: bug #438665: Contains files owned by buildsystem
- Add dialupadmin-mysql, dialupadmin-postgresql, dialupadmin-ldap subpackages
  to further partition external dependencies.
- Clean up some unnecessary requires dependencies
- Add versioned requires between subpackages

* Tue Mar 18 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.0.2-2
- add Requires for versioned perl (libperl.so)

* Thu Feb 28 2008  <jdennis@redhat.com> - 2.0.2-1
- upgrade to new 2.0 release
- split into subpackages for more fine grained installation

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.1.7-4.4.ipa
- Autorebuild for GCC 4.3

* Thu Dec 06 2007 Release Engineering <rel-eng at fedoraproject dot org> - 1.1.7-3.4.ipa
- Rebuild for deps

* Sat Nov 10 2007  <jdennis@redhat.com> - 1.1.7-3.3.ipa
- add support in rlm_ldap for reading clients from ldap
- fix TLS parameter controling if a cert which fails to validate
  will be accepted (i.e. self-signed),
  rlm_ldap config parameter=tls_require_cert
  ldap LDAP_OPT_X_TLS_REQUIRE_CERT parameter was being passed to
  ldap_set_option() when it should have been ldap_int_tls_config()

* Sat Nov 3 2007  <jdennis@redhat.com> - 1.1.7-3.2.ipa
- add support in rlm_ldap for SASL/GSSAPI binds to the LDAP server

* Mon Sep 17 2007 Thomas Woerner <twoerner@redhat.com> 1.1.7-3.1
- made init script fully lsb conform

* Mon Sep 17 2007 Thomas Woerner <twoerner@redhat.com> 1.1.7-3
- fixed initscript problem (rhbz#292521)

* Tue Aug 28 2007 Thomas Woerner <twoerner@redhat.com> 1.1.7-2
- fixed initscript for LSB (rhbz#243671, rhbz#243928)
- fixed license tag

* Tue Aug  7 2007 Thomas Woerner <twoerner@redhat.com> 1.1.7-1
- new versin 1.1.7
- install snmp MIB files
- dropped LDAP_DEPRECATED flag, it is upstream
- marked config files for sub packages as config (rhbz#240400)
- moved db files to /var/lib/raddb (rhbz#199082)

* Fri Jun 15 2007 Thomas Woerner <twoerner@redhat.com> 1.1.6-2
- radiusd expects /etc/raddb to not be world readable or writable
  /etc/raddb now belongs to radiusd, post script sets permissions

* Fri Jun 15 2007 Thomas Woerner <twoerner@redhat.com> 1.1.6-1
- new version 1.1.6

* Fri Mar  9 2007 Thomas Woerner <twoerner@redhat.com> 1.1.5-1
- new version 1.1.5
  - no /etc/raddb/otppasswd.sample anymore
  - build is pie by default, dropped pie patch
- fixed build requirement for perl (perl-devel)

* Fri Feb 23 2007 Karsten Hopp <karsten@redhat.com> 1.1.3-3
- remove trailing dot from summary
- fix buildroot
- fix post/postun/preun requirements
- use rpm macros

* Fri Dec  8 2006 Thomas Woerner <twoerner@redhat.com> 1.1.3-2.1
- rebuild for new postgresql library version

* Thu Nov 30 2006 Thomas Woerner <twoerner@redhat.com> 1.1.3-2
- fixed ldap code to not use internals, added LDAP_DEPRECATED compile time flag
  (#210912)

* Tue Aug 15 2006 Thomas Woerner <twoerner@redhat.com> 1.1.3-1
- new version 1.1.3 with lots of upstream bug fixes, some security fixes
  (#205654)

* Tue Aug 15 2006 Thomas Woerner <twoerner@redhat.com> 1.1.2-2
- commented out include for sql.conf in radiusd.conf (#202561)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.1.2-1.1
- rebuild

* Thu Jun  1 2006 Thomas Woerner <twoerner@redhat.com> 1.1.2-1
- new version 1.1.2

* Wed May 31 2006 Thomas Woerner <twoerner@redhat.com> 1.1.1-1
- new version 1.1.1
- fixed incorrect rlm_sql globbing (#189095)
  Thanks to Yanko Kaneti for the fix.
- fixed chown syntax in post script (#182777)
- dropped gcc34, libdir and realloc-return patch
- spec file cleanup with additional libtool build fixes

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.0.5-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.0.5-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Dec 13 2005 Thomas Woerner <twoerner@redhat.com> 1.0.5-1
- new version 1.0.5

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sat Nov 12 2005 Tom Lane <tgl@redhat.com> - 1.0.4-5
- Rebuild due to mysql update.

* Wed Nov  9 2005 Tomas Mraz <tmraz@redhat.com> - 1.0.4-4
- rebuilt with new openssl
- fixed ignored return value of realloc

* Fri Sep 30 2005 Tomas Mraz <tmraz@redhat.com> - 1.0.4-3
- use include instead of pam_stack in pam config

* Wed Jul 20 2005 Thomas Woerner <twoerner@redhat.com> 1.0.4-2
- added missing build requires for libtool-ltdl-devel (#160877)
- modified file list to get a report for missing plugins

* Tue Jun 28 2005 Thomas Woerner <twoerner@redhat.com> 1.0.4-1
- new version 1.0.4
- droppend radrelay patch (fixed upstream)

* Thu Apr 14 2005 Warren Togami <wtogami@redhat.com> 1.0.2-2
- rebuild against new postgresql-libs

* Mon Apr  4 2005 Thomas Woerner <twoerner@redhat.com> 1.0.2-1
- new version 1.0.2

* Fri Nov 19 2004 Thomas Woerner <twoerner@redhat.com> 1.0.1-3
- rebuild for MySQL 4
- switched over to installed libtool

* Fri Nov  5 2004 Thomas Woerner <twoerner@redhat.com> 1.0.1-2
- Fixed install problem of radeapclient (#138069)

* Wed Oct  6 2004 Thomas Woerner <twoerner@redhat.com> 1.0.1-1
- new version 1.0.1
- applied radrelay CVS patch from Kevin Bonner

* Wed Aug 25 2004 Warren Togami <wtogami@redhat.com> 1.0.0-3
- BuildRequires pam-devel and libtool
- Fix errant text in description
- Other minor cleanups

* Wed Aug 25 2004 Thomas Woerner <twoerner@redhat.com> 1.0.0-2.1
- renamed /etc/pam.d/radius to /etc/pam.d/radiusd to match default 
  configuration (#130613)

* Wed Aug 25 2004 Thomas Woerner <twoerner@redhat.com> 1.0.0-2
- fixed BuildRequires for openssl-devel (#130606)

* Mon Aug 16 2004 Thomas Woerner <twoerner@redhat.com> 1.0.0-1
- 1.0.0 final

* Mon Jul  5 2004 Thomas Woerner <twoerner@redhat.com> 1.0.0-0.pre3.2
- added buildrequires for zlib-devel (#127162)
- fixed libdir patch to prefer own libeap instead of installed one (#127168)
- fixed samba account maps in LDAP for samba v3 (#127173)

* Thu Jul  1 2004 Thomas Woerner <twoerner@redhat.com> 1.0.0-0.pre3.1
- third "pre" release of version 1.0.0
- rlm_ldap is using SASLv2 (#126507)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jun  3 2004 Thomas Woerner <twoerner@redhat.com> 0.9.3-4.1
- fixed BuildRequires for gdbm-devel

* Tue Mar 30 2004 Harald Hoyer <harald@redhat.com> - 0.9.3-4
- gcc34 compilation fixes

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Feb 24 2004 Thomas Woerner <twoerner@redhat.com> 0.9.3-3.2
- added sql scripts for rlm_sql to documentation (#116435)

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb  5 2004 Thomas Woerner <twoerner@redhat.com> 0.9.3-2.1
- using -fPIC instead of -fpic for s390 ans s390x

* Thu Feb  5 2004 Thomas Woerner <twoerner@redhat.com> 0.9.3-2
- radiusd is pie, now

* Tue Nov 25 2003 Thomas Woerner <twoerner@redhat.com> 0.9.3-1
- new version 0.9.3 (bugfix release)

* Fri Nov  7 2003 Thomas Woerner <twoerner@redhat.com> 0.9.2-1
- new version 0.9.2

* Mon Sep 29 2003 Thomas Woerner <twoerner@redhat.com> 0.9.1-1
- new version 0.9.1

* Mon Sep 22 2003 Nalin Dahyabhai <nalin@redhat.com> 0.9.0-2.2
- modify default PAM configuration to remove the directory part of the module
  name, so that 32- and 64-bit libpam (called from 32- or 64-bit radiusd) on
  multilib systems will always load the right module for the architecture
- modify default PAM configuration to use pam_stack

* Mon Sep  1 2003 Thomas Woerner <twoerner@redhat.com> 0.9.0-2.1
- com_err.h moved to /usr/include/et

* Tue Jul 22 2003 Thomas Woerner <twoerner@redhat.com> 0.9.0-1
- 0.9.0 final

* Wed Jul 16 2003 Thomas Woerner <twoerner@redhat.com> 0.9.0-0.9.0
- new version 0.9.0 pre3

* Thu May 22 2003 Thomas Woerner <twoerner@redhat.com> 0.8.1-6
- included directory /var/log/radius/radacct for logrotate

* Wed May 21 2003 Thomas Woerner <twoerner@redhat.com> 0.8.1-5
- moved log and run dir to files section, cleaned up post

* Wed May 21 2003 Thomas Woerner <twoerner@redhat.com> 0.8.1-4
- added missing run dir in post

* Tue May 20 2003 Thomas Woerner <twoerner@redhat.com> 0.8.1-3
- fixed module load patch

* Fri May 16 2003 Thomas Woerner <twoerner@redhat.com>
- removed la files, removed devel package
- split into 4 packages: freeradius, freeradius-mysql, freeradius-postgresql,
    freeradius-unixODBC
- fixed requires and buildrequires
- create logging dir in post if it does not exist
- fixed module load without la files

* Thu Apr 17 2003 Thomas Woerner <twoerner@redhat.com> 
- Initial build.
