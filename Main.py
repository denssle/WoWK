from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import *
from direct.gui.OnscreenText import OnscreenText
import World
import Character
import Object


# Function to put instructions on the screen.
def addInstructions(pos, msg):
    return OnscreenText(text=msg, style=1, fg=(1,1,1,1), pos=(-1.3, pos), align=TextNode.ALeft, scale = .05)

class Main(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        wp = WindowProperties()
        wp.setSize(1000, 800)

        addInstructions(0.95, 'Text ')

        self.world = World.World()
        self.mainCharakter = Character.Character(self.world.odeWorld, self.world.space)
        self.world.addToObjects(self.mainCharakter)

        self.makeSomeTea()

        taskMgr.add(self.loop, 'loop')

    def loop(self, task):
        self.world.space.autoCollide()
        self.world.odeWorld.quickStep(globalClock.getDt())

        for obj in self.world.getAllObjects():
            obj.setPosOnGeo()
        self.world.clearContacts()

        self.mainCharakter.moveCam()
        self.mainCharakter.moveChar()
        self.mainCharakter.sos()

        for obj in self.world.getAllObjects():
            obj.setGeoOnPos()

        return task.cont

    def makeSomeTea(self):
        teapot01 = Object.Object('teapo01',
                                 'teapot',
                                self.world.odeWorld,
                               self.world.space,
                               0,10,40)
        self.world.addToObjects(teapot01)

        teapot02 = Object.Object('teapo02',
                                 'teapot',
                                self.world.odeWorld,
                               self.world.space,
                               0,10,80)
        self.world.addToObjects(teapot02)

if __name__ == '__main__':
    main = Main()
    run()