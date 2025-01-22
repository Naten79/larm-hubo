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
from std_msgs.msg import String
import sys


def listen():
    rclpy.init()
    essai = ROSListener1()
    aNode= Node( "listener" )
    essai.initializelistener(aNode)
    rclpy.spin(aNode)
    aNode.destroy_node()
    rclpy.shutdown()
    


class ROSListener1():

    def initializelistener(self, rosNode):
        self.msg = String()
        self.coord = String()
        self._logger= rosNode.get_logger()
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener( self.tf_buffer, rosNode )
        self._timer1=rosNode.create_timer(0.1,self.publish_goal)
        self.position = Point()
        self.posebase_link= Pose()
        self.posebase_link.position.x= 0.0
        self.posebase_link.position.y= 0.0
        self._pub=rosNode.create_publisher(String,"Apres_tf",10)                            #publie sur le topic "Apres_tf" pour afficher le marqueur
        self._timForCtrl= rosNode.create_timer(
            1, self.control_callback2
        )
        self._sub=rosNode.create_subscription(String,'detection',self.listener_callback1,10)
    
    def listener_callback1(self,message):
        self.coord=message
    
    def coord_base_link(self):
        if self.coord.data!='':
            r=float(self.coord.data.split(',',2)[0])
            alpha=float(self.coord.data.split(',',2)[1])
            self.posebase_link.position.x = r*np.cos(alpha)
            self.posebase_link.position.y = r*np.sin(alpha)

    def publish_goal(self):
        self.coord_base_link()
        currentTime= rclpy.time.Time()
        stampedTransform= None
        try:
            stampedTransform = self.tf_buffer.lookup_transform(
                        'map',
                        'base_link',
                        currentTime)
        except : # (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):TransformException as tex:
            self._logger.info( f"Could not transform poses from 'base_link' into 'map'")
            return
        myLocalPose = tf2_geometry_msgs.do_transform_pose( self.posebase_link, stampedTransform )
        self.msg.data=str(myLocalPose._position.x)+","+str(myLocalPose._position.y)                 #la position voulue est transformée en type string afin qu'elle puisse être envoyée sur le topic Apres_tf

    def control_callback2(self):
        self._pub.publish(self.msg)

if __name__ == '__main__':
    listen()