#!/usr/bin/env python3

import socket
import csv
from filecount import filecount
import json


def collect_data():
    HOST = '192.168.0.179'  # Standard loopback interface address (localhost)
    PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print(HOST)
        print(PORT)
        s.bind((HOST, PORT))
        s.listen()
        print('runnings')
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                # print("ga")
                data = conn.recv(1024)
                rd = []
                a_dict = json.loads(data)
                print(dict(a_dict))
                print("ga")
                print(a_dict.get('id'))
                if(a_dict.get('id')=="ecke"):
                    res={'zug':'vor'}
                    serialized_dict = json.dumps(res).encode("ascii")

                    conn.sendall(serialized_dict)
                    print("here")
               # for v in data:

                #    rd.append(int(v))

                #if not data
                   # print("ok jetzt hier")
                #if data:
#                    print(rd)

                    #  conn.sendall(rd)
                 #   data = []
