from direct.directbase.DirectStart import base
from direct.showbase.DirectObject import DirectObject
from direct.actor.Actor import Actor
import string

# liste von events die wir abfangen
POLLKEYS = list(string.ascii_lowercase+string.digits)
POLLKEYS.extend(
  [ '_del', 'alt', 'asciiKey', 'backspace', 'capsLock', 'control', 'down', 'end', 'enter', 'escape', \
    'f1', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', \
    'f9', 'help', 'home', 'insert', 'lalt', 'lcontrol', 'left', 'lshift', 'meta', 'numLock', \
    'pageDown', 'pageUp', 'pause', 'printScreen', 'ralt', 'rcontrol', 'right', 'rshift', 'scrollLock', \
    'shift', 'shiftLock', 'space', 'tab', 'this', 'this_metatype', 'up',  'arrow_up', 'arrow_down', \
    'arrow_left', 'arrow_right' ] )

# diese klasse speichert welche tasten momentan gedrueckt werden
class KeyPollerClass( DirectObject ):
  def __init__(self):
    DirectObject.__init__(self)
    self.data = dict()
    for key in POLLKEYS:
      self.accept( key, self.event, [key, True] )
      self.accept( key+"-up", self.event, [key, False] )
      self.data[key] = False
  def event( self, key, active ):
    self.data[key] = active
  def __getitem__( self, key ):
    return self.data[key]
keyPoller = KeyPollerClass()

# defintion der tasten und der ausgefuehrten bewegung
MOVEFUNCTIONS = {   'w'   : Vec3(0,-20,0),
                    's'   : Vec3(0, 20,0),
                    'a'   : Vec3(20,0,0),
                    'd'   : Vec3(-20,0,0),
                    'space': Vec3(0,0,5 )}


class Character:
    def __init__(self, world, space):
        self.name = "Name"
        # lade den character
        self.character = Actor('models/box')
        self.character.setScale(0.5)
        self.character.reparentTo(render)
        self.character.setPos(0,0,30)

        M = OdeMass()
        M.setBox(50, 1, 1, 1)

        self.boxBody = OdeBody(world)
        self.boxBody.setMass(M)
        self.boxBody.setPosition(self.character.getPos(render))
        self.boxBody.setQuaternion(self.character.getQuat(render))
        boxGeom = OdeBoxGeom(space, 1,1,1)
        boxGeom.setCollideBits(BitMask32(0x00000002))
        boxGeom.setCategoryBits(BitMask32(0x00000001))
        boxGeom.setBody(self.boxBody)

        # positioniere die kamera
        base.disableMouse()
        base.camera.reparentTo(self.character)
        base.camera.setPos(0,40,20)
        base.camera.lookAt(self.character)

        #kollision
        self.collider = self.character.attachNewNode(CollisionNode(self.name))
        self.collider.node().addSolid(CollisionSphere(0, 0, 0, 1))

        print "Charakter erschaffen. "

    def getCharakter(self):
        return self.character

    def getGeo(self):
        return self.boxBody

    def setPosOnGeo(self):
        self.character.setPosQuat(render, self.boxBody.getPosition(), Quat(self.boxBody.getQuaternion()))

    def setGeoOnPos(self):
        self.boxBody.setPosition(self.character.getPos(render))
        self.boxBody.setQuaternion(self.character.getQuat(render))

    def moveChar(self):
        self.jump = False
        for key, action in MOVEFUNCTIONS.items():
            if keyPoller[key]:
                self.character.setPos(self.character, action * globalClock.getDt())
                if key is 'space':
                    self.jump = True

    def moveCam(self):
        # trackt mausbewegung und aendert die ausrichtung der figur und kamara danach.
        if base.mouseWatcherNode.hasMouse():
            md      = base.win.getPointer(0)
            xmod = -0.8
            ymod = 0.05
            deltaX  = md.getX()*xmod
            deltaY  = md.getY()*ymod
            #print 'X: '+str(deltaX) +' Y: '+str(deltaY)
            self.character.setHpr(deltaX,0,0)
            #base.camera.lookAt(0, deltaY, 15)
            base.camera.setPos(0,40,deltaY)
            base.camera.lookAt(self.character)

    def sos(self):
        #print str(self.character.getZ())
        if(self.character.getZ() > 200 or self.character.getZ < 0):
            print 'SOS'+ str(self.character.getZ())+' Boxy: '+str(self.boxBody.getAngularVel())
            self.character.setZ(50)
            self.boxBody.setPosition(self.character.getPos(render))
            self.boxBody.setQuaternion(self.character.getQuat(render))

    def getName(self):
        return 'character'

    def setZ(self, z):
        self.character.setZ(z)