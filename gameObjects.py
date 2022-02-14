from baseDataTypes import vector2d
from rich.console import Console
import time

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
    def update(self, dt, colliders=[]):
        self.position.x += self.velocity.x * dt
        self.position.y += self.velocity.y * dt
        for c in colliders:
            if self.position.x + self.velocity.x * dt > c.x and self.position.x + self.velocity.x * dt < c.x + c.w:
                if self.position.y + self.velocity.y * dt > c.y and self.position.y + self.velocity.y * dt < c.y + c.h:
                    self.velocity.x *= -1
                    self.position.x += self.velocity.x * dt
                    self.position.y += self.velocity.y * dt
            if self.position.x + self.velocity.x * dt > c.x and self.position.x + self.velocity.x * dt < c.x + c.w:
                if self.position.y + self.velocity.y * dt > c.y and self.position.y + self.velocity.y * dt < c.y + c.h:
                    self.velocity.y *= -1
                    self.position.x += self.velocity.x * dt
                    self.position.y += self.velocity.y * dt

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


