# TODO:
# 	doesn't compile with libstdc++-4.2.0
%define		_rel	r5

%define		ma_realversion	1.2.4-rc
%define		qb_realversion	1.2.4-beta
%define		wb_realversion	1.1.4-alpha

Summary:	GUI Tools for MySQL 5.0 - common files
Summary(pl):	Narzêdzia GUI dla MySQL-a 5.0 - pliki wspólne
Name:		mysql-gui-tools
Version:	5.0
Release:	0.%{_rel}.1
License:	GPL
Group:		Applications/Databases
Source0:	http://sunsite.icm.edu.pl/mysql/Downloads/MySQLGUITools/%{name}-%{version}%{_rel}.tar.gz
# Source0-md5:	57a3ea4c15bf085437e81edc4edcb2c1
Patch0:		%{name}-lua.patch
Patch1:		%{name}-termcap.patch
URL:		http://www.mysql.com/products/tools/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	gtkhtml-devel >= 3.6.0
BuildRequires:	gtkmm-devel >= 2.4.0
BuildRequires:	libglade2-devel >= 1:2.0.0
BuildRequires:	libgtkhtml-devel
BuildRequires:	lua-devel >= 5.0.3-2
BuildRequires:	mysql-devel
BuildRequires:	pcre-devel >= 3.9
BuildRequires:	perl-XML-Parser
BuildRequires:	pkgconfig
BuildRequires:	popt-devel
BuildRequires:	OpenGL-GLU-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GUI Tools for MySQL 5.0 is a suite of applications written for
developing and managing MySQL servers. 

This package contains data files and libraries for MySQL GUI Tools.
Actual applications are in mysql-administrator, mysql-query-browser
and mysql-workbench packages.

%description -l pl
GUI Tools dla MySQL-a 5.0 to zestaw aplikacji do rozwijania i
zarz±dzania serwerami MySQL.

Ten pakiet zawiera pliki danych i bibliotek dla MySQL GUI Tools.
W³a¶ciwe aplikacje znajduj± siê w pakietach mysql-administrator,
mysq-query-browser oraz mysql-workbench.

%package -n mysql-administrator
Summary:	A MySQL server management, configuration and monitoring tool
Summary(pl):	Narzêdzie do zarz±dzania, konfiguracji i monitorowania pracy serwera MySQL
Group:		Applications/Databases
Requires:	mysql-gui-tools = %{version}

%description -n mysql-administrator
MySQL Administrator is a powerful visual administration console that
enables you to easily administer your MySQL environment and gain
significantly better visibility into how your databases are operating.
MySQL Administrator now integrates database management and maintenance
into a single, seamless environment, with a clear and intuitive
graphical user interface.

This is MySQL Administrator %{ma_realversion}.

%description -n mysql-administrator -l pl
MySQL Administrator jest potê¿nym graficznym narzêdziem umo¿liwiaj±cym
³atwe administrowanie ca³ym ¶rodowiskiem MySQL. Dziêki przejrzystemu
interfejsowi i logicznemu usytuowaniu elementów jest bardzo ³atwy i
intuicyjny w obs³udze.

Ten pakiet zawiera MySQL Administrator %{ma_realversion}.

%package -n mysql-query-browser
Summary:	Query shell for MySQL 5.0
Summary(pl):	Graficzna pow³oka do zapytañ MySQL-a 5.0
Group:		Applications/Databases
Requires:	mysql-gui-tools = %{version}

%description -n mysql-query-browser
MySQL Query Browser is a GUI tool for executing SQL queries. It will
display the result in a list where you can edit its contents and save.
It has several auxiliar features to facilitate work, such as query
"bookmarking", query history, syntax highlighting and online help.

It's part of the MySQL Developer Suite.
This is MySQL QueryBrowser %{qb_realversion}.

%description -n mysql-query-browser -l pl
MySQL Query Browser to narzêdzie z graficznym interfejsem do
wykonywania zapytañ SQL. Wy¶wietla wyniki w postaci listy, gdzie mo¿na
modyfikowaæ jej zawarto¶æ i zapisywaæ. Ma kilka dodatkowych mo¿liwo¶ci
u³atwiaj±cych pracê, takie jak "zak³adki" dla zapytañ, historiê
zapytañ, pod¶wietlanie sk³adni i pomoc podrêczn±.

Ten pakiet zawiera MySQL Query Browser %{qb_realversion}.

