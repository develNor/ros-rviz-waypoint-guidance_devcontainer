# Windows Setup
- install WSL 2
- install Docker Desktop with WSL 2 Backend
- install VSC with extensions: "Dev Containers", "WSL"
- in WSL:
    - install and setup xhost
        - `sudo apt-get update`
        - `sudo apt-get install x11-server-utils`
        - `xhost +local:docker`
    - add startup of ssh-agent to bashrc: `'eval "$(ssh-agent)"' >> ~/.bashrc`
        - (prevents error because of empty SSH_AUTH_SOCK)
    - get code `git clone https://github.com/develNor/ros-rviz-waypoint-guidance_devcontainer.git`

# Start the demo
- (For Windows: Start Docker Desktop)
- open this repository in VSC
- `Show all commands`/`Ctrl+Shift+P` -> `Dev-Containers: Reopen in Container`
- in integrated Terminal (`Ctrl+Shift+ö`):
    - `cd ~/catkin_ws && catkin_make`
    - `roslaunch rviz-waypoint-gui_ros1 demo.launch`

# How does the demo work?
Click (=Publish) at least two points in rviz. The Node will then create a tube connecting one point with the other