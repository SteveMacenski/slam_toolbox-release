%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/iron/.*$
%global __requires_exclude_from ^/opt/ros/iron/.*$

Name:           ros-iron-slam-toolbox
Version:        2.7.2
Release:        1%{?dist}%{?release_suffix}
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
Requires:       ros-iron-builtin-interfaces
Requires:       ros-iron-interactive-markers
Requires:       ros-iron-message-filters
Requires:       ros-iron-nav-msgs
Requires:       ros-iron-nav2-map-server
Requires:       ros-iron-pluginlib
Requires:       ros-iron-rclcpp
Requires:       ros-iron-rosidl-default-generators
Requires:       ros-iron-rviz-common
Requires:       ros-iron-rviz-default-plugins
Requires:       ros-iron-rviz-ogre-vendor
Requires:       ros-iron-rviz-rendering
Requires:       ros-iron-sensor-msgs
Requires:       ros-iron-std-msgs
Requires:       ros-iron-std-srvs
Requires:       ros-iron-tf2
Requires:       ros-iron-tf2-geometry-msgs
Requires:       ros-iron-tf2-ros
Requires:       ros-iron-tf2-sensor-msgs
Requires:       ros-iron-visualization-msgs
Requires:       suitesparse-devel
Requires:       tbb-devel
Requires:       ros-iron-ros-workspace
BuildRequires:  boost-devel
BuildRequires:  boost-python%{python3_pkgversion}-devel
BuildRequires:  ceres-solver-devel
BuildRequires:  eigen3-devel
BuildRequires:  flexiblas-devel
BuildRequires:  lapack-devel
BuildRequires:  qt5-qtbase
BuildRequires:  qt5-qtbase-devel
BuildRequires:  ros-iron-ament-cmake
BuildRequires:  ros-iron-builtin-interfaces
BuildRequires:  ros-iron-interactive-markers
BuildRequires:  ros-iron-message-filters
BuildRequires:  ros-iron-nav-msgs
BuildRequires:  ros-iron-pluginlib
BuildRequires:  ros-iron-rclcpp
BuildRequires:  ros-iron-rosidl-default-generators
BuildRequires:  ros-iron-rviz-common
BuildRequires:  ros-iron-rviz-default-plugins
BuildRequires:  ros-iron-rviz-ogre-vendor
BuildRequires:  ros-iron-rviz-rendering
BuildRequires:  ros-iron-sensor-msgs
BuildRequires:  ros-iron-std-msgs
BuildRequires:  ros-iron-std-srvs
BuildRequires:  ros-iron-tf2
BuildRequires:  ros-iron-tf2-geometry-msgs
BuildRequires:  ros-iron-tf2-ros
BuildRequires:  ros-iron-tf2-sensor-msgs
BuildRequires:  ros-iron-visualization-msgs
BuildRequires:  suitesparse-devel
BuildRequires:  tbb-devel
BuildRequires:  ros-iron-ros-workspace
BuildRequires:  ros-iron-rosidl-typesupport-fastrtps-c
BuildRequires:  ros-iron-rosidl-typesupport-fastrtps-cpp
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Provides:       %{name}-runtime = %{version}-%{release}
Provides:       ros-iron-rosidl-interface-packages(member)

%if 0%{?with_tests}
BuildRequires:  ros-iron-ament-cmake-cpplint
BuildRequires:  ros-iron-ament-cmake-flake8
BuildRequires:  ros-iron-ament-cmake-gtest
BuildRequires:  ros-iron-ament-cmake-uncrustify
BuildRequires:  ros-iron-ament-lint-auto
BuildRequires:  ros-iron-launch
BuildRequires:  ros-iron-launch-testing
%endif

%if 0%{?with_weak_deps}
Supplements:    ros-iron-rosidl-interface-packages(all)
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
if [ -f "/opt/ros/iron/setup.sh" ]; then . "/opt/ros/iron/setup.sh"; fi
mkdir -p .obj-%{_target_platform} && cd .obj-%{_target_platform}
%cmake3 \
    -UINCLUDE_INSTALL_DIR \
    -ULIB_INSTALL_DIR \
    -USYSCONF_INSTALL_DIR \
    -USHARE_INSTALL_PREFIX \
    -ULIB_SUFFIX \
    -DCMAKE_INSTALL_PREFIX="/opt/ros/iron" \
    -DAMENT_PREFIX_PATH="/opt/ros/iron" \
    -DCMAKE_PREFIX_PATH="/opt/ros/iron" \
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
if [ -f "/opt/ros/iron/setup.sh" ]; then . "/opt/ros/iron/setup.sh"; fi
%make_install -C .obj-%{_target_platform}

%if 0%{?with_tests}
%check
# Look for a Makefile target with a name indicating that it runs tests
TEST_TARGET=$(%__make -qp -C .obj-%{_target_platform} | sed "s/^\(test\|check\):.*/\\1/;t f;d;:f;q0")
if [ -n "$TEST_TARGET" ]; then
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/iron/setup.sh" ]; then . "/opt/ros/iron/setup.sh"; fi
CTEST_OUTPUT_ON_FAILURE=1 \
    %make_build -C .obj-%{_target_platform} $TEST_TARGET || echo "RPM TESTS FAILED"
else echo "RPM TESTS SKIPPED"; fi
%endif

%files
/opt/ros/iron

%changelog
* Mon Sep 25 2023 Steve Macenski <stevenmacenski@gmail.com> - 2.7.2-1
- Autogenerated by Bloom

* Fri Aug 04 2023 Steve Macenski <stevenmacenski@gmail.com> - 2.7.1-1
- Autogenerated by Bloom

* Thu May 25 2023 Steve Macenski <stevenmacenski@gmail.com> - 2.7.0-2
- Autogenerated by Bloom

