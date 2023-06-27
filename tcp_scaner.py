import argparse
import socket
import threading

HOST = "127.0.0.1"

def scan_tcp(port):
    try:
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.settimeout(1)
        tcp_socket.connect((HOST, port))
        print(f'TCP порт: {port}')
        tcp_socket.close()
    except:
        pass


def get_port():
    parser = argparse.ArgumentParser()
    parser.add_argument('--start_port', type=int, help='Начальный порт')
    parser.add_argument('--end_port', type=int, help='Конечный Порт')
    args = parser.parse_args()

    if args is not None:
        return args


def scan_udp(port):
    try:
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.settimeout(2)
        udp_socket.sendto(bytes("Hi", "utf-8"), (HOST, port))
        data, addr = udp_socket.recvfrom(1024)
        # если мы не получили ответ, значит порт открыт
        print(f'UDP порт: {port}')
        # закрываем сокет
        udp_socket.close()
    except socket.timeout:
        udp_socket.close()
    except ConnectionResetError:
        pass


if __name__ == '__main__':
    args = get_port()
    start = args.start_port
    end = args.end_port
    for i in range(start, end):
        t = threading.Thread(target=scan_tcp, kwargs={'port': i})
        t.start()

    for i in range(start, end):
        t = threading.Thread(target=scan_udp, kwargs={'port': i})
        t.start()
