"""
ESP32 Wear Leveling Layer for FAT Filesystem Images

This module implements the ESP-IDF wear leveling layer structure following
the official wl_fatfsgen.py implementation from ESP-IDF.

Based on ESP-IDF components:
- https://github.com/espressif/esp-idf/blob/master/components/fatfs/wl_fatfsgen.py
- https://github.com/espressif/esp-idf/tree/master/components/wear_levelling

ESP-IDF WL Layout:
    [dummy sector] [FAT data] [state1] [state2] [config]
    
    - dummy sector: 1 sector (0xFF filled)
    - FAT data: N sectors (actual filesystem)
    - state1: 1 sector (WL_State structure)
    - state2: 1 sector (WL_State copy for redundancy)
    - config: 1 sector (WL_Config structure)
    
    Total overhead: 4 sectors

WL_State structure (64 bytes header + padding):
    - pos: uint32_t (4 bytes) - Current position
    - max_pos: uint32_t (4 bytes) - plain_fat_sectors + 1 (includes dummy)
    - move_count: uint32_t (4 bytes) - Move counter
    - access_count: uint32_t (4 bytes) - Access counter
    - max_count: uint32_t (4 bytes) - Update rate (typically 16)
    - block_size: uint32_t (4 bytes) - Sector size (4096)
    - version: uint32_t (4 bytes) - WL version (2)
    - device_id: uint32_t (4 bytes) - Random device ID
    - reserved: 28 bytes (0x00)
    - crc32: uint32_t (4 bytes) - CRC32 of first 60 bytes
    - padding: rest of sector filled with 0xFF

WL_Config structure (48 bytes header + padding):
    - start_addr: uint32_t (4 bytes) - Start address (0)
    - full_mem_size: uint32_t (4 bytes) - Full partition size
    - page_size: uint32_t (4 bytes) - Page size (= sector_size)
    - sector_size: uint32_t (4 bytes) - Sector size (4096)
    - updaterate: uint32_t (4 bytes) - Update rate (16)
    - wr_size: uint32_t (4 bytes) - Write size (16)
    - version: uint32_t (4 bytes) - Version (2)
    - temp_buff_size: uint32_t (4 bytes) - Temp buffer size (32)
    - crc32: uint32_t (4 bytes) - CRC32 of first 32 bytes
    - padding: 3x uint32_t (12 bytes) zeros for alignment
    - rest: filled with 0xFF to sector size

Example:
    >>> from fatfs import RamDisk, Partition, create_esp32_wl_image_v2
    >>> 
    >>> # Create FAT filesystem
    >>> partition_size = 1507328  # Total partition size
    >>> wl_overhead = 4 * 4096    # 4 sectors for WL
    >>> fat_size = partition_size - wl_overhead
    >>> 
    >>> storage = bytearray(fat_size)
    >>> disk = RamDisk(storage, sector_size=4096)
    >>> partition = Partition(disk)
    >>> partition.mkfs()
    >>> partition.mount()
    >>> # ... add files ...
    >>> partition.unmount()
    >>> 
    >>> # Wrap with wear leveling for ESP32 (ESP-IDF layout)
    >>> wl_image = create_esp32_wl_image_v2(storage, partition_size)
    >>> 
    >>> # Write to file
    >>> with open('fatfs.bin', 'wb') as f:
    >>>     f.write(wl_image)
"""

import struct
import zlib
import random
from typing import Optional, Tuple


