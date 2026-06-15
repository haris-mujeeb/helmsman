import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    pkg_nav = get_package_share_directory("helmsman_navigation")
    pkg_slam = get_package_share_directory("slam_toolbox")

    slam_params = os.path.join(pkg_nav, "config", "slam_async.yaml")

    use_sim_time = LaunchConfiguration("use_sim_time")
    declare_sim_time = DeclareLaunchArgument(
        "use_sim_time",
        default_value="true",
        description="Use Gazebo's /clock instead of wall time",
    )

    # Reuse slam_toolbox's maintained launch file (it drives the lifecycle
    # node through configure -> activate for us) and feed it our params.
    slam = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_slam, "launch", "online_async_launch.py")
        ),
        launch_arguments={
            "slam_params_file": slam_params,
            "use_sim_time": use_sim_time,
        }.items(),
    )

    return LaunchDescription([declare_sim_time, slam])
