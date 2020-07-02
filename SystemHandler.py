import lookUpTable
from GameHandler import GameHandler
import json

from TestHandler import TestHandler


class SystemHandler:


    Table = [['N', 'N', 'N', 'N'], ['N', 'N', 'N', 'N'], ['N', 'N', 'N', 'N'], ['N', 'N', 'N', 'N']] #Table loaded all neutral
    next_corner=[None,None]
    neutrals =[]
    neutral_idx=0
    active =None
    dif=None




    def __init__(self,defaultM):
        self.default_message=defaultM #default message that sends parameter for the roboter
        self.testHandler=TestHandler(defaultM)

        self.position = [0,0] #position of robot
        self.orientation=[1,0] #orientation of robot
        self.next_corner = [None, None]
        self.game = GameHandler(defaultM,kfirst="E")  # todo default message    Gamhehandler handles the gamelogic and the AI of the robot
        print("in constroktor")
        print(self.game.game_on)
        self.target=[3,0]
        self.aktivescan=False
        self.scanidx = 0
        self.Field_to_Table= lookUpTable.LookUpTable() # class to cast from an edge to a field and back


        if self.game.first =="E":
            print("human player starts")
            self.aktion="waitUser"
            self.nextaktion="findUserInput"




    def getEnemyMove(self): #for testing
        b = input('Choose a number: ')
        return b



    def handleMessage(self,message): #handle message
        message=json.loads(message.decode('utf-8'))  #decode the the message
        print("message:")
        print(message)


        if(message.get('Aktion')=="Test"): # for testing
            print("in test")
            return self.testHandler.handleMessage(message)





        if (message.get('Aktion') == "Befehl"): #determine in what state the server is to correctly respond
            print(self.game.game_on)

            if not self.game.game_on: #start new game
                self.game = GameHandler(self.default_message)



                if self.game.first == "E":
                    self.aktion = "waitUser"
                    self.nextaktion = "findUserInput"
            print("vor sennd prep")
            message = self.sendprep()
            message['gameEndSound'] = "True"
            return message

            if self.aktion=="waitUser": #send wait
                return self.sendwait()

            if self.aktion == "UserInputFind": #look for marked field
                if self.aktivescan:
                    if message.get('found'): #merked field was found
                        inputvalue =self.Field_to_Table.lookUpTable(self.position)

                        return self.endscan(inputvalue)
                    if self.scanidx >= len(self.neutrals): # walked through whole field and npthing found
                        x = input("where did you play?")
                        return self.endscan(x)
                    if self.position == self.Field_to_Table.lookUpField(self.neutrals[self.scanidx]): #nothing found on the current posiiton
                        print("ist das selbe erhöhen")
                        self.scanidx = self.scanidx + 1




                    return self.handleScan() #determine where to scan next









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



        if message.get('Aktion') == "endwait":
            print("endwait on server")
    def handleSystem(self,message):
        print("System message")


    def findWay(self): # find next field to go

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
            return "s" ##straight
        if self.valid(self.getLeft()):
            return "l"
        if self.valid(self.getRight()):
            return "r"
        print("ERRRRRRRRRROR")
        return None

    def doMove(self,m): #execute the move in self table AND add letter for way command to the path that will be send to roboter
        if m =="s":
            self.position[0]=self.position[0]+self.orientation[0]
            self.position[1] = self.position[1] + self.orientation[1]
            return 's'
        if m =="r":
            print("in r")

            self.position[0] = self.position[0] + self.getRight()[0]
            self.position[1] = self.position[1] + self.getRight()[1]
            self.orientation = self.getRight()
            return 'r'

        if m =="l":
            self.position[0] = self.position[0] + self.getLeft()[0]
            self.position[1] = self.position[1] + self.getLeft()[1]
            self.orientation=self.getLeft()
            return 'l'

    def testMove(self,testmove): # test the given move if its a improvement
        testmove = self.valid(testmove) #valid function checks if move is possible or out of bounds
        if testmove == None:
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
                return testmove # if move is a improvemnt return the move, else fasle
            return False

    def valid(self,move): # checks if given move is a valid move and not out of bounds
        if self.position[0]+move[0]>3  or self.position[0]+move[0]<0 or self.position[1]+move[1]>3  or self.position[1]+move[1]<0:
            return None
        return [self.position[0]+move[0],self.position[1]+move[1]]

    def testRight(self):
        self.testMove(self.getRight())

    def getRight(self): #return orientation after turning right
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
    def getLeft(self): #return orientation after turning left
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




    def findwholeway(self,scan=False): #finds the whole way from the given position to target & returns the way as string

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
            if scan: #if scanning the robot should scan the neutral points in between the given position and the target
                if self.Field_to_Table.lookUpTable(self.position) in self.neutrals:
                    self.neutrals.remove(self.Field_to_Table.lookUpTable(self.position))
                    break
        return way #return way as string


    def sendwait(self): #send a wait to the robot
        print("in send wait")
        message = self.default_message
        message['Aktion'] = 'wait'
        self.aktion="waiting"
        self.nextaktion="UserInputFind"
        return message
    def sendprep(self): #send a preperation to robot (not used)

        self.target==[0,0]
        self.aktion = "waitUser"
        self.nextaktion = "findUserInput"
        way=self.findwholeway()
        message = self.default_message
        message['Aktion'] = "move"
        message['way'] = way
        return message
    def handleScan(self): # handle the scan algorithm
        if not self.aktivescan:

           self.neutrals= self.game.getNeutral() #get array of neutral fields
           self.scanidx=0 #set index to 0
           self.aktivescan=True #set sacn to active

        self.target=self.Field_to_Table.lookUpField(self.neutrals[self.scanidx]) #target first field of the neutral array
        way=self.findwholeway(scan=True) #find the way
        message = self.default_message #build message
        message['Aktion'] = "scan"
        message['way'] = way

        return message


    def endscan(self,inputvalue): #ends the scan, get
        print(inputvalue) #check if value was correct
        x = input("yours?")
        if x == "":
            move = self.game.getMove(inputvalue)
        else:
            move = self.game.getMove(int(x))
        self.target = self.Field_to_Table.lookUpField(move)
        way = self.findwholeway()
        message = self.default_message
        message['Aktion'] = "move"
        message['way'] = way

        self.scanidx = 0
        self.aktivescan = False

        self.aktion = "sendprep"
        self.nextaktion = "sendprep"


        return message

    def printPos(self): # print position and orientation of robot
        print("position and orientation of robot")
        print(self.position)
        print(self.orientation)


