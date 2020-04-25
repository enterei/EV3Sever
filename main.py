import socket
from tutorial1 import collect_data

def server():
   # host = socket.gethostname()  # get local machine name
    host = "192.168.0.179"
    print(host)
    port = 8060  # Make sure it's within the > 1024 $$ <65535 range

    s = socket.socket()
    s.bind((host, port))

    s.listen(1)
    client_socket, adress = s.accept()
    print("Connection from: " + str(adress))
    while True:
        c, addr = s.accept()  # Establish a connection with the client
        print ("Got connection from", addr)
        c.send("Thank you for connecting!")
        c.close()
    c.close()


if __name__ == '__main__':
    #server()
    collect_data()