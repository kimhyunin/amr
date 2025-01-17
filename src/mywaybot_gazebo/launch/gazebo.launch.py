from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
import os
import xacro
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    share_dir = get_package_share_directory('mywaybot_gazebo')

    xacro_file = os.path.join(share_dir, 'urdf', 'mywaybot.xacro')
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    robot_description_config = xacro.process_file(xacro_file)
    robot_urdf = robot_description_config.toxml()
    robot_spawn_position = [0,0,0] # x y z
    robot_spawn_rotation = [0,0,0] # r p y

    world = os.path.join(
        get_package_share_directory('aws_robomaker_bookstore_world'),
        'worlds',
        'bookstore.world'
    )
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[
            {'robot_description': robot_urdf,
             'use_sim_time' : use_sim_time}
        ],
    )

    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        parameters=[{'use_sim_time' : use_sim_time}]
    )

    gazebo_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('gazebo_ros'),
                'launch',
                'gzserver.launch.py'
            ])
        ]),
        launch_arguments={
            'pause': 'false',
            'world': world
        }.items()
    )

    gazebo_client = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('gazebo_ros'),
                'launch',
                'gzclient.launch.py'
            ])
        ])
    )

    urdf_spawn_node = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-entity', 'mywaybot',
            '-topic', 'robot_description',
            '-x', str(robot_spawn_position[0]),
            '-y', str(robot_spawn_position[1]),
            '-z', str(robot_spawn_position[2]),
            '-R', str(robot_spawn_rotation[0]),
            '-P', str(robot_spawn_rotation[1]),
            '-Y', str(robot_spawn_rotation[2]),

        ],
        output='screen'
    )

    ld = LaunchDescription()
    ld.add_action(robot_state_publisher_node)
    ld.add_action(joint_state_publisher_node)
    ld.add_action(gazebo_server)
    ld.add_action(gazebo_client)
    ld.add_action(urdf_spawn_node)

    
    return ld