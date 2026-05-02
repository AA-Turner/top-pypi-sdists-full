from __future__ import annotations

import sys as _sys
import packages.context.runtime_impl as _impl

if __spec__ is not None:
    _sys.modules[__spec__.name] = _impl
