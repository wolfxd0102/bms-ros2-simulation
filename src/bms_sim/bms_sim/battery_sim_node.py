import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, Float32MultiArray


class BatterySimNode(Node):
    def __init__(self):
        super().__init__('battery_sim_node')

        self.cell_pub = self.create_publisher(Float32MultiArray, '/battery/cell_voltages', 10)
        self.temp_pub = self.create_publisher(Float32, '/battery/temperature', 10)
        self.current_pub = self.create_publisher(Float32, '/battery/current', 10)
        self.soc_pub = self.create_publisher(Float32, '/battery/soc', 10)

        self.timer = self.create_timer(1.0, self.update_battery)

        self.cell_voltages = [3.80, 3.82, 3.78, 3.86]
        self.temperature = 25.0
        self.current = 5.0
        self.soc = 60.0

    def update_battery(self):
        # Simple charging model
        for i in range(len(self.cell_voltages)):
            self.cell_voltages[i] += 0.002

        # Make cell 4 slightly higher to test balancing
        self.cell_voltages[3] += 0.001

        self.temperature += 0.05
        self.soc += 0.1

        cell_msg = Float32MultiArray()
        cell_msg.data = self.cell_voltages
        self.cell_pub.publish(cell_msg)

        temp_msg = Float32()
        temp_msg.data = self.temperature
        self.temp_pub.publish(temp_msg)

        current_msg = Float32()
        current_msg.data = self.current
        self.current_pub.publish(current_msg)

        soc_msg = Float32()
        soc_msg.data = self.soc
        self.soc_pub.publish(soc_msg)

        self.get_logger().info(
            f'Cells: {self.cell_voltages}, Temp: {self.temperature:.1f}, SOC: {self.soc:.1f}%'
        )


def main(args=None):
    rclpy.init(args=args)
    node = BatterySimNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
