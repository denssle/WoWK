from direct.directbase import DirectStart
from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
from direct.actor.Actor import Actor
from direct.gui.OnscreenText import OnscreenText
from panda3d.ode import OdeWorld

class Object:
    def __init__(self, model, world, space):
        self.obj = loader.loadModel(model)
        self.obj.reparentTo(render)

        M = OdeMass()
        M.setBox(50, 1, 1, 1)

        self.boxBody = OdeBody(world)
        self.boxBody.setMass(M)
        self.boxBody.setPosition(self.obj.getPos(render))
        self.boxBody.setQuaternion(self.obj.getQuat(render))
        boxGeom = OdeBoxGeom(space, 1,1,1)
        boxGeom.setCollideBits(BitMask32(0x00000002))
        boxGeom.setCategoryBits(BitMask32(0x00000001))
        boxGeom.setBody(self.boxBody)

        print str(model)+' erschaffen. '

    def setPosition(self, x, y, z):
        self.obj.setPos(x,y,z)

    def setPosOnGeo(self):
        self.obj.setPosQuat(render, self.boxBody.getPosition(), Quat(self.boxBody.getQuaternion()))

    def setGeoOnPos(self):
        self.boxBody.setPosition(self.obj.getPos(render))
        self.boxBody.setQuaternion(self.obj.getQuat(render))