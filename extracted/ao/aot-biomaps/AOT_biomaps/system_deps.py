import os
import shutil
import platform

def ensure_system_dependencies():
    """
    Check that the system libraries required by k-Wave (szip/libaec, fftw3)
    are available. If present, inject them into LD_LIBRARY_PATH (Linux) or
    PATH (Windows). If absent, print a warning: k-Wave will be unavailable,
    but reconstruction (precomputed SMatrix, CuPy) works normally.
    """
    system = platform.system()

    if system == 'Linux':
        user_lib_dir = os.path.expanduser("~/.local/lib")
        if os.path.isdir(user_lib_dir):
            current = os.environ.get('LD_LIBRARY_PATH', '')
            if user_lib_dir not in current:
                os.environ['LD_LIBRARY_PATH'] = f"{user_lib_dir}:{current}"

        # k-Wave needs these libs: if missing, warn and return gracefully.
        required = ['libsz.so.2', 'libaec.so.0', 'libfftw3f.so.3', 'libfftw3.so.3']
        search_dirs = ["/usr/lib/x86_64-linux-gnu", "/usr/lib", user_lib_dir]
        missing = [lib for lib in required
                   if not any(os.path.isfile(os.path.join(d, lib))
                              for d in search_dirs if os.path.isdir(d))]
        if missing:
            print("[AOT-biomaps] Warning: k-Wave system libraries missing: " + ", ".join(missing))
            print("[AOT-biomaps] Acoustic simulation will be disabled. Fix: sudo apt install libsz2 libaec0 libfftw3-3 (ask your administrator). Reconstruction with precomputed SMatrix is NOT affected.")
            return False

    elif system == 'Windows':
        # szip.dll must be either in ~\.local\bin or already in PATH
        user_bin = os.path.expanduser("~/.local/bin")
        szip = os.path.join(user_bin, "szip.dll")
        if os.path.isfile(szip):
            os.environ['PATH'] = f"{user_bin};{os.environ.get('PATH', '')}"
            return True
        # Is szip.dll accessible some other way? (installed elsewhere)
        if shutil.which("szip.dll") is None:
            print("[AOT-biomaps] Warning: szip.dll not found. k-Wave (acoustic simulation) will be disabled.")
            print("[AOT-biomaps] Fix on Windows: download szip 2.1.1 (HDF Group) and place szip.dll in ~\\.local\\bin. Reconstruction with precomputed SMatrix is NOT affected.")
            return False

    return True