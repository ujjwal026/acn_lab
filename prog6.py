//server
import struct

ICMP_ECHO_REQUEST = 8
ICMP_ECHO_REPLY = 0

def checksum(data):
    sum = 0
    for i in range(0, len(data), 2):
        word = (data[i] << 8) + (data[i + 1] if i + 1 < len(data) else 0)
        sum += word
        sum = (sum & 0xFFFF) + (sum >> 16)
    return ~sum & 0xFFFF

def create_icmp_reply_packet(data, identifier, sequence):
    packet = bytearray(8 + len(data))
    packet[0] = ICMP_ECHO_REPLY
    packet[1] = 0
    packet[2:4] = struct.pack('!H', 0)
    packet[4:6] = struct.pack('!H', identifier)
    packet[6:8] = struct.pack('!H', sequence)
    packet[8:] = data
    pkt_checksum = checksum(packet)
    packet[2:4] = struct.pack('!H', pkt_checksum)
    return packet

def icmp_server(host='0.0.0.0'):
    raw_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    raw_socket.bind((host, 7))
    while True:
        print("Waiting for ICMP Echo Request...")
        packet, addr = raw_socket.recvfrom(1024)
        icmp_header = packet[20:28]
        data = packet[28:]
        identifier, sequence = struct.unpack("!HH", icmp_header[4:8])
        print(f"Received from client ({addr}): {data.decode('utf-8', 'ignore')}")
        reply_packet = create_icmp_reply_packet(data, identifier, sequence)
        raw_socket.sendto(reply_packet, addr)

if __name__ == '__main__':
    icmp_server()
  #client
  import socket
import struct
import time

ICMP_ECHO_REQUEST = 8
ICMP_ECHO_REPLY = 0

def checksum(data):
    sum = 0
    for i in range(0, len(data), 2):
        word = (data[i] << 8) + (data[i + 1] if i + 1 < len(data) else 0)
        sum += word
        sum = (sum & 0xFFFF) + (sum >> 16)
    return ~sum & 0xFFFF

def create_icmp_request_packet(data):
    packet = bytearray(8 + len(data))
    packet[0] = ICMP_ECHO_REQUEST
    packet[1] = 0
    packet[2:4] = struct.pack('!H', 0)
    packet[4:6] = struct.pack('!H', 1)
    packet[6:8] = struct.pack('!H', 1)
    packet[8:] = data
    pkt_checksum = checksum(packet)
    packet[2:4] = struct.pack('!H', pkt_checksum)
    return packet

def icmp_client(host='localhost'):
    raw_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    raw_socket.settimeout(2)
    message = input("Enter the message to send: ").encode()
    packet = create_icmp_request_packet(message)
    raw_socket.sendto(packet, (host, 7))
    try:
        reply_packet, addr = raw_socket.recvfrom(1024)
        print(f"Raw reply data: {reply_packet}")
        reply_data = reply_packet[28:]
        try:
            print(f"Received from server: {reply_data.decode('utf-8')}")
        except UnicodeDecodeError:
            print("Received from server: (Non-UTF-8 data, unable to decode as text)")
    except socket.timeout:
        print("Request timed out. No reply received.")
    finally:
        raw_socket.close()

if __name__ == '__main__':
    icmp_client()
