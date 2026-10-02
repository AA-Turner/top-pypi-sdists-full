"""Directory listing, keyboard behavior, and the rendered import dialog."""

from __future__ import annotations

from pathlib import Path

import pytest

from probe.cli import backfill
from probe.cli import backfill_evidence as ev

# Every test here drives a prompt_toolkit app session and asserts on the frames
# it rendered. That is a finished-render measurement, so it belongs in the serial
# lane with the pty tests -- see the `tui` marker in agent/pyproject.toml.
pytestmark = pytest.mark.tui


def _tree(root, *names):
    for n in names:
        (root / n).mkdir(parents=True, exist_ok=True)
    return root


def test_every_child_is_listed_with_no_cap(tmp_path):
    """The old `[:40]` slice hid the rest silently. On the shared drive this
    feature exists for, a folder you cannot see reads as one that is not there."""
    _tree(tmp_path, *[f"researcher_{i:03d}" for i in range(60)])
    assert len(backfill.subdirectories(tmp_path)) == 60


def test_children_come_back_as_paths_not_censused_tuples(tmp_path):
    _tree(tmp_path, "michael")
    got = backfill.subdirectories(tmp_path)
    assert got == [tmp_path / "michael"]
    assert all(isinstance(p, Path) for p in got)


def test_listing_children_never_walks_into_them(tmp_path, monkeypatch):
    """The reason the cap existed: every child was walked RECURSIVELY before the
    screen could draw, paid again on every keypress that changes directory."""
    _tree(tmp_path, "a", "b")
    (tmp_path / "a" / "deep").mkdir()
    (tmp_path / "a" / "deep" / "f.bin").write_text("x")

    # Repointed at the walker that exists. This patched `backfill.scan`, which
    # is deleted -- monkeypatching a missing attribute raises, so the test
    # would have died loudly rather than quietly stopping guarding, but the
    # guard still has to point somewhere real.
    calls = []
    real = ev.walk
    monkeypatch.setattr(ev, "walk", lambda *a, **k: calls.append(a) or real(*a, **k))
    backfill.subdirectories(tmp_path)
    assert calls == [], "the picker must not census its children"


def test_build_noise_and_dotdirs_are_not_offered(tmp_path):
    _tree(tmp_path, "keep", "__pycache__", ".git", "node_modules", ".venv")
    assert [p.name for p in backfill.subdirectories(tmp_path)] == ["keep"]


def test_children_are_sorted_so_the_list_is_stable(tmp_path):
    _tree(tmp_path, "zeta", "alpha", "mid")
    assert [p.name for p in backfill.subdirectories(tmp_path)] == ["alpha", "mid", "zeta"]


def test_files_are_not_offered_as_folders(tmp_path):
    _tree(tmp_path, "adir")
    (tmp_path / "afile.txt").write_text("x")
    assert [p.name for p in backfill.subdirectories(tmp_path)] == ["adir"]


def test_an_unreadable_directory_lists_as_empty_rather_than_raising(tmp_path, monkeypatch):
    # Patched at `os.scandir`, not `Path.iterdir`. The picker stopped calling
    # iterdir when it moved to scandir, so this test kept passing while
    # guarding nothing -- it never entered the code path it names.
    def boom(*a, **k):
        raise OSError("permission denied")

    monkeypatch.setattr(backfill.os, "scandir", boom)
    assert backfill.subdirectories(tmp_path) == []


def test_the_picker_never_censuses_the_folder_it_is_standing_in(tmp_path, monkeypatch):
    """INVERTED, and deliberately so.

    This test used to assert the opposite -- that `own = scan(here)` stays,
    "capped and fast". On a laptop over a git checkout it is. On the research
    drives this feature exists for it is a full recursive stat walk before a
    single row can be drawn, paid again on every `cd`, and `../` paid it on a
    bigger tree. A user watched it for minutes to be shown "20,000+ files".

    Without this assertion, re-adding the census leaves every other test green.
    """
    _tree(tmp_path, "a", "b")
    (tmp_path / "a" / "deep").mkdir()
    (tmp_path / "a" / "deep" / "f.bin").write_text("x")

    walked = []
    real = ev.walk
    monkeypatch.setattr(ev, "walk", lambda *a, **k: walked.append(a) or real(*a, **k))
    backfill.subdirectories(tmp_path)
    assert walked == [], "the picker must not walk the tree to draw a row"


