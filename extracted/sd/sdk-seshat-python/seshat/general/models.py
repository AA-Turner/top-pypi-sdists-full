from dataclasses import dataclass


@dataclass
class CodePackage:
    name: str
    version: str
    executor_image_tag: str
    files: dict[str, str]
    metadata: dict[str, str]
    hash: str
    binary_files: set[str] = None

    def __post_init__(self):
        if self.binary_files is None:
            self.binary_files = set()
