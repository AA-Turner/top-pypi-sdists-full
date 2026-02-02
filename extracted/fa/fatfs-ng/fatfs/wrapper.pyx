from fatfs.ff cimport *
from fatfs.diskio cimport *

#from pyfatfs.diskio import RamDisk

__diskio_wrapper_disks = {}

cdef public DSTATUS disk_initialize (BYTE pdrv):
    if pdrv in __diskio_wrapper_disks:
        return DSTATUS_Values.STA_OK
    else:
        return DSTATUS_Values.STA_NODISK

cdef public DSTATUS disk_status (BYTE pdrv):
    if pdrv in __diskio_wrapper_disks:
        return DSTATUS_Values.STA_OK
    else:
        return DSTATUS_Values.STA_NODISK

cdef public DRESULT disk_read (BYTE pdrv, BYTE* buff, DWORD sector, UINT count):
    if not pdrv in __diskio_wrapper_disks:
        return DRESULT.RES_NOTRDY
    drive = __diskio_wrapper_disks[pdrv]

    # Count is actually in number of sectors. Convert to bytes now.
    count *= drive.ioctl_get_sector_size()
    data = drive.read(sector, count)
    for i in range(count):
        buff[i] = data[i]
    # TODO: This doesn't work: buff[:count] = data
    return DRESULT.RES_OK

cdef public DRESULT disk_write (BYTE pdrv, const BYTE* buff, DWORD sector, UINT count):
    if not pdrv in __diskio_wrapper_disks:
        return DRESULT.RES_NOTRDY
    drive = __diskio_wrapper_disks[pdrv]

    # Count is actually in number of sectors. Convert to bytes now.
    count *= drive.ioctl_get_sector_size()
    drive.write(sector, count, buff[:count])
    return DRESULT.RES_OK

cdef public DRESULT disk_ioctl (BYTE pdrv, BYTE cmd, void* buff):
    if not pdrv in __diskio_wrapper_disks:
        return DRESULT.RES_NOTRDY
    drive = __diskio_wrapper_disks[pdrv]

    if cmd == IOCTL_Commands.CTRL_SYNC:
        drive.ioctl_sync()
    elif cmd == IOCTL_Commands.GET_SECTOR_COUNT:
        (<DWORD*> buff)[0] = drive.ioctl_get_sector_count()
    elif cmd == IOCTL_Commands.GET_SECTOR_SIZE:
        (<WORD*> buff)[0] = drive.ioctl_get_sector_size()
    elif cmd == IOCTL_Commands.GET_BLOCK_SIZE:
        (<DWORD*> buff)[0] = drive.ioctl_get_block_size()
    else:
        print("Unknown ioctl command %d." % cmd)
        return DRESULT.RES_ERROR

cdef extern int diskiocheck()

import datetime

cdef public DWORD get_fattime():
    t = datetime.datetime.now()
    return ((t.year - 1980) << 25) | (t.month << 21) | (t.day << 16) | (t.minute << 5) | int(t.second / 2)
    # Return Value
    # Currnet local time shall be returned as bit-fields packed into a DWORD value. The bit fields are as follows:
    # bit31:25
    #     Year origin from the 1980 (0..127, e.g. 37 for 2017)
    # bit24:21
    #     Month (1..12)
    # bit20:16
    #     Day of the month (1..31)
    # bit15:11
    #     Hour (0..23)
    # bit10:5
    #     Minute (0..59)
    # bit4:0
    #     Second / 2 (0..29, e.g. 25 for 50)



