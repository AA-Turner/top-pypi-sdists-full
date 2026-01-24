import pathlib
from typing import Union, List


def get_files(src_dir: Union[pathlib.Path, str], recurse: bool = True) -> List[pathlib.Path]:
    """
    Walks the given directory and collects files to be uploaded. If
    recurse option is False, only the files on the root of the directory
    will be returned.

    :param src_dir: location of files
    :param recurse: If false, only the files on the root of src_dir
                    are returned
    :return: file set to be used with upload_directory
    :rtype: set
    """
    src_dir = pathlib.Path(src_dir)
    if recurse:
        files = src_dir.rglob('*')
    else:
        files = src_dir.glob('*')

    return [f for f in files if f.is_file()]
