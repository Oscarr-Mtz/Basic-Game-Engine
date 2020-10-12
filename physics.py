# collision homework
# CS 314, Fall 2020

from graphics import *
from random import *
from time import *
import math

class Ball:
    def __init__(self, r, x, y, vx, vy):
        self.radius = r
        self.position = [x, y]
        self.velocity = [vx, vy]
        self.graphic = Circle(Point(x, y), r)

    def draw(self, g):
        self.graphic.draw(g)

    def move(self, deltaTime):
        oldposition = [self.position[0], self.position[1]]

        ### UPDATE POSITION HERE ###
        newX = oldposition[0] + (deltaTime*self.velocity[0])
        newY = oldposition[1] + (deltaTime*self.velocity[1])
        self.position = [newX, newY]

        # code for making balls wrap around the screen
        if self.position[0] < 0:
            self.position[0] = 500
        if self.position[0] > 500:
            self.position[0] = 0
        if self.position[1] < 0:
            self.position[1] = 500
        if self.position[1] > 500:
            self.position[1] = 0

        # move the graphical object
        self.graphic.move(self.position[0] - oldposition[0], self.position[1] - oldposition[1])

    def collidesWith(self, ball2):
        # checks if distance between balls' centers is less than sum of radii
        ### UPDATE CODE HERE ###
        x = (self.position[0] - ball2.position[0])**2
        y = (self.position[1] - ball2.position[1])**2

        d = math.sqrt(x + y)
        if (d <= (self.radius + ball2.radius)):
            return True

        return False

    def bounce(self, ball2):
        ### ADD BOUNCE CODE HERE ###
        # Calc 1: assume that the balls are point masses and swap velocities
        # Calc 2: decompose each ball's velocity vector into components
        #         parallel and perpendicular to collision vector. Then
        #         swap parallel components, keeping perpendicular ones same.

        selfV = self.velocity
        ballV = ball2.velocity

        ball2.velocity = selfV
        self.velocity = ballV

        return

def main():
    g = GraphWin("Physics example", 500, 500, autoflush=False)

    balls = []
    for i in range(20):
        # initialize with different x so that none collide to begin with
        b = Ball(10, i * 25, randint(0, 500), randint(-100, 100), randint(-100, 100))
        balls.append(b)
        b.draw(g)

    deltaTime = 0.01
    while g.checkMouse() == None:
        # move the balls
        for b in balls:
            b.move(deltaTime)

        # handle collisions
        for i in range(len(balls)):
            for j in range(i + 1, len(balls)):
                if balls[i].collidesWith(balls[j]):
                    balls[i].bounce(balls[j])

        sleep(deltaTime)
        update()

    g.close()

if __name__ == "__main__":
    main()
