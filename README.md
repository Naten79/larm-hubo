# grp- repository for the UV-LARM

# Start a simulation
cd ~/ros_space
git clone https://github.com/imt-mobisyst/pkg-tsim
colcon build
source ./install/setup.bash
git clone https://github.com/Naten79/larm-hubo.git
cd larm-hubo
colcon build 
source ./install/setup.bash
ros2 launch grp_pibot27 simulation_v1_launch.yaml

# Move the robot
cd ~/ros_space
git clone https://github.com/Naten79/larm-hubo.git
cd larm-hubo
colcon build 
source ./install/setup.bash
ros2 launch grp_pibot27 tbot_v1_launch.yaml