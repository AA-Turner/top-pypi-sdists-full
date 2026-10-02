from .auth import AuthResource
from .searches import SearchesResource
from .collections import CollectionsResource
from .indexes import IndexesResource
from .admin import AdminResource
from .gdrive import GDriveResource
from .sql import SqlResource
from .images import ImagesResource
from .r2 import R2Resource

__all__ = [
    "AuthResource",
    "SearchesResource",
    "CollectionsResource",
    "IndexesResource",
    "AdminResource",
    "GDriveResource",
    "SqlResource",
    "ImagesResource",
    "R2Resource",
]
