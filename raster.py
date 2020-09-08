# rasterization homework
# CS 314, Fall 2020

from graphics import *
from math import *
from random import *

# Constants #
pixHeight = 400    # height of screen in pixels
pixWidth = 400     # width of screen in pixels
d = 1.0            # distance of eye from screen in world units
screenWidth = 1.0  # width of screen in world size
screenHeight = 1.0 # height of screen in world size
infinity = 100000  # needed for max and min

def projectX(x, z):
	''' maps x to screen x location '''
	return pixWidth / 2 + (pixWidth / screenWidth) * x * d / (z + d)

def projectY(y, z):
	''' maps y to screen y location '''
	return pixHeight / 2 + (pixHeight / screenHeight) * y * d / (z + d)

def forward(point, distance):
	''' update point when player moves forward given distance '''
	point[2] -= distance

def backward(point, distance):
	''' update point when player moves backward given distance '''
	point[2] += distance

def rotate(point, angle, center):
	''' rotates the polygon 'angle' radians around the point 'center'
	point: a 3D point represented by a list of size 3
	angle: an angle in radians
	center: the point around which we are rotating the point
	'''

	# center point on rotation center
	for i in range(3):
		point[i] = point[i] - center[i]

	# use the rotation formula
	x = point[0] * cos(angle) + point[2] * sin(angle)
	z = point[2] * cos(angle) - point[0] * sin(angle)
	point[0] = x
	point[2] = z

	# un-center point on rotation center
	for i in range(3):
		point[i] = point[i] + center[i]

def depth(polygon):
	''' the average depth of a polygon, represented as a list of points '''
	return sum([point[2] for point in polygon])/len(polygon) # average of z-coordinate

def drawPoint(x, y, size, color, win):
    ''' draws a size X size rectangle on win at given coordinates
    with given color
    '''
    pt = Rectangle(Point(x, y), Point(x + size, y + size))
    pt.setFill(color)
    pt.setOutline(color)
    pt.draw(win)


def drawPolygon(p, win, color):
	''' draws polygon onto screen g using rasterization algorithm '''
	n = len(p)   # number of vertices in polygon
	x = []       # x-coordinates of polygon on screen
	y = []       # y-coordinates of polygon on screen
	for point in p:
		x.append(projectX(point[0], point[2]))
		y.append(projectY(point[1], point[2]))

	print("This the list of points:",p)
	print("This is list y:",y)

	# find bounds on scan lines
	# YOUR CODE GOES HERE

	m = ((y2-y1)/(x2-x1))
	lineEQ = m * (x2-x1) + y2
	resolution = 3
    # YOUR CODE GOES HERE
	for each line in polygone:
		for each point(x,y) on the line:
			xmin[y] = min(xmin[y], x)
			xmax[y] = max(xmax[y], x)

	for each y value from ymin to ymax:
		for each x value from xmin[y] to xmax[y]:
			#color pixel(x,y)
    # The following draws a point at (x, y) of color 'color'
    # size controls the size of the point (to speed up drawing)
    # drawPoint(x, y, size, color, win)
    # for example:
    # drawPoint(100, 100, 1, color, win)


    # draws in the bounding polygon
	for i in range(n):
		x1 = int(x[i])
		y1 = int(y[i])
		x2 = int(x[(i + 1) % n])
		y2 = int(y[(i + 1) % n])
		line = Line(Point(x1, y1), Point(x2, y2))
		line.draw(win)

def main():
    ''' Main program that runs everything '''

    win = GraphWin("Projection", pixHeight, pixWidth)

    # create points on a cube
    points = []
    for x in range(-1, 2, 2):
        for y in range(-1, 2, 2):
            for z in range(5, 8, 2):
                points.append([x, y, z])

    # rotate around center by 45 degrees
    for p in points:
        rotate(p, 3.14/4, [0, 0, 6])

    # create the polygons for the 6 faces of a cube
    polygons = [[points[0], points[2], points[6], points[4]],  # front
                [points[1], points[3], points[7], points[5]],  # back
                [points[2], points[3], points[7], points[6]],  # top
                [points[0], points[1], points[5], points[4]],  # bottom
                [points[0], points[1], points[3], points[2]],  # left
                [points[4], points[5], points[7], points[6]]]  # right

    # sort points by z-axis (draw farther points first)
    polygons = sorted(polygons, key=lambda polygon: -depth(polygon))

    # draw all the polygons
    for p in polygons:
        color = color_rgb(randint(0, 255), randint(0, 255), randint(0, 255))
        drawPolygon(p, win, color)
        win.getMouse()


    win.getMouse()
    win.close()


if __name__ == "__main__":
	main()