# TODO: Wrap or remove
# /* LFN support functions */
# #if FF_USE_LFN >= 1						/* Code conversion (defined in unicode.c) */
# WCHAR ff_oem2uni (WCHAR oem, WORD cp);	/* OEM code to Unicode conversion */
# WCHAR ff_uni2oem (DWORD uni, WORD cp);	/* Unicode to OEM code conversion */
# DWORD ff_wtoupper (DWORD uni);			/* Unicode upper-case conversion */
# #endif
# #if FF_USE_LFN == 3						/* Dynamic memory allocation */
# void* ff_memalloc (UINT msize);			/* Allocate memory block */
# void ff_memfree (void* mblock);			/* Free memory block */
# #endif
# 
# /* Sync functions */
# #if FF_FS_REENTRANT
# int ff_cre_syncobj (BYTE vol, FF_SYNC_t* sobj);	/* Create a sync object */
# int ff_req_grant (FF_SYNC_t sobj);		/* Lock sync object */
# void ff_rel_grant (FF_SYNC_t sobj);		/* Unlock sync object */
# int ff_del_syncobj (FF_SYNC_t sobj);	/* Delete a sync object */
# #endif

cdef class FIL_Handle:
    cdef FIL *fp
    def __cinit__(self):
        self.fp = <FIL*> PyMem_Malloc(sizeof(FIL))

    def __dealloc__(self):
        PyMem_Free(self.fp)

cdef class FATFS_Handle:
    cdef FATFS* fp
    def __cinit__(self):
        self.fp = <FATFS*> PyMem_Malloc(sizeof(FATFS))

    def __dealloc__(self):
        PyMem_Free(self.fp)


# Open or create a file
def pyf_open (FIL_Handle fph, const TCHAR* path, BYTE mode) -> FRESULT:
    return f_open(fph.fp, path, mode)

# Close an open file object
def pyf_close (FIL_Handle fph) -> FRESULT:
    return f_close(fph.fp)

# Read data from the file
#def pyf_read (FIL* fp, void* buff, UINT btr, UINT* br) -> FRESULT:
#    raise Exception("Not implemented.")
## Write data to the file
def pyf_write (FIL_Handle fph, data) -> FRESULT:
    assert isinstance(data, (bytes, bytearray))
    cdef UINT written
    cdef char* dataptr = data
    ret = f_write(fph.fp, <void*>dataptr, len(data), &written)
    if ret != FR_OK:
        raise FatFSException("write", ret, fph, data)
    assert((ret != FR_OK) or (written == len(data)), "FatFS::write succeeded, but written different %i bytes out of %i." % (written, len(data)))
    return ret, written
## Move file pointer of the file object
#def pyf_lseek (FIL* fp, FSIZE_t ofs) -> FRESULT:
#    raise Exception("Not implemented.")
## Truncate the file
#def pyf_truncate (FIL* fp) -> FRESULT:
#    raise Exception("Not implemented.")
## Flush cached data of the writing file
#def pyf_sync (FIL* fp) -> FRESULT:
#    raise Exception("Not implemented.")
## Open a directory
#def pyf_opendir (DIR* dp, const TCHAR* path) -> FRESULT:
#    raise Exception("Not implemented.")
## Close an open directory
#def pyf_closedir (DIR* dp) -> FRESULT:
#    raise Exception("Not implemented.")
## Read a directory item
#def pyf_readdir (DIR* dp, FILINFO* fno) -> FRESULT:
#    raise Exception("Not implemented.")
## Find first file
#def pyf_findfirst (DIR* dp, FILINFO* fno, const TCHAR* path, const TCHAR* pattern) -> FRESULT:
#    raise Exception("Not implemented.")
## Find next file
#def pyf_findnext (DIR* dp, FILINFO* fno) -> FRESULT:
#    raise Exception("Not implemented.")
## Create a sub directory
def pyf_mkdir (path) -> FRESULT:
    return f_mkdir(path)
