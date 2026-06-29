import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray, String


class BMSControllerNode(Node):
    def __init__(self):
        super().__init__('bms_controller_node')

        self.cell_sub = self.create_subscription(
            Float32MultiArray,
            '/battery/cell_voltages',
            self.cell_callback,
            10
        )

        self.fault_pub = self.create_publisher(String, '/bms/fault_status', 10)
        self.balance_pub = self.create_publisher(Float32MultiArray, '/bms/balance_command', 10)
        self.contactor_pub = self.create_publisher(String, '/bms/contactor_command', 10)

        self.overvoltage_limit = 4.20
        self.undervoltage_limit = 3.00
        self.balance_threshold = 0.03

    def cell_callback(self, msg):
        cells = list(msg.data)
        max_cell = max(cells)
        min_cell = min(cells)

        fault_msg = String()
        contactor_msg = String()
        balance_msg = Float32MultiArray()

        # Default: no balancing
        balance_command = [0.0 for _ in cells]

        if max_cell > self.overvoltage_limit:
            fault_msg.data = 'FAULT: CELL_OVERVOLTAGE'
            contactor_msg.data = 'STOP_CHARGE'

        elif min_cell < self.undervoltage_limit:
            fault_msg.data = 'FAULT: CELL_UNDERVOLTAGE'
            contactor_msg.data = 'STOP_DISCHARGE'

        else:
            fault_msg.data = 'OK'
            contactor_msg.data = 'ALLOW_OPERATION'

            # Simple passive balancing command:
            # balance cells that are higher than the minimum by more than threshold
            for i, voltage in enumerate(cells):
                if voltage - min_cell > self.balance_threshold:
                    balance_command[i] = 1.0

        balance_msg.data = balance_command

        self.fault_pub.publish(fault_msg)
        self.contactor_pub.publish(contactor_msg)
        self.balance_pub.publish(balance_msg)

        self.get_logger().info(
            f'Fault: {fault_msg.data}, Contactor: {contactor_msg.data}, Balance: {balance_command}'
        )


def main(args=None):
    rclpy.init(args=args)
    node = BMSControllerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
