#!/usr/bin/python3
import rclpy
from  rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import sys
import math


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
        self._publisher= rosNode.create_publisher( Twist, '/multi/cmd_nav', 10 )

    
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
        obstaclesg=[]
        obstaclesd=[]
        obstacles= []
        angle= scanMsg.angle_min
        for aDistance in scanMsg.ranges :
            if aDistance < 1.0 :
                aPoint= [
                    math.cos(angle) * aDistance,
                    math.sin(angle) * aDistance 
                    ]
                obstacles.append(aPoint)
                angle+= scanMsg.angle_increment
        for i in range(len(obstacles)):
            if obstacles[i][0]<0:
                obstaclesg.append(obstacles[i])
            if obstacles[i][0]>0:
                obstaclesd.append(obstacles[i])
        if len(obstaclesg)==0:
            self.obstacle_gauche=True
        if len(obstaclesd)==0:
            self.obstacle_droit=True
        

    def control_callback(self):
        v=Twist()
        if self.obstacle_droit==False:
            if self.obstacle_gauche==False:
                v._linear.x=0.5
        if self.obstacle_droit==True or self.obstacle_gauche==True:
            v.angular.z=math.pi

    


# Go:
if __name__ == '__main__' :
    main()