## Delete an existing file or directory
#def pyf_unlink (const TCHAR* path) -> FRESULT:
#    raise Exception("Not implemented.")
## Rename/Move a file or directory
#def pyf_rename (const TCHAR* path_old, const TCHAR* path_new) -> FRESULT:
#    raise Exception("Not implemented.")
## Get file status
#def pyf_stat (const TCHAR* path, FILINFO* fno) -> FRESULT:
#    raise Exception("Not implemented.")
## Change attribute of a file/dir
#def pyf_chmod (const TCHAR* path, BYTE attr, BYTE mask) -> FRESULT:
#    raise Exception("Not implemented.")
## Change timestamp of a file/dir
#def pyf_utime (const TCHAR* path, const FILINFO* fno) -> FRESULT:
#    raise Exception("Not implemented.")
## Change current directory
#def pyf_chdir (const TCHAR* path) -> FRESULT:
#    raise Exception("Not implemented.")
## Change current drive
#def pyf_chdrive (const TCHAR* path) -> FRESULT:
#    raise Exception("Not implemented.")
## Get current directory
#def pyf_getcwd (TCHAR* buff, UINT len) -> FRESULT:
#    raise Exception("Not implemented.")
## Get number of free clusters on the drive
#def pyf_getfree (const TCHAR* path, DWORD* nclst, FATFS** fatfs) -> FRESULT:
#    raise Exception("Not implemented.")
## Get volume label
#def pyf_getlabel (const TCHAR* path, TCHAR* label, DWORD* vsn) -> FRESULT:
#    raise Exception("Not implemented.")
## Set volume label
#def pyf_setlabel (const TCHAR* label) -> FRESULT:
#    raise Exception("Not implemented.")
## Forward data to the stream
#def pyf_forward (FIL* fp, UINT(*func)(const BYTE*,UINT), UINT btf, UINT* bf) -> FRESULT:
#    raise Exception("Not implemented.")
## Allocate a contiguous block to the file
#def pyf_expand (FIL* fp, FSIZE_t fsz, BYTE opt) -> FRESULT:
#    raise Exception("Not implemented.")
# Mount/Unmount a logical drive
def pyf_mount (FATFS_Handle fph, const TCHAR* path, BYTE opt) -> FRESULT:
    return f_mount(fph.fp, path, opt)

# Create a FAT volume
def pyf_mkfs (path, n_fat = 1, align = 0, n_root = 0, au_size = 0, workarea_size = 512) -> FRESULT:
    """
    Create a new FAT filesystem on volum given in path. The optional parameters
    are passed to FATFS as is. Defaults will create filesystem with 1 FAT
    table, auto alignment probed from backing device, automatically choose
    number of rot entries and allocation unit size.
    """
    cdef char* buff = <char*> PyMem_Malloc(workarea_size)
    cdef MKFS_PARM opt
    opt.fmt = FM_FAT | FM_SFD
    opt.n_fat = n_fat # 1 copy of FAT table
    opt.align = align # auto align from lower layer
    opt.n_root = n_root # auto number of root FAT entries
    opt.au_size = au_size # auto
    cdef FRESULT ret = f_mkfs(path, &opt, buff, workarea_size)
    PyMem_Free(buff)
    return ret
## Divide a physical drive into some partitions
#def pyf_fdisk (BYTE pdrv, const LBA_t ptbl[], void* work) -> FRESULT:
#    raise Exception("Not implemented.")
## Set current code page
#def pyf_setcp (WORD cp) -> FRESULT:
#    raise Exception("Not implemented.")
## Put a character to the file
#def pyf_putc (TCHAR c, FIL* fp) -> int:
#    raise Exception("Not implemented.")
## Put a string to the file
#def pyf_puts (const TCHAR* str, FIL* cp) -> int:
#    raise Exception("Not implemented.")
## Put a formatted string to the file
#def pyf_printf (FIL* fp, const TCHAR* str, ...) -> int:
#    raise Exception("Not implemented.")
## Get a string from the file
#def pyf_gets (TCHAR* buff, int len, FIL* fp) -> str
#    raise Exception("Not implemented.")


from cpython.mem cimport PyMem_Malloc, PyMem_Realloc, PyMem_Free

def fresult_to_name(fresult):
    # TODO: Implement.
    return "UNKNOWN_%i" % fresult

