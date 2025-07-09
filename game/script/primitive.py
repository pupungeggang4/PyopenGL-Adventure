class Vector2():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Vector3():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class Cuboid3():
    def __init__(self, x, y, z, w, h, d):
        self.pos = Vector3(x, y, z)
        self.size = Vector3(w, h, d)