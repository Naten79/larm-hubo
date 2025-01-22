# Group repository for the UV-LARM 
**Group 27**
## Members:
Antoine GUEUDET  
Tanguy HIS  
Nathan DELAUNAY  
## Description
This deposit contains the project of the UV LARM. The goal was to create a robot with safe moves detecting ghosts while exploring an area and marking them in a map. 
## Steps to start a simulation  
#### Step 1 : Select the workspace
```bash
cd ~/ros_space
```
#### Step 2 : Clone the simulator deposit
```bash
git clone https://github.com/imt-mobisyst/pkg-tsim
```
#### Step 3 : Clone the project
```bash
git clone https://github.com/Naten79/larm-hubo.git
```
#### Step 4 : Build and source the environement 
```bash
colcon build
source ./install/setup.bash
```
#### Step 5 : Launch the simulation
```bash
ros2 launch grp_pibot27 simulation_v1_launch.yaml
```

## Steps to move the robot:
#### Step 1 : Clone and install ultralytics to use YOLO
```bash
cd
git clone https://github.com/ultralytics/ultralytics.git
cd ultralytics
pip install -e .
```
#### Step 2 : Select the workspace
```bash
cd ~/ros_space
```
#### Step 3 : Clone the project
```bash
git clone https://github.com/Naten79/larm-hubo.git
```
#### Step 4 : Build and source the environement
```bash
colcon build
source ./install/setup.bash
```
#### Step 5 : Launch the simulation
```bash
ros2 launch grp_pibot27 tbot_v1_launch.yaml
```