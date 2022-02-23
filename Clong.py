from math import e
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
    windowChangeBuffer = []
    
    def inBuffer(self,pos,char=None):
        indexes = []
        if char == None:
            I = 0
            for i in self.windowChangeBuffer:
                if i[0] == pos:
                    indexes.append(I)
                I+=1
        else:
            I = 0
            for i in self.windowChangeBuffer:
                if i[1] == char:
                    indexes.append(I)
                I+=1
        return indexes
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
        for i in range(h+1):
            print(u"\u2800"*w+"\n",end="\r")
    def clear(self):
        print('\u001b[H',end="")
        print('\u001b[J',end="")
        # for i in range(self.h+1):
        #     print(u"\u2800"*(self.w),end="\r")
        #     print(u"\u001b[1B",end="")
    def draw_paddle(self,paddle):
        print(f"\u001b[{self.h-paddle.position.y};{paddle.position.x}H",end="")
        for i in range(paddle.length):
            print(f"\u001b[{self.h-paddle.position.y+i};{paddle.position.x}H",end="")
            print(f"{paddle.character}\r",end="")
            self.windowChangeBuffer.append([[int(self.h-paddle.position.y+i),int(paddle.position.x)],paddle.character])
            #print(u"\u001b[1B",end="")
        print('\u001b[H',end="")

    def draw_ball(self,ball):
        if [[int(self.h-ball.position.y),int(ball.position.x)],ball.character] in self.windowChangeBuffer:
            return
        else:
            self.clear_ball(ball)
            self.windowChangeBuffer.append([[int(self.h-ball.position.y),int(ball.position.x)],ball.character])
            print(f"\u001b[{int(self.h-ball.position.y)};{int(ball.position.x)}H",end="")
            print(f"\u001b[1B",end="")
            print(f"{ball.character}\r",end="")
            print('\u001b[H',end="")
    def clear_ball(self,ball):
        indexes = self.inBuffer([0,0],ball.character)
        if len(indexes) != 0:
            for i in indexes:
                print(f"\u001b[{self.windowChangeBuffer[i][0][0]};{self.windowChangeBuffer[i][0][1]}H",end="")
                print(f"\u001b[1B",end="")
                print(u" \r",end="")
                print('\u001b[H',end="")
            #remove all the indexes from the buffer:
            for i in indexes:
                self.windowChangeBuffer[i] = None
            #remove all the None values from the buffer:
            self.windowChangeBuffer = [i for i in self.windowChangeBuffer if i != None]
    def clear_paddle(self,paddle):
        for i in range(paddle.dlimit-paddle.length+1,paddle.ulimit-1):    
            print(f"\u001b[{i};{paddle.position.x}H",end="")
            print(u" \r",end="")
            #print(u"\u001b[1B",end="")
    def debug_draw_colliders(self,colliders):
        for c in colliders:
            for i in range(min(c.h,self.h)):
                for j in range(min(c.w,self.w)):
                    if [[self.h-c.y-i,c.x+j],'\u2592'] in self.windowChangeBuffer:
                        continue
                    else:
                        self.windowChangeBuffer.append([[self.h-c.y-i,c.x+j],'\u2592'])
                    print(f"\u001b[{self.h-c.y-i};{c.x+j}H",end="")
                    print(f"\u2592\r",end="")
            print('\u001b[H',end="")
        print('\u001b[H',end="")
    def draw_scores(self,scores):
        print(f"\u001b[;{int(self.w/2)}H",end="") 
        print(f"{scores[0]}:{scores[1]}\r",end="")


ball = gameObjects.ball(40, 20, -1, -1)
p1paddle = gameObjects.paddle(8, 11,8, 39, 9)
p2paddle = gameObjects.paddle(76, 11,8, 39, 9)

static_colliders=[
    gameObjects.collider(0, 0, 90, 3),
    gameObjects.collider(0, 0, 5, 100),
    gameObjects.collider(0, 40, 90, 5),
    gameObjects.collider(80, 0, 5, 100),
        ]
paddle_colliders=[
    gameObjects.collider(p1paddle.position.x, p1paddle.position.y, 1, p1paddle.length),
    gameObjects.collider(p2paddle.position.x, p2paddle.position.y, 1, p2paddle.length),
    ]

win = window(80,40)

def on_press(key):
    global p1paddle,p2paddle
    try:
        if key.char == 'w':
            if p1paddle.position.y+1 < p1paddle.ulimit:
                win.clear_paddle(p1paddle)
                p1paddle.position.y+=1
        elif key.char == 's':
            if p1paddle.position.y-1 > p1paddle.dlimit:
                win.clear_paddle(p1paddle)
                p1paddle.position.y-=1
        elif key.char == 'i':
            if p2paddle.position.y+1 < p2paddle.ulimit:
                win.clear_paddle(p2paddle)
                p2paddle.position.y+=1
        elif key.char == 'k':
            if p2paddle.position.y-1 > p2paddle.dlimit:
                win.clear_paddle(p2paddle)
                p2paddle.position.y-=1 
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
scores = [0,0]
while True:
    curTime,dt = time.time(),time.time()-curTime
    paddle_colliders[0].y = p1paddle.position.y
    paddle_colliders[1].y = p2paddle.position.y
    time.sleep(0.01)
    #win.clear()
    win.clear_ball(ball)
    win.draw_paddle(p1paddle)
    win.draw_paddle(p2paddle)
    win.draw_ball(ball)
    win.debug_draw_colliders(static_colliders)#[static_colliders[0],static_colliders[2]])
    scored = ball.update(dt*10,p1paddle,p2paddle,colliders=static_colliders,p1goal=static_colliders[1],p2goal=static_colliders[3])
    if scored == 1:
        scores[0]+=1
        ball.ballSpeed=0.1
        ball.position = vector2d(int(win.w/2),int(win.h/2))
        ball.velocity = vector2d(-0.5,0)
    elif scored == 2:
        scores[1]+=1
        ball.ballSpeed=0.1
        ball.position = vector2d(int(win.w/2),int(win.h/2))
        ball.velocity = vector2d(0.5,0)
    win.draw_scores(scores)
    


