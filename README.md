[README.md](https://github.com/user-attachments/files/29459857/README.md)
# bms_sim

A simple ROS 2 Jazzy simulation package for a Battery Management System (BMS). The package includes:

- a battery simulation node that publishes synthetic cell voltages, temperature, current, and state of charge (SOC)
- a controller node that subscribes to the simulated cell data and publishes fault status, contactor commands, and balancing commands
- an optional launch file that starts both nodes together

## Overview

This project is intended for testing and demonstration of basic BMS behavior in a ROS 2 environment. It is useful for learning ROS 2 topics, publishers/subscribers, and simple control logic without hardware.

## Package contents

- `bms_sim/battery_sim_node.py` — publishes simulated battery measurements
- `bms_sim/bms_controller_node.py` — evaluates the battery state and publishes control outputs
- `launch/bms_sim.launch.py` — launches both nodes together

## Requirements

- Ubuntu 24.04 or a compatible Linux environment
- ROS 2 Jazzy installed
- Python 3
- `colcon`
- `ament` build tools

## Installation

If you do not already have a ROS 2 workspace:

```bash
mkdir -p ~/bms_ros2_ws/src
cd ~/bms_ros2_ws/src
git clone <your-repo-url> bms_sim
```

If you already have a workspace, place this package inside the `src` directory of that workspace.

## Build

```bash
cd ~/bms_ros2_ws
source /opt/ros/jazzy/setup.bash
colcon build --packages-select bms_sim
```

## Run

Source the workspace after building:

```bash
source ~/bms_ros2_ws/install/setup.bash
```

Run the nodes separately:

```bash
ros2 run bms_sim battery_sim_node
ros2 run bms_sim bms_controller_node
```

Or launch both at once:

```bash
ros2 launch bms_sim bms_sim.launch.py
```

## ROS 2 topics

The simulation publishes and subscribes to the following topics:

- `/battery/cell_voltages` — `std_msgs/Float32MultiArray`
- `/battery/temperature` — `std_msgs/Float32`
- `/battery/current` — `std_msgs/Float32`
- `/battery/soc` — `std_msgs/Float32`
- `/bms/fault_status` — `std_msgs/String`
- `/bms/balance_command` — `std_msgs/Float32MultiArray`
- `/bms/contactor_command` — `std_msgs/String`

You can inspect them with:

```bash
ros2 topic list
ros2 topic echo /bms/fault_status
ros2 topic echo /bms/contactor_command
```

## Troubleshooting

### ROS 2 environment not sourced

If commands such as `ros2` or `colcon` are not found, source your ROS 2 setup script:

```bash
source /opt/ros/jazzy/setup.bash
```

### Package not found after build

If `ros2 run bms_sim ...` fails, source the workspace setup file again:

```bash
source ~/bms_ros2_ws/install/setup.bash
```

### Build errors

Make sure your workspace is clean and dependencies are available:

```bash
cd ~/bms_ros2_ws
colcon build --packages-select bms_sim --cmake-clean-cache
```

## GitHub setup

Initialize a new Git repository from the workspace root:

```bash
git init
git add .
git commit -m "Initial commit"
```

Then connect to GitHub and push:

```bash
git remote add origin <your-github-repo-url>
git branch -M main
git push -u origin main
```
