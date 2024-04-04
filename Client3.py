import socket

def get_program_data():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 9090))
    data = b''
    while True:
        recv_data = client_socket.recv(1024)
        if not recv_data:
            break
        data += recv_data
    client_socket.close()
    return data

program_data = get_program_data()
print(program_data.decode('utf-8'))
