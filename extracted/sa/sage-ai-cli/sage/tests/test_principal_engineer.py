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
            # Critical: "React Native with Web" must route to react-native-web,
            # NOT plain React. Even though "react" appears multiple times in
            # the spec, the more specific "react native" phrase wins.
            (
                "Build a React Native app with Web support, TypeScript, and "
                "Expo. Use React Native components shared between mobile and web.",
                "react-native-web",
            ),
            (
                "Build an Expo app with expo-router for iOS, Android, and web",
                "react-native-web",
            ),
            # Plain React (web only) still routes to react
            ("Build a Vite React TypeScript dashboard", "react"),
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
        assert CURRENT_VERSIONS["python"]["fastapi"] in pyproject.role
        assert "fastapi==0.85" not in pyproject.role

    def test_fastapi_security_spec_forbids_plain_compare(self) -> None:
        sec = next(f for f in plan_fastapi_jwt() if f.path == "app/security.py")
        assert "bcrypt" in sec.must_contain
        assert "plain_password ==" in sec.must_not_contain

    def test_react_plan_pins_react_18(self) -> None:
        # Pinned to 18.3.1 (NOT 19) to match Expo SDK 52's react requirement.
        # If you bump Expo, bump react together — they MUST match or
        # `npm install` fails with a peer-dep conflict.
        pkg = next(f for f in plan_react_frontend() if f.path == "frontend/package.json")
        assert pkg.role is not None
        
        assert "^18" in pkg.role
        # No react@19 anywhere in the runtime deps section
        assert "^19" not in pkg.role

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
        assert app_gradle.role is not None
        assert CURRENT_VERSIONS["kotlin"]["compose_bom"] in app_gradle.role
        assert "1.0.5" not in app_gradle.role


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

    def test_react_native_web_task_returns_expo_plan(self) -> None:
        from sage.core.principal_engineer import plan_react_native_web

        stack, files = plan_for_task(
            "Build a React Native with Web support app using Expo and TypeScript"
        )
        assert stack == "react-native-web"
        paths = {f.path for f in files}
        # Expo essentials present
        assert "frontend/package.json" in paths
        assert "frontend/app.json" in paths
        assert "frontend/babel.config.js" in paths
        assert "frontend/metro.config.js" in paths
        assert "frontend/tsconfig.json" in paths
        # Expo Router app/ tree present
        assert "frontend/app/_layout.tsx" in paths
        assert "frontend/app/index.tsx" in paths
        assert "frontend/app/(auth)/login.tsx" in paths
        assert "frontend/app/(tabs)/dashboard.tsx" in paths
        # Cross-platform components
        assert "frontend/components/Button.tsx" in paths
        assert "frontend/components/TextField.tsx" in paths
        assert "frontend/context/AuthContext.tsx" in paths
        # Verify it's NOT React-DOM-only (no frontend/package.json)
        assert "frontend/vite.config.ts" not in paths

    def test_rn_web_plus_fastapi_returns_combined_plan(self) -> None:
        """User's actual ask: React Native + Web + FastAPI backend. Sage
        must produce BOTH halves, with backend nested under backend/ so
        files don't collide with the frontend at the project root."""
        stack, files = plan_for_task(
            "Build a React Native app with web support, TypeScript, Expo. "
            "Use FastAPI in Python for the backend with PostgreSQL and JWT auth."
        )
        assert stack == "react-native-web+fastapi"
        paths = {f.path for f in files}
        # Frontend essentials at project root
        assert "frontend/package.json" in paths
        assert "frontend/app/_layout.tsx" in paths
        # Backend essentials under backend/
        assert "backend/pyproject.toml" in paths
        assert "backend/app/main.py" in paths
        assert "backend/app/routers/auth.py" in paths
        assert "backend/tests/test_auth.py" in paths
        # No path collisions
        assert "pyproject.toml" not in paths
        assert "app/main.py" not in paths

    def test_login_in_spec_does_not_match_gin(self) -> None:
        """Regression: 'login' contains 'gin' but must not trigger
        go-microservices backend addition. Word-boundary regex required."""
        from sage.core.principal_engineer import _spec_mentions_backend

        assert _spec_mentions_backend("Build an iOS Swift app with login screen") is None
        assert _spec_mentions_backend("Build a Flutter app with signup and login flow") is None
        # Real go-microservice asks still detected
        assert _spec_mentions_backend(
            "Build a React Native app plus a Go microservice backend"
        ) == "go-microservices"

    def test_react_native_web_login_screen_forbids_html_elements(self) -> None:
        from sage.core.principal_engineer import plan_react_native_web

        login = next(
            f for f in plan_react_native_web() if f.path == "frontend/app/(auth)/login.tsx"
        )
        # Must use React Native primitives, not HTML
        assert "TextInput" in login.must_contain
        assert "<input" in login.must_not_contain
        assert "<form" in login.must_not_contain
        assert "className=" in login.must_not_contain

    def test_react_native_web_dashboard_uses_responsive_rn_primitives(self) -> None:
        from sage.core.principal_engineer import plan_react_native_web

        dash = next(
            f for f in plan_react_native_web() if f.path == "frontend/app/(tabs)/dashboard.tsx"
        )
        assert "FlatList" in dash.must_contain
        assert "useWindowDimensions" in dash.must_contain
        assert "<div" in dash.must_not_contain
        assert "<table" in dash.must_not_contain

    def test_react_native_web_package_pins_expo_sdk_52(self) -> None:
        from sage.core.principal_engineer import plan_react_native_web, CURRENT_VERSIONS

        pkg = next(f for f in plan_react_native_web() if f.path == "frontend/package.json")
        assert pkg.role is not None
        assert CURRENT_VERSIONS["expo"]["expo"] in pkg.role
        assert "react-native-web" in pkg.role
        assert "expo-router" in pkg.role

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
        assert CURRENT_VERSIONS["rust"]["tokio"] in cargo.role
        assert CURRENT_VERSIONS["rust"]["axum"] in cargo.role

    def test_spring_pom_pins_current_boot(self) -> None:
        from sage.core.principal_engineer import plan_spring_boot, CURRENT_VERSIONS

        pom = next(f for f in plan_spring_boot() if f.path == "pom.xml")
        assert pom.role is not None
        assert CURRENT_VERSIONS["java"]["spring_boot"] in pom.role

    def test_flutter_pubspec_pins_current_riverpod(self) -> None:
        from sage.core.principal_engineer import plan_flutter, CURRENT_VERSIONS

        pubspec = next(f for f in plan_flutter() if f.path == "pubspec.yaml")
        assert pubspec.role is not None
        assert CURRENT_VERSIONS["dart"]["riverpod"] in pubspec.role


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


