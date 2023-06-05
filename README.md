# Prerequisits
- install WSL2 (only for Windows)
    - WSL is often preinstalled on windows
    - It could be the case that WSL 1 is installed and has to be upgraded
    - check and upgrade: https://learn.microsoft.com/en-us/windows/wsl/install#upgrade-version-from-wsl-1-to-wsl-2
    - particularly old versions of windows require a manual installation of WSL2: https://learn.microsoft.com/de-de/windows/wsl/install-manual#step-4---download-the-linux-kernel-update-package
- Current installation of `docker` and `docker compose`
    - Linux: install docker engine (tested with Decker Engine 24.0.2, Docker Compose version v2.18.1)
    - Windows: install docker desktop (tested with Docker Desktop 4.20)
    - **Note: Docker compose v1 will not work**
- enable WSL2 backend for Docker (only for Windows)
    - should be the default when installing docker
- setup ssh-agent for later forwarding (only for Windows)
    - (Motivation: prevents error because of empty SSH_AUTH_SOCK)
    - enable SSH Agent automatically on Windows
        - start PowerShell **with administrator rights**, then
        - `Set-Service ssh-agent -StartupType Automatic`
        - `Start-Service ssh-agent`
        - `Get-Service ssh-agent`
    - startup ssh-agent in WSL automatically in the background
        - open WSL
        - add startup of ssh-agent to bashrc via `echo 'eval "$(ssh-agent)"' >> ~/.bashrc`
- enable X11 Forwarding for Docker
    - `sudo apt-get update` (only for Windows)
    - `sudo apt-get install x11-server-utils` (only for Windows)
    - `xhost +local:docker`
- VSC is installed and has the extension 
    - "Dev Container"
    - "WSL" (only for Windows)
- get this repository: `git clone https://github.com/develNor/ros-rviz-waypoint-guidance_devcontainer.git` 
    - (For Windows: execute inside WSL)

# Start the demo via VSC (recommended)
- (For Windows: Start Docker Desktop)
- Open VSC
- (For Windows: Connect to WSL)
- open this repository
- `Show all commands` (`Ctrl+Shift+P`) -> `Dev-Containers: Reopen in Container`
- two options:
    - **manual**    
        - in integrated Terminal (`Ctrl+Shift+ö`):
            - `cd ~/catkin_ws && catkin_make`
            - `roslaunch rviz-waypoint-gui_ros1 demo.launch`
    - **shortcut**
        - `Show all commands` (`Ctrl+Shift+P`) -> `Tasks: Run Test Task`

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