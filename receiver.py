import socket
import sys
import re
from datetime import datetime
import logging

protocol = 'udp'
size = 1111
port = 9090
config_port = 9091
ip = '127.0.0.1'

def receive_config():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((ip, config_port))

    s.listen(1)
    conn, addr = s.accept()

    data = conn.recv(1024)

    data = data.decode('utf-8')

    global size, port, protocol

    size = int(re.search(r'(?<=size:)\d+', data).group())
    port = int(re.search(r'(?<=port:)\d+', data).group())
    protocol = re.search(r'(?<=protocol:)\w+', data).group()

    conn.send(b'OK')

    conn.close()
    s.shutdown(1)
    s.close()

def receive_udp(logger):
    print('Receiving UDP')

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((ip, port))

    running = True

    while(running):
        data, addr = s.recvfrom(size)
        recv_time = datetime.now()
        data = data.decode('utf-8')
        nr = re.search(r'(?<=nr:)\d+', data).group()
        send_time = datetime.strptime(re.search(r'(?<=\[).*(?=\])', data).group(), '%Y-%m-%d %H:%M:%S.%f')
        print(f'Received packet {nr} at {recv_time} latency {recv_time - send_time}')
        logger.error(f'Received packet {nr} at {recv_time} latency {recv_time - send_time}')
    
    s.close()

def receive_tcp(logger):
    print('Receiving TCP')

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip, port))
    s.listen(1)

    running = True

    conn, addr = s.accept()

    while(running):
        
        data = conn.recv(size)
        recv_time = datetime.now()

        data = data.decode('utf-8')
        nr = re.search(r'(?<=nr:)\d+', data).group()
        send_time = datetime.strptime(re.search(r'(?<=\[).*(?=\])', data).group(), '%Y-%m-%d %H:%M:%S.%f')
        print(f'Received packet {nr} at {recv_time} latency {recv_time - send_time}')
        #logger.error(f'Received packet {nr} at {recv_time} latency {recv_time - send_time}')
        logger.error(f'{recv_time - send_time}')
    
    conn.close()
        

def main():
    print('Starting receiver script')

    receive_config()

    logger = logging.getLogger()
    handler = logging.FileHandler(str(datetime.now()) + '.log')
    logger.addHandler(handler)

    if(protocol == 'udp'):
        receive_udp(logger)
    elif(protocol == 'tcp'):
        receive_tcp(logger)


if __name__ == '__main__':
    main()