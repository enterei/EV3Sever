import argparse
import json
import selectors
import socket
import types

from SystemHandler import SystemHandler
from TTT import TTT
parser = argparse.ArgumentParser(description="rosolve robo modes")



parser.add_argument('--ms',type=int,default=4500,help='ms!',required=False)
parser.add_argument('--cornerC ',type=int,default=1,help='cornerC !',required=False) #how often count dark value to stop
parser.add_argument('--cornervalue',type=int,default=54,help='cornervalue!',required=False) # how dark to stop at corner
#line following arguments
parser.add_argument('--kp',type=float,default=2,help='kp!',required=False)
parser.add_argument('--ki',type=float,default=0.001,help='ki!',required=False)
parser.add_argument('--kd',type=float,default=0.3,help='kd!',required=False)
parser.add_argument('--tlr',type=float,default=62,help='tlr!',required=False)
parser.add_argument('--wsp',type=int,default=78,help='wsp!',required=False)
parser.add_argument('--speed',type=int,default=7,help='speed!',required=False)

#turning arguments
parser.add_argument('--turnls',type=int,default=0,help='turnls!',required=False) #left speed
parser.add_argument('--turnrs',type=int,default=5,help='turnrs!',required=False)#right speed

parser.add_argument('--initial_rot',type=int,default=120,help='initial_rot!',required=False) #turn for this degrees
parser.add_argument('--adjust_rot',type=float,default=0,help='rot!',required=False)
parser.add_argument('--adjust_s',type=int,default=1,help='adjust_s!',required=False)
parser.add_argument('--initial_ls',type=float,default=7,help='initial_ls!',required=False)
parser.add_argument('--initial_rs',type=float,default=-3,help='initial_ls!',required=False)
#testing arguments
parser.add_argument('--edgetest',type=bool,default=False,help='edgetest!',required=False) #test edges
parser.add_argument('--back',type=bool,default=False,help='back!',required=False) # drive backwards
parser.add_argument('--way',type=str,help='way!',required=False) # way as string("s","l","r")
parser.add_argument('--rmode',type=str,help='rmode!',required=False)  #running mode
parser.add_argument('--cmode',type=int,default=1,help='cmode!',required=False)# color sensor mode
parser.add_argument('--time',type=int,default=10,help='time!',required=False) #follow line for ms seconds
parser.add_argument('--turn',type=bool,default=False,help='turn!',required=False)
parser.add_argument('--bscan',type=bool,default=False,help='bscan!',required=False) #testing
parser.add_argument('--port',type=str,default=65432,help='turn!',required=False)
parser.add_argument('--host',type=str,default='192.168.0.179',help='bscan!',required=False) #testing


messageOut=None
def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print('accepted connection from', addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)


def send(key, mask, message):
    sock = key.fileobj
    data = key.data
    data.out = message
    print("send")
    if mask & selectors.EVENT_WRITE:
        if message:
            print('echoing', repr(message), 'to', data.addr)
            if len(message)>1000:
                print("ITS OVER 1000")
                return False
            sent = sock.send(message)  # Should be ready to write
            message = data.outb[sent:]
            print("server out after send: " + repr(message))
def rec(key,mask):
    sock = key.fileobj
    data = key.data
    data.out = messageOut
    recv_data = None
    if mask & selectors.EVENT_READ:
        print("in read")
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            return recv_data
        else:
            print('closing connection to', data.addr)
            sel.unregister(sock)
            sock.close()

sel = selectors.DefaultSelector()
pargs = parser.parse_args()

defaultM={'speed':pargs.speed,'time':pargs.time,'ms':pargs.ms,
                          'edgemax':pargs.corner ,'bscan':pargs.bscan,'edgev':pargs.cornervalue,
                          'ki':pargs.ki,'kd':pargs.kd,'kp':pargs.kp,
                          'turn':pargs.turn,'lspeed':pargs.turnls,'rspeed':pargs.turnrs,'degrees':pargs.initial_rot,
                          'rot':pargs.adjust_rot,'target_light_intensity':pargs.tlr,'way':pargs.way,'back':pargs.back,
                            'wsp':pargs.wsp,'edgetest':pargs.edgetest,'ulspeed':pargs.initial_ls,'urspeed':pargs.initial_rs,'uspeed':pargs.adjust_s

                          }
# ...

MessageHandler=SystemHandler(defaultM)
host = pargs.host  # The server's hostname or IP address
port = pargs.port
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
lsock.listen()
print('listening on', (host, port))
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)
messageOut=None
while True:
    events = sel.select(timeout=None)
    for key, mask in events:
        if key.data is None:
            accept_wrapper(key.fileobj)
        else:
            res=rec(key,mask) #receive the data
            if res != None:
                messageOut=MessageHandler.handleMessage(res) # handle the message
            if messageOut !=None:
                messageOut=res_bytes = json.dumps(messageOut).encode('utf-8')
                MessageHandler.printPos()
                send(key, mask, messageOut)
                messageOut=None

