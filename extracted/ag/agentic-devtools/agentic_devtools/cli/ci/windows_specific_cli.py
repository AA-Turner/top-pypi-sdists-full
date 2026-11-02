"""Private command dispatch for trusted Windows-specific CI orchestration."""

from __future__ import annotations

import argparse
import ast
import json
import os
import subprocess
import sys
from collections.abc import Collection, Mapping, Sequence
from pathlib import Path
from typing import Literal, Never, Protocol, TypeVar, cast

from agentic_devtools.cli.ci.windows_fixture_bytes import verify_fixture_bytes
from agentic_devtools.cli.ci.windows_process_tree import ProcessCleanupError

POut = TypeVar("POut", covariant=True)
PIn = TypeVar("PIn", contravariant=True)
GOut = TypeVar("GOut", bound=Literal["setup-check", "portability", "benchmark"], covariant=True)
GIn = TypeVar("GIn", bound=Literal["setup-check", "portability", "benchmark"], contravariant=True)
RIn = TypeVar("RIn", bound=Literal["success", "failure", "cancelled", "skipped"], contravariant=True)
_P = str | Path
type _G[T] = Collection[T]
_R = dict[str, bool | list[str] | int]
_S = Mapping[str, object]
_E = dict[str, bool | str]


class _LoadPolicy(Protocol[POut, GIn]):
    def __call__(self, m: _P, b: _P, h: _P, /, *, applicable_groups: _G[GIn], bootstrap: bool) -> POut: ...


class _SelectGroups(Protocol[GOut]):
    def __call__(self, changed_paths: Sequence[str]) -> tuple[frozenset[GOut], bool]: ...


class _RunSelectedTests(Protocol[PIn, GIn]):
    def __call__(self, root: _P, policy: PIn, groups: _G[GIn], /, *, junit_path: _P) -> _R: ...


class _EvaluateGate(Protocol[RIn]):
    def __call__(self, selection: _S, linux: RIn | None, windows: RIn | None, /) -> _E: ...


def _check_bindings(tree: ast.Module, allowed_targets: set[int], expectation_names: set[str]) -> None:
    """Reject expectation bindings other than the approved literal targets."""
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, (ast.Store, ast.Del)):
            if node.id in expectation_names and id(node) not in allowed_targets:
                raise ValueError("Additional expectation binding or deletion")
        # Some Python bindings are string fields rather than Name(Store) nodes.
        names: Sequence[str | None]
        if isinstance(node, ast.alias):
            if node.name == "*":
                raise ValueError("Wildcard imports may rebind policy expectations")
            names = [node.asname or node.name.split(".")[0]]
        elif isinstance(node, ast.arg):
            names = [node.arg]
        elif isinstance(node, (ast.Global, ast.Nonlocal)):
            names = node.names
        else:
            names = [getattr(node, "name", None), getattr(node, "rest", None)]
        if any(name in expectation_names for name in names):
            raise ValueError("Additional expectation binding")


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    """Reject duplicate JSON keys at every nesting level."""
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON object key: {key}")
        result[key] = value
    return result


