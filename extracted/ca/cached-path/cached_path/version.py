import os

_MAJOR = "1"
_MINOR = "7"
# On main and in a nightly release the patch should be one ahead of the last
# released build.
_PATCH = "3"
# This is mainly for nightly builds which have the suffix ".dev$DATE". See
# https://semver.org/#is-v123-a-semantic-version for the semantics.
_SUFFIX = os.environ.get("CACHED_PATH_VERSION_SUFFIX", "")

VERSION_SHORT = "{0}.{1}".format(_MAJOR, _MINOR)
VERSION = "{0}.{1}.{2}{3}".format(_MAJOR, _MINOR, _PATCH, _SUFFIX)
