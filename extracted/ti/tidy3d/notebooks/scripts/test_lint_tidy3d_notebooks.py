from __future__ import annotations

import subprocess
import sys
from io import BytesIO
from pathlib import Path
from urllib.error import HTTPError

import lint_tidy3d_notebooks as lint
import pytest


def test_restore_qmd_code_from_ruff_preserves_commented_magic_identity() -> None:
    original_code = "\n".join(
        [
            "# %matplotlib inline",
            "%matplotlib inline",
            "import sys",
            "import os",
        ]
    )
    fixed_code = lint.normalize_code_for_ruff(original_code).replace(
        "import sys\nimport os",
        "import os\nimport sys",
    )

    restored_code, restored_safe = lint.restore_qmd_code_from_ruff(
        original_code,
        fixed_code,
    )

    assert restored_safe
    assert restored_code.splitlines() == [
        "# %matplotlib inline",
        "%matplotlib inline",
        "import os",
        "import sys",
    ]


def test_normalize_code_for_ruff_preserves_question_mark_comments() -> None:
    assert lint.normalize_line_for_ruff(1, "# does this intersect?") == "# does this intersect?"
    assert (
        lint.normalize_line_for_ruff(2, "print(value)  # does this intersect?")
        == "print(value)  # does this intersect?"
    )
    assert lint.normalize_line_for_ruff(3, "value?") == ("# __tidy3d_qmd_ruff_ipython_line_3")


def test_normalize_code_for_ruff_preserves_quarto_cell_metadata() -> None:
    assert lint.normalize_line_for_ruff(1, "#| include: false") == (
        "# __tidy3d_qmd_ruff_quarto_metadata_line_1"
    )
    assert lint.normalize_line_for_ruff(2, "    #| label: fig-field") == (
        "    # __tidy3d_qmd_ruff_quarto_metadata_line_2"
    )


def test_ruff_writeback_updates_only_target_qmd_fences(tmp_path: Path) -> None:
    notebook = tmp_path / "MultiCell.qmd"
    notebook.write_text(
        "---\ntitle: Multi Cell\n---\n"
        "Intro markdown\n\n"
        "```{python}\n"
        "# %matplotlib inline\n"
        "%matplotlib inline\n"
        "print( 1)\n"
        "```\n\n"
        "text between cells\n\n"
        "```{python}\n"
        "print( 2)\n"
        "```\n\n"
        "Closing markdown\n",
        encoding="utf-8",
    )

    document = lint.parse_qmd(notebook)
    status = lint.check_python_code_with_ruff(
        {"MultiCell": document},
        ["MultiCell"],
        fix=True,
        ruff_select="E",
    )

    assert status == 0
    updated = notebook.read_text(encoding="utf-8")
    assert "# %matplotlib inline\n%matplotlib inline\n" in updated
    assert "print(1)\n" in updated
    assert "print(2)\n" in updated
    assert "Intro markdown" in updated
    assert "text between cells" in updated
    assert "Closing markdown" in updated
    assert updated.count("```") == 4


def test_ruff_writeback_preserves_question_mark_comments(
    tmp_path: Path,
) -> None:
    notebook = tmp_path / "QuestionComment.qmd"
    notebook.write_text(
        "---\ntitle: Question Comment\n---\n```{python}\n# does this intersect?\nprint( 1)\n```\n",
        encoding="utf-8",
    )
    document = lint.parse_qmd(notebook)

    status = lint.check_python_code_with_ruff(
        {"QuestionComment": document},
        ["QuestionComment"],
        fix=True,
        ruff_select="E",
    )

    assert status == 0
    updated = notebook.read_text(encoding="utf-8")
    assert "# does this intersect?\n" in updated
    assert "print(1)\n" in updated


