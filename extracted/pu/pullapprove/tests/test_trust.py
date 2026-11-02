"""Tests for static hunk classification.

The bulk of coverage is the `CASES` table below. To cover a new rule (or a new
edge case), add a `pytest.param(...)` row — no new test function needed.

Each case's `lines` use a one-char prefix DSL: ``+`` added, ``-`` removed, and a
leading space for context. Set ``new_file=True`` for brand-new-file hunks.
``expected`` is the single label string, or ``None`` when nothing should match.
"""

from __future__ import annotations

import pytest
from pullapprove.diff import (
    DiffCode,
    DiffFile,
    DiffHunk,
    iter_file_hunks,
    iter_hunkless_files,
)
from pullapprove.trust import trust_diff, trust_file_label, trust_label


def make_hunk(lines: list[str], *, new_file: bool = False) -> DiffHunk:
    # A brand-new file's hunk is `@@ -0,0 +1,N @@` in real git output: both the
    # old length AND the old line anchor are 0 (a mid-file pure insertion has
    # old_length 0 but a nonzero anchor).
    hunk = DiffHunk(
        old_line=0 if new_file else 1,
        old_length=0 if new_file else 1,
        new_line=1,
        new_length=1,
    )
    for spec in lines:
        change, content = spec[0], spec[1:]
        if change == "+":
            hunk.lines.append(
                DiffCode(
                    old_line_number=None,
                    new_line_number=1,
                    content=content,
                    change_type="+",
                )
            )
        elif change == "-":
            hunk.lines.append(
                DiffCode(
                    old_line_number=1,
                    new_line_number=None,
                    content=content,
                    change_type="-",
                )
            )
        else:  # leading space => context line
            hunk.lines.append(
                DiffCode(
                    old_line_number=1,
                    new_line_number=1,
                    content=content,
                    change_type="",
                )
            )
    return hunk


