#!/usr/bin/python3
import select
import socket
import sys


def client(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    sock.connect((ip, port))
    sys.stdout.write(">>>")
    sys.stdout.flush()
    running = True
    while running:
        socket_list = [sys.stdin, sock]
        ready_to_read,ready_to_write,in_error = select.select(socket_list,[],[],0)

        for s in ready_to_read:
            if s == sock:
                response = str(sock.recv(1024), 'utf-8')
                if response:
                    sys.stdout.write(response)
                    sys.stdout.write(">>>")
                    sys.stdout.flush()
            else:
                message = s.readline()
                if message.strip('\n') == '/quit':
                    sock.shutdown(socket.SHUT_WR)
                    sock.close()
                    running = False
                    break
                else:
                    sock.sendall(bytes(message, 'utf-8'))
                    sys.stdout.write(">>>")
                    sys.stdout.flush()

if __name__ == "__main__":
    # client("camelotserver.ddns.net", 9009)
    client("localhost", 9009)
