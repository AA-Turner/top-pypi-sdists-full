from enum import Enum

class FileType(str, Enum):
    Animation = "animation",
    Audio = "audio",
    Code = "code",
    Data = "data",
    Document = "document",
    Drawing = "drawing",
    Email = "email",
    Geometry = "geometry",
    Image = "image",
    Manifest = "manifest",
    Package = "package",
    Point_cloud = "point_cloud",
    Shape = "shape",
    Subtitles = "subtitles",
    Unknown = "unknown",
    Video = "video",

