from GameHandler import GameHandler
import json

from TestHandler import TestHandler


class SystemHandler:
    game=GameHandler()#todo default message

    Table = [['N', 'N', 'N', 'N'], ['N', 'N', 'N', 'N'], ['N', 'N', 'N', 'N'], ['N', 'N', 'N', 'N']]
    next_corner=[None,None]
    orientation =[1,0]
    neutrals =[]
    neutral_idx=0
    active =None
    dif=None



    def __init__(self,defaultM):
        self.default_message=defaultM
        self.testHandler=TestHandler(defaultM)
        self.Table[0][0]= 'P'
        self.target = [0, 0]
        self.position = [3, 0]
        self.orientation=[1,0]
        self.next_corner = [None, None]



    def getEnemyMove(self):
        self.active="getEnemeyMove"
        self.neutrals=self.game.getNeutral()
        self.neutral_idx=0
        self.setGoal(self.neutrals[self.neutral_idx])
        #pr

    def checkField(self,idx):
        print("mudda")

    def handleMessage(self,message):
        res =[{}]
        message=json.loads(message.decode('utf-8'))
        if(message.get('ID')=="System"):
            self.handleSystem(message)
        if(message.get('Aktion')=="Test"):
            print("in test")
            return self.testHandler.handleMessage(message)

    def handleSystem(self,message):
        print("System message")




    def handleAktion(self, message):
        if(message.get('Turn')):
            self.getEnemyMove()
            return self.getOrder()
    def getOrder(self):
        if self.active=="getEnemeyMove":
            if self.target:
                order=self.findWay()
    def findWay(self):
        print("pos: ")
        print(self.position)
        print("or: ")
        print(self.orientation)

        self.dif=[self.target[0]-self.position[0],self.target[1]-self.position[1]] #difference
        if self.dif == [0,0]:
            return True
        if self.testMove(self.orientation):
            print("in s : "+ str(self.testMove(self.orientation)))
            return "s" ##straight
        if self.testMove(self.getRight()):
            return "r"
        if self.testMove(self.getLeft()):
            return "l"
        if self.valid(self.getLeft()):
            return "l"
        if self.valid(self.getRight()):
            return "r"
        print("ERRRRRRRRRROR")
        return None

    def doMove(self,m):
        if m =="s":
            self.position[0]=self.position[0]+self.orientation[0]
            self.position[1] = self.position[1] + self.orientation[1]
            print("s")
        if m =="r":
            self.position[0] = self.position[0] + self.getRight()[0]
            self.position[1] = self.position[1] + self.getRight()[1]
            self.orientation = self.getRight()
            print("r")
        if m =="l":
            self.position[0] = self.position[0] + self.getLeft()[0]
            self.position[1] = self.position[1] + self.getLeft()[1]
            self.orientation=self.getLeft()
            print("l")



    def setGoal(self,corner):
        self.target=corner

    def testMove(self,testmove):
        testmove = self.valid(testmove)
        if testmove == None:
            print("test not valid")
            return False
        else :
            helpdifx=self.dif[0]
            helpdify=self.dif[1]
            if helpdifx < 0:
                helpdifx = helpdifx *-1
            if helpdify < 0:
                helpdify = helpdify *-1

            difsum=helpdifx+helpdify

            diftestx= testmove[0]-self.target[0]
            diftesty = testmove[1] - self.target[1]
            if diftestx <0 :
                diftestx=diftestx *-1
            if diftesty <0 :
                diftesty=diftesty *-1
            testsum= diftestx+diftesty
            if testsum< difsum:
                return testmove
            return False

    def valid(self,move):
        if self.position[0]+move[0]>3  or self.position[0]+move[0]<0 or self.position[1]+move[1]>3  or self.position[1]+move[1]<0:
            print("nOT FUCKING VALID: "+ str(move[0])+ " "+ str(move[1]))
            return None
        return [self.position[0]+move[0],self.position[1]+move[1]]

    def testRight(self):
        self.testMove(self.getRight())

    def getRight(self):
        if self.orientation[0] == 1:
            return [0,-1]
        if self.orientation[0] ==-1:
            return [0,1]
        if self.orientation[1] == 1:
            return [1,0]
        if self.orientation[1] ==-1:
            return [-1,0]
        print("ERROR")
        return None
    def getLeft(self):
        if self.orientation[0] == 1:
            return [0,1]
        if self.orientation[0] ==-1:
            return [0,-1]
        if self.orientation[1] == 1:
            return [-1,0]
        if self.orientation[1] ==-1:
            return [1,0]
        print("ERROR")
        return None

    def lookUp(self,idx):
        if(idx == 0):
            return [0,0]
        if (idx == 1):
            return [0, 1]
        if (idx == 2):
            return [0, 2]
        if (idx == 3):
            return [0, 3]
        if (idx == 4):
            return [1, 0]
        if (idx == 5):
            return [1, 1]
        if (idx == 6):
            return [1, 2]
        if (idx == 7):
            return [1, 3]
        if (idx == 8):
            return [2,0]
        if (idx == 9):
            return [2, 1]
        if (idx == 10):
            return [2, 2]
        if (idx == 11):
            return [2, 3]
        if (idx == 12):
            return [3, 0]
        if (idx == 13):
            return [3, 1]
        if (idx == 14):
            return [3, 2]
        if (idx == 15):
            return [3, 3]

    def print(self):
        print(self.Table[0][0]+" "+self.Table[0][1]," "+self.Table[0][2]+ " "+self.Table[0][3])
        print(self.Table[1][0]+" "+self.Table[1][1]," "+self.Table[1][2]+ " "+self.Table[1][3])
        print(self.Table[2][0]+" "+self.Table[2][1]," "+self.Table[2][2]+ " "+self.Table[2][3])
        print(self.Table[3][0]+" "+self.Table[3][1]," "+self.Table[3][2]+ " "+self.Table[3][3])



