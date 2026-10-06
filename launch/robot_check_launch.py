from launch import LaunchDescription
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
import launch_ros.descriptions

def generate_launch_description():
    # Declare arguments
    description_file = LaunchConfiguration("description_file", default='robot.urdf.xacro')
    prefix = LaunchConfiguration("prefix", default='')
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    rviz_config_name = LaunchConfiguration('rviz_config_name', default='robot.rviz')

    rviz_file = PathJoinSubstitution([FindPackageShare("simulacion"), "rviz", rviz_config_name])

    robot_description_content = Command([
            PathJoinSubstitution([FindExecutable(name="xacro")]),
            " ",
            PathJoinSubstitution([FindPackageShare("simulacion"), "robots", description_file]),
    ])
    robot_description_param = launch_ros.descriptions.ParameterValue(robot_description_content, value_type=str)

    # Load the robot state publisher node
    '''
    Se publicará el estado de las articulaciones del robot.
    '''
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
          'use_sim_time': use_sim_time,
          'robot_description': robot_description_param,
          'publish_frequency': 100.0,
          'frame_prefix': prefix,
        }],
    )

    # Load the joint state publisher GUI node
    '''
    Se abrirá una ventana gráfica para controlar el estado de las articulaciones
    '''
    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui'
    )

    # Load the rviz2 node
    '''
    Si el archivo de configuración de RViz no se encuentra en la ruta especificada,
    se deberá crear uno la primera vez que se utilice y configurar su nombre en
    el argumento denominado rviz_file.
    '''
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="log",
        arguments=["-d", rviz_file],
    )

    nodes = [
        robot_state_publisher_node,
        joint_state_publisher_gui_node,
        rviz_node
    ]

    return LaunchDescription(nodes)