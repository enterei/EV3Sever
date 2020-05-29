import argparse
import json
import selectors
import socket
import types

from SystemHandler import SystemHandler
from TTT import TTT
parser = argparse.ArgumentParser(description="rosolve robo modes")
parser.add_argument('--rmode',type=str,help='rmode!',required=False)
parser.add_argument('--cmode',type=int,default=1,help='cmode!',required=False)
parser.add_argument('--speed',type=int,default=5,help='speed!',required=False)
parser.add_argument('--time',type=int,default=10,help='time!',required=False)
parser.add_argument('--ms',type=int,default=4500,help='ms!',required=False)
parser.add_argument('--edgemax',type=int,default=1,help='edgemax!',required=False)
parser.add_argument('--edgev',type=int,default=54,help='tagarget_light_intensity!',required=False)
parser.add_argument('--bscan',type=bool,default=False,help='bscan!',required=False)
#follow
parser.add_argument('--kp',type=float,default=2,help='kp!',required=False)
parser.add_argument('--ki',type=float,default=0.0,help='ki!',required=False)
parser.add_argument('--kd',type=float,default=0.3,help='kd!',required=False)
parser.add_argument('--tlr',type=float,default=62,help='tlr!',required=False)
parser.add_argument('--wsp',type=int,default=78,help='wsp!',required=False)

#### turnsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
parser.add_argument('--lspeed',type=int,default=0,help='rsped!',required=False)
parser.add_argument('--rspeed',type=int,default=5,help='lspeed!',required=False)
parser.add_argument('--turn',type=bool,default=False,help='turn!',required=False)
parser.add_argument('--degrees',type=int,default=120,help='deg!',required=False)
parser.add_argument('--rot',type=float,default=0,help='rot!',required=False)
parser.add_argument('--edgetest',type=bool,default=False,help='edgetest!',required=False)

parser.add_argument('--uspeed',type=int,default=1,help='deg!',required=False)
parser.add_argument('--ulspeed',type=float,default=7,help='rot!',required=False)
parser.add_argument('--urspeed',type=float,default=-3,help='rot!',required=False)


parser.add_argument('--back',type=bool,default=False,help='back!',required=False)

parser.add_argument('--way',type=str,help='way!',required=False)


message=None
def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print('accepted connection from', addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)
def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    data.out=message
    recv_data=None
    if mask & selectors.EVENT_READ:
        print("in read")
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            #data.outb += recv_data
            print(recv_data)
            print("here???")
        else:
            print('closing connection to', data.addr)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print('echoing', repr(data.outb), 'to', data.addr)
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]
            print("server out after send: "+data.out)
    return recv_data


def send(key, mask,mes):
    sock = key.fileobj
    data = key.data
    data.out = message
    print("send")

    if mask & selectors.EVENT_WRITE:
        if mes:
            print('echoing', repr(mes), 'to', data.addr)
            if len(mes)>1000:
                print("ITS OVER 1000")
                return False
            sent = sock.send(mes)  # Should be ready to write
            mes = data.outb[sent:]
            print("server out after send: " + repr(mes))
def rec(key,mask):
    sock = key.fileobj
    data = key.data
    data.out = message

    recv_data = None
    if mask & selectors.EVENT_READ:
        print("in read")
        recv_data = sock.recv(1024)  # Should be ready to read

       # print(recv_data)
        if recv_data:
            # data.outb += recv_data
            print("ga")
            print(recv_data)
            return recv_data
        else:
            print('closing connection to', data.addr)
            sel.unregister(sock)
            sock.close()

sel = selectors.DefaultSelector()
pargs = parser.parse_args()

defaultM={'speed':pargs.speed,'time':pargs.time,'ms':pargs.ms,
                          'edgemax':pargs.edgemax,'bscan':pargs.bscan,'edgev':pargs.edgev,
                          'ki':pargs.ki,'kd':pargs.kd,'kp':pargs.kp,
                          'turn':pargs.turn,'lspeed':pargs.lspeed,'rspeed':pargs.rspeed,'degrees':pargs.degrees,
                          'rot':pargs.rot,'target_light_intensity':pargs.tlr,'way':pargs.way,'back':pargs.back,
                            'wsp':pargs.wsp,'edgetest':pargs.edgetest,'ulspeed':pargs.ulspeed,'urspeed':pargs.urspeed,'uspeed':pargs.uspeed

                          }
# ...

message_handelr=SystemHandler(defaultM)
host = '192.168.0.179'  # The server's hostname or IP address
port = 65432
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
lsock.listen()
print('listening on', (host, port))
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)
TTT=TTT()
message=None
while True:
    events = sel.select(timeout=None)
    for key, mask in events:
        if key.data is None:
            accept_wrapper(key.fileobj)
        else:
            #print("in loop")
            #m= TTT.doSomething(service_connectionTTT.doSomething(res)(key, mask))
            res=rec(key,mask)
           # print(res)TTT.doSomething(res)

            if res != None:
                print(res)
                message=message_handelr.handleMessage(res)
                print(message)
            if message !=None:
                print("m!=NOne")
                message=res_bytes = json.dumps(message).encode('utf-8')
                send(key,mask,message)
                message=None

