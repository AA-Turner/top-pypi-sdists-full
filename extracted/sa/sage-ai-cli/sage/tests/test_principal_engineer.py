"""Tests for the principal-engineer multi-pass builder.

These tests cover the deterministic pieces (planning, templates,
validators, review parsing, fence-stripping, orchestration with a stub
generator) without needing a real LLM, so they run fast in CI.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from sage.core.principal_engineer import (
    CURRENT_VERSIONS,
    FileSpec,
    _find_dangling_imports,
    build_file_prompt,
    build_integrity_fix_prompt,
    build_project,
    build_review_prompt,
    detect_stack,
    looks_like_build_request,
    parse_review_response,
    plan_android_compose,
    plan_fastapi_jwt,
    plan_for_task,
    plan_go_microservices,
    plan_react_frontend,
    strip_code_fences,
    validate_file,
)


class TestStackDetection:
    @pytest.mark.parametrize(
        "task,expected",
        [
            ("Build a FastAPI backend with JWT and SQLModel", "fastapi"),
            ("Go ecommerce microservices with gin and postgres", "go-microservices"),
            ("Native Android app with Jetpack Compose and Hilt", "android-compose"),
            ("Flutter app with riverpod", "flutter"),
            ("Rust analytics service with axum and tokio", "rust-axum"),
        ],
    )
    def test_detects_correct_stack(self, task: str, expected: str) -> None:
        assert detect_stack(task) == expected


class TestProjectPlans:
    def test_fastapi_plan_includes_principal_essentials(self) -> None:
        paths = {f.path for f in plan_fastapi_jwt()}
        for required in [
            "pyproject.toml",
            ".env.example",
            ".gitignore",
            "Dockerfile",
            "docker-compose.yml",
            ".github/workflows/ci.yml",
            "README.md",
            "app/main.py",
            "app/security.py",
            "app/routers/auth.py",
            "tests/test_auth.py",
            "alembic/env.py",
        ]:
            assert required in paths, f"plan missing {required}"

    def test_fastapi_plan_pins_current_versions(self) -> None:
        pyproject = next(f for f in plan_fastapi_jwt() if f.path == "pyproject.toml")
        assert pyproject.template is not None
        assert CURRENT_VERSIONS["python"]["fastapi"] in pyproject.template
        # NEVER pin a stale 0.85
        assert "fastapi==0.85" not in pyproject.template

    def test_fastapi_security_spec_forbids_plain_compare(self) -> None:
        sec = next(f for f in plan_fastapi_jwt() if f.path == "app/security.py")
        assert "bcrypt" in sec.must_contain
        assert "plain_password ==" in sec.must_not_contain

    def test_react_plan_pins_react_19(self) -> None:
        pkg = next(f for f in plan_react_frontend() if f.path == "frontend/package.json")
        assert pkg.template is not None
        assert "\"react\": \"^19" in pkg.template

    def test_go_plan_forbids_wrong_db_driver(self) -> None:
        plan = plan_go_microservices()
        mains = [f for f in plan if f.path.endswith("cmd/main.go")]
        assert mains, "no main.go in go plan"
        for m in mains:
            assert "github.com/go-sql-driver/mysql" in m.must_not_contain
            assert "mysql.Config" in m.must_not_contain

    def test_go_plan_has_all_five_services(self) -> None:
        paths = {f.path for f in plan_go_microservices()}
        for svc in ["user", "product", "cart", "order", "payment"]:
            assert f"{svc}-service/cmd/main.go" in paths
            assert f"{svc}-service/Dockerfile" in paths

    def test_android_plan_forbids_empty_string_value(self) -> None:
        plan = plan_android_compose()
        login = next(f for f in plan if f.path.endswith("LoginScreen.kt"))
        assert 'value = ""' in login.must_not_contain
        assert "collectAsStateWithLifecycle" in login.must_contain

    def test_android_plan_pins_current_compose_bom(self) -> None:
        plan = plan_android_compose()
        app_gradle = next(f for f in plan if f.path == "app/build.gradle.kts")
        assert app_gradle.template is not None
        assert CURRENT_VERSIONS["kotlin"]["compose_bom"] in app_gradle.template
        assert "1.0.5" not in app_gradle.template


class TestPlanForTaskRouting:
    def test_fastapi_react_task_includes_both_plans(self) -> None:
        stack, files = plan_for_task(
            "Build a FastAPI backend with JWT and a React TypeScript frontend"
        )
        paths = {f.path for f in files}
        assert "app/main.py" in paths
        assert "frontend/package.json" in paths
        assert stack == "fastapi"

    def test_rust_axum_task_returns_rust_plan(self) -> None:
        stack, files = plan_for_task("Build a Rust analytics service with axum and tokio")
        assert stack == "rust-axum"
        paths = {f.path for f in files}
        assert "Cargo.toml" in paths
        assert "src/main.rs" in paths

    def test_spring_boot_task_returns_spring_plan(self) -> None:
        stack, files = plan_for_task("Build a Spring Boot banking API with JWT")
        assert stack == "spring-boot"
        paths = {f.path for f in files}
        assert "pom.xml" in paths
        assert any("SecurityConfig.java" in p for p in paths)

    def test_ios_task_returns_ios_plan(self) -> None:
        stack, files = plan_for_task("Build an iOS Swift app with SwiftUI login")
        assert stack == "ios-swift"
        paths = {f.path for f in files}
        assert "Package.swift" in paths
        assert any("LoginView.swift" in p for p in paths)

    def test_flutter_task_returns_flutter_plan(self) -> None:
        stack, files = plan_for_task("Build a Flutter app with riverpod and go_router")
        assert stack == "flutter"
        paths = {f.path for f in files}
        assert "pubspec.yaml" in paths
        assert any("auth_repository.dart" in p for p in paths)


class TestExpandedPlanPinsCurrentVersions:
    def test_rust_cargo_pins_current_tokio(self) -> None:
        from sage.core.principal_engineer import plan_rust_axum, CURRENT_VERSIONS

        cargo = next(f for f in plan_rust_axum() if f.path == "Cargo.toml")
        assert cargo.template is not None
        assert CURRENT_VERSIONS["rust"]["tokio"] in cargo.template
        assert CURRENT_VERSIONS["rust"]["axum"] in cargo.template

    def test_spring_pom_pins_current_boot(self) -> None:
        from sage.core.principal_engineer import plan_spring_boot, CURRENT_VERSIONS

        pom = next(f for f in plan_spring_boot() if f.path == "pom.xml")
        assert pom.template is not None
        assert CURRENT_VERSIONS["java"]["spring_boot"] in pom.template

    def test_flutter_pubspec_pins_current_riverpod(self) -> None:
        from sage.core.principal_engineer import plan_flutter, CURRENT_VERSIONS

        pubspec = next(f for f in plan_flutter() if f.path == "pubspec.yaml")
        assert pubspec.template is not None
        assert CURRENT_VERSIONS["dart"]["riverpod"] in pubspec.template


class TestPromptBuilder:
    def test_prompt_includes_version_pins(self) -> None:
        spec = FileSpec(path="app/main.py", role="r", language="python")
        prompt = build_file_prompt(
            "build fastapi app", spec, ["app/main.py"], "fastapi", CURRENT_VERSIONS["python"]
        )
        assert "fastapi: 0.115" in prompt
        assert "Output ONLY the raw file contents" in prompt

    def test_prompt_includes_must_contain_constraints(self) -> None:
        spec = FileSpec(
            path="x.py",
            role="r",
            language="python",
            must_contain=["asyncio"],
            must_not_contain=["time.sleep"],
        )
        prompt = build_file_prompt("t", spec, ["x.py"], "fastapi", {"fastapi": "0.115"})
        assert "asyncio" in prompt
        assert "time.sleep" in prompt

    def test_review_prompt_requests_json(self) -> None:
        spec = FileSpec(path="x.py", role="r", language="python")
        prompt = build_review_prompt("t", spec, "print('hi')")
        assert "\"score\"" in prompt
        assert "ONE line of JSON" in prompt


class TestReviewParsing:
    def test_extracts_json_from_clean_response(self) -> None:
        r = parse_review_response('{"score": 9.2, "notes": "looks good", "gaps": []}')
        assert r.score == 9.2
        assert r.notes == "looks good"
        assert r.gaps == []

    def test_extracts_from_prose_wrapped_json(self) -> None:
        r = parse_review_response(
            'Sure, here\'s the review: {"score": 7.5, "notes": "missing tests", "gaps": ["add tests"]} thanks!'
        )
        assert r.score == 7.5
        assert r.gaps == ["add tests"]

    def test_handles_unparseable(self) -> None:
        r = parse_review_response("totally not json")
        assert r.score == 5.0  # safe default
        assert r.gaps == []


class TestValidator:
    def test_returns_empty_when_all_constraints_met(self) -> None:
        spec = FileSpec(
            path="x.py",
            role="r",
            language="python",
            must_contain=["import bcrypt"],
            must_not_contain=["plain =="],
        )
        assert validate_file(spec, "import bcrypt\nhash = bcrypt.hashpw(b'x', bcrypt.gensalt())") == []

    def test_flags_missing_required(self) -> None:
        spec = FileSpec(path="x.py", role="r", language="python", must_contain=["asyncio"])
        errors = validate_file(spec, "import os\n")
        assert len(errors) == 1
        assert "asyncio" in errors[0]

    def test_flags_forbidden_token(self) -> None:
        spec = FileSpec(
            path="x.py", role="r", language="python", must_not_contain=["password =="]
        )
        errors = validate_file(spec, "if password == form_password: ...")
        assert any("password ==" in e for e in errors)


class TestFenceStripping:
    def test_strips_python_fence(self) -> None:
        out = strip_code_fences("```python\nprint(1)\n```")
        assert out.strip() == "print(1)"

    def test_strips_generic_fence(self) -> None:
        out = strip_code_fences("```\nfoo\nbar\n```")
        assert "foo" in out and "```" not in out

    def test_passes_through_when_no_fence(self) -> None:
        assert strip_code_fences("clean code") == "clean code\n"

    def test_extracts_fenced_block_from_prose_wrapper(self) -> None:
        """Model sometimes emits 'Here is the file:\\n```python\\n...\\n```\\nDone.'"""
        out = strip_code_fences(
            "Here is the file:\n```python\nclass User: pass\n```\nDone."
        )
        assert out.strip() == "class User: pass"

    def test_strips_trailing_fence_with_extra_newlines(self) -> None:
        """The bug seen in live run: trailing ``` survived after class body."""
        out = strip_code_fences("class User:\n    pass\n```\n\n")
        assert "```" not in out
        assert "class User" in out


