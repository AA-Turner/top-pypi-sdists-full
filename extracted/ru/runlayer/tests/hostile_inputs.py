"""Crafted inputs a shadow-AI user could plant to knock a scan channel offline."""

# Overflows the recursion limit in json5, stdlib json, PyYAML and tomllib
# alike (each raises RecursionError, a RuntimeError, not a decode error). A few
# hundred KiB, so it stays under every bounded-read cap the scanners apply.
DEEP_NESTING = "[" * 100_000 + "]" * 100_000
DEEP_NESTING_BYTES = DEEP_NESTING.encode()
DEEP_NESTING_TOML = "a = " + DEEP_NESTING
