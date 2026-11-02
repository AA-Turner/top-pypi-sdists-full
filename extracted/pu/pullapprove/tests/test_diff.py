from __future__ import annotations

import json
from pathlib import Path

from pullapprove.diff import (
    DiffCode,
    DiffFile,
    _unquote_git_path,
    filter_diff_text,
    iter_hunkless_files,
    iterate_diff_parts,
    parse_diff,
    parse_diff_file_line,
)

TWO_FILE_DIFF = (
    "diff --git a/uv.lock b/uv.lock\n"
    "index 1111111..2222222 100644\n"
    "--- a/uv.lock\n"
    "+++ b/uv.lock\n"
    "@@ -1,1 +1,1 @@\n"
    '-version = "1.0"\n'
    '+version = "1.1"\n'
    "diff --git a/core.py b/core.py\n"
    "index 3333333..4444444 100644\n"
    "--- a/core.py\n"
    "+++ b/core.py\n"
    "@@ -5,1 +5,1 @@ def f():\n"
    "-    value = compute_old()\n"
    "+    value = compute_new()\n"
)


def test_diff_hunk_context_line():
    # Technically there is a space missing here on the empty line
    diff = """diff --git a/LICENSE b/LICENSE
index fdddb29..314ba5d 100644
--- a/LICENSE
+++ b/LICENSE
@@ -6,7 +6,7 @@ binary, for any purpose, commercial or non-commercial, and by any
 means.

 In jurisdictions that recognize copyright laws, the author or authors
-of this software dedicate any and all copyright interest in the
+of this software dedicate any and all copyright interest! in the
 software to the public domain. We make this dedication for the benefit
 of the public at large and to the detriment of our heirs and
 successors. We intend this dedication to be an overt act of"""

    # Make sure the line with "binary" is seen
    lines = list(iterate_diff_parts(diff))

    # Filter down to the DiffCode objects so we can inspect the actual lines
    code_lines = [line for line in lines if isinstance(line, DiffCode)]

    # We should have parsed the trailing context that appears on the same
    # line as the hunk header ("binary, for any purpose ...")
    assert any(
        "binary, for any purpose" in code_line.content for code_line in code_lines
    ), "The first context line that trails the hunk header was not captured."


def test_blank_context_line_advances_counters():
    # Some hosts strip a blank context line's leading space, so it arrives as
    # a bare "" rather than " " — must still count as context on both sides
    # (matching file-contents.ts/review-state.ts on the client), not be
    # dropped and desync every line number after it.
    diff = (
        "diff --git a/a.py b/a.py\n"
        "--- a/a.py\n"
        "+++ a/a.py\n"
        "@@ -1,5 +1,5 @@\n"
        " first\n"
        "\n"
        "-old\n"
        "+new\n"
        " last\n"
    )

    (hunk,) = parse_diff(diff)[0].hunks

    assert [c.content for c in hunk.lines] == ["first", "", "old", "new", "last"]

    blank = hunk.lines[1]
    assert blank.content == ""
    assert (blank.old_line_number, blank.new_line_number) == (2, 2)

    # The line after the blank must have advanced past it on both sides, not
    # repeated the blank's numbers (which is what dropping it without
    # advancing the counters would produce).
    old_line = hunk.lines[2]
    assert (old_line.old_line_number, old_line.new_line_number) == (3, None)
    last = hunk.lines[4]
    assert (last.old_line_number, last.new_line_number) == (4, 4)


def test_parse_diff_groups_files_hunks_and_lines():
    diff = (
        "diff --git a/a.py b/a.py\n"
        "--- a/a.py\n"
        "+++ b/a.py\n"
        "@@ -1,2 +1,2 @@\n"
        " context\n"
        "-old\n"
        "+new\n"
        "@@ -10,1 +10,2 @@\n"
        "+added\n"
        "diff --git a/b.py b/b.py\n"
        "--- a/b.py\n"
        "+++ b/b.py\n"
        "@@ -1,1 +1,1 @@\n"
        "+only\n"
    )

    files = parse_diff(diff)

    assert [f.new_path for f in files] == ["a.py", "b.py"]
    # a.py has two hunks; b.py has one.
    assert [len(f.hunks) for f in files] == [2, 1]

    first_hunk = files[0].hunks[0]
    assert [c.content for c in first_hunk.lines] == ["context", "old", "new"]
    assert [c.content for c in first_hunk.changed_lines] == ["old", "new"]


