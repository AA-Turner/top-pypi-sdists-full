from enum import Enum


class CollaboratorRole(str, Enum):
    owner = "owner"
    editor = "editor"
    annotator = "annotator"
    viewer = "viewer"
