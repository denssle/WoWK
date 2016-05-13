from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
from direct.actor.Actor import Actor
from direct.gui.OnscreenText import OnscreenText
from panda3d.ode import OdeWorld
import string

class World:
    def __init__(self):

        # lade eine umgebung
        environment = loader.loadModel('models/world')
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

        #kollision
        base.cTrav=CollisionTraverser()
        self.collisionHandler = CollisionHandlerQueue()

        print "Welt erschaffen. "

        #Alle Objekte:
        self.__allObjects = {}

    def clearContacts(self):
        self.__contacts.empty()

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
        self.__allObjects[object.name] = object
        base.cTrav.addCollider(object.collider, self.collisionHandler)

    def setModelOnGeom(self):
        for obj in self.__allObjects.values():
            obj.setPosOnGeo()
        self.clearContacts()

    def setGeomOnModel(self):
        for obj in self.__allObjects.values():
            obj.setGeoOnPos()

    def checkForCollision(self):
        for i in range(self.collisionHandler.getNumEntries()):
            entry = self.collisionHandler.getEntry(i)
            #print str(entry.getIntoNode().getName())
            #print str(entry.getFromNodePath().getNode(0).getName())
            if entry.getIntoNode().getName() == "terrain":
                for objectNames in self.__allObjects.keys():
                    if entry.getFromNodePath().getNode(0).getName() == objectNames:
                        self.__allObjects[objectNames].setZ(entry.getSurfacePoint(render).getZ())
                        #print str(objectNames)+ ' wurde in der Hoehe korrigiert. '
            else:
                for objectNames in self.__allObjects.keys():
                    if entry.getFromNodePath().getNode(0).getName() == objectNames:
                        attacker = self.__allObjects[objectNames].name

                    if entry.getIntoNode().getName() == objectNames:
                        victim = self.__allObjects[objectNames].name

                if(victim != attacker):
                    print victim + ' is the victim and ' + attacker + 'is the attacker. '
