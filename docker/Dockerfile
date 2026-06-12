FROM osrf/ros:jazzy-desktop-full

ENV DEBIAN_FRONTEND=noninteractive


# --- System & development tools ---
RUN apt-get update && apt-get install -y \
    git \
    nano \
    python3-pip \
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
    && rm -rf /var/lib/apt/lists/*

WORKDIR /ws

RUN echo "source /opt/ros/jazzy/setup.bash" >> /root/.bashrc \
    && echo "[ -f /ws/install/setup.bash ] && source /ws/install/setup.bash" >> /root/.bashrc

CMD ["bash"]