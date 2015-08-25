from direct.directbase import DirectStart
from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
from direct.actor.Actor import Actor
from direct.gui.OnscreenText import OnscreenText
from panda3d.ode import OdeWorld

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

#hier kommen alle existierenden objekte rein
allObjects = {}

# diese klasse speichert welche tasten momentan gedrueckt werden
class KeyPollerClass( DirectObject ):
  def __init__( self ):
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
                    'space': Vec3(0,0,20)}

ROTATEFUNCTIONS = { 'q' : Vec3( 90,0,0),
                    'e': Vec3(-90,0,0)}

# Function to put instructions on the screen.
def addInstructions(pos, msg):
    return OnscreenText(text=msg, style=1, fg=(1,1,1,1), pos=(-1.3, pos), align=TextNode.ALeft, scale = .05)

class World:
    def __init__(self):
        addInstructions(0.95, 'Text ')
        self.buildWorld()
        self.mainCharakter = self.buildChar()
        self.buildOtherStuff()
        taskMgr.add(self.loop, 'loop')

    def loop(self, task):
        self.space.autoCollide()
        self.world.quickStep(globalClock.getDt())

        for obj, geo in allObjects.iteritems():
            obj.setPosQuat(render, geo.getPosition(), Quat(geo.getQuaternion()))

        self.contacts.empty()

        self.moveCam()
        self.moveChar()
        self.rotateChar()

        for obj, geo in allObjects.iteritems():
            self.geo.setPosition(self.obj.getPos(render))
            self.geo.setQuaternion(self.obj.getQuat(render))
        return task.cont

    def buildWorld(self):
        # lade eine umgebung
        environment = loader.loadModel('environment')
        environment.reparentTo(render)
        environment.setPos(0,0,0)

        # erstelle gravitation
        self.world = OdeWorld()
        self.world.setGravity(0, 0, -9.81)
        self.world.initSurfaceTable(1)
        self.world.setSurfaceEntry(0, 0, 150, 0.0, 9.1, 0.9, 0.00001, 0.0, 0.002)

        self.space = OdeSimpleSpace()
        self.space.setAutoCollideWorld(self.world)
        self.contacts = OdeJointGroup()
        self.space.setAutoCollideJointGroup(self.contacts)

        cm = CardMaker("ground")
        x = 100
        cm.setFrame(-x, x, -x, x)
        ground = render.attachNewNode(cm.generate())
        ground.setPos(0, 0, 0)
        ground.lookAt(0, 0, -1)
        groundGeom = OdePlaneGeom(self.space, Vec4(0, 0, 1, 0))
        groundGeom.setCollideBits(BitMask32(0x00000001))
        groundGeom.setCategoryBits(BitMask32(0x00000002))

    def buildChar(self):
        # lade den character
        character = loader.loadModel('box')
        character.reparentTo(render)
        character.setPos(0,0,10)

        M = OdeMass()
        M.setBox(50, 1, 1, 1)

        boxBody = OdeBody(self.world)
        boxBody.setMass(M)
        boxBody.setPosition(character.getPos(render))
        boxBody.setQuaternion(character.getQuat(render))
        boxGeom = OdeBoxGeom(self.space, 1,1,1)
        boxGeom.setCollideBits(BitMask32(0x00000002))
        boxGeom.setCategoryBits(BitMask32(0x00000001))
        boxGeom.setBody(boxBody)

        # positioniere die kamera
        base.disableMouse()
        base.camera.reparentTo(character)
        base.camera.setPos(0,40,20)
        base.camera.lookAt(0,0,5)

        allObjects[character]=boxBody
        return character

    def buildOtherStuff(self):
        teabot = loader.loadModel('teapot')
        teabot.reparentTo(render)
        teabot.setPos(0,10,20)

    def moveChar(self):
        for key, action in MOVEFUNCTIONS.items():
          if keyPoller[ key ]:
            self.mainCharakter.setPos(self.mainCharakter, action * globalClock.getDt())

    def rotateChar(self):
        for key, action in ROTATEFUNCTIONS.items():
          if keyPoller[ key ]:
            self.mainCharakter.setHpr(self.mainCharakter, action * globalClock.getDt())

    def moveCam(self):
        # trackt mausbewegung und aendert die ausrichtung der figur danach.
        if base.mouseWatcherNode.hasMouse():
            md      = base.win.getPointer(0)
            deltaX  = md.getX()
            deltaY  = md.getY()
            #print 'X: '+str(deltaX) +'Y: '+str(deltaY)
            self.mainCharakter.setHpr(deltaX * (-0.8),0,0)

if __name__ == '__main__':
  # dieser teil wird nur ausgefuehrt wenn dieses file _nicht_ importiert wird
  world = World()
  run()