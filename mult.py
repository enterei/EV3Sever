import argparse
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
parser.add_argument('--edgemax',type=int,default=2,help='edgemax!',required=False)
parser.add_argument('--edgev',type=int,default=21,help='tagarget_light_intensity!',required=False)
parser.add_argument('--bscan',type=bool,default=False,help='bscan!',required=False)
#follow
parser.add_argument('--kp',type=float,default=3,help='kp!',required=False)
parser.add_argument('--ki',type=float,default=0.05,help='ki!',required=False)
parser.add_argument('--kd',type=float,default=0.2,help='kd!',required=False)
parser.add_argument('--tlr',type=float,default=36,help='tlr!',required=False)
#### turn
parser.add_argument('--lspeed',type=int,default=20,help='rsped!',required=False)
parser.add_argument('--rspeed',type=int,default=-5,help='lspeed!',required=False)
parser.add_argument('--turn',type=bool,default=False,help='turn!',required=False)
parser.add_argument('--degrees',type=int,default=200,help='deg!',required=False)
parser.add_argument('--rot',type=float,default=1,help='rot!',required=False)


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
        print(recv_data)
        if recv_data:
            # data.outb += recv_data
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
                          'rot':pargs.rot,'target_light_intensity':pargs.tlr,'way':pargs.way,'back':pargs.back
                          }
# ...
message_handelr=SystemHandler(defaultM)
host = '192.168.0.179'  # The server's hostname or IP address
port = 65432
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print('listening on', (host, port))
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)
TTT=TTT()

while True:
    events = sel.select(timeout=None)
    for key, mask in events:
        if key.data is None:
            accept_wrapper(key.fileobj)
        else:
            #m= TTT.doSomething(service_connection(key, mask))
            res=rec(key,mask)
            print(res)
            message=message_handelr.handleMessage(res)
            if message !=None:
                print("m!=NOne")
                send(key,mask,message)