class ESP32WearLeveling:
    """ESP32 Wear Leveling Layer following ESP-IDF wl_fatfsgen.py implementation
    
    This class implements the exact ESP-IDF wear leveling structure as used
    by wl_fatfsgen.py and the ESP32 Arduino FFat library.
    
    Attributes:
        sector_size: Size of each sector in bytes (default: 4096)
    """
    
    # Constants from ESP-IDF
    WL_VERSION = 2
    WL_STATE_HEADER_SIZE = 64  # Size of WL_State header
    WL_CONFIG_HEADER_SIZE = 48  # Size of WL_Config header
    WL_DUMMY_SECTORS_COUNT = 1
    WL_STATE_COPY_COUNT = 2
    WL_CFG_SECTORS_COUNT = 1
    UPDATE_RATE = 16  # Default update rate from ESP-IDF
    WR_SIZE = 16      # Default write size from ESP-IDF
    TEMP_BUFF_SIZE = 32  # Default temp buffer size from ESP-IDF
    
    # Total WL overhead: 1 dummy + 2 states + 1 config = 4 sectors
    WL_TOTAL_SECTORS = WL_DUMMY_SECTORS_COUNT + WL_STATE_COPY_COUNT + WL_CFG_SECTORS_COUNT
    
    DEFAULT_SECTOR_SIZE = 4096
    
    def __init__(self, sector_size: int = DEFAULT_SECTOR_SIZE):
        """
        Initialize ESP32 Wear Leveling Layer
        
        Args:
            sector_size: Size of each sector in bytes (default: 4096)
        """
        self.sector_size = sector_size
        
    def create_wl_state(self, pos: int = 0, max_pos: int = 0, 
                       move_count: int = 0, access_count: int = 0,
                       max_count: int = UPDATE_RATE, device_id: Optional[int] = None) -> bytes:
        """
        Create a WL_State structure following ESP-IDF format
        
        Args:
            pos: Current position (default: 0)
            max_pos: plain_fat_sectors + WL_DUMMY_SECTORS_COUNT
            move_count: Move counter (default: 0)
            access_count: Access counter (default: 0)
            max_count: Update rate (default: 16)
            device_id: Device ID (default: random)
            
        Returns:
            bytes: WL_State structure (64 bytes header + CRC)
        """
        if device_id is None:
            device_id = random.randint(0, 0xFFFFFFFF)
        
        # Pack WL_State structure (60 bytes before CRC)
        # 8 uint32_t fields + 28 bytes reserved = 60 bytes
        state_data = struct.pack('<IIIIIIII',
            pos,                    # pos (4 bytes)
            max_pos,                # max_pos (4 bytes) 
            move_count,             # move_count (4 bytes)
            access_count,           # access_count (4 bytes)
            max_count,              # max_count (4 bytes)
            self.sector_size,       # block_size (4 bytes)
            self.WL_VERSION,        # version (4 bytes)
            device_id               # device_id (4 bytes)
        )
        # Add 28 bytes reserved (0x00, not 0xFF as per ESP-IDF)
        state_data += b'\x00' * 28
        
        # Calculate CRC32 of the first 60 bytes
        crc = zlib.crc32(state_data) & 0xFFFFFFFF
        
        # Append CRC32 (4 bytes) to make 64 bytes total
        state_with_crc = state_data + struct.pack('<I', crc)
        
        return state_with_crc
    
    def create_wl_config(self, partition_size: int, device_id: Optional[int] = None) -> bytes:
        """
        Create a WL_Config structure following ESP-IDF format
        
        Args:
            partition_size: Total partition size in bytes
            device_id: Device ID (optional, not used in config but kept for consistency)
            
        Returns:
            bytes: WL_Config structure (48 bytes header)
        """
        # Pack WL_Config structure (32 bytes before CRC)
        config_data = struct.pack('<IIIIIIII',
            0,                      # start_addr (4 bytes)
            partition_size,         # full_mem_size (4 bytes)
            self.sector_size,       # page_size (4 bytes)
            self.sector_size,       # sector_size (4 bytes)
            self.UPDATE_RATE,       # updaterate (4 bytes)
            self.WR_SIZE,           # wr_size (4 bytes)
            self.WL_VERSION,        # version (4 bytes)
            self.TEMP_BUFF_SIZE     # temp_buff_size (4 bytes)
        )
        
        # Calculate CRC32 of the first 32 bytes
        crc = zlib.crc32(config_data) & 0xFFFFFFFF
        
        # Append CRC32 + 3 zeros for alignment (48 bytes total)
        config_with_crc = config_data + struct.pack('<IIII', crc, 0, 0, 0)
        
        return config_with_crc
    
    def wrap_fat_image_v2(self, fat_data: bytes, partition_size: int) -> bytes:
        """
        Wrap a FAT filesystem image with ESP-IDF wear leveling layout
        
        This follows the exact layout from ESP-IDF wl_fatfsgen.py:
        [dummy sector] [FAT data] [state1] [state2] [config]
        
        Args:
            fat_data: Raw FAT filesystem data (without WL overhead)
            partition_size: Total partition size in bytes (including WL overhead)
            
        Returns:
            bytes: Wear-leveling wrapped FAT image
            
        Raises:
            ValueError: If FAT data doesn't fit in partition
        """
        # Calculate sector counts
        total_sectors = partition_size // self.sector_size
        wl_overhead_sectors = self.WL_TOTAL_SECTORS  # 4 sectors
        plain_fat_sectors = total_sectors - wl_overhead_sectors
        
        # Validate FAT data size
        fat_data_size = len(fat_data)
        max_fat_size = plain_fat_sectors * self.sector_size
        
        if fat_data_size > max_fat_size:
            raise ValueError(
                f"FAT data ({fat_data_size} bytes) exceeds available space "
                f"({max_fat_size} bytes, {plain_fat_sectors} sectors)"
            )
        
        # Read total_sectors from FAT boot sector for validation
        if len(fat_data) >= 21:
            fat_total_sectors = struct.unpack('<H', fat_data[19:21])[0]
            if fat_total_sectors != plain_fat_sectors:
                print(f"Warning: FAT boot sector total_sectors ({fat_total_sectors}) "
                      f"!= calculated plain_fat_sectors ({plain_fat_sectors})")
        
        # ESP-IDF formula: max_pos = plain_fat_sectors + WL_DUMMY_SECTORS_COUNT
        max_pos = plain_fat_sectors + self.WL_DUMMY_SECTORS_COUNT
        
        # max_count is just UPDATE_RATE (not multiplied by sectors!)
        max_count = self.UPDATE_RATE
        
        # Generate random device ID
        device_id = random.randint(0, 0xFFFFFFFF)
        
        # Create WL state
        wl_state = self.create_wl_state(
            pos=0,
            max_pos=max_pos,
            move_count=0,
            access_count=0,
            max_count=max_count,
            device_id=device_id
        )
        
        # Create WL config
        wl_config = self.create_wl_config(partition_size, device_id)
        
        # Pad structures to full sectors
        wl_state_sector = wl_state + (b'\xFF' * (self.sector_size - len(wl_state)))
        wl_config_sector = wl_config + (b'\xFF' * (self.sector_size - len(wl_config)))
        
        # Build the wear-leveling image following ESP-IDF layout
        wl_image = bytearray(partition_size)
        
        # 1. Dummy sector at beginning (all 0xFF)
        wl_image[0:self.sector_size] = b'\xFF' * self.sector_size
        
        # 2. FAT data after dummy sector
        fat_start = self.sector_size
        wl_image[fat_start:fat_start + len(fat_data)] = fat_data
        
        # 3. Pad FAT data area with 0xFF
        fat_end = fat_start + (plain_fat_sectors * self.sector_size)
        if fat_start + len(fat_data) < fat_end:
            wl_image[fat_start + len(fat_data):fat_end] = b'\xFF' * (fat_end - fat_start - len(fat_data))
        
        # 4. State sectors at end (before config)
        # state1 at: partition_size - 3 * sector_size
        # state2 at: partition_size - 2 * sector_size
        addr_state1 = partition_size - 3 * self.sector_size
        addr_state2 = partition_size - 2 * self.sector_size
        wl_image[addr_state1:addr_state1 + self.sector_size] = wl_state_sector
        wl_image[addr_state2:addr_state2 + self.sector_size] = wl_state_sector
        
        # 5. Config sector at very end
        addr_config = partition_size - self.sector_size
        wl_image[addr_config:addr_config + self.sector_size] = wl_config_sector
        
        return bytes(wl_image)
    
    # Keep old method for backwards compatibility
    wrap_fat_image = wrap_fat_image_v2
    
    def wrap_fat_image(self, fat_data: bytes, partition_size: int) -> bytes:
        """
        Wrap a FAT filesystem image with wear leveling layer
        
        Args:
            fat_data: Raw FAT filesystem data
            partition_size: Total partition size in bytes
            
        Returns:
            bytes: Wear-leveling wrapped FAT image
            
        Raises:
            ValueError: If FAT data doesn't fit in partition
        """
        # Calculate sector counts
        total_sectors = partition_size // self.sector_size
        
        # WL structure (based on ESP-IDF actual implementation):
        # - State sector 1 (at beginning)
        # - State sector 2 (at beginning + 1)
        # - FAT data sectors
        # - Temp sector (for wear leveling operations)
        # - State sector 1 copy (near end)
        # - State sector 2 copy (at end)
        # 
        # ESP-IDF reserves 1 additional sector (likely for alignment or safety)
        # Total overhead: 2 + 1 + 2 + 1 = 6 sectors
        
        # Calculate available sectors for FAT data
        wl_overhead_sectors = (self.wl_state_size * 2) + self.wl_temp_size + 1  # +1 for ESP-IDF reserved
        fat_sectors = total_sectors - wl_overhead_sectors
        
        # Ensure FAT data fits
        fat_data_size = len(fat_data)
        required_fat_sectors = (fat_data_size + self.sector_size - 1) // self.sector_size
        
        if required_fat_sectors > fat_sectors:
            raise ValueError(
                f"FAT data ({fat_data_size} bytes, {required_fat_sectors} sectors) "
                f"does not fit in partition ({partition_size} bytes, {fat_sectors} available sectors)"
            )
        
        # Calculate max_pos (number of sectors that can be moved)
        max_pos = fat_sectors
        
        # Calculate max_count (when to trigger wear leveling)
        max_count = self.update_rate * fat_sectors
        
        # Create WL state
        wl_state = self.create_wl_state(
            pos=0,
            max_pos=max_pos,
            move_count=0,
            access_count=0,
            max_count=max_count,
            device_id=0
        )
        
        # Pad WL state to full sector
        wl_state_sector = wl_state + (b'\xFF' * (self.sector_size - len(wl_state)))
        
        # Build the wear-leveling image
        wl_image = bytearray()
        
        # 1. Add first state sector copy (sector 0)
        wl_image.extend(wl_state_sector)
        
        # 2. Add second state sector copy (sector 1)
        wl_image.extend(wl_state_sector)
        
        # 3. Add FAT data
        wl_image.extend(fat_data)
        
        # 4. Pad FAT data to sector boundary
        fat_padding = (fat_sectors * self.sector_size) - len(fat_data)
        wl_image.extend(b'\xFF' * fat_padding)
        
        # 5. Add temp sector (erased)
        wl_image.extend(b'\xFF' * (self.wl_temp_size * self.sector_size))
        
        # 6. Add state sector copies at end (for redundancy)
        wl_image.extend(wl_state_sector)  # State copy 1
        wl_image.extend(wl_state_sector)  # State copy 2
        
        # Verify final size
        if len(wl_image) != partition_size:
            # Pad or trim to exact partition size
            if len(wl_image) < partition_size:
                wl_image.extend(b'\xFF' * (partition_size - len(wl_image)))
            else:
                wl_image = wl_image[:partition_size]
        
        return bytes(wl_image)
    
    def verify_wl_state(self, state_data: bytes) -> bool:
        """
        Verify a WL_State structure's CRC32
        
        Args:
            state_data: 48-byte WL_State structure
            
        Returns:
            bool: True if CRC is valid, False otherwise
        """
        if len(state_data) != self.WL_STATE_SIZE:
            return False
        
        # Extract CRC from end
        stored_crc = struct.unpack('<I', state_data[-4:])[0]
        
        # Calculate CRC of data without CRC field
        calculated_crc = zlib.crc32(state_data[:-4]) & 0xFFFFFFFF
        
        return stored_crc == calculated_crc
    
    def extract_fat_from_wl(self, wl_data: bytes) -> Optional[bytes]:
        """
        Extract FAT filesystem data from wear-leveling wrapped image
        
        Args:
            wl_data: Wear-leveling wrapped image
            
        Returns:
            bytes: Raw FAT filesystem data, or None if invalid
        """
        if len(wl_data) < (self.wl_state_size * 2 + 1) * self.sector_size:
            return None
        
        # Verify first state sector
        first_state = wl_data[:self.WL_STATE_SIZE]
        if not self.verify_wl_state(first_state):
            return None
        
        # Extract FAT data (skip state sectors at beginning)
        fat_start = self.wl_state_size * self.sector_size
        
        # Calculate FAT data size (exclude temp and state sectors at end)
        total_sectors = len(wl_data) // self.sector_size
        wl_overhead_sectors = (self.wl_state_size * 2) + self.wl_temp_size
        fat_sectors = total_sectors - wl_overhead_sectors
        fat_size = fat_sectors * self.sector_size
        
        fat_data = wl_data[fat_start:fat_start + fat_size]
        
        return fat_data
    
    def calculate_overhead(self, partition_size: int) -> Tuple[int, int, int]:
        """
        Calculate wear leveling overhead for a given partition size
        
        Args:
            partition_size: Total partition size in bytes
            
        Returns:
            Tuple of (total_sectors, wl_overhead_sectors, fat_sectors)
        """
        total_sectors = partition_size // self.sector_size
        # Total WL overhead based on ESP-IDF actual implementation:
        # - 2 state sectors at start
        # - 1 temp sector
        # - 2 state sectors at end
        # - 1 reserved sector (ESP-IDF specific)
        # Total: 6 sectors
        wl_overhead_sectors = (self.wl_state_size * 2) + self.wl_temp_size + 1
        fat_sectors = total_sectors - wl_overhead_sectors
        
        return (total_sectors, wl_overhead_sectors, fat_sectors)


