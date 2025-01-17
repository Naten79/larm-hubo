#!/usr/bin/python3
import rclpy
import numpy as np
import tf2_geometry_msgs
import tf2_ros                 
import matplotlib.pyplot as plt
from geometry_msgs.msg import Point, Pose
from rclpy.node import Node
from std_msgs.msg import String
from tf2_msgs.msg import TFMessage



def listen():
        rclpy.init()
        essai = ROSListener1()
        aNode= Node( "listener" )
        essai.initializelistener(aNode)
        rclpy.spin(aNode)

        # Clean everything and switch the light off
        aNode.destroy_node()
        rclpy.shutdown()


class ROSListener1():

    def initializelistener(self, rosNode):
        self._logger= rosNode.get_logger()
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener( self.tf_buffer, rosNode )
        self._timer1=rosNode.create_timer(0.1,self.publish_goal)
        self.position = Point()
        self.posebase_link= Pose()
        self.posebase_link.position.x= 10.0
        self.posebase_link.position.y= 8.5


    def publish_goal(self):
        currentTime= rclpy.time.Time()
        # Get Transformation (import poses referenced in odom into base_link)
        stampedTransform= None
        try:
            print('get transform...')
            stampedTransform = self.tf_buffer.lookup_transform(
                        'base_link',
                        'map',
                        currentTime)
        except : # (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):TransformException as tex:
            self._logger.info( f"Could not transform poses from 'odom' into 'base_link'")
            return
        # Now transform....
        print( f"Transform.  {stampedTransform}" )
        myLocalPose = tf2_geometry_msgs.do_transform_pose( self.posebase_link, stampedTransform )
        print( f"Results:  {myLocalPose}" )


if __name__ == '__main__':
    listen()