%package -n mysql-workbench
Summary:	Extensible modeling tool for MySQL 5.0
Summary(pl):	Narzêdzie do modelowania baz danych dla MySQL-a 5.0
Group:		Applications/Databases
Requires:	mysql-gui-tools = %{version}

%description -n mysql-workbench
MySQL Workbench is a database modeling tool for MySQL. You can use it
to design and create new database schemas, document existing databases
and even perform complex migrations to MySQL.

MySQL Workbench requires OpenGL and a 3D accelerated graphics card
with at least 16MB of memory.

This is MySQL Workbench %{wb_realversion}.

%description -n mysql-workbench -l pl
MySQL Workbench to narzêdzie do modelowania baz danych dla MySQL-a.
Mo¿na u¿ywaæ go do projektowania i tworzenia schematów nowych baz
danych, dokumentowania istniej±cych baz danych, a nawet wykonywania
skomplikowanych migracji do MySQL-a.

MySQL Workbench wymaga OpenGL-a i karty graficznej ze sprzêtow±
akceleracj± operacji 3D z minimum 16 MB pamiêci.

Ten pakiet zawiera MySQL Workbench %{wb_realversion}.

%prep
%setup -q -n %{name}-%{version}%{_rel}
%patch0 -p1
%patch1 -p1

%build
PKG_CONFIG=pkg-config
export PKG_CONFIG

# GUI Common
cd mysql-gui-common
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-gtkhtml=libgtkhtml-3.8 \
	--enable-canvas \
	--enable-grt \
	--with-lua-includes="`pkg-config lua50 --cflags-only-I | sed s:-I::`" \
	--with-lua-libs="`pkg-config lua50 --libs`"
%{__make}
cd ..

# Administrator
cd mysql-administrator
%{__aclocal}
%{__autoconf}
%{__automake}
%configure
%{__make}
cd ..

# Query Browser
cd mysql-query-browser
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-gtkhtml=libgtkhtml-3.8
%{__make}
cd ..

# Workbench
cd mysql-workbench
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-gtkhtml=libgtkhtml-3.8 \
	--with-commondirname=workbench
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

for dir in \
	mysql-gui-common \
	mysql-administrator \
	mysql-query-browser \
	mysql-workbench
do
	%{__make} -C $dir -k install \
		DESTDIR=$RPM_BUILD_ROOT
done

%find_lang mysql-administrator
%find_lang mysql-query-browser

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %{_datadir}/mysql-gui
%dir %{_datadir}/mysql-gui/common
%dir %{_datadir}/mysql-gui/common/lua
%dir %{_datadir}/mysql-gui/common/grt
%dir %{_datadir}/mysql-gui/common/grt/db
%dir %{_datadir}/mysql-gui/common/grt/icons
%dir %{_datadir}/mysql-gui/common/grt/icons/structs
# FIXME: "*" duplicates all below
%{_datadir}/mysql-gui/common/*
%{_datadir}/mysql-gui/common/lua/*.lua
%{_datadir}/mysql-gui/common/grt/*.xml
%{_datadir}/mysql-gui/common/grt/db/*.png
%{_datadir}/mysql-gui/common/grt/icons/*.png
%{_datadir}/mysql-gui/common/grt/icons/structs/*.png

%files -n mysql-administrator -f mysql-administrator.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mabackup
%attr(755,root,root) %{_bindir}/mysql-administrator
%attr(755,root,root) %{_bindir}/mysql-administrator-bin
%dir %{_datadir}/mysql-gui/administrator
%{_datadir}/mysql-gui/administrator/*
%{_datadir}/mysql-gui/MySQLIcon_Admin*
%{_desktopdir}/MySQLAdministrator.desktop

%files -n mysql-query-browser -f mysql-query-browser.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mysql-query-browser
%attr(755,root,root) %{_bindir}/mysql-query-browser-bin
%dir %{_datadir}/mysql-gui/query-browser
%{_datadir}/mysql-gui/query-browser/*
%{_datadir}/mysql-gui/MySQLIcon_Query*
%{_desktopdir}/MySQLQueryBrowser.desktop

%files -n mysql-workbench
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mysql-workbench
%attr(755,root,root) %{_bindir}/mysql-workbench-bin
%dir %{_datadir}/mysql-gui/workbench
%{_datadir}/mysql-gui/workbench/*
%{_datadir}/mysql-gui/MySQLIcon_Workbench*
%{_desktopdir}/MySQLWorkbench.desktop
