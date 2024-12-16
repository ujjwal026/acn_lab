//server
import socket
def start_server(host='localhost',port=12345):
    with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((host,port))
        print(f'running on {host} and {port}')
        while True:
            message,client_add=server_socket.recvfrom(1024)
           
            decoded_msg=message.decode();
            print(f'client address:{client_add} : meassage: {decoded_msg}')
            message_length=len(decoded_msg)
            response_message=decoded_msg.upper()
            response=f"Response:{response_message},length:{message_length}"
            server_socket.sendto(response.encode(),client_add)
if __name__=="__main__":
    start_server()
            
//client
import socket
def start_client(host='localhost',port=12345):
    with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as client_socket:
        while True:
            message=input("enter the message")
            if message.lower()=='exit':
                print("exiting..")
                break;
            client_socket.sendto(message.encode(),(host,port))
            print(f"sent message to {host} {port}")
            massage,server_add=client_socket.recvfrom(1024)
            print(f"received msg from {server_add} :{massage}")
if __name__=="__main__":
  start_client()