class TestProjectRootLayout:
    """Sage scaffolds INTO the project root, internal artifacts in .sage/"""

    def test_project_brief_lands_in_dot_sage_subdir(self, tmp_path) -> None:
        """A long-input build must write PROJECT_BRIEF.md to ./.sage/, not
        to the project root — keeps the user's repo clean."""

        def stub(p: str) -> str:
            if "filled template" in p or "ONE chunk" in p:
                return (
                    "PROJECT: x\nSTACK: y\nAUTH: jwt\nFEATURES:\n- f\n"
                    "INTEGRATIONS:\nCROSS-CUTTING:\n- s\n"
                    "TENANCY: x\nDEPLOYMENT: docker\n"
                )
            if "ONE line of JSON" in p:
                return '{"score": 9.0, "notes": "ok", "gaps": []}'
            return "from __future__ import annotations\nimport asyncio\n"

        long_task = "Build a FastAPI backend. " * 200
        report = build_project(long_task, tmp_path, stub, max_review_passes=0)

        # PROJECT_BRIEF.md exists at .sage/PROJECT_BRIEF.md
        assert (tmp_path / ".sage" / "PROJECT_BRIEF.md").exists()
        # And NOT at the project root
        assert not (tmp_path / "PROJECT_BRIEF.md").exists()


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
        

        # The README is LLM-generated (no template) so we must have at least 1 LLM call
        assert report["llm_count"] >= 1

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

    def test_long_platform_spec_without_build_verb_routes(self) -> None:
        """The user's exact failure pattern: a long platform-spec prompt
        that says "Design the platform" instead of "Build a X" should
        still route through the principal pipeline."""
        spec = (
            "15. Development Requirements\n"
            "Use clean, scalable architecture:\n"
            "- TypeScript-first frontend\n"
            "- Modular React Native components\n"
            "- Shared code between mobile and web\n"
            "- SSR-compatible web routes\n"
            "- FastAPI backend with typed schemas\n"
            "- Clear API contracts\n"
            "- Background workers for long-running jobs\n"
            "- Real-time updates where needed\n"
            "- Testable services\n"
            "- Reusable AI prompt modules\n"
            "- Secure integration layer\n"
            "- Multi-tenant SaaS architecture\n\n"
            "The final product should feel like a combination of an AI ad "
            "agency, social media manager, SEO strategist, growth marketer, "
            "analytics dashboard, and campaign optimization engine.\n\n"
            "Design the platform to be modern, automated, scalable, secure, "
            "and focused on measurable user growth."
        )
        assert looks_like_build_request(spec) is True

    def test_design_verb_also_triggers(self) -> None:
        """`design a` should trigger build mode same as `build a`."""
        assert looks_like_build_request(
            "Design a production-grade FastAPI backend with JWT auth and React"
        ) is True
        assert looks_like_build_request(
            "Develop a modern SaaS platform using FastAPI and React Native"
        ) is True


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


