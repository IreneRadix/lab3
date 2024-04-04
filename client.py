import socket


class Client:
    def __init__(self):
        self.port = int(input('input port number > '))
        self.host = input('input host > ')
        self.sock = None

    def __get_connection(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))
        return sock

    def main(self):
        self.sock = self.__get_connection()
        while True:
            mssg = input('input > ')
            if mssg == 'exit':
                self.sock.close()
                print('Connection refused')
                break
            self.sock.send(mssg.encode())

            data = self.sock.recv(1024)
            print(f"Recieved data from server - {data.decode()}")


client = Client()

client.main()