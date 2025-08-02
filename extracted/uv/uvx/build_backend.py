import sys


message = """
`uvx` is provided by the uv package (https://pypi.org/project/uv/). There is no need to install it
separately. This is just a dummy package guarding against dependency confusion attacks.

Previously, this was a third-party package used to extend uv's functionality. The author of that
package graciously renamed it to  `uvenv` (https://pypi.org/project/uvenv/) to avoid confusion. If
you're attempting to use that package, replace your dependency on `uvx` with `uvenv`.
"""

from hatchling.build import *  # noqa:F401,F403


def build_wheel(wheel_directory, config_settings, metadata_directory) -> str:
    print(message, file=sys.stderr)
    sys.exit(1)


def prepare_metadata_for_build_wheel(metadata_directory, config_settings) -> str:
    print(message, file=sys.stderr)
    sys.exit(1)
