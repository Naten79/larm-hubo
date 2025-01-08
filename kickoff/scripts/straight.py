#!/usr/bin/python3
import rclpy
from  rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
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

    # infinite Loop:
    rclpy.spin( node )

    # clean end
    node.destroy_node()
    rclpy.shutdown()

# Ros Node Class:
class StraightCtrl :
    def __init__(self):
        self.obstacle_droit=False
        self.obstacle_gauche=False
        self.fobstacle_droit=False
        self.fobstacle_gauche=False
        self.last_move = "None"
        self.speed = 0

    
    def initializeRosNode(self, rosNode ):
        # Get logger from the node:
        self._logger= rosNode.get_logger()

        # Initialize publisher:
        self._pubVelocity= rosNode.create_publisher(
            Twist, '/multi/cmd_nav', 10
        )

        # Initialize scan callback:
        self._subToScan= rosNode.create_subscription(
            LaserScan, '/scan',
            self.scan_callback, 10
        )

        # Initialize control callback:
        self._timForCtrl= rosNode.create_timer(
            0.05, self.control_callback
        )

    def scan_callback(self, scanMsg ):
        global rosNode
        angle= scanMsg.angle_min
        L_obs = 0
        R_obs = 0
        fL_obs = 0
        fR_obs = 0
        for aDistance in scanMsg.ranges :
            if 0.1<aDistance and aDistance < 0.3 and abs(angle)<1:
                if angle>0:
                    L_obs = L_obs + 1
                else:
                    R_obs = R_obs + 1

            if 0.3<aDistance and aDistance < 1.2 and abs(angle)<0.5:
                if angle>0:
                    fL_obs = fL_obs + 1
                else:
                    fR_obs = fR_obs + 1
            angle+= scanMsg.angle_increment

        if L_obs + R_obs > 20:
            if L_obs > R_obs:
                self.obstacle_gauche=True
                self.obstacle_droit=False
            else:
                self.obstacle_gauche=False
                self.obstacle_droit=True
        else:
            self.obstacle_gauche=False
            self.obstacle_droit=False

        if fL_obs + fR_obs > 2:
            if fL_obs > fR_obs:
                self.fobstacle_gauche=True
                self.fobstacle_droit=False
            else:
                self.fobstacle_gauche=False
                self.fobstacle_droit=True
        else:
            self.fobstacle_gauche=False
            self.fobstacle_droit=False

    def control_callback(self):
        v=Twist()
        acc_step = 0.01
        desc_step = 0.01
        if not self.obstacle_droit and not self.obstacle_gauche and not self.fobstacle_droit and  not self.fobstacle_gauche:
            if not self.last_move=="Go straight" and not self.last_move=="Straight left" and not self.last_move=="Straight right":
                self.speed=0.05
                v.angular.z=0.0
                self.last_move = "Go straight"
            else:
                self.speed = max(self.speed + acc_step, 0.4)

        if self.obstacle_droit and not self.obstacle_gauche:
            v.angular.z= math.pi/2
            self.speed=0.0
            self.last_move = "Turn left"

        if self.obstacle_gauche and not self.obstacle_droit:
            v.angular.z= -math.pi/2
            self.speed=0.0
            self.last_move = "Turn right"

        if self.obstacle_gauche and self.obstacle_droit:
            if self.last_move == "Turn right":
                v.angular.z= -math.pi/2
                self.speed=0.0
            if self.last_move == "Turn left":
                v.angular.z= math.pi/2
                self.speed=0.0
            else: 
                v.angular.z= math.pi/2
                self.speed=0.0
                self.last_move = "Turn left"



        print(self.speed)
        angle = math.pi/max(self.speed,0.1)*4
        if self.fobstacle_droit and not self.fobstacle_gauche:
            v.angular.z= angle
            self.speed = max(self.speed-desc_step,0.25)
            self.last_move = "Straight left"

        if self.fobstacle_gauche and not self.fobstacle_droit:
            v.angular.z= -angle
            self.speed = max(self.speed-desc_step,0.25)
            self.last_move = "Straight right"

        if self.fobstacle_gauche and self.fobstacle_droit:
            if self.last_move == "Straight right":
                v.angular.z= -angle
                self.speed = max(self.speed-desc_step,0.25)

            if self.last_move == "Straight left":
                v.angular.z= angle
                self.speed = max(self.speed-desc_step,0.25)
            else: 
                v.angular.z= angle
                self.speed = max(self.speed-desc_step,0.25)
                self.last_move = "Straight left"    

        print(self.speed)
        v.linear.x = self.speed
        self._pubVelocity.publish(v)

# Go:
if __name__ == '__main__' :
    main()
