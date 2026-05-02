from __future__ import annotations

import sys as _sys
import apps.cli.shell_impl as _impl

if __spec__ is not None:
    _sys.modules[__spec__.name] = _impl
