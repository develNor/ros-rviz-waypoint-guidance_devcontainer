#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e
# Print commands and their arguments as they are executed.
set -x

# it is necessary to create the directory before mounting it.
# Unfortunately it not possible to save this directory in git, because it has to be completely empty.
# So it would not work, if there is a .gitkeep file in it.
mkdir -p catkin-ws-src_bind-volume

git clone git@ids-git.fzi.de:go914/demo-ros-pkg.git catkin-ws-src_bind-volume/rviz-waypoint-gui_ros1