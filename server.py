from threading import Thread
import socket
import struct
from dopserver import *

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 65432))
s.listen(3)
folder_name = create_folder()

def handle_commands(client):
    data = client.recv(1024)
    if data.decode() in ('var_2_1', 'var_2_2'):
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
    client.close()


while True:
    client_socket, address = s.accept()
    print("Connected by", address)
    Thread(target=handle_commands, args=(client_socket,)).start()
