from direct.directbase import DirectStart
from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
from direct.actor.Actor import Actor
from direct.gui.OnscreenText import OnscreenText
from panda3d.ode import OdeWorld

class Object:
    def __init__(self, model):
        self.obj = loader.loadModel(model)
        self.obj.reparentTo(render)

    def setPosition(self, x, y, z):
        self.obj.setPos(x,y,z)