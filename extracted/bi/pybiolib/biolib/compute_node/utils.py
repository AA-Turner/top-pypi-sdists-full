import random
import string

from biolib.biolib_logging import logger

BIOLIB_PROXY_NETWORK_NAME = 'biolib-proxy-network'


def get_package_type(package):
    package_type = int.from_bytes(package[1:2], 'big')
    if package_type == 1:
        return 'ModuleInput'
    elif package_type == 2:
        return 'ModuleOutput'  # Note: This package is deprecated
    elif package_type == 3:
        return 'ModuleSource'  # Note: This package is deprecated
    elif package_type == 4:
        return 'AttestationDocument'  # Note: This package is deprecated
    elif package_type == 5:
        return 'SavedJob'
    elif package_type == 6:
        return 'RsaEncryptedAesPackage'  # Note: This package is deprecated
    elif package_type == 7:
        return 'AesEncryptedPackage'  # Note: This package is deprecated
    elif package_type == 8:
        return 'SystemStatusUpdate'
    elif package_type == 9:
        return 'SystemException'
    elif package_type == 10:
        return 'StdoutAndStderr'

    else:
        raise Exception(f'Unexpected package type {package_type}')


class WorkerThreadException(Exception):
    def __init__(self, original_error, error_code, worker_thread):
        super().__init__()
        worker_thread.compute_state['status']['error_code'] = error_code
        logger.error(original_error)
        worker_thread.terminate()


def random_string(length):
    return ''.join(random.choices(string.ascii_letters, k=length))
