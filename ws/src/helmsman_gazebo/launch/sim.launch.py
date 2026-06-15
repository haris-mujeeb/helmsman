import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    IncludeLaunchDescription,
    DeclareLaunchArgument,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command, LaunchConfiguration
from launch.conditions import IfCondition
import tempfile
import xacro


def generate_launch_description():
    pkg_gazebo = get_package_share_directory("helmsman_gazebo")
    pkg_desc = get_package_share_directory("helmsman_description")
    pkg_ros_gz = get_package_share_directory("ros_gz_sim")

    world_path = os.path.join(pkg_gazebo, "worlds", "empty_helmsman.sdf")
    xacro_path = os.path.join(pkg_desc, "urdf", "helmsman.urdf.xacro")
    bridge_config = os.path.join(pkg_gazebo, "config", "bridge.yaml")

    robot_description = ParameterValue(Command(["xacro ", xacro_path]), value_type=str)

    rviz_config = os.path.join(pkg_gazebo, "rviz", "helmsman.rviz")

    world_xacro = os.path.join(pkg_gazebo, "worlds", "warehouse.sdf.xacro")
    # Process the xacro world into a temporary plain SDF
    world_sdf = os.path.join(tempfile.gettempdir(), "helmsman_warehouse.sdf")
    doc = xacro.process_file(world_xacro)
    with open(world_sdf, "w") as f:
        f.write(doc.toxml())

    # 1. Start Gazebo with our world
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz, "launch", "gz_sim.launch.py")
        ),
        launch_arguments={"gz_args": f"-r {world_sdf}"}.items(),
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
        arguments=["-topic", "robot_description", "-name", "helmsman", "-z", "0.15"],
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

    use_rviz = LaunchConfiguration("rviz")
    declare_rviz = DeclareLaunchArgument(
        "rviz", default_value="true", description="Launch RViz with saved config"
    )

    rviz = Node(
        package="rviz2",
        executable="rviz2",
        arguments=["-d", rviz_config],
        parameters=[{"use_sim_time": True}],
        condition=IfCondition(use_rviz),
        output="screen",
    )

    declare_teleop = DeclareLaunchArgument(
        "teleop",
        default_value="true",
        description="Open the hold-to-drive keyboard teleop window",
    )

    teleop = Node(
        package="helmsman_gazebo",
        executable="keyboard_teleop",
        name="keyboard_teleop",
        parameters=[{"linear_speed": 0.4, "angular_speed": 0.8}],
        condition=IfCondition(LaunchConfiguration("teleop")),
        output="screen",
    )

    return LaunchDescription(
        [
            declare_teleop,
            declare_rviz,
            gz_sim,
            robot_state_publisher,
            spawn,
            bridge,
            rviz,
            teleop,
        ]
    )
