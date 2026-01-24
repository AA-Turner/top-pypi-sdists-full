from ..imports import *
def normalize_video_id(video_id) -> str:
    if video_id is None:
        raise ValueError("video_id cannot be None")
    return str(video_id)
