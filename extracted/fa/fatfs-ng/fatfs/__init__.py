from fatfs.wrapper import *
from fatfs.diskio import RamDisk

# Import extended features if available
try:
    from fatfs.partition_extended import PartitionExtended, create_extended_partition
    __all__ = ["wrapper", "diskio", "PartitionExtended", "create_extended_partition"]
except ImportError:
    __all__ = ["wrapper", "diskio"]

# Import ESP32 Wear Leveling support
try:
    from fatfs.esp32_wl import (
        ESP32WearLeveling,
        create_esp32_wl_image,
        extract_fat_from_esp32_wl,
        is_esp32_wl_image,
        calculate_esp32_wl_overhead
    )
    __all__.extend([
        "ESP32WearLeveling",
        "create_esp32_wl_image", 
        "extract_fat_from_esp32_wl",
        "is_esp32_wl_image",
        "calculate_esp32_wl_overhead"
    ])
except ImportError:
    pass

# Re-export constants with cleaner names (without PY_ prefix)
try:
    from fatfs.wrapper import (
        PY_FR_OK as FR_OK,
        PY_FR_DISK_ERR as FR_DISK_ERR,
        PY_FR_INT_ERR as FR_INT_ERR,
        PY_FR_NOT_READY as FR_NOT_READY,
        PY_FR_NO_FILE as FR_NO_FILE,
        PY_FR_NO_PATH as FR_NO_PATH,
        PY_FR_INVALID_NAME as FR_INVALID_NAME,
        PY_FR_DENIED as FR_DENIED,
        PY_FR_EXIST as FR_EXIST,
        PY_FR_INVALID_OBJECT as FR_INVALID_OBJECT,
        PY_FR_WRITE_PROTECTED as FR_WRITE_PROTECTED,
        PY_FR_INVALID_DRIVE as FR_INVALID_DRIVE,
        PY_FR_NOT_ENABLED as FR_NOT_ENABLED,
        PY_FR_NO_FILESYSTEM as FR_NO_FILESYSTEM,
        PY_FR_MKFS_ABORTED as FR_MKFS_ABORTED,
        PY_FR_TIMEOUT as FR_TIMEOUT,
        PY_FR_LOCKED as FR_LOCKED,
        PY_FR_NOT_ENOUGH_CORE as FR_NOT_ENOUGH_CORE,
        PY_FR_TOO_MANY_OPEN_FILES as FR_TOO_MANY_OPEN_FILES,
        PY_FR_INVALID_PARAMETER as FR_INVALID_PARAMETER,
        PY_FA_READ as FA_READ,
        PY_FA_WRITE as FA_WRITE,
        PY_FA_OPEN_EXISTING as FA_OPEN_EXISTING,
        PY_FA_CREATE_NEW as FA_CREATE_NEW,
        PY_FA_CREATE_ALWAYS as FA_CREATE_ALWAYS,
        PY_FA_OPEN_ALWAYS as FA_OPEN_ALWAYS,
        PY_FA_OPEN_APPEND as FA_OPEN_APPEND,
        PY_AM_DIR as AM_DIR,
        PY_AM_RDO as AM_RDO,
    )
except ImportError:
    # Constants not available (old compiled version)
    pass