def test_ruff_writeback_preserves_quarto_cell_metadata(tmp_path: Path) -> None:
    notebook = tmp_path / "QuartoMetadata.qmd"
    notebook.write_text(
        "---\ntitle: Quarto Metadata\n---\n"
        "```{python}\n"
        "#| include: false\n"
        "#| label: gui-data-mock\n"
        "print( 1)\n"
        "```\n",
        encoding="utf-8",
    )
    document = lint.parse_qmd(notebook)

    status = lint.check_python_code_with_ruff(
        {"QuartoMetadata": document},
        ["QuartoMetadata"],
        fix=True,
        ruff_select="E",
    )

    assert status == 0
    updated = notebook.read_text(encoding="utf-8")
    assert "#| include: false\n" in updated
    assert "#| label: gui-data-mock\n" in updated
    assert "# | include: false\n" not in updated
    assert "print(1)\n" in updated


def test_import_mapping_accepts_nested_misc_files(tmp_path: Path) -> None:
    misc = tmp_path / "misc"
    nested = misc / "fixtures"
    nested.mkdir(parents=True)
    (misc / "mock_loader.py").write_text("", encoding="utf-8")
    (nested / "result.hdf5").write_text("", encoding="utf-8")
    (misc / "import_file_mapping.json").write_text(
        "{\n"
        '    "NestedAsset.qmd": [\n'
        '        "mock_loader.py",\n'
        '        "fixtures/result.hdf5"\n'
        "    ]\n"
        "}\n",
        encoding="utf-8",
    )
    notebook = tmp_path / "NestedAsset.qmd"
    notebook.write_text(
        "---\ntitle: Nested Asset\n---\n```{python}\nrun_path('misc/mock_loader.py')\n```\n",
        encoding="utf-8",
    )

    errors = lint.validate_import_mapping(
        tmp_path,
        {"NestedAsset": lint.parse_qmd(notebook)},
    )

    assert errors == []


def test_ruff_writeback_preserves_inline_comment_padding(tmp_path: Path) -> None:
    notebook = tmp_path / "InlineCommentPadding.qmd"
    notebook.write_text(
        "---\ntitle: Inline Comment Padding\n---\n"
        "```{python}\n"
        "rows = plt.imread('misc/mona_lisa.jpg')[..., :3].mean(axis=2) / 255   # grayscale\n"
        "print( 1)\n"
        "```\n",
        encoding="utf-8",
    )
    document = lint.parse_qmd(notebook)

    status = lint.check_python_code_with_ruff(
        {"InlineCommentPadding": document},
        ["InlineCommentPadding"],
        fix=True,
        ruff_select="E",
    )

    assert status == 0
    updated = notebook.read_text(encoding="utf-8")
    assert "/ 255   # grayscale\n" in updated
    assert "print(1)\n" in updated


def test_ruff_writeback_preserves_notebook_output_semicolon(tmp_path: Path) -> None:
    notebook = tmp_path / "OutputSuppression.qmd"
    notebook.write_text(
        "---\ntitle: Output Suppression\n---\n```{python}\nplot_field();\nprint( 1)\n```\n",
        encoding="utf-8",
    )
    document = lint.parse_qmd(notebook)

    status = lint.check_python_code_with_ruff(
        {"OutputSuppression": document},
        ["OutputSuppression"],
        fix=True,
        ruff_select="E",
    )

    assert status == 0
    updated = notebook.read_text(encoding="utf-8")
    assert "plot_field();\n" in updated
    assert "print(1)\n" in updated


def test_ruff_writeback_rejects_unsafe_restore_without_rewriting(
    tmp_path: Path,
) -> None:
    notebook = tmp_path / "Unsafe.qmd"
    original_text = (
        "---\ntitle: Unsafe\n---\n```{python}\n%matplotlib inline\nimport sys\nimport os\n```\n"
    )
    notebook.write_text(original_text, encoding="utf-8")
    document = lint.parse_qmd(notebook)
    fence = lint.extract_python_fences(document)[0]
    fixed_code_path = tmp_path / "fixed.py"
    fixed_code_path.write_text("import os\nimport sys\n", encoding="utf-8")

    restored = lint.write_back_ruff_code_fixes(
        [
            lint.RuffCodeFile(
                path=fixed_code_path,
                document=document,
                fence=fence,
            )
        ]
    )

    assert not restored
    assert notebook.read_text(encoding="utf-8") == original_text


