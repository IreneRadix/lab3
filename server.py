import socket
from program import Program
from threading import Thread

prog = Program()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 65432))
s.listen(3)


def handle_commands(client):
    data = client.recv(1024)
    if data.decode().startswith('var_1_ch_dir'):
        new_dir = data.decode().split('var_1_ch_dir', 1)[1].strip()
        prog.update_directory(new_dir)
        client.sendall(b'ok your changes accepted')

    if data.decode() == 'var_1_get_file':
        prog.save_file_info(prog.get_directory_data())
        file_data = prog.get_binary_file_info()
        client.sendall(file_data)
    client_socket.close()


while True:
    client_socket, address = s.accept()
    print("Connected by", address)
    Thread(target=handle_commands, args=(client_socket,)).start()

