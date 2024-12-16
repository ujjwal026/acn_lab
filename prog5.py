//server

import socket
import pickle 

class IPFragment:
    def __init__(self, identifier, offset, more_fragments, df_flag, data):
        self.identifier = identifier
        self.offset = offset
        self.more_fragments = more_fragments
        self.df_flag = df_flag  
        self.data = data

    def __repr__(self):
        return f"IPFragment(id={self.identifier}, offset={self.offset}, more={self.more_fragments}, DF={self.df_flag}, size={len(self.data)})"

def reassemble_packet(fragments):
    fragments_dict = {}
    for fragment in fragments:
        if fragment.identifier not in fragments_dict:
            fragments_dict[fragment.identifier] = []
        fragments_dict[fragment.identifier].append(fragment)

    reassembled_data = {}
    for identifier, fragments_list in fragments_dict.items():
        fragments_list.sort(key=lambda frag: frag.offset)
        reassembled_data[identifier] = b''.join([frag.data for frag in fragments_list])

    return reassembled_data

def start_server(host='localhost', port=5000):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    print(f"Server listening on {host}:{port}...")

    fragments = []
    try:
        while True:
            fragment_data, client_address = server_socket.recvfrom(2048)
            fragment = pickle.loads(fragment_data)  
            fragments.append(fragment)
            print(f"Received fragment: {fragment}")

            if fragment.more_fragments == 0:
                print("All fragments received, reassembling packet...")
                reassembled = reassemble_packet(fragments)
                for identifier, data in reassembled.items():
                    print(f"Reassembled packet with ID={identifier} (first 50 bytes): {data[:50]}")
                    break  
                break 
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()
//client

import socket
import pickle
import time

class IPFragment:
    def __init__(self, identifier, offset, more_fragments, df_flag, data):
        self.identifier = identifier
        self.offset = offset
        self.more_fragments = more_fragments
        self.df_flag = df_flag 
        self.data = data

    def __repr__(self):
        return f"IPFragment(id={self.identifier}, offset={self.offset}, more={self.more_fragments}, DF={self.df_flag}, size={len(self.data)})"

def fragment_packet(packet_data, identifier, mtu=1500, df_flag=0):
    fragments = []
    ip_header_size = 20
    max_data_size = mtu - ip_header_size 

    offset = 0
    while len(packet_data) > 0:
        fragment_data = packet_data[:max_data_size]
        packet_data = packet_data[max_data_size:]

        more_fragments = 1 if len(packet_data) > 0 else 0

        fragment = IPFragment(identifier, offset, more_fragments, df_flag, fragment_data)
        fragments.append(fragment)

        
        print(f"Created fragment: ID={fragment.identifier}, Offset={fragment.offset}, More Fragments={fragment.more_fragments}, DF={fragment.df_flag}, Size={len(fragment.data)} bytes")

        offset += len(fragment_data)

    return fragments

def start_client(host='localhost', port=5000, packet_identifier=12345, mtu=1500):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    original_packet_data = bytearray(b"This is an example of a large IP packet. " * 100)  

    fragments = fragment_packet(original_packet_data, packet_identifier, mtu)

    for fragment in fragments:
        fragment_data = pickle.dumps(fragment)  
        client_socket.sendto(fragment_data, (host, port))
        time.sleep(0.1)  

    client_socket.close()

if __name__ == "__main__":
    start_client()
