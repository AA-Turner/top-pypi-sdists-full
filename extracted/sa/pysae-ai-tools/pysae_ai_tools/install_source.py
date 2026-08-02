"""Resolve where the running ``pysae-ai-tools`` was installed from.

The install source decides how self-update and the version banner behave:

- a **local directory** install (``uv tool install [-e] <repo>``) updates via
  ``git pull`` + ``install.sh`` and checks ``origin/main`` for new commits;
- a **registry** install (``uv tool install pysae-ai-tools``) updates via
  ``uv tool upgrade`` and checks PyPI for a newer release.

Detection reads uv's tool receipt (``uv-receipt.toml``), which records the
original requirement. This is authoritative even when uv copied the package
into the tool venv — the case a non-editable directory install produces, and
exactly the case ``__file__``-based detection gets wrong (the package then
lives under the venv, not the checkout, so it looks like a registry install).
"""

import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path

import pysae_ai_tools

PACKAGE = "pysae-ai-tools"


@dataclass
class InstallSource:
    """Resolved origin of the running install.

    ``local_dir`` is the source directory when uv installed the tool from a
    local path (``editable`` or plain ``directory`` requirement) — the repo we
    can ``git pull`` and reinstall from. It is ``None`` for a registry (PyPI)
    install.
    """

    local_dir: Path | None

    @property
    def is_local(self) -> bool:
        return self.local_dir is not None


def _receipt_path() -> Path | None:
    """uv tool receipt for the running interpreter, if present.

    uv installs each tool into its own venv and drops the receipt at the venv
    root; ``sys.prefix`` of the running interpreter is that root.
    """
    receipt = Path(sys.prefix) / "uv-receipt.toml"
    return receipt if receipt.is_file() else None


def _parse_receipt(receipt: Path) -> dict[str, object] | None:
    """Parse the receipt; ``None`` when it can't be read or isn't valid TOML."""
    try:
        return tomllib.loads(receipt.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError):
        return None


def _local_dir_from_data(data: dict[str, object]) -> Path | None:
    """Local source directory recorded in the parsed receipt, if any."""
    tool = data.get("tool")
    requirements = tool.get("requirements") if isinstance(tool, dict) else None
    if not isinstance(requirements, list):
        return None

    for req in requirements:
        if not isinstance(req, dict) or req.get("name") != PACKAGE:
            continue
        path = req.get("editable") or req.get("directory")
        if isinstance(path, str) and path:
            return Path(path)
    return None


def detect_install_source() -> InstallSource:
    """Determine whether the running install is local or from a registry."""
    receipt = _receipt_path()
    if receipt is not None:
        data = _parse_receipt(receipt)
        if data is not None:
            # A readable receipt is authoritative: it records a local source
            # path (editable or plain directory), or a registry install when
            # none is present.
            return InstallSource(local_dir=_local_dir_from_data(data))

    # No receipt, or one we couldn't parse: fall back to the package location.
    # An editable install run straight from a checkout has its ``__file__``
    # inside the repo, so a ``.git`` sibling still flags it local.
    pkg_root = Path(pysae_ai_tools.__file__).resolve().parent.parent
    if (pkg_root / ".git").exists():
        return InstallSource(local_dir=pkg_root)

    return InstallSource(local_dir=None)
