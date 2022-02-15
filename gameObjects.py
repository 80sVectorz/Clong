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
        self.velocity = vector2d(vx, vy)
        self.character = char
    def update(self, dt,bat1,bat2,colliders=[]):
        self.position.x += self.velocity.x * dt
        self.position.y += self.velocity.y * dt
        for c in colliders:
            if int(self.position.x) in range(c.x, c.x + c.w):
                if int(self.position.y) in range(c.y, c.y + c.h):
                    modifier = 0.2
                    if abs(self.velocity.x) > 1:
                        modifier=0
                    if c.h > c.w:
                        self.velocity.y *= -1-modifier
                    elif c.w > c.h:
                        self.velocity.x *= -1-modifier
                    else:
                        self.velocity.x *= -1-modifier
                        self.velocity.y *= -1-modifier
                    self.velocity.x *= -1-modifier
                    self.velocity.y *= -1-modifier
                    self.position.x += self.velocity.x * dt*2
                    self.position.y += self.velocity.y * dt*2
        if self.position.x <= bat1.position.x:
            if int(self.position.y) in range(bat1.position.y, bat1.position.y - bat1.length,-1):
                relativeIntersectY = (bat1.position.y-int(bat1.length/2))+self.position.y
                normalizedRelativeIntersectionY = (relativeIntersectY/(bat1.length/2))
                bounceAngle = normalizedRelativeIntersectionY * 70
                self.velocity.x = math.cos(bounceAngle)
                self.velocity.y = -math.sin(bounceAngle)
                self.position.x += self.velocity.x * dt*2
                self.position.y += self.velocity.y * dt*2
        if self.position.x >= bat2.position.x:
            if int(self.position.y) in range(bat2.position.y, bat2.position.y + bat2.length,-1):
                relativeIntersectY = (bat2.position.y-int(bat2.length/2))+self.position.y
                normalizedRelativeIntersectionY = (relativeIntersectY/(bat2.length/2))
                bounceAngle = normalizedRelativeIntersectionY * 70
                self.velocity.x = math.cos(bounceAngle)
                self.velocity.y = -math.sin(bounceAngle)
                self.position.x += self.velocity.x * dt*2
                self.position.y += self.velocity.y * dt*2

class bat:
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


