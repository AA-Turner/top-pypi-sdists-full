import os
from functools import lru_cache

from arpakitlib.ar_json_db_util import BaseJSONDb
from project.core.settings import get_cached_settings


class JSONDb(BaseJSONDb):
    def __init__(self, dirpath: str):
        super().__init__()
        self.story_log = self.create_json_db_file(
            filepath=os.path.join(dirpath, "story_log.json"), use_memory=True, beautify_json=False
        )


def create_json_db() -> JSONDb | None:
    if get_cached_settings().json_db_dirpath is None:
        return None
    return JSONDb(
        dirpath=get_cached_settings().json_db_dirpath
    )


@lru_cache()
def get_cached_json_db() -> JSONDb:
    return JSONDb(
        dirpath=get_cached_settings().json_db_dirpath
    )
