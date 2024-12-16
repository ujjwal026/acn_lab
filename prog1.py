//server
import socket
import os
def start_server(host='localhost', port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server listening on {host}:{port}")
    while True:
        conn, addr = server_socket.accept()
        print(f"Connection from {addr}")
        filename = conn.recv(1024).decode()
        print(f"Requested file: {filename}")
        if os.path.isfile(filename):
            conn.send(b'EXISTS ' + str(os.path.getsize(filename)).encode())
            with open(filename, 'rb') as f:
                bytes_to_send = f.read(1024)
                while bytes_to_send:
                    conn.send(bytes_to_send)
                    bytes_to_send = f.read(1024)
                    print(f"Sent {filename} to {addr}")
        else:
            conn.send(b'ERR_FILE_NOT_FOUND')
            conn.close()
if __name__ == "__main__":
    start_server()

//client
import socket
def request_file(host='localhost', port=12345, filename=''):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    client_socket.send(filename.encode())
    response = client_socket.recv(1024).decode()
    if response.startswith('EXISTS'):
        file_size = int(response.split()[1])
        print(f"Receiving file: {filename} of size {file_size} bytes")
        with open('received_' + filename, 'wb') as f:
            bytes_received = 0
            while bytes_received < file_size:
                bytes_data = client_socket.recv(1024)
                f.write(bytes_data)
                bytes_received += len(bytes_data)
                print(f"File {filename} received successfully.")
    else:
        print("File not found on server.")
        client_socket.close()
if __name__ == "__main__":
    filename_to_request = input("Enter the filename to request: ")
    request_file(filename=filename_to_request)


