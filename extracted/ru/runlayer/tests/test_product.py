from pathlib import Path

import pytest

from runlayer_cli import product
from runlayer_cli.platform_installers import WINDOWS_PRODUCT_NAME_BY_PACKAGE


def test_legacy_install_without_marker_defaults_to_cli(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(product, "_PRODUCT_MARKER_PATH", tmp_path / "missing")

    assert product.installed_package() == "cli"


@pytest.mark.parametrize(
    ("marker", "expected_name"),
    [("cli\n", "Runlayer CLI"), ("desktop\n", "Runlayer")],
)
def test_reads_package_owned_product_marker(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    marker: str,
    expected_name: str,
) -> None:
    marker_path = tmp_path / "product"
    marker_path.write_text(marker, encoding="ascii")
    monkeypatch.setattr(product, "_PRODUCT_MARKER_PATH", marker_path)

    package = product.installed_package()

    assert product.package_display_name(package) == expected_name


def test_windows_product_names_extend_shared_display_names() -> None:
    assert WINDOWS_PRODUCT_NAME_BY_PACKAGE == {
        "ai-watch": "Runlayer AI Watch",
        **product.PRODUCT_DISPLAY_NAMES,
    }


def test_rejects_unknown_product_marker(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    marker_path = tmp_path / "product"
    marker_path.write_text("untrusted-package\n", encoding="ascii")
    monkeypatch.setattr(product, "_PRODUCT_MARKER_PATH", marker_path)

    with pytest.raises(RuntimeError, match="marker is invalid"):
        product.installed_package()
