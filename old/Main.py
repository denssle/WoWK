import sys

from direct.ffi.DoGenPyCode import run
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.ShowBase import ShowBase
from direct.task.TaskManagerGlobal import taskMgr

import Character
import Object
import World


# Function to put instructions on the screen.
def addInstructions(pos, msg):
    return OnscreenText(text=msg, style=1, fg=(1,1,1,1), pos=(-1.3, pos), align=TextNode.ALeft, scale = .05)

class Main(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        addInstructions(0.95, 'Text ')

        self.world = World.World()
        self.mainCharakter = Character.Character(self.world.odeWorld, self.world.space)
        self.world.addToObjects(self.mainCharakter)
        #self.eventHandler = EventHandler.EventHandler()
        self.makeSomeTea()

        taskMgr.add(self.worldTasksBeforCharacter, 'worldTask01')
        taskMgr.add(self.charakterTasks, 'charakterTask02')
        taskMgr.add(self.worldTasktsAfterCharacter, 'worldTask02')
        self.accept("escape", sys.exit)

    def worldTasksBeforCharacter(self, task):
        #Kollisionen werden gesammelt, Gravitation ausgewfuehrt und das Modell auf die Position des Geoms gesetzt.
        self.world.space.autoCollide()
        self.world.odeWorld.quickStep(globalClock.getDt())
        self.world.setModelOnGeom()
        self.world.checkForCollision()
        return task.cont

    def charakterTasks(self, task):
        #Charakter und Kamara koennen bewegt werden. Steht der Char falsch wird das korrigiert
        self.mainCharakter.moveCam()
        self.mainCharakter.moveChar()
        self.mainCharakter.sos()
        return task.cont

    def worldTasktsAfterCharacter(self, task):
        #das Gemom wird auf die eventuell neue Position des Charakters verlegt
        self.world.setGeomOnModel()
        return task.cont

    def makeSomeTea(self):
        teapot01 = Object.Object('teapo01',
                                 'teapot',
                                 self.world.odeWorld,
                                 self.world.space,
                                 0, 10, 40)
        self.world.addToObjects(teapot01)

        teapot02 = Object.Object('teapo02',
                                 'teapot',
                                 self.world.odeWorld,
                                 self.world.space,
                                 0, 10, 80)
        self.world.addToObjects(teapot02)

if __name__ == '__main__':
    main = Main()
    run()