from GameHandler import GameHandler
import json

from TestHandler import TestHandler


class SystemHandler:
    game=GameHandler()#todo default message

    Table = [['N', 'N', 'N', 'N'], ['N', 'N', 'N', 'N'], ['N', 'N', 'N', 'N'], ['N', 'N', 'N', 'N']]
    target = [None,None]
    position=[0,0]
    next_corner=[None,None]
    orientation =[1,0]
    neutrals =[]
    neutral_idx=0
    active =None



    def __init__(self,defaultM):
        self.default_message=defaultM
        self.testHandler=TestHandler(defaultM)
        self.Table[0][0]= 'P'
        self.orientation ="up"
        self.target = [None, None]
        self.position = [0, 0]
        self.next_corner = [None, None]



    def getEnemyMove(self):
        self.active="getEnemeyMove"
        self.neutrals=self.game.getNeutral()
        self.neutral_idx=0
        self.setGoal(self.neutrals[self.neutral_idx])

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
        res=[self.target[0]-self.position[0],self.target[1]-self.position[1]]


    def setGoal(self,corner):
        self.target=corner

    def lookUp(self,idx):
        if(idx == 0):
            return [2,0]
        if (idx == 1):
            return [2, 1]
        if (idx == 2):
            return [2, 2]
        if (idx == 3):
            return [1, 0]
        if (idx == 4):
            return [1, 1]
        if (idx == 5):
            return [1, 2]
        if (idx == 6):
            return [0, 0]
        if (idx == 7):
            return [0, 1]
        if (idx == 8):
            return [0, 2]

    def print(self):
        print(self.Table[0][0]+" "+self.Table[0][1]," "+self.Table[0][2]+ " "+self.Table[0][3])
        print(self.Table[1][0]+" "+self.Table[1][1]," "+self.Table[1][2]+ " "+self.Table[1][3])
        print(self.Table[2][0]+" "+self.Table[2][1]," "+self.Table[2][2]+ " "+self.Table[2][3])
        print(self.Table[3][0]+" "+self.Table[3][1]," "+self.Table[3][2]+ " "+self.Table[3][3])