def test_restore_qmd_code_from_ruff_allows_blank_lines_before_magic_sentinel() -> None:
    original_code = "\n".join(
        [
            "import numpy as np",
            "import os",
            "%matplotlib inline",
        ]
    )

    restored_code, restored_safe = lint.restore_qmd_code_from_ruff(
        original_code,
        "\n".join(
            [
                "import os",
                "",
                "import numpy as np",
                "",
                "# __tidy3d_qmd_ruff_ipython_line_3",
            ]
        ),
    )

    assert restored_safe
    assert restored_code.splitlines() == [
        "import os",
        "",
        "import numpy as np",
        "",
        "%matplotlib inline",
    ]


def test_restore_qmd_code_from_ruff_rejects_moved_magic_sentinel() -> None:
    original_code = "\n".join(
        [
            "import sys",
            "%matplotlib inline",
            "import os",
        ]
    )

    restored_code, restored_safe = lint.restore_qmd_code_from_ruff(
        original_code,
        "\n".join(
            [
                "# __tidy3d_qmd_ruff_ipython_line_2",
                "import os",
                "import sys",
            ]
        ),
    )

    assert restored_code == ""
    assert not restored_safe


def test_ruff_writeback_rejects_non_isolated_cell_safe_selectors(
    tmp_path: Path,
) -> None:
    notebook = tmp_path / "UnsafeSelector.qmd"
    original_text = "---\ntitle: Unsafe Selector\n---\n```{python}\nimport os\n```\n"
    notebook.write_text(original_text, encoding="utf-8")
    document = lint.parse_qmd(notebook)

    status = lint.check_python_code_with_ruff(
        {"UnsafeSelector": document},
        ["UnsafeSelector"],
        fix=True,
        ruff_select="F401",
    )

    assert status == 2
    assert notebook.read_text(encoding="utf-8") == original_text


def test_ruff_writeback_rejects_terminal_semicolon_selector(tmp_path: Path) -> None:
    notebook = tmp_path / "TerminalSemicolonSelector.qmd"
    original_text = (
        "---\ntitle: Terminal Semicolon Selector\n---\n```{python}\nplot_field();\n```\n"
    )
    notebook.write_text(original_text, encoding="utf-8")
    document = lint.parse_qmd(notebook)

    status = lint.check_python_code_with_ruff(
        {"TerminalSemicolonSelector": document},
        ["TerminalSemicolonSelector"],
        fix=True,
        ruff_select="E703",
    )

    assert status == 2
    assert notebook.read_text(encoding="utf-8") == original_text


def test_effective_ruff_select_uses_notebook_profile_defaults() -> None:
    assert lint.effective_ruff_select(None, fix=False) == "B,C,E,F,NPY201,UP,W"
    assert lint.effective_ruff_select(None, fix=True) == "E"
    assert lint.effective_ruff_select("E9", fix=True) == "E9"


def test_ruff_check_args_match_tidy3d_notebook_profile() -> None:
    base_args = [
        "check",
        "--isolated",
        "--target-version",
        "py310",
        "--line-length",
        "100",
        "--select",
        "E",
    ]
    default_ignore_args = [
        "--ignore",
        "B006,B007,B008,B018,B028,B904,B905,C408,C417,C901,E402,E501,E703,E722,E731,E741,F401,F811,F821,NPY201,UP006,UP007,UP035",
    ]

    assert lint.ruff_check_args("E") == base_args
    assert lint.ruff_check_args("E", use_default_ignores=True) == [
        *base_args,
        *default_ignore_args,
    ]
    assert lint.ruff_check_args("E", fix=True) == [
        *base_args,
        "--ignore",
        "E703",
        "--preview",
    ]
    assert lint.ruff_check_args("E", fix=True, use_default_ignores=True) == [
        *base_args,
        "--ignore",
        "B006,B007,B008,B018,B028,B904,B905,C408,C417,C901,E402,E501,E703,E722,E731,E741,F401,F811,F821,NPY201,UP006,UP007,UP035",
        "--preview",
    ]


