from baseDataTypes
import gameObjects
from rich.console import Console

ball = gameObjects.Ball(50, 25, 1, 1)
p1Bat = gameObjects.Bat(1, 15,10, 50, 0)
p2Bat = gameObjects.Bat(99, 15,10, 50, 0)

static_colliders=[
    gameObjects.collider(1, 1, 100, 1),
    gameObjects.collider(1, 1, 1, 100),
    gameObjects.collider(99, 1, 100, 1),
    gameObjects.collider(1, 99, 1, 100),
        ]
bat_colliders=[
    gameObjects.collider(p1Bat.x, p1Bat.y, 1, p1Bat.length),
    gameObjects.collider(p2Bat.x, p2Bat.y, 1, p2Bat.length),
    ]


