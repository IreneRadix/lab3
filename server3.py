import os
import json
import socket

def get_program_info():
    path = os.environ.get('PATH')
    path_dirs = path.split(os.pathsep)
    tree = {}

    for dir in path_dirs:
        programs = []
        for filename in os.listdir(dir):
            file_path = os.path.join(dir, filename)
            if os.access(file_path, os.X_OK):
                programs.append(filename)
        tree[dir] = programs

    with open('program_info.json', 'w', encoding='utf-8') as json_file:
        json.dump(tree, json_file, indent=4)

def get_request(conn, addr):
    print(f'Получен запрос от {addr}')
    get_program_info()
    with open('program_info.json', 'rb') as json_file:
        data = json_file.read()
    conn.sendall(data)
    conn.close()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 9090))
server_socket.listen(1)

print('Сервер запущен. Ожидание подключения...')

while True:
    conn, addr = server_socket.accept()
    get_request(conn, addr)
