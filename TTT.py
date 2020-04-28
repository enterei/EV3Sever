import json
class TTT:

    def __init__(self, **kwargs):
        print("init")
    def doSomething(self,message):
        if  message!= None:
            message = json.loads(message.decode('utf-8'))
            print("message in != null "+ message)
            if(message.get('Atktion')==None):
                print("in none weil aktion null")
                return None
            if(message.get('Aktion')=="Ecke"):
                print("sollten hier")
                return json.dumps({'Aktion':"messen"}).encode('uft-8')
        else:
            #print("message==null")
            return None
        print("kein if in dosomething")