CASES = [
    # --- generated:lockfile (path-based) ---
    pytest.param(
        "uv.lock", ["+foo = 1"], False, "generated:lockfile", id="lockfile-uv"
    ),
    pytest.param(
        "a/b/yarn.lock", ["+x"], False, "generated:lockfile", id="lockfile-nested"
    ),
    pytest.param(
        "Cargo.lock",
        ["+# version info"],
        False,
        "generated:lockfile",
        id="lockfile-beats-comment",
    ),
    pytest.param("src/main.py", ["+x = 1"], False, None, id="not-lockfile"),
    # --- file:added-empty ---
    pytest.param(
        "pkg/__init__.py", [], True, "file:added-empty", id="empty-file-no-lines"
    ),
    pytest.param(
        "pkg/__init__.py",
        ["+", "+   ", "+"],
        True,
        "file:added-empty",
        id="empty-file-blank-lines",
    ),
    pytest.param(
        "pkg/__init__.py",
        ["+# a comment"],
        True,
        "comments:added",
        id="new-file-with-content-not-empty",
    ),
    pytest.param(
        "a.py", ["-old content"], False, None, id="emptied-existing-file-not-new"
    ),
    # --- formatting:whitespace ---
    pytest.param(
        "src/main.py",
        ["+", "+   ", "-  "],
        False,
        "formatting:whitespace",
        id="whitespace-blank-lines",
    ),
    pytest.param(
        "src/main.py",
        [" x = 1", "+  ", "+"],
        False,
        "formatting:whitespace",
        id="whitespace-context-ignored",
    ),
    pytest.param(
        "src/main.py", ["+", "+x = 1"], False, None, id="whitespace-with-content"
    ),
    # --- comments:* (line comments) ---
    pytest.param(
        "app.py", ["+# a", "+# b"], False, "comments:added", id="comments-added-py"
    ),
    pytest.param(
        "main.rs", ["+// a", "+// b"], False, "comments:added", id="comments-added-rs"
    ),
    pytest.param(
        "script.py",
        ["-# old", "-# older"],
        False,
        "comments:removed",
        id="comments-removed-py",
    ),
    pytest.param(
        "app.js",
        ["-// old", "+// new"],
        False,
        "comments:modified",
        id="comments-modified-js",
    ),
    # A real inline comment on a kept CODE language (shell) is still comment-only —
    # the whitespace guard keeps a glued `#` in a value from masquerading as one.
    pytest.param(
        "deploy.sh",
        ["-echo a  # old", "+echo a  # new"],
        False,
        "comments:modified",
        id="shell-inline-comment-modified",
    ),
    # Data/config formats aren't trusted for content: a YAML `#` can be a comment,
    # a value fragment (`url: …/#frag`), or literal text in a block scalar — too
    # ambiguous — so YAML is declined entirely and its churn stays visible.
    pytest.param(
        "config.yml", ["-# old", "+# new"], False, None, id="yaml-not-trusted"
    ),
    pytest.param(
        "config.yml",
        ["-url: https://x/#old", "+url: https://x/#new"],
        False,
        None,
        id="yaml-value-fragment-not-trusted",
    ),
    pytest.param(
        "app.js",
        ["+// note", "+const x = 1;"],
        False,
        None,
        id="comments-mixed-with-code",
    ),
    pytest.param(
        "file.xyz", ["+// note"], False, None, id="comments-unknown-extension"
    ),
    # --- comments:* (block comments) ---
    pytest.param(
        "app.js", ["+/* block */"], False, "comments:added", id="block-comment-added-js"
    ),
    pytest.param(
        "app.js",
        ["+/* start", "+   mid", "+   end */"],
        False,
        "comments:added",
        id="block-comment-multiline-js",
    ),
    pytest.param(
        "styles.css",
        ["-/* old */"],
        False,
        "comments:removed",
        id="block-comment-removed-css",
    ),
    # CSS has no `//` line comment: a `//` in a protocol-relative url() is a real
    # value, so a host change must NOT be hidden as a comment-only edit.
    pytest.param(
        "styles.css",
        [
            "-  background: url(//cdn.old/logo.png);",
            "+  background: url(//cdn.new/logo.png);",
        ],
        False,
        None,
        id="css-protocol-relative-url-not-comment",
    ),
    pytest.param(
        "index.html",
        ["+<!-- note -->"],
        False,
        "comments:added",
        id="block-comment-html",
    ),
    pytest.param(
        "index.html",
        ["+<!-- start", "+   mid", "+   end -->"],
        False,
        "comments:added",
        id="block-comment-multiline-html",
    ),
    pytest.param(
        "app.js",
        ["+/* c */", "+const x = 1;"],
        False,
        None,
        id="block-comment-mixed-with-code",
    ),
    # Opening a `/*` that never closes in the changed lines comments out the code
    # BELOW the hunk — a real change, not comment churn, so it must not be hidden.
    pytest.param(
        "app.js",
        ["+/* disabling this"],
        False,
        None,
        id="block-comment-unclosed-not-trusted",
    ),
    # --- formatting:line-length (wrap / unwrap) ---
    pytest.param(
        "app.ts",
        [
            "-const result = foo(bar, baz, qux);",
            "+const result =",
            "+  foo(bar, baz, qux);",
        ],
        False,
        "formatting:line-length",
        id="line-length-wrap",
    ),
    pytest.param(
        "app.ts",
        ["-const result =", "-  foo(bar, baz);", "+const result = foo(bar, baz);"],
        False,
        "formatting:line-length",
        id="line-length-unwrap",
    ),
    pytest.param(
        "app.ts",
        ["-const result = foo(bar, baz);", "+const result = foo(bar, qux);"],
        False,
        None,
        id="line-length-real-change",
    ),
    # A wrap that ALSO edits content (baz -> qux) is not a neutral reflow: the
    # joined text differs, so it stays visible.
    pytest.param(
        "app.ts",
        ["-const result = foo(bar, baz);", "+const result =", "+  foo(bar, qux);"],
        False,
        None,
        id="line-length-wrap-with-content-change",
    ),
    # A newline is a record separator in data formats, so merging two CSV rows is a
    # real change, not a reflow — _line_length must not run on non-code formats.
    pytest.param(
        "data.csv",
        ["-a,b,", "-c,d", "+a,b, c,d"],
        False,
        None,
        id="line-length-csv-row-merge-not-reflow",
    ),
    # A reflow that ALSO dedents the statement (indent 8 -> 4) is a Python block-
    # scope change, not a neutral wrap — the first line's indent must be preserved.
    pytest.param(
        "app.py",
        ["-        x = foo(a, b)", "+    x = foo(a,", "+        b)"],
        False,
        None,
        id="py-reflow-dedent-not-line-length",
    ),
    # A "reflow" whose join lands INSIDE a multi-line string changes the string's
    # value (interior newline <-> space), so it must not be hidden as a wrap.
    pytest.param(
        "q.py",
        [
            '-query = """SELECT name,',
            '-email FROM users"""',
            '+query = """SELECT name, email FROM users"""',
        ],
        False,
        None,
        id="line-length-must-not-splice-triple-quote-string",
    ),
    pytest.param(
        "a.ts",
        [
            "-const s = `Dear user, code 12345`;",
            "+const s = `Dear user,",
            "+code 12345`;",
        ],
        False,
        None,
        id="line-length-must-not-split-template-literal",
    ),
    # --- formatting:style (semicolons / quotes / trailing commas) ---
    pytest.param(
        "app.ts",
        ["-const x = 1", "+const x = 1;"],
        False,
        "formatting:style",
        id="style-semicolon",
    ),
    # A trailing `;` is still stylistic when the next line starts a fresh statement.
    pytest.param(
        "app.ts",
        ["-const x = 1", "+const x = 1;", " const y = 2;"],
        False,
        "formatting:style",
        id="style-semicolon-safe-next-line",
    ),
    # ...but NOT when the next line starts with `(` — under ASI, adding the `;`
    # splits `foo(bar).baz()` into two statements, a real behavior change.
    pytest.param(
        "app.ts",
        ["-const value = foo", "+const value = foo;", " (bar).baz()"],
        False,
        None,
        id="style-asi-semicolon-not-stylistic",
    ),
    # A following regex/division line (leading `/`) is also an ASI continuation, so
    # dropping the `;` before it changes meaning (`a = b / hi / g.exec(c)`).
    pytest.param(
        "app.ts",
        ["-a = b;", "+a = b", " /hi/g.exec(c)"],
        False,
        None,
        id="style-asi-regex-not-stylistic",
    ),
    # A following comment line (`//`) is inert — the `;` stays stylistic.
    pytest.param(
        "app.ts",
        ["-const x = 1", "+const x = 1;", " // a comment"],
        False,
        "formatting:style",
        id="style-semicolon-comment-next-line-ok",
    ),
    # ASI ignores blank lines, so a blank line between the statement and its `(`
    # continuation still merges under ASI — the `;` change must stay visible.
    pytest.param(
        "app.ts",
        [
            "-const handler = makeHandler;",
            "+const handler = makeHandler",
            " ",
            " (init())()",
        ],
        False,
        None,
        id="style-asi-semicolon-across-blank-line",
    ),
    # Only blank lines visible after the change: the statement ASI would merge
    # with sits past the context window, so the `;` can't be proven inert —
    # decline. (A hunk ENDING on the change is EOF and stays stylistic — see
    # style-semicolon above.)
    pytest.param(
        "app.ts",
        [
            "-const a = getThing();",
            "+const a = getThing()",
            " ",
            " ",
            " ",
        ],
        False,
        None,
        id="style-asi-follower-past-context-window",
    ),
    pytest.param(
        "app.js",
        ["-const x = 'hello'", '+const x = "hello"'],
        False,
        "formatting:style",
        id="style-quote",
    ),
    pytest.param(
        "app.ts",
        ["-  foo: 'bar'", "+  foo: 'bar',"],
        False,
        "formatting:style",
        id="style-trailing-comma",
    ),
    pytest.param(
        "app.ts",
        ["-const x = 1;", "+const x = 2;"],
        False,
        None,
        id="style-real-change",
    ),
    pytest.param(
        "app.ts",
        ["-const x = 1", "+const x = 1;", "+const y = 2;"],
        False,
        None,
        id="style-different-line-count",
    ),
    # A trailing comma is stylistic in JS/TS (an array/arg list), so it collapses.
    pytest.param(
        "app.ts",
        ["-const a = [1, 2,]", "+const a = [1, 2]"],
        False,
        "formatting:style",
        id="style-trailing-comma-ts-collapses",
    ),
    # ...but in Python a trailing comma builds a TUPLE — a real value-type change
    # that must NOT be hidden as style (end of line, before `)`, and in a subscript).
    pytest.param(
        "app.py",
        ["-x = 1,", "+x = 1"],
        False,
        None,
        id="py-bare-trailing-comma-is-tuple",
    ),
    pytest.param(
        "app.py",
        ["-x = (a,)", "+x = (a)"],
        False,
        None,
        id="py-paren-trailing-comma-is-tuple",
    ),
    pytest.param(
        "app.py",
        ["-d[k,]", "+d[k]"],
        False,
        None,
        id="py-subscript-trailing-comma-is-tuple",
    ),
    # --- Review-evasion regressions: a real change must never hide behind a
    # trivial token delta. The tokenizer drops comments, so a directive change
    # under cover of a quote swap must be declined (left for _comments), and a
    # runtime-active annotation (a call: Depends/Field/validators) is not an
    # erasable type edit.
    pytest.param(
        "a.py",
        ["-x = 'a'  # noqa: E501", '+x = "a"'],
        False,
        None,
        id="style-must-not-hide-noqa-removal",
    ),
    pytest.param(
        "a.py",
        ["-x = 'a'  # type: ignore[foo]", '+x = "a"  # type: ignore[bar]'],
        False,
        None,
        id="style-must-not-hide-type-ignore-change",
    ),
    pytest.param(
        "a.ts",
        [
            "-let x = 'a' /* eslint-disable no-eval */",
            '+let x = "a" /* eslint-disable */',
        ],
        False,
        None,
        id="style-must-not-hide-eslint-directive",
    ),
    pytest.param(
        "v.py",
        [
            "-def f(u: Annotated[User, Depends(require_admin)]): pass",
            "+def f(u: Annotated[User, Depends(require_login)]): pass",
        ],
        False,
        None,
        id="annotation-must-not-hide-depends-swap",
    ),
    pytest.param(
        "m.py",
        [
            "-limit: Annotated[int, Field(le=1000)] = 100",
            "+limit: Annotated[int, Field(le=100000)] = 100",
        ],
        False,
        None,
        id="annotation-must-not-hide-field-validator",
    ),
    # `//` is floor division in Python, not a comment — a quote swap on the same
    # line must not let the ts-lexer drop the divisor change (2 -> 4).
    pytest.param(
        "app.py",
        ["-msg = 'hi'; n = x // 2", '+msg = "hi"; n = x // 4'],
        False,
        None,
        id="py-floordiv-not-hidden-by-style",
    ),
    # --- footgun audit: trivial-looking edits that are actually semantic ---
    # A bare trailing comma makes a tuple even after a keyword.
    pytest.param(
        "app.py", ["-return a,", "+return a"], False, None, id="py-return-tuple"
    ),
    # `:=` (walrus) is not a type-annotation colon — a renamed target is a real edit.
    pytest.param(
        "app.py",
        ["-if (n := f()):", "+if (m := f()):"],
        False,
        None,
        id="py-walrus-not-annotation",
    ),
    # An f-string interpolation change is a value change, not a quote-style edit.
    pytest.param(
        "app.py",
        ["-msg = f'{a}'", "+msg = f'{b}'"],
        False,
        None,
        id="py-fstring-interp-change",
    ),
    # A TypeScript `as` cast target change is semantic, not style.
    pytest.param(
        "app.ts",
        ["-const x = y as A", "+const x = y as B"],
        False,
        None,
        id="ts-as-cast-change",
    ),
    # Removing optional chaining (`?.` -> `.`) changes null-handling behavior.
    pytest.param(
        "app.ts", ["-a?.b", "+a.b"], False, None, id="ts-optional-chaining-change"
    ),
    # A regex literal must not be mislexed as a comment/style token (flag g -> i).
    pytest.param(
        "app.js",
        ["-const r = /a/g", "+const r = /a/i"],
        False,
        None,
        id="js-regex-change",
    ),
    # --- imports:* ---
    pytest.param(
        "app.ts",
        ["+import { Foo } from './foo';"],
        False,
        "imports:added",
        id="import-added-ts",
    ),
    # A dynamic `import(...)` call is executable code, not a static import.
    pytest.param(
        "app.ts", ['+import ("./setup");'], False, None, id="dynamic-import-not-import"
    ),
    pytest.param(
        "main.py",
        ["-import os", "-from sys import argv"],
        False,
        "imports:removed",
        id="import-removed-py",
    ),
    pytest.param(
        "lib.rs",
        ["+use std::collections::HashMap;"],
        False,
        "imports:added",
        id="import-rust-use",
    ),
    pytest.param(
        "main.c", ["+#include <stdio.h>"], False, "imports:added", id="import-c-include"
    ),
    pytest.param(
        "index.js",
        [
            "-import { b } from './b';",
            "-import { a } from './a';",
            "+import { a } from './a';",
            "+import { b } from './b';",
        ],
        False,
        "imports:reordered",
        id="import-reorder-js",
    ),
    pytest.param(
        "index.js",
        ["-import { a } from './a';", "+import { b } from './b';"],
        False,
        None,
        id="import-modified-js-source-swap-not-trusted",
    ),
    pytest.param(
        "index.js",
        ["-import { a } from './a';", "+import { a, b } from './a';"],
        False,
        "imports:modified",
        id="import-modified-js-same-source",
    ),
    pytest.param(
        "main.py",
        ["-from foo import bar", "+from evil import bar"],
        False,
        None,
        id="import-modified-py-source-swap-not-trusted",
    ),
    pytest.param(
        "main.c",
        ['-#include "config.h"', '+#include "evil.h"'],
        False,
        None,
        id="import-modified-c-source-swap-not-trusted",
    ),
    # A module/target swap must not be trusted even in a language we can't split
    # into module-vs-names — `require` executes the target file, so swapping it
    # is a full code swap, not import churn.
    pytest.param(
        "app.rb",
        ["-require 'safe'", "+require 'evil'"],
        False,
        None,
        id="import-modified-rb-source-swap-not-trusted",
    ),
    # A reorder of the exact same #include set is still not trusted — order
    # can be load-bearing for macros/typedefs/conditional compilation.
    pytest.param(
        "main.c",
        [
            '-#include "a.h"',
            '-#include "b.h"',
            '+#include "b.h"',
            '+#include "a.h"',
        ],
        False,
        None,
        id="import-reorder-c-never-trusted",
    ),
    # A reorder that includes a bare JS/TS side-effect import is not trusted —
    # its only purpose is running top-level code, and that can be order-
    # dependent even though the same two files are still both imported.
    pytest.param(
        "index.js",
        ["-import './b';", "-import './a';", "+import './a';", "+import './b';"],
        False,
        None,
        id="import-reorder-js-side-effect-not-trusted",
    ),
    pytest.param(
        "app.ts",
        ["+import { Foo } from './foo';", "+const x = new Foo();"],
        False,
        None,
        id="import-mixed-with-code",
    ),
    # --- imports:* (multi-line) ---
    pytest.param(
        "main.py",
        ["+from plain.models import (", "+    query_utils,", "+    sql,", "+)"],
        False,
        "imports:added",
        id="import-py-multiline",
    ),
    pytest.param(
        "app.tsx",
        ["+import {", "+  useState,", "+  useEffect,", '+} from "react";'],
        False,
        "imports:added",
        id="import-ts-multiline",
    ),
    pytest.param(
        "lib.rs",
        ["+use std::collections::{", "+    HashMap,", "+    HashSet,", "+};"],
        False,
        "imports:added",
        id="import-rust-multiline",
    ),
    pytest.param(
        "main.go",
        ["+import (", '+    "fmt"', '+    "os"', "+)"],
        False,
        "imports:added",
        id="import-go-multiline",
    ),
    pytest.param(
        "main.py",
        [
            "-from plain.models import (",
            "-    query_utils,",
            "-    sql,",
            "-    transaction,",
            "-)",
            "+from plain.models import query_utils, transaction",
        ],
        False,
        "imports:modified",
        id="import-py-multiline-modified",
    ),
    pytest.param(
        "main.py",
        ["+from os import (", "+    path,", "+)", "+x = path.join('a', 'b')"],
        False,
        None,
        id="import-multiline-not-mixed-with-code",
    ),
    # --- comments:* (inline comments — code identical, only the comment changed) ---
    pytest.param(
        "app.py",
        ["-    x = get_value()", "+    x = get_value()  # TODO"],
        False,
        "comments:added",
        id="inline-comment-added-py",
    ),
    pytest.param(
        "app.py",
        ["-    foo()  # obvious note", "+    foo()"],
        False,
        "comments:removed",
        id="inline-comment-removed-py",
    ),
    # Directive comments steer tools — removing a `type: ignore` comment
    # re-enables the type checker on that line, a real change, never comment churn.
    pytest.param(
        "app.py",
        ["-    foo()  # type: ignore", "+    foo()"],
        False,
        None,
        id="inline-directive-comment-declined",
    ),
    # The canonical doctest directive — controls test collection, not prose.
    pytest.param(
        "app.py",
        ["-    >>> foo()  # doctest: +SKIP", "+    >>> foo()"],
        False,
        None,
        id="inline-directive-comment-doctest-declined",
    ),
    pytest.param(
        "app.py",
        ["-    foo()  # pylint: disable=no-member", "+    foo()"],
        False,
        None,
        id="inline-directive-comment-pylint-declined",
    ),
    pytest.param(
        "app.py",
        ["-    foo()  # nopep8", "+    foo()"],
        False,
        None,
        id="inline-directive-comment-nopep8-declined",
    ),
    pytest.param(
        "app.py",
        ["-    foo()  # skipcq: PYL-W0612", "+    foo()"],
        False,
        None,
        id="inline-directive-comment-skipcq-declined",
    ),
    pytest.param(
        "app.py",
        ["-    foo()  # pyre-ignore[6]", "+    foo()"],
        False,
        None,
        id="inline-directive-comment-pyre-ignore-declined",
    ),
    pytest.param(
        "app.py",
        ["-    foo()  # pyre-fixme[6]", "+    foo()"],
        False,
        None,
        id="inline-directive-comment-pyre-fixme-declined",
    ),
    pytest.param(
        "app.py",
        ["-    foo()  # pytype: disable=attribute-error", "+    foo()"],
        False,
        None,
        id="inline-directive-comment-pytype-declined",
    ),
    pytest.param(
        "app.py",
        ["-x = format(y)  # yapf: disable", "+x = format(y)"],
        False,
        None,
        id="inline-directive-comment-yapf-declined",
    ),
    pytest.param(
        "app.js",
        ["-const x = 1; // old reason", "+const x = 1; // new reason"],
        False,
        "comments:modified",
        id="inline-comment-modified-js",
    ),
    pytest.param(
        "app.py",
        ['-    x = "foo # bar"', '+    x = "foo # baz"'],
        False,
        None,
        id="inline-comment-hash-in-string",
    ),
    pytest.param(
        "app.py",
        ["-    x = old_value()  # comment", "+    x = new_value()"],
        False,
        None,
        id="inline-comment-code-also-changed",
    ),
    # --- type-annotations:modified (Python + TypeScript) ---
    pytest.param(
        "app.py",
        ["-def greet(name):", "+def greet(name: str):"],
        False,
        "type-annotations:modified",
        id="type-anno-py-param",
    ),
    pytest.param(
        "app.py",
        ["-def greet(name):", "+def greet(name) -> str:"],
        False,
        "type-annotations:modified",
        id="type-anno-py-return",
    ),
    pytest.param(
        "app.ts",
        ["-const x = 1", "+const x: number = 1"],
        False,
        "type-annotations:modified",
        id="type-anno-ts-var",
    ),
    pytest.param(
        "app.py",
        ["-x: Dict[str, int] = {}", "+x: Dict[str, str] = {}"],
        False,
        "type-annotations:modified",
        id="type-anno-py-generic",
    ),
    pytest.param(
        "app.ts",
        ["-function f(a: number) {}", "+function f(a: string) {}"],
        False,
        "type-annotations:modified",
        id="type-anno-ts-function-param",
    ),
    pytest.param(
        "app.rs",
        ["-let x = 1;", "+let x: i32 = 1;"],
        False,
        None,
        id="type-anno-unsupported-ext",
    ),
    pytest.param(
        "app.py",
        ["-def greet(name):", "+def hello(name: str):"],
        False,
        None,
        id="type-anno-real-change",
    ),
    pytest.param(
        "app.py",
        ["+def greet(name: str) -> str:"],
        False,
        None,
        id="type-anno-additions-only",
    ),
    pytest.param(
        "app.py",
        [
            '-            DB_NAMESPACE: db.settings_dict.get("NAME"),',
            '+            DB_NAMESPACE: db.settings_dict.get("DATABASE"),',
        ],
        False,
        None,
        id="type-anno-dict-call-value",
    ),
    pytest.param(
        "app.py",
        ['-    "key": old_value,', '+    "key": new_value,'],
        False,
        None,
        id="type-anno-dict-string-key",
    ),
    # --- false positives that must NOT be trusted (real changes in disguise) ---
    pytest.param(
        "app.ts",
        ["-const o = { enabled: false }", "+const o = { enabled: true }"],
        False,
        None,
        id="fp-ts-object-value-not-annotation",
    ),
    pytest.param(
        "app.py",
        ["-d = {KEY: old}", "+d = {KEY: new}"],
        False,
        None,
        id="fp-py-dict-bare-key-not-annotation",
    ),
    pytest.param(
        "app.py",
        ["-    KEY: old_value,", "+    KEY: new_value,"],
        False,
        None,
        id="fp-py-multiline-dict-entry-not-annotation",
    ),
    pytest.param(
        "app.ts",
        ["-  enabled: false,", "+  enabled: true,"],
        False,
        None,
        id="fp-ts-multiline-object-entry-not-annotation",
    ),
    pytest.param(
        "app.py",
        ['-x = "a  b"', '+x = "a b"'],
        False,
        None,
        id="fp-string-whitespace-not-formatting",
    ),
    pytest.param(
        "app.js",
        ["-x = 'a  b'", "+x = 'a b'"],
        False,
        None,
        id="fp-string-whitespace-not-style",
    ),
    pytest.param(
        "app.js",
        ["-const url = `http://old.com`;", "+const url = `http://new.com`;"],
        False,
        None,
        id="fp-template-literal-not-comment",
    ),
    pytest.param(
        "app.js",
        ["+/* note */ doThing()"],
        False,
        None,
        id="fp-code-after-block-comment",
    ),
    pytest.param(
        "app.js",
        ['+import x from "x"; doThing()'],
        False,
        None,
        id="fp-import-with-trailing-code-js",
    ),
    pytest.param(
        "app.py",
        ["+import os; do_thing()"],
        False,
        None,
        id="fp-import-with-trailing-code-py",
    ),
    # --- conservative guards for classifier false positives (from Codex review) ---
    # A ternary's false branch changing must not read as a TS type-annotation change.
    pytest.param(
        "app.ts",
        ["-const v = flag ? a : b", "+const v = flag ? a : c"],
        False,
        None,
        id="ternary-false-branch-not-annotation",
    ),
    # A lambda body changing must not read as a Python type-annotation change.
    pytest.param(
        "app.py",
        ["-f = lambda x: old_value", "+f = lambda x: new_value"],
        False,
        None,
        id="lambda-body-not-annotation",
    ),
    pytest.param(
        "app.py",
        ["-sorted(xs, key=lambda x: x.a)", "+sorted(xs, key=lambda x: x.b)"],
        False,
        None,
        id="lambda-in-call-not-annotation",
    ),
    # go.mod is the editable manifest (not a generated lockfile); go.sum is.
    pytest.param(
        "go.mod",
        ["+\trequire example.com/foo v1.2.3"],
        False,
        None,
        id="go-mod-not-lockfile",
    ),
    pytest.param(
        "go.sum",
        ["+example.com/foo v1.2.3 h1:abcdef="],
        False,
        "generated:lockfile",
        id="go-sum-still-lockfile",
    ),
    # A trailing statement on a multi-line import's closing line is executable
    # code that must not be hidden as import churn.
    pytest.param(
        "app.ts",
        ["+import {", "+  foo,", "+} from './foo'; doThing();"],
        False,
        None,
        id="import-closing-trailing-statement",
    ),
    # A quote *character* inside a string value flipping is a semantic change,
    # not a quote-style change.
    pytest.param(
        "app.ts",
        ["-const sep = '\"'", '+const sep = "\'"'],
        False,
        None,
        id="quote-char-in-string-not-style",
    ),
    # --- annotation false positives (from the second Codex review) ---
    # A one-line compound-statement suite colon is not a type annotation.
    pytest.param(
        "app.py",
        ["-if flag: return old", "+if flag: return new"],
        False,
        None,
        id="py-suite-colon-not-annotation",
    ),
    pytest.param(
        "app.py",
        ["-while cond: step(old)", "+while cond: step(new)"],
        False,
        None,
        id="py-while-suite-not-annotation",
    ),
    # A colon inside a (multi-line) dict is a data entry, not an annotation.
    pytest.param(
        "app.py",
        [
            "-config = {",
            "-    KEY: old_value,",
            "-}",
            "+config = {",
            "+    KEY: new_value,",
            "+}",
        ],
        False,
        None,
        id="py-dict-entry-not-annotation",
    ),
    # A TypeScript switch/case label colon is not a type annotation.
    pytest.param(
        "app.ts",
        ["-case Foo: return old", "+case Foo: return new"],
        False,
        None,
        id="ts-case-label-not-annotation",
    ),
    # A TypeScript object-literal value (no declaration context) is not an annotation.
    pytest.param(
        "app.ts",
        ["-  enabled: false", "+  enabled: true"],
        False,
        None,
        id="ts-object-value-not-annotation",
    ),
    # A parameter DEFAULT-value change must not be swallowed by the annotation span.
    pytest.param(
        "app.py",
        ["-def connect(timeout: int = 30):", "+def connect(timeout: int = 5):"],
        False,
        None,
        id="py-param-default-change-not-annotation",
    ),
    pytest.param(
        "app.ts",
        ["-function f(a: number = 1) {}", "+function f(a: number = 2) {}"],
        False,
        None,
        id="ts-param-default-change-not-annotation",
    ),
    # ...but changing only the TYPE (default unchanged) IS a trusted annotation edit.
    pytest.param(
        "app.py",
        ["-def f(a: int = 1):", "+def f(a: str = 1):"],
        False,
        "type-annotations:modified",
        id="py-param-type-change-with-default",
    ),
    # A bare `NAME: X` (no `=`) is ambiguous — a type decl vs a dict entry whose
    # `{` opened on a prior line — so it is never stripped (could hide a value).
    pytest.param(
        "app.py",
        ["-    retries: DEFAULT_RETRIES", "+    retries: FALLBACK_RETRIES"],
        False,
        None,
        id="py-bare-colon-not-stripped",
    ),
    # --- style only where ';'/','/quote-delimiter are non-semantic ---
    # A trailing comma in a data file (CSV) is content, not style.
    pytest.param(
        "data.csv",
        ["-id,name,", "+id,name"],
        False,
        None,
        id="style-not-on-data-file",
    ),
    # A quote change in a Go char literal ('a' rune vs "a" string) is semantic.
    pytest.param(
        "main.go",
        ["-const c = 'a'", '+const c = "a"'],
        False,
        None,
        id="style-not-on-non-interchangeable-quotes",
    ),
    # --- a bare export list is a public-API change, not import churn ---
    pytest.param(
        "app.ts",
        ["-export { Foo };", "+export { Foo, Bar };"],
        False,
        None,
        id="export-list-is-api-not-import",
    ),
    # --- semantic-newline / indentation guards (third Codex review) ---
    # A Python indentation (dedent) change is semantic, not a style edit.
    pytest.param(
        "app.py",
        ["-        return 1", "+    return 1"],
        False,
        None,
        id="py-indent-not-style",
    ),
    # ...but a same-indent quote-style change is still trusted.
    pytest.param(
        "app.py",
        ["-    x = 'a'", '+    x = "a"'],
        False,
        "formatting:style",
        id="py-quote-style-same-indent",
    ),
    # Joining two statements across a newline (no bracket/continuation) is NOT a
    # reflow — the newline is semantic (Python suite, JS ASI).
    pytest.param(
        "app.py",
        ["-    return", "-    value", "+    return value"],
        False,
        None,
        id="py-statement-join-not-line-length",
    ),
    pytest.param(
        "app.js",
        ["-  return", "-  value", "+  return value"],
        False,
        None,
        id="js-asi-join-not-line-length",
    ),
    # A dedent of a commented code line is a real (indent) change, not a
    # comment-only edit.
    pytest.param(
        "app.py",
        ["-        do()  # note", "+    do()  # note"],
        False,
        None,
        id="py-comment-line-dedent-not-comment",
    ),
    # A multi-line import whose members CHANGE is modified, not reordered.
    pytest.param(
        "app.ts",
        [
            "-import {",
            "-  A,",
            "-} from './x';",
            "+import {",
            "+  B,",
            "+} from './x';",
        ],
        False,
        "imports:modified",
        id="multiline-import-modified-not-reordered",
    ),
    # --- no changed lines / unclassified ---
    pytest.param("src/main.py", [" just context"], False, None, id="no-changed-lines"),
    pytest.param(
        "src/main.py",
        ["+def real():", "+    return 1"],
        False,
        None,
        id="real-code-unlabeled",
    ),
    # --- default-deny regressions: real changes that once classified as trivial ---
    # A value change in a one-line def body: the dict colon is NOT a param
    # annotation (the params already closed).
    pytest.param(
        "config.py",
        [
            '-def default(): return {"timeout": 30}',
            '+def default(): return {"timeout": 60}',
        ],
        False,
        None,
        id="py-one-line-def-body-value-not-annotation",
    ),
    # A rename in a multi-declarator let: the second declarator's name is not
    # part of the first's annotation span.
    pytest.param(
        "app.ts",
        ["-let x: number, oldName: string", "+let x: number, newName: string"],
        False,
        None,
        id="ts-multi-declarator-rename-not-annotation",
    ),
    # A statement MOVED across a context line plus a quote swap is not style —
    # execution order changed.
    pytest.param(
        "app.py",
        ["-x = 'a'", " do_something()", '+x = "a"'],
        False,
        None,
        id="style-move-across-context-declined",
    ),
    # Commenting OUT live context code: the block opened on an added line
    # swallows the unchanged statement between the added lines.
    pytest.param(
        "app.js",
        ["+/* start", " existingCode();", "+end */"],
        False,
        None,
        id="comment-out-live-context-code-declined",
    ),
    # A change to a triple-quoted string's VALUE is not a comment change — the
    # apostrophe inside must not desync the scanner.
    pytest.param(
        "app.py",
        ["-x = '''don't # old'''", "+x = '''don't # new'''"],
        False,
        None,
        id="py-triple-quote-hash-is-not-comment",
    ),
    # Deletions bracketing a context line is a move, not a reflow.
    pytest.param(
        "app.py",
        ["-x = f(a,", " ctx()", "-    b)", "+x = f(a, b)"],
        False,
        None,
        id="line-length-across-context-declined",
    ),
    # Blank lines are semantic in markup/data — no whitespace label outside the
    # validated code languages.
    pytest.param("README.md", ["-", " text"], False, None, id="whitespace-md-declined"),
    pytest.param("config.yml", ["+"], False, None, id="whitespace-yaml-declined"),
    # Reordering a __future__ import breaks the module at import time.
    pytest.param(
        "app.py",
        [
            "-from __future__ import annotations",
            "-import os",
            "+import os",
            "+from __future__ import annotations",
        ],
        False,
        None,
        id="future-import-reorder-declined",
    ),
    # --- shebangs & tool-directive comments (comment syntax, tool semantics) ---
    # A `#!` on line 1 selects the interpreter — an execution change. (make_hunk
    # numbers every line 1; a mid-file `#!` is covered by a standalone test.)
    pytest.param(
        "run.sh", ["-#!/bin/bash", "+#!/bin/sh"], False, None, id="sh-shebang-declined"
    ),
    pytest.param(
        "run.py",
        ["-#!/usr/bin/env python2", "+#!/usr/bin/env python3"],
        False,
        None,
        id="py-shebang-declined",
    ),
    # Removing a linter suppression changes what the linter enforces.
    pytest.param(
        "app.py",
        ["-x = f()  # noqa: E501", "+x = f()"],
        False,
        None,
        id="py-noqa-removed-declined",
    ),
    # Narrowing/widening a type-checker escape is a type-checking change.
    pytest.param(
        "app.py",
        ["-x = f()  # type: ignore", "+x = f()  # type: ignore[arg-type]"],
        False,
        None,
        id="py-type-ignore-changed-declined",
    ),
    pytest.param(
        "app.ts",
        ["+// @ts-ignore", " broken();"],
        False,
        None,
        id="ts-ignore-added-declined",
    ),
    pytest.param(
        "app.ts",
        ["-// eslint-disable-next-line no-eval", " eval(x);"],
        False,
        None,
        id="eslint-disable-removed-declined",
    ),
    pytest.param(
        "app.py",
        ["-# pragma: no cover", " def f():"],
        False,
        None,
        id="py-pragma-removed-declined",
    ),
    pytest.param(
        "main.go",
        ["+//go:generate mockgen", " package main"],
        False,
        None,
        id="go-directive-added-declined",
    ),
    # ...but ordinary prose comments are still comment churn.
    pytest.param(
        "app.py",
        ["-# helper", "+# helper for parsing"],
        False,
        "comments:modified",
        id="py-prose-comment-still-trusted",
    ),
    # --- a join must not drag code into a line comment ---
    # Unwrapping moves `baz)` INTO the `// why` comment: the joined texts compare
    # equal, but the new line comments the argument out.
    pytest.param(
        "app.js",
        ["-foo(bar, // why", "-    baz);", "+foo(bar, // why baz);"],
        False,
        None,
        id="js-unwrap-into-line-comment-declined",
    ),
    pytest.param(
        "app.py",
        ["-foo(bar,  # why", "-    baz)", "+foo(bar,  # why baz)"],
        False,
        None,
        id="py-unwrap-into-line-comment-declined",
    ),
    # A comment on the FINAL line swallows nothing — still a neutral reflow.
    pytest.param(
        "app.js",
        ["-foo(bar,", "-    baz); // note", "+foo(bar, baz); // note"],
        False,
        "formatting:line-length",
        id="js-unwrap-final-line-comment-ok",
    ),
    # A `//` inside a string is not a comment — the reflow stays neutral.
    pytest.param(
        "app.js",
        [
            "-const u = fetch('http://x',",
            "-    opts);",
            "+const u = fetch('http://x', opts);",
        ],
        False,
        "formatting:line-length",
        id="js-url-in-string-reflow-ok",
    ),
    # --- formatting:spacing (tokens identical, only whitespace moved) ---
    pytest.param(
        "app.py", ["-x=1", "+x = 1"], False, "formatting:spacing", id="py-op-spacing"
    ),
    pytest.param(
        "app.py",
        ["-x = 1  ", "+x = 1"],
        False,
        "formatting:spacing",
        id="py-trailing-whitespace-trim",
    ),
    pytest.param(
        "app.ts",
        ["-const x = f( a, b );", "+const x = f(a, b);"],
        False,
        "formatting:spacing",
        id="ts-paren-padding",
    ),
    # Whitespace before a trailing comment is still just spacing...
    pytest.param(
        "app.py",
        ["-x = 1  # note", "+x = 1 # note"],
        False,
        "formatting:spacing",
        id="py-space-before-comment-is-spacing",
    ),
    # ...but a change to the comment itself is _comments' call, not spacing.
    pytest.param(
        "app.py",
        ["-x = 1  # a", "+x = 1  # b"],
        False,
        "comments:modified",
        id="py-comment-edit-not-spacing",
    ),
    # Whitespace inside a string literal is a value change.
    pytest.param(
        "app.py",
        ["-x = 'a  b'", "+x = 'a b'"],
        False,
        None,
        id="py-string-interior-ws-declined",
    ),
    # Regrouping punctuation is semantic even though the token texts match.
    pytest.param(
        "app.js", ["-a + +b", "+a ++ b"], False, None, id="js-op-regroup-declined"
    ),
    pytest.param(
        "app.py", ["-a ** b", "+a * * b"], False, None, id="py-op-regroup-declined"
    ),
    # Gluing a word to a string makes an f-string — not spacing.
    pytest.param(
        "app.py", ["-f 'x'", "+f'x'"], False, None, id="py-string-prefix-glue-declined"
    ),
    # A mid-line block comment sits in a token gap — could be edited, not spacing.
    pytest.param(
        "app.ts",
        ["-f(/* a */ x)", "+f( /* a */x)"],
        False,
        None,
        id="ts-block-comment-gap-declined",
    ),
    # Respacing that also dedents is an indentation change (semantic in Python).
    pytest.param(
        "app.py",
        ["-    x=1", "+  x = 1"],
        False,
        None,
        id="py-respace-with-dedent-declined",
    ),
    # In JS/TS, spacing around `<`/`>`/`/` decides how the line parses (generic
    # call vs comparisons, regex vs division) — never trusted as spacing.
    pytest.param(
        "app.tsx",
        ["-f<T>(x)", "+f < T > (x)"],
        False,
        None,
        id="ts-generic-spacing-declined",
    ),
    pytest.param(
        "app.js",
        ["-f(a, /b/ x)", "+f(a, / b / x)"],
        False,
        None,
        id="js-regex-spacing-declined",
    ),
    # ...while Python `/` is always division — plain spacing.
    pytest.param(
        "app.py",
        ["-x = a/b", "+x = a / b"],
        False,
        "formatting:spacing",
        id="py-slash-spacing-ok",
    ),
    # Spacing rules don't run on data formats, where whitespace can be the format.
    pytest.param("data.csv", ["-a,b", "+a, b"], False, None, id="csv-spacing-declined"),
]