def create_esp32_wl_image(fat_data: bytes, partition_size: int, 
                          sector_size: int = 4096) -> bytes:
    """
    Create a wear-leveling wrapped FAT image for ESP32 following ESP-IDF layout
    
    This function follows the exact ESP-IDF wl_fatfsgen.py implementation:
    Layout: [dummy sector] [FAT data] [state1] [state2] [config]
    
    Args:
        fat_data: Raw FAT filesystem data (without WL overhead)
        partition_size: Total partition size in bytes (including WL overhead)
        sector_size: Sector size in bytes (default: 4096)
        
    Returns:
        bytes: Wear-leveling wrapped FAT image ready for ESP32
        
    Example:
        >>> from fatfs import RamDisk, Partition, create_esp32_wl_image
        >>> 
        >>> # Calculate sizes
        >>> partition_size = 1507328  # Total partition
        >>> wl_overhead = 4 * 4096    # 4 sectors for WL
        >>> fat_size = partition_size - wl_overhead
        >>> 
        >>> # Create FAT filesystem
        >>> storage = bytearray(fat_size)
        >>> disk = RamDisk(storage, sector_size=4096, sector_count=fat_size//4096)
        >>> partition = Partition(disk)
        >>> partition.mkfs()
        >>> partition.mount()
        >>> # ... add files ...
        >>> partition.unmount()
        >>> 
        >>> # Wrap with WL
        >>> wl_image = create_esp32_wl_image(storage, partition_size)
        >>> with open('fatfs.bin', 'wb') as f:
        >>>     f.write(wl_image)
    """
    wl = ESP32WearLeveling(sector_size=sector_size)
    return wl.wrap_fat_image_v2(fat_data, partition_size)


