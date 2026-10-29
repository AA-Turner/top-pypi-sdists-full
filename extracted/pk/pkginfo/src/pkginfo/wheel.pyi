from .distribution import Distribution as Distribution, parse as parse

class Wheel(Distribution):
    filename: str
    metadata_version: str | None
    python_tag: str | None
    abi_tag: str | None
    platform_tag: str | None
    build_tag: str | None
    purelib: bool | None
    def __init__(self, filename: str, metadata_version: str | None = ...) -> None: ...
    def read(self) -> bytes: ...