def test_mid_file_insertion_is_whitespace_not_empty_file():
    """A pure insertion into an EXISTING file (`@@ -5,0 +6,2 @@`, e.g. a -U0
    diff) has old_length 0 but a nonzero old anchor — it must not read as a
    brand-new empty file."""
    file = DiffFile(old_path="main.py", new_path="main.py")
    hunk = DiffHunk(old_line=5, old_length=0, new_line=6, new_length=2)
    for _ in range(2):
        hunk.lines.append(
            DiffCode(
                old_line_number=None, new_line_number=6, content="", change_type="+"
            )
        )
    assert not hunk.is_new_file
    assert trust_label(file, hunk) == "formatting:whitespace"


def test_hashbang_mid_file_is_still_a_comment():
    """`#!` only means "interpreter" on line 1 of the file; deeper in a file it's
    ordinary comment text, so a change there stays comment churn."""
    file = DiffFile(old_path="run.py", new_path="run.py")
    hunk = DiffHunk(old_line=5, old_length=1, new_line=5, new_length=1)
    hunk.lines.append(
        DiffCode(
            old_line_number=5,
            new_line_number=None,
            content="#!/bin/bash is required here",
            change_type="-",
        )
    )
    hunk.lines.append(
        DiffCode(
            old_line_number=None,
            new_line_number=5,
            content="#!/bin/sh is required here",
            change_type="+",
        )
    )
    assert trust_label(file, hunk) == "comments:modified"