class FatFSException(Exception):
    def __init__(self, function, ret, *args):
        self.code = ret
        args_str = ", ".join(map(str, args))
        ret_str = fresult_to_name(ret)
        Exception.__init__(self, "FatFS::%s(%s) failed with error code %i (%s)" % (function, args_str, ret, ret_str))
    pass

class FileHandle:
    def __init__(self):
        self.isopen = False
        self.fp = FIL_Handle()

    def close(self):
        ret = pyf_close(self.fp)
        if ret != FR_OK:
            raise FatFSException("FatFS::close failed with error code %s" % ret)
    def __enter__(self):
        return self

    def __exit__(self, except_type, except_value, except_traceback):
        self.close()

    def __dealloc__(self):
        if self.isopen:
            self.close()

    def write(self, data):
        if isinstance(data, str):
            data = bytes(data, 'ascii')
        ret, written = pyf_write(self.fp, data)
        if ret != FR_OK:
            raise FatFSException("FatFS::close failed with error code %s" % ret)
        return written

    def read(self, size = -1):
        pass


class Partition():
    def __init__(self, disk):
        self.fs = FATFS_Handle()
        self.disk = disk
        self.pname = None
        self.pdev = None

        # Find pdev and pname
        # TODO: Can we fetch the constant directly? Or define it here? Does it have to be 10 only?
        for i in range(10): # corresponds to FF_VOLUMES in ffconf.h
            if not i in __diskio_wrapper_disks:
                self.pdev = i
                self.pname = bytes("%d:" % i, 'ascii')
                __diskio_wrapper_disks[i] = disk
                break
        else:
            # All slots are full
            raise FatFSException("__init__", -1)
    def _adjust_path(self, path):
        """
        Adjusts path for use in pyf_ calls: adds partition prefix and converts to bytes.
        """
        return self.pname + bytes(path, 'ascii')

    def mount(self):
        ret = pyf_mount(self.fs, self.pname, 1)
        if ret == FR_OK:
            return True
        else:
            raise FatFSException("mount", ret, self.pname)

    def unmount(self):
        ret = f_mount(NULL, self.pname, 0)
        if ret == FR_OK:
            del __diskio_wrapper_disks[self.pdev]
            return True
        else:
            raise FatFSException("unmount", ret, self.pname)

    def mkfs(self):
        pyf_mkfs(self.pname)

    def mkdir(self, path):
        p = self._adjust_path(path)
        ret = pyf_mkdir(p)
        if ret != FR_OK:
            #raise FatFSException("FatFS::mkdir(%s) failed with error code %s" % (p, ret))
            raise FatFSException("mount", ret, p)

    def open(self, path, mode):
        # TODO: Implement mode.
        handle = FileHandle()
        p = self._adjust_path(path)
        ret = pyf_open(handle.fp, p, FA_WRITE | FA_CREATE_ALWAYS)
        if ret != FR_OK:
            raise FatFSException("open", ret, p)
        handle.isopen = True
        return handle

def check_diskio(drive):
    assert(not 0 in __diskio_wrapper_disks, "Check diskio must be used before mounting any real drives.")
    __diskio_wrapper_disks[0] = drive
    ret = diskiocheck()
    del __diskio_wrapper_disks[0]



# Extended wrapper functions for directory traversal and file operations

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
        # Use 'replace' error handler to handle invalid UTF-8 bytes (e.g., 0xFF in deleted entries)
        try:
            return (<bytes>self.fno.fname).decode('utf-8', errors='replace')
        except:
            # Fallback: try ASCII with replace
            return (<bytes>self.fno.fname).decode('ascii', errors='replace')
    
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


