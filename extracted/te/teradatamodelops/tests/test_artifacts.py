import os
from types import SimpleNamespace

import pytest

from tmo.util import artifacts


def test_save_plot_with_context_and_custom_dpi(tmp_path):
    out_dir = tmp_path / "out"
    out_dir.mkdir(parents=True, exist_ok=True)
    ctx = SimpleNamespace()
    ctx.artifact_output_path = str(out_dir)
    artifacts.save_plot("My Plot Title", dpi=300, context=ctx)  # type: ignore
    expected = os.path.join(ctx.artifact_output_path, "my_plot_title.png")
    assert os.path.isfile(expected)
    os.remove(expected)


def test_save_plot_without_context_uses_default_path():
    out_dir = os.path.join("artifacts", "output")
    os.makedirs(out_dir, exist_ok=True)
    artifacts.save_plot("Another Plot", dpi=150)
    expected = os.path.join(out_dir, "another_plot.png")
    assert os.path.isfile(expected)
    os.remove(expected)


def test_save_plot_propagates_exception_and_does_not_clear(monkeypatch, tmp_path):
    def raise_oserror(self, *args, **kwargs):  # noqa
        raise OSError("disk full")

    import matplotlib.figure as mf

    monkeypatch.setattr(mf.Figure, "savefig", raise_oserror)
    ctx = SimpleNamespace()
    ctx.artifact_output_path = str(tmp_path / "out")
    with pytest.raises(OSError):
        artifacts.save_plot("Bad Plot", dpi=72, context=ctx)  # type: ignore


def test_title_transformation_multiple_spaces():
    out_dir = os.path.join("artifacts", "output")
    os.makedirs(out_dir, exist_ok=True)
    artifacts.save_plot("  Mixed   CASE Title  ", dpi=10)
    expected_name = "__mixed___case_title__"
    expected = os.path.join(out_dir, f"{expected_name}.png")
    assert os.path.isfile(expected)
    os.remove(expected)


def test_save_plot_unicode_title(tmp_path):
    out_dir = tmp_path / "out"
    out_dir.mkdir(parents=True, exist_ok=True)
    ctx = SimpleNamespace()
    ctx.artifact_output_path = str(out_dir)
    title = "Título Ñá"
    artifacts.save_plot(title, dpi=72, context=ctx)  # type: ignore
    expected_name = title.replace(" ", "_").lower()
    expected = os.path.join(ctx.artifact_output_path, f"{expected_name}.png")
    assert os.path.isfile(expected)
    os.remove(expected)


def test_save_plot_with_subdir_in_title_creates_in_subdir():
    base = os.path.join("artifacts", "output")
    sub = os.path.join(base, "sub")
    os.makedirs(sub, exist_ok=True)
    title = "sub/plot name"
    artifacts.save_plot(title, dpi=50)
    expected_name = "plot_name"
    expected = os.path.join(base, "sub", f"{expected_name}.png")
    assert os.path.isfile(expected)
    os.remove(expected)


def test_save_plot_empty_title_raises(tmp_path):
    out_dir = tmp_path / "out"
    out_dir.mkdir(parents=True, exist_ok=True)
    ctx = SimpleNamespace()
    ctx.artifact_output_path = str(out_dir)
    try:
        artifacts.save_plot("", dpi=10, context=ctx)  # type: ignore
    except OSError:
        return
    files = [
        f
        for f in os.listdir(ctx.artifact_output_path)
        if os.path.isfile(os.path.join(ctx.artifact_output_path, f))
    ]
    assert files, "Expected a file to be created when title is empty"
    for f in files:
        os.remove(os.path.join(ctx.artifact_output_path, f))


def test_save_plot_passes_dpi_to_savefig(monkeypatch):
    import matplotlib.figure as mf

    captured = {}

    def fake_savefig(self, filename, dpi=None):
        captured["filename"] = filename
        captured["dpi"] = dpi

    monkeypatch.setattr(mf.Figure, "savefig", fake_savefig)
    artifacts.save_plot("My DPI Test", dpi=123)
    assert captured["dpi"] == 123
    assert captured["filename"].endswith("my_dpi_test")
