#!/usr/bin/env python3
# This is a basic inverse kinematics for a Three DoF Manipulator
# Known Parameters are Xc,Yc and Zc
# Angles of the motor (base_angle, arm_angle, shoulder_angle and wrist_angle) remains unknown.
import math
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import String

global joint_timer

class TimeSubscriberNode(Node):
    def __init__(self):
        super().__init__("time_subscriber_joint_state")
        self.time_subscriber_joint_state_ = self.create_subscription(JointState,"/joint_states",self.time_callback,10)
        self.joint_state_publisher = self.create_publisher(JointState,"/joint_states",10)
        
    def time_callback(self,timer:JointState):
        msg = JointState()
        msg._header=timer._header
        msg._position[0]=0.95
        self.get_logger().info(str(msg))
        self.joint_state_publisher.publish(msg)


def inverse_kinematics():

    global base_angle,arm_angle,shoulder_angle,wrist_angle

    #length of links (in m)
    l1=0.318 #base height
    l2=0.28250#shoulder length
    l3=0.17#wrist length
    l4=0.095#gripper length

    #End points
    x,y,z = 0.23,0.30,0.4

    #Angle of the arm can be changed into three modes 0, 45 and 90.
    arm_angle=45

    #base angle is the easiest to calculate
    base_angle=math.atan(y/x)
    arm_angle=math.radians(arm_angle)
    #Since there is arm link attached to the cobot which is fixed, it should be considered in calculation of joint angles.
    #wrist angle is now calculated.
    r=(x*x)+(y*y)-(2*l2*math.cos(arm_angle)*(x*math.cos(base_angle)+y*math.sin(base_angle)))+(l2*l2*math.cos(arm_angle)*math.cos(arm_angle))+math.pow((z-l1-l2*math.sin(arm_angle)),2)
    wrist_angle=math.acos((r-(l3*l3)-(l4*l4))/(2*l3*l4))

    #shoulder angle is calculated
    alpha=math.atan((z-l1-l2*math.sin(arm_angle))/math.sqrt((x*x)+(y*y)-(2*l2*math.cos(arm_angle)*(x*math.cos(base_angle)+y*math.sin(base_angle)))+(l2*l2*math.cos(arm_angle)*math.cos(arm_angle))))
    beta=math.atan((math.sin(wrist_angle)*l4)/(l3+l4*math.cos(wrist_angle)))

    shoulder_angle=alpha-beta


def main(args=None):
    rclpy.init(args=args)
    inverse_kinematics()
    node=TimeSubscriberNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