def test_the_picker_still_offers_a_symlinked_directory(tmp_path):
    """`scandir` is a speedup, not a UX change.

    `Path.is_dir()` follows links and always did, so a symlinked directory has
    always been a browsable row. `DirEntry.is_dir(follow_symlinks=False)` is
    faster still and would silently drop it -- which is a different feature,
    not an optimisation.
    """
    (tmp_path / "real").mkdir()
    (tmp_path / "link").symlink_to(tmp_path / "real")
    assert [p.name for p in backfill.subdirectories(tmp_path)] == ["link", "real"]


def _pick(root, keys):
    from prompt_toolkit.application import create_app_session
    from prompt_toolkit.input import create_pipe_input
    from prompt_toolkit.output import DummyOutput

    with create_pipe_input() as pipe:
        with create_app_session(input=pipe, output=DummyOutput()):
            # A broken binding must fail the assertion instead of hanging CI.
            pipe.send_text(keys + "\x03")
            return backfill.choose_directory(root)


def test_confirmation_imports_current_folder_even_when_a_child_is_highlighted(tmp_path):
    _tree(tmp_path, "child")
    assert _pick(tmp_path, "i") == tmp_path


def test_enter_opens_a_child_and_only_the_button_confirms_it(tmp_path):
    _tree(tmp_path, "child")
    assert _pick(tmp_path, "\ri") == tmp_path / "child"


def test_last_folder_is_reachable_without_losing_any_children(tmp_path):
    _tree(tmp_path, *[f"folder_{i:03d}" for i in range(194)])
    assert _pick(tmp_path, "\x1b[F\ri") == tmp_path / "folder_193"


def test_up_one_folder_returns_to_parent_and_can_reopen_previous_child(tmp_path):
    _tree(tmp_path, "a", "b")
    # The explicit parent row opens up, retaining the directory we left.
    assert _pick(tmp_path / "b", "\r\ri") == tmp_path / "b"


@pytest.mark.parametrize("key", ["\x1b[D", "\x1b[C", "\x7f"])
def test_arrows_and_backspace_do_not_navigate_the_folder_list(tmp_path, key):
    _tree(tmp_path, "child")
    assert _pick(tmp_path, key + "i") == tmp_path


def test_arrows_and_backspace_still_edit_the_path(tmp_path):
    _tree(tmp_path, "abcd")
    keys = "\x0c\x01\x0bac\x1b[Db\x1b[CdX\x7f\ri"
    assert _pick(tmp_path, keys) == tmp_path / "abcd"


def test_path_field_accepts_a_quoted_relative_path(tmp_path):
    _tree(tmp_path, "with spaces")
    assert _pick(tmp_path, '\x0c\x01\x0b"with spaces"\ri') == tmp_path / "with spaces"


def test_path_field_accepts_a_quoted_absolute_path(tmp_path):
    target = _tree(tmp_path, "with spaces") / "with spaces"
    assert _pick(tmp_path, f"\x0c\x01\x0b  '{target}'  \ri") == target


def test_tilde_path_expands_to_home(tmp_path):
    assert _pick(tmp_path, "\x0c\x01\x0b~\ri") == Path.home().resolve()


def test_file_path_is_rejected_and_can_be_corrected(tmp_path):
    (tmp_path / "file.txt").write_text("x")
    _tree(tmp_path, "child")
    assert _pick(tmp_path, "\x0c\x01\x0bfile.txt\r\x01\x0bchild\ri") == tmp_path / "child"


def test_escape_leaves_the_picker_after_invalid_path_edits(tmp_path):
    from probe.cli import tui

    assert _pick(tmp_path, "\x0c\x01\x0bmissing\r\x1b") is tui.BACK


def test_import_with_an_unsubmitted_address_opens_it_for_review_first(tmp_path):
    from prompt_toolkit.application import create_app_session
    from prompt_toolkit.input import create_pipe_input
    from prompt_toolkit.output import DummyOutput
    from probe.cli.directory_picker import DirectoryPicker

    _tree(tmp_path, "child")
    with create_pipe_input() as pipe, create_app_session(input=pipe, output=DummyOutput()):
        picker = DirectoryPicker(tmp_path, backfill.subdirectories)
        picker.path.text = "child"
        picker.import_folder()
        assert picker.here == tmp_path / "child"
        assert not picker.app.is_done


