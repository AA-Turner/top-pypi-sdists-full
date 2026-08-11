#  Copyright (c) 2026 Snowflake Computing Inc. All rights reserved.

# Minimal entrypoint for the named Code Bundle execute integration test. The test only asserts that the
# execution is accepted, so the entrypoint just needs to be a valid, importable Python module.


def main() -> None:
    print("hello from named code bundle")


if __name__ == "__main__":
    main()