class TestBuildProjectOrchestration:
    """End-to-end with a stub generator that emits valid-looking content."""

    def test_writes_all_planned_files(self, tmp_path: Path) -> None:
        calls: list[str] = []

        def stub(prompt: str) -> str:
            calls.append(prompt)
            # If the prompt is a review prompt, emit a high JSON score
            if "ONE line of JSON" in prompt:
                return '{"score": 9.0, "notes": "ok", "gaps": []}'
            # Emit code satisfying common must_contain tokens
            return (
                "from __future__ import annotations\n"
                "import asyncio, bcrypt\n"
                "from fastapi import FastAPI, Depends, HTTPException\n"
                "from sqlmodel import SQLModel\n"
                "from pydantic_settings import BaseSettings\n"
                "from pydantic import BaseModel, EmailStr\n"
                "from jose import jwt\n"
                "\n"
                "class Settings(BaseSettings):\n"
                "    SECRET_KEY: str\n"
                "    DATABASE_URL: str\n"
                "\n"
                "class User(SQLModel, table=True):\n"
                "    id: int\n"
                "    hashed_password: str\n"
                "\n"
                "def hash_password(p: str) -> str: return bcrypt.hashpw(p.encode(), bcrypt.gensalt()).decode()\n"
                "def verify_password(p: str, h: str) -> bool: return bcrypt.checkpw(p.encode(), h.encode())\n"
                "encoded = jwt.encode({}, 'k')\n"
                "401, 200\n"
                "/register /login /me /health\n"
                "CORSMiddleware\n"
                "include_router(...)\n"
                "def get_current_user(token = Depends(...)):\n"
                "    raise HTTPException(401)\n"
                "@asynccontextmanager\n"
                "async def get_session(): yield\n"
                "target_metadata = None\n"
                "def upgrade(): pass\n"
                "def downgrade(): pass\n"
                "users\n"
                "def test_foo():\n    assert 1 == 1\n"
                "pytest.fixture\n"
            )

        report = build_project(
            "Build a FastAPI backend with JWT auth",
            tmp_path,
            stub,
            max_review_passes=1,
            review_threshold=8.0,
        )

        assert report["stack"] == "fastapi"
        # All planned files must exist on disk
        for entry in report["files"]:
            assert (tmp_path / entry["path"]).exists(), f"{entry['path']} missing"

        # Templates produce a meaningful chunk of files (deterministic 10/10s)
        assert report["template_count"] >= 6

        # The README is LLM-generated (no template) so we must have at least 1 LLM call
        assert report["llm_count"] >= 1

    def test_template_files_score_ten(self, tmp_path: Path) -> None:
        def stub(prompt: str) -> str:
            if "ONE line of JSON" in prompt:
                return '{"score": 9.0, "notes": "ok", "gaps": []}'
            return "OK\n"

        report = build_project("build fastapi", tmp_path, stub, max_review_passes=0)
        for entry in report["files"]:
            if entry["source"] == "template":
                assert entry["score"] == 10.0

    def test_validator_retries_when_content_violates_constraints(
        self, tmp_path: Path
    ) -> None:
        """First call returns bad content; second call returns content
        satisfying must_contain — orchestrator should keep the second."""
        attempts = {"n": 0}

        def stub(prompt: str) -> str:
            if "ONE line of JSON" in prompt:
                return '{"score": 9.0, "notes": "ok", "gaps": []}'
            attempts["n"] += 1
            if attempts["n"] == 1:
                # First emission misses must_contain tokens
                return "x = 1\n"
            # Subsequent emissions are valid
            return (
                "import asyncio, bcrypt\nfrom fastapi import FastAPI\n"
                "SECRET_KEY = ''\nDATABASE_URL = ''\n"
                "class User: hashed_password = ''\nBaseSettings\nEmailStr\n"
                "jwt.encode bcrypt /register /login /me hash_password "
                "Depends HTTPException 401 CORSMiddleware include_router /health "
                "target_metadata def upgrade(): def downgrade(): users "
                "def test_x():\n    assert True\n"
            )

        report = build_project("build fastapi", tmp_path, stub, max_review_passes=0)
        # Code files should have been retried; orchestrator should not have crashed
        assert any(f["source"] == "llm" for f in report["files"])