# Alias for backwards compatibility
create_esp32_wl_image_v2 = create_esp32_wl_image


def extract_fat_from_esp32_wl(wl_data: bytes, sector_size: int = 4096) -> Optional[bytes]:
    """
    Extract FAT data from ESP32 wear-leveling image (ESP-IDF layout)
    
    Args:
        wl_data: Wear-leveling wrapped image
        sector_size: Sector size in bytes (default: 4096)
        
    Returns:
        bytes: Raw FAT filesystem data, or None if invalid
        
    Example:
        >>> from fatfs import extract_fat_from_esp32_wl
        >>> with open('fatfs.bin', 'rb') as f:
        >>>     wl_image = f.read()
        >>> fat_data = extract_fat_from_esp32_wl(wl_image)
        >>> if fat_data:
        >>>     # Mount and read FAT data
        >>>     pass
    """
    # Check if first sector is dummy (all 0xFF)
    if len(wl_data) < sector_size:
        return None
    
    first_sector = wl_data[:sector_size]
    if not all(b == 0xFF for b in first_sector):
        return None
    
    # Calculate FAT data size
    total_sectors = len(wl_data) // sector_size
    wl_overhead = ESP32WearLeveling.WL_TOTAL_SECTORS  # 4 sectors
    fat_sectors = total_sectors - wl_overhead
    
    # Extract FAT data (skip dummy sector)
    fat_start = sector_size
    fat_size = fat_sectors * sector_size
    fat_data = wl_data[fat_start:fat_start + fat_size]
    
    return fat_data


