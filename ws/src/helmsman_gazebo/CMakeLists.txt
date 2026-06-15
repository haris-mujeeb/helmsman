cmake_minimum_required(VERSION 3.8)
project(helmsman_gazebo)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY worlds launch config rviz
  DESTINATION share/${PROJECT_NAME}
)

install(PROGRAMS
  scripts/keyboard_teleop.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME keyboard_teleop
)


ament_package()