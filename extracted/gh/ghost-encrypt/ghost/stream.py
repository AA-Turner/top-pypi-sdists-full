# stream.py

try:
    from .encryption import *
except ImportError:
    from encryption import *
import socket
from threading import Thread
import os


class Stream_Host:
    def __init__(self, ip: str, port: int, key=None):
        if platform.system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")
        if key is None:
            key = Key()
        self.encryptor = Encryptor(key, silent=True)
        self.decrypter = Decrypter(key, silent=True)
        self.ip = ip
        self.port = port
        self.header = 64
        self.format = "utf-8"
        self.session = []
        self.server = socket.socket(socket.AF_INET6, socket.SOCK_STREAM) if ip.find(":") >= 0 \
            else socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((ip, port))
        msg = ("Server", f"Server started on {self.ip if self.ip.find(':') < 0 else '[' + self.ip + ']'}:{self.port} "
                         f"with key '{self.encryptor.key}'")
        self.session.append((msg[0], msg[1], datetime.now().strftime("%H:%M:%S")))
        log(msg[0], msg[1])
        self.conn, self.addr = None, None

    def send(self, msg: bytes):
        msg_len = str(len(msg)).encode(self.format)
        msg_len += b" " * (self.header - len(msg_len))
        self.conn.send(msg_len)
        self.conn.send(msg)

    def receive(self):
        while True:
            msg_len = self.conn.recv(self.header)
            if msg_len:
                if platform.system() == "Windows":
                    os.system("cls")
                else:
                    os.system("clear")
                msg = self.decrypter.decrypt(self.conn.recv(int(msg_len)).decode(self.format))
                self.session.append((f"{self.addr[0] if self.addr[0].find(':') < 0 else '[' + self.addr[0] + ']'}:"
                                     f"{self.addr[1]}", msg, datetime.now().strftime("%H:%M:%S")))
                for i, j, t in self.session:
                    if len(i) != 0:
                        print(f"[{t} - {i}] {j}")
                    else:
                        print(f"> {j}")
                print(">", end=" ")
                Thread(target=self.read_input).start()

    def listen(self):
        self.server.listen()
        self.conn, self.addr = self.server.accept()
        log(f"{self.addr[0] if self.addr[0].find(':') < 0 else '[' + self.addr[0] + ']'}:{self.addr[1]}", "Connection established")
        self.session.append((f"{self.addr[0] if self.addr[0].find(':') < 0 else '[' + self.addr[0] + ']'}:"
                             f"{self.addr[1]}", "Connection established", datetime.now().strftime("%H:%M:%S")))
        Thread(target=self.receive).start()
        Thread(target=self.read_input).start()

    def read_input(self):
        inp = input("> ")
        self.session.append(("", inp, ""))
        self.send(self.encryptor.encrypt(inp)[1].encode(self.format))
        self.read_input()


class Stream_Client:
    def __init__(self, ip: str, port: int, key=None):
        if platform.system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")
        self.encryptor = Encryptor(key, silent=True)
        self.decrypter = Decrypter(key, silent=True)
        self.ip = ip
        self.port = port
        self.header = 64
        self.format = "utf-8"
        self.session = []
        self.server = socket.socket(socket.AF_INET6, socket.SOCK_STREAM) if ip.find(":") >= 0 \
            else socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send(self, msg: bytes):
        msg_len = str(len(msg)).encode(self.format)
        msg_len += b" " * (self.header - len(msg_len))
        self.server.send(msg_len)
        self.server.send(msg)

    def receive(self):
        while True:
            msg_len = self.server.recv(self.header)
            if msg_len:
                if platform.system() == "Windows":
                    os.system("cls")
                else:
                    os.system("clear")
                msg = self.decrypter.decrypt(self.server.recv(int(msg_len)).decode(self.format))
                self.session.append((f"{self.ip if self.ip.find(':') < 0 else '[' + self.ip + ']'}:{self.port}", msg,
                                     datetime.now().strftime("%H:%M:%S")))
                for i, j, t in self.session:
                    if len(i) != 0:
                        print(f"[{t} - {i}] {j}")
                    else:
                        print(f"> {j}")
                print(">", end=" ")
                Thread(target=self.read_input).start()

    def read_input(self):
        inp = input("> ")
        self.session.append(([], inp, []))
        self.send(self.encryptor.encrypt(inp)[1].encode(self.format))
        self.read_input()

    def connect(self):
        self.server.connect((self.ip, self.port))
        log(f"{self.ip if self.ip.find(':') < 0 else '[' + self.ip + ']'}:{self.port}", "Connection established")
        self.session.append((f"{self.ip if self.ip.find(':') < 0 else '[' + self.ip + ']'}:{self.port}",
                             "Connection established", datetime.now().strftime("%H:%M:%S")))
        Thread(target=self.receive).start()
        Thread(target=self.read_input).start()
