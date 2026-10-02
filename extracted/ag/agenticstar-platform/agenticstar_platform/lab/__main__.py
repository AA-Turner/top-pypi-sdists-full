"""`python -m agenticstar_platform.lab` のエントリポイント。

- 引数なし / `--reset` / `--yes`: run_lab（journey 実行 or 破棄）へ委譲
- 第 1 引数 `doctor`: read-only 診断へ委譲
"""

from __future__ import annotations

import sys


def main() -> None:
    argv = sys.argv[1:]
    if argv and argv[0] == "doctor":
        from .doctor import main as doctor_main

        sys.argv = [sys.argv[0]] + argv[1:]
        doctor_main()
        return
    from .run_lab import main as run_main

    run_main()


if __name__ == "__main__":
    main()
