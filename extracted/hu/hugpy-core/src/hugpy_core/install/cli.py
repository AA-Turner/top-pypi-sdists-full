"""Core commands. The installed server is the abstract_flask application."""
from __future__ import annotations


import sys

from hugpy_core.imports.constant.install import (
    INSTALLER_VERBS,
)


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] == "legacy":
        argv.pop(0)
    if argv and argv[0] == "addon":
        from hugpy_core.install.addons import main as addon_main
        return addon_main(argv[1:])
    if argv and argv[0] in INSTALLER_VERBS:
        if "--system" in argv:
            from hugpy_core.install.system import main as system_main
            return system_main(argv)
        from hugpy_core.install.installer import main as installer_main
        return installer_main(argv)
    if argv and argv[0] == "serve":
        argv.pop(0)
        from hugpy_core.web.server import main as server_main
        return server_main(argv)
    # The per-user orbit keeps the extra startup jobs in the original Flask
    # entry point. The installed system service uses web.server plus intake.
    from hugpy_core.web.app import main as server_main
    return server_main(argv)


if __name__ == "__main__":
    sys.exit(main())
