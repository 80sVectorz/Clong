from baseDataTypes import *
import gameObjects
from rich.console import Console
import time,os,sys,keyboard,threading
operatingSystem = "windows"
if os.name == "posix":
    operatingSystem = "linux"
    os.system('xhost +local:')
from pynput.keyboard import Key, Listener, Events

class window:
    w,h = 0,0
    grid = []
    def __init__(self,w,h):
        self.w,self.h=w,h

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
            print(u'\u001b[5m'+u'Press space to start'[:i+1]+u'\u001b[25m',end="")
            time.sleep(0.05)
            print(u'\u2592'*len("Press space to start")+"\r",end="")
            print(f"\u001b[{int(h/2)+2};{int(w/2-10)}H",end="")
        print(u'\u001b[H',end="")
        #Wait for space to start:
        while True:
            if keyboard.is_pressed(' '):
                break
            time.sleep(0.1)
        #Fill window with empty space:
        for i in range(h):
            print(u"\u2800"*w+"\n",end="\r")
    def clear(self):
        print('\u001b[H',end="")
        for i in range(self.h+1):
            print(u"\u2800"*self.w,end="\r")
            print(u"\u001b[1B",end="")
    def drawBat(self,bat):
        print(f"\u001b[{self.h-bat.position.y};{bat.position.x}H",end="")
        for i in range(bat.length):    
            print(f"\u001b[{self.h-bat.position.y+i};{bat.position.x}H",end="")
            print(f"{bat.character}\r",end="")
            #print(u"\u001b[1B",end="")
        print('\u001b[H',end="")
    def drawBall(self,ball):
        print(f"\u001b[{int(self.h-ball.position.y)};{int(ball.position.x)}H",end="")
        print(f"\u001b[1B",end="")
        print(f"{ball.character}\r",end="")
        print('\u001b[H',end="")
    def debug_draw_colliders(self,colliders):
        for c in colliders:
            for i in range(c.h):
                for j in range(c.w):
                    print(f"\u001b[{self.h-c.y-i};{c.x+j}H",end="")
                    print(f"\u2592\r",end="")
            print('\u001b[H',end="")
        print('\u001b[H',end="")

ball = gameObjects.ball(40, 20, -1, -1)
p1Bat = gameObjects.bat(4, 1,8, 50, 0)
p2Bat = gameObjects.bat(76, 1,8, 50, 0)

static_colliders=[
    gameObjects.collider(1, 1, 79, 2),
    gameObjects.collider(1, 1, 2, 79),
    gameObjects.collider(1, 39, 79, 2),
    gameObjects.collider(79, 1, 2, 79),
        ]
bat_colliders=[
    gameObjects.collider(p1Bat.position.x, p1Bat.position.y, 1, p1Bat.length),
    gameObjects.collider(p2Bat.position.x, p2Bat.position.y, 1, p2Bat.length),
    ]

win = window(80,40)

def on_press(key):
    global p1Bat,p2Bat
    try:
        if key.char == 'w':
            p1Bat.position.y+=1
        elif key.char == 's':
            p1Bat.position.y-=1
        elif key.char == 'i':
            p2Bat.position.y+=1
        elif key.char == 'k':
            p2Bat.position.y-=1
    except:
        pass

def on_release(key):
    return

listener = Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()
"""
Main loop
"""
releaseBuffer = 0
curTime = time.time()
while True:
    curTime,dt = time.time(),time.time()-curTime
    bat_colliders[0].y = p1Bat.position.y
    bat_colliders[1].y = p2Bat.position.y
    win.clear()
    win.drawBat(p1Bat)
    win.drawBat(p2Bat)
    win.drawBall(ball)
    win.debug_draw_colliders([static_colliders[0],static_colliders[2]])
    ball.update(0.2,p1Bat,p2Bat,colliders=static_colliders+bat_colliders)
    time.sleep(0.01)


