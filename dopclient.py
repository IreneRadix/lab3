import struct
import json

def send_data_to_program1(data, conn):
    format_choice = input("Выберите формат сохранения файлов (json/xml): ")
    if format_choice != "json" and format_choice != "xml":
        print("Выбран непправильный формат для файлов!")
        conn.close()
    conn.send(format_choice.encode())

    data_packed = struct.pack(f'{len(data)}I', *data)
    conn.sendall(data_packed)
    conn.close()

def request_file_from_program1(folder_name, file_name, conn):
    conn.sendall(folder_name.encode())
    conn.sendall(str(file_name).encode())
    res = conn.recv(1024)
    recv_size0, = struct.unpack('I', res[:struct.calcsize('I')])

    expected_max_string_size = 1024 - struct.calcsize('I')
    if recv_size0 < expected_max_string_size:
        current_extracting_size = recv_size0
    else:
        current_extracting_size = expected_max_string_size

    _, string_buff = struct.unpack(f'I{current_extracting_size}s', res)

    recv_size0 -= current_extracting_size
    expected_max_string_size = 1024

    while recv_size0 > 0:
        if recv_size0 < expected_max_string_size:
            current_extracting_size = recv_size0
        else:
            current_extracting_size = expected_max_string_size

        data = conn.recv(1024)
        string_buff += struct.unpack(f'{current_extracting_size}s', data)[0]

        recv_size0 -= current_extracting_size

    recv_string = string_buff.decode()
    json_res = json.loads(recv_string)
    return json_res
