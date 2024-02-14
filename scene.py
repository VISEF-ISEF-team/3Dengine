from model2 import *

class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.load()
        
    def add_object(self, object):
        self.objects.append(object)
        
    def load(self):
        app = self.app
        add = self.add_object
        
        length, step = 30, 2
        for x in range(-length, length, step):
            for z in range(-length, length, step):
                add(
                    Cube(app, pos=(x, -step, z))
                )

        add(
            Model(app, pos=(0, 0, 0), rot=(-90,0,0))
        )
            
    def render(self):
        for object in self.objects:
            object.render()