#define beta rc2
#define snapshot 20200627
%define major 6

%define _qtdir %{_libdir}/qt%{major}

Name:		qt6-qtgraphs
Version:	6.8.1
Release:	%{?beta:0.%{beta}.}%{?snapshot:0.%{snapshot}.}1
%if 0%{?snapshot:1}
# "git archive"-d from "dev" branch of git://code.qt.io/qt/qtbase.git
Source:		qtgraphs-%{?snapshot:%{snapshot}}%{!?snapshot:%{version}}.tar.zst
%else
Source:		http://download.qt-project.org/%{?beta:development}%{!?beta:official}_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}%{?beta:-%{beta}}/submodules/qtgraphs-everywhere-src-%{version}%{?beta:-%{beta}}.tar.xz
%endif
Group:		System/Libraries
Summary:	Qt %{major} Graphs module
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	cmake(Qt%{major}Core)
BuildRequires:	cmake(Qt%{major}DBus)
BuildRequires:	cmake(Qt%{major}Qml)
BuildRequires:	cmake(Qt%{major}QmlCore)
BuildRequires:	cmake(Qt%{major}Gui)
BuildRequires:	cmake(Qt%{major}Widgets)
BuildRequires:	cmake(Qt%{major}OpenGL)
BuildRequires:	cmake(Qt%{major}OpenGLWidgets)
BuildRequires:	cmake(Qt%{major}Quick)
BuildRequires:	cmake(Qt%{major}Network)
BuildRequires:	cmake(Qt%{major}QuickTest)
BuildRequires:	cmake(Qt%{major}QuickWidgets)
BuildRequires:	cmake(Qt%{major}Quick3D)
BuildRequires:	cmake(Qt%{major}Test)
BuildRequires:	cmake(Qt%{major}QuickShapesPrivate)
BuildRequires:	pkgconfig(xkbcommon)
BuildRequires:	pkgconfig(xkbfile)
BuildRequires:	pkgconfig(vulkan)
BuildRequires:	qt%{major}-cmake
License:	LGPLv3/GPLv3/GPLv2

%description
Qt %{major} Graphs module

%define extra_files_Graphs \
%{_qtdir}/qml/QtGraphs
#{_qtdir}/qml/QtGraphs3D
# ^^^ seems to have gone away in 6.7-beta2, need to make sure that's intentional

%define extra_devel_files_Graphs \
%{_qtdir}/lib/cmake/Qt6Qml/QmlPlugins/Qt6Graphsplugin*.cmake \
%{_qtdir}/sbom/*

%define extra_devel_files_Graphs2D \
%{_qtdir}/lib/cmake/Qt6Qml/QmlPlugins/Qt6Graphs2Dplugin*.cmake

%qt6libs Graphs GraphsWidgets
# Graphs2D is gone in 6.7-beta2

%package examples
Summary: Examples for the Qt %{major} Graphs module
Group: Development/KDE and Qt

%description examples
Examples for the Qt %{major} Graphs module

%files examples
%{_qtdir}/examples/graphs

%prep
%autosetup -p1 -n qtgraphs%{!?snapshot:-everywhere-src-%{version}%{?beta:-%{beta}}}
%cmake -G Ninja \
	-DCMAKE_INSTALL_PREFIX=%{_qtdir} \
	-DQT_BUILD_EXAMPLES:BOOL=ON \
	-DQT_WILL_INSTALL:BOOL=ON

%build
export LD_LIBRARY_PATH="$(pwd)/build/lib:${LD_LIBRARY_PATH}"
%ninja_build -C build

%install
%ninja_install -C build
%qt6_postinstall
