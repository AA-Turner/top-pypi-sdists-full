from enum import Enum

class MySQLConnectionMethod(str, Enum):
    AUTO = "auto"
    TCP = "tcp"
    SOCKET = "socket"