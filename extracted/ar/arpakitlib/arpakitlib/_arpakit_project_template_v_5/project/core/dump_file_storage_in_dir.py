from functools import lru_cache

from arpakitlib.ar_file_storage_in_dir_util import FileStorageInDir
from project.core.settings import get_cached_settings


def create_dump_file_storage_in_dir() -> FileStorageInDir | None:
    if get_cached_settings().dump_dirpath is None:
        return None
    return FileStorageInDir(dirpath=get_cached_settings().dump_dirpath)


@lru_cache()
def get_cached_dump_file_storage_in_dir() -> FileStorageInDir | None:
    return create_dump_file_storage_in_dir()


def __example():
    print(get_cached_dump_file_storage_in_dir().dirpath)


if __name__ == '__main__':
    __example()
