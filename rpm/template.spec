%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/kilted/.*$
%global __requires_exclude_from ^/opt/ros/kilted/.*$

Name:           ros-kilted-slam-toolbox
Version:        2.9.0
Release:        2%{?dist}%{?release_suffix}
Summary:        ROS slam_toolbox package

License:        LGPL
Source0:        %{name}-%{version}.tar.gz

Requires:       boost-devel
Requires:       boost-python%{python3_pkgversion}-devel
Requires:       ceres-solver-devel
Requires:       eigen3-devel
Requires:       flexiblas-devel
Requires:       lapack-devel
Requires:       qt5-qtbase
Requires:       qt5-qtbase-gui
Requires:       ros-kilted-bond
Requires:       ros-kilted-bondcpp
Requires:       ros-kilted-builtin-interfaces
Requires:       ros-kilted-interactive-markers
Requires:       ros-kilted-lifecycle-msgs
Requires:       ros-kilted-message-filters
Requires:       ros-kilted-nav-msgs
Requires:       ros-kilted-nav2-map-server
Requires:       ros-kilted-pluginlib
Requires:       ros-kilted-rclcpp
Requires:       ros-kilted-rclcpp-lifecycle
Requires:       ros-kilted-rosidl-default-generators
Requires:       ros-kilted-rviz-common
Requires:       ros-kilted-rviz-default-plugins
Requires:       ros-kilted-rviz-ogre-vendor
Requires:       ros-kilted-rviz-rendering
Requires:       ros-kilted-sensor-msgs
Requires:       ros-kilted-std-msgs
Requires:       ros-kilted-std-srvs
Requires:       ros-kilted-tf2
Requires:       ros-kilted-tf2-geometry-msgs
Requires:       ros-kilted-tf2-ros
Requires:       ros-kilted-tf2-sensor-msgs
Requires:       ros-kilted-visualization-msgs
Requires:       suitesparse-devel
Requires:       tbb-devel
Requires:       ros-kilted-ros-workspace
BuildRequires:  boost-devel
BuildRequires:  boost-python%{python3_pkgversion}-devel
BuildRequires:  ceres-solver-devel
BuildRequires:  eigen3-devel
BuildRequires:  flexiblas-devel
BuildRequires:  lapack-devel
BuildRequires:  qt5-qtbase
BuildRequires:  qt5-qtbase-devel
BuildRequires:  ros-kilted-ament-cmake
BuildRequires:  ros-kilted-bond
BuildRequires:  ros-kilted-bondcpp
BuildRequires:  ros-kilted-builtin-interfaces
BuildRequires:  ros-kilted-interactive-markers
BuildRequires:  ros-kilted-lifecycle-msgs
BuildRequires:  ros-kilted-message-filters
BuildRequires:  ros-kilted-nav-msgs
BuildRequires:  ros-kilted-pluginlib
BuildRequires:  ros-kilted-rclcpp
BuildRequires:  ros-kilted-rclcpp-lifecycle
BuildRequires:  ros-kilted-rosidl-default-generators
BuildRequires:  ros-kilted-rviz-common
BuildRequires:  ros-kilted-rviz-default-plugins
BuildRequires:  ros-kilted-rviz-ogre-vendor
BuildRequires:  ros-kilted-rviz-rendering
BuildRequires:  ros-kilted-sensor-msgs
BuildRequires:  ros-kilted-std-msgs
BuildRequires:  ros-kilted-std-srvs
BuildRequires:  ros-kilted-tf2
BuildRequires:  ros-kilted-tf2-geometry-msgs
BuildRequires:  ros-kilted-tf2-ros
BuildRequires:  ros-kilted-tf2-sensor-msgs
BuildRequires:  ros-kilted-visualization-msgs
BuildRequires:  suitesparse-devel
BuildRequires:  tbb-devel
BuildRequires:  ros-kilted-ros-workspace
BuildRequires:  ros-kilted-rosidl-typesupport-fastrtps-c
BuildRequires:  ros-kilted-rosidl-typesupport-fastrtps-cpp
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Provides:       %{name}-runtime = %{version}-%{release}
Provides:       ros-kilted-rosidl-interface-packages(member)

%if 0%{?with_tests}
BuildRequires:  ros-kilted-ament-cmake-cpplint
BuildRequires:  ros-kilted-ament-cmake-flake8
BuildRequires:  ros-kilted-ament-cmake-gtest
BuildRequires:  ros-kilted-ament-cmake-uncrustify
BuildRequires:  ros-kilted-ament-lint-auto
BuildRequires:  ros-kilted-launch
BuildRequires:  ros-kilted-launch-testing
%endif

%if 0%{?with_weak_deps}
Supplements:    ros-kilted-rosidl-interface-packages(all)
%endif

%description
This package provides a sped up improved slam karto with updated SDK and
visualization and modification toolsets

%prep
%autosetup -p1

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/kilted/setup.sh" ]; then . "/opt/ros/kilted/setup.sh"; fi
mkdir -p .obj-%{_target_platform} && cd .obj-%{_target_platform}
%cmake3 \
    -UINCLUDE_INSTALL_DIR \
    -ULIB_INSTALL_DIR \
    -USYSCONF_INSTALL_DIR \
    -USHARE_INSTALL_PREFIX \
    -ULIB_SUFFIX \
    -DCMAKE_INSTALL_PREFIX="/opt/ros/kilted" \
    -DAMENT_PREFIX_PATH="/opt/ros/kilted" \
    -DCMAKE_PREFIX_PATH="/opt/ros/kilted" \
    -DSETUPTOOLS_DEB_LAYOUT=OFF \
%if !0%{?with_tests}
    -DBUILD_TESTING=OFF \
%endif
    ..

%make_build

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/kilted/setup.sh" ]; then . "/opt/ros/kilted/setup.sh"; fi
%make_install -C .obj-%{_target_platform}

%if 0%{?with_tests}
%check
# Look for a Makefile target with a name indicating that it runs tests
TEST_TARGET=$(%__make -qp -C .obj-%{_target_platform} | sed "s/^\(test\|check\):.*/\\1/;t f;d;:f;q0")
if [ -n "$TEST_TARGET" ]; then
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/kilted/setup.sh" ]; then . "/opt/ros/kilted/setup.sh"; fi
CTEST_OUTPUT_ON_FAILURE=1 \
    %make_build -C .obj-%{_target_platform} $TEST_TARGET || echo "RPM TESTS FAILED"
else echo "RPM TESTS SKIPPED"; fi
%endif

%files
/opt/ros/kilted

%changelog
* Mon Jun 09 2025 Steve Macenski <stevenmacenski@gmail.com> - 2.9.0-2
- Autogenerated by Bloom

