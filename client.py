import socket
from dopclient import *


class Client:
    def __init__(self):
        self.port = 65432
        self.host = 'localhost'
        self.sock = None

    def __get_connection(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))
        return sock

    def send_command(self, message):
        if not self.sock:
            self.sock = self.__get_connection()

        self.sock.sendall(message.encode())

        try:
            string_buff = b''
            while data := self.sock.recv(1024):
                string_buff += data

            if message.startswith("GET_FILE"):
                with open('downloaded_file.json', 'wb') as f:
                    f.write(string_buff)
                print('File downloaded')

            else:
                print(string_buff.decode())

        except:
            print('Invalid response from server')

    def close(self):
        self.sock.close()
        self.sock = None

    def main(self):
        while True:
            u_command = input('Введите команду на отправку на сервер:\n\n'
                              '(0) exit\n>>')

            if u_command == 'exit':
                break

            if u_command == 'var_2_1':
                self.sock = self.__get_connection()
                numbers_list = []
                while True:
                    user_input = input("Введите число или пустую строку для завершения: ")
                    if not user_input:
                        break
                    number = int(user_input)
                    numbers_list.append(int(number))
                self.sock.send('var_2_1'.encode())
                send_data_to_program1(numbers_list, self.sock)
            elif u_command == 'var_2_2':
                self.sock = self.__get_connection()
                folder_name = input("Введите номер запуска программы(время создания директории): ")
                file_name = input("Введите номер дерева для получения(название файла): ")
                self.sock.send('var_2_2'.encode())
                file_data = request_file_from_program1(folder_name, file_name, self.sock)
                with open(file_name + ".json", 'w') as file:
                    json.dump(file_data, file, indent=4)
                print(file_data)

            else:
                self.send_command(u_command)

            self.close()

cl = Client()
cl.main()
