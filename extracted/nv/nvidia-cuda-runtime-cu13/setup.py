import sys
from setuptools import setup

ERROR_MESSAGE = '''⚠️ THIS PROJECT 'nvidia-cuda-runtime-cu13' IS DEPRECATED.
Please use 'nvidia-cuda-runtime' instead.

To install the correct package, use:

    pip install nvidia-cuda-runtime

For more information, visit: https://pypi.org/project/nvidia-cuda-runtime/

'''

if any(arg in sys.argv for arg in ('bdist_wheel', 'bdist', 'wheel')):
    print(ERROR_MESSAGE, file=sys.stderr)
    sys.exit(1)

setup()