def test_invalid_path_can_be_corrected_without_leaving_the_dialog(tmp_path):
    _tree(tmp_path, "child")
    keys = "\x0c\x01\x0bmissing\r\x01\x0bchild\ri"
    assert _pick(tmp_path, keys) == tmp_path / "child"


def test_empty_folder_can_be_confirmed(tmp_path):
    assert _pick(tmp_path, "i") == tmp_path


@pytest.mark.parametrize("focus", ["", "\t", "\t\t", "\t\t\t"],
                         ids=["folders", "back", "skip", "import"])
def test_b_leaves_from_every_browsing_control(tmp_path, focus):
    from probe.cli import tui

    _tree(tmp_path, "child")
    assert _pick(tmp_path, focus + "b") is tui.BACK


@pytest.mark.parametrize("focus", ["", "\t", "\t\t", "\t\t\t"],
                         ids=["folders", "back", "skip", "import"])
def test_i_confirms_from_every_browsing_control(tmp_path, focus):
    _tree(tmp_path, "child")
    assert _pick(tmp_path, focus + "i") == tmp_path


def test_i_opens_an_edited_path_before_confirming_it(tmp_path):
    from probe.cli import tui

    _tree(tmp_path, "child")
    edited = "\x0c\x01\x0bchild\ti"
    assert _pick(tmp_path, edited + "b") is tui.BACK
    assert _pick(tmp_path, edited + "i") == tmp_path / "child"


def test_i_keeps_an_invalid_path_editable_until_corrected(tmp_path):
    _tree(tmp_path, "child")
    keys = "\x0c\x01\x0bmissing\ti\x01\x0bchild\rii"
    assert _pick(tmp_path, keys) == tmp_path / "child"


@pytest.mark.parametrize("focus", ["", "\t", "\t\t", "\t\t\t"],
                         ids=["folders", "back", "skip", "import"])
def test_s_skips_from_every_browsing_control(tmp_path, focus):
    from probe.cli import tui

    _tree(tmp_path, "child")
    assert _pick(tmp_path, focus + "s") is tui.SKIP


@pytest.mark.parametrize("letter", ["b", "s", "i"])
def test_action_letters_type_in_path_instead_of_triggering_actions(tmp_path, letter):
    _tree(tmp_path, letter)
    assert _pick(tmp_path, "\x0c\x01\x0b" + letter + "\ri") == tmp_path / letter


def test_ctrl_b_edits_path_without_leaving_picker(tmp_path):
    _tree(tmp_path, "bis")
    assert _pick(tmp_path, "\x0c\x01\x0bbs\x02i\ri") == tmp_path / "bis"


def test_skip_folder_button_does_not_confirm_the_folder(tmp_path):
    from probe.cli import tui

    assert _pick(tmp_path, "\t\t\r") is tui.SKIP


@pytest.mark.parametrize("keys, quit", [
    ("\x1b", False), ("\t\r", False), ("\t\x1b", False),
    ("\t\t\x1b", False), ("\x0c\x1b", False),
    ("\x03", True), ("\x0c\x03", True),
])
def test_back_and_quit_keep_their_distinct_results(tmp_path, keys, quit):
    from probe.cli import tui

    assert _pick(tmp_path, keys) is (None if quit else tui.BACK)


def _browser_screen(
    *, rows=24, cols=80, keys=b"", root="/Users/richy/Documents/GitHub", onboarding=False,
    count=194,
):
    import sys
    from tests.test_setup_wizard import _pty_screen

    code = """
from contextlib import nullcontext
from pathlib import Path
from probe.cli import backfill, tui
count = int(__import__('sys').argv[3])
backfill.subdirectories = lambda p: [p / ("project_%03d" % i) for i in range(count)]
def header():
    width = min(tui.CONTENT_WIDTH, tui.columns())
    title, step = "Install Probe", "Step 3 of 4"
    if width < 50:
        return [title, step, "─" * width]
    return [title + " " * (width - len(title) - len(step)) + step, "─" * width]
context = tui.onboarding(header) if __import__('sys').argv[2] == 'yes' else nullcontext()
with context:
    backfill.choose_directory(Path(__import__('sys').argv[1]))
"""
    return _pty_screen(
        [sys.executable, "-c", code, root, "yes" if onboarding else "no", str(count)],
        rows=rows, cols=cols, keys=keys,
    )


