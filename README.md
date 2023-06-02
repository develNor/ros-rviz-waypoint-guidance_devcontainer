# Windows Setup
- install WSL 2
- install Docker Desktop with WSL 2 Backend
- install VSC with extensions: "Dev Containers", "WSL"
- in WSL-Terminal:
    - install and setup xhost
        - `sudo apt-get update`
        - `sudo apt-get install x11-server-utils`
        - `xhost +local:docker`
    - add startup of ssh-agent to bashrc: `echo 'eval "$(ssh-agent)"' >> ~/.bashrc`
        - (prevents error because of empty SSH_AUTH_SOCK)
    - get code `git clone https://github.com/develNor/ros-rviz-waypoint-guidance_devcontainer.git`

# Start the demo via VSC (recommended)
- (For Windows: Start Docker Desktop)
- Open VSC
- (For Windows: Connect to WSL)
- open this repository
- `Show all commands`/`Ctrl+Shift+P` -> `Dev-Containers: Reopen in Container`
- two options:
    - **manuell**    
        - in integrated Terminal (`Ctrl+Shift+ö`):
            - `cd ~/catkin_ws && catkin_make`
            - `roslaunch rviz-waypoint-gui_ros1 demo.launch`
    - **shortcut**
        - `Show all commands`/`Ctrl+Shift+P` -> `Tasks: Run Test Task`

# Start the demo via CLI (e.g. for debugging)
- (For Windows: Start Docker Desktop)
- (For Windows: Use WSL-Terminal)
- `cd path/to/ros-rviz-waypoint-guidance_devcontainer`
- `./build_docker-compose.sh`
- `./up_container.sh`
- `./start_terminal.sh`
    - (now you are inside the docker container:)
    - `cd ~/catkin_ws && catkin_make`
    - `roslaunch rviz-waypoint-gui_ros1 demo.launch`

# How does the demo work?
Click (=Publish) at least two points in rviz. The Node will then create a tube connecting one point with the other