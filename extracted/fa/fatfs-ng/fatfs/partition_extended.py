"""
Extended Partition class with directory traversal support
This extends the basic Partition class with walk(), listdir(), and other features
"""

import os
from pathlib import Path
from typing import Iterator, Tuple, List, Optional


class PartitionExtended:
    """
    Extended Partition class with full directory traversal support.
    
    This class adds the following features to the basic Partition:
    - walk() - os.walk()-like directory traversal
    - listdir() - List directory contents
    - stat() - Get file/directory information
    - remove() - Delete files
    - rmdir() - Remove directories
    - rename() - Rename/move files
    - exists() - Check if path exists
    - isfile() / isdir() - Check path type
    """
    
    def __init__(self, partition):
        """
        Initialize extended partition wrapper.
        
        Args:
            partition: Basic Partition instance from wrapper
        """
        self._partition = partition
        self._mounted = False
    
    def __getattr__(self, name):
        """Delegate unknown attributes to wrapped partition"""
        return getattr(self._partition, name)
    
    def listdir(self, path: str = "/") -> List[str]:
        """
        List directory contents.
        
        Args:
            path: Directory path to list
            
        Returns:
            List of filenames in the directory
            
        Example:
            >>> files = partition.listdir("/")
            >>> print(files)
            ['file1.txt', 'dir1', 'file2.dat']
        """
        from fatfs.wrapper import DIR_Handle, FILINFO_Handle, pyf_opendir, pyf_readdir, pyf_closedir, PY_FR_OK as FR_OK
        
        entries = []
        dh = DIR_Handle()
        fh = FILINFO_Handle()
        
        adjusted_path = self._partition._adjust_path(path)
        
        ret = pyf_opendir(dh, adjusted_path)
        if ret != FR_OK:
            raise OSError(f"Failed to open directory: {path}")
        
        try:
            while True:
                ret = pyf_readdir(dh, fh)
                if ret != FR_OK:
                    break
                
                try:
                    name = fh.get_name()
                except (UnicodeDecodeError, UnicodeError):
                    # Skip entries with invalid UTF-8 (e.g., deleted entries with 0xFF)
                    continue
                
                if not name or name == '':
                    break
                
                # Skip . and ..
                if name in ('.', '..'):
                    continue
                
                # Skip entries that contain replacement characters (from invalid UTF-8)
                if '\ufffd' in name:
                    continue
                    
                entries.append(name)
        finally:
            pyf_closedir(dh)
        
        return entries
    
    def stat(self, path: str) -> dict:
        """
        Get file/directory information.
        
        Args:
            path: Path to file or directory
            
        Returns:
            Dictionary with file information:
            - size: File size in bytes
            - is_dir: True if directory
            - is_readonly: True if read-only
            - attr: Raw attribute byte
            
        Example:
            >>> info = partition.stat("/file.txt")
            >>> print(f"Size: {info['size']} bytes")
        """
        from fatfs.wrapper import FILINFO_Handle, pyf_stat, PY_FR_OK as FR_OK
        
        fh = FILINFO_Handle()
        adjusted_path = self._partition._adjust_path(path)
        
        ret = pyf_stat(adjusted_path, fh)
        if ret != FR_OK:
            raise FileNotFoundError(f"Path not found: {path}")
        
        return {
            'size': fh.get_size(),
            'is_dir': fh.is_directory(),
            'is_readonly': fh.is_readonly(),
            'attr': fh.get_attr()
        }
    
    def exists(self, path: str) -> bool:
        """
        Check if path exists.
        
        Args:
            path: Path to check
            
        Returns:
            True if path exists, False otherwise
        """
        try:
            self.stat(path)
            return True
        except FileNotFoundError:
            return False
    
    def isfile(self, path: str) -> bool:
        """
        Check if path is a file.
        
        Args:
            path: Path to check
            
        Returns:
            True if path is a file, False otherwise
        """
        try:
            info = self.stat(path)
            return not info['is_dir']
        except FileNotFoundError:
            return False
    
    def isdir(self, path: str) -> bool:
        """
        Check if path is a directory.
        
        Args:
            path: Path to check
            
        Returns:
            True if path is a directory, False otherwise
        """
        try:
            info = self.stat(path)
            return info['is_dir']
        except FileNotFoundError:
            return False
    
    def walk(self, top: str = "/") -> Iterator[Tuple[str, List[str], List[str]]]:
        """
        Directory tree generator, similar to os.walk().
        
        For each directory in the tree rooted at top (including top itself),
        yields a 3-tuple: (dirpath, dirnames, filenames)
        
        Args:
            top: Root directory to start walking from
            
        Yields:
            Tuple of (dirpath, dirnames, filenames)
            
        Example:
            >>> for root, dirs, files in partition.walk("/"):
            ...     print(f"Directory: {root}")
            ...     for file in files:
            ...         print(f"  File: {file}")
            ...     for dir in dirs:
            ...         print(f"  Dir: {dir}")
        """
        dirs = []
        files = []
        
        # List current directory
        try:
            entries = self.listdir(top)
        except OSError:
            return
        
        # Separate files and directories
        for entry in entries:
            entry_path = os.path.join(top, entry).replace('\\', '/')
            if self.isdir(entry_path):
                dirs.append(entry)
            else:
                files.append(entry)
        
        # Yield current directory
        yield top, dirs, files
        
        # Recursively walk subdirectories
        for dirname in dirs:
            new_path = os.path.join(top, dirname).replace('\\', '/')
            yield from self.walk(new_path)
    
    def remove(self, path: str) -> None:
        """
        Delete a file.
        
        Args:
            path: Path to file to delete
            
        Raises:
            OSError: If deletion fails
        """
        from fatfs.wrapper import pyf_unlink, PY_FR_OK as FR_OK
        
        adjusted_path = self._partition._adjust_path(path)
        ret = pyf_unlink(adjusted_path)
        
        if ret != FR_OK:
            raise OSError(f"Failed to delete file: {path}")
    
    def rmdir(self, path: str) -> None:
        """
        Remove an empty directory.
        
        Args:
            path: Path to directory to remove
            
        Raises:
            OSError: If removal fails
        """
        # In FatFS, f_unlink works for both files and directories
        self.remove(path)
    
    def rename(self, old_path: str, new_path: str) -> None:
        """
        Rename or move a file/directory.
        
        Args:
            old_path: Current path
            new_path: New path
            
        Raises:
            OSError: If rename fails
        """
        from fatfs.wrapper import pyf_rename, PY_FR_OK as FR_OK
        
        old_adjusted = self._partition._adjust_path(old_path)
        new_adjusted = self._partition._adjust_path(new_path)
        
        ret = pyf_rename(old_adjusted, new_adjusted)
        
        if ret != FR_OK:
            raise OSError(f"Failed to rename {old_path} to {new_path}")
    
    def makedirs(self, path: str, exist_ok: bool = False) -> None:
        """
        Create a directory and all parent directories.
        
        Args:
            path: Directory path to create
            exist_ok: If True, don't raise error if directory exists
            
        Raises:
            OSError: If creation fails
        """
        parts = path.strip('/').split('/')
        current = ""
        
        for part in parts:
            if not part:
                continue
            
            current = f"{current}/{part}"
            
            if self.exists(current):
                if not exist_ok and not self.isdir(current):
                    raise OSError(f"Path exists and is not a directory: {current}")
                continue
            
            try:
                self._partition.mkdir(current)
            except Exception as e:
                if not exist_ok:
                    raise OSError(f"Failed to create directory {current}: {e}")
    
    def read_file(self, path: str) -> bytes:
        """
        Read entire file contents.
        
        Args:
            path: Path to file
            
        Returns:
            File contents as bytes
        """
        from fatfs.wrapper import FIL_Handle, pyf_open, pyf_read, pyf_close, PY_FR_OK as FR_OK, PY_FA_READ as FA_READ
        
        fh = FIL_Handle()
        adjusted_path = self._partition._adjust_path(path)
        
        ret = pyf_open(fh, adjusted_path, FA_READ)
        if ret != FR_OK:
            raise FileNotFoundError(f"Failed to open file: {path}")
        
        try:
            # Get file size
            info = self.stat(path)
            size = info['size']
            
            # Read file
            ret, data = pyf_read(fh, size)
            if ret != FR_OK:
                raise OSError(f"Failed to read file: {path}")
            
            return data
        finally:
            pyf_close(fh)
    
    def write_file(self, path: str, data: bytes) -> None:
        """
        Write data to file (overwrites existing file).
        
        Args:
            path: Path to file
            data: Data to write
        """
        with self._partition.open(path, 'w') as f:
            f.write(data)
    
    def copy_tree_from(self, source_dir: Path, dest_path: str = "/") -> None:
        """
        Copy entire directory tree from host filesystem to FatFS.
        
        Args:
            source_dir: Source directory on host filesystem
            dest_path: Destination path in FatFS
        """
        source_dir = Path(source_dir)
        
        if not source_dir.exists():
            raise FileNotFoundError(f"Source directory not found: {source_dir}")
        
        for item in source_dir.rglob("*"):
            rel_path = item.relative_to(source_dir)
            fs_path = os.path.join(dest_path, str(rel_path)).replace('\\', '/')
            
            if item.is_dir():
                self.makedirs(fs_path, exist_ok=True)
            else:
                # Ensure parent directory exists
                parent = os.path.dirname(fs_path)
                if parent and parent != '/':
                    self.makedirs(parent, exist_ok=True)
                
                # Copy file
                self.write_file(fs_path, item.read_bytes())
    
    def copy_tree_to(self, source_path: str, dest_dir: Path) -> None:
        """
        Copy entire directory tree from FatFS to host filesystem.
        
        Args:
            source_path: Source path in FatFS
            dest_dir: Destination directory on host filesystem
        """
        dest_dir = Path(dest_dir)
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        for root, dirs, files in self.walk(source_path):
            # Calculate relative path
            if root == source_path:
                rel_root = ""
            else:
                rel_root = root[len(source_path):].lstrip('/')
            
            # Create directories
            for dirname in dirs:
                dir_path = dest_dir / rel_root / dirname
                dir_path.mkdir(parents=True, exist_ok=True)
            
            # Copy files
            for filename in files:
                src_file = os.path.join(root, filename).replace('\\', '/')
                dst_file = dest_dir / rel_root / filename
                
                data = self.read_file(src_file)
                dst_file.write_bytes(data)


def create_extended_partition(disk):
    """
    Create an extended partition with full directory traversal support.
    
    Args:
        disk: Disk instance (e.g., RamDisk)
        
    Returns:
        PartitionExtended instance
        
    Example:
        >>> from fatfs import RamDisk, create_extended_partition
        >>> storage = bytearray(1024 * 1024)  # 1MB
        >>> disk = RamDisk(storage, sector_size=512)
        >>> partition = create_extended_partition(disk)
        >>> partition.mkfs()
        >>> partition.mount()
        >>> 
        >>> # Now use extended features
        >>> partition.makedirs("/test/dir", exist_ok=True)
        >>> partition.write_file("/test/file.txt", b"Hello World")
        >>> 
        >>> for root, dirs, files in partition.walk("/"):
        ...     print(f"{root}: {files}")
    """
    from fatfs.wrapper import Partition
    
    basic_partition = Partition(disk)
    return PartitionExtended(basic_partition)
