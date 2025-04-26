import base64
import gzip


def gzip_b64_encode(payload: str) -> str:
    compressed_data = gzip.compress(payload.encode("utf-8"))
    b64_encoded_data = base64.b64encode(compressed_data)
    return b64_encoded_data.decode("utf-8")


def gzip_b64_decode(payload: str) -> str:
    compressed_data = base64.b64decode(payload.encode("utf-8"))
    decompressed_data = gzip.decompress(compressed_data)
    return decompressed_data.decode("utf-8")
