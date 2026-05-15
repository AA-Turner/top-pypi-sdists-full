"""Tests for the pre-write validator."""

from __future__ import annotations

from pathlib import Path

import pytest

from sage.core.pre_write_validator import (
    ValidationResult,
    validate_generated_file,
    validate_python,
    validate_typescript,
    validated_generate,
)


class TestValidatePython:
    def test_clean_module_passes(self) -> None:
        src = (
            "from datetime import datetime\n"
            "\n"
            "def hello() -> str:\n"
            "    return f'hi at {datetime.now()}'\n"
        )
        r = validate_python(src)
        assert r.ok, r.errors

    def test_syntax_error_fails(self) -> None:
        src = "def foo(:::\n    return 1\n"
        r = validate_python(src)
        assert not r.ok
        assert any("SyntaxError" in e for e in r.errors)

    def test_undefined_name_fails(self) -> None:
        src = (
            "def route(user = Depends(get_current_user)):\n"
            "    return user\n"
        )
        r = validate_python(src)
        assert not r.ok
        # Both Depends AND get_current_user should be flagged
        assert any("Depends" in e for e in r.errors)
        assert any("get_current_user" in e for e in r.errors)

    def test_imports_satisfy_uses(self) -> None:
        src = (
            "from fastapi import Depends\n"
            "from app.auth.dependencies import get_current_user\n"
            "\n"
            "def route(user = Depends(get_current_user)):\n"
            "    return user\n"
        )
        r = validate_python(src)
        assert r.ok, r.errors

    def test_truncated_at_colon_fails(self) -> None:
        src = (
            "def foo() -> int:\n"
            "    if True:\n"
        )
        r = validate_python(src)
        assert not r.ok
        # Either syntax error or truncation flag — either is fine
        assert r.errors

    def test_empty_fails(self) -> None:
        r = validate_python("")
        assert not r.ok

    def test_class_method_arg_names_count_as_bound(self) -> None:
        src = (
            "class Foo:\n"
            "    def bar(self, x: int) -> int:\n"
            "        return x + 1\n"
        )
        r = validate_python(src)
        assert r.ok, r.errors


class TestValidateTypescript:
    def test_clean_tsx_passes(self) -> None:
        src = (
            "import { View, Text } from 'react-native';\n"
            "export function X() {\n"
            "  return <View><Text>hi</Text></View>;\n"
            "}\n"
        )
        r = validate_typescript(src, is_rn_frontend=True)
        assert r.ok, r.errors

    def test_unbalanced_braces_fails(self) -> None:
        src = "function X() {\n  if (true) {\n    return 1;\n"
        r = validate_typescript(src)
        assert not r.ok
        assert any("brace" in e.lower() for e in r.errors)

    def test_truncated_mid_tag_fails(self) -> None:
        src = "function X() {\n  return <View><Text"
        r = validate_typescript(src, is_rn_frontend=True)
        assert not r.ok

    def test_forbidden_react_router_dom_in_rn(self) -> None:
        src = (
            "import { Link } from 'react-router-dom';\n"
            "export function X() { return <Link to='/'>x</Link>; }\n"
        )
        r = validate_typescript(src, is_rn_frontend=True)
        assert not r.ok
        assert any("react-router-dom" in e for e in r.errors)

    def test_forbidden_div_in_rn(self) -> None:
        src = "export function X() { return <div>hi</div>; }\n"
        r = validate_typescript(src, is_rn_frontend=True)
        assert not r.ok
        assert any("<div>" in e or "div" in e for e in r.errors)

    def test_div_ok_when_not_rn(self) -> None:
        # For a plain React (not RN) project, <div> is fine
        src = "export function X() { return <div>hi</div>; }\n"
        r = validate_typescript(src, is_rn_frontend=False)
        # We should NOT flag div outside RN context
        assert r.ok

    def test_string_with_brace_doesnt_break_count(self) -> None:
        # Quote-stripping must work so a string containing { doesn't unbalance
        src = "const a = '{ hello }';\nexport default function X() { return null; }\n"
        r = validate_typescript(src)
        assert r.ok, r.errors


class TestValidatedGenerate:
    def test_returns_first_clean_response(self) -> None:
        responses = iter([
            "from datetime import datetime\ndef f(): return datetime.now()\n",
        ])
        result_content, result = validated_generate(
            initial_prompt="prompt",
            path="x.py",
            generate=lambda _: next(responses),
            sanitize=lambda s: s,
            max_attempts=3,
        )
        assert result.ok
        assert "datetime" in result_content

    def test_retries_with_error_feedback(self) -> None:
        responses = iter([
            "def f(): return undefined_name + 1\n",  # fails
            "def f(): return 1\n",                    # passes
        ])
        prompts_seen: list[str] = []

        def gen(p: str) -> str:
            prompts_seen.append(p)
            return next(responses)

        content, result = validated_generate(
            initial_prompt="prompt",
            path="x.py",
            generate=gen,
            sanitize=lambda s: s,
            max_attempts=3,
        )
        assert result.ok
        assert "undefined_name" not in content
        # Second prompt MUST contain the defect description
        assert "undefined_name" in prompts_seen[1] or "previous attempt" in prompts_seen[1]

    def test_returns_best_effort_after_max_attempts(self) -> None:
        responses = iter([
            "def f(:::\n",                           # syntax error
            "def f():\n    return undefined_x + 1\n",  # undefined
            "def f(:::\n",                           # syntax error again
        ])
        content, result = validated_generate(
            initial_prompt="prompt",
            path="x.py",
            generate=lambda _: next(responses),
            sanitize=lambda s: s,
            max_attempts=3,
        )
        assert not result.ok
        # Returned the LAST attempt (caller decides what to do)
        assert content


class TestValidateGeneratedFile:
    def test_dispatch_by_extension(self) -> None:
        py = validate_generated_file("def x(): return 1\n", "x.py")
        ts = validate_generated_file(
            "export function X() { return null; }\n", "x.tsx"
        )
        assert py.ok
        assert ts.ok

    def test_unknown_extension_passes(self) -> None:
        r = validate_generated_file("anything", "x.md")
        assert r.ok
