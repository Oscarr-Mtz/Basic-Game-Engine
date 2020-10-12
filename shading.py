# shading homework
# CS 314, Fall 2020

from graphics import *
from math import *
from random import *
from time import *

# Constants #
pixHeight = 400    # height of screen in pixels
pixWidth = 400     # width of screen in pixels
d = 1.0            # distance of eye from screen in world units
screenWidth = 1.0  # width of screen in world size
screenHeight = 1.0 # height of screen in world size
infinity = 100000  # needed for max and min
PI = 3.1415926535897932384626433 # number of decimal places Dr. Lall has memorized

def projectX(x, z):
    ''' maps x to screen x location '''
    return pixWidth / 2 + (pixWidth / screenWidth) * x * d / (z + d)

def projectY(y, z):
    ''' maps y to screen y location '''
    return pixHeight / 2 + (pixHeight / screenHeight) * y * d / (z + d)

def drawPoint(x, y, size, color, g):
    ''' draws a size X size rectangle on g at given coordinates
    with given color '''
    pt = Rectangle(Point(x, y), Point(x + size, y + size))
    pt.setFill(color)
    pt.setOutline(color)
    pt.draw(g)

def rotate(p, angle, center):
    ''' rotates the 3D point 'angle' radians around the point 'center'
    pre-condition: The point p should be a LIST with 3 elements '''

    # center point on rotation center
    for i in range(3):
        p[i] = p[i] - center[i]

    x = p[0] * cos(angle) - p[2] * sin(angle)
    z = p[2] * cos(angle) + p[0] * sin(angle)
    p[0] = x
    p[2] = z

    # un-center point on rotation center
    for i in range(3):
        p[i] = p[i] + center[i]


def mag(v):
    ''' returns the magnitude of a vector v '''
    return sqrt( (v[0])**2 + (v[1])**2 + (v[2])**2)


def cross(u, v):
    ''' computes cross product of two vectors
    pre-condition: each vector is a list with 3 elements '''
    cross = []
    cross.append((u[1]*v[2]) - (u[2]*v[1]))
    cross.append((u[2]*v[0]) - (u[0]*v[2]))
    cross.append((u[0]*v[1]) - (u[1]*v[0]))

    return cross

def unitize(u):
    curMag = mag(u)
    if (curMag == 1): #unit vextor
        return u

    elif (curMag != 1): #not unit vector
        for i in range(3):
            if (curMag != 0): #if its point [0,0,0] then we skip
                u[i] /= curMag
        return u


def dot(u, v):
    ''' computes cross product of two vectors
    pre-condition: each vector is a list with 3 elements '''
    dotV = []
    dot = 0
    u = unitize(u)
    v = unitize(v)
    for i in range(3):
        dotV.append((u[i]*v[i]))
        dot += dotV[i]

    return dot

def drawPolygon(p, w):
    ''' draws shaded polygon '''

    # direction of light source
    light = [1, 0, 1]
    # light = [1, 0, 0]  # from the left

    # make the light vector into a unit vector
    lightmag = mag(light)
    for i in range(3):
        light[i] /= lightmag

    ### Compute the shade of the polygon ###
    ##############################################################
    # FILL YOUR CODE IN HERE

    # compute two edge vectors of polygon
    u = []
    v = []

    for i in range(3):
        u.append(p[1][i] - p[0][i])
        v.append(p[3][i] - p[0][i])

    # use cross product to get normal vector (and make into a unit vector)
    normalV = unitize(cross(u, v))

    # use dot product to compute cosine of angle between normal and light
    cosine = dot(normalV, light)
    ##############################################################

    # estimate shade of polygon based on cos of angle
    shade = 128 + int(96 * cosine)
    color = color_rgb(shade, shade, shade)

    ## Project and draw in the polygon ##
    polygon = []
    for point in p:
        polygon.append(Point(projectX(point[0], point[2]), projectY(point[1], point[2])))
    poly = Polygon(polygon)
    poly.setFill(color)
    poly.setOutline(color)
    poly.draw(w)

    w.update()

# computes the average z value of a face
def avgZ(polygon):
    return float(sum([point[2] for point in polygon]))/len(polygon)

def main():
    ''' Main program '''

    g = GraphWin("Shading", pixHeight, pixWidth, autoflush=False)

    # get points on a sphere
    res = 30
    radius = 1
    points = [[None for i in range(res)] for j in range(res)]
    for theta in range(res):
        for phi in range(res):
            x = radius * cos(2 * PI * theta / res) * sin(PI * phi / res)
            y = radius * sin(2 * PI * theta / res) * sin(PI * phi / res)
            z = 3 + radius * cos(PI * phi / res)
            points[theta][phi] = [x, y, z]

            # rotate around center by 90 degrees
            rotate(points[theta][phi], 3.14/2, [0, 0, 3])

    # create the polygons for a sphere
    polygons = []
    for i in range(res-1):
        for j in range(res-1):
            polygons.append([points[i][j], points[i+1][j], points[i+1][j+1], points[i][j+1]])


    # sort points by z-axis (draw farther points first)
    polygons = sorted(polygons, key=avgZ, reverse=True)


    # draw all the polygons
    for p in polygons:
        drawPolygon(p, g)
        #g.getMouse()

    g.getMouse()
    g.close()

if __name__ == "__main__":
    main()
