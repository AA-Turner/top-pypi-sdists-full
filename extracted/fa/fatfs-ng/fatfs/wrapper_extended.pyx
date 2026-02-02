# Extended wrapper functions for directory traversal
# Add these to the existing wrapper.pyx file

from cpython.mem cimport PyMem_Malloc, PyMem_Free
from fatfs.ff cimport *

# Directory handle class
cdef class DIR_Handle:
    cdef DIR *dp
    def __cinit__(self):
        self.dp = <DIR*> PyMem_Malloc(sizeof(DIR))

    def __dealloc__(self):
        PyMem_Free(self.dp)

# File info handle class  
cdef class FILINFO_Handle:
    cdef FILINFO *fno
    def __cinit__(self):
        self.fno = <FILINFO*> PyMem_Malloc(sizeof(FILINFO))

    def __dealloc__(self):
        PyMem_Free(self.fno)
    
    def get_name(self):
        """Get filename from FILINFO structure"""
        # Assuming fname is a null-terminated string
        return (<bytes>self.fno.fname).decode('utf-8')
    
    def get_size(self):
        """Get file size"""
        return self.fno.fsize
    
    def get_attr(self):
        """Get file attributes"""
        return self.fno.fattrib
    
    def is_directory(self):
        """Check if entry is a directory"""
        return (self.fno.fattrib & AM_DIR) != 0
    
    def is_readonly(self):
        """Check if entry is read-only"""
        return (self.fno.fattrib & AM_RDO) != 0

# Python wrapper functions for directory operations
def pyf_opendir(DIR_Handle dh, const TCHAR* path) -> FRESULT:
    """Open a directory"""
    return f_opendir(dh.dp, path)

def pyf_closedir(DIR_Handle dh) -> FRESULT:
    """Close an open directory"""
    return f_closedir(dh.dp)

def pyf_readdir(DIR_Handle dh, FILINFO_Handle fh) -> FRESULT:
    """Read a directory item"""
    return f_readdir(dh.dp, fh.fno)

def pyf_stat(const TCHAR* path, FILINFO_Handle fh) -> FRESULT:
    """Get file status"""
    return f_stat(path, fh.fno)

def pyf_unlink(const TCHAR* path) -> FRESULT:
    """Delete an existing file or directory"""
    return f_unlink(path)

def pyf_rename(const TCHAR* path_old, const TCHAR* path_new) -> FRESULT:
    """Rename/Move a file or directory"""
    return f_rename(path_old, path_new)

def pyf_read(FIL_Handle fh, UINT size) -> tuple:
    """Read data from file"""
    cdef UINT bytes_read = 0
    cdef char* buffer = <char*> PyMem_Malloc(size)
    
    try:
        ret = f_read(fh.fp, buffer, size, &bytes_read)
        if ret != FR_OK:
            return (ret, b'')
        
        # Convert C buffer to Python bytes
        data = buffer[:bytes_read]
        return (ret, data)
    finally:
        PyMem_Free(buffer)

def pyf_lseek(FIL_Handle fh, FSIZE_t offset) -> FRESULT:
    """Move file pointer"""
    return f_lseek(fh.fp, offset)

def pyf_sync(FIL_Handle fh) -> FRESULT:
    """Flush cached data"""
    return f_sync(fh.fp)

def pyf_truncate(FIL_Handle fh) -> FRESULT:
    """Truncate file"""
    return f_truncate(fh.fp)
