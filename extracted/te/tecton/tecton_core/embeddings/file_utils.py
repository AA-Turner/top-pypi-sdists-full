import hashlib


# Method copied from 3.11 standard library, signature tweaked to remove the position-only operator for 3.7 compatibility
def file_digest(fileobj, digest, *, _bufsize=2**18):
    """Hash the contents of a file-like object. Returns a digest object.

    *fileobj* must be a file-like object opened for reading in binary mode.
    It accepts file objects from open(), io.BytesIO(), and SocketIO objects.
    The function may bypass Python's I/O and use the file descriptor *fileno*
    directly.

    *digest* must either be a hash algorithm name as a *str*, a hash
    constructor, or a callable that returns a hash object.
    """
    # On Linux we could use AF_ALG sockets and sendfile() to archive zero-copy
    # hashing with hardware acceleration.
    if isinstance(digest, str):
        digestobj = hashlib.new(digest)
    else:
        digestobj = digest()

    if hasattr(fileobj, "getbuffer"):
        # io.BytesIO object, use zero-copy buffer
        digestobj.update(fileobj.getbuffer())
        return digestobj

    # Only binary files implement readinto().
    if not (hasattr(fileobj, "readinto") and hasattr(fileobj, "readable") and fileobj.readable()):
        msg = f"'{fileobj!r}' is not a file-like object in binary reading mode."
        raise ValueError(msg)

    # binary file, socket.SocketIO object
    # Note: socket I/O uses different syscalls than file I/O.
    buf = bytearray(_bufsize)  # Reusable buffer to reduce allocations.
    view = memoryview(buf)
    while True:
        size = fileobj.readinto(buf)
        if size == 0:
            break  # EOF
        digestobj.update(view[:size])

    return digestobj


def hash_file(file_path: str) -> str:
    """
    Calculate the SHA256 hash of a file.
    """
    with open(file_path, "rb") as f:
        return file_digest(f, "sha256").hexdigest()
