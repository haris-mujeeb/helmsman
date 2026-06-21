import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
  use_slam = LaunchConfiguration('use_slam')
  use_sim_time = LaunchConfiguration("use_sim_time")

  use_slam_arg = DeclareLaunchArgument('use_slam', default_value="false")
  declare_use_sim_time_arg = DeclareLaunchArgument(
    'use_sim_time',
    default_value='true',
    description='Use simulation (Gazebo) clock if true'
  )
  
  gazebo = IncludeLaunchDescription(
    os.path.join(
      get_package_share_directory("helmsman_gazebo"),
      "launch",
      "sim.launch.py"
    )
  )
  
  slam = IncludeLaunchDescription(
    os.path.join(
      get_package_share_directory("helmsman_navigation"),
      "launch",
      "slam.launch.py"
    ),
    condition=IfCondition(use_slam)
  )
  
  localization = IncludeLaunchDescription(
    os.path.join(
      get_package_share_directory("helmsman_navigation"),
      "launch",
      "localization.launch.py"
    ),
    condition=UnlessCondition(use_slam)
  )
  
  return LaunchDescription([
    use_slam_arg,
    declare_use_sim_time_arg,
    gazebo,
    slam,
    localization,
    ])