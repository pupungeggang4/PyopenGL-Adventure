from script.module import *

class World_Player():
    def __init__(self):
        pass

class Camera():
    def __init__(self):
        self.pos = Vector3(0, 0, 0)
        self.rot = Vector3(0, 0, 0)

    def move(self, game):
        if game.key_pressed['l'] == True:
            self.pos.x -= 0.5 / 60
        if game.key_pressed['r'] == True:
            self.pos.x += 0.5 / 60
        if game.key_pressed['f'] == True:
            self.pos.z += 0.5 / 60
        if game.key_pressed['b'] == True:
            self.pos.z -= 0.5 / 60

class World():
    def __init__(self):
        self.camera = Camera()