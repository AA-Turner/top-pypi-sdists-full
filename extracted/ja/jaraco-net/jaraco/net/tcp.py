import socket
import argparse


def get_connect_options():
    parser = argparse.ArgumentParser(conflict_handler="resolve")
    parser.add_argument('-h', '--host', default='localhost')
    parser.add_argument('-p', '--port', default=80, type=int)
    args = parser.parse_args()
    return args


def test_connect():
    args = get_connect_options()
    addr = args.host, args.port
    family, socktype, proto, canonname, sockaddr = socket.getaddrinfo(*addr)[0]
    sock = socket.socket(family, socktype, proto)
    try:
        sock.connect(sockaddr)
    except OSError as e:
        print(e)
        raise SystemExit(1)
    print(f"Successfully connected to {args.host} on port {args.port}")


def start_echo_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 8099))
    s.listen(1)
    while True:
        conn, addr = s.accept()
        print('connected from', addr)
        while True:
            dat = conn.recv(4096)
            if not dat:
                break
            conn.send(dat)
