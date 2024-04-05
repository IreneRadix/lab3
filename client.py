
import socket
#from signal import signal, SIGPIPE, SIG_DFL
#signal(SIGPIPE,SIG_DFL)

sock = socket.socket()
sock.setblocking(1)
sock.connect(('localhost', 65432))

msg = input()
sock.send(msg.encode())

#file = open('./received_file.txt', 'w')
#data = sock.recv(1024)
while True:
    data = sock.recv(1024)

    if not data:
        break
    print(data.decode())
    #file.write(data.decode())

sock.close()

print(data.decode())
