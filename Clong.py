from baseDataTypes import *
import gameObjects
from rich.console import Console
import time
class window:
    w,h = 0,0
    grid = []
    def __init__(self,w,h):
        self.w,self.h=w,h
        self.console = Console(
            width=w,
            height=h,
        )
        """
        Intro animation
        """
        print("\u001b[J")#clear screen
        #Create empty window:
        for i in range(h):
            print(u"\u2800"*w+"\n",end="")
        print(f"\u001b[{h}A",end="")
        #Fill animation:
        for i in range(h):
            print(u"\u001b[1B",end="")
            time.sleep(0.05)
            print(u"\u2592"*w+"\r",end="")
        #Print 'Clong!' with typewriter effect:
        print(f"\u001b[{int(h/2)-4};{int(w/2-2)}H",end="")
        for i in range(len("Clong!")):
            print(u'Clong!'[:i+1],end="")
            time.sleep(0.05)
            print(u'\u2592'*len("Clong!")+"\r",end="")
            print(f"\u001b[{int(h/2)-4};{int(w/2-2)}H",end="")
        #Show 'Press space to start' with typewriter effect 4 lines below:
        print(f"\u001b[{int(h/2)+2};{int(w/2-10)}H",end="")
        for i in range(len("Press space to start")):
            print(u'Press space to start'[:i+1],end="")
            time.sleep(0.05)
            print(u'\u2592'*len("Press space to start")+"\r",end="")
            print(f"\u001b[{int(h/2)+2};{int(w/2-10)}H",end="")
        print(u'\u001b[H',end="")
ball = gameObjects.ball(50, 25, 1, 1)
p1Bat = gameObjects.bat(1, 15,10, 50, 0)
p2Bat = gameObjects.bat(99, 15,10, 50, 0)

static_colliders=[
    gameObjects.collider(1, 1, 100, 1),
    gameObjects.collider(1, 1, 1, 100),
    gameObjects.collider(99, 1, 100, 1),
    gameObjects.collider(1, 99, 1, 100),
        ]
bat_colliders=[
    gameObjects.collider(p1Bat.position.x, p1Bat.position.y, 1, p1Bat.length),
    gameObjects.collider(p2Bat.position.x, p2Bat.position.y, 1, p2Bat.length),
    ]

win = window(100,50)