# Export constants for Python use by creating Python integer objects
# These are copies of the C enum values from ff.h
cdef int _FR_OK = FR_OK
cdef int _FR_DISK_ERR = FR_DISK_ERR
cdef int _FR_INT_ERR = FR_INT_ERR
cdef int _FR_NOT_READY = FR_NOT_READY
cdef int _FR_NO_FILE = FR_NO_FILE
cdef int _FR_NO_PATH = FR_NO_PATH
cdef int _FR_INVALID_NAME = FR_INVALID_NAME
cdef int _FR_DENIED = FR_DENIED
cdef int _FR_EXIST = FR_EXIST
cdef int _FR_INVALID_OBJECT = FR_INVALID_OBJECT
cdef int _FR_WRITE_PROTECTED = FR_WRITE_PROTECTED
cdef int _FR_INVALID_DRIVE = FR_INVALID_DRIVE
cdef int _FR_NOT_ENABLED = FR_NOT_ENABLED
cdef int _FR_NO_FILESYSTEM = FR_NO_FILESYSTEM
cdef int _FR_MKFS_ABORTED = FR_MKFS_ABORTED
cdef int _FR_TIMEOUT = FR_TIMEOUT
cdef int _FR_LOCKED = FR_LOCKED
cdef int _FR_NOT_ENOUGH_CORE = FR_NOT_ENOUGH_CORE
cdef int _FR_TOO_MANY_OPEN_FILES = FR_TOO_MANY_OPEN_FILES
cdef int _FR_INVALID_PARAMETER = FR_INVALID_PARAMETER

# File access mode constants
cdef int _FA_READ = 0x01
cdef int _FA_WRITE = 0x02
cdef int _FA_OPEN_EXISTING = 0x00
cdef int _FA_CREATE_NEW = 0x04
cdef int _FA_CREATE_ALWAYS = 0x08
cdef int _FA_OPEN_ALWAYS = 0x10
cdef int _FA_OPEN_APPEND = 0x30

# File attribute constants
cdef int _AM_DIR = 0x10
cdef int _AM_RDO = 0x01

# Create Python-accessible module-level constants
# These will be available when importing from fatfs.wrapper
PY_FR_OK = _FR_OK
PY_FR_DISK_ERR = _FR_DISK_ERR
PY_FR_INT_ERR = _FR_INT_ERR
PY_FR_NOT_READY = _FR_NOT_READY
PY_FR_NO_FILE = _FR_NO_FILE
PY_FR_NO_PATH = _FR_NO_PATH
PY_FR_INVALID_NAME = _FR_INVALID_NAME
PY_FR_DENIED = _FR_DENIED
PY_FR_EXIST = _FR_EXIST
PY_FR_INVALID_OBJECT = _FR_INVALID_OBJECT
PY_FR_WRITE_PROTECTED = _FR_WRITE_PROTECTED
PY_FR_INVALID_DRIVE = _FR_INVALID_DRIVE
PY_FR_NOT_ENABLED = _FR_NOT_ENABLED
PY_FR_NO_FILESYSTEM = _FR_NO_FILESYSTEM
PY_FR_MKFS_ABORTED = _FR_MKFS_ABORTED
PY_FR_TIMEOUT = _FR_TIMEOUT
PY_FR_LOCKED = _FR_LOCKED
PY_FR_NOT_ENOUGH_CORE = _FR_NOT_ENOUGH_CORE
PY_FR_TOO_MANY_OPEN_FILES = _FR_TOO_MANY_OPEN_FILES
PY_FR_INVALID_PARAMETER = _FR_INVALID_PARAMETER

PY_FA_READ = _FA_READ
PY_FA_WRITE = _FA_WRITE
PY_FA_OPEN_EXISTING = _FA_OPEN_EXISTING
PY_FA_CREATE_NEW = _FA_CREATE_NEW
PY_FA_CREATE_ALWAYS = _FA_CREATE_ALWAYS
PY_FA_OPEN_ALWAYS = _FA_OPEN_ALWAYS
PY_FA_OPEN_APPEND = _FA_OPEN_APPEND

PY_AM_DIR = _AM_DIR
PY_AM_RDO = _AM_RDO
