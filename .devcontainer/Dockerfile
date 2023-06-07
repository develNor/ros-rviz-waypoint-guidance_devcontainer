# Use the official image for ROS Noetic under Ubuntu 20.04
FROM osrf/ros:noetic-desktop-full-focal


####################################################################################################
############# Dockerfile Settings ##################################################################
####################################################################################################

# Add non-root user
ENV USERNAME=myuser
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID $USERNAME \
  && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
  && apt-get update \
  && apt-get -y install sudo \
   # [Optional] Add sudo support for the non-root user
  && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME\
  && chmod 0440 /etc/sudoers.d/$USERNAME \
   # Clean up
  && rm -rf /var/lib/apt/lists/*

# Use the non-root user in this script
USER ${USERNAME}:${USERNAME}

WORKDIR /home/${USERNAME}/


####################################################################################################
############# Install Container Setup ##############################################################
####################################################################################################

# install git and ssh
RUN sudo apt-get update && sudo apt-get -y install \
    git \
    ssh \
  && sudo rm -rf /var/lib/apt/lists/*


####################################################################################################
############# ROS configuration ####################################################################
####################################################################################################

RUN mkdir -p ~/catkin_ws/src
RUN /bin/bash -c "source /opt/ros/${ROS_DISTRO}/setup.bash; cd ~/catkin_ws && catkin_make"

## Source ROS in bash
RUN echo 'source /opt/ros/$ROS_DISTRO/setup.bash' >> /home/${USERNAME}/.bashrc
RUN echo 'source ~/catkin_ws/devel/setup.bash' >> /home/${USERNAME}/.bashrc


####################################################################################################
############# Use-Case specific packages ###########################################################
####################################################################################################

RUN sudo apt-get update && sudo apt-get -y install \
    python-is-python3 \
    python3-shapely \
    python3-scipy \
    ros-$ROS_DISTRO-foxglove-bridge \
  && sudo rm -rf /var/lib/apt/lists/*


####################################################################################################
############# Quality of Life ######################################################################
####################################################################################################

COPY to-be-copied/.vscode /home/${USERNAME}/.vscode