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
        #initialize the data for the transformation of the coordinates 
        
        self.msg = String()
        self.coord = String()
        self._logger= rosNode.get_logger()
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener( self.tf_buffer, rosNode )
        #self._timer1=rosNode.create_timer(0.1,self.publish_goal)
        self.position = Point()
        self.posebase_link= Pose()
        self.posebase_link.position.x= 0.0
        self.posebase_link.position.y= 0.0
        self._pub=rosNode.create_publisher(String,"Apres_tf",10)                    
        self._sub=rosNode.create_subscription(String,'detection',self.listener_callback1,10)
    
    def listener_callback1(self,message):
        #get the message from the topic 'detection'
        
        self.coord=message
        self.publish_goal()
    
    def coord_base_link(self):
        #transform the coordinates (r,alpha) to (x,y) in base_link
        
        if self.coord.data!='':
            r=float(self.coord.data.split(',',2)[0])
            alpha=float(self.coord.data.split(',',2)[1])
            self.posebase_link.position.x = r*np.cos(alpha)
            self.posebase_link.position.y = -r*np.sin(alpha)

    def publish_goal(self):
        #transform the coordinates from base_link into map
        
        self.coord_base_link()
        print( f"message transfo {self.coord}")
        currentTime= rclpy.time.Time()
        stampedTransform= None
        try:
            stampedTransform = self.tf_buffer.lookup_transform(                                        #get the transformation between base_link and map from the topic tf
                        'map',
                        'base_link',
                        currentTime)
        except : 
            self._logger.info( f"Could not transform poses from 'base_link' into 'map'")
            return
        myLocalPose = tf2_geometry_msgs.do_transform_pose( self.posebase_link, stampedTransform )
        if self.posebase_link.position.x!=0.0 and self.posebase_link.position.y!=0.0 :                #if the position doesn't change since the initialisation we don't publish coordinates
            self.msg.data=str(myLocalPose._position.x)+","+str(myLocalPose._position.y)               #the coordinates change into the frame map
            self._pub.publish(self.msg)

    #def control_callback2(self):
     #   self._pub.publish(self.msg)

if __name__ == '__main__':
    listen()