class TestMultiBuildDecomposer:
    def test_single_task_stays_single(self) -> None:
        from sage.core.principal_engineer import decompose_multi_build_request

        task = (
            "Build a production-grade FastAPI backend with JWT auth and a React "
            "TypeScript frontend that consumes the auth flow."
        )
        result = decompose_multi_build_request(task)
        assert len(result) == 1
        assert result[0][0] == "project"

    def test_mega_prompt_with_14_builds_splits_correctly(self) -> None:
        from sage.core.principal_engineer import decompose_multi_build_request

        mega = (
            "Test sage on these tasks.\n\n"
            "Build a production-grade FastAPI backend with JWT auth and React.\n"
            "Build a Go-based microservices backend for ecommerce.\n"
            "Build a Rust backend API for analytics ingestion using axum.\n"
            "Build a Spring Boot backend for a banking transaction system.\n"
            "Build a native Android app using Kotlin and Jetpack Compose.\n"
            "Build a native iOS app using Swift and SwiftUI.\n"
            "Build a cross-platform mobile app using React Native and TypeScript.\n"
            "Build a Flutter app using Dart.\n"
            "Build a .NET backend API for a project management tool.\n"
            "Build a Laravel web application for appointment booking.\n"
            "Build a Rails application for customer support tickets.\n"
            "Build a C++ service component for high-speed message processing.\n"
            "Build a GraphQL API with a web client.\n"
            "Create production infrastructure for a full-stack app.\n"
        )
        result = decompose_multi_build_request(mega)
        # Should find ALL 14 tasks
        assert len(result) >= 13, f"only found {len(result)} sub-tasks"
        labels = [label for label, _ in result]
        # Each label should be distinct and meaningful
        assert len(set(labels)) >= len(result) - 1  # allow one near-collision
        for label, sub in result:
            assert len(sub) >= 25, f"sub-task too short: {label}"

    def test_decomposer_handles_numbered_lists(self) -> None:
        from sage.core.principal_engineer import decompose_multi_build_request

        task = (
            "1. Build a FastAPI backend with JWT auth and SQLModel for users.\n"
            "2. Build a Go microservices backend for ecommerce platform.\n"
            "3. Build a Rust analytics API using axum framework.\n"
        )
        result = decompose_multi_build_request(task)
        assert len(result) == 3

    def test_extremely_short_chunks_are_skipped(self) -> None:
        """A truly tiny 'Build a X.' shouldn't create a sub-task."""
        from sage.core.principal_engineer import decompose_multi_build_request

        task = (
            "Build a X.\n"
            "Build a production-grade FastAPI backend with JWT auth, SQLModel, "
            "Alembic migrations, Redis caching, and a React TypeScript frontend.\n"
        )
        result = decompose_multi_build_request(task)
        real_tasks = [sub for _, sub in result if len(sub) >= 50]
        assert len(real_tasks) >= 1


