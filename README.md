
# AMR (Autonomous Mobile Robot) Project

![Platform](https://img.shields.io/badge/platform-ROS2-blue)
![Language](https://img.shields.io/badge/language-Python-green)

## Overview
이 프로젝트는 현재 **개발 진행 중**으로, 지속적으로 업데이트 되고있습니다

이 프로젝트는 **메카넘 휠**을 장착하여 **전방향 이동**이 가능한 **자율주행 로봇**을 개발하고 있습니다.
현재 로봇에는 하나의 LIDAR와 IMU 센서가 장착되어 있어 지도 작성, 위치 추정, 그리고 경로 계획 등 다양한 작업을 수행할 수 있습니다.

추후 **카메라**와 **추가 센서**를 장착하여 로봇의 기능과 적응력을 더욱 확장할 계획입니다. 

---

## Table of Contents

- [AMR (Autonomous Mobile Robot) Project](#amr-autonomous-mobile-robot-project)
  - [Overview](#overview)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)

---

## Installation

Follow these steps to set up the project:

1. Clone this repository:
   ```bash
   cd workspace/src
   git clone https://github.com/kimhyunin/amr.git
   colcon build  

## Hardware
[BOM LIST](https://docs.google.com/spreadsheets/d/17i33JBXEkXfOwazE9-yJbk71xQYlvXrB8qZKd1UBQDE/edit?usp=sharing)
 
## Software Requirements

-   **Operating System**: Ubuntu 22.04 (ROS2 Humble)
-   **Programming Languages**: Python
-   **Libraries/Tools**:
    -   ROS2 Humble
    -   RViz2 (for visualization)
    -   Gazebo (for simulation)

## Usage

1.  Launch the Gazebo Simulation
```bash
ros2 launch mywaybot_gazebo gazebo.launch.py
```
2.  run to Move robot
```bash
ros2 run mywaybot_command omni_teleop_keyboard
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

3.  Launch the mapping (Cartographer)
```bash
ros2 launch mywaybot_slam cartographer_launch.py open_rviz:=true use_sim_time:=true
```

4. Map save
```bash
cd your_ws/mywaybot_nav/map
ros2 run nav2_map_server map_saver_cli -f filename
```

