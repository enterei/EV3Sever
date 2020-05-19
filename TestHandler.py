class TestHandler:
    move_message={'Aktion':"Bewegung"}
    def __init__(self,defaultM):
        self.default_message=defaultM



    def handleMessage(self,message):
        res =[{}]
        if message.get('Case')=="case1":
           res = self.straight()
        return res

    def straight(self):
        message= self.default_message
        message['Bewegung']='straight'
        message['way']='s'
        message.update(self.move_message)
        print(message)
        return message

    def getTestTarget(self):
        value = input("ecke x: ")
        print(value)
        target=[]
        target[0]=value
        value = input("ecke y: ")
        target[1] = value
        return target
