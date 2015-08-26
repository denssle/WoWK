from direct.directbase import DirectStart
from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
from direct.actor.Actor import Actor
from direct.gui.OnscreenText import OnscreenText
from panda3d.ode import OdeWorld
import World
import Character

#hier kommen alle existierenden objekte rein
allObjects = []

# Function to put instructions on the screen.
def addInstructions(pos, msg):
    return OnscreenText(text=msg, style=1, fg=(1,1,1,1), pos=(-1.3, pos), align=TextNode.ALeft, scale = .05)

class Main:
    def __init__(self):
        addInstructions(0.95, 'Text ')
        self.world = World.World()
        self.mainCharakter = Character.Character(self.world.odeWorld, self.world.space)
        self.buildOtherStuff()
        taskMgr.add(self.loop, 'loop')

    def loop(self, task):
        self.world.space.autoCollide()
        self.world.odeWorld.quickStep(globalClock.getDt())

        for obj, geo in allObjects.iteritems():
            obj.setPosQuat(render, geo.getPosition(), Quat(geo.getQuaternion()))

        self.world.contacts.empty()

        self.mainCharakter.moveCam()
        self.mainCharakter.moveChar()
        self.mainCharakter.rotateChar()

        for obj2, geo2 in allObjects.iteritems():
            self.geo2.setPosition(self.obj2.getPos(render))
            self.geo2.setQuaternion(self.obj2.getQuat(render))
        return task.cont

    def buildOtherStuff(self):
        teabot = loader.loadModel('teapot')
        teabot.reparentTo(render)
        teabot.setPos(0,10,20)

if __name__ == '__main__':
  # dieser teil wird nur ausgefuehrt wenn dieses file _nicht_ importiert wird
  main = Main()
  run()