from enum import Enum

class VfsEntry_kind(str, Enum):
    Directory = "directory",
    Content = "content",

