import socket
import argparse


class EchoServer:
    def __init__(self):
        args = self._get_args()
        self.serve(args)

    @staticmethod
    def _get_args():
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-p", "--port", help="listen on this port", type=int, default=9999
        )
        return parser.parse_args()

    def serve(self, args):
        host = ''
        port = args.port
        infos = socket.getaddrinfo(host, port)
        (family, socktype, proto, canonname, sockaddr) = infos[0]
        s = socket.socket(family, socket.SOCK_DGRAM)
        s.settimeout(1)
        s.bind(('', args.port))
        while True:
            try:
                res, addr = s.recvfrom(1024)
                print(res, addr)
            except socket.timeout:
                pass
            except KeyboardInterrupt:
                break


class Sender:
    def __init__(self):
        self.args = self._get_args()
        self.send_message()

    def send_message(self):
        host, port = self.args.connect.split(':')
        infos = socket.getaddrinfo(host, port)
        (family, socktype, proto, canonname, sockaddr) = infos[0]
        self.sockaddr = sockaddr
        s = socket(family, socket.SOCK_DGRAM)
        s.connect(sockaddr)
        s.send(self.args.message)
        s.close()

    @staticmethod
    def _get_args():
        parser = argparse.ArgumentParser()
        parser.add_option(
            "-m", "--message", help="send this message", default="message!"
        )
        parser.add_option(
            '-c', '--connect', help="host:port to connect to", default="localhost:9999"
        )
        return parser.parse_args()

    def __repr__(self):
        return 'message sent to {sockaddr}'.format(**vars(self))
