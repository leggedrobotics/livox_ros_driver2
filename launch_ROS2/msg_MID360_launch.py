import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    pkg_share = get_package_share_directory("livox_ros_driver2")
    config_dir = os.path.join(pkg_share, "config")

    default_user_config_path = os.path.join(config_dir, "MID360_config.json")
    default_rviz_config_path = os.path.join(config_dir, "display_point_cloud_ROS2.rviz")

    xfer_format = LaunchConfiguration("xfer_format")
    multi_topic = LaunchConfiguration("multi_topic")
    data_src = LaunchConfiguration("data_src")
    publish_freq = LaunchConfiguration("publish_freq")
    output_type = LaunchConfiguration("output_type")
    rviz_enable = LaunchConfiguration("rviz_enable")
    rosbag_enable = LaunchConfiguration("rosbag_enable")
    msg_frame_id = LaunchConfiguration("msg_frame_id")
    user_config_path = LaunchConfiguration("user_config_path")
    lvx_file_path = LaunchConfiguration("lvx_file_path")
    bd_list = LaunchConfiguration("bd_list")

    livox_driver = Node(
        package="livox_ros_driver2",
        executable="livox_ros_driver2_node",
        name="livox_lidar_publisher",
        output="screen",
        parameters=[{
            "xfer_format": xfer_format,
            "multi_topic": multi_topic,
            "data_src": data_src,
            "publish_freq": publish_freq,
            "output_data_type": output_type,
            "frame_id": ParameterValue(msg_frame_id, value_type=str),
            "lvx_file_path": ParameterValue(lvx_file_path, value_type=str),
            "user_config_path": ParameterValue(user_config_path, value_type=str),
            "cmdline_input_bd_code": ParameterValue(bd_list, value_type=str),
        }],
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="livox_rviz",
        output="screen",
        arguments=["--display-config", default_rviz_config_path],
        condition=IfCondition(rviz_enable),
    )

    rosbag_record = ExecuteProcess(
        cmd=["ros2", "bag", "record", "-a"],
        output="screen",
        condition=IfCondition(rosbag_enable),
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            "lvx_file_path",
            default_value="livox_test.lvx",
            description="Path to LVX file when file playback is used.",
        ),
        DeclareLaunchArgument(
            "bd_list",
            default_value="100000000000000",
            description="Broadcast/device code string used by the Livox driver.",
        ),
        DeclareLaunchArgument(
            "xfer_format",
            default_value="0",
            description="0=PointCloud2, 1=customized Livox message format.",
        ),
        DeclareLaunchArgument(
            "multi_topic",
            default_value="0",
            description="0=all LiDARs on one topic, 1=one topic per LiDAR.",
        ),
        DeclareLaunchArgument(
            "data_src",
            default_value="0",
            description="0=raw lidar data source.",
        ),
        DeclareLaunchArgument(
            "publish_freq",
            default_value="10.0",
            description="Pointcloud publish frequency in Hz.",
        ),
        DeclareLaunchArgument(
            "output_type",
            default_value="0",
            description="Driver output mode.",
        ),
        DeclareLaunchArgument(
            "rviz_enable",
            default_value="false",
            description="Launch RViz2 with the Livox pointcloud config.",
        ),
        DeclareLaunchArgument(
            "rosbag_enable",
            default_value="false",
            description="Record all ROS 2 topics with ros2 bag.",
        ),
        DeclareLaunchArgument(
            "msg_frame_id",
            default_value="livox_frame",
            description="Frame id used for published Livox messages.",
        ),
        DeclareLaunchArgument(
            "user_config_path",
            default_value=default_user_config_path,
            description="Path to the Livox JSON configuration file.",
        ),
        livox_driver,
        rviz_node,
        rosbag_record,
    ])
