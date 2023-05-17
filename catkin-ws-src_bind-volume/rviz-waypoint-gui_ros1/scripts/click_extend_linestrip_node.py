#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Joy
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point, Point32, PointStamped, PolygonStamped
from shapely.geometry import LineString
from scipy.interpolate import CubicSpline
import numpy as np
from scipy.interpolate import make_interp_spline

class ClickExtendLineStripNode:
    def __init__(self):
        rospy.init_node('click_extend_line_strip_node')

        # Initialize the line strip marker
        self.marker = Marker()
        self.marker.header.frame_id = "map"
        #self.marker.header.frame_id = "robot_base_link"
        self.marker.type = Marker.LINE_STRIP
        self.marker.scale.x = 0.05
        self.marker.color.g = 1.0
        self.marker.color.a = 1.0
        #self.marker.points = [Point(x=0.0, y=0.0, z=0.0)]
        self.marker.points = []

        self.polygon = PolygonStamped()
        self.polygon.header.frame_id = "map"
        #self.polygon.header.frame_id = "robot_base_link"
        rospy.loginfo("hello worlda")

        # Create a marker publisher and advertise the line strip marker
        self.marker_pub = rospy.Publisher('line_strip_marker', Marker, queue_size=1)
        self.polygon_pub = rospy.Publisher('buffered_line', PolygonStamped, queue_size=1)

        # Create a point subscriber and set the callback function
        self.subscription = rospy.Subscriber( '/clicked_point', PointStamped,
            self.point_callback,
            10)

    def point_callback(self, msg, other):
        # Add the received point to the line strip marker
        self.marker.points.append(msg.point)
        # Publish the updated marker
        self.marker_pub.publish(self.marker)
        rospy.loginfo("hello world")

        points2d = [(p.x, p.y) for p in self.marker.points]

        if len(points2d) == 1: return

        if len(points2d) >= 4:
            degree=3
        elif len(points2d) >= 2:
            degree=len(points2d)-1
        x_arr = [p[0] for p in points2d]
        y_arr = [p[1] for p in points2d]
        p_st = np.stack((x_arr,y_arr))
        dp = p_st[:, 1:] - p_st[:, :-1] # 2-vector distances between points
        l = (dp**2).sum(axis=0)         # squares of lengths of 2-vectors between points
        u_cord = np.sqrt(l).cumsum()    # cumulative sums of 2-norms
        u_cord = np.r_[0, u_cord]       # the first point is parameterized at zero
        spl = make_interp_spline(u_cord, p_st,k=degree, axis=1)    # note p is a 2D array
        uu = np.linspace(u_cord[0], u_cord[-1], 51)
        xx, yy = spl(uu)
        points2d_smooth = [(xx[i], yy[i]) for i in range(len(xx))]
        shapely_line = LineString(points2d_smooth)
        shapely_polygon = shapely_line.buffer(2.5)
        polygon_points = [Point32(x=p[0], y=p[1], z=0.0) for p in shapely_polygon.exterior.coords]
        self.polygon.polygon.points = polygon_points
        self.polygon_pub.publish(self.polygon)


def main(args=None):
    node = ClickExtendLineStripNode()
    rospy.spin()

    rospy.shutdown()

if __name__ == '__main__':
    main()