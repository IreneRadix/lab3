import socket
from program import Program
from threading import Thread
import json
import os
import struct
from dopserver import *

prog = Program()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 65432))
s.listen(3)

def make_file():
  path_dirs = os.getenv('PATH').split(os.pathsep)
  data = {}

  for path_dir in path_dirs:
    for root, dirs, files in os.walk(path_dir):
      executables = [f for f in files if os.access(os.path.join(root, f), os.X_OK)]
      if executables:
        data[root] = executables

  with open('./program_data.json', 'w') as file:
    json.dump(data, file, indent=4)

  f = open('./program_data.json')
  resp = f.read()
  f.close()

  return resp.encode()

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

    if data.decode() == 'GET_JSON_FILE':
        client.sendall(make_file())

    if data.decode() in ('var_2_1', 'var_2_2'):
        folder_name = create_folder()
        data1 = client.recv(1024)
        data2 = client.recv(1024)

        if str(data1.decode()) == "json" or str(data1.decode()) == "xml":
            file_extension = str(data1.decode())
            numbers = struct.unpack(f'{len(data2) // 4}I', data2)

            for number in numbers:
                save_data(number, folder_name, file_extension)

            binary_tree_root = build_binary_tree(numbers)
            save_tree(binary_tree_root, folder_name)

        else:
            directory = str(data1.decode())
            all_directory = [filename for filename in os.listdir()]

            if directory in all_directory:
                file_name = str(data2.decode()) + ".json"

                if file_name in os.listdir(directory):
                    with open(os.path.join(folder_name, file_name), 'r') as file:
                        data = json.load(file)
                        string = json.dumps(data)
                        client.send(struct.pack(f'I{len(string)}s', len(string), string.encode()))
    client_socket.close()


while True:
    client_socket, address = s.accept()
    print("Connected by", address)
    Thread(target=handle_commands, args=(client_socket,)).start()

