# Simulación de Brazo 1 DoF

Este paquete proporciona una simulación de un brazo robótico de 1 grado de libertad (DoF) utilizando **Gazebo** como motor de simulación y **joint_trajectory_controller** para controlar las articulaciones.

## Descripción

El paquete `simulacion_1dof` permite simular un brazo robótico simple con una articulación que puede rotarse. La simulación incluye:

- **Modelo URDF/Xacro**: Descripción completa del robot con base fija y articulación rotativa
- **Integración con Gazebo**: Simulación física realista usando el simulador Gazebo
- **Control de Trayectorias**: Controlador de trayectorias de articulaciones para comandar movimientos
- **Visualización en RViz2**: Visualización 3D del robot y su estado
- **Puente ROS2-Gazebo**: Comunicación entre ROS2 y Gazebo mediante `ros_gz_bridge`

## Requisitos Previos

- ROS 2 jazzy o superior
- Gazebo (incluido en la instalación de `ros_gz_sim`)

## Instalación

1. Clonar o descargar el paquete en el workspace:

```bash
cd ~/tu_workspace/src
git clone https://github.com/docencia-juanscelyg/simulacion_1dof.git
```

2. Compilar el paquete:

```bash
cd ~/tu_workspace
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
```

3. Source el workspace:

```bash
source install/setup.bash
```

## Uso

### 1. Lanzar la Simulación Completa

Para lanzar el brazo de 1 DoF en Gazebo con RViz2 y los controladores:

```bash
ros2 launch simulacion_1dof robot_gazebo.launch.py
```

Esto iniciará:

- Gazebo con el mundo vacío
- RViz2 para visualización
- Robot State Publisher
- Puente ROS2-Gazebo
- El robot spawneado en la simulación

### 2. Lanzar Solo el Robot State Publisher

Si solo necesitas publicar el estado del robot sin Gazebo:

```bash
ros2 launch simulacion_1dof robot_state_publisher.launch.py
```

### 3. Cargar los Controladores

Una vez que el robot esté en Gazebo, cargar los controladores:

```bash
ros2 launch simulacion_1dof robot_controllers.launch.py
```

Esto cargará:

- **joint_state_broadcaster**: Publica el estado de las articulaciones
- **joint_trajectory_controller**: Controlador para seguimiento de trayectorias

## Control del Brazo

### Enviar Comandos de Trayectoria

Una vez que los controladores están cargados, puedes enviar comandos de trayectoria:

```bash
ros2 topic pub --once /joint_trajectory_controller/follow_trajectory trajectory_msgs/JointTrajectory '{
  header: {frame_id: "world"},
  joint_names: ["brazo_joint"],
  points: [
    {
      positions: [1.57],
      velocities: [0.0],
      time_from_start: {sec: 2}
    }
  ]
}'
```

Si lo prefieres a través de la interfaz gráfica de rqt, con el paquete `rqt_joint_trajectory_controller`, puedes enviar comandos de manera más intuitiva. Se puede intalar con:

```bash
sudo apt install ros-<distro>-rqt-joint-trajectory-controller
```

### Visualizar el Estado de las Articulaciones

Para ver el estado actual de las articulaciones:

```bash
ros2 topic echo /joint_states
```

### Verificar los Controladores Cargados

```bash
ros2 control list_controllers
```

## Solución de Problemas

### El robot no aparece en Gazebo

1. Verifica que el robot_state_publisher esté publicando correctamente:

   ```bash
   ros2 topic list | grep robot_description
   ```

2. Verifica que el bridge ROS2-Gazebo esté en ejecución
3. Revisa los logs de gazebo

### Los controladores no responden

1. Verifica que los controladores estén cargados:

   ```bash
   ros2 control list_controllers
   ```

2. Comprueba que el joint_state_broadcaster está activo
3. Revisa la configuración en `config/controllers.yaml`

### RViz2 no muestra el robot

1. Actualiza el fixed frame a "world" en RViz2
2. Verifica que el robot_state_publisher esté publicando los transforms
