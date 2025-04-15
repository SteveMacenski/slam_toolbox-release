%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/jazzy/.*$
%global __requires_exclude_from ^/opt/ros/jazzy/.*$

Name:           ros-jazzy-slam-toolbox
Version:        2.8.3
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
Requires:       ros-jazzy-bond
Requires:       ros-jazzy-bondcpp
Requires:       ros-jazzy-builtin-interfaces
Requires:       ros-jazzy-interactive-markers
Requires:       ros-jazzy-lifecycle-msgs
Requires:       ros-jazzy-message-filters
Requires:       ros-jazzy-nav-msgs
Requires:       ros-jazzy-pluginlib
Requires:       ros-jazzy-rclcpp
Requires:       ros-jazzy-rclcpp-lifecycle
Requires:       ros-jazzy-rosidl-default-generators
Requires:       ros-jazzy-rviz-common
Requires:       ros-jazzy-rviz-default-plugins
Requires:       ros-jazzy-rviz-ogre-vendor
Requires:       ros-jazzy-rviz-rendering
Requires:       ros-jazzy-sensor-msgs
Requires:       ros-jazzy-std-msgs
Requires:       ros-jazzy-std-srvs
Requires:       ros-jazzy-tf2
Requires:       ros-jazzy-tf2-geometry-msgs
Requires:       ros-jazzy-tf2-ros
Requires:       ros-jazzy-tf2-sensor-msgs
Requires:       ros-jazzy-visualization-msgs
Requires:       suitesparse-devel
Requires:       tbb-devel
Requires:       ros-jazzy-ros-workspace
BuildRequires:  boost-devel
BuildRequires:  boost-python%{python3_pkgversion}-devel
BuildRequires:  ceres-solver-devel
BuildRequires:  eigen3-devel
BuildRequires:  flexiblas-devel
BuildRequires:  lapack-devel
BuildRequires:  qt5-qtbase
BuildRequires:  qt5-qtbase-devel
BuildRequires:  ros-jazzy-ament-cmake
BuildRequires:  ros-jazzy-bond
BuildRequires:  ros-jazzy-bondcpp
BuildRequires:  ros-jazzy-builtin-interfaces
BuildRequires:  ros-jazzy-interactive-markers
BuildRequires:  ros-jazzy-lifecycle-msgs
BuildRequires:  ros-jazzy-message-filters
BuildRequires:  ros-jazzy-nav-msgs
BuildRequires:  ros-jazzy-pluginlib
BuildRequires:  ros-jazzy-rclcpp
BuildRequires:  ros-jazzy-rclcpp-lifecycle
BuildRequires:  ros-jazzy-rosidl-default-generators
BuildRequires:  ros-jazzy-rviz-common
BuildRequires:  ros-jazzy-rviz-default-plugins
BuildRequires:  ros-jazzy-rviz-ogre-vendor
BuildRequires:  ros-jazzy-rviz-rendering
BuildRequires:  ros-jazzy-sensor-msgs
BuildRequires:  ros-jazzy-std-msgs
BuildRequires:  ros-jazzy-std-srvs
BuildRequires:  ros-jazzy-tf2
BuildRequires:  ros-jazzy-tf2-geometry-msgs
BuildRequires:  ros-jazzy-tf2-ros
BuildRequires:  ros-jazzy-tf2-sensor-msgs
BuildRequires:  ros-jazzy-visualization-msgs
BuildRequires:  suitesparse-devel
BuildRequires:  tbb-devel
BuildRequires:  ros-jazzy-ros-workspace
BuildRequires:  ros-jazzy-rosidl-typesupport-fastrtps-c
BuildRequires:  ros-jazzy-rosidl-typesupport-fastrtps-cpp
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Provides:       %{name}-runtime = %{version}-%{release}
Provides:       ros-jazzy-rosidl-interface-packages(member)

%if 0%{?with_tests}
BuildRequires:  ros-jazzy-ament-cmake-cpplint
BuildRequires:  ros-jazzy-ament-cmake-flake8
BuildRequires:  ros-jazzy-ament-cmake-gtest
BuildRequires:  ros-jazzy-ament-cmake-uncrustify
BuildRequires:  ros-jazzy-ament-lint-auto
BuildRequires:  ros-jazzy-launch
BuildRequires:  ros-jazzy-launch-testing
%endif

%if 0%{?with_weak_deps}
Supplements:    ros-jazzy-rosidl-interface-packages(all)
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
if [ -f "/opt/ros/jazzy/setup.sh" ]; then . "/opt/ros/jazzy/setup.sh"; fi
mkdir -p .obj-%{_target_platform} && cd .obj-%{_target_platform}
%cmake3 \
    -UINCLUDE_INSTALL_DIR \
    -ULIB_INSTALL_DIR \
    -USYSCONF_INSTALL_DIR \
    -USHARE_INSTALL_PREFIX \
    -ULIB_SUFFIX \
    -DCMAKE_INSTALL_PREFIX="/opt/ros/jazzy" \
    -DAMENT_PREFIX_PATH="/opt/ros/jazzy" \
    -DCMAKE_PREFIX_PATH="/opt/ros/jazzy" \
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
if [ -f "/opt/ros/jazzy/setup.sh" ]; then . "/opt/ros/jazzy/setup.sh"; fi
%make_install -C .obj-%{_target_platform}

%if 0%{?with_tests}
%check
# Look for a Makefile target with a name indicating that it runs tests
TEST_TARGET=$(%__make -qp -C .obj-%{_target_platform} | sed "s/^\(test\|check\):.*/\\1/;t f;d;:f;q0")
if [ -n "$TEST_TARGET" ]; then
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/jazzy/setup.sh" ]; then . "/opt/ros/jazzy/setup.sh"; fi
CTEST_OUTPUT_ON_FAILURE=1 \
    %make_build -C .obj-%{_target_platform} $TEST_TARGET || echo "RPM TESTS FAILED"
else echo "RPM TESTS SKIPPED"; fi
%endif

%files
/opt/ros/jazzy

%changelog
* Tue Apr 15 2025 Steve Macenski <stevenmacenski@gmail.com> - 2.8.3-1
- Autogenerated by Bloom

* Fri Dec 13 2024 Steve Macenski <stevenmacenski@gmail.com> - 2.8.2-1
- Autogenerated by Bloom

* Tue Jun 25 2024 Steve Macenski <stevenmacenski@gmail.com> - 2.8.1-2
- Autogenerated by Bloom

* Tue Jun 25 2024 Steve Macenski <stevenmacenski@gmail.com> - 2.8.1-1
- Autogenerated by Bloom