class TestBuildRequestDetector:
    @pytest.mark.parametrize(
        "prompt",
        [
            "Build a production-grade FastAPI backend with JWT auth and a React TypeScript frontend",
            "Create a Go microservices backend for an ecommerce platform with five services",
            "Make a native Android app using Kotlin and Jetpack Compose with login + signup",
            "Build a Rust analytics service with axum and tokio that handles 10k req/s",
        ],
    )
    def test_detects_real_build_requests(self, prompt: str) -> None:
        assert looks_like_build_request(prompt) is True

    @pytest.mark.parametrize(
        "prompt",
        [
            "What does FastAPI do?",
            "Explain JWT authentication",
            "Why is async slower in some cases?",
            "How do I read a file?",
            "Tell me about React hooks",
        ],
    )
    def test_does_not_detect_pure_questions(self, prompt: str) -> None:
        assert looks_like_build_request(prompt) is False

    def test_short_prompt_below_min_chars_is_rejected(self) -> None:
        # Has a build verb but is too short to be a real project request
        assert looks_like_build_request("build api") is False


class TestCrossFileIntegrity:
    def test_finds_dangling_import_when_symbol_missing(self) -> None:
        py = {
            "app/db.py": "async def get_session(): pass\n",
            "app/deps.py": "from app.db import get_session, get_user_by_email\n",
        }
        issues = _find_dangling_imports(py)
        assert ("app/deps.py", "app.db", "get_user_by_email") in issues
        assert ("app/deps.py", "app.db", "get_session") not in issues

    def test_returns_empty_when_all_imports_resolve(self) -> None:
        py = {
            "app/db.py": "async def get_session(): pass\nclass Engine: pass\n",
            "app/main.py": "from app.db import get_session, Engine\n",
        }
        assert _find_dangling_imports(py) == []

    def test_skips_third_party_imports(self) -> None:
        py = {
            "app/main.py": "from fastapi import FastAPI\nfrom sqlmodel import select\n",
        }
        assert _find_dangling_imports(py) == []

    def test_handles_syntax_errors_gracefully(self) -> None:
        py = {"app/broken.py": "def oops(:\n", "app/main.py": "from app.broken import oops\n"}
        # Should not raise; broken file's symbols are simply unknown.
        result = _find_dangling_imports(py)
        assert isinstance(result, list)

    def test_integrity_fix_prompt_includes_sibling_contents(self) -> None:
        prompt = build_integrity_fix_prompt(
            "app/deps.py",
            "from app.db import get_user_by_email\nimport asyncio\n",
            {"app/db.py": "async def get_session(): pass\n"},
            [("app.db", "get_user_by_email")],
        )
        assert "app/deps.py" in prompt
        assert "app/db.py" in prompt
        assert "get_user_by_email" in prompt
        assert "async def get_session" in prompt  # sibling content present


