/*
 * laser_utils
 * Copyright (c) 2019, Samsung Research America
 *
 * THE WORK (AS DEFINED BELOW) IS PROVIDED UNDER THE TERMS OF THIS CREATIVE
 * COMMONS PUBLIC LICENSE ("CCPL" OR "LICENSE"). THE WORK IS PROTECTED BY
 * COPYRIGHT AND/OR OTHER APPLICABLE LAW. ANY USE OF THE WORK OTHER THAN AS
 * AUTHORIZED UNDER THIS LICENSE OR COPYRIGHT LAW IS PROHIBITED.
 *
 * BY EXERCISING ANY RIGHTS TO THE WORK PROVIDED HERE, YOU ACCEPT AND AGREE TO
 * BE BOUND BY THE TERMS OF THIS LICENSE. THE LICENSOR GRANTS YOU THE RIGHTS
 * CONTAINED HERE IN CONSIDERATION OF YOUR ACCEPTANCE OF SUCH TERMS AND
 * CONDITIONS.
 *
 */

/* Author: Steven Macenski */

#include "slam_toolbox/laser_utils.hpp"
#include <cmath>

namespace laser_utils
{

LaserMetadata::LaserMetadata()
{
};

LaserMetadata::~LaserMetadata()
{
}

LaserMetadata::LaserMetadata(karto::LaserRangeFinder * lsr, bool invert)
{
  laser = lsr;
  inverted = invert;
};

bool LaserMetadata::isInverted() const
{
  return inverted;
}

karto::LaserRangeFinder* LaserMetadata::getLaser()
{
  return laser;
}

void LaserMetadata::invertScan(sensor_msgs::msg::LaserScan & scan) const
{
  sensor_msgs::msg::LaserScan temp;
  temp.intensities.reserve(scan.intensities.size());
  temp.ranges.reserve(scan.ranges.size());
  const bool has_intensities = scan.intensities.size() > 0 ? true : false;

  for (int i = scan.ranges.size(); i != 0; i--)
  {
    temp.ranges.push_back(scan.ranges[i]);
    if (has_intensities)
    {
      temp.intensities.push_back(scan.intensities[i]);
    }
  }

  scan.ranges = temp.ranges;
  scan.intensities = temp.intensities;
  return;
};


LaserAssistant::LaserAssistant(rclcpp::Node::SharedPtr node,
  tf2_ros::Buffer * tf, const std::string & base_frame)
  : node_(node), tf_(tf), base_frame_(base_frame)
{
};

LaserAssistant::~LaserAssistant()
{
};

LaserMetadata LaserAssistant::toLaserMetadata(sensor_msgs::msg::LaserScan scan)
{
  scan_ = scan;
  frame_ = scan_.header.frame_id;

  double mountingYaw;
  bool inverted = isInverted(mountingYaw);
  karto::LaserRangeFinder * laser = makeLaser(mountingYaw);
  LaserMetadata laserMeta(laser, inverted);
  return laserMeta;
};

karto::LaserRangeFinder* LaserAssistant::makeLaser(const double & mountingYaw)
{
  karto::LaserRangeFinder * laser = 
    karto::LaserRangeFinder::CreateLaserRangeFinder(
    karto::LaserRangeFinder_Custom, karto::Name("Custom Described Lidar"));
  laser->SetOffsetPose(karto::Pose2(laser_pose_.transform.translation.x,
    laser_pose_.transform.translation.y, mountingYaw));
  laser->SetMinimumRange(scan_.range_min);
  laser->SetMaximumRange(scan_.range_max);
  laser->SetMinimumAngle(scan_.angle_min);
  laser->SetMaximumAngle(scan_.angle_max);
  laser->SetAngularResolution(scan_.angle_increment);

  bool is_360_lidar = false;
  if ((std::fabs(scan_.angle_min + M_PI) < 1e-3) &&
    (std::fabs(scan_.angle_max - M_PI) < 1e-3))
  {
    is_360_lidar = true;
  }

  laser->SetIs360Laser(is_360_lidar);

  double max_laser_range = 25;
  max_laser_range = node_->declare_parameter("max_laser_range", max_laser_range);
  if (max_laser_range > scan_.range_max)
  {
    RCLCPP_WARN(node_->get_logger(), 
      "maximum laser range setting (%.1f m) exceeds the capabilities "
      "of the used Lidar (%.1f m)", max_laser_range, scan_.range_max);
    max_laser_range = scan_.range_max;
  }
  laser->SetRangeThreshold(max_laser_range);
  return laser;
}

bool LaserAssistant::isInverted(double & mountingYaw)
{
  geometry_msgs::msg::TransformStamped laser_ident;
  laser_ident.header.stamp = scan_.header.stamp;
  laser_ident.header.frame_id = frame_;
  laser_ident.transform.rotation.w = 1.0;

  laser_pose_ = tf_->transform(laser_ident, base_frame_);
  mountingYaw = tf2::getYaw(laser_pose_.transform.rotation);

  RCLCPP_DEBUG(node_->get_logger(), "laser %s's pose wrt base: %.3f %.3f %.3f %.3f",
    frame_.c_str(), laser_pose_.transform.translation.x,
    laser_pose_.transform.translation.y,
    laser_pose_.transform.translation.z, mountingYaw);

  geometry_msgs::msg::Vector3Stamped laser_orient;
  laser_orient.vector.z = laser_orient.vector.y = 0.;
  laser_orient.vector.z = 1 + laser_pose_.transform.translation.z;
  laser_orient.header.stamp = scan_.header.stamp;
  laser_orient.header.frame_id = base_frame_;
  laser_orient = tf_->transform(laser_orient, frame_);
  
  if (laser_orient.vector.z <= 0)
  {
    RCLCPP_DEBUG(node_->get_logger(), "laser is mounted upside-down");
    return true;
  }

  return false;
};

ScanHolder::ScanHolder(std::map<std::string, laser_utils::LaserMetadata> & lasers)
: lasers_(lasers)
{
  current_scans_ = std::make_unique<std::vector<sensor_msgs::msg::LaserScan> >();
};

ScanHolder::~ScanHolder()
{
  current_scans_.reset();
};

sensor_msgs::msg::LaserScan ScanHolder::getCorrectedScan(const int& id)
{
  sensor_msgs::msg::LaserScan scan = current_scans_->at(id);
  const laser_utils::LaserMetadata& laser = lasers_[scan.header.frame_id];
  if (laser.isInverted())
  {
    laser.invertScan(scan);
  }
  return scan;
};

void ScanHolder::addScan(const sensor_msgs::msg::LaserScan scan)
{
  current_scans_->push_back(scan);
};

} // end namespace