class _Dispatcher[
    PolicyT,
    GroupT: Literal["setup-check", "portability", "benchmark"],
    ResultT: Literal["success", "failure", "cancelled", "skipped"],
]:
    def __init__(
        self,
        load_policy: _LoadPolicy[PolicyT, GroupT],
        select_groups: _SelectGroups[GroupT],
        run_selected_tests: _RunSelectedTests[PolicyT, GroupT],
        evaluate_gate: _EvaluateGate[ResultT],
    ) -> None:
        self._load_policy = load_policy
        self._select_groups = select_groups
        self._run_selected_tests = run_selected_tests
        self._evaluate_gate = evaluate_gate
        self._product_group_order = ("setup-check", "portability", "benchmark")

    def _emit(self, payload: Mapping[str, object], status: int = 0) -> int:
        print(json.dumps(payload, separators=(",", ":")))
        return status

    def _fail(self, error_code: str, detail: object, status: int = 1) -> int:
        print(str(detail), file=sys.stderr)
        return self._emit({"ok": False, "error_code": error_code}, status)

    def _missing_file_code(self, exc: FileNotFoundError, base_policy: str, manifest: str, head_policy: str) -> str:
        if not isinstance(exc.filename, str):
            return "policy_io_failed"
        path = Path(exc.filename)
        if path == Path(base_policy):
            return "base_policy_missing"
        if path == Path(manifest):
            return "manifest_missing"
        if path == Path(head_policy):
            return "head_policy_missing"
        return "policy_io_failed"

    def _decode_json(self, raw: str, error_code: str) -> tuple[object | None, int | None]:
        try:
            return json.loads(raw, object_pairs_hook=_unique_object), None
        except ValueError as exc:
            return None, self._fail(error_code, exc)

    def _retry_select_policy(
        self, manifest: str, base_policy: str, head_policy: str, groups: frozenset[GroupT]
    ) -> tuple[int, bool]:
        try:
            self._load_policy(
                manifest,
                base_policy,
                head_policy,
                applicable_groups=groups,
                bootstrap=True,
            )
        except FileNotFoundError as exc:
            return self._fail(self._missing_file_code(exc, base_policy, manifest, head_policy), exc), False
        except ValueError as exc:
            return self._fail("bootstrap_not_allowed", exc), False
        except OSError as exc:
            return self._fail("policy_io_failed", exc), False
        return 0, True

    def _select_policy(
        self, manifest: str, base_policy: str, head_policy: str, groups: frozenset[GroupT], bootstrap: bool
    ) -> tuple[int, bool]:
        try:
            self._load_policy(
                manifest,
                base_policy,
                head_policy,
                applicable_groups=groups,
                bootstrap=False,
            )
        except FileNotFoundError as exc:
            code = self._missing_file_code(exc, base_policy, manifest, head_policy)
            if code == "base_policy_missing" and bootstrap and not groups:
                return self._retry_select_policy(manifest, base_policy, head_policy, groups)
            return self._fail(code, exc), False
        except ValueError as exc:
            return self._fail("policy_invalid", exc), False
        except OSError as exc:
            return self._fail("policy_io_failed", exc), False
        if bootstrap:
            return self._fail(
                "bootstrap_not_allowed", "--bootstrap is not allowed when the trusted base policy exists"
            ), False
        return 0, False

    def _select(self, args: argparse.Namespace) -> int:
        changed_paths, status = self._decode_json(args.changed_paths_json, "changed_paths_failed")
        if status is not None:
            return status
        if not isinstance(changed_paths, list) or any(not isinstance(path, str) for path in changed_paths):
            return self._fail("changed_paths_failed", "Changed paths must be a JSON array of strings")
        try:
            applicable_groups, contract_required = self._select_groups(changed_paths)
        except ValueError as exc:
            return self._fail("changed_paths_failed", exc)
        base_policy = os.environ.get("WINDOWS_CI_BASE_POLICY")
        if not base_policy:
            return self._fail("base_policy_unset", "WINDOWS_CI_BASE_POLICY must name the trusted base policy")
        status, bootstrap_allowed = self._select_policy(
            args.manifest, base_policy, args.head_policy, applicable_groups, args.bootstrap
        )
        if status:
            return status
        return self._emit(
            {
                "ok": True,
                "product_groups": [group for group in self._product_group_order if group in applicable_groups],
                "contract_required": contract_required,
                "windows_required": bool(applicable_groups),
                "bootstrap_allowed": bootstrap_allowed,
            }
        )

    def _validate_groups(self, groups: object) -> list[GroupT] | None:
        if not isinstance(groups, list):
            return None
        for group in groups:
            if not isinstance(group, str) or group not in self._product_group_order:
                return None
        if len(set(groups)) != len(groups):
            return None
        if groups != [group for group in self._product_group_order if group in groups]:
            return None
        return cast(list[GroupT], groups)

    def _validate_run_selection(self, selection: object) -> list[GroupT] | None:
        keys = {"ok", "product_groups", "contract_required", "windows_required", "bootstrap_allowed"}
        if not isinstance(selection, dict) or set(selection) != keys or selection.get("ok") is not True:
            return None
        groups = self._validate_groups(selection.get("product_groups"))
        if groups is None:
            return None
        if any(
            not isinstance(selection.get(key), bool)
            for key in ("contract_required", "windows_required", "bootstrap_allowed")
        ):
            return None
        if selection["windows_required"] != bool(groups):
            return None
        if groups and selection["bootstrap_allowed"]:
            return None
        return groups

    def _load_run_policy(
        self, manifest: str, base_policy: str, head_policy: str, groups: list[GroupT]
    ) -> tuple[int, PolicyT | None]:
        try:
            policy = self._load_policy(
                manifest,
                base_policy,
                head_policy,
                applicable_groups=groups,
                bootstrap=False,
            )
        except FileNotFoundError as exc:
            return self._fail(self._missing_file_code(exc, base_policy, manifest, head_policy), exc), None
        except ValueError as exc:
            return self._fail("policy_invalid", exc), None
        except OSError as exc:
            return self._fail("policy_io_failed", exc), None
        return 0, policy

    @staticmethod
    def _test_failure_detail(
        exc: subprocess.TimeoutExpired | ProcessCleanupError | subprocess.CalledProcessError | OSError,
    ) -> str:
        if isinstance(exc, subprocess.TimeoutExpired):
            detail = f"Test subprocess timed out: {exc}"
            stdout = exc.output.decode(errors="replace") if isinstance(exc.output, bytes) else exc.output
            stderr = exc.stderr.decode(errors="replace") if isinstance(exc.stderr, bytes) else exc.stderr
        elif isinstance(exc, ProcessCleanupError):
            detail = "Test subprocess cleanup failed"
            stdout, stderr = exc.completed_process.stdout, exc.completed_process.stderr
        else:
            if isinstance(exc, subprocess.CalledProcessError):
                detail = f"Test subprocess failed with exit status {exc.returncode}: {exc}"
            else:
                detail = str(exc)
            stdout, stderr = getattr(exc, "output", None), getattr(exc, "stderr", None)
            stdout = stdout.decode(errors="replace") if isinstance(stdout, bytes) else stdout
            stderr = stderr.decode(errors="replace") if isinstance(stderr, bytes) else stderr
        if stdout:
            detail += f"\nstdout:\n{stdout}"
        if stderr:
            detail += f"\nstderr:\n{stderr}"
        for diagnostic in getattr(exc, "cleanup_errors", ()):
            detail += f"\ncleanup: {diagnostic.stage}: {diagnostic.message}"
        return detail

    def _execute_tests(self, args: argparse.Namespace, policy: PolicyT, groups: list[GroupT]) -> int:
        try:
            result = self._run_selected_tests(args.root, policy, groups, junit_path=args.junit)
        except (subprocess.TimeoutExpired, ProcessCleanupError) as exc:
            return self._fail("test_process_failed", self._test_failure_detail(exc))
        except subprocess.CalledProcessError as exc:
            return self._fail("test_process_failed", self._test_failure_detail(exc), exc.returncode)
        except ValueError as exc:
            return self._fail("test_validation_failed", exc)
        except OSError as exc:
            return self._fail("test_io_failed", self._test_failure_detail(exc))
        return self._emit(
            {
                "ok": True,
                "collected_ids": result["collected_ids"],
                "executed_ids": result["executed_ids"],
                "skipped": result["skipped"],
            }
        )

    def _run(self, args: argparse.Namespace) -> int:
        selection, status = self._decode_json(args.selection_json, "selection_failed")
        if status is not None:
            return status
        groups = self._validate_run_selection(selection)
        if groups is None:
            return self._fail("selection_failed", "Run requires a successful select result")
        if not groups:
            return self._fail("no_product_groups", "No Windows product groups apply")
        base_policy = os.environ.get("WINDOWS_CI_BASE_POLICY")
        if not base_policy:
            return self._fail("base_policy_unset", "WINDOWS_CI_BASE_POLICY must name the trusted base policy")
        status, policy = self._load_run_policy(args.manifest, base_policy, args.head_policy, groups)
        if status:
            return status
        return self._execute_tests(args, cast(PolicyT, policy), groups)

    def _gate(self, args: argparse.Namespace) -> int:
        selection, status = self._decode_json(args.selection_json, "selection_failed")
        if status is not None:
            return status
        result = self._evaluate_gate(
            cast(_S, selection),
            cast(ResultT | None, args.linux_result),
            cast(ResultT | None, args.windows_result),
        )
        return self._emit(result, 0 if result.get("ok") is True else 1)

    def _verify_fixtures(self, args: argparse.Namespace) -> int:
        try:
            files_checked = verify_fixture_bytes(args.commit, Path(args.root))
        except subprocess.CalledProcessError as exc:
            detail = str(exc)
            for label, output in (("stdout", exc.stdout), ("stderr", exc.stderr)):
                if output:
                    detail += f"\n{label}:\n{os.fsdecode(output)}"
            return self._fail("fixture_audit_failed", detail)
        except (ValueError, FileNotFoundError, NotADirectoryError, OSError) as exc:
            return self._fail("fixture_audit_failed", exc)
        return self._emit({"ok": True, "files_checked": files_checked})

    def run(self, argv: Sequence[str] | None) -> int:
        class _JsonArgumentParser(argparse.ArgumentParser):
            def error(self, message: str) -> Never:
                self.print_usage(sys.stderr)
                print(f"{self.prog}: error: {message}", file=sys.stderr)
                print(json.dumps({"ok": False, "error_code": "invalid_arguments"}, separators=(",", ":")))
                self.exit(2)

        parser = _JsonArgumentParser(description="Run focused trusted Windows CI commands")
        commands = parser.add_subparsers(dest="command", required=True)

        select_parser = commands.add_parser("select")
        select_parser.add_argument("--changed-paths-json", required=True)
        select_parser.add_argument("--manifest", required=True)
        select_parser.add_argument("--head-policy", required=True)
        select_parser.add_argument("--bootstrap", action="store_true")

        run_parser = commands.add_parser("run")
        run_parser.add_argument("--selection-json", required=True)
        run_parser.add_argument("--manifest", required=True)
        run_parser.add_argument("--head-policy", required=True)
        run_parser.add_argument("--root", required=True)
        run_parser.add_argument("--junit", required=True)

        gate_parser = commands.add_parser("gate")
        gate_parser.add_argument("--selection-json", required=True)
        gate_parser.add_argument("--linux-result")
        gate_parser.add_argument("--windows-result")

        fixture_parser = commands.add_parser("verify-fixtures")
        fixture_parser.add_argument("--commit", required=True)
        fixture_parser.add_argument("--root", required=True)

        args = parser.parse_args(argv)
        return {
            "select": self._select,
            "run": self._run,
            "gate": self._gate,
            "verify-fixtures": self._verify_fixtures,
        }[args.command](args)


def _run_cli[
    PolicyT,
    GroupT: Literal["setup-check", "portability", "benchmark"],
    ResultT: Literal["success", "failure", "cancelled", "skipped"],
](
    argv: Sequence[str] | None,
    *,
    load_policy: _LoadPolicy[PolicyT, GroupT],
    select_groups: _SelectGroups[GroupT],
    run_selected_tests: _RunSelectedTests[PolicyT, GroupT],
    evaluate_gate: _EvaluateGate[ResultT],
) -> int:
    """Dispatch through the private typed command handler."""
    return _Dispatcher(load_policy, select_groups, run_selected_tests, evaluate_gate).run(argv)
