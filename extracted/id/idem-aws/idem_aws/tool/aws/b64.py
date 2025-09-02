import base64


def decode(hub, data: bytes) -> bytes:
    if not isinstance(data, bytes):
        data = str(data).encode("utf-8")
    decoded_data = base64.b64decode(data)
    return decoded_data


def encode(hub, data: bytes) -> str:
    if not isinstance(data, bytes):
        data = str(data).encode("utf-8")
    b64_data_bytes = base64.b64encode(data)
    b64_data_str = b64_data_bytes.decode("utf-8")
    return b64_data_str
