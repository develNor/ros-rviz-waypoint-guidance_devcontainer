#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Joy
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point, Point32, PointStamped, PolygonStamped
from shapely.geometry import LineString
from scipy.interpolate import CubicSpline
from nav_msgs.msg import OccupancyGrid
import numpy as np
from scipy.interpolate import make_interp_spline
import tf2_ros
from std_msgs.msg import String,Int32


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

        self.intersection_pub = rospy.Publisher('/intersection_topic', String, queue_size=10)
        self.intersection_pub.publish(String("hello world"))
        rospy.logerr("run")
        self.has_intersection = False
        self.current_costmap = None
        rospy.Subscriber('costmap/costmap', OccupancyGrid, self.costmap_callback)

        # Create a marker publisher and advertise the line strip marker
        self.marker_pub = rospy.Publisher('line_strip_marker', Marker, queue_size=1)
        self.polygon_pub = rospy.Publisher('buffered_line', PolygonStamped, queue_size=1)

        # Create a point subscriber and set the callback function
        self.subscription = rospy.Subscriber( '/clicked_point', PointStamped,
            self.point_callback,
            10)
        # Create a point subscriber and set the callback function
        self.subscriptionReset = rospy.Subscriber('/reset', Int32,
            self.reset,
            10)

    def reset(self,msg,other):
        self.marker.points = []
        self.polygon.polygon.points= []
        self.polygon_pub.publish(self.polygon)
        self.marker_pub.publish(self.marker)
        self.publishIntersectionMessage(False)         

    def costmap_callback(self, costmap):
        if self.current_costmap is None or self.has_costmap_changed(costmap):
            self.current_costmap = self.extract_costmap_data(costmap)
            rospy.logout(len(self.current_costmap))
            

           
           # self.check_polygon_intersection(self.polygon)
            
               
                # Do something if the polygon intersects with the costmap

    def extract_costmap_data(self, costmap):
        data = []
        width = costmap.info.width
        height = costmap.info.height

        for y in range(height):
            for x in range(width):
                index = x + y * width
                cost = costmap.data[index]
                coord_x = costmap.info.origin.position.x + (x + 0.5) * costmap.info.resolution
                coord_y = costmap.info.origin.position.y + (y + 0.5) * costmap.info.resolution

                if cost != 0:  # Store only cells with non-zero cost
                  
                    data.append((coord_x, coord_y,cost))

        return data

    def has_costmap_changed(self, costmap):
        if self.current_costmap is None:
            return True

        return (
            costmap.info.origin.position.x != self.current_costmap[0][0] or
            costmap.info.origin.position.y != self.current_costmap[0][1] or
            costmap.info.resolution != (self.current_costmap[1][0] - self.current_costmap[0][0]) or
            costmap.data != [1 for _ in self.current_costmap]
        )

    def check_polygon_intersection(self, polygon):
        polygon_bounds = self.get_polygon_bounds(polygon)
        rospy.logout(self.current_costmap[0])
        intersects = False
        for cell in self.current_costmap:
            if not intersects:
                coord_x, coord_y,cost = cell

                if self.is_cell_intersects_polygon(coord_x, coord_y, polygon_bounds):
                    intersects=True
                    self.publishIntersectionMessage(True)           
                

        self.publishIntersectionMessage(False)  

    def check_polygon_intersection_withPath(self, polygon):
        polygon_bounds = self.get_polygon_bounds(polygon)
        rospy.logout(self.marker.points)
        points2d = [(p.x, p.y) for p in self.marker.points]
        rospy.logout(points2d)
        intersects = False
 
        for cell in points2d:
            if not intersects:
                coord_x, coord_y = cell
                print("cell",cell)

                # Perform detailed intersection check with polygon
                if self.is_cell_intersects_polygon(coord_x, coord_y, polygon_bounds):
                    rospy.logout("IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
                    intersects=True
                    return self.publishIntersectionMessage(True)           
                

        return self.publishIntersectionMessage(False)   
    
    def publishIntersectionMessage(self,status):
        if status :
                rospy.logout("Intersection")
                self.publish_intersection('not_driveable')
                self.has_intersection = True
        elif not status :
                self.publish_intersection('driveable')
                self.has_intersection = False 
         
    
                
    def publish_intersection(self, status):
        rospy.logerr("publish")
        msg = String()
        msg.data = status
        self.intersection_pub.publish(status)
        

    def get_polygon_bounds(self, polygon):
        min_x = float('inf')
        min_y = float('inf')
        max_x = float('-inf')
        max_y = float('-inf')

        for point in polygon.polygon.points:
            min_x = min(min_x, point.x)
            min_y = min(min_y, point.y)
            max_x = max(max_x, point.x)
            max_y = max(max_y, point.y)

        return (min_x, min_y, max_x, max_y)

    def is_cell_intersects_polygon(self, coord_x, coord_y, polygon_bounds):
        # Perform intersection check between cell and polygon
        # Implement your polygon-cell intersection logic here
        # You can use libraries like Shapely for detailed polygon-cell intersection checks

        # Placeholder implementation using bounding box check
        return (
            coord_x >= polygon_bounds[0] and
            coord_x <= polygon_bounds[2] and
            coord_y >= polygon_bounds[1] and
            coord_y <= polygon_bounds[3]
        )

    
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
        self.check_polygon_intersection(self.polygon)
        #self.check_polygon_intersection_withPath(self.polygon)
            

        self.polygon_pub.publish(self.polygon)
        


def main(args=None):
    node = ClickExtendLineStripNode()
  
    rospy.spin()

    rospy.shutdown()

if __name__ == '__main__':
    main()