#  Copyright (c) 2026 Snowflake Computing Inc. All rights reserved.

# Minimal entrypoint for the Code Bundle execution integration tests. The tests exercise the anonymous
# EXECUTE CODE BUNDLE FROM <stage> REST endpoint and only assert that the execution is accepted, so the
# entrypoint just needs to be a valid, importable Python module that runs without error.


def main() -> None:
    print("hello from code bundle execution")


if __name__ == "__main__":
    main()