@pytest.mark.parametrize(("path", "lines", "new_file", "expected"), CASES)
def test_trust_label(path, lines, new_file, expected):
    file = DiffFile(old_path=path, new_path=path)
    hunk = make_hunk(lines, new_file=new_file)
    assert trust_label(file, hunk) == expected


def test_lockfile_rename_from_non_lockfile_is_not_trusted():
    # Renaming a hand-written file INTO a lockfile name must not hide its
    # content wholesale as "generated" (CASES can't express a rename: it sets
    # old_path == new_path).
    file = DiffFile(old_path="secrets.py", new_path="poetry.lock")
    hunk = make_hunk(["-API_KEY = 'old'", "+API_KEY = 'new'"], new_file=False)
    assert trust_label(file, hunk) is None


def test_lockfile_regenerated_in_place_is_trusted():
    file = DiffFile(old_path="uv.lock", new_path="uv.lock")
    hunk = make_hunk(['-version = "1.0"', '+version = "1.1"'], new_file=False)
    assert trust_label(file, hunk) == "generated:lockfile"


def test_trust_diff_end_to_end():
    """Parse a real multi-file diff and confirm hunks get labeled in place."""
    diff = (
        "diff --git a/uv.lock b/uv.lock\n"
        "index 1111111..2222222 100644\n"
        "--- a/uv.lock\n"
        "+++ b/uv.lock\n"
        "@@ -1,2 +1,2 @@\n"
        '-version = "1.0"\n'
        '+version = "1.1"\n'
        "diff --git a/app.py b/app.py\n"
        "index 3333333..4444444 100644\n"
        "--- a/app.py\n"
        "+++ b/app.py\n"
        "@@ -1,2 +1,2 @@\n"
        "-# old comment\n"
        "+# new comment\n"
        "diff --git a/core.py b/core.py\n"
        "index 5555555..6666666 100644\n"
        "--- a/core.py\n"
        "+++ b/core.py\n"
        "@@ -1,1 +1,1 @@\n"
        "-value = compute_old()\n"
        "+value = compute_new()\n"
    )

    files = trust_diff(diff)

    label_by_file = {f.new_path: [h.trust for h in f.hunks] for f in files}
    assert label_by_file == {
        "uv.lock": ["generated:lockfile"],
        "app.py": ["comments:modified"],
        "core.py": [None],  # real code change stays unlabeled
    }


