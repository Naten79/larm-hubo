#!/usr/bin/python3
import rclpy
from  rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from kobuki_ros_interfaces.msg import BumperEvent
from kobuki_ros_interfaces.msg import ButtonEvent
from kobuki_ros_interfaces.msg import WheelDropEvent
from kobuki_ros_interfaces.msg import CliffEvent
import sys
import math
import time

# Ros Node process:
def main():
    # Initialize ROS and a ROS node
    rclpy.init(args=sys.argv)
    node= Node( 'basic_move' )

    # Initialize our control:
    control= StraightCtrl()
    control.initializeRosNode( node )

    # Infinite Loop:
    rclpy.spin( node )

    # Clean end
    node.destroy_node()
    rclpy.shutdown()

# Ros Node Class:
class StraightCtrl :
    def __init__(self):
        # Initialize our variables:
        self.near_right_obstacle=False
        self.near_left_obstacle=False
        self.far_right_obstacle=False
        self.far_left_obstacle=False
        self.last_move = "None"
        self.speed = 0.0
        self.angular_speed = 0.0
        self.bumper=False
        self.button=False

    def initializeRosNode(self, rosNode ):
        # Get logger from the node:
        self._logger= rosNode.get_logger()

        # Initialize publisher:
        self._pubVelocity= rosNode.create_publisher(
            Twist, '/multi/cmd_nav', 10
        )

        # Initialize our parameters:
        global acc_step
        global desc_step
        global distance_near
        global distance_far
        global angle_near
        global angle_far
        global max_speed
        global min_curve_speed

        rosNode.declare_parameter( 'acc_step', 0.01 )
        rosNode.declare_parameter( 'desc_step', 0.01 )
        rosNode.declare_parameter( 'distance_near', 0.3 )
        rosNode.declare_parameter( 'distance_far', 1.0 )
        rosNode.declare_parameter( 'angle_near', 2 )
        rosNode.declare_parameter( 'angle_far', 0.5 )
        rosNode.declare_parameter( 'max_speed', 0.3 )
        rosNode.declare_parameter( 'min_curve_speed', 0.1 )
        
        acc_step = rosNode.get_parameter( 'acc_step').value
        desc_step = rosNode.get_parameter( 'desc_step').value
        distance_near = rosNode.get_parameter( 'distance_near').value
        distance_far = rosNode.get_parameter( 'distance_far').value
        angle_near = rosNode.get_parameter( 'angle_near').value
        angle_far = rosNode.get_parameter( 'angle_far').value
        max_speed = rosNode.get_parameter( 'max_speed').value
        min_curve_speed = rosNode.get_parameter( 'max_speed').value

        # Print the parameters:
        print( f"> Acceleration step value: {acc_step} m/s \n> Desceleration step value: {desc_step} m/s\n> Max nearby scan distance value: {distance_near} m\n> Max far scan distance value:: {distance_far} m\n> Nearby scan angle value: {angle_near} rad\n> Far scan angle value: {angle_far} rad\nMax speed: {max_speed} m/s" )
        

        # Initialize scan callback:
        self._sub1=rosNode.create_subscription(BumperEvent,'/events/bumper',self.listener_callback1,10)
        self._sub2=rosNode.create_subscription(ButtonEvent,'/events/button',self.listener_callback2,10)
        self._sub3=rosNode.create_subscription(WheelDropEvent,'/events/wheel_drop',self.listener_callback3,10)
        self._sub4=rosNode.create_subscription(CliffEvent,'/events/cliff',self.listener_callback4,10)
        self._subToScan= rosNode.create_subscription(
            LaserScan, '/scan',
            self.scan_callback, 10
        )

        # Initialize control callback:
        self._timForCtrl= rosNode.create_timer(
            0.05, self.control_callback
        )
    def listener_callback1(self,msg):
        if msg.state==BumperEvent.PRESSED:
            
            self.bumper=True
            

    def listener_callback2(self,msg):
        if msg.state==ButtonEvent.PRESSED:
            self.button=True
        if self.button:
            self.bumper=False

    def listener_callback3(self,msg):
        if msg.state==1:
            self.bumper=True
        if msg.state==0:
            self.bumper==False
    def listener_callback4(self,msg):
        if msg.state==CliffEvent.CLIFF:
            self.bumper=True
        
    def scan_callback(self, scanMsg ):
        global rosNode
        angle= scanMsg.angle_min

        # Initialize our variables:
        L_obs = 0   # Ammount of nearby obstacles on the left
        R_obs = 0   # Ammount of nearby obstacles on the right
        fL_obs = 0  # Ammount of far obstacles on the left
        fR_obs = 0  # Ammount of far obstacles on the right

        # Count the ammount of obstacles nearby
        for aDistance in scanMsg.ranges :
            if 0.1<aDistance and aDistance < distance_near and abs(angle)<angle_near:
                if angle>0:
                    L_obs += 1
                else:
                    R_obs += 1

        # Count the ammount of obstacles far away
            if distance_near<aDistance and aDistance < distance_far and abs(angle)<angle_far:
                if angle>0:
                    fL_obs += 1
                else:
                    fR_obs += 1

            angle+= scanMsg.angle_increment

        # Update the variables
        self.near_left_obstacle=False
        self.near_right_obstacle=False
        if L_obs + R_obs > 20:  # Nearby obstacle detected
            if L_obs > R_obs:   # Obstacle on the left 
                self.near_left_obstacle=True
                self.near_right_obstacle=False
            else:               # Obstacle on the right
                self.near_left_obstacle=False
                self.near_right_obstacle=True
        
        self.far_left_obstacle=False
        self.far_right_obstacle=False
        if fL_obs + fR_obs > 4:
            if fL_obs > fR_obs:     # Far obstacle on the left
                self.far_left_obstacle=True
                self.far_right_obstacle=False
            else:                   # Far obstacle on the right
                self.far_left_obstacle=False
                self.far_right_obstacle=True
            

    def control_callback(self):
        print(self.bumper)
        if self.bumper==False:
            v=Twist()
            # Move the robot
            if not self.near_right_obstacle and not self.near_left_obstacle and not self.far_right_obstacle and not self.far_left_obstacle:
                self.speed = min(self.speed + acc_step, max_speed)
                self.angular_speed=0.0
                self.last_move = "Straight"
            curve_speed_rotation = math.pi/3


            if self.far_right_obstacle and not self.far_left_obstacle and not self.last_move == "Straight right" and not self.last_move == "Turn right":
                self.angular_speed= curve_speed_rotation
                self.speed = max(self.speed - desc_step, 0.3)
                self.last_move = "Straight left"

            if self.far_left_obstacle and not self.far_right_obstacle and not self.last_move == "Straight left" and not self.last_move == "Turn left":
                self.angular_speed= -curve_speed_rotation
                self.speed = min(self.speed + acc_step, max_speed)
                self.last_move = "Straight right"




            if self.near_right_obstacle and not self.near_left_obstacle and not self.last_move=="Turn right" :
                self.angular_speed= math.pi/2
                self.speed=0.0
                self.last_move = "Turn left"

            if self.near_left_obstacle and not self.near_right_obstacle and not self.last_move=="Turn left":
                self.angular_speed= -math.pi/2
                self.speed=0.0
                self.last_move = "Turn right"


        
            v.linear.x = self.speed
            v.angular.z= self.angular_speed
            print(f"\0>Current speed: {self.speed} m/s")
            self._pubVelocity.publish(v)

# Go:
if __name__ == '__main__' :
    main()
