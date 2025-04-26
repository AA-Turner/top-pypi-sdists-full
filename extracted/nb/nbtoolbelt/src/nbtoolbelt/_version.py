"""
Version, easily accessible in other files

Copyright (c) 2017 - Eindhoven University of Technology, The Netherlands

This software is made available under the terms of the MIT License.
"""

# TODO: should each tool have its own version?

import importlib.metadata

#: Package name
package_name = 'nbtoolbelt'

#: Version number, as string
try:
    __version__ = importlib.metadata.version(package_name)
except importlib.metadata.PackageNotFoundError:
    __version__ = 'unknown'
