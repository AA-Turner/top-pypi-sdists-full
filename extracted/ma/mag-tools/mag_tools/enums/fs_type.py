from mag_tools.enums.base_enum import BaseEnum


class FsType(BaseEnum):
    """
    磁盘文件类型枚举类
    """
    NTFS = ("NTFS", "New Technology File System, commonly used in Windows.")
    FAT32 = ("FAT32", "File Allocation Table 32, an older file system used in Windows and other devices.")
    EXFAT = ("exFAT", "Extended File Allocation Table, optimized for flash drives.")
    EXT4 = ("EXT4", "Fourth Extended File System, commonly used in Linux.")
    HFS_PLUS = ("HFS+", "Hierarchical File System Plus, used in older macOS versions.")
    APFS = ("APFS", "Apple File System, used in newer macOS versions.")
    BTRFS = ("BTRFS", "B-tree File System, used in Linux for advanced features.")
    XFS = ("XFS", "High-performance journaling file system used in Linux.")
    ZFS = ("ZFS", "Zettabyte File System, known for high storage capacities and data integrity.")
