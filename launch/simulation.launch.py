import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')
    bluerov2_ignition_path = get_package_share_directory('bluerov2_ignition')
    world_path = os.path.join(
        bluerov2_ignition_path, 'worlds', 'underwater_minimal.world')
    sand_path = os.path.join(
        bluerov2_ignition_path, 'models', 'sand_heightmap')
    axes_path = os.path.join(
        bluerov2_ignition_path, 'models', 'axes')
    bluerov2_path = os.path.join(
        bluerov2_ignition_path, 'models', 'bluerov2')

    underwater_world = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')),
        launch_arguments={
           'gz_args': '-r ' + world_path
        }.items(),
    )

    x = LaunchConfiguration('x')
    y = LaunchConfiguration('y')
    z = LaunchConfiguration('z')
    x_arg = DeclareLaunchArgument(
        'x',
        default_value='0.0',
        description='Initial x coordinate for bluerov2'
    )

    y_arg = DeclareLaunchArgument(
        'y',
        default_value='0.0',
        description='Initial y coordinate for bluerov2'
    )

    z_arg = DeclareLaunchArgument(
        'z',
        default_value='-1.5',
        description='Initial z coordinate for bluerov2'
    )

    gz_bluerov_pose_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=['/model/bluerov2/pose@geometry_msgs/msg/Pose@gz.msgs.Pose'],
        output='screen',
        name='gz_bluerov_pose_bridge',
    )

    bluerov_spawn = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-v4',
            '-g',
            '-world', 'underwater',
            '-file', bluerov2_path,
            '-name', 'bluerov2',
            '-x', x,
            '-y', y,
            '-z', z,
            '-Y', '0']
    )

    sand_spawn = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-v4',
            '-g',
            '-world', 'underwater',
            '-file', sand_path,
            '-name', 'sand',
            '-x', '0.0',
            '-y', '7.0',
            '-z', '-10.0',
            '-Y', '0']
    )
    axes_spawn = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-v4',
            '-g',
            '-world', 'underwater',
            '-file', axes_path,
            '-name', 'axes',
            '-x', '0.0',
            '-y', '0.0',
            '-z', '0.2',
            '-Y', '0']
    )

    return LaunchDescription([
        x_arg,
        y_arg,
        z_arg,
        underwater_world,
        bluerov_spawn,
        sand_spawn,
        axes_spawn,
        gz_bluerov_pose_bridge,
    ])
