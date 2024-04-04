import socket


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

            self.send_command(u_command)
            self.close()

cl = Client()
cl.main()
