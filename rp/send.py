import socket
import os.path

IP = '192.168.0.32'
# IP = '172.20.10.14'
# IP = '172.30.1.9'
PORT = 6000
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
PATH = './images/images2/labels'

# socket - connect
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
print('** [CLIENT] connected')


def sk_client(i, t):

    file = open(os.path.join(PATH, ('yolo' + str(i) + '.txt')), "r")
    data = file.read()
    # client.send(('yolo' + str(t) + '.txt').encode(FORMAT))
    # print('[CLIENT] sending filename...')

    client.send(data.encode(FORMAT))
    print('** [CLIENT] sending data...')
    
    file.close()

    msg = client.recv(SIZE).decode(FORMAT)
    print('** [SERVER] ' + msg)
    print('** [CLIENT] END')


if __name__ == "__main__":
    sk_client()