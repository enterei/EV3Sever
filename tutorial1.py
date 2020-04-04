#!/usr/bin/env python3

import socket
import csv
from filecount import filecount
def collect_data():
    filename = 'Sensor_data_'+ str(filecount())+'.csv'
    with open(filename, 'w', newline='') as csvfile:

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
                    data = conn.recv(1024)
                    print(data)
                    spamwriter.writerow(int(v) for v in data.split())
                    if not data:
                        break
                    conn.sendall(data)