def _assert_compact_folder_controls(screen):
    lines = screen.lines()
    list_top = next(i for i, line in enumerate(lines) if "Folders ·" in line)
    list_bottom = max(i for i, line in enumerate(lines) if "└" in line)
    status = list_bottom + 1
    actions = next(i for i, line in enumerate(lines) if "Skip (s)" in line)
    help_row = max(i for i, line in enumerate(lines) if "i Import" in line and "b Back" in line)
    assert "folder" in lines[status], screen.dump()
    assert 1 <= actions - status <= 2, screen.dump()
    assert "Back" in lines[actions], screen.dump()
    assert "Import" in lines[actions], screen.dump()
    assert "s Skip" in lines[help_row], screen.dump()
    assert 1 <= help_row - actions <= 2, screen.dump()
    assert not any(lines[help_row + 1:]), screen.dump()
    # The list still scrolls, without a scrollbar consuming its last column.
    # Its former arrow cells are spaces right up to the frame's inner edge.
    for line in lines[list_top + 1:list_bottom]:
        assert line.rstrip().endswith(" │"), screen.dump()
    return help_row


@pytest.mark.parametrize("rows,cols", [(24, 80), (40, 120), (12, 80), (24, 40)])
@pytest.mark.pty
def test_actual_folder_dialog_keeps_controls_visible_at_end_of_large_list(rows, cols):
    screen = _browser_screen(rows=rows, cols=cols, keys=b"\x1b[F")
    lines = screen.lines()
    text = "\n".join(lines)
    assert "Import a folder" in text, screen.dump()
    assert "Current folder" in text, screen.dump()
    assert text.count("/Users/richy/Documents/GitHub") == 1, screen.dump()
    assert ("Import (i) >" if cols < 50 else "Import this folder (i) >") in text, screen.dump()
    assert "Back" in text, screen.dump()
    assert "project_193/" in text, screen.dump()
    assert "project_000/" not in text, screen.dump()
    assert sum("project_" in line for line in lines) <= 10, screen.dump()
    margin = {12: 0, 24: 3, 40: 5}[rows]
    assert "Import a folder" in lines[margin], screen.dump()
    if margin:
        assert not any(lines[:margin] + lines[-margin:]), screen.dump()
    copy = " ".join(text.split())
    assert "Pick a project folder." in copy, screen.dump()
    assert "Your agent describes its files and results in Probe." in copy, screen.dump()
    assert "You review the plan before upload." in copy, screen.dump()
    path_row = next(i for i, line in enumerate(lines) if "Current folder" in line)
    assert "before upload" in " ".join(" ".join(lines[:path_row]).split()), screen.dump()
    assert "Ctrl+B" not in text and "Ctrl+N" not in text and "Ctrl+S" not in text, screen.dump()
    actions = next(line for line in lines if "Skip (s)" in line)
    assert "< Back (b)" in actions and "Skip (s)" in actions, screen.dump()
    assert actions.count("<") == actions.count(">") == 1, screen.dump()
    assert actions.rstrip().endswith("(i) >"), screen.dump()
    _assert_compact_folder_controls(screen)


