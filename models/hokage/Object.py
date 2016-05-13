from pandac.PandaModules import *


class Object:
    def __init__(self, name, model, world, space,x, y, z):
        self.name = name
        self.obj = loader.loadModel('models/'+str(model))
        self.obj.reparentTo(render)
        self.obj.setPos(x,y,z)

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

        frowneyCollider = self.obj.attachNewNode(CollisionNode(name))
        frowneyCollider.node().addSolid(CollisionSphere(0, 0, 0, 1))

        #kollision
        self.collider = self.obj.attachNewNode(CollisionNode(name))
        self.collider.node().addSolid(CollisionSphere(0, 0, 0, 1))

        print name+' erschaffen. '

    def setPosOnGeo(self):
        self.obj.setPosQuat(render, self.boxBody.getPosition(), Quat(self.boxBody.getQuaternion()))

    def setGeoOnPos(self):
        self.boxBody.setPosition(self.obj.getPos(render))
        self.boxBody.setQuaternion(self.obj.getQuat(render))

    def getName(self):
        return self.name

    def setZ(self, z):
        self.obj.setZ(z)