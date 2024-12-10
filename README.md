# **Open Manipulator Pro Gazebo**  
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## **Overview**
Repository to Gazebo simulation files of the Botanic Grasping project.

### **License**

This project is licensed under the [MIT License](LICENSE).

**Author**: Deivid Gomes\
**Affiliation**: Brazilian Institute of Robotics - BIR\
**Maintainer**: Deivid Gomes, deivid.silva@fbter.org.br

## **Requirements**

The `open_manipulator_pro_gazebo` package has been tested under:

- ROS2 [`Humble Hawksbill`](https://docs.ros.org/en/humble/Releases/Release-Humble-Hawksbill.html), Gazebo Classic and Ubuntu 22.04 LTS (Jammy Jellyfish).

## **Installation**
1. Clone this repository into your workspace:
    ```bash
    cd ~/ros2_ws/src
    git clone https://github.com/deividG0/open_manipulator_pro_gazebo.git
    ```
2. Install dependencies:
    ```bash
    cd ~/ros2_ws
    rosdep install --from-paths src --ignore-src -r -y
    ```
3. Build the workspace:
    ```bash
    cd ~/ros2_ws
    colcon build --symlink-install --event-handlers console_direct+
    ```

## **Usage**

For launch, run the following command:

```
ros2 launch open_manipulator_pro_gazebo simulation.launch.py
```

### **Contributing**

To contribute to this package, you can either [open an issue](https://github.com/deividG0/open_manipulator_pro_gazebo/issues) describing the desired subject or develop the feature yourself and [submit a pull request](https://github.com/deividG0/open_manipulator_pro_gazebo/pulls) to the main branch.

If you choose to develop the feature yourself, please adhere to the [ROS 2 Code style and language] guidelines to improve code readability and maintainability.

