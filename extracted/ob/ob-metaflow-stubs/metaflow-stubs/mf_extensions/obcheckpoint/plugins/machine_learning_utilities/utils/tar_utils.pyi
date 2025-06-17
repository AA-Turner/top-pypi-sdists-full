######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:03.004709                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.exception

from ......exception import MetaflowException as MetaflowException

class TarballCreationError(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, message, error):
        ...
    ...

def warning_message(message, logger = None, ts = False, prefix = '[@checkpoint][tarball-creator]'):
    ...

def os_error_safe_file_adding(tar, file_path, arcname):
    ...

def create_tarball_in_memory(source_paths: typing.Union[str, typing.List[str]], compression_method = 'gz', strict = False):
    ...

def create_tarball_on_disk(source_path: str, output_filename = None, compression_method = 'gz', strict = False):
    """
    Create a tarball of the specified file or directory.
    
    Parameters:
    - source_path: The path to the file or directory to add to tarball.
    - output_filename: The path where the tarball should be saved.
    """
    ...

def extract_tarball(tarball_path_or_bytes, target_directory, compression_method = 'gz'):
    """
    Extract a tarball to the specified directory.
    
    Parameters:
    - tarball_path_or_bytes: The path to the tarball to be extracted or the bytes of the tarball.
    - target_directory: The directory where the contents of the tarball should be extracted.
    """
    ...