class TestTaskCompression:
    """Long prompts get compressed to a compact brief before per-file LLM calls."""

    def test_short_task_returned_unchanged(self) -> None:
        from sage.core.principal_engineer import compress_task_brief

        short = "Build a FastAPI backend with JWT auth."
        # No generate call is needed for short inputs — pass a stub that
        # would raise to prove it isn't called.
        def boom(_p: str) -> str:
            raise AssertionError("generate should not be called for short input")

        assert compress_task_brief(short, boom) == short

    def test_long_task_compressed_via_generate(self) -> None:
        from sage.core.principal_engineer import compress_task_brief

        long = ("Build a SaaS platform. " * 200)  # ~4000 chars
        compact = (
            "PROJECT: SaaS platform\n"
            "STACK: FastAPI, React, Postgres\n"
            "AUTH: JWT\n"
            "FEATURES:\n- core feature 1\n- core feature 2\n"
            "CROSS-CUTTING:\n- secure secrets\n"
            "TENANCY: multi-tenant\n"
            "DEPLOYMENT: docker\n"
        )

        def stub(_p: str) -> str:
            return compact

        result = compress_task_brief(long, stub)
        assert "PROJECT:" in result
        assert "STACK:" in result
        assert len(result) < len(long)

    def test_compression_falls_back_to_truncation_on_generate_error(self) -> None:
        from sage.core.principal_engineer import compress_task_brief

        long = ("X " * 2000)  # ~4000 chars

        def fail(_p: str) -> str:
            raise RuntimeError("model unavailable")

        result = compress_task_brief(long, fail)
        # Falls back to head/tail truncation; never raises
        assert isinstance(result, str)
        assert len(result) < len(long)
        assert "[middle omitted]" in result

    def test_compression_falls_back_when_brief_is_empty(self) -> None:
        from sage.core.principal_engineer import compress_task_brief

        long = ("X " * 2000)

        def empty(_p: str) -> str:
            return ""

        result = compress_task_brief(long, empty)
        # Falls back; never returns an empty brief
        assert len(result) > 100

    def test_compression_falls_back_when_brief_grows_larger(self) -> None:
        from sage.core.principal_engineer import compress_task_brief

        long = "Build a SaaS platform. " * 200  # ~4400 chars

        def bloated(_p: str) -> str:
            return long + " extra padding " * 1000  # bigger than input

        result = compress_task_brief(long, bloated)
        # Fall-back truncation must be smaller than the original input
        assert len(result) < len(long)

    def test_chunked_compression_for_huge_input(self) -> None:
        """Inputs larger than one LLM context get map-reduced."""
        from sage.core.principal_engineer import compress_task_brief

        # ~160K chars — must be chunked into ~4-5 pieces.
        huge_input = ("Build feature X with Postgres and Redis. " * 4000)
        calls: list[str] = []

        def stub(prompt: str) -> str:
            calls.append(prompt)
            if "ONE chunk of a larger" in prompt:
                return (
                    "TECH:\n- FastAPI\nFEATURES:\n- feature X\n"
                    "INTEGRATIONS:\nSECURITY:\nPERFORMANCE:\nOTHER:\n"
                )
            return (
                "PROJECT: huge SaaS\nSTACK: FastAPI\nAUTH: JWT\n"
                "FEATURES:\n- f1\nCROSS-CUTTING:\n- secrets\n"
                "TENANCY: multi-tenant\nDEPLOYMENT: docker\n"
            )

        result = compress_task_brief(huge_input, stub)
        map_calls = [c for c in calls if "ONE chunk of a larger" in c]
        assert len(map_calls) >= 3, (
            f"expected >=3 map calls, got {len(map_calls)}; "
            f"total calls={len(calls)}; "
            f"first call preview: {(calls[0][:120] if calls else '<none>')!r}"
        )
        # Final brief is bounded
        assert len(result) < len(huge_input)
        assert isinstance(result, str) and len(result) > 50

    def test_chunk_text_respects_paragraph_boundaries(self) -> None:
        from sage.core.principal_engineer import _chunk_text

        # Use real paragraphs (no trailing whitespace that .strip() would
        # eat) so we can measure that the chunker covers the full input.
        paragraphs = [f"Paragraph {i} with substantial content body." for i in range(50)]
        text = "\n\n".join(paragraphs)
        chunks = _chunk_text(text, max_chunk_chars=500)
        # All chunks under cap (with slight overshoot allowance at boundary)
        assert all(len(c) <= 600 for c in chunks)
        # Coverage: every paragraph appears in some chunk
        for i in range(50):
            assert any(f"Paragraph {i} " in c for c in chunks), (
                f"Paragraph {i} missing from chunks"
            )

    def test_chunk_text_handles_no_natural_breakpoints(self) -> None:
        """Single giant blob with no spaces should still be split."""
        from sage.core.principal_engineer import _chunk_text

        blob = "x" * 10_000
        chunks = _chunk_text(blob, max_chunk_chars=1000)
        assert len(chunks) >= 9
        assert all(len(c) <= 1000 for c in chunks)

    def test_extreme_input_at_hard_cap_does_not_hang(self) -> None:
        """Inputs over the 2M-char hard cap are pre-truncated."""
        from sage.core.principal_engineer import compress_task_brief

        # 3M chars — over the hard cap
        extreme = "Build a SaaS thing. " * 150_000
        call_count = {"n": 0}

        def stub(_p: str) -> str:
            call_count["n"] += 1
            return "TECH:\n- X\nFEATURES:\n- f\nINTEGRATIONS:\nSECURITY:\nPERFORMANCE:\nOTHER:\n"

        result = compress_task_brief(extreme, stub)
        # Should make a bounded number of calls — not thousands
        assert call_count["n"] < 100, f"too many calls: {call_count['n']}"
        assert isinstance(result, str)
        assert len(result) < len(extreme)


