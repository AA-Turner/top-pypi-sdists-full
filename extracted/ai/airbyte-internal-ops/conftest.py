"""Shared pytest configuration."""

collect_ignore_glob = [
    # Standalone webapps have isolated dependency and test configuration.
    "webapps/**/*",
]