def test_ruff_writeback_fixes_keyword_spacing(tmp_path: Path) -> None:
    notebook = tmp_path / "KeywordSpacing.qmd"
    notebook.write_text(
        "---\ntitle: Keyword Spacing\n---\n```{python}\ndef f(a):\n    return a\n\nf(a= 3)\n```\n",
        encoding="utf-8",
    )
    document = lint.parse_qmd(notebook)

    status = lint.check_python_code_with_ruff(
        {"KeywordSpacing": document},
        ["KeywordSpacing"],
        fix=True,
        ruff_select="E",
    )

    assert status == 0
    assert "f(a=3)\n" in notebook.read_text(encoding="utf-8")


def test_ruff_check_uses_combined_notebook_code_for_cross_cell_names(
    tmp_path: Path,
) -> None:
    notebook = tmp_path / "CrossCell.qmd"
    notebook.write_text(
        "---\ntitle: Cross Cell\n---\n"
        "```{python}\n"
        "value = 1\n"
        "```\n\n"
        "```{python}\n"
        "print(value)\n"
        "```\n",
        encoding="utf-8",
    )
    document = lint.parse_qmd(notebook)

    status = lint.check_python_code_with_ruff(
        {"CrossCell": document},
        ["CrossCell"],
        fix=False,
        ruff_select="F",
    )

    assert status == 0


