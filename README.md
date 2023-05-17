# Start the demo
in VSC
- "Dev-Containers: Reopen in Container"
in integrated Terminal
- `cd ~/catkin_ws && catkin_make`
- `roslaunch rviz-waypoint-gui_ros1 demo.launch`

# How does the demo work?
Click (=Publish) at least two points in rviz. The Node will then create a tube connecting one point with the other