def test_parse_diff_captures_header_lines():
    # Everything from `diff --git` through the last metadata line before the
    # first `@@` — verbatim, matching the client's headerLines (the file-level
    # trust hash is built from exactly these lines on both sides).
    files = parse_diff(TWO_FILE_DIFF)

    assert files[0].header_lines == [
        "diff --git a/uv.lock b/uv.lock",
        "index 1111111..2222222 100644",
        "--- a/uv.lock",
        "+++ b/uv.lock",
    ]
    assert files[1].header_lines == [
        "diff --git a/core.py b/core.py",
        "index 3333333..4444444 100644",
        "--- a/core.py",
        "+++ b/core.py",
    ]


def test_iter_hunkless_files_yields_only_hunkless():
    diff = (
        "diff --git a/renamed_old.py b/renamed_new.py\n"
        "similarity index 100%\n"
        "rename from renamed_old.py\n"
        "rename to renamed_new.py\n"
        "diff --git a/core.py b/core.py\n"
        "index 3333333..4444444 100644\n"
        "--- a/core.py\n"
        "+++ b/core.py\n"
        "@@ -5,1 +5,1 @@ def f():\n"
        "-    value = compute_old()\n"
        "+    value = compute_new()\n"
        "diff --git a/logo.bin b/logo.bin\n"
        "index 0f49c4a..4c2de3c 100644\n"
        "Binary files a/logo.bin and b/logo.bin differ\n"
    )

    files = list(iter_hunkless_files(diff))

    # The pure rename and the binary — never core.py, which has a hunk.
    assert [f.new_path for f in files] == ["renamed_new.py", "logo.bin"]
    # Header lines are complete by the time each file is yielded (the yield
    # happens at the next file boundary / end of input).
    assert files[0].header_lines == [
        "diff --git a/renamed_old.py b/renamed_new.py",
        "similarity index 100%",
        "rename from renamed_old.py",
        "rename to renamed_new.py",
    ]
    assert files[1].header_lines == [
        "diff --git a/logo.bin b/logo.bin",
        "index 0f49c4a..4c2de3c 100644",
        "Binary files a/logo.bin and b/logo.bin differ",
    ]


def test_parse_diff_keeps_trailing_context_containing_at_signs():
    # A section heading that itself contains `@@` must not truncate the context.
    diff = (
        "diff --git a/x.py b/x.py\n"
        "--- a/x.py\n"
        "+++ b/x.py\n"
        "@@ -1,2 +1,2 @@ def f():  # uses @@ marker\n"
        "-old\n"
        "+new\n"
    )

    (hunk,) = parse_diff(diff)[0].hunks

    assert hunk.lines[0].content == "def f():  # uses @@ marker"


def test_parse_diff_attaches_trailing_context_line_to_hunk():
    diff = (
        "diff --git a/LICENSE b/LICENSE\n"
        "--- a/LICENSE\n"
        "+++ b/LICENSE\n"
        "@@ -6,7 +6,7 @@ binary, for any purpose, commercial or non-commercial\n"
        "-of this software dedicate\n"
        "+of this software dedicate!\n"
    )

    files = parse_diff(diff)

    (hunk,) = files[0].hunks
    # The text trailing the hunk header is captured as the hunk's first line.
    assert "binary, for any purpose" in hunk.lines[0].content


def test_diff_binary_file():
    """Binary file markers and replacement characters in diff content don't cause issues."""
    diff = (
        "diff --git a/image.png b/image.png\n"
        "Binary files /dev/null and b/image.png differ\n"
        "diff --git a/README.md b/README.md\n"
        "index abc1234..def5678 100644\n"
        "--- a/README.md\n"
        "+++ b/README.md\n"
        "@@ -1,3 +1,3 @@\n"
        " hello\n"
        "-old line\n"
        "+new line\n"
        " world"
    )

    parts = list(iterate_diff_parts(diff))
    files = [p for p in parts if isinstance(p, DiffFile)]
    code_lines = [p for p in parts if isinstance(p, DiffCode)]

    assert len(files) == 2
    assert files[0].new_path == "image.png"
    assert files[1].new_path == "README.md"

    # The binary marker line is skipped; only README.md code lines are parsed
    assert len(code_lines) == 4
    assert any(c.content == "new line" and c.is_addition() for c in code_lines)


def test_diff_with_replacement_characters():
    """Lines containing Unicode replacement characters (from errors='replace') are handled."""
    diff = (
        "diff --git a/data.bin b/data.bin\n"
        "index 0000000..1111111 100644\n"
        "--- a/data.bin\n"
        "+++ b/data.bin\n"
        "@@ -0,0 +1,2 @@\n"
        "+\ufffd\ufffd\ufffd binary content\n"
        "+more \ufffd data"
    )

    parts = list(iterate_diff_parts(diff))
    code_lines = [p for p in parts if isinstance(p, DiffCode)]

    assert len(code_lines) == 2
    assert "\ufffd" in code_lines[0].content
    assert code_lines[0].is_addition()
    assert code_lines[1].is_addition()