class TestAuthRouterContractEnforcement:
    """Tests pinning the spec changes made after live-build bugs."""

    def test_auth_router_forbids_pydantic_v1_from_orm(self) -> None:
        plan = plan_fastapi_jwt()
        spec = next(f for f in plan if f.path == "app/routers/auth.py")
        assert "from_orm" in spec.must_not_contain
        assert "UserCreateSchema" in spec.must_not_contain

    def test_auth_router_requires_schema_imports(self) -> None:
        plan = plan_fastapi_jwt()
        spec = next(f for f in plan if f.path == "app/routers/auth.py")
        assert any("UserCreate" == m for m in spec.must_contain)
        assert any("UserRead" == m for m in spec.must_contain)
        assert any("Token" == m for m in spec.must_contain)

    def test_main_py_forbids_deprecated_lifespan_patterns(self) -> None:
        plan = plan_fastapi_jwt()
        spec = next(f for f in plan if f.path == "app/main.py")
        assert "@app.on_event" in spec.must_not_contain
        assert "lifespan=\"on\"" in spec.must_not_contain
        assert "async def lifespan" in spec.must_contain
        assert "@asynccontextmanager" in spec.must_contain

    def test_tests_forbid_username_field(self) -> None:
        plan = plan_fastapi_jwt()
        spec = next(f for f in plan if f.path == "tests/test_auth.py")
        assert "\"username\":" in spec.must_not_contain
        assert "\"email\":" in spec.must_contain
        assert "\"password\":" in spec.must_contain

    def test_authcontext_login_signature_pinned(self) -> None:
        plan = plan_fastapi_jwt() + plan_react_frontend()
        spec = next(f for f in plan if f.path == "frontend/src/context/AuthContext.tsx")
        assert "email: string, password: string" in spec.must_contain
        assert "Promise<void>" in spec.must_contain
        assert "user: any" in spec.must_not_contain


