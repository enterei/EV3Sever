import json
class TTT:

    def __init__(self, **kwargs):
        print("init")
    def doSomething(self,message):
        if not message:
            message = json.loads(message.decode('utf-8'))
            if(message.get('Atktion')==None):
                print("none")
                return None
            if(message.get('Aktion')=="Ecke"):
                return json.dumps({'Aktion':"messen"}).encode('uft-8')
        else:
            return None