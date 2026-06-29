from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='bms_sim',
            executable='battery_sim_node',
            name='battery_sim_node'
        ),
        Node(
            package='bms_sim',
            executable='bms_controller_node',
            name='bms_controller_node'
        ),
    ])
