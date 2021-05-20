%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/galactic/.*$
%global __requires_exclude_from ^/opt/ros/galactic/.*$

Name:           ros-galactic-slam-toolbox
Version:        2.5.0
Release:        2%{?dist}%{?release_suffix}
Summary:        ROS slam_toolbox package

License:        LGPL
Source0:        %{name}-%{version}.tar.gz

Requires:       boost-devel
Requires:       boost-python%{python3_pkgversion}-devel
Requires:       ceres-solver-devel
Requires:       eigen3-devel
Requires:       lapack-devel
Requires:       qt5-qtbase
Requires:       qt5-qtbase-gui
Requires:       ros-galactic-builtin-interfaces
Requires:       ros-galactic-interactive-markers
Requires:       ros-galactic-message-filters
Requires:       ros-galactic-nav-msgs
Requires:       ros-galactic-nav2-map-server
Requires:       ros-galactic-pluginlib
Requires:       ros-galactic-rclcpp
Requires:       ros-galactic-rosidl-default-generators
Requires:       ros-galactic-rviz-common
Requires:       ros-galactic-rviz-default-plugins
Requires:       ros-galactic-rviz-ogre-vendor
Requires:       ros-galactic-rviz-rendering
Requires:       ros-galactic-sensor-msgs
Requires:       ros-galactic-std-msgs
Requires:       ros-galactic-std-srvs
Requires:       ros-galactic-tf2
Requires:       ros-galactic-tf2-geometry-msgs
Requires:       ros-galactic-tf2-ros
Requires:       ros-galactic-tf2-sensor-msgs
Requires:       ros-galactic-visualization-msgs
Requires:       suitesparse-devel
Requires:       tbb-devel
Requires:       ros-galactic-ros-workspace
BuildRequires:  boost-devel
BuildRequires:  boost-python%{python3_pkgversion}-devel
BuildRequires:  ceres-solver-devel
BuildRequires:  eigen3-devel
BuildRequires:  lapack-devel
BuildRequires:  qt5-qtbase
BuildRequires:  qt5-qtbase-devel
BuildRequires:  ros-galactic-ament-cmake
BuildRequires:  ros-galactic-ament-cmake-cpplint
BuildRequires:  ros-galactic-ament-cmake-flake8
BuildRequires:  ros-galactic-ament-cmake-gtest
BuildRequires:  ros-galactic-ament-cmake-uncrustify
BuildRequires:  ros-galactic-ament-lint-auto
BuildRequires:  ros-galactic-builtin-interfaces
BuildRequires:  ros-galactic-interactive-markers
BuildRequires:  ros-galactic-launch
BuildRequires:  ros-galactic-launch-testing
BuildRequires:  ros-galactic-message-filters
BuildRequires:  ros-galactic-nav-msgs
BuildRequires:  ros-galactic-nav2-map-server
BuildRequires:  ros-galactic-pluginlib
BuildRequires:  ros-galactic-rclcpp
BuildRequires:  ros-galactic-rosidl-default-generators
BuildRequires:  ros-galactic-rviz-common
BuildRequires:  ros-galactic-rviz-default-plugins
BuildRequires:  ros-galactic-rviz-ogre-vendor
BuildRequires:  ros-galactic-rviz-rendering
BuildRequires:  ros-galactic-sensor-msgs
BuildRequires:  ros-galactic-std-msgs
BuildRequires:  ros-galactic-std-srvs
BuildRequires:  ros-galactic-tf2
BuildRequires:  ros-galactic-tf2-geometry-msgs
BuildRequires:  ros-galactic-tf2-ros
BuildRequires:  ros-galactic-tf2-sensor-msgs
BuildRequires:  ros-galactic-visualization-msgs
BuildRequires:  suitesparse-devel
BuildRequires:  tbb-devel
BuildRequires:  ros-galactic-ros-workspace
BuildRequires:  ros-galactic-rosidl-typesupport-fastrtps-c
BuildRequires:  ros-galactic-rosidl-typesupport-fastrtps-cpp
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Provides:       %{name}-runtime = %{version}-%{release}
Provides:       ros-galactic-rosidl-interface-packages(member)

%if 0%{?with_weak_deps}
Supplements:    ros-galactic-rosidl-interface-packages(all)
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
if [ -f "/opt/ros/galactic/setup.sh" ]; then . "/opt/ros/galactic/setup.sh"; fi
mkdir -p obj-%{_target_platform} && cd obj-%{_target_platform}
%cmake3 \
    -UINCLUDE_INSTALL_DIR \
    -ULIB_INSTALL_DIR \
    -USYSCONF_INSTALL_DIR \
    -USHARE_INSTALL_PREFIX \
    -ULIB_SUFFIX \
    -DCMAKE_INSTALL_PREFIX="/opt/ros/galactic" \
    -DAMENT_PREFIX_PATH="/opt/ros/galactic" \
    -DCMAKE_PREFIX_PATH="/opt/ros/galactic" \
    -DSETUPTOOLS_DEB_LAYOUT=OFF \
    ..

%make_build

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/galactic/setup.sh" ]; then . "/opt/ros/galactic/setup.sh"; fi
%make_install -C obj-%{_target_platform}

%if 0%{?with_tests}
%check
# Look for a Makefile target with a name indicating that it runs tests
TEST_TARGET=$(%__make -qp -C obj-%{_target_platform} | sed "s/^\(test\|check\):.*/\\1/;t f;d;:f;q0")
if [ -n "$TEST_TARGET" ]; then
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/galactic/setup.sh" ]; then . "/opt/ros/galactic/setup.sh"; fi
CTEST_OUTPUT_ON_FAILURE=1 \
    %make_build -C obj-%{_target_platform} $TEST_TARGET || echo "RPM TESTS FAILED"
else echo "RPM TESTS SKIPPED"; fi
%endif

%files
/opt/ros/galactic

%changelog
* Thu May 20 2021 Steve Macenski <stevenmacenski@gmail.com> - 2.5.0-2
- Autogenerated by Bloom

