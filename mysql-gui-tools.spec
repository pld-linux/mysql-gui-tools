%define		_rel	r12

%define		ma_realversion	1.2.10
%define		qb_realversion	1.2.10
%define		wb_realversion	1.1.10-alpha

%define		_gtkhtml_ver	3.14

Summary:	GUI Tools for MySQL 5.0 - common files
Summary(pl.UTF-8):	Narzędzia GUI dla MySQL-a 5.0 - pliki wspólne
Name:		mysql-gui-tools
Version:	5.0
Release:	0.%{_rel}.4
License:	GPL
Group:		Applications/Databases
#Source0:	http://sunsite.icm.edu.pl/mysql/Downloads/MySQLGUITools/%{name}-%{version}%{_rel}.tar.gz
Source0:	http://sunsite.informatik.rwth-aachen.de/mysql/Downloads/MySQLGUITools/%{name}-%{version}%{_rel}.tar.gz
# Source0-md5:	755a62e8cd0ea0e138be6eedc430d7a9
Patch0:		%{name}-lua.patch
Patch1:		%{name}-termcap.patch
Patch2:		%{name}-gcc42.patch
Patch3:		%{name}-workbench.patch
Patch4:		%{name}-bash.patch
Patch5:		%{name}-global.patch
Patch6:		%{name}-configure.patch
Patch7:		%{name}-desktop.patch
URL:		http://www.mysql.com/products/tools/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dos2unix
BuildRequires:	gettext-tools
BuildRequires:	gtkhtml-devel >= 3.14.0
BuildRequires:	gtkmm-devel >= 2.4.0
%ifarch i586 i686 pentium3 pentium4 athlon %{x8664}
BuildRequires:	jdk
%endif
BuildRequires:	libglade2-devel >= 1:2.0.0
BuildRequires:	libgnomeprint-devel >= 2.2.0
BuildRequires:	libgtkhtml-devel
BuildRequires:	libuuid-devel
BuildRequires:	lua50-devel >= 5.0.3-2
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

%description -l pl.UTF-8
GUI Tools dla MySQL-a 5.0 to zestaw aplikacji do rozwijania i
zarządzania serwerami MySQL.

Ten pakiet zawiera pliki danych i bibliotek dla MySQL GUI Tools.
Właściwe aplikacje znajdują się w pakietach mysql-administrator,
mysq-query-browser oraz mysql-workbench.

%package -n mysql-administrator
Summary:	A MySQL server management, configuration and monitoring tool
Summary(pl.UTF-8):	Narzędzie do zarządzania, konfiguracji i monitorowania pracy serwera MySQL
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

%description -n mysql-administrator -l pl.UTF-8
MySQL Administrator jest potężnym graficznym narzędziem umożliwiającym
łatwe administrowanie całym środowiskiem MySQL. Dzięki przejrzystemu
interfejsowi i logicznemu usytuowaniu elementów jest bardzo łatwy i
intuicyjny w obsłudze.

Ten pakiet zawiera MySQL Administrator %{ma_realversion}.

%package -n mysql-query-browser
Summary:	Query shell for MySQL 5.0
Summary(pl.UTF-8):	Graficzna powłoka do zapytań MySQL-a 5.0
Group:		Applications/Databases
Requires:	mysql-gui-tools = %{version}

%description -n mysql-query-browser
MySQL Query Browser is a GUI tool for executing SQL queries. It will
display the result in a list where you can edit its contents and save.
It has several auxiliar features to facilitate work, such as query
"bookmarking", query history, syntax highlighting and online help.

It's part of the MySQL Developer Suite.
This is MySQL QueryBrowser %{qb_realversion}.

%description -n mysql-query-browser -l pl.UTF-8
MySQL Query Browser to narzędzie z graficznym interfejsem do
wykonywania zapytań SQL. Wyświetla wyniki w postaci listy, gdzie można
modyfikować jej zawartość i zapisywać. Ma kilka dodatkowych możliwości
ułatwiających pracę, takie jak "zakładki" dla zapytań, historię
zapytań, podświetlanie składni i pomoc podręczną.

Ten pakiet zawiera MySQL Query Browser %{qb_realversion}.

%package -n mysql-workbench
Summary:	Extensible modeling tool for MySQL 5.0
Summary(pl.UTF-8):	Narzędzie do modelowania baz danych dla MySQL-a 5.0
Group:		Applications/Databases
Requires:	mysql-gui-tools = %{version}

%description -n mysql-workbench
MySQL Workbench is a database modeling tool for MySQL. You can use it
to design and create new database schemas, document existing databases
and even perform complex migrations to MySQL.

MySQL Workbench requires OpenGL and a 3D accelerated graphics card
with at least 16MB of memory.

This is MySQL Workbench %{wb_realversion}.

%description -n mysql-workbench -l pl.UTF-8
MySQL Workbench to narzędzie do modelowania baz danych dla MySQL-a.
Można używać go do projektowania i tworzenia schematów nowych baz
danych, dokumentowania istniejących baz danych, a nawet wykonywania
skomplikowanych migracji do MySQL-a.

MySQL Workbench wymaga OpenGL-a i karty graficznej ze sprzętową
akceleracją operacji 3D z minimum 16 MB pamięci.

Ten pakiet zawiera MySQL Workbench %{wb_realversion}.

%prep
%setup -q -n %{name}-%{version}%{_rel}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
dos2unix mysql-administrator/MySQLAdministrator.desktop.in
%patch7 -p1

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
%ifnarch i586 i686 pentium3 pentium4 athlon %{x8664}
	--disable-java-modules \
%endif
	--with-gtkhtml=libgtkhtml-%{_gtkhtml_ver} \
	--enable-canvas \
	--enable-grt \
	--with-lua-includes="`pkg-config lua50 --cflags-only-I | sed s:-I::`" \
	--with-lua-libs="`pkg-config lua50 --libs`"
%{__make} -j1
cd ..

# Administrator
cd mysql-administrator
%{__aclocal}
%{__autoconf}
%{__automake}
%configure
cd ..

# Query Browser
cd mysql-query-browser
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-gtkhtml=libgtkhtml-%{_gtkhtml_ver}
cd ..

# Workbench
cd mysql-workbench
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-gtkhtml=libgtkhtml-%{_gtkhtml_ver} \
	--with-commondirname=common
cd ..

%{__make} -C mysql-gui-common
%{__make} -C mysql-administrator
%{__make} -C mysql-query-browser
%{__make} -C mysql-workbench

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
%{_datadir}/mysql-gui/common/*.gif
%{_datadir}/mysql-gui/common/*.glade
%{_datadir}/mysql-gui/common/*.png
%{_datadir}/mysql-gui/common/*.txt
%{_datadir}/mysql-gui/common/*.xml
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
