import os
import sys
import subprocess
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

def check_python_version():
    """Check if the current Python version is supported"""
    if sys.version_info >= (3, 14):
        raise RuntimeError("Python 3.14 is not supported. Please use Python 3.13 or lower.")

def install_pyarrow():
    """Install pyarrow from bundled wheel if on Python 3.13"""
    check_python_version()
    
    if sys.version_info < (3, 13):
        return
    
    try:
        version('pyarrow')
        return
    except PackageNotFoundError:
        pass

    # Get the package's installation directory
    pipebio_location = Path(__file__).parent
    vendor_dir = pipebio_location / 'vendor' / 'pyarrow'
    
    if not vendor_dir.exists():
        raise RuntimeError(
            "Could not find bundled pyarrow wheel. "
            "Please ensure you have the necessary build dependencies installed:\n"
            "- On Linux: cmake, ninja-build, libboost-all-dev, libarrow-dev\n"
            "- On macOS: cmake, ninja, boost, apache-arrow"
        )
    
    # Find and install the appropriate wheel
    wheels = list(vendor_dir.glob("*.whl"))
    if not wheels:
        raise RuntimeError("No pyarrow wheel found in vendor directory")
    
    wheel_path = wheels[0]
    subprocess.check_call([
        sys.executable,
        "-m",
        "pip",
        "install",
        "--no-deps",
        str(wheel_path)
    ])

if __name__ == "__main__":
    install_pyarrow() 