def test_streaming_classification_matches_trust_diff():
    """Composing `iter_file_hunks` with `trust_label` — the streaming form the
    processing path and the CLI use — labels hunks exactly like `trust_diff`
    (the unlabeled real code change gets no label either way)."""
    diff = (
        "diff --git a/uv.lock b/uv.lock\n"
        "--- a/uv.lock\n"
        "+++ b/uv.lock\n"
        "@@ -1,2 +1,2 @@\n"
        '-version = "1.0"\n'
        '+version = "1.1"\n'
        "diff --git a/core.py b/core.py\n"
        "--- a/core.py\n"
        "+++ b/core.py\n"
        "@@ -1,1 +1,1 @@\n"
        "-value = compute_old()\n"
        "+value = compute_new()\n"
    )

    streamed = [
        (file.new_path, hunk.old_line, hunk.new_line, trust_label(file, hunk))
        for file, hunk in iter_file_hunks(diff)
    ]
    parsed = [
        (file.new_path, hunk.old_line, hunk.new_line, hunk.trust)
        for file in trust_diff(diff)
        for hunk in file.hunks
    ]
    assert streamed == parsed
    assert streamed == [
        ("uv.lock", 1, 1, "generated:lockfile"),
        ("core.py", 1, 1, None),
    ]


# File-level rename rule: each case is the metadata lines that follow the
# `diff --git` line of a HUNKLESS file (`None` lines omitted), and the expected
# label. Default-deny: only the exact pure-rename shape labels; a mode change,
# binary delta, copy, or any extra/substitute line must be shown.
FILE_CASES = [
    pytest.param(
        "a/old.py b/new.py",
        ["similarity index 100%", "rename from old.py", "rename to new.py"],
        "file:renamed",
        id="pure-rename",
    ),
    pytest.param(
        "a/old.py b/new.py",
        [
            "old mode 100644",
            "new mode 100755",
            "similarity index 100%",
            "rename from old.py",
            "rename to new.py",
        ],
        None,
        id="rename-with-mode-change",
    ),
    pytest.param(
        "a/old.bin b/new.bin",
        [
            "similarity index 98%",
            "rename from old.bin",
            "rename to new.bin",
            "index 0f49c4a..4c2de3c 100644",
            "Binary files a/old.bin and b/new.bin differ",
        ],
        None,
        id="binary-rename-with-changes",
    ),
    pytest.param(
        "a/old.py b/new.py",
        ["similarity index 100%", "copy from old.py", "copy to new.py"],
        None,
        id="copy-not-rename",
    ),
    pytest.param(
        "a/logo.bin b/logo.bin",
        [
            "index 0f49c4a..4c2de3c 100644",
            "Binary files a/logo.bin and b/logo.bin differ",
        ],
        None,
        id="binary-same-path",
    ),
    pytest.param(
        "a/script.sh b/script.sh",
        ["old mode 100644", "new mode 100755"],
        None,
        id="mode-only-change",
    ),
]


@pytest.mark.parametrize(("git_paths", "meta_lines", "expected"), FILE_CASES)
def test_trust_file_label(git_paths, meta_lines, expected):
    diff = "\n".join([f"diff --git {git_paths}", *meta_lines]) + "\n"
    (file,) = iter_hunkless_files(diff)
    label = trust_file_label(file)
    assert (label.value if label else None) == expected


def test_trust_file_label_declines_files_with_hunks():
    # A rename WITH content changes carries hunks — those classify per-hunk;
    # the file itself never reads as a trivial rename.
    diff = (
        "diff --git a/old.py b/new.py\n"
        "similarity index 95%\n"
        "rename from old.py\n"
        "rename to new.py\n"
        "--- a/old.py\n"
        "+++ b/new.py\n"
        "@@ -1,1 +1,1 @@\n"
        "-value = compute_old()\n"
        "+value = compute_new()\n"
    )
    assert list(iter_hunkless_files(diff)) == []
    (file,) = trust_diff(diff)
    assert trust_file_label(file) is None