def is_esp32_wl_image(data: bytes, sector_size: int = 4096) -> bool:
    """
    Check if data is an ESP32 wear-leveling wrapped image (ESP-IDF layout)
    
    Args:
        data: Image data to check
        sector_size: Sector size in bytes (default: 4096)
        
    Returns:
        bool: True if data appears to be a WL-wrapped image
        
    Example:
        >>> from fatfs import is_esp32_wl_image
        >>> with open('fatfs.bin', 'rb') as f:
        >>>     data = f.read()
        >>> if is_esp32_wl_image(data):
        >>>     print("This is a wear-leveling wrapped image")
    """
    if len(data) < sector_size * 4:  # Need at least 4 sectors
        return False
    
    # Check if first sector is dummy (all 0xFF)
    first_sector = data[:sector_size]
    if not all(b == 0xFF for b in first_sector):
        return False
    
    # Check if second sector looks like FAT boot sector
    second_sector = data[sector_size:sector_size + 512]
    # FAT boot sector starts with jump instruction (EB xx 90 or E9 xx xx)
    if len(second_sector) < 3:
        return False
    if second_sector[0] not in (0xEB, 0xE9):
        return False
    
    # Check boot signature at offset 510-511
    if second_sector[510:512] != b'\x55\xAA':
        return False
    
    return True


