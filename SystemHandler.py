import lookUpTable
from GameHandler import GameHandler
import json

from TestHandler import TestHandler


class SystemHandler:


    Table = [['N', 'N', 'N', 'N'], ['N', 'N', 'N', 'N'], ['N', 'N', 'N', 'N'], ['N', 'N', 'N', 'N']]
    next_corner=[None,None]
    neutrals =[]
    neutral_idx=0
    active =None
    dif=None




    def __init__(self,defaultM):
        self.default_message=defaultM
        self.testHandler=TestHandler(defaultM)
        self.Table[0][0]= 'P'
        self.position = [0,0]
        self.orientation=[1,0]
        self.next_corner = [None, None]
        self.game = GameHandler(defaultM,kfirst="E")  # todo default message
        self.target=[3,0]
        self.aktivescan=False
        self.scanidx = 0
        self.Field_to_Table= lookUpTable.LookUpTable()

        if self.game.first =="E":
            print("da")
            self.aktion="waitUser"
            self.nextaktion="findUserInput"




    def getEnemyMove(self):
        #self.active="getEnemeyMove"
        #self.neutrals=self.game.getNeutral()
        #self.neutral_idx=0
        #self.setGoal(self.neutrals[self.neutral_idx])
        b = input('Choose a number: ')
        return b

    def checkField(self,idx):
        print("mudda")

    def handleMessage(self,message):
        res =[{}]
        print("in handle message")
        message=json.loads(message.decode('utf-8'))
        print("message:")
        print(message)

        if(message.get('ID')=="System"):
            self.handleSystem(message)
        if(message.get('Aktion')=="Test"):
            print("in test")
            return self.testHandler.handleMessage(message)



        if (message.get('Aktion') == "measureOver"):
            if message.get('Found')==True:
                print("in zug machen")
                #zug machen und schicken
                return self.makeMove()
                print("zug machen und schicken")
        if (message.get('Aktion') == "Befehl"):


            print(self.aktion)
            print(self.nextaktion)

            if not self.game.game_on:
                self.game = GameHandler(self.default_message)
                if self.game.first == "E":
                    self.aktion = "waitUser"
                    self.nextaktion = "findUserInput"

            if self.aktion=="waitUser":
                print("in waitUser")
                return self.sendwait()

            if self.aktion == "UserInputFind":
                if self.aktivescan:
                    if message.get('found'):
                        inputvalue =self.Field_to_Table.lookUpTable(self.position)
                        print(inputvalue)
                        x = input("yours?")
                        if x == "":
                            move = self.game.getMove(inputvalue)
                        else:
                            move=int(x)

                        print("davor targetting:")
                        print(self.target)
                        print("davor move:")
                        print(move)
                        #  self.target = self.lookUp(move)
                        self.target = self.Field_to_Table.lookUpField(move)
                        print("targetting:")
                        print(self.target)
                        way = self.findwholeway()
                        #  return self.doMove(self.findWay())
                        message = self.default_message
                        message['Aktion'] = "move"
                        message['way'] = way
                        print("return:")
                        print(message)
                        self.scanidx = 0
                        self.aktivescan = False

                        self.aktion = "sendprep"
                        self.nextaktion = "sendprep"
                        print("hinterhernim found")
                        print(self.aktion)
                        return message
                    if self.position == self.Field_to_Table.lookUpField(self.neutrals[self.scanidx]):
                        print("ist das selbe erhöhen")
                        self.scanidx = self.scanidx + 1

                    return self.handleScan()

                    print("no active scan errorrr")







            if self.aktion=="sendprep":
                print("send prep")
                return self.sendprep()

            if (self.aktion == "waiting" and self.nextaktion=="UserInputFind"):


                if self.nextaktion == "UserInputFind":  # wenn nicht weitersuchen
                    print("in findUserInput")
                    self.neutrals = self.game.getNeutral()
                    self.scanidx = 0
                    self.aktivescan = True
                    self.aktion = "UserInputFind"
                    self.nextaktion = "makemove"
                    return self.handleScan()


            if self.game.game_on:
                self.game.print()
                value = input("wählen sie ihr Feld: ")
                move= self.game.getMove(int(value))
                print("davor targetting:")
                print(self.target)
                print("davor move:")
                print(move)
                self.target = self.lookUp(move)
                print("targetting:")
                print(self.target)
                way = self.findwholeway()
                #  return self.doMove(self.findWay())
                message = self.default_message
                message['Aktion'] = "move"
                message['way'] = way
                print("return:")
                print(message)
                return message

                print(value)
            print("in Befehl")

            way =self.findwholeway()
              #  return self.doMove(self.findWay())
            message=self.default_message
            message['Aktion']="move"
            message['way']=way
            print("return:")
            print(message)
            return message
        if message.get('Aktion') == "endwait":
            print("endwait on server")
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
        print(self.target)


        self.dif=[self.target[0]-self.position[0],self.target[1]-self.position[1]] #difference

        if self.dif == [0,0]:
            #self.target=[None,None]
            return True

        if self.testMove(self.getRight()):
            #print("in r : "+ str(self.testMove(self.orientation)))

            return "r"
        if self.testMove(self.getLeft()):
            #print("in l : "+ str(self.testMove(self.orientation)))

            return "l"
        if self.testMove(self.orientation):
            print("in s : "+ str(self.testMove(self.orientation)))
            return "s" ##straight
        if self.valid(self.getLeft()):
            return "l"
        if self.valid(self.getRight()):
            return "r"
        print("ERRRRRRRRRROR")
        return None

    def doMove(self,m):
        if m =="s":
            print("in s")
            self.position[0]=self.position[0]+self.orientation[0]
            self.position[1] = self.position[1] + self.orientation[1]
          #  message['mode']='way'
         #   message['way']='s'
           # message['Aktion']='move'
            return 's'
        if m =="r":
            print("in r")

            self.position[0] = self.position[0] + self.getRight()[0]
            self.position[1] = self.position[1] + self.getRight()[1]
            self.orientation = self.getRight()
          #  message['way']='r'
            #message['Aktion']='move'

            return 'r'

        if m =="l":
            print("in l")

            self.position[0] = self.position[0] + self.getLeft()[0]
            self.position[1] = self.position[1] + self.getLeft()[1]
            self.orientation=self.getLeft()
            #message['way']='l'
            #message['Aktion']='move'

            return 'l'




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
        print(self.position[0]+move[0])
        print(self.position[1]+move[1])
        if self.position[0]+move[0]>3  or self.position[0]+move[0]<0 or self.position[1]+move[1]>3  or self.position[1]+move[1]<0:
            return None
        return [self.position[0]+move[0],self.position[1]+move[1]]

    def testRight(self):
        self.testMove(self.getRight())

    def getRight(self):
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
    def getLeft(self):
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




    def findwholeway(self,scan=False):

        loop = False
        way=""
        i = 1
        while not loop:
            x = self.findWay()
            if x == True:
                break
            if x == None:
                break
            way=way+self.doMove(x)
            i=i+1 # i brauc ich nicht
            if scan:
                if self.Field_to_Table.lookUpTable(self.position) in self.neutrals:
                    print("dazwischen ist eins vorgekommen das scan amal")
                    break
            else:
                print(self.Field_to_Table.lookUpTable(self.position))
                print(self.neutrals)
        print("way would be:")
        print(way)
        print("resting pos:")
        print(self.position)
        print("rest or:")
        print(self.orientation)
        return way

    def print(self):
        print(self.Table[0][0]+" "+self.Table[0][1]," "+self.Table[0][2]+ " "+self.Table[0][3])
        print(self.Table[1][0]+" "+self.Table[1][1]," "+self.Table[1][2]+ " "+self.Table[1][3])
        print(self.Table[2][0]+" "+self.Table[2][1]," "+self.Table[2][2]+ " "+self.Table[2][3])
        print(self.Table[3][0]+" "+self.Table[3][1]," "+self.Table[3][2]+ " "+self.Table[3][3])

    def sendwait(self):
        print("in send wait")
        message = self.default_message
        message['Aktion'] = 'wait'
        self.aktion="waiting"
        self.nextaktion="UserInputFind"
        return message
    def sendprep(self):
        print("in prep no?")
        self.target==[0,0]
        self.aktion = "waitUser"
        self.nextaktion = "findUserInput"
        way=self.findwholeway()
        message = self.default_message
        message['Aktion'] = "move"
        message['way'] = way
        return message
    def handleScan(self):
        if not self.aktivescan:
           print("not here pls")
           self.neutrals= self.game.getNeutral()
           self.scanidx=0
           self.aktivescan=True
       # lookUpTable.L

        self.target=self.Field_to_Table.lookUpField(self.neutrals[self.scanidx])
     #   self.Table.
        print("target in handle scan:")
        print(self.target)
        way=self.findwholeway()
        message = self.default_message
        message['Aktion'] = "scan"
        message['way'] = way

        return message

    def makemove(self,value):
        print("in make move")
        move = self.game.getMove(int(value))
        if not self.game.game_on:
            if self.game.winner=="E":
                return self.sendprep()
            if self.game.winner==None:
                return self.sendprep()
            self.aktion=="sendPrep"


        self.target=self.Field_to_Table.lookUpField(move)
        way=self.findWay()
        message = self.default_message
        message['Aktion'] = "move"
        message['way'] = way
        print("return:")


