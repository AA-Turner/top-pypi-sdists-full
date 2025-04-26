# Copyright 2019 Cognite AS
# flake8: noqa
# mypy: allow-untyped-defs


def get_version():
    try:
        # Python 3.8+
        from importlib import metadata
    except ImportError:
        # Python 3.7
        import importlib_metadata as metadata

    try:
        v = metadata.version("cognite-seismic-sdk")
    except Exception:
        v = "(n/a)"
    return v
