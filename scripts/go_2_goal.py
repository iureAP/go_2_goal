#!/usr/bin/env python

from math import pow, atan2, sqrt
from geometry_msgs.msg import Twist
from turtlesim_go2goal.srv import Point2D
from turtlesim.msg import Pose


import rospy

class Turtle:
    def __init__(self):
        rospy.init_node('go_2_goal')
        self.vel_publisher = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size=10)
        rospy.Subscriber("turtle1/pose", Pose, self.get_pose_callback)
        self.s = rospy.Service('set_coordinates', Point2D, self.get_coordinates_callback)
        self.rate = rospy.Rate(10)
        self.get_param()

    def get_param(self):
        if not rospy.has_param('~velocity_constant') or not rospy.has_param('~angular_constant') :
            if not rospy.has_param('~velocity_constant'):
                rospy.logerr("Parametro 'velocity_constant' inexistnte")
            if not rospy.has_param('~angular_constant'):
                rospy.logerr("Parametro 'angular_constant' inexistnte")
            rospy.logwarn("there is no parameters they will be parametrized as default mode")
            self.vel_linear_constant = 1.5
            self.vel_angle_constant = 6.0

        if rospy.has_param('~angular_constant'):
            self.vel_linear_constant = rospy.get_param('~velocity_constant')
            rospy.loginfo("linear velocity constant was parameterized with value %.2lf", self.vel_linear_constant)
        
        if rospy.has_param('~angular_constant'):
            self.vel_angle_constant = rospy.get_param('~angular_constant')
            rospy.loginfo("angle velocity constant was parametrized with value %.2lf", self.vel_angle_constant)
            
    def euclidean_distance(self, target_pose):
        return sqrt(pow((self.target_pose.x - self.pose_x), 2) + 
                    pow((self.target_pose.y - self.pose_y), 2))

    def linear_velocity(self, target_pose):
        return (self.vel_linear_constant * self.euclidean_distance(self.target_pose))

    def angle(self, target_pose):
        return atan2(self.target_pose.y  - self.pose_y, self.target_pose.x - self.pose_x)
   
    def angular_velocity(self, target_pose):
        return self.vel_angle_constant * (self.angle(target_pose) - self.pose_theta)
        
    def get_pose_callback(self, data):
        self.pose_x = round(data.x, 2)
        self.pose_y = round(data.y, 2)
        self.pose_theta = round (data.theta, 2)
        self.vel_msg = Twist()
        #rospy.loginfo("Curent pose [%s, %s, %s] ", self.pose_x, self.pose_y, data.theta) 

    def get_coordinates_callback(self, req):
        rospy.loginfo ("Request Point [%s, %s] with tolerance = %.4s", req.x, req.y, req.tolerance)
        if (req.tolerance <= 0.0) or (req.x <= 0.0) or (req.y <= 0.0):
            rospy.logerr("value of parameters must be greater than zero")
            return False
        self.target_pose = Pose()   
        self.target_pose.x = req.x #input("set the required X value: \n")
        self.target_pose.y = req.y #input("set the required Y value: \n")
        self.desired_tolerance = req.tolerance #input("set the required tolerance: ")
        self.move_to_goal()
        #if self.euclidean_distance(target_pose) >= self.desired_tolerance:
        #   rospy.loginfo("testando se da certo")
        #rospy.loginfo("teste %s, %s, %.4s", target_pose.x, target_pose.y, desired_tolerance)
        return True

    def move_to_goal(self):
        while self.euclidean_distance(self.target_pose) >= self.desired_tolerance:
            self.vel_msg.linear.x = self.linear_velocity(self.target_pose)
            self.vel_msg.linear.y = 0
            self.vel_msg.linear.z = 0

            self.vel_msg.angular.x = 0
            self.vel_msg.angular.y = 0
            self.vel_msg.angular.z = self.angular_velocity(self.target_pose)

            self.vel_publisher.publish(self.vel_msg)

            self.rate.sleep()
        self.vel_msg.linear.x = 0
        self.vel_msg.angular.z = 0

    
    def run(self):
        rospy.loginfo("Move to go has started with target pose")
        rospy.spin()

if __name__ == "__main__":
    turtle = Turtle()
    turtle.run()