#!/usr/bin/python3
import rclpy
import time
import math
from rclpy.node import Node
from geometry_msgs.msg import Twist


def infiniteTalk():
    # Initialize ROS node with ROS client
    time.time()
    rclpy.init()
    aNode= Node( "infTalker" )
    talker= ROSTalker(aNode)
    # Start infinite loop
    rclpy.spin(aNode)
    # Clean everything and switch the light off
    aNode.destroy_node()
    rclpy.shutdown()

class ROSTalker:
    def __init__(self, rosNode):
        self._publisher= rosNode.create_publisher( Twist, '/multi/cmd_nav', 10 )
        self._timer = rosNode.create_timer(0.5, self.timer_callback)
        self._i = 0

    def timer_callback(self):
    	velocity = Twist()
    # Feed Twist velocity values
    	if int(time.time())%2==0:
    		velocity.linear.x=0.5
    		velocity.angular.z=0.0
    # Publish
    	else :
    		velocity.linear.x=0.0
    		velocity.angular.z=math.pi*0.7
    	self._publisher.publish(velocity)

    	
    	

# Execute the function.
if __name__ == "__main__":
    infiniteTalk()
