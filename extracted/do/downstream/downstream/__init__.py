"""Top-level package for downstream."""

import lazy_loader

__author__ = "Matthew Andres Moreno"
__email__ = "m.more500@gmail.com"

__getattr__, __dir__, _ = lazy_loader.attach_stub(__name__, __file__)
