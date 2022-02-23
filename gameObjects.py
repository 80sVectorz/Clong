from baseDataTypes import vector2d
from rich.console import Console
import time, math

class collider:
    x = 0
    y = 0
    w = 0
    h = 0
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

class ball:
    position = vector2d(0, 0)
    velocity = vector2d(0, 0)
    character = 'o'
    def __init__(self, x, y, vx, vy,char='o'):
        self.position = vector2d(x, y)
        self.ballSpeed = 0.1
        self.velocity = vector2d(vx+self.ballSpeed, vy+self.ballSpeed)
        self.character = char
    def update(self, dt,paddle1,paddle2,colliders=[],p1goal=None,p2goal=None):
        self.position.x += self.velocity.x * dt*(1+self.ballSpeed)
        self.position.y += self.velocity.y * dt
        for c in colliders:
            if int(self.position.x) in range(c.x, c.x + c.w):
                if int(self.position.y) in range(c.y, c.y + c.h):
                    if abs(self.ballSpeed) > 0.5:
                        self.ballSpeed=0.2
                    else:
                        self.ballSpeed+=0.1
                    if c.h > c.w:
                        self.velocity.y *= -1
                    elif c.w > c.h:
                        self.velocity.x *= -1
                    else:
                        self.velocity.x *= -1
                        self.velocity.y *= -1
                    self.velocity.x *= -1
                    self.velocity.y *= -1
                    self.position.x += self.velocity.x * dt*2
                    self.position.y += self.velocity.y * dt*2
                    if c == p1goal:
                        return 2
                    elif c == p2goal:
                        return 1
                    
        if int(self.position.x) in range(int(paddle1.position.x)-3,int(paddle1.position.x)):
            if int(self.position.y) in range(paddle1.position.y - paddle1.length+1,paddle1.position.y):
                relativeIntersectY = (paddle1.position.y-paddle1.length/2)-self.position.y
                normalizedRelativeIntersectionY = (relativeIntersectY/(paddle1.length/2))
                bounceAngle = normalizedRelativeIntersectionY * 40
                self.velocity.x = math.cos(bounceAngle)*(-1-self.ballSpeed)
                self.velocity.y = -abs(math.sin(bounceAngle))*(-1-self.ballSpeed)
                self.position.x += self.velocity.x * dt*3
                self.position.y += self.velocity.y * dt*3
                if self.position.x <= paddle1.position.x:
                    self.position.x = paddle1.position.x+1
        if int(self.position.x) in range(int(paddle2.position.x),int(paddle2.position.x)+3):
            if int(self.position.y) in range(paddle2.position.y - paddle2.length+1,paddle2.position.y):
                relativeIntersectY = (paddle2.position.y-paddle2.length/2)-self.position.y
                normalizedRelativeIntersectionY = (relativeIntersectY/(paddle2.length/2))
                bounceAngle = normalizedRelativeIntersectionY * 40
                self.velocity.x = math.cos(bounceAngle)*(1-self.ballSpeed)
                self.velocity.y = -abs(math.sin(bounceAngle))*(-1-self.ballSpeed)
                self.position.x += self.velocity.x * dt*3
                self.position.y += self.velocity.y * dt*3
                if self.position.x >= paddle2.position.x:
                    self.position.x = paddle2.position.x-1

class paddle:
    position = vector2d(0, 0)
    character = '|'
    ulimit = 0
    dlimit = 0
    def __init__(self, x, y, l, u, d, char='|'):
        self.position = vector2d(x, y)
        self.length = l
        self.ulimit = u
        self.dlimit = d
        self.character = char


