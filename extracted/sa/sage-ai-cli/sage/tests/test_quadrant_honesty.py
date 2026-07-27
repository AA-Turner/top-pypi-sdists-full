"""The 4-point verification quadrant must not be able to lie.

Every test here builds a REAL project on disk, runs the REAL verifier
(`sage.core.install_verify`), and asserts on the verifier's verdict. No
subprocess is mocked, no command is stubbed, and no step result is
fabricated. If a toolchain is missing the test SKIPS with an explicit
reason — it never silently passes.

The properties under test, one per failure mode:

    install fails          → install_ok is False
    source does not compile→ build_ok   is False
    crashes on boot        → runs_ok    is False
    NO tests at all        → tests_ok   is False   ← the central case
    tests fail             → tests_ok   is False
    0 tests collected      → tests_ok   is False
    0-byte / wrong-magic   → media verification False
    everything genuinely OK→ all four True (positive control)

Each negative assertion is paired with a positive control on the same
axis, so none of them is a constant asserted against itself: the same
verifier applied to a working project must return True.
"""

from __future__ import annotations

import json
import math
import shutil
import struct
import sys
import wave
import zlib
from pathlib import Path

import pytest

from sage.core.install_verify import (
    DiscoveredProject,
    VerifyReport,
    count_tests_executed,
    discover_projects,
    verify_all,
    verify_media_report,
    verify_project,
)
from sage.core.media_verify import verify_media_file
from sage.core.validation_helpers import strict_aggregate_status


pytestmark = pytest.mark.slow


# ────────────────────────── fixtures / builders ──────────────────────────


def _python_project(
    root: Path,
    *,
    requirements: str = "",
    main_py: str | None = 'def hello():\n    return "hi"\n',
    tests: dict[str, str] | None = None,
) -> DiscoveredProject:
    """Materialise a real python project and return its DiscoveredProject."""
    root.mkdir(parents=True, exist_ok=True)
    (root / "requirements.txt").write_text(requirements, encoding="utf-8")
    if main_py is not None:
        (root / "main.py").write_text(main_py, encoding="utf-8")
    for name, body in (tests or {}).items():
        (root / name).write_text(body, encoding="utf-8")
    return DiscoveredProject(kind="python", root=root)


def _report(project: DiscoveredProject) -> VerifyReport:
    return VerifyReport(project=project, steps=verify_project(project))


def _named_steps(report: VerifyReport) -> list[tuple[str, bool]]:
    return [(s.name, s.ok) for s in report.steps]


# ═════════════════════════ 1. install_ok ═════════════════════════════════


class TestInstallOk:
    def test_broken_requirements_makes_install_ok_false(self, tmp_path: Path) -> None:
        """A requirements.txt pip cannot parse must fail install_ok.

        Uses a locally-detectable syntax error rather than a bogus package
        name so the assertion does not depend on network access.
        """
        project = _python_project(
            tmp_path / "bad_install",
            requirements="this is not a valid requirement specifier!!!\n",
            tests={"test_x.py": "def test_x():\n    assert True\n"},
        )
        report = _report(project)
        assert report.install_ok is False, (
            f"pip could not parse the requirements yet install_ok was "
            f"{report.install_ok}. steps={_named_steps(report)}"
        )

    def test_valid_requirements_makes_install_ok_true(self, tmp_path: Path) -> None:
        """Positive control on the same axis: an installable project passes."""
        project = _python_project(
            tmp_path / "good_install",
            requirements="",
            tests={"test_x.py": "def test_x():\n    assert True\n"},
        )
        report = _report(project)
        assert report.install_ok is True, (
            f"an empty (therefore satisfiable) requirements.txt should install. "
            f"steps={_named_steps(report)}"
        )


# ═════════════════════════ 2. build_ok ═══════════════════════════════════


class TestBuildOk:
    def test_syntax_error_makes_build_ok_false(self, tmp_path: Path) -> None:
        project = _python_project(
            tmp_path / "no_compile",
            main_py="def broken(:\n    return  # <- syntax error\n",
            tests={"test_x.py": "def test_x():\n    assert True\n"},
        )
        report = _report(project)
        assert report.build_ok is False, (
            f"source does not parse yet build_ok was {report.build_ok}. "
            f"steps={_named_steps(report)}"
        )

    def test_compiling_source_makes_build_ok_true(self, tmp_path: Path) -> None:
        project = _python_project(
            tmp_path / "compiles",
            tests={"test_x.py": "def test_x():\n    assert True\n"},
        )
        report = _report(project)
        assert report.build_ok is True, (
            f"valid python should compile. steps={_named_steps(report)}"
        )


