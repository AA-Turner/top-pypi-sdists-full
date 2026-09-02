import platform

from importlib import metadata

try:
    package_version = metadata.version("novita-sandbox")
except metadata.PackageNotFoundError:
    package_version = "0.0.0"

default_headers = {
    "lang": "python",
    "lang_version": platform.python_version(),
    "package_version": package_version,
    "publisher": "Novita",
    "sdk_runtime": "python",
    "system": platform.system(),
}
