import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command


def generate_launch_description():
    pkg_gazebo = get_package_share_directory("helmsman_gazebo")
    pkg_desc = get_package_share_directory("helmsman_description")
    pkg_ros_gz = get_package_share_directory("ros_gz_sim")

    world_path = os.path.join(pkg_gazebo, "worlds", "empty_helmsman.sdf")
    xacro_path = os.path.join(pkg_desc, "urdf", "helmsman.urdf.xacro")
    bridge_config = os.path.join(pkg_gazebo, "config", "bridge.yaml")

    robot_description = ParameterValue(Command(["xacro ", xacro_path]), value_type=str)

    # 1. Start Gazebo with our world
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz, "launch", "gz_sim.launch.py")
        ),
        launch_arguments={"gz_args": f"-r {world_path}"}.items(),
    )

    # 2. Publish the robot description + TF tree
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": robot_description, "use_sim_time": True}],
    )

    # 3. Spawn the robot into Gazebo from the /robot_description topic
    spawn = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=["-topic", "robot_description", "-name", "helmsman", "-z", "0.0"],
        output="screen",
    )

    # 4. Bridge topics between Gazebo and ROS2
    bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=["--ros-args", "-p", f"config_file:={bridge_config}"],
        parameters=[{"use_sim_time": True}],
        output="screen",
    )

    return LaunchDescription([gz_sim, robot_state_publisher, spawn, bridge])