class TestLintValidator:
    def test_undefined_names_finds_missing_import(self) -> None:
        from sage.core.principal_engineer import detect_python_undefined_names

        source = (
            "from sqlmodel import SQLModel\n"
            "from app.config import settings\n"
            "engine = None\n"
            "def fetch_user(session, email):\n"
            "    return session.query(User).filter(User.email == email).first()\n"
        )
        undef = detect_python_undefined_names(source)
        assert "User" in undef

    def test_undefined_names_clean_source_returns_empty(self) -> None:
        from sage.core.principal_engineer import detect_python_undefined_names

        source = (
            "from sqlmodel import SQLModel\n"
            "from app.models import User\n"
            "from app.config import settings\n"
            "def fetch_user(session, email):\n"
            "    return session.query(User).filter(User.email == email).first()\n"
        )
        undef = detect_python_undefined_names(source)
        assert "User" not in undef

    def test_undefined_names_handles_syntax_error(self) -> None:
        from sage.core.principal_engineer import detect_python_undefined_names

        assert detect_python_undefined_names("def broken(:\n    pass\n") == []

    def test_build_lint_fix_prompt_includes_diagnostics(self) -> None:
        from sage.core.principal_engineer import build_lint_fix_prompt

        prompt = build_lint_fix_prompt(
            "app/db.py",
            "User()\n",
            ["app/db.py:1:1: F821 undefined name 'User'"],
            ["User"],
        )
        assert "F821" in prompt
        assert "`User`" in prompt
        assert "Rewrite the WHOLE file" in prompt


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
