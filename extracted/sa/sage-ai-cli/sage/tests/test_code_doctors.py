"""Tests for code_doctors — deterministic post-generation repair."""

from __future__ import annotations

from pathlib import Path

import pytest

from sage.core.code_doctors import (
    DoctorReport,
    add_missing_imports,
    detect_truncated_python,
    detect_truncated_tsx,
    fix_framework_collision_rn,
    run_code_doctors,
)


class TestAddMissingImports:
    def test_adds_index_import(self, tmp_path: Path) -> None:
        p = tmp_path / "x.py"
        p.write_text(
            "class Foo:\n    __table_args__ = (Index('ix_x', 'col'),)\n"
        )
        n = add_missing_imports(p)
        assert n >= 1
        content = p.read_text()
        assert "from sqlalchemy import Index" in content

    def test_adds_get_current_user_import(self, tmp_path: Path) -> None:
        p = tmp_path / "x.py"
        p.write_text(
            "def route(user = Depends(get_current_user)):\n    return user\n"
        )
        n = add_missing_imports(p)
        assert n >= 2  # Depends + get_current_user
        content = p.read_text()
        assert "from fastapi import Depends" in content
        assert "from app.auth.dependencies import get_current_user" in content

    def test_skips_already_imported_names(self, tmp_path: Path) -> None:
        p = tmp_path / "x.py"
        p.write_text(
            "from datetime import datetime\n"
            "x = datetime.now()\n"
        )
        n = add_missing_imports(p)
        assert n == 0
        # datetime already there, not re-added

    def test_skips_locally_defined_names(self, tmp_path: Path) -> None:
        p = tmp_path / "x.py"
        p.write_text(
            "def Index(x):\n    return x\n"
            "Index(5)\n"
        )
        n = add_missing_imports(p)
        # Index is defined locally — must NOT add the sqlalchemy import
        assert n == 0
        assert "from sqlalchemy import Index" not in p.read_text()

    def test_preserves_module_docstring(self, tmp_path: Path) -> None:
        p = tmp_path / "x.py"
        p.write_text(
            '"""Module docstring.\n\nWith multiple lines."""\n'
            "from __future__ import annotations\n\n"
            "def foo(): return bcrypt.hash('x')\n"
        )
        add_missing_imports(p)
        content = p.read_text()
        # Docstring must be first; future import second
        assert content.startswith('"""Module docstring.')
        assert "from __future__ import annotations" in content


class TestFixFrameworkCollisionRn:
    def test_replaces_react_router_dom_import(self, tmp_path: Path) -> None:
        p = tmp_path / "login.tsx"
        p.write_text(
            "import { Link } from 'react-router-dom';\n"
            "export default function L() { return <Link to='/'>Home</Link>; }\n"
        )
        n = fix_framework_collision_rn(p)
        assert n >= 1
        content = p.read_text()
        assert "react-router-dom" not in content
        assert "expo-router" in content

    def test_replaces_html_div_with_view(self, tmp_path: Path) -> None:
        p = tmp_path / "comp.tsx"
        p.write_text(
            "export default function C() { return <div className='x'><div>hello</div></div>; }\n"
        )
        n = fix_framework_collision_rn(p)
        assert n >= 2  # 2 <div> opens + 2 </div> closes = 4 substitutions
        content = p.read_text()
        assert "<div" not in content
        assert "<View" in content
        # And View must be imported
        assert "View" in content
        assert "react-native" in content

    def test_replaces_html_form_input_button(self, tmp_path: Path) -> None:
        p = tmp_path / "form.tsx"
        p.write_text(
            "export default function F() {\n"
            "  return (\n"
            "    <form>\n"
            "      <input type='text' />\n"
            "      <button>Submit</button>\n"
            "    </form>\n"
            "  );\n"
            "}\n"
        )
        fix_framework_collision_rn(p)
        content = p.read_text()
        assert "<form" not in content
        assert "<input" not in content
        assert "<button" not in content
        assert "<View" in content
        assert "<TextInput" in content
        assert "<Pressable" in content

    def test_replaces_use_navigate_with_use_router(self, tmp_path: Path) -> None:
        p = tmp_path / "x.tsx"
        p.write_text(
            "import { useNavigate } from 'react-router-dom';\n"
            "const nav = useNavigate();\n"
        )
        fix_framework_collision_rn(p)
        content = p.read_text()
        assert "useNavigate" not in content
        assert "useRouter" in content

    def test_extends_existing_rn_import(self, tmp_path: Path) -> None:
        p = tmp_path / "x.tsx"
        p.write_text(
            "import { Text } from 'react-native';\n"
            "export default function X() { return <div><Text>hi</Text></div>; }\n"
        )
        fix_framework_collision_rn(p)
        content = p.read_text()
        # Single import line, must contain both Text and View
        rn_lines = [line for line in content.split("\n")
                    if "react-native" in line and "import" in line]
        assert len(rn_lines) == 1
        assert "View" in rn_lines[0]
        assert "Text" in rn_lines[0]


class TestDetectTruncations:
    def test_detects_unclosed_python(self, tmp_path: Path) -> None:
        p = tmp_path / "x.py"
        p.write_text("def foo():\n    return {\n        'a': 1,\n        'b': \n")
        assert detect_truncated_python(p)

    def test_clean_python_not_detected(self, tmp_path: Path) -> None:
        p = tmp_path / "x.py"
        p.write_text("def foo():\n    return 1\n")
        assert not detect_truncated_python(p)

    def test_detects_unbalanced_tsx(self, tmp_path: Path) -> None:
        p = tmp_path / "x.tsx"
        p.write_text(
            "function X() {\n  return (\n    <View>\n      <View>\n        <Text>{"
        )
        assert detect_truncated_tsx(p)

    def test_clean_tsx_not_detected(self, tmp_path: Path) -> None:
        p = tmp_path / "x.tsx"
        p.write_text(
            "function X() { return <View><Text>hi</Text></View>; }\n"
        )
        assert not detect_truncated_tsx(p)


class TestRunCodeDoctors:
    def test_no_backend_no_frontend_returns_empty_report(self, tmp_path: Path) -> None:
        report = run_code_doctors(tmp_path, log=lambda _: None)
        assert isinstance(report, DoctorReport)
        assert report.imports_added == 0
        assert report.framework_collisions_fixed == 0

    def test_fixes_imports_in_backend(self, tmp_path: Path) -> None:
        backend = tmp_path / "backend" / "app"
        backend.mkdir(parents=True)
        (backend / "models.py").write_text(
            "class Campaign(SQLModel, table=True):\n"
            "    id: int = Field(primary_key=True)\n"
            "    __table_args__ = (Index('ix_c', 'id'),)\n"
        )
        report = run_code_doctors(
            tmp_path, log=lambda _: None,
            run_ruff=False, run_eslint=False,  # skip in test
        )
        assert report.imports_added >= 1
        content = (backend / "models.py").read_text()
        assert "SQLModel" in content
        assert "from sqlalchemy import Index" in content

    def test_fixes_framework_collision_in_frontend(self, tmp_path: Path) -> None:
        frontend = tmp_path / "frontend"
        screens = frontend / "app" / "(auth)"
        screens.mkdir(parents=True)
        (screens / "login.tsx").write_text(
            "import { Link } from 'react-router-dom';\n"
            "export default function L() { return <div>hi</div>; }\n"
        )
        report = run_code_doctors(
            tmp_path, log=lambda _: None,
            run_ruff=False, run_eslint=False,
        )
        assert report.framework_collisions_fixed > 0
        content = (screens / "login.tsx").read_text()
        assert "react-router-dom" not in content
        assert "<div" not in content