def test_ruff_check_reports_explicit_undefined_name_selection(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    notebook = tmp_path / "UndefinedName.qmd"
    notebook.write_text(
        "---\ntitle: Undefined Name\n---\n```{python}\nprint(value)\n```\n",
        encoding="utf-8",
    )
    document = lint.parse_qmd(notebook)

    status = lint.check_python_code_with_ruff(
        {"UndefinedName": document},
        ["UndefinedName"],
        fix=False,
        ruff_select="F",
    )

    assert status == 1
    output = capsys.readouterr().out
    assert f"{notebook}:5:7: F821" in output
    assert "UndefinedName.py" not in output


def test_parse_args_rejects_skip_and_fix_ruff_code(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(
        sys,
        "argv",
        ["lint_tidy3d_notebooks.py", "--skip-ruff-code", "--fix-ruff-code"],
    )

    with pytest.raises(SystemExit) as exc_info:
        lint.parse_args()

    assert exc_info.value.code == 2
    assert "--skip-ruff-code cannot be used with --fix-ruff-code" in capsys.readouterr().err


def test_run_ruff_prefers_pinned_python_module(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    commands: list[list[str]] = []

    def fake_run(
        command: list[str],
        **_: object,
    ) -> subprocess.CompletedProcess[str]:
        commands.append(command)
        return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

    monkeypatch.setattr(lint.subprocess, "run", fake_run)
    monkeypatch.setattr(lint.shutil, "which", lambda _: "/tmp/ruff")

    result = lint.run_ruff(["check", "."])

    assert result.returncode == 0
    assert commands == [[sys.executable, "-m", "ruff", "check", "."]]


def test_run_ruff_falls_back_to_path_when_module_wrapper_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    commands: list[list[str]] = []

    def fake_run(
        command: list[str],
        **_: object,
    ) -> subprocess.CompletedProcess[str]:
        commands.append(command)
        if command[:3] == [sys.executable, "-m", "ruff"]:
            return subprocess.CompletedProcess(
                command,
                1,
                stdout="",
                stderr="FileNotFoundError: /tmp/bin/ruff\n",
            )
        return subprocess.CompletedProcess(command, 0)

    monkeypatch.setattr(lint.subprocess, "run", fake_run)
    monkeypatch.setattr(lint.shutil, "which", lambda _: "/usr/bin/ruff")

    result = lint.run_ruff(["check", "."])

    assert result.returncode == 0
    assert commands == [
        [sys.executable, "-m", "ruff", "check", "."],
        ["/usr/bin/ruff", "check", "."],
    ]


def test_check_spelling_flags_close_typos_but_not_novel_jargon(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(lint, "CUSTOM_DICT_PATH", tmp_path / "missing_dictionary.json")
    notebook = tmp_path / "Spelling.qmd"
    notebook.write_text(
        "---\ntitle: Spelling\n---\n"
        "The waveguode confines the mode.\n\n"
        "We characterize the optomechanical resonator.\n",
        encoding="utf-8",
    )
    document = lint.parse_qmd(notebook)

    errors = lint.check_spelling(
        {"Spelling": document},
        ["Spelling"],
        reference_threshold=0,
    )

    spelling_report = "\n".join(errors)
    assert "waveguode" in spelling_report
    assert "optomechanical" not in spelling_report


def test_extract_links_from_qmd_finds_markdown_html_reference_and_bare_urls(
    tmp_path: Path,
) -> None:
    notebook = tmp_path / "Links.qmd"
    notebook.write_text(
        "---\ntitle: Links\n---\n"
        "[docs](https://docs.example.com/page#section)\n"
        '<img src="img/example.png" alt="Example">\n'
        "[ref]: https://example.com/reference\n"
        "Bare https://example.com/path).\n"
        "Angle [doi](<https://doi.org/10.1016/S0045-7825(02)00559-5>).\n"
        "`not_a_link[0](optical axis)`\n"
        '<!-- <img src="img/ignored.png"> -->\n'
        "```{python}\n"
        "url = 'https://example.com/ignored'\n"
        "```\n",
        encoding="utf-8",
    )
    document = lint.parse_qmd(notebook)

    links = lint.extract_links_from_qmd(document)

    assert [(link.line_number, link.target) for link in links] == [
        (4, "https://docs.example.com/page#section"),
        (5, "img/example.png"),
        (6, "https://example.com/reference"),
        (7, "https://example.com/path"),
        (8, "https://doi.org/10.1016/S0045-7825(02)00559-5"),
    ]


def test_extract_links_from_qmd_ignores_html_attributes_outside_tags(
    tmp_path: Path,
) -> None:
    notebook = tmp_path / "Links.qmd"
    notebook.write_text(
        "---\ntitle: Links\n---\n"
        "[query](https://example.com/view?src=image.png)\n"
        "Example prose with src=image.png is not an HTML tag.\n"
        "<img src=img/actual.png>\n",
        encoding="utf-8",
    )

    links = lint.extract_links_from_qmd(lint.parse_qmd(notebook))

    assert [(link.line_number, link.target) for link in links] == [
        (4, "https://example.com/view?src=image.png"),
        (6, "img/actual.png"),
    ]


def test_check_links_flags_empty_and_missing_local_targets(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    notebook = tmp_path / "Broken.qmd"
    notebook.write_text(
        "---\ntitle: Broken\n---\n[missing](missing.png)\n[empty]()\n",
        encoding="utf-8",
    )
    document = lint.parse_qmd(notebook)
    monkeypatch.setattr(lint, "check_http_links", lambda *_, **__: {})

    errors = lint.check_links(
        tmp_path,
        {"Broken": document},
        ["Broken"],
        timeout=1.0,
        workers=1,
    )

    assert any("local link target does not exist: missing.png" in error for error in errors)
    assert any("empty link target" in error for error in errors)


def test_check_links_accepts_existing_assets_and_notebook_html_links(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    (tmp_path / "img").mkdir()
    (tmp_path / "img" / "example.png").write_bytes(b"png")
    target_notebook = tmp_path / "Target.qmd"
    target_notebook.write_text("---\ntitle: Target\n---\n", encoding="utf-8")
    notebook = tmp_path / "Links.qmd"
    notebook.write_text(
        '---\ntitle: Links\n---\n<img src="img/example.png">\n[target](Target.html)\n',
        encoding="utf-8",
    )
    documents = {
        "Links": lint.parse_qmd(notebook),
        "Target": lint.parse_qmd(target_notebook),
    }
    monkeypatch.setattr(lint, "check_http_links", lambda *_, **__: {})

    assert (
        lint.check_links(
            tmp_path,
            documents,
            ["Links"],
            timeout=1.0,
            workers=1,
        )
        == []
    )


def test_check_links_rejects_notebook_html_links_in_wrong_subdirectory(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    target_notebook = tmp_path / "Target.qmd"
    target_notebook.write_text("---\ntitle: Target\n---\n", encoding="utf-8")
    notebook = tmp_path / "Links.qmd"
    notebook.write_text(
        "---\ntitle: Links\n---\n[wrong](docs/Target.html)\n",
        encoding="utf-8",
    )
    documents = {
        "Links": lint.parse_qmd(notebook),
        "Target": lint.parse_qmd(target_notebook),
    }
    checked_targets: set[str] = set()

    def fake_check_http_links(
        targets: set[str],
        *,
        timeout: float,
        workers: int,
    ) -> dict[str, str | None]:
        checked_targets.update(targets)
        return dict.fromkeys(targets)

    monkeypatch.setattr(lint, "check_http_links", fake_check_http_links)

    errors = lint.check_links(
        tmp_path,
        documents,
        ["Links"],
        timeout=1.0,
        workers=1,
    )

    assert any("local link target does not exist: docs/Target.html" in error for error in errors)
    assert checked_targets == set()


def test_check_links_resolves_missing_relative_docs_links_against_published_docs(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    target_notebook = tmp_path / "Simulation.qmd"
    target_notebook.write_text("---\ntitle: Simulation\n---\n", encoding="utf-8")
    notebook = tmp_path / "StartHere.qmd"
    notebook.write_text(
        "---\ntitle: Start Here\n---\n"
        "[api](../api/_autosummary/tidy3d.Simulation.html#tidy3d.Simulation)\n",
        encoding="utf-8",
    )
    document = lint.parse_qmd(notebook)
    checked_targets: set[str] = set()

    def fake_check_http_links(
        targets: set[str],
        *,
        timeout: float,
        workers: int,
    ) -> dict[str, str | None]:
        checked_targets.update(targets)
        return dict.fromkeys(targets)

    monkeypatch.setattr(lint, "check_http_links", fake_check_http_links)

    assert (
        lint.check_links(
            tmp_path,
            {
                "Simulation": lint.parse_qmd(target_notebook),
                "StartHere": document,
            },
            ["StartHere"],
            timeout=1.0,
            workers=1,
        )
        == []
    )
    assert checked_targets == {
        "https://docs.flexcompute.com/projects/tidy3d/en/latest/api/_autosummary/"
        "tidy3d.Simulation.html#tidy3d.Simulation"
    }


def test_check_links_resolves_relative_rst_docs_links_as_published_html(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    notebook = tmp_path / "StartHere.qmd"
    notebook.write_text(
        "---\ntitle: Start Here\n---\n"
        "[api](../api/_autosummary/tidy3d.Simulation.rst#tidy3d.Simulation)\n",
        encoding="utf-8",
    )
    document = lint.parse_qmd(notebook)
    checked_targets: set[str] = set()

    def fake_check_http_links(
        targets: set[str],
        *,
        timeout: float,
        workers: int,
    ) -> dict[str, str | None]:
        checked_targets.update(targets)
        return dict.fromkeys(targets)

    monkeypatch.setattr(lint, "check_http_links", fake_check_http_links)

    assert (
        lint.check_links(
            tmp_path,
            {"StartHere": document},
            ["StartHere"],
            timeout=1.0,
            workers=1,
        )
        == []
    )
    assert checked_targets == {
        "https://docs.flexcompute.com/projects/tidy3d/en/latest/api/_autosummary/"
        "tidy3d.Simulation.html#tidy3d.Simulation"
    }


def test_check_links_rejects_missing_relative_notebook_html_links(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    notebook = tmp_path / "StartHere.qmd"
    notebook.write_text(
        "---\ntitle: Start Here\n---\n[removed](../notebooks/Removed.html)\n",
        encoding="utf-8",
    )
    document = lint.parse_qmd(notebook)
    checked_targets: set[str] = set()

    def fake_check_http_links(
        targets: set[str],
        *,
        timeout: float,
        workers: int,
    ) -> dict[str, str | None]:
        checked_targets.update(targets)
        return dict.fromkeys(targets)

    monkeypatch.setattr(lint, "check_http_links", fake_check_http_links)

    errors = lint.check_links(
        tmp_path,
        {"StartHere": document},
        ["StartHere"],
        timeout=1.0,
        workers=1,
    )

    assert any(
        "local link target does not exist: ../notebooks/Removed.html" in error for error in errors
    )
    assert checked_targets == set()


@pytest.mark.parametrize("head_status", [403, 404, 500])
def test_check_http_link_falls_back_to_get_after_head_http_error(
    monkeypatch: pytest.MonkeyPatch,
    head_status: int,
) -> None:
    calls: list[str] = []

    class FakeResponse:
        def __enter__(self) -> FakeResponse:
            return self

        def __exit__(self, *_: object) -> None:
            return None

        def getcode(self) -> int:
            return 200

    def fake_urlopen(
        request: lint.Request,
        *,
        timeout: float,
    ) -> FakeResponse:
        calls.append(request.get_method())
        if request.get_method() == "HEAD":
            raise HTTPError(
                request.full_url,
                head_status,
                "HEAD failed",
                hdrs=None,
                fp=None,
            )
        assert timeout == 1.0
        return FakeResponse()

    monkeypatch.setattr(lint, "urlopen", fake_urlopen)

    assert lint.check_http_link("https://example.com", timeout=1.0) is None
    assert calls == ["HEAD", "GET"]


def test_check_http_link_retries_without_range_after_416(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[tuple[str, str | None]] = []

    class FakeResponse:
        def __enter__(self) -> FakeResponse:
            return self

        def __exit__(self, *_: object) -> None:
            return None

        def getcode(self) -> int:
            return 200

    def fake_urlopen(
        request: lint.Request,
        *,
        timeout: float,
    ) -> FakeResponse:
        calls.append((request.get_method(), request.get_header("Range")))
        if request.get_method() == "HEAD":
            raise HTTPError(
                request.full_url,
                405,
                "HEAD unsupported",
                hdrs=None,
                fp=None,
            )
        if request.get_header("Range"):
            raise HTTPError(
                request.full_url,
                416,
                "Range Not Satisfiable",
                hdrs=None,
                fp=None,
            )
        assert timeout == 1.0
        return FakeResponse()

    monkeypatch.setattr(lint, "urlopen", fake_urlopen)

    assert lint.check_http_link("https://example.com", timeout=1.0) is None
    assert calls == [
        ("HEAD", None),
        ("GET", "bytes=0-0"),
        ("GET", None),
    ]


def test_check_http_link_reports_rate_limit_responses(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_urlopen(
        request: lint.Request,
        *,
        timeout: float,
    ) -> object:
        assert timeout == 1.0
        raise HTTPError(
            request.full_url,
            429,
            "Too Many Requests",
            hdrs=None,
            fp=None,
        )

    monkeypatch.setattr(lint, "urlopen", fake_urlopen)

    assert lint.check_http_link("https://example.com", timeout=1.0) == "HTTP 429: Too Many Requests"


@pytest.mark.parametrize(
    ("body", "expected"),
    [
        (b'<html><h1 id="tidy3d.Simulation">Simulation</h1></html>', None),
        (
            b'<html><h1 id="tidy3d.Structure">Structure</h1></html>',
            "missing URL fragment",
        ),
    ],
)
def test_check_http_link_validates_fragments(
    monkeypatch: pytest.MonkeyPatch,
    body: bytes,
    expected: str | None,
) -> None:
    calls: list[tuple[str, str, str | None]] = []

    class FakeResponse:
        headers = {"Content-Type": "text/html; charset=utf-8"}

        def __init__(self, response_body: bytes = b"") -> None:
            self.response_body = response_body

        def __enter__(self) -> FakeResponse:
            return self

        def __exit__(self, *_: object) -> None:
            return None

        def getcode(self) -> int:
            return 200

        def read(self, size: int = -1) -> bytes:
            if size < 0:
                return self.response_body
            return self.response_body[:size]

    def fake_urlopen(
        request: lint.Request,
        *,
        timeout: float,
    ) -> FakeResponse:
        calls.append(
            (
                request.get_method(),
                request.full_url,
                request.get_header("Range"),
            )
        )
        assert timeout == 1.0
        if request.get_method() == "HEAD":
            return FakeResponse()
        return FakeResponse(body)

    monkeypatch.setattr(lint, "urlopen", fake_urlopen)

    error = lint.check_http_link(
        "https://example.com/api.html#tidy3d.Simulation",
        timeout=1.0,
    )

    if expected is None:
        assert error is None
    else:
        assert error is not None
        assert expected in error
    assert calls == [
        ("HEAD", "https://example.com/api.html", None),
        ("GET", "https://example.com/api.html", None),
    ]


@pytest.mark.parametrize(
    ("body", "expected"),
    [
        (b'<html><h1 id="tidy3d.Simulation">Simulation</h1></html>', None),
        (
            b'<html><h1 id="tidy3d.Structure">Structure</h1></html>',
            "missing URL fragment",
        ),
    ],
)
def test_check_http_link_validates_fragments_after_limited_access_http_error(
    monkeypatch: pytest.MonkeyPatch,
    body: bytes,
    expected: str | None,
) -> None:
    calls: list[str] = []

    def fake_urlopen(
        request: lint.Request,
        *,
        timeout: float,
    ) -> object:
        calls.append(request.get_method())
        assert timeout == 1.0
        if request.get_method() == "HEAD":
            raise HTTPError(
                request.full_url,
                405,
                "HEAD unsupported",
                hdrs=None,
                fp=None,
            )
        raise HTTPError(
            request.full_url,
            403,
            "Forbidden",
            hdrs={"Content-Type": "text/html; charset=utf-8"},
            fp=BytesIO(body),
        )

    monkeypatch.setattr(lint, "urlopen", fake_urlopen)

    error = lint.check_http_link(
        "https://example.com/api.html#tidy3d.Simulation",
        timeout=1.0,
    )

    if expected is None:
        assert error is None
    else:
        assert error is not None
        assert expected in error
    assert calls == ["HEAD", "GET"]


def test_check_http_links_fetches_shared_fragment_page_once(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[str] = []

    class FakeResponse:
        headers = {"Content-Type": "text/html; charset=utf-8"}

        def __enter__(self) -> FakeResponse:
            return self

        def __exit__(self, *_: object) -> None:
            return None

        def getcode(self) -> int:
            return 200

        def read(self, size: int = -1) -> bytes:
            return b'<html><h1 id="first">First</h1><h2 id="second">Second</h2></html>'

    def fake_urlopen(
        request: lint.Request,
        *,
        timeout: float,
    ) -> FakeResponse:
        calls.append(request.get_method())
        assert request.full_url == "https://example.com/api.html"
        assert timeout == 1.0
        return FakeResponse()

    monkeypatch.setattr(lint, "urlopen", fake_urlopen)

    results = lint.check_http_links(
        {
            "https://example.com/api.html",
            "https://example.com/api.html#first",
            "https://example.com/api.html#second",
            "https://example.com/api.html#missing",
        },
        timeout=1.0,
        workers=4,
    )

    assert results == {
        "https://example.com/api.html": None,
        "https://example.com/api.html#first": None,
        "https://example.com/api.html#second": None,
        "https://example.com/api.html#missing": "missing URL fragment: #missing",
    }
    assert calls == ["HEAD", "GET"]
