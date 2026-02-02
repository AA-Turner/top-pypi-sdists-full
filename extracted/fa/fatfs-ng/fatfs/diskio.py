"""
Disk I/O abstraction layer for FatFS.

This module provides disk interface classes for FatFS filesystem operations.
"""

from abc import ABC, abstractmethod
from typing import Optional


class Disk(ABC):
    """
    Abstract base class for disk devices.
    
    Subclasses must implement all abstract methods to provide
    disk I/O functionality for FatFS.
    """
    
    def __init__(self):
        """Initialize disk device."""
        pass
    
    @abstractmethod
    def ioctl_get_sector_count(self) -> int:
        """
        Get total number of sectors on the disk.
        
        Returns:
            int: Total sector count
        """
        raise NotImplementedError("Subclass must implement ioctl_get_sector_count()")
    
    @abstractmethod
    def ioctl_get_sector_size(self) -> int:
        """
        Get sector size in bytes.
        
        Returns:
            int: Sector size (typically 512 bytes)
        """
        raise NotImplementedError("Subclass must implement ioctl_get_sector_size()")
    
    @abstractmethod
    def ioctl_get_block_size(self) -> int:
        """
        Get erase block size in sectors.
        
        Returns:
            int: Block size in sectors
        """
        raise NotImplementedError("Subclass must implement ioctl_get_block_size()")
    
    def ioctl_sync(self) -> None:
        """
        Flush any cached write data to disk.
        
        Default implementation does nothing (no caching).
        """
        pass
    
    def ioctl_trim(self) -> None:
        """
        Inform device about unused sectors (TRIM/UNMAP).
        
        Default implementation does nothing.
        """
        pass
    
    @abstractmethod
    def read(self, sector: int, count: int) -> bytes:
        """
        Read data from disk.
        
        Args:
            sector: Starting sector number
            count: Number of bytes to read
            
        Returns:
            bytes: Data read from disk
            
        Raises:
            IOError: If read operation fails
        """
        raise NotImplementedError("Subclass must implement read()")
    
    @abstractmethod
    def write(self, sector: int, count: int, buff: bytes) -> None:
        """
        Write data to disk.
        
        Args:
            sector: Starting sector number
            count: Number of bytes to write
            buff: Data buffer to write
            
        Raises:
            IOError: If write operation fails
            ValueError: If buffer size doesn't match count
        """
        raise NotImplementedError("Subclass must implement write()")


class RamDisk(Disk):
    """
    RAM-based disk implementation for testing and in-memory filesystems.
    
    This class provides a disk interface backed by a bytearray in memory.
    Useful for testing and creating filesystem images.
    
    Example:
        >>> storage = bytearray(1024 * 1024)  # 1MB
        >>> disk = RamDisk(storage, sector_size=512)
        >>> # Use with FatFS Partition
    """
    
    def __init__(
        self, 
        storage: bytearray, 
        sector_size: int = 512, 
        block_size: int = 1, 
        sector_count: Optional[int] = None
    ):
        """
        Initialize RAM disk.
        
        Args:
            storage: Bytearray to use as storage backend
            sector_size: Size of each sector in bytes (default: 512)
            block_size: Erase block size in sectors (default: 1)
            sector_count: Total number of sectors (default: auto-calculate from storage size)
            
        Raises:
            ValueError: If storage size doesn't match sector_count * sector_size
        """
        super().__init__()
        self.storage = storage
        self.sector_size = sector_size
        self.block_size = block_size
        
        if sector_count is None:
            self.sector_count = len(storage) // sector_size
        else:
            self.sector_count = sector_count
        
        # Validate storage size
        expected_size = self.sector_count * sector_size
        if len(storage) != expected_size:
            raise ValueError(
                f"Storage size mismatch: got {len(storage)} bytes, "
                f"expected {expected_size} bytes "
                f"({self.sector_count} sectors × {sector_size} bytes/sector)"
            )
    
    def ioctl_get_sector_count(self) -> int:
        """Get total number of sectors."""
        return self.sector_count
    
    def ioctl_get_sector_size(self) -> int:
        """Get sector size in bytes."""
        return self.sector_size
    
    def ioctl_get_block_size(self) -> int:
        """Get erase block size in sectors."""
        return self.block_size
    
    def ioctl_sync(self) -> None:
        """Flush cached data (no-op for RAM disk)."""
        pass
    
    def ioctl_trim(self) -> None:
        """TRIM unused sectors (no-op for RAM disk)."""
        pass
    
    def read(self, sector: int, count: int) -> bytes:
        """
        Read data from RAM disk.
        
        Args:
            sector: Starting sector number
            count: Number of bytes to read
            
        Returns:
            bytes: Data read from storage
            
        Raises:
            ValueError: If read would exceed storage bounds
        """
        offset = sector * self.sector_size
        end = offset + count
        
        if end > len(self.storage):
            raise ValueError(
                f"Read would exceed storage bounds: "
                f"sector {sector}, count {count}, "
                f"offset {offset}, end {end}, "
                f"storage size {len(self.storage)}"
            )
        
        return bytes(self.storage[offset:end])
    
    def write(self, sector: int, count: int, buff: bytes) -> None:
        """
        Write data to RAM disk.
        
        Args:
            sector: Starting sector number
            count: Number of bytes to write
            buff: Data buffer to write
            
        Raises:
            ValueError: If buffer size doesn't match count or write would exceed bounds
        """
        if len(buff) != count:
            raise ValueError(
                f"Buffer size mismatch: got {len(buff)} bytes, expected {count} bytes"
            )
        
        offset = sector * self.sector_size
        end = offset + count
        
        if end > len(self.storage):
            raise ValueError(
                f"Write would exceed storage bounds: "
                f"sector {sector}, count {count}, "
                f"offset {offset}, end {end}, "
                f"storage size {len(self.storage)}"
            )
        
        self.storage[offset:end] = buff
    
    def __repr__(self) -> str:
        """String representation of RamDisk."""
        return (
            f"RamDisk(size={len(self.storage)} bytes, "
            f"sector_size={self.sector_size}, "
            f"sector_count={self.sector_count}, "
            f"block_size={self.block_size})"
        )
