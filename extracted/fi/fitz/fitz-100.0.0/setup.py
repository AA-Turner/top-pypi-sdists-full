from setuptools import setup
import sys

sys.stderr.write(
    "\nERROR: Package 'fitz' has been deactivated and cannot be installed.\n"
    "Please install 'pymupdf' instead."
)
raise SystemExit(1)
# setup()