from __future__ import annotations

import sys as _sys
import apps.cli.cli_main_impl as _impl

if __spec__ is not None:
    _sys.modules[__spec__.name] = _impl

if __name__ == "__main__":
    raise SystemExit(_impl.main())
