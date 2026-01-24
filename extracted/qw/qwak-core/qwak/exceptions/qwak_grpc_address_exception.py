from typing import Union
from urllib.parse import ParseResult

from qwak.exceptions import QwakException


class QwakGrpcAddressException(QwakException):
    def __init__(self, details: str, grpc_address: Union[str, ParseResult]):
        self.message = f"Not a valid gRPC address: '{grpc_address}'. Details: {details}"
