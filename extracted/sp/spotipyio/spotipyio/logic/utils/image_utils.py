from base64 import b64encode


def read_image(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()


def encode_image_to_base64(image: bytes) -> str:
    encoded_image = b64encode(image)
    return encoded_image.decode("utf-8")
