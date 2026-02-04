from enum import Enum


class Modality(str, Enum):
    document = "document"
    image = "image"
    audio = "audio"
