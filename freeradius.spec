Summary: High-performance and highly configurable free RADIUS server.
Name: freeradius
Version: 1.0.1
Release: 3
License: GPL
Group: System Environment/Daemons
URL: http://www.freeradius.org/
Source0: ftp://ftp.freeradius.org/pub/radius/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires: chkconfig net-snmp krb5-libs net-snmp-utils
BuildRequires: net-snmp-devel net-snmp-utils krb5-devel openldap-devel postgresql-devel 
BuildRequires: mysql-devel unixODBC-devel gdbm-devel zlib-devel openssl-devel libtool pam-devel
Patch1: freeradius-1.0.0-ltdl_no_la.patch
Patch2: freeradius-1.0.0-libdir.patch
Patch3: freeradius-0.9.0-pam-multilib.patch
Patch4: freeradius-0.9.0-com_err.patch
Patch5: freeradius-1.0.0-pie.patch
Patch6: freeradius-0.9.3-gcc34.patch
Patch7: freeradius-1.0.0-sasl2.patch
Patch8: freeradius-1.0.0-samba3.patch
Patch9: freeradius-1.0.1-radrelay.patch
Patch10: freeradius-1.0.1-build.patch
Patch11: freeradius-1.0.1-lib64.patch

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

%package mysql
Summary: MySQL bindings for freeradius
Group: System Environment/Daemons
Requires: %{name} = %{version}-%{release}
Requires: mysql

%description mysql
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

%package postgresql
Summary: postgresql bindings for freeradius
Group: System Environment/Daemons
Requires: %{name} = %{version}-%{release}
Requires: postgresql

%description postgresql
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

%package unixODBC
Summary: unixODBC bindings for freeradius
Group: System Environment/Daemons
Requires: %{name} = %{version}-%{release}
Requires: unixODBC

%description unixODBC
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


%prep
%setup -q 
%patch1 -p1 -b .ltdl_no_la
%patch2 -p1 -b .libdir
%patch3 -p1 -b .pam-multilib
%patch4 -p1 -b .com_err
%patch5 -p1 -b .pie
%patch6 -p1 -b .gcc34
%patch7 -p1 -b .sasl2
%patch8 -p1 -b .samba3
%patch9 -p1 -b .radrelay
%patch10 -p1 -b .build


%build
%ifarch s390 s390x
export CFLAGS="$RPM_OPT_FLAGS -fPIC"
%else
export CFLAGS="$RPM_OPT_FLAGS -fpic"
%endif
%configure \
	--enable-shared --disable-static \
	--with-gnu-ld \
	--with-threads \
	--with-thread-pool \
 	--disable-ltdl-install --with-system-libtool \
	--with-rlm-sql_postgresql-include-dir=/usr/include/pgsql \
	--with-rlm-sql_mysql-include-dir=/usr/include/mysql \
	--with-mysql-lib-dir=%{_libdir}/mysql \
	--with-rlm-dbm-lib-dir=%{_libdir} \
	--with-rlm-krb5-include-dir=/usr/kerberos/include
%if "%{_lib}" == "lib64"
perl -pi -e 's:sys_lib_search_path_spec=.*:sys_lib_search_path_spec="/lib64 /usr/lib64 /usr/local/lib64":' libtool
%endif

make


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc/{logrotate.d,pam.d,rc.d/init.d}
%makeinstall

RADDB=$RPM_BUILD_ROOT/etc/raddb
# set radiusd as default user/group
perl -i -pe 's/^#user =.*$/user = radiusd/' $RADDB/radiusd.conf
perl -i -pe 's/^#group =.*$/group = radiusd/' $RADDB/radiusd.conf
# shadow password file MUST be defined on Linux
perl -i -pe 's/#	shadow =/shadow =/' $RADDB/radiusd.conf

install -m 755 redhat/rc.radiusd-redhat $RPM_BUILD_ROOT/etc/rc.d/init.d/radiusd
install -m 644 redhat/radiusd-logrotate $RPM_BUILD_ROOT/etc/logrotate.d/radiusd
install -m 644 redhat/radiusd-pam $RPM_BUILD_ROOT/etc/pam.d/radiusd

install -m 644 src/modules/rlm_sql/drivers/rlm_sql_*/*.sql $RPM_BUILD_ROOT%{_docdir}/freeradius-%{version}*/

# remove unwanted rc.radiusd
rm -f $RPM_BUILD_ROOT%{_prefix}/sbin/rc.radiusd

find $RPM_BUILD_ROOT%{_libdir} -name "*.la" -print | xargs rm -f
find $RPM_BUILD_ROOT%{_libdir} -name "*.a" -print | xargs rm -f

mkdir -p $RPM_BUILD_ROOT/var/log/radius
touch $RPM_BUILD_ROOT/var/log/radius/{radutmp,radwtmp,radius.log}
mkdir -p $RPM_BUILD_ROOT/var/log/radius/radacct
mkdir -p $RPM_BUILD_ROOT/var/run/radiusd


%clean
rm -rf $RPM_BUILD_ROOT


%pre
/usr/sbin/useradd -M -o -r -d / -u 95 -c "radiusd user" -s /bin/false radiusd > /dev/null 2>&1 || :


%post
/sbin/ldconfig
if [ $1 = 1 ]; then
  /sbin/chkconfig --add radiusd
fi
for i in /var/log/radius/{radutmp,radwtmp,radius.log}; do
  /bin/touch $i && /bin/chown radiusd: $i && /bin/chmod 600 $i
done


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
%defattr(-,root,root,-)
%doc %{_docdir}/freeradius-%{version}*/
%config (noreplace) /etc/pam.d/radiusd
%config (noreplace) /etc/logrotate.d/radiusd
%config (noreplace) /etc/rc.d/init.d/radiusd
%config (noreplace) /etc/raddb/[a-ce-z]*
%config /etc/raddb/dictionary*
%{_bindir}/*
%{_libdir}/libeap*.so
%{_libdir}/libradius*.so
%{_libdir}/rlm_[a-r]*.so
%{_libdir}/rlm_sql-%{version}*.so
%{_libdir}/rlm_sql.so
%{_libdir}/rlm_[t-z]*.so
%{_datadir}/freeradius
%{_sbindir}/*
%{_mandir}/man1/*.1*
%{_mandir}/man5/*.5*
%{_mandir}/man8/*.8*
%attr(0700,radiusd,radiusd) %dir /var/log/radius
%ghost %attr(0600,radiusd,radiusd) /var/log/radius/radutmp
%ghost %attr(0600,radiusd,radiusd) /var/log/radius/radwtmp
%ghost %attr(0600,radiusd,radiusd) /var/log/radius/radius.log
%attr(0700,radiusd,radiusd) %dir /var/log/radius/radacct
%attr(0700,radiusd,radiusd) %dir /var/run/radiusd

%files mysql
%defattr(-,root,root,-)
%{_libdir}/*_mysql*.so

%files postgresql
%defattr(-,root,root,-)
%{_libdir}/*_postgresql*.so

%files unixODBC
%defattr(-,root,root,-)
%{_libdir}/*_unixodbc*.so


%changelog
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