def test_filter_diff_text_keep_all_is_identity():
    assert filter_diff_text(TWO_FILE_DIFF, lambda *_: True) == TWO_FILE_DIFF


def test_filter_diff_text_drop_all_is_empty():
    assert filter_diff_text(TWO_FILE_DIFF, lambda *_: False) == ""


def test_filter_diff_text_drops_whole_file_when_no_hunks_kept():
    # Keep only core.py; uv.lock's lone hunk is dropped, so its header goes too.
    result = filter_diff_text(TWO_FILE_DIFF, lambda path, *_: path == "core.py")

    assert "uv.lock" not in result
    assert result == (
        "diff --git a/core.py b/core.py\n"
        "index 3333333..4444444 100644\n"
        "--- a/core.py\n"
        "+++ b/core.py\n"
        "@@ -5,1 +5,1 @@ def f():\n"  # trailing context copied verbatim
        "-    value = compute_old()\n"
        "+    value = compute_new()\n"
    )


def test_filter_diff_text_partial_drop_emits_header_once():
    diff = (
        "diff --git a/a.py b/a.py\n"
        "index aaa..bbb 100644\n"
        "--- a/a.py\n"
        "+++ b/a.py\n"
        "@@ -1,1 +1,1 @@\n"
        "-drop_me\n"
        "+drop_me_too\n"
        "@@ -10,1 +10,1 @@\n"
        "-keep_me\n"
        "+keep_me_too\n"
    )

    # Drop the first hunk (new_line 1), keep the second (new_line 10).
    result = filter_diff_text(diff, lambda path, old, new: new == 10)

    assert result == (
        "diff --git a/a.py b/a.py\n"
        "index aaa..bbb 100644\n"
        "--- a/a.py\n"
        "+++ b/a.py\n"
        "@@ -10,1 +10,1 @@\n"
        "-keep_me\n"
        "+keep_me_too\n"
    )


def test_filter_diff_text_preserves_body_bytes_and_preamble():
    diff = (
        "commit deadbeef\n"  # preamble (e.g. from `git show`) passes through
        "Author: Someone\n"
        "\n"
        "diff --git a/f.txt b/f.txt\n"
        "--- a/f.txt\n"
        "+++ b/f.txt\n"
        "@@ -1,1 +1,1 @@\n"
        "-old\n"
        "+new\n"
        "\\ No newline at end of file\n"
    )

    assert filter_diff_text(diff, lambda *_: True) == diff


def test_filter_diff_text_keeps_files_without_hunks():
    # Binary, pure-rename, and mode-only changes have no @@ hunks to classify,
    # so they must pass through even when keep_hunk would drop everything.
    binary = (
        "diff --git a/logo.png b/logo.png\n"
        "Binary files a/logo.png and b/logo.png differ\n"
    )
    rename = (
        "diff --git a/a.txt b/b.txt\n"
        "similarity index 100%\n"
        "rename from a.txt\n"
        "rename to b.txt\n"
    )
    mode = "diff --git a/run.sh b/run.sh\nold mode 100644\nnew mode 100755\n"
    for diff in (binary, rename, mode):
        assert filter_diff_text(diff, lambda *_: False) == diff


def test_filter_diff_text_preserves_crlf_and_control_chars():
    crlf = (
        "diff --git a/x.txt b/x.txt\r\n"
        "--- a/x.txt\r\n"
        "+++ b/x.txt\r\n"
        "@@ -1,1 +1,1 @@\r\n"
        "-old\r\n"
        "+new\r\n"
    )
    assert filter_diff_text(crlf, lambda *_: True) == crlf

    # A form-feed inside body content must not be treated as a line break.
    formfeed = (
        "diff --git a/x.py b/x.py\n"
        "--- a/x.py\n"
        "+++ b/x.py\n"
        "@@ -1,1 +1,1 @@\n"
        "-a\x0cb\n"
        "+c\x0cd\n"
    )
    assert filter_diff_text(formfeed, lambda *_: True) == formfeed


def test_filter_diff_text_does_not_add_a_trailing_newline():
    no_newline = (
        "diff --git a/x.py b/x.py\n"
        "--- a/x.py\n"
        "+++ b/x.py\n"
        "@@ -1,1 +1,1 @@\n"
        "-old\n"
        "+new"  # no trailing newline on the final line
    )
    assert filter_diff_text(no_newline, lambda *_: True) == no_newline


def test_parse_diff_file_line_unquoted():
    file = parse_diff_file_line("diff --git a/src/main.py b/src/main.py")
    assert file is not None
    assert file.old_path == "src/main.py"
    assert file.new_path == "src/main.py"