class TestPasteIndicator:
    """The paste indicator is a UX signal so the user can see exactly how
    much text made it through the terminal. It must bypass verbose-mode
    gating so it shows in clean/normal mode too — that's the whole point."""

    @staticmethod
    def _capture(monkeypatch) -> list[str]:
        """Replace renderer.console.print so we can assert what was emitted."""
        import sage.core.validation_helpers as validation_mod
        import sage.core.exploration_helpers as exp_mod
        import sage.core.session_helpers as session_mod
        import sage.core.renderer as renderer_mod

        captured: list[str] = []
        monkeypatch.setattr(
            renderer_mod.console, "print", lambda msg, **_kw: captured.append(str(msg))
        )
        return captured

    def test_emits_for_multiline_input(self, monkeypatch: pytest.MonkeyPatch) -> None:
        import sage.core.validation_helpers as validation_mod
        import sage.core.exploration_helpers as exp_mod
        import sage.core.session_helpers as session_mod
        import sage.core.renderer as renderer_mod

        captured = self._capture(monkeypatch)
        validation_mod._show_paste_indicator("line one\nline two\nline three")
        assert any("Text pasted" in m and "3 lines" in m for m in captured)

    def test_emits_for_large_single_line_input(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        import sage.core.validation_helpers as validation_mod
        import sage.core.exploration_helpers as exp_mod
        import sage.core.session_helpers as session_mod
        import sage.core.renderer as renderer_mod

        captured = self._capture(monkeypatch)
        validation_mod._show_paste_indicator("x" * 800)
        assert any("Text pasted" in m and "800 characters" in m for m in captured)

    def test_silent_for_short_single_line_input(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        import sage.core.validation_helpers as validation_mod
        import sage.core.exploration_helpers as exp_mod
        import sage.core.session_helpers as session_mod
        import sage.core.renderer as renderer_mod

        captured = self._capture(monkeypatch)
        validation_mod._show_paste_indicator("write a quick test")
        assert captured == []

    def test_silent_for_empty(self, monkeypatch: pytest.MonkeyPatch) -> None:
        import sage.core.validation_helpers as validation_mod
        import sage.core.exploration_helpers as exp_mod
        import sage.core.session_helpers as session_mod
        import sage.core.renderer as renderer_mod

        captured = self._capture(monkeypatch)
        validation_mod._show_paste_indicator("")
        validation_mod._show_paste_indicator(None)  # type: ignore[arg-type]
        assert captured == []

    def test_line_count_uses_thousands_separator(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        import sage.core.validation_helpers as validation_mod
        import sage.core.exploration_helpers as exp_mod
        import sage.core.session_helpers as session_mod
        import sage.core.renderer as renderer_mod

        captured = self._capture(monkeypatch)
        big = "\n".join(["row"] * 2500)
        validation_mod._show_paste_indicator(big)
        assert any("2,500 lines" in m for m in captured)

    def test_indicator_bypasses_verbose_mode_gating(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """REGRESSION: renderer.info() is verbose-mode-only and was
        suppressing the paste indicator in clean/normal mode (the default).
        Indicator must use renderer.console.print directly so it always
        renders."""
        import sage.core.validation_helpers as validation_mod
        import sage.core.exploration_helpers as exp_mod
        import sage.core.session_helpers as session_mod
        import sage.core.renderer as renderer_mod
        import sage.core.renderer as r

        # Pretend we're in clean mode (verbose disabled)
        monkeypatch.setattr(r, "is_verbose", lambda: False)
        captured = self._capture(monkeypatch)
        validation_mod._show_paste_indicator("a\nb\nc\nd")
        assert any("Text pasted" in m for m in captured), (
            "Paste indicator was suppressed in non-verbose mode — "
            "regression of the renderer.info() verbose-gating bug"
        )

    def test_indicator_visible_on_users_actual_8k_text(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Pin the exact user-facing string for an 8K-char, 369-line input
        like the user's advertising platform spec."""
        import sage.core.validation_helpers as validation_mod
        import sage.core.exploration_helpers as exp_mod
        import sage.core.session_helpers as session_mod
        import sage.core.renderer as renderer_mod

        # Reconstruct an 8138-char, 369-line input shape
        lines = ["Long content line " + str(i).rjust(3) for i in range(369)]
        text = "\n".join(lines)
        # Ensure roughly the right size shape (within a few hundred chars)
        assert text.count("\n") + 1 == 369
        captured = self._capture(monkeypatch)
        validation_mod._show_paste_indicator(text)
        joined = " ".join(captured)
        assert "Text pasted" in joined
        assert "369 lines" in joined

    def test_prompt_reader_attaches_bracketed_paste_handler(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path
    ) -> None:
        """The REPL prompt reader must wire a BracketedPaste key binding
        so the indicator fires the moment the user pastes, before they
        hit Enter."""
        import sys
        import sage.core.validation_helpers as validation_mod
        import sage.core.exploration_helpers as exp_mod
        import sage.core.session_helpers as session_mod
        import sage.core.renderer as renderer_mod

        monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
        monkeypatch.setattr(sys.stdout, "isatty", lambda: True)

        captured_kwargs: dict = {}

        class FakeSession:
            def __init__(self, **kwargs) -> None:  # type: ignore[no-untyped-def]
                captured_kwargs.update(kwargs)

            def prompt(self, prompt_text: str) -> str:
                return ""

        from prompt_toolkit.keys import Keys
        monkeypatch.setattr("prompt_toolkit.PromptSession", FakeSession)

        exp_mod._build_prompt_reader(tmp_path)
        bindings = captured_kwargs.get("key_bindings")
        assert bindings is not None
        all_keys = [b.keys for b in bindings.bindings]
        assert any(Keys.BracketedPaste in seq for seq in all_keys)

    def test_paste_handler_inserts_placeholder_and_expands_on_submit(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path
    ) -> None:
        """Simulate: user pastes 8K text → buffer shows `[Pasted text 8,138 characters]`
        → user types additional text → presses Enter → reader returns FULL
        expanded content (placeholder replaced with real paste)."""
        import sys
        import sage.core.validation_helpers as validation_mod
        import sage.core.exploration_helpers as exp_mod
        import sage.core.session_helpers as session_mod
        import sage.core.renderer as renderer_mod
        from prompt_toolkit.keys import Keys

        monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
        monkeypatch.setattr(sys.stdout, "isatty", lambda: True)

        large_paste = "Build a SaaS platform.\n" * 400  # ~8800 chars, multi-line

        # Capture the BracketedPaste handler so we can invoke it directly
        captured: dict = {"bindings": None, "buffer_text": ""}

        class FakeBuffer:
            def __init__(self) -> None:
                self.text = ""

            def insert_text(self, t: str) -> None:
                self.text += t

        class FakeEvent:
            def __init__(self, data: str, buf: FakeBuffer) -> None:
                self.data = data
                self.current_buffer = buf

        class FakeSession:
            def __init__(self, **kwargs) -> None:  # type: ignore[no-untyped-def]
                captured["bindings"] = kwargs.get("key_bindings")
                self._buf = FakeBuffer()

            def prompt(self, prompt_text: str) -> str:
                # Simulate the paste event firing, then the user typing
                # additional text, then submitting.
                paste_event = FakeEvent(large_paste, self._buf)
                # Find and call the BracketedPaste handler
                for b in captured["bindings"].bindings:
                    if Keys.BracketedPaste in b.keys:
                        b.handler(paste_event)
                        break
                # Capture what's now in the buffer (with placeholder)
                captured["buffer_text"] = self._buf.text
                # Simulate the user appending some text and pressing Enter
                return self._buf.text + " — build this"

        monkeypatch.setattr("prompt_toolkit.PromptSession", FakeSession)

        reader = exp_mod._build_prompt_reader(tmp_path)
        result = reader("you> ")

        # Buffer (what the terminal displayed) had the compact placeholder
        assert "[Pasted " in captured["buffer_text"]
        assert "lines]" in captured["buffer_text"]
        # The actual large paste is NOT in the displayed buffer
        assert "Build a SaaS platform.\nBuild a SaaS platform." not in captured["buffer_text"]
        # But the reader's return value HAS the full expanded text
        assert "Build a SaaS platform." in result
        assert result.count("Build a SaaS platform.") == 400
        # And the user's additional text is preserved at the end
        assert result.endswith(" — build this")
        # The paste-fired flag is exposed
        assert reader.last_paste_fired() is True

    def test_paste_handler_skips_placeholder_for_small_pastes(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path
    ) -> None:
        """Tiny pastes (URLs, single words) skip the placeholder and go in verbatim."""
        import sys
        import sage.core.validation_helpers as validation_mod
        import sage.core.exploration_helpers as exp_mod
        import sage.core.session_helpers as session_mod
        import sage.core.renderer as renderer_mod
        from prompt_toolkit.keys import Keys

        monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
        monkeypatch.setattr(sys.stdout, "isatty", lambda: True)

        small_paste = "https://example.com/api/v2/things"

        captured: dict = {"bindings": None, "buffer_text": ""}

        class FakeBuffer:
            def __init__(self) -> None:
                self.text = ""

            def insert_text(self, t: str) -> None:
                self.text += t

        class FakeEvent:
            def __init__(self, data: str, buf: FakeBuffer) -> None:
                self.data = data
                self.current_buffer = buf

        class FakeSession:
            def __init__(self, **kwargs) -> None:  # type: ignore[no-untyped-def]
                captured["bindings"] = kwargs.get("key_bindings")
                self._buf = FakeBuffer()

            def prompt(self, prompt_text: str) -> str:
                ev = FakeEvent(small_paste, self._buf)
                for b in captured["bindings"].bindings:
                    if Keys.BracketedPaste in b.keys:
                        b.handler(ev)
                        break
                captured["buffer_text"] = self._buf.text
                return self._buf.text

        monkeypatch.setattr("prompt_toolkit.PromptSession", FakeSession)

        reader = exp_mod._build_prompt_reader(tmp_path)
        result = reader("you> ")
        # Small paste goes in verbatim — no placeholder substitution
        assert captured["buffer_text"] == small_paste
        assert "[Pasted text" not in result
        assert result == small_paste


class TestBuildModelPicker:
    """Tests for the slow-model -> fast-model auto-swap in build mode."""

    def test_picker_swaps_slow_qwen3_when_devstral_available(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        import sage.core.validation_helpers as validation_mod
        import sage.core.exploration_helpers as exp_mod
        import sage.core.session_helpers as session_mod
        import sage.core.renderer as renderer_mod

        monkeypatch.setattr("sage.core.session_helpers._ollama_local_models", lambda: {
            "devstral:latest", "llama3.2:latest", "qwen3-coder-next:latest",
        })
        new_id, reason = validation_mod._pick_build_model("ollama:qwen3-coder-next:latest")
        assert new_id == "ollama:devstral:latest"
        assert reason is not None
        assert "qwen3-coder-next" in reason
        assert "devstral" in reason

    def test_picker_keeps_already_fast_model(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        import sage.core.validation_helpers as validation_mod
        import sage.core.exploration_helpers as exp_mod
        import sage.core.session_helpers as session_mod
        import sage.core.renderer as renderer_mod

        monkeypatch.setattr("sage.core.session_helpers._ollama_local_models", lambda: {
            "devstral:latest", "llama3.2:latest",
        })
        new_id, reason = validation_mod._pick_build_model("ollama:devstral:latest")
        assert new_id == "ollama:devstral:latest"
        assert reason is None

    def test_picker_keeps_cloud_models_alone(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        import sage.core.validation_helpers as validation_mod
        import sage.core.exploration_helpers as exp_mod
        import sage.core.session_helpers as session_mod
        import sage.core.renderer as renderer_mod

        monkeypatch.setattr("sage.core.session_helpers._ollama_local_models", lambda: set())
        new_id, reason = validation_mod._pick_build_model("anthropic:claude-sonnet-4-6")
        assert new_id == "anthropic:claude-sonnet-4-6"
        assert reason is None

    def test_picker_falls_back_to_llama32_when_devstral_unavailable(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        import sage.core.validation_helpers as validation_mod
        import sage.core.exploration_helpers as exp_mod
        import sage.core.session_helpers as session_mod
        import sage.core.renderer as renderer_mod

        monkeypatch.setattr("sage.core.session_helpers._ollama_local_models", lambda: {
            "llama3.2:latest", "qwen3-coder-next:latest",
        })
        new_id, reason = validation_mod._pick_build_model("ollama:qwen3-coder-next:latest")
        assert new_id == "ollama:llama3.2:latest"
        assert reason is not None

    def test_picker_no_swap_when_no_fast_model_available(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        import sage.core.validation_helpers as validation_mod
        import sage.core.exploration_helpers as exp_mod
        import sage.core.session_helpers as session_mod
        import sage.core.renderer as renderer_mod

        monkeypatch.setattr("sage.core.session_helpers._ollama_local_models", lambda: {
            "qwen3-coder-next:latest",  # only the slow one
        })
        new_id, reason = validation_mod._pick_build_model("ollama:qwen3-coder-next:latest")
        # No alternative — stays on the slow one (timeout extension still helps)
        assert new_id == "ollama:qwen3-coder-next:latest"
        assert reason is None


class TestRuntimeValidator:
    """Install + test pass: catches broken package.json before the user does."""

    def test_validate_node_project_returns_not_ran_without_package_json(
        self, tmp_path
    ) -> None:
        from sage.core.principal_engineer import validate_node_project

        result = validate_node_project(tmp_path)
        assert result["ran"] is False

    def test_validate_python_project_returns_not_ran_without_pyproject(
        self, tmp_path
    ) -> None:
        from sage.core.principal_engineer import validate_python_project

        result = validate_python_project(tmp_path)
        assert result["ran"] is False

    def test_build_runtime_fix_prompt_includes_error_and_files(self) -> None:
        from sage.core.principal_engineer import build_runtime_fix_prompt

        prompt = build_runtime_fix_prompt(
            "npm error ERESOLVE could not resolve @testing-library/react-native",
            {"package.json": '{"dependencies": {}}'},
        )
        assert "ERESOLVE" in prompt
        assert "package.json" in prompt
        assert "JSON object mapping each file path" in prompt
        assert "No prose, no markdown fences" in prompt


class TestRNWebInstallability:
    """The RN+Web plan must produce a package.json that npm install can
    actually resolve. Pin .npmrc + react-test-renderer to prevent the
    regression we saw with @testing-library/react-native peer-dep failure."""

    def test_plan_includes_npmrc_with_legacy_peer_deps(self) -> None:
        from sage.core.principal_engineer import plan_react_native_web

        npmrc = next(f for f in plan_react_native_web() if f.path == "frontend/.npmrc")
        assert npmrc.role is not None
        assert "legacy-peer-deps=true" in npmrc.role

    def test_package_json_includes_react_test_renderer(self) -> None:
        from sage.core.principal_engineer import plan_react_native_web, CURRENT_VERSIONS

        pkg = next(f for f in plan_react_native_web() if f.path == "frontend/package.json")
        assert pkg.role is not None
        # react-test-renderer is a peer of @testing-library/react-native;
        # missing it caused the install failure the user reported.
        assert "react-test-renderer" in pkg.role
        # Must pin to the same react version
        assert CURRENT_VERSIONS["expo"]["react"] in pkg.role


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
