"""Versioned digest-pinned Python bases shared by authored image declarations."""

from typing import ClassVar


class BaseCatalog:
    """Resolve supported Python minors without consulting a registry at import time."""

    version: ClassVar[str] = "1"
    uv: ClassVar[str] = "0.9.2"
    renderer: ClassVar[str] = "8"
    snapshot: ClassVar[str] = "20260914T000000Z"
    slim: ClassVar[str] = (
        "ghcr.io/astral-sh/uv:0.9.2-python3.13-bookworm-slim@sha256:"
        "7072fbb9cf84e6b76bee43905c27a1cf4afa48bfa49de3cb2b57f748ada6cc10"
    )
    bases: ClassVar[dict[str, str]] = {
        "3.11": "ghcr.io/astral-sh/uv:0.9.2-python3.11-bookworm-slim@sha256:"
        "2e81b2831b2650c82457c15c3c9fbd9e2fe9531c37df6dbf93a50550810193d2",
        "3.12": "ghcr.io/astral-sh/uv:0.9.2-python3.12-bookworm-slim@sha256:"
        "ba24faa296dff74a70e284a1ec7b27ec3bb86ecd5679c8a68550cd99e62f4a2b",
        "3.13": slim,
    }

    @classmethod
    def resolve(cls, python_version: str) -> str:
        """Return the locked base or reject a Python version absent from this catalog."""
        return cls.bases[cls.supported(python_version)]

    @classmethod
    def supported(cls, python_version: str) -> str:
        """Accept the worker interpreter minors the SDK and its runtime lock support."""
        if python_version not in cls.bases:
            raise ValueError(f"Workers support Python {', '.join(cls.bases)}; got {python_version!r}")
        return python_version
