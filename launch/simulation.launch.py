#!/usr/bin/env python3

# Copyright (c) 2024, SENAI CIMATEC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import \
    DeclareLaunchArgument, IncludeLaunchDescription, OpaqueFunction
from launch_ros.substitutions import FindPackageShare
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node


def controllers_node_launch(context, *args, **kwargs):
    controllers_group = LaunchConfiguration(
        'controllers_group').perform(context)
    nodes = []
    if controllers_group == 'trajectory':
        nodes.append(Node(
            package="controller_manager",
            executable="spawner",
            arguments=[
                "joint_trajectory_controller",
                "-c",
                "/controller_manager"
                ],
            output="screen",
        ))
    elif controllers_group == 'position':
        nodes.append(Node(
            package="controller_manager",
            executable="spawner",
            arguments=["position_controller", "-c", "/controller_manager"],
            output="screen",
        ))
    return nodes


def generate_launch_description():
    # Arguments values
    use_sim_time = LaunchConfiguration('use_sim_time', default=True)
    is_real_launch = LaunchConfiguration('is_real_launch', default=False)

    # Arguments
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value=use_sim_time,
        description='If true, use simulated clock'
    )

    controllers_group_arg = DeclareLaunchArgument(
        'controllers_group',
        default_value='trajectory',
        description='Determine the set of controllers to be launched',
        choices=['trajectory', 'position']
    )

    # Gazebo related
    world_path = os.path.join(get_package_share_directory(
        'open_manipulator_pro_gazebo'), 'worlds', 'wall_objects_done2.world'
        )

    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('gazebo_ros'),
                'launch',
                'gazebo.launch.py'])])
    )

    robot_description = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                FindPackageShare("open_manipulator_pro_description"),
                '/launch',
                '/robot_description.launch.py'
            ]
        ),
        launch_arguments={
            'is_real_launch': is_real_launch
        }.items(),
    )

    robot_spawn_node = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description',
                   '-entity', 'robot'],
        output='screen'
    )

    declare_world_cmd = DeclareLaunchArgument(
        name='world',
        default_value=world_path,
        description='Full path to the world model file to load'
    )

    return LaunchDescription([
        robot_spawn_node,
        robot_description,
        use_sim_time_arg,
        controllers_group_arg,
        Node(
            package="controller_manager",
            executable="spawner",
            arguments=[
                    "joint_state_broadcaster",
                    "--controller-manager",
                    "/controller_manager"
                    ],
            output="screen",
        ),
        Node(
            package="controller_manager",
            executable="spawner",
            arguments=["velocity_controller", "-c", "/controller_manager"],
            output="screen",
        ),
        OpaqueFunction(function=controllers_node_launch),
        declare_world_cmd,
        gazebo_launch,
    ])
