try:  # assume python>=3.9
    from importlib.metadata import version as _version
except ImportError:  # older python
    from pkg_resources import get_distribution as _distribution

    def _version(package_name):
        return _distribution(package_name).version


__version__ = _version("eyes-common")
