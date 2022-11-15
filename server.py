import socket
from identifier import log

IP = '172.20.10.3'
# IP = '192.168.0.32'
# IP = '172.30.1.9'
PORT = 6000
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024
PATH = "./fridge_python2/static/points.txt"
PATH2 = "./fridge_python2/static/points_re.txt"

def set_file():
    file = open(PATH2, 'a')
    for i in range(6):
        file.write("\n")
    file.close()
    print('cleared')

def sk_server():

    i = 0
    print("[SERVER] starting")

    # socket - bind - listen - accept
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"{i}. [SERVER] listening")

    # accept and waiting
    conn, addr = server.accept() 
    
    while True:
 
        print(f"{i}. [SERVER] {addr} connected")
        print(f'{i}. [SERVER] waiting...')

        file = open(PATH, 'a')
        data = conn.recv(SIZE).decode(FORMAT)
        print(f'{i}. [SERVER] writing txt...')
        file.write(data)

        conn.send(f' [SERVER] received, END, {i}'.encode(FORMAT))
        file.close()
        print(f'{i}. [SERVER] END')

        data = data.split()

        n_items, current_items, in_and_out, exp, fifo, in_cnt = log(data, i) 

        n_items = ' '.join(map(str, n_items))
        in_cnt = ' '.join(map(str, in_cnt))
        print(n_items)
        print(current_items)
        print(in_and_out)
        print(exp)
        print(fifo)
        print(in_cnt)


        re_file = open(PATH2, 'a', encoding="UTF-8")
        re_file.write(n_items)
        re_file.write('\n')
        re_file.write(current_items + "\n")
        re_file.write(in_and_out + "\n")
        re_file.write(exp + "\n")
        re_file.write(fifo + "\n")
        re_file.write(in_cnt)
        re_file.write('\n')
        # re_file.write(fifo)
        re_file.close()

        i += 1

if __name__ == "__main__":
    set_file()
    sk_server()