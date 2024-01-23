%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/humble/.*$
%global __requires_exclude_from ^/opt/ros/humble/.*$

Name:           ros-humble-slam-toolbox
Version:        2.6.7
Release:        1%{?dist}%{?release_suffix}
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
Requires:       ros-humble-builtin-interfaces
Requires:       ros-humble-interactive-markers
Requires:       ros-humble-message-filters
Requires:       ros-humble-nav-msgs
Requires:       ros-humble-nav2-map-server
Requires:       ros-humble-pluginlib
Requires:       ros-humble-rclcpp
Requires:       ros-humble-rosidl-default-generators
Requires:       ros-humble-rviz-common
Requires:       ros-humble-rviz-default-plugins
Requires:       ros-humble-rviz-ogre-vendor
Requires:       ros-humble-rviz-rendering
Requires:       ros-humble-sensor-msgs
Requires:       ros-humble-std-msgs
Requires:       ros-humble-std-srvs
Requires:       ros-humble-tf2
Requires:       ros-humble-tf2-geometry-msgs
Requires:       ros-humble-tf2-ros
Requires:       ros-humble-tf2-sensor-msgs
Requires:       ros-humble-visualization-msgs
Requires:       suitesparse-devel
Requires:       tbb-devel
Requires:       ros-humble-ros-workspace
BuildRequires:  boost-devel
BuildRequires:  boost-python%{python3_pkgversion}-devel
BuildRequires:  ceres-solver-devel
BuildRequires:  eigen3-devel
BuildRequires:  lapack-devel
BuildRequires:  qt5-qtbase
BuildRequires:  qt5-qtbase-devel
BuildRequires:  ros-humble-ament-cmake
BuildRequires:  ros-humble-builtin-interfaces
BuildRequires:  ros-humble-interactive-markers
BuildRequires:  ros-humble-message-filters
BuildRequires:  ros-humble-nav-msgs
BuildRequires:  ros-humble-pluginlib
BuildRequires:  ros-humble-rclcpp
BuildRequires:  ros-humble-rosidl-default-generators
BuildRequires:  ros-humble-rviz-common
BuildRequires:  ros-humble-rviz-default-plugins
BuildRequires:  ros-humble-rviz-ogre-vendor
BuildRequires:  ros-humble-rviz-rendering
BuildRequires:  ros-humble-sensor-msgs
BuildRequires:  ros-humble-std-msgs
BuildRequires:  ros-humble-std-srvs
BuildRequires:  ros-humble-tf2
BuildRequires:  ros-humble-tf2-geometry-msgs
BuildRequires:  ros-humble-tf2-ros
BuildRequires:  ros-humble-tf2-sensor-msgs
BuildRequires:  ros-humble-visualization-msgs
BuildRequires:  suitesparse-devel
BuildRequires:  tbb-devel
BuildRequires:  ros-humble-ros-workspace
BuildRequires:  ros-humble-rosidl-typesupport-fastrtps-c
BuildRequires:  ros-humble-rosidl-typesupport-fastrtps-cpp
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Provides:       %{name}-runtime = %{version}-%{release}
Provides:       ros-humble-rosidl-interface-packages(member)

%if 0%{?with_tests}
BuildRequires:  ros-humble-ament-cmake-cpplint
BuildRequires:  ros-humble-ament-cmake-flake8
BuildRequires:  ros-humble-ament-cmake-gtest
BuildRequires:  ros-humble-ament-cmake-uncrustify
BuildRequires:  ros-humble-ament-lint-auto
BuildRequires:  ros-humble-launch
BuildRequires:  ros-humble-launch-testing
%endif

%if 0%{?with_weak_deps}
Supplements:    ros-humble-rosidl-interface-packages(all)
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
if [ -f "/opt/ros/humble/setup.sh" ]; then . "/opt/ros/humble/setup.sh"; fi
mkdir -p .obj-%{_target_platform} && cd .obj-%{_target_platform}
%cmake3 \
    -UINCLUDE_INSTALL_DIR \
    -ULIB_INSTALL_DIR \
    -USYSCONF_INSTALL_DIR \
    -USHARE_INSTALL_PREFIX \
    -ULIB_SUFFIX \
    -DCMAKE_INSTALL_PREFIX="/opt/ros/humble" \
    -DAMENT_PREFIX_PATH="/opt/ros/humble" \
    -DCMAKE_PREFIX_PATH="/opt/ros/humble" \
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
if [ -f "/opt/ros/humble/setup.sh" ]; then . "/opt/ros/humble/setup.sh"; fi
%make_install -C .obj-%{_target_platform}

%if 0%{?with_tests}
%check
# Look for a Makefile target with a name indicating that it runs tests
TEST_TARGET=$(%__make -qp -C .obj-%{_target_platform} | sed "s/^\(test\|check\):.*/\\1/;t f;d;:f;q0")
if [ -n "$TEST_TARGET" ]; then
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/humble/setup.sh" ]; then . "/opt/ros/humble/setup.sh"; fi
CTEST_OUTPUT_ON_FAILURE=1 \
    %make_build -C .obj-%{_target_platform} $TEST_TARGET || echo "RPM TESTS FAILED"
else echo "RPM TESTS SKIPPED"; fi
%endif

%files
/opt/ros/humble

%changelog
* Tue Jan 23 2024 Steve Macenski <stevenmacenski@gmail.com> - 2.6.7-1
- Autogenerated by Bloom

* Mon Sep 25 2023 Steve Macenski <stevenmacenski@gmail.com> - 2.6.6-1
- Autogenerated by Bloom

* Fri Aug 04 2023 Steve Macenski <stevenmacenski@gmail.com> - 2.6.5-1
- Autogenerated by Bloom

* Tue Dec 20 2022 Steve Macenski <stevenmacenski@gmail.com> - 2.6.4-1
- Autogenerated by Bloom

* Wed Nov 09 2022 Steve Macenski <stevenmacenski@gmail.com> - 2.6.3-1
- Autogenerated by Bloom

* Tue Nov 08 2022 Steve Macenski <stevenmacenski@gmail.com> - 2.6.2-1
- Autogenerated by Bloom

* Wed Aug 24 2022 Steve Macenski <stevenmacenski@gmail.com> - 2.6.1-1
- Autogenerated by Bloom

* Mon Jun 06 2022 Steve Macenski <stevenmacenski@gmail.com> - 2.6.0-2
- Autogenerated by Bloom

