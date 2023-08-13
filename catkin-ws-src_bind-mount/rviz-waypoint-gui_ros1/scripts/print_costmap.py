#!/usr/bin/env python

import rospy
from nav_msgs.msg import OccupancyGrid, MapMetaData

class PrintCostmapNode:
    def __init__(self):
        rospy.logwarn("init PrintCostmapNode")
        rospy.init_node('click_extend_line_strip_node')

        # Create a point subscriber and set the callback function
        self.subscription = rospy.Subscriber( '/costmap/costmap', OccupancyGrid, self.costmap_callback, 10)

    def costmap_callback(self, msg, other):
        # Add the received point to the line strip marker
        #rospy.logwarn("costmap_callback")
        filtered_list = [data for data in msg.data if data not in [0,-1]]
        str_msg = str(filtered_list)
        #rospy.logwarn(str_msg)

def main(args=None):
    node = PrintCostmapNode()
    rospy.spin()
    rospy.shutdown()

if __name__ == '__main__':
    main()