# ═════════════════════════ 3. runs_ok ════════════════════════════════════


class TestRunsOk:
    def test_crash_on_import_makes_runs_ok_false(self, tmp_path: Path) -> None:
        """Compiles fine, explodes the moment it is executed."""
        project = _python_project(
            tmp_path / "crashes",
            main_py='raise RuntimeError("boom on boot")\n',
            tests={"test_x.py": "def test_x():\n    assert True\n"},
        )
        report = _report(project)
        assert report.build_ok is True, (
            "the crashing module must still COMPILE, otherwise this test is "
            f"measuring build_ok instead of runs_ok. steps={_named_steps(report)}"
        )
        assert report.runs_ok is False, (
            f"module raises on import yet runs_ok was {report.runs_ok}. "
            f"steps={_named_steps(report)}"
        )

    def test_clean_boot_makes_runs_ok_true(self, tmp_path: Path) -> None:
        project = _python_project(
            tmp_path / "boots",
            main_py='def hello():\n    return "hi"\n\n\nif __name__ == "__main__":\n    print(hello())\n',
            tests={"test_x.py": "def test_x():\n    assert True\n"},
        )
        report = _report(project)
        assert report.runs_ok is True, (
            f"a clean module should import and run. steps={_named_steps(report)}"
        )


# ═════════════ 4. tests_ok — the case the user cares most about ═══════════


class TestTestsOkNoTests:
    def test_project_with_zero_test_files_is_not_green(self, tmp_path: Path) -> None:
        """THE regression test.

        A project with no tests whatsoever used to produce a synthesized
        step named "<kind> test (not required)" with ok=True, which made
        `VerifyReport.tests_ok` — and therefore the whole quadrant —
        report success. Nothing had been tested.
        """
        project = _python_project(tmp_path / "no_tests", tests={})
        report = _report(project)

        assert report.tests_ok is False, (
            "a project with ZERO test files reported tests_ok=True. That is the "
            "false positive the quadrant exists to prevent. "
            f"steps={_named_steps(report)}"
        )
        # And no synthesized step may claim tests passed.
        for step in report.steps:
            if step.synthetic and "test" in step.name.lower():
                assert step.ok is False, (
                    f"synthetic step {step.name!r} claims tests passed without running any"
                )

    def test_zero_tests_also_fails_strict_aggregation(self, tmp_path: Path) -> None:
        """The build pipeline aggregates per-project reports; check that path too."""
        root = tmp_path / "ws"
        _python_project(root / "backend", tests={})
        reports = verify_all(root)
        assert reports, "discovery found no project to verify"
        assert strict_aggregate_status(reports, "tests_ok") is False, (
            f"aggregated tests_ok was not False for a workspace with no tests: "
            f"{[(r.project.kind, r.tests_ok) for r in reports]}"
        )

    def test_project_with_a_passing_test_is_green(self, tmp_path: Path) -> None:
        """Positive control: the same verifier says True when tests really run."""
        project = _python_project(
            tmp_path / "has_tests",
            tests={"test_ok.py": "from main import hello\n\n\ndef test_hello():\n    assert hello() == 'hi'\n"},
        )
        report = _report(project)
        assert report.tests_ok is True, (
            f"a real passing test suite must report tests_ok=True. steps={_named_steps(report)}"
        )
        assert report.tests_collected >= 1, "at least one test should have been counted"


class TestTestsOkFailingTests:
    def test_failing_test_makes_tests_ok_false(self, tmp_path: Path) -> None:
        project = _python_project(
            tmp_path / "failing_tests",
            tests={"test_bad.py": "def test_bad():\n    assert 1 == 2\n"},
        )
        report = _report(project)
        assert report.tests_ok is False, (
            f"a failing suite reported tests_ok={report.tests_ok}. steps={_named_steps(report)}"
        )

    def test_erroring_test_collection_makes_tests_ok_false(self, tmp_path: Path) -> None:
        """A test module that cannot even be imported is not a pass."""
        project = _python_project(
            tmp_path / "erroring_tests",
            tests={"test_boom.py": "import a_module_that_does_not_exist_xyzzy\n\n\ndef test_x():\n    assert True\n"},
        )
        report = _report(project)
        assert report.tests_ok is False, (
            f"collection error reported tests_ok={report.tests_ok}. steps={_named_steps(report)}"
        )


class TestTestsOkZeroCollected:
    def test_test_file_with_no_test_functions_is_not_green(self, tmp_path: Path) -> None:
        """pytest exits 5 ("no tests ran"). That is not success."""
        project = _python_project(
            tmp_path / "zero_collected",
            tests={"test_empty.py": "# a test module that declares no tests\nimport os  # noqa: F401\n"},
        )
        report = _report(project)
        pytest_steps = [s for s in report.steps if s.name == "pytest"]
        assert pytest_steps, f"pytest did not run at all: {_named_steps(report)}"
        assert pytest_steps[0].tests_collected == 0, (
            f"expected 0 collected, got {pytest_steps[0].tests_collected}"
        )
        assert report.tests_ok is False, (
            "pytest collected ZERO tests and exited 5, but tests_ok was True. "
            f"steps={_named_steps(report)}"
        )

    @pytest.mark.parametrize(
        ("runner", "log", "rc", "expected"),
        [
            ("pytest", "no tests ran in 0.01s", 5, 0),
            ("pytest", "collected 7 items\n7 passed", 0, 7),
            ("go test", "?   demo  [no test files]\n", 0, 0),
            ("go test", "=== RUN TestAdd\n--- PASS: TestAdd (0.00s)\nok   demo\n", 0, 1),
            ("cargo test", "running 0 tests\n\ntest result: ok. 0 passed", 0, 0),
            ("cargo test", "running 3 tests\n\ntest result: ok. 3 passed", 0, 3),
            ("swift test", "Executed 0 tests, with 0 failures", 0, 0),
            ("swift test", "Executed 4 tests, with 0 failures", 0, 4),
            ("ctest", "No tests were found!!!", 8, 0),
            ("ctest", "Total Tests: 5\n100% tests passed", 0, 5),
            ("dotnet test", "No test is available in project.dll", 1, 0),
            ("npm test", "No tests found, exiting with code 1", 1, 0),
            ("npm test", "Tests:       9 passed, 9 total", 0, 9),
            ("rspec", "0 examples, 0 failures", 0, 0),
            ("dart test", "No tests ran.", 0, 0),
        ],
    )
    def test_zero_test_output_is_recognised_per_runner(
        self, runner: str, log: str, rc: int, expected: int
    ) -> None:
        """Each runner's own "I ran nothing" wording must map to 0.

        This is what stops `go test` / `cargo test` / `swift test` — all of
        which exit ZERO on an empty suite — from reading as success.
        """
        assert count_tests_executed(runner, log, rc) == expected


# ═════════════════════ 5. media asset verification ═══════════════════════


def _real_png(path: Path, w: int = 4, h: int = 4) -> Path:
    def chunk(tag: bytes, data: bytes) -> bytes:
        return (
            struct.pack(">I", len(data))
            + tag
            + data
            + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        )

    raw = b"".join(b"\x00" + bytes([255, 0, 0] * w) for _ in range(h))
    path.write_bytes(
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(raw))
        + chunk(b"IEND", b"")
    )
    return path


def _real_wav(path: Path) -> Path:
    with wave.open(str(path), "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(8000)
        f.writeframes(
            b"".join(
                struct.pack("<h", int(20000 * math.sin(2 * math.pi * 440 * i / 8000)))
                for i in range(2000)
            )
        )
    return path


def _real_glb(path: Path) -> Path:
    doc = {
        "asset": {"version": "2.0"},
        "meshes": [{"primitives": [{"attributes": {"POSITION": 0}}]}],
        "nodes": [{"mesh": 0}],
        "scenes": [{"nodes": [0]}],
    }
    payload = json.dumps(doc).encode("utf-8")
    payload += b" " * ((4 - len(payload) % 4) % 4)
    path.write_bytes(
        b"glTF"
        + struct.pack("<II", 2, 12 + 8 + len(payload))
        + struct.pack("<I", len(payload))
        + b"JSON"
        + payload
    )
    return path


class TestMediaVerification:
    def test_zero_byte_asset_fails(self, tmp_path: Path) -> None:
        for name in ("a.png", "a.wav", "a.mp3", "a.mp4", "a.glb"):
            p = tmp_path / name
            p.write_bytes(b"")
            check = verify_media_file(p)
            assert check.ok is False, f"0-byte {name} passed verification: {check}"
            assert "0 bytes" in check.reason

    def test_the_historical_gltf_stub_fails(self, tmp_path: Path) -> None:
        """`b"glTF"` — the exact 4-byte stub an earlier bug wrote."""
        p = tmp_path / "model.glb"
        p.write_bytes(b"glTF")
        check = verify_media_file(p)
        assert check.ok is False, f"the 4-byte glTF stub passed verification: {check}"

    def test_the_historical_bare_png_header_fails(self, tmp_path: Path) -> None:
        """A bare 8-byte PNG signature with no IHDR/IDAT/IEND."""
        p = tmp_path / "sprite.png"
        p.write_bytes(b"\x89PNG\r\n\x1a\n")
        check = verify_media_file(p)
        assert check.ok is False, f"a bare PNG header passed verification: {check}"

    def test_png_header_padded_to_size_still_fails(self, tmp_path: Path) -> None:
        """Padding a stub past the size floor must not buy it a pass —
        the container structure is checked, not just the length."""
        p = tmp_path / "padded.png"
        p.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 4096)
        check = verify_media_file(p)
        assert check.ok is False, f"a padded PNG stub passed verification: {check}"

    def test_wrong_magic_bytes_fail(self, tmp_path: Path) -> None:
        cases = {
            "x.png": b"NOT-A-PNG" * 40,
            "x.wav": b"NOT-A-WAV" * 40,
            "x.mp4": b"NOT-AN-MP4" * 40,
            "x.glb": b"NOT-A-GLB-FILE-AT-ALL" * 40,
        }
        for name, blob in cases.items():
            p = tmp_path / name
            p.write_bytes(blob)
            check = verify_media_file(p)
            assert check.ok is False, f"{name} with wrong magic bytes passed: {check}"

    def test_truncated_wav_fails(self, tmp_path: Path) -> None:
        """A WAV whose RIFF size disagrees with the real file length."""
        good = _real_wav(tmp_path / "good.wav")
        blob = good.read_bytes()
        truncated = tmp_path / "truncated.wav"
        truncated.write_bytes(blob[: len(blob) // 2])
        check = verify_media_file(truncated)
        assert check.ok is False, f"a truncated WAV passed verification: {check}"

    def test_real_assets_pass(self, tmp_path: Path) -> None:
        """Positive control — the verifier is not simply rejecting everything."""
        for builder in (_real_png, _real_wav, _real_glb):
            suffix = {"_real_png": ".png", "_real_wav": ".wav", "_real_glb": ".glb"}[
                builder.__name__
            ]
            p = builder(tmp_path / f"asset{suffix}")
            check = verify_media_file(p)
            assert check.ok is True, f"a genuine {suffix} was rejected: {check}"

    def test_bad_asset_fails_the_quadrant(self, tmp_path: Path) -> None:
        """A stub asset must fail the quadrant, not just a standalone check."""
        _real_png(tmp_path / "fine.png")
        (tmp_path / "stub.glb").write_bytes(b"glTF")
        report = verify_media_report(tmp_path)
        assert report is not None, "media assets were present but produced no report"
        assert report.tests_ok is False, (
            f"a 4-byte glTF stub did not fail the media quadrant: {_named_steps(report)}"
        )
        assert report.build_ok is False

    def test_good_assets_pass_the_quadrant(self, tmp_path: Path) -> None:
        _real_png(tmp_path / "fine.png")
        _real_wav(tmp_path / "fine.wav")
        _real_glb(tmp_path / "fine.glb")
        report = verify_media_report(tmp_path)
        assert report is not None
        assert report.tests_ok is True, (
            f"genuine assets failed the media quadrant: {_named_steps(report)}"
        )

    def test_no_media_produces_no_media_report(self, tmp_path: Path) -> None:
        (tmp_path / "readme.txt").write_text("no assets here")
        assert verify_media_report(tmp_path) is None


# ═════════════════════════ 6. cross-language ═════════════════════════════


def _cxx_toolchain_works() -> tuple[bool, str]:
    """Probe whether CMAKE can configure, compile AND LINK a trivial C++ binary.

    Must go through cmake, not a bare `c++` invocation: cmake may select a
    different compiler (e.g. /usr/local/bin/g++-14) whose linker is broken
    even when clang++ works. A cmake positive-control test is meaningless
    if that path is broken, so the probe result is used to SKIP LOUDLY
    rather than let the test fail for an unrelated reason.
    """
    import subprocess
    import tempfile

    cmake = shutil.which("cmake")
    if not cmake:
        return False, "cmake is not on PATH"
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / "CMakeLists.txt").write_text(
            "cmake_minimum_required(VERSION 3.16)\n"
            "project(probe CXX)\n"
            "add_executable(probe main.cpp)\n"
        )
        (root / "main.cpp").write_text("int main() { return 0; }\n")
        build = root / "build"
        build.mkdir()
        try:
            cfg = subprocess.run(
                [cmake, ".."], cwd=build, capture_output=True, text=True,
                timeout=300, check=False,
            )
            if cfg.returncode != 0:
                return False, (
                    "cmake cannot configure a trivial C++ project on this machine: "
                    + (cfg.stderr or cfg.stdout or "").strip()[-400:]
                )
            bld = subprocess.run(
                [cmake, "--build", "."], cwd=build, capture_output=True, text=True,
                timeout=300, check=False,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            return False, f"cmake probe could not be run: {exc}"
    if bld.returncode != 0:
        return False, (
            "cmake cannot BUILD a trivial C++ project on this machine: "
            + (bld.stderr or bld.stdout or "").strip()[-400:]
        )
    return True, "ok"


_CXX_OK, _CXX_WHY = _cxx_toolchain_works()


def _requires(tool: str) -> pytest.MarkDecorator:
    """Skip LOUDLY (never silently pass) when a toolchain is absent."""
    return pytest.mark.skipif(
        shutil.which(tool) is None,
        reason=(
            f"TOOLCHAIN MISSING: {tool!r} is not on PATH, so this language's real "
            f"install/build/test commands cannot be executed. This test is SKIPPED, "
            f"NOT passed — install {tool} to verify this language."
        ),
    )


class TestCrossLanguage:
    @_requires("go")
    def test_go_no_test_files_is_not_green(self, tmp_path: Path) -> None:
        """`go test ./...` exits 0 for a package with no tests. Not a pass."""
        root = tmp_path / "gomod"
        root.mkdir()
        (root / "go.mod").write_text("module demo\n\ngo 1.21\n")
        (root / "main.go").write_text("package main\n\nfunc main() {}\n")
        report = _report(DiscoveredProject(kind="go", root=root))
        assert report.build_ok is True, f"go build should succeed: {_named_steps(report)}"
        assert report.tests_ok is False, (
            f"go project with no _test.go files reported tests_ok=True: {_named_steps(report)}"
        )

    @_requires("go")
    def test_go_with_a_real_test_is_green(self, tmp_path: Path) -> None:
        root = tmp_path / "gomod_tested"
        root.mkdir()
        (root / "go.mod").write_text("module demo\n\ngo 1.21\n")
        (root / "main.go").write_text(
            "package main\n\nfunc Add(a, b int) int { return a + b }\n\nfunc main() {}\n"
        )
        (root / "main_test.go").write_text(
            'package main\n\nimport "testing"\n\n'
            "func TestAdd(t *testing.T) {\n\tif Add(1, 2) != 3 {\n\t\tt.Fatal(\"bad\")\n\t}\n}\n"
        )
        report = _report(DiscoveredProject(kind="go", root=root))
        assert report.tests_ok is True, (
            f"a real passing go test reported tests_ok=False: {_named_steps(report)}"
        )

    @_requires("cargo")
    def test_rust_no_tests_is_not_green(self, tmp_path: Path) -> None:
        """`cargo test` exits 0 with "running 0 tests". Not a pass."""
        root = tmp_path / "crate"
        (root / "src").mkdir(parents=True)
        (root / "Cargo.toml").write_text(
            '[package]\nname = "demo"\nversion = "0.1.0"\nedition = "2021"\n'
        )
        (root / "src" / "main.rs").write_text('fn main() { println!("hi"); }\n')
        report = _report(DiscoveredProject(kind="rust", root=root))
        assert report.build_ok is True, f"cargo build should succeed: {_named_steps(report)}"
        assert report.tests_ok is False, (
            f"rust crate with no #[test] reported tests_ok=True: {_named_steps(report)}"
        )

    @_requires("cargo")
    def test_rust_with_a_real_test_is_green(self, tmp_path: Path) -> None:
        root = tmp_path / "crate_tested"
        (root / "src").mkdir(parents=True)
        (root / "Cargo.toml").write_text(
            '[package]\nname = "demo"\nversion = "0.1.0"\nedition = "2021"\n'
        )
        (root / "src" / "main.rs").write_text(
            "fn add(a: i32, b: i32) -> i32 { a + b }\n\n"
            'fn main() { println!("{}", add(1, 2)); }\n\n'
            "#[cfg(test)]\nmod tests {\n    use super::*;\n"
            "    #[test]\n    fn it_adds() { assert_eq!(add(1, 2), 3); }\n}\n"
        )
        report = _report(DiscoveredProject(kind="rust", root=root))
        assert report.tests_ok is True, (
            f"a real passing cargo test reported tests_ok=False: {_named_steps(report)}"
        )

    @_requires("node")
    def test_node_placeholder_test_script_is_not_green(self, tmp_path: Path) -> None:
        """npm's default `"test": "echo ... && exit 1"` proves nothing."""
        root = tmp_path / "nodeapp"
        root.mkdir()
        (root / "package.json").write_text(
            json.dumps(
                {
                    "name": "demo",
                    "version": "1.0.0",
                    "scripts": {"test": 'echo "Error: no test specified" && exit 1'},
                }
            )
        )
        (root / "index.js").write_text("module.exports = { add: (a, b) => a + b };\n")
        report = _report(DiscoveredProject(kind="node", root=root))
        assert report.tests_ok is False, (
            f"npm placeholder test script reported tests_ok=True: {_named_steps(report)}"
        )

    @_requires("node")
    def test_node_missing_test_script_is_not_green(self, tmp_path: Path) -> None:
        root = tmp_path / "nodeapp2"
        root.mkdir()
        (root / "package.json").write_text(
            json.dumps({"name": "demo", "version": "1.0.0", "scripts": {}})
        )
        (root / "index.js").write_text("module.exports = 1;\n")
        report = _report(DiscoveredProject(kind="node", root=root))
        assert report.tests_ok is False, (
            f"node project with no test script reported tests_ok=True: {_named_steps(report)}"
        )

    @_requires("node")
    def test_node_with_a_real_node_test_is_green(self, tmp_path: Path) -> None:
        root = tmp_path / "nodeapp3"
        root.mkdir()
        (root / "package.json").write_text(
            json.dumps(
                {
                    "name": "demo",
                    "version": "1.0.0",
                    "scripts": {"test": "node --test"},
                }
            )
        )
        (root / "index.js").write_text("module.exports = { add: (a, b) => a + b };\n")
        (root / "index.test.js").write_text(
            "const test = require('node:test');\n"
            "const assert = require('node:assert');\n"
            "const { add } = require('./index.js');\n"
            "test('add', () => { assert.strictEqual(add(1, 2), 3); });\n"
        )
        report = _report(DiscoveredProject(kind="node", root=root))
        assert report.tests_ok is True, (
            f"a real passing node --test suite reported tests_ok=False: {_named_steps(report)}"
        )

    @_requires("cmake")
    def test_cpp_without_add_test_is_not_green(self, tmp_path: Path) -> None:
        root = tmp_path / "cpp"
        root.mkdir()
        (root / "CMakeLists.txt").write_text(
            "cmake_minimum_required(VERSION 3.16)\n"
            "project(demo CXX)\n"
            "add_executable(demo main.cpp)\n"
        )
        (root / "main.cpp").write_text("int main() { return 0; }\n")
        report = _report(DiscoveredProject(kind="cpp", root=root))
        assert report.tests_ok is False, (
            "a CMake project that never calls add_test() reported tests_ok=True: "
            f"{_named_steps(report)}"
        )

    @_requires("cmake")
    @pytest.mark.skipif(
        not _CXX_OK,
        reason=(
            "TOOLCHAIN BROKEN: cannot compile/link C++ on this machine, so a cmake "
            "positive-control cannot be run. This test is SKIPPED, NOT passed. "
            f"Reason: {_CXX_WHY}"
        ),
    )
    def test_cpp_with_ctest_is_green(self, tmp_path: Path) -> None:
        root = tmp_path / "cpp_tested"
        root.mkdir()
        (root / "CMakeLists.txt").write_text(
            "cmake_minimum_required(VERSION 3.16)\n"
            "project(demo CXX)\n"
            "add_executable(demo main.cpp)\n"
            "enable_testing()\n"
            "add_test(NAME runs COMMAND demo)\n"
        )
        (root / "main.cpp").write_text("int main() { return 0; }\n")
        report = _report(DiscoveredProject(kind="cpp", root=root))
        assert report.build_ok is True, f"cmake build failed: {_named_steps(report)}"
        assert report.tests_ok is True, (
            f"a real ctest run reported tests_ok=False: {_named_steps(report)}"
        )

    @_requires("swift")
    def test_swift_without_tests_dir_is_not_green(self, tmp_path: Path) -> None:
        root = tmp_path / "swiftpkg"
        (root / "Sources" / "demo").mkdir(parents=True)
        (root / "Package.swift").write_text(
            "// swift-tools-version:5.7\nimport PackageDescription\n"
            'let package = Package(name: "demo", targets: [.target(name: "demo")])\n'
        )
        (root / "Sources" / "demo" / "main.swift").write_text('print("hi")\n')
        report = _report(DiscoveredProject(kind="swift", root=root))
        assert report.tests_ok is False, (
            f"swift package with no Tests/ reported tests_ok=True: {_named_steps(report)}"
        )

    def test_static_html_without_a_test_runner_is_not_green(self, tmp_path: Path) -> None:
        """A .html deliverable is verified too — and gets no free pass."""
        root = tmp_path / "site"
        root.mkdir()
        (root / "index.html").write_text(
            "<html><body><h1>Hello</h1><script>const x = 1;</script></body></html>\n"
        )
        projects = discover_projects(root)
        assert [p.kind for p in projects] == ["static-web"], (
            f"a bare index.html was not discovered as a project: {projects}"
        )
        report = _report(projects[0])
        assert report.build_ok is True, (
            f"well-formed HTML should pass the structure check: {_named_steps(report)}"
        )
        assert report.tests_ok is False, (
            f"a static site with no test runner reported tests_ok=True: {_named_steps(report)}"
        )

    def test_malformed_html_fails_build(self, tmp_path: Path) -> None:
        root = tmp_path / "badsite"
        root.mkdir()
        (root / "index.html").write_text("<html><body><h1>Hello</h1>\n")  # never closed
        report = _report(DiscoveredProject(kind="static-web", root=root))
        assert report.build_ok is False, (
            f"unclosed <html>/<body> passed the structure check: {_named_steps(report)}"
        )


# ═══════════════════ 7. structural guarantees ════════════════════════════


class TestStructuralGuarantees:
    def test_no_synthetic_step_can_assert_tests_passed(self, tmp_path: Path) -> None:
        """Whatever the project kind, a synthesized test step is never ok."""
        kinds = [
            "python", "node", "go", "rust", "java", "kotlin",
            "ruby", "swift", "dart", "cpp", "csharp", "static-web",
        ]
        empty = tmp_path / "empty"
        empty.mkdir()
        for kind in kinds:
            steps = verify_project(DiscoveredProject(kind=kind, root=empty))
            report = VerifyReport(
                project=DiscoveredProject(kind=kind, root=empty), steps=steps
            )
            assert report.tests_ok is False, (
                f"{kind}: an empty directory reported tests_ok=True: "
                f"{[(s.name, s.ok, s.synthetic) for s in steps]}"
            )

    def test_every_project_kind_emits_a_test_step(self, tmp_path: Path) -> None:
        """tests_ok must be well-defined, so a test step always exists."""
        from sage.core.install_verify import is_test_step

        empty = tmp_path / "empty2"
        empty.mkdir()
        for kind in ("python", "node", "go", "rust", "swift", "cpp", "static-web"):
            steps = verify_project(DiscoveredProject(kind=kind, root=empty))
            assert any(is_test_step(s.name) for s in steps), (
                f"{kind} produced no test step at all: {[s.name for s in steps]}"
            )

    def test_no_sage_testing_bypass_in_production_source(self) -> None:
        """No env-var may short-circuit real command execution."""
        core = Path(__file__).resolve().parent.parent / "core"
        offenders: list[str] = []
        for py in core.rglob("*.py"):
            try:
                text = py.read_text("utf-8", errors="replace")
            except OSError:
                continue
            for needle in ("SAGE_TESTING", "SAGE_REAL_COMMANDS"):
                if needle in text:
                    offenders.append(f"{py.relative_to(core)}: {needle}")
        assert not offenders, (
            "production source references a test-mode env var that could bypass "
            f"real execution: {offenders}"
        )

    def test_run_step_really_executes(self, tmp_path: Path) -> None:
        """Sanity: the step runner is not a stub."""
        from sage.core.install_verify import run_step

        marker = tmp_path / "proof.txt"
        res = run_step(
            "probe", [sys.executable, "-c", f"open({str(marker)!r}, 'w').write('ran')"],
            cwd=tmp_path,
        )
        assert res.ok, res.log
        assert marker.read_text() == "ran", "run_step did not actually execute the command"


# ═════════════════ 8. TDD is the DEFAULT generation order ════════════════


class TestTddIsTheDefault:
    """Sage must write the test for a feature BEFORE the code it covers."""

    def _slots(self):
        from sage.core.project_layout import FileSlot

        return [
            FileSlot(path="backend/app/api/v1/orders.py", role="api", language="python",
                     feature="orders"),
            FileSlot(path="backend/tests/unit/test_orders_service.py", role="tests",
                     language="python", feature="orders", is_test=True),
            FileSlot(path="backend/app/models/orders.py", role="model", language="python",
                     feature="orders"),
            FileSlot(path="backend/tests/integration/test_orders_api.py", role="tests",
                     language="python", feature="orders", is_test=True),
            FileSlot(path="backend/app/services/orders.py", role="service", language="python",
                     feature="orders"),
        ]

    def test_default_is_tdd_first(self) -> None:
        from sage.core.principal_builder import TDD_FIRST_DEFAULT, _sort_for_generation

        assert TDD_FIRST_DEFAULT is True, "TDD ordering must be ON by default"
        ordered = _sort_for_generation(self._slots())
        flags = [sl.is_test for sl in ordered]
        assert flags == sorted(flags, reverse=True), (
            f"tests must be generated first; got {[(sl.path, sl.is_test) for sl in ordered]}"
        )
        first_impl = next(i for i, sl in enumerate(ordered) if not sl.is_test)
        assert first_impl == 2, "both test files should precede all implementation files"

    def test_build_entrypoint_defaults_to_tdd(self) -> None:
        """The public build function's default really is TDD, not just the constant."""
        import inspect

        from sage.core.principal_builder import (
            _build_project_principal_inner,
            build_project_principal,
        )

        for fn in (build_project_principal, _build_project_principal_inner):
            param = inspect.signature(fn).parameters["tdd_first"]
            assert param.default is True, f"{fn.__name__} does not default to TDD"

    def test_opt_out_restores_legacy_order(self) -> None:
        from sage.core.principal_builder import _sort_for_generation

        ordered = _sort_for_generation(self._slots(), tdd_first=False)
        flags = [sl.is_test for sl in ordered]
        assert flags == sorted(flags), (
            f"tdd_first=False must put tests last; got {[(sl.path, sl.is_test) for sl in ordered]}"
        )

    def test_layer_topology_is_preserved_within_implementation(self) -> None:
        """TDD ordering must not destroy model→service→api dependency order."""
        from sage.core.principal_builder import _sort_for_generation

        ordered = [sl.path for sl in _sort_for_generation(self._slots()) if not sl.is_test]
        assert ordered.index("backend/app/models/orders.py") < ordered.index(
            "backend/app/services/orders.py"
        ) < ordered.index("backend/app/api/v1/orders.py"), ordered

    def test_test_file_is_pinned_into_the_implementation_prompt(self, tmp_path: Path) -> None:
        """The implementation prompt must SEE the test it has to satisfy.

        Tests are written first, so without pinning they fall out of the
        3-most-recent sibling window before the code is generated.
        """
        from sage.core.principal_builder import _read_sibling_context

        (tmp_path / "test_first.py").write_text("def test_contract():\n    assert add(1, 2) == 3\n")
        recents = []
        for i in range(5):
            name = f"filler_{i}.py"
            (tmp_path / name).write_text(f"# filler {i}\n")
            recents.append(name)

        unpinned = _read_sibling_context(tmp_path, recents)
        assert "test_first.py" not in unpinned, "precondition: it should have scrolled out"

        pinned = _read_sibling_context(tmp_path, recents, pinned=("test_first.py",))
        assert "test_first.py" in pinned, (
            "the feature's test was not pinned into the implementation prompt"
        )
        assert "assert add(1, 2) == 3" in pinned["test_first.py"]
        assert list(pinned)[0] == "test_first.py", "pinned test should lead the prompt"
