#!/usr/bin/env python

import rospy

from tcp_endpoint.RosTCPServer import TCPServer
from tcp_endpoint.RosPublisher import RosPublisher
from tcp_endpoint.RosSubscriber import RosSubscriber


from std_msgs.msg import Int32
from simulation_msgs.msg import Robot, PoseRobotArray, TwistRobot


def main():
    buffer_size = rospy.get_param("~buffer_size", 1024)
    max_connections = rospy.get_param("~max_connections", 10)
    tcp_server = TCPServer("UnityBridge", buffer_size, max_connections)

    tcp_server.source_destination_dict = {
        'presence': RosPublisher('presence', Int32, queue_size=10, latch=True),
        'robots': RosPublisher('robots', PoseRobotArray, queue_size=10),
        'robot_def': RosSubscriber('robot_def', Robot, tcp_server),
        'robot_cmd_vel': RosSubscriber('robot_cmd_vel', TwistRobot, tcp_server)
    }

    rospy.init_node("UnityBridge")
    tcp_server.start()
    rospy.spin()


if __name__ == "__main__":
    main()