def calculate_esp32_wl_overhead(partition_size: int, sector_size: int = 4096) -> dict:
    """
    Calculate wear leveling overhead for ESP32 (ESP-IDF layout)
    
    Args:
        partition_size: Total partition size in bytes
        sector_size: Sector size in bytes (default: 4096)
        
    Returns:
        dict: Dictionary with overhead information
        
    Example:
        >>> from fatfs import calculate_esp32_wl_overhead
        >>> info = calculate_esp32_wl_overhead(1507328)
        >>> print(f"FAT data size: {info['fat_size']} bytes")
        >>> print(f"WL overhead: {info['wl_overhead_size']} bytes")
        >>> print(f"Layout: {info['layout']}")
    """
    total_sectors = partition_size // sector_size
    wl_overhead_sectors = ESP32WearLeveling.WL_TOTAL_SECTORS  # 4 sectors
    fat_sectors = total_sectors - wl_overhead_sectors
    
    return {
        'partition_size': partition_size,
        'sector_size': sector_size,
        'total_sectors': total_sectors,
        'wl_overhead_sectors': wl_overhead_sectors,
        'wl_overhead_size': wl_overhead_sectors * sector_size,
        'fat_sectors': fat_sectors,
        'fat_size': fat_sectors * sector_size,
        'layout': f'[dummy:{sector_size}] [FAT:{fat_sectors * sector_size}] [state1:{sector_size}] [state2:{sector_size}] [config:{sector_size}]',
        'layout_description': 'ESP-IDF wl_fatfsgen.py compatible layout'
    }