def test_parse_diff_file_line_unquoted_path_with_space():
    # Git doesn't quote spaces, so a non-rename `a/PATH b/PATH` with a space
    # followed by a single-char dir (`Section 1/`) must not mis-split on the
    # greedy ` \w/` — that would corrupt new_path and route the change to the
    # wrong config/reviewers.
    file = parse_diff_file_line(
        "diff --git a/Section 1/report.py b/Section 1/report.py"
    )
    assert file is not None
    assert file.old_path == "Section 1/report.py"
    assert file.new_path == "Section 1/report.py"


def test_parse_diff_file_line_unquoted_rename_still_splits():
    # A rename names two different paths; the equal-name split declines and the
    # greedy fallback recovers old/new (no spaces -> unambiguous).
    file = parse_diff_file_line("diff --git a/old.py b/new.py")
    assert file is not None
    assert file.old_path == "old.py"
    assert file.new_path == "new.py"


def test_parse_diff_file_line_quoted_non_ascii():
    # git C-quotes a non-ASCII path (octal bytes, prefix inside the quotes).
    file = parse_diff_file_line(r'diff --git "a/caf\303\251.py" "b/caf\303\251.py"')
    assert file is not None
    assert file.old_path == "café.py"
    assert file.new_path == "café.py"


def test_parse_diff_file_line_short_octal_does_not_crash():
    # git emits exactly 3 octal digits, but arbitrary stdin might have a short run
    # (`\7y`); decoding must read only the octal digits, not raise from int(_, 8).
    file = parse_diff_file_line(r'diff --git "a/x\7y.py" "b/x\7y.py"')
    assert file is not None  # recognized as a header, no ValueError


def test_filter_diff_text_keeps_quoted_path_after_hidden_hunk():
    # A quoted (non-ASCII) header following a HIDDEN hunk must be recognized, or
    # the quoted file's real change gets swallowed into the dropped hunk's state.
    diff = (
        "diff --git a/uv.lock b/uv.lock\n"
        "@@ -1,1 +1,1 @@\n"
        '-version = "1.0"\n'
        '+version = "1.1"\n'
        'diff --git "a/caf\\303\\251.py" "b/caf\\303\\251.py"\n'
        '--- "a/caf\\303\\251.py"\n'
        '+++ "b/caf\\303\\251.py"\n'
        "@@ -1,1 +1,1 @@\n"
        "-real_old()\n"
        "+real_new()\n"
    )
    result = filter_diff_text(diff, lambda path, *_: path != "uv.lock")

    assert "real_new()" in result  # the real change survived
    assert 'version = "1.1"' not in result  # the lockfile hunk was hidden
    assert r'diff --git "a/caf\303\251.py"' in result  # header preserved verbatim


def test_parse_diff_file_line_quoted_then_bare_rename_strips_newline():
    # Git quotes each side independently: a rename from a non-ASCII name to a
    # plain one mixes a quoted and a bare token. Streamed lines keep their
    # trailing newline, which must never end up in the path.
    file = parse_diff_file_line('diff --git "a/caf\\303\\251.txt" b/plain.txt\n')
    assert file is not None
    assert file.old_path == "caf\u00e9.txt"
    assert file.new_path == "plain.txt"


def test_parse_diff_file_line_bare_with_space_then_quoted():
    # A bare name may contain spaces; the quoted second token marks the split.
    file = parse_diff_file_line('diff --git a/my file.py "b/my fil\\303\\251.py"')
    assert file is not None
    assert file.old_path == "my file.py"
    assert file.new_path == "my fil\u00e9.py"


def test_filter_diff_text_preserves_final_newline_when_last_hunk_dropped():
    diff = (
        "diff --git a/a.py b/a.py\n"
        "@@ -1,1 +1,1 @@\n"
        "-keep_old()\n"
        "+keep_new()\n"
        "@@ -5,1 +5,1 @@\n"
        "-drop_old()\n"
        "+drop_new()\n"
    )
    result = filter_diff_text(diff, lambda path, old, new: old == 1)

    assert result.endswith("+keep_new()\n")


def test_unquote_git_path_matches_client_on_shared_fixture():
    """Cross-runtime parity: the server's _unquote_git_path and the client's
    unquoteGitPath (file-contents.test.ts asserts the same fixture) must decode
    every git C-quoted path identically — otherwise a non-ASCII/quoted filename
    keys trust labels and the /file fetch under two different names. Mirrors the
    cyrb53 hash-parity fixture's shared-golden approach."""
    fixture = json.loads(
        (
            Path(__file__).resolve().parents[2]
            / "tests"
            / "fixtures"
            / "path_unquote_parity.json"
        ).read_text()
    )
    for case in fixture["cases"]:
        assert _unquote_git_path(case["quoted"]) == case["decoded"], case["quoted"]
