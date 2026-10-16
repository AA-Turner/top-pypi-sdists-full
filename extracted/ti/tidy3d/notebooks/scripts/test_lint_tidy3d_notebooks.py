from __future__ import annotations

import subprocess
import sys
from pathlib import Path

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


def test_ruff_writeback_rejects_unsafe_restore_without_rewriting(tmp_path: Path) -> None:
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


def test_ruff_writeback_rejects_non_isolated_cell_safe_selectors(tmp_path: Path) -> None:
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


def test_ruff_check_uses_combined_notebook_code_for_cross_cell_names(tmp_path: Path) -> None:
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
