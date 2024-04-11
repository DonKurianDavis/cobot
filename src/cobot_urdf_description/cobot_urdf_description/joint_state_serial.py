#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import JointState
import serial
import math

arduino_data = serial.Serial("/dev/ttyACM0",baudrate=115200, timeout=3.0)

class JointStatetoSerialNode(Node):
    def __init__(self):
        super().__init__("joint_state_serial")
        self.joint_subscriber = self.create_subscription(JointState,'/joint_states',self.joint_state,10)

    def joint_state(self, msg: JointState):
        #self.get_logger().info(str(msg))
        a=math.degrees(msg.position[0])
        b=math.degrees(msg.position[1])
        c=math.degrees(msg.position[2])
        cmd=str(a)+","+str(b)+","+str(c)+',\r'
        arduino_data.write(cmd.encode())


def main(args=None):
    rclpy.init(args=args)
    node = JointStatetoSerialNode()
    rclpy.spin(node)
    rclpy.shutdown()

