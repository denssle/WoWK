from pandac.PandaModules import *
from panda3d.ode import OdeWorld

class World:
    def __init__(self):

        # lade eine umgebung
        environment = loader.loadModel('world')
        environment.reparentTo(render)
        environment.setPos(0,0,0)

        # erstelle gravitation
        self.__odeWorld = OdeWorld()
        self.__odeWorld.setGravity(0, 0, -9.81)
        self.__odeWorld.initSurfaceTable(1)
        self.__odeWorld.setSurfaceEntry(0, 0, 150, 0.0, 9.1, 0.9, 0.00001, 0.0, 0.002)

        self.__space = OdeSimpleSpace()
        self.__space.setAutoCollideWorld(self.__odeWorld)
        self.__contacts = OdeJointGroup()
        self.__space.setAutoCollideJointGroup(self.__contacts)

        cm = CardMaker("ground")
        x = 1000
        cm.setFrame(-x, x, -x, x)
        ground = render.attachNewNode(cm.generate())
        ground.setPos(0, 0, -10)
        ground.lookAt(0, 0, -1)
        groundGeom = OdePlaneGeom(self.__space, Vec4(0, 0, 1, 0))
        groundGeom.setCollideBits(BitMask32(0x00000001))
        groundGeom.setCategoryBits(BitMask32(0x00000002))

        print "Welt erschaffen. "

        #Alle Objekte:
        self.__allObjects = []

    def clearContacts(self):
        self.contacts.empty()

    def __getWorld(self):
        return self.__odeWorld

    def __setWorld(self, world):
        self.__odeWorld = world
    odeWorld = property(__getWorld, __setWorld)

    def __getSpace(self):
        return self.__space

    def __setSpace(self, space):
        self.__space = space
    space = property(__getSpace, __setSpace)

    def __getContacts(self):
        return self.__contacts

    def __setContacs(self, contacts):
        self.__contacts = contacts
    contacts = property(__getContacts, __setContacs)

    def getAllObjects(self):
        return self.__allObjects

    def addToObjects(self, object):
        self.__allObjects.append(object)


    def setModelOnGeom(self):
        for obj in self.__allObjects:
            obj.setPosOnGeo()
        self.clearContacts()

    def setGeomOnModel(self):
        for obj in self.__allObjects:
            obj.setGeoOnPos()