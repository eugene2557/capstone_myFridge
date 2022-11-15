from django.shortcuts import render
# from .models import api
# import socket
# from .identifier import log
# import time

# IP = '172.20.10.14'
# IP = '192.168.0.32'
# PORT = 6000
# ADDR = (IP, PORT)
# FORMAT = "utf-8"
# SIZE = 1024
# PATH = "./static/points.txt"
PATH2 = "./static/points_re.txt"
# server = None


# Create your views here.
def fridge(request):
    ci_lst = []
    iot_lst = []
    epff_lst = []
    re = open(PATH2, 'r', encoding='UTF8')
    lines = re.readlines()

    print(lines)

    for i in range(len(lines)):
        line = lines[i]

        if i % 5 == 0:
            line = list(map(int, line.split()))
            ci_lst.append(line)
        elif i % 5 == 2:
            if line == "\n":
                continue
            iot_lst.append(line)
        elif i % 5 == 3 or i % 5 == 4:
            if line == "\n":
                continue
            epff_lst.append(line)
    re.close()
    return render(request, 'fridge.html', {'ci' : ci_lst[-1], 'iot' : iot_lst, 'epff' : epff_lst})

# def sk_server(request):
#     global server
#     if server != None:
#         server.close()

#         time.sleep(5)
    
#     i = 0
#     print("[SERVER] starting")

#     # socket - bind - listen - accept
#     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server.bind(ADDR)   
#     server.listen()
#     print(f"{i}. [SERVER] listening")

#     # accept and waiting
#     conn, addr = server.accept() 

#     while True:
#         data = None
 
#         print(f"{i}. [SERVER] {addr} connected")
#         print(f'{i}. [SERVER] waiting...')

#         file = open(PATH, 'a')
#         data = conn.recv(SIZE).decode(FORMAT)
#         print(f'{i}. [SERVER] writing txt...')
#         file.write(data)

#         conn.send(f' [SERVER] received, END, {i}'.encode(FORMAT))
#         file.close()
#         print(f'{i}. [SERVER] END')

#         data = data.split()
#         print('* data')
#         print(data)
#         print('*')
#         ci, iot, ep, ff = log(data, i)
#         print(ci)
#         print(iot)
#         print(ep)
#         print(ff)
#         ap = api(current_items=ci, in_and_out=iot, exp=ep, fifo=ff)
#         ap.save()

#         i += 1

# def delete(request):
#     apis = api.objects.all()
#     apis.delete()
#     return render(request, 'delete.html')
    
           



