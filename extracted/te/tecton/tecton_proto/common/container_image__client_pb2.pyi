from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ContainerImage(_message.Message):
    __slots__ = ["image_digest", "image_tag", "image_uri", "repository_name"]
    IMAGE_DIGEST_FIELD_NUMBER: _ClassVar[int]
    IMAGE_TAG_FIELD_NUMBER: _ClassVar[int]
    IMAGE_URI_FIELD_NUMBER: _ClassVar[int]
    REPOSITORY_NAME_FIELD_NUMBER: _ClassVar[int]
    image_digest: str
    image_tag: str
    image_uri: str
    repository_name: str
    def __init__(self, repository_name: _Optional[str] = ..., image_uri: _Optional[str] = ..., image_digest: _Optional[str] = ..., image_tag: _Optional[str] = ...) -> None: ...
