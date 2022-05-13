import socket
import sys
import string
import random
from datetime import datetime
import time
import logging

protocol = 'udp'
size = 1024
port = 9090
config_port = 9091
ip = '127.0.0.1'
freq = 100
counter = 0
TIME_STRING_LENGTH = 26

def send_config(port, size, protocol):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, config_port))

    s.sendall(bytes(f'size:{size}, port:{port}, protocol:{protocol}<EOF>', 'utf-8'))

    data = s.recv(1024)

    print(data)

    s.shutdown(1)
    s.close()

    if(data == b'OK'):
        return True
    return False

    time.sleep(1)

def create_message(counter):
    HEADER = bytes(f'nr:{counter}:[', 'utf-8')
    EOF = bytes('<EOF>', 'utf-8')

    msg_size = size - (len(HEADER) + len(EOF) + TIME_STRING_LENGTH + 1)

    msg = ""
    for i in range(msg_size):
        msg += random.choice(string.ascii_letters)

    MESSAGE = HEADER + bytes(str(datetime.now()) + ']', 'utf-8') + bytes(msg, 'utf-8') + EOF

    return MESSAGE

def send_udp(logger):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    counter = 0

    #for i in range(16384):
    while True:
        msg = create_message(counter)
        s.sendto(msg, (ip, port))
        logger.error(msg)
        counter = counter + 1
        time.sleep(1/(freq+1))

def send_tcp(logger):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))

    counter = 0

    #for i in range(16384):
    while True:
        msg = create_message(counter)
        s.sendall(msg)
        logger.error(msg)
        counter = counter + 1
        time.sleep(1/(freq+1))

def main():
    print(f'Sending to {ip}:{port}')

    logger = logging.getLogger()
    handler = logging.FileHandler(str(datetime.now()) + '.log')
    logger.addHandler(handler)

    if send_config(port, size, protocol) == True:
        print('Successfully initiated server')
    else:
        print('Failed to initiate server')
        exit()

    running = True

    if(protocol == 'udp'):
        send_udp(logger)
    elif(protocol == 'tcp'):
        send_tcp(logger)

if __name__ == '__main__':
    main()
