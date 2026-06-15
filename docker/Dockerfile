FROM osrf/ros:jazzy-desktop-full

ENV DEBIAN_FRONTEND=noninteractive


# --- System & development tools ---
RUN apt-get update && apt-get install -y \
    git \
    nano \
    python3-pip \
    python3-pygame \
    x11-apps \
    && rm -rf /var/lib/apt/lists/*

    
# --- ROS packages for Helmsman ---
RUN apt-get update && apt-get install -y \
    ros-jazzy-navigation2 \
    ros-jazzy-nav2-bringup \
    ros-jazzy-slam-toolbox \
    ros-jazzy-robot-localization \
    ros-jazzy-ros-gz \ 
    ros-jazzy-teleop-twist-keyboard \
    ros-jazzy-xacro \
    ros-jazzy-joint-state-publisher-gui \
    && rm -rf /var/lib/apt/lists/*

# --- Non-root user (UID 1000 matches the host user; 'ubuntu' ships with the base image) ---
RUN apt-get update && apt-get install -y sudo \
    && echo "ubuntu ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/ubuntu \
    && rm -rf /var/lib/apt/lists/*

USER ubuntu


RUN echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc \
    && echo "[ -f /ws/install/setup.bash ] && source /ws/install/setup.bash" >> ~/.bashrc

WORKDIR /ws
CMD ["bash"]