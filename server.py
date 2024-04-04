import socket
import json
from program import Program
from threading import Thread

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
    if data.decode().startswith('CH_DIR'):
        new_dir = data.decode().split('CH_DIR', 1)[1].strip()
        prog.update_directory(new_dir)
        client.sendall(b'ok your changes accepted')

    if data.decode() == 'GET_FILE':
        prog.save_file_info(prog.get_directory_data())
        file_data = prog.get_binary_file_info()
        client.sendall(file_data)
    client_socket.close()

    if data.decode() == 'GET_JSON_FILE':
        client.sendall(make_file())



while True:
    client_socket, address = s.accept()
    print("Connected by", address)
    Thread(target=handle_commands, args=(client_socket,)).start()