@pytest.mark.parametrize("rows,cols", [(24, 80), (40, 120), (24, 40)])
@pytest.mark.pty
def test_onboarding_folder_dialog_keeps_progress_and_compact_controls_around_the_list(rows, cols):
    screen = _browser_screen(rows=rows, cols=cols, keys=b"\x1b[F", onboarding=True)
    lines = screen.lines()
    text = "\n".join(lines)
    header_rows = 3 if cols < 50 else 2
    margin = {24: 3, 40: 5}[rows]
    assert lines[0] == lines[-1] == "", screen.dump()
    assert not any(lines[:margin] + lines[-margin:]), screen.dump()
    assert "Install Probe" in lines[margin], screen.dump()
    assert "Step 3 of 4" in "\n".join(lines[margin:margin + header_rows]), screen.dump()
    assert "─" in lines[margin + header_rows - 1], screen.dump()
    assert lines[margin + header_rows] == "", screen.dump()
    assert "Import a folder" in lines[margin + header_rows + 1], screen.dump()
    assert "project_193/" in text, screen.dump()
    assert "project_000/" not in text, screen.dump()
    help_row = _assert_compact_folder_controls(screen)
    expected_left = max(0, (cols - 76) // 2)
    for line in (lines[margin], lines[margin + header_rows - 1],
                 lines[margin + header_rows + 1], lines[help_row]):
        assert len(line) - len(line.lstrip()) == expected_left, screen.dump()


@pytest.mark.parametrize("count", [0, 2])
@pytest.mark.pty
def test_small_folder_lists_use_only_the_rows_they_need(count):
    screen = _browser_screen(rows=40, cols=120, count=count)
    lines = screen.lines()
    list_top = next(i for i, line in enumerate(lines) if "Folders ·" in line)
    list_bottom = max(i for i, line in enumerate(lines) if "└" in line)
    description_end = next(i for i, line in enumerate(lines) if "before upload." in line)
    path_top = next(i for i, line in enumerate(lines) if "Current folder" in line)
    assert path_top - description_end >= 2, screen.dump()
    assert list_top - (path_top + 2) >= 2, screen.dump()
    # The current folder's parent remains available alongside its children.
    assert list_bottom - list_top - 1 == count + 1, screen.dump()
    help_row = _assert_compact_folder_controls(screen)
    assert len(lines) - help_row - 1 >= 10, screen.dump()


@pytest.mark.pty
def test_compact_onboarding_shows_the_parent_beside_the_selected_folder():
    screen = _browser_screen(rows=24, cols=80, count=30, onboarding=True)
    text = "\n".join(screen.lines())
    assert "../  Up one folder" in text, screen.dump()
    assert "› project_000/" in text, screen.dump()
    assert "project_001/" in text, screen.dump()
    assert "Import this folder" in text, screen.dump()
    _assert_compact_folder_controls(screen)


def test_folder_list_reflows_when_terminal_and_progress_header_resize(tmp_path, monkeypatch):
    from prompt_toolkit.application import create_app_session
    from prompt_toolkit.data_structures import Size
    from prompt_toolkit.input import create_pipe_input
    from prompt_toolkit.output import DummyOutput
    from probe.cli import tui
    from probe.cli.directory_picker import DirectoryPicker

    _tree(tmp_path, *[f"folder_{i:03d}" for i in range(12)])
    terminal = Size(rows=40, columns=120)
    output = DummyOutput()
    monkeypatch.setattr(output, "get_size", lambda: terminal)
    header = ["Install Probe · Step 3 of 4", "─" * 76]
    with create_pipe_input() as pipe, create_app_session(input=pipe, output=output):
        with tui.onboarding(lambda: header):
            picker = DirectoryPicker(tmp_path, backfill.subdirectories)
            assert picker.visible_rows() == 10
            terminal = Size(rows=24, columns=80)
            assert picker.visible_rows() == 3
            assert picker.outer_rows().top == picker.outer_rows().bottom == 3
            terminal = Size(rows=24, columns=40)
            header[:] = ["Install Probe", "Step 3 of 4", "─" * 40]
            assert picker.visible_rows() == 1
            assert picker.outer_rows().top == picker.outer_rows().bottom == 3
            terminal = Size(rows=40, columns=120)
            assert picker.visible_rows() == 10


@pytest.mark.pty
def test_long_path_does_not_wrap_and_displace_the_header_or_confirm_button():
    screen = _browser_screen(root="/very-long-parent" * 20 + "/research")
    text = "\n".join(screen.lines())
    assert "Import a folder" in text, screen.dump()
    assert "Folders · 194" in text, screen.dump()
    assert "Import this folder" in text, screen.dump()
    assert "project_000/" in text, screen.dump()


@pytest.mark.pty
def test_path_editing_hint_omits_inactive_action_shortcuts():
    screen = _browser_screen(keys=b"\x0c")
    text = "\n".join(screen.lines())
    assert "Enter Open path · Esc Back" in text, screen.dump()
    assert "i Import" not in text and "s Skip" not in text and "b Back" not in text, screen.dump()
