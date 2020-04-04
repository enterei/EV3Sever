#!/usr/bin/env python3

import socket
import csv
from filecount import filecount
def collect_data():
    filename = 'Sensor_data_'+ str(filecount())+'.csv'
    with open(filename, 'w', newline='') as csvfile:
        c = 0
        spamwriter = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow('NEW ROW')
        spamwriter.writerow('')
        spamwriter.writerow(['number', 'red', 'green','blue'])


        HOST = '192.168.0.94'  # Standard loopback interface address (localhost)
        PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            print('running')
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    #print("ga")
                    data = conn.recv(1024)
                    rd = []
                    for v in data:

                        rd.append(int(v))


                    if not data:
                        print("ok jetzt hier")
                    if data:
                        print(rd)
                        spamwriter.writerow('')
                        spamwriter.writerow(v for v in rd)
                      #  conn.sendall(rd)
                        data =[]