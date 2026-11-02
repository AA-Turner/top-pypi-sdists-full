import os
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from agentic_devtools.cli.ci.windows_selector_policy import V2_EXTENSION_EXPANSIONS, V2_EXTENSION_SELECTORS
from agentic_devtools.cli.ci.windows_specific import (
    _FROZEN_V1_EXPANSIONS as V1_EXPANSIONS,
)
from agentic_devtools.cli.ci.windows_specific import (
    _FROZEN_V1_SELECTORS as V1_SELECTORS,
)
from agentic_devtools.cli.ci.windows_specific import (
    SelectorPolicy,
    run_selected_tests,
)


def _policy():
    return SelectorPolicy(V1_SELECTORS, tuple(V1_EXPANSIONS.items()))


def _v2_policy():
    return SelectorPolicy(
        (*V1_SELECTORS[:-1], *V2_EXTENSION_SELECTORS, V1_SELECTORS[-1]),
        (*V1_EXPANSIONS.items(), *V2_EXTENSION_EXPANSIONS),
    )


def _selected_ids(policy, groups):
    group_by_index = ("setup-check",) * 2 + ("portability",) * (len(policy.selectors) - 3) + ("benchmark",)
    result = []
    for index, selector in enumerate(policy.selectors):
        if group_by_index[index] not in groups:
            continue
        params = dict(policy.expansions).get(selector)
        result.extend([f"{selector}[{item}]" for item in params] if params else [selector])
    return result


def _collection(ids):
    return "\n".join([*ids, f"{len(ids)} {'test' if len(ids) == 1 else 'tests'} collected"])


def _junit(ids):
    suite = ET.Element("testsuite")
    for node_id in ids:
        selector = node_id.split("[", 1)[0]
        module, *parts = selector.split("::")
        classname = ".".join([*Path(module).with_suffix("").parts, *parts[:-1]])
        name = parts[-1] + node_id[len(selector) :]
        ET.SubElement(suite, "testcase", classname=classname, name=name)
    return ET.tostring(suite, encoding="unicode")


@pytest.mark.parametrize("policy", [_policy(), _v2_policy()])
def test_runs_exact_selected_tests_with_shared_child_environment(tmp_path, monkeypatch, policy):
    root = tmp_path / "pr-checkout"
    root.mkdir()
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("AGDT_RUN_PHASE0_REVIEW_BENCHMARK", "0")
    groups = {"setup-check", "portability", "benchmark"}
    ids = _selected_ids(policy, groups)
    if len(policy.selectors) == 19:
        assert {
            "tests/unit/cli/checks/changed_files/test_find_consumer_test_paths.py"
            "::TestFindConsumerTestPaths::test_windows_conftest_path_returns_posix_directory",
            "tests/unit/cli/checks/changed_files/test_find_consumer_test_paths.py"
            "::TestFindConsumerTestPaths::test_helper_consumers_are_sorted_posix_paths[consumer_names0]",
            "tests/unit/cli/checks/changed_files/test_find_consumer_test_paths.py"
            "::TestFindConsumerTestPaths::test_helper_consumers_are_sorted_posix_paths[consumer_names1]",
            "tests/unit/cli/checks/commands/test__collect_extra_test_targets.py"
            "::TestCollectExtraTestTargets::test_support_consumer_not_duplicated[tests/unit/other/test_bar.py]",
            "tests/unit/cli/checks/commands/test__collect_extra_test_targets.py"
            "::TestCollectExtraTestTargets::test_support_consumer_not_duplicated[tests/unit/other]",
        } <= set(ids)
    calls = []
    junit_destination = root / "reports" / "focused.xml"
    junit_destination.parent.mkdir()

    def fake_run(args, **kwargs):
        calls.append((args, kwargs))
        if "--collect-only" in args:
            return subprocess.CompletedProcess(args, 0, _collection(ids), "")
        junit_destination.write_text(_junit(ids), encoding="utf-8")
        return subprocess.CompletedProcess(args, 0, f"{len(ids)} passed", "")

    monkeypatch.setattr("agentic_devtools.cli.ci.windows_specific.run_bounded_process", fake_run)
    result = run_selected_tests(root, policy, groups, junit_path="reports/focused.xml")

    assert set(result) == {"ok", "collected_ids", "executed_ids", "skipped"}
    assert result == {"ok": True, "collected_ids": sorted(ids), "executed_ids": sorted(ids), "skipped": 0}
    assert len(calls) == 2
    collect_args, collect_kwargs = calls[0]
    execute_args, execute_kwargs = calls[1]
    assert collect_args[:7] == [
        sys.executable,
        "-m",
        "pytest",
        "--collect-only",
        "-q",
        "--no-cov",
        "--override-ini=addopts=",
    ]
    assert execute_args[:6] == [
        sys.executable,
        "-m",
        "pytest",
        "--no-cov",
        "--override-ini=addopts=",
        f"--junitxml={junit_destination}",
    ]
    assert collect_args[7:] == execute_args[6:] == list(policy.selectors)
    assert collect_kwargs["cwd"] == execute_kwargs["cwd"] == root.resolve()
    assert collect_kwargs["timeout"] == execute_kwargs["timeout"] == 600
    assert collect_kwargs["env"] is execute_kwargs["env"]
    assert collect_kwargs["env"]["AGDT_RUN_PHASE0_REVIEW_BENCHMARK"] == "1"
    assert os.environ["AGDT_RUN_PHASE0_REVIEW_BENCHMARK"] == "0"
    assert junit_destination.exists()
    if len(policy.selectors) == 19:
        assert len(ids) == 26
        assert len(_selected_ids(policy, {"setup-check"})) == 8
        assert len(_selected_ids(policy, {"portability"})) == 17
        assert len(_selected_ids(policy, {"benchmark"})) == 1


def test_runner_collects_and_executes_changed_file_consumer_targets(tmp_path, monkeypatch):
    policy = _v2_policy()
    groups = {"portability"}
    ids = _selected_ids(policy, groups)
    calls = []

    def fake_run(args, **kwargs):
        calls.append(args)
        if "--collect-only" in args:
            return subprocess.CompletedProcess(args, 0, _collection(ids), "")
        (tmp_path / "run.xml").write_text(_junit(ids), encoding="utf-8")
        return subprocess.CompletedProcess(args, 0, f"{len(ids)} passed", "")

    monkeypatch.setattr("agentic_devtools.cli.ci.windows_specific.run_bounded_process", fake_run)
    result = run_selected_tests(tmp_path, policy, groups, junit_path="run.xml")
    expected = {
        "tests/unit/cli/checks/changed_files/test_find_consumer_test_paths.py"
        "::TestFindConsumerTestPaths::test_windows_conftest_path_returns_posix_directory",
        "tests/unit/cli/checks/changed_files/test_find_consumer_test_paths.py"
        "::TestFindConsumerTestPaths::test_helper_consumers_are_sorted_posix_paths[consumer_names0]",
        "tests/unit/cli/checks/changed_files/test_find_consumer_test_paths.py"
        "::TestFindConsumerTestPaths::test_helper_consumers_are_sorted_posix_paths[consumer_names1]",
        "tests/unit/cli/checks/commands/test__collect_extra_test_targets.py"
        "::TestCollectExtraTestTargets::test_support_consumer_not_duplicated[tests/unit/other/test_bar.py]",
        "tests/unit/cli/checks/commands/test__collect_extra_test_targets.py"
        "::TestCollectExtraTestTargets::test_support_consumer_not_duplicated[tests/unit/other]",
    }

    assert len(calls) == 2
    assert calls[0][7:][-4:] == [
        "tests/unit/cli/checks/changed_files/test_find_consumer_test_paths.py"
        "::TestFindConsumerTestPaths::test_windows_conftest_path_returns_posix_directory",
        "tests/unit/cli/checks/changed_files/test_find_consumer_test_paths.py"
        "::TestFindConsumerTestPaths::test_helper_consumers_are_sorted_posix_paths",
        "tests/unit/cli/checks/commands/test__collect_extra_test_targets.py"
        "::TestCollectExtraTestTargets::test_support_consumer_not_duplicated[tests/unit/other/test_bar.py]",
        "tests/unit/cli/checks/commands/test__collect_extra_test_targets.py"
        "::TestCollectExtraTestTargets::test_support_consumer_not_duplicated[tests/unit/other]",
    ]
    assert expected <= set(result["collected_ids"])
    assert expected <= set(result["executed_ids"])


def test_runner_preserves_benchmark_environment_without_benchmark_group(tmp_path, monkeypatch):
    policy = _policy()
    ids = _selected_ids(policy, {"setup-check"})
    monkeypatch.setenv("AGDT_RUN_PHASE0_REVIEW_BENCHMARK", "inherited")
    calls = []

    def fake_run(args, **kwargs):
        calls.append(kwargs["env"])
        if "--collect-only" in args:
            return subprocess.CompletedProcess(args, 0, _collection(ids), "")
        report = tmp_path / "run.xml"
        report.write_text(_junit(ids), encoding="utf-8")
        return subprocess.CompletedProcess(args, 0, "8 passed", "")

    monkeypatch.setattr("agentic_devtools.cli.ci.windows_specific.run_bounded_process", fake_run)
    run_selected_tests(tmp_path, policy, ["setup-check"], junit_path="run.xml")
    assert calls[0] is calls[1]
    assert calls[0]["AGDT_RUN_PHASE0_REVIEW_BENCHMARK"] == "inherited"
    assert os.environ["AGDT_RUN_PHASE0_REVIEW_BENCHMARK"] == "inherited"


@pytest.mark.parametrize(
    ("groups", "policy", "junit_path"),
    [
        ([], _policy(), "junit.xml"),
        (["unknown"], _policy(), "junit.xml"),
        (["setup-check", "setup-check"], _policy(), "junit.xml"),
        (["setup-check"], None, "junit.xml"),
        (
            ["setup-check"],
            SelectorPolicy((_policy().selectors[0] + "[bad", *_policy().selectors[1:]), _policy().expansions),
            "junit.xml",
        ),
        (["setup-check"], SelectorPolicy(("bad",) * len(_policy().selectors), ()), "junit.xml"),
        (["setup-check"], SelectorPolicy(_policy().selectors, ()), "junit.xml"),
        (["setup-check"], SelectorPolicy(_policy().selectors, _policy().expansions[::-1]), "junit.xml"),
    ],
)
def test_runner_rejects_invalid_inputs_without_spawning(tmp_path, monkeypatch, groups, policy, junit_path):
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.windows_specific.run_bounded_process", lambda *args, **kwargs: pytest.fail()
    )
    with pytest.raises(ValueError):
        run_selected_tests(tmp_path, policy, groups, junit_path=junit_path)


def test_runner_refuses_existing_junit_destination(tmp_path, monkeypatch):
    report = tmp_path / "existing.xml"
    report.write_text("keep", encoding="utf-8")
    ids = _selected_ids(_policy(), {"setup-check"})
    calls = []

    def fake_run(args, **kwargs):
        calls.append(args)
        return subprocess.CompletedProcess(args, 0, _collection(ids), "")

    monkeypatch.setattr("agentic_devtools.cli.ci.windows_specific.run_bounded_process", fake_run)
    with pytest.raises(ValueError):
        run_selected_tests(tmp_path, _policy(), ["setup-check"], junit_path=report)
    assert len(calls) == 1
    assert report.read_text(encoding="utf-8") == "keep"


def test_runner_does_not_execute_after_collection_mismatch(tmp_path, monkeypatch):
    calls = []

    def fake_run(args, **kwargs):
        calls.append(args)
        return subprocess.CompletedProcess(args, 0, "tests/unit/a.py::test_wrong\n1 test collected", "")

    monkeypatch.setattr("agentic_devtools.cli.ci.windows_specific.run_bounded_process", fake_run)
    with pytest.raises(ValueError):
        run_selected_tests(tmp_path, _policy(), ["setup-check"], junit_path="out.xml")
    assert len(calls) == 1


def test_runner_preserves_process_failures_and_diagnostics(tmp_path, monkeypatch):
    error = subprocess.CalledProcessError(7, ["pytest"], output="partial", stderr="diagnostic")
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.windows_specific.run_bounded_process",
        lambda *args, **kwargs: (_ for _ in ()).throw(error),
    )
    with pytest.raises(subprocess.CalledProcessError) as raised:
        run_selected_tests(tmp_path, _policy(), ["setup-check"], junit_path="out.xml")
    assert raised.value is error
    assert raised.value.returncode == 7
    assert raised.value.output == "partial"
    assert raised.value.stderr == "diagnostic"


def test_runner_nonzero_return_code_and_missing_report_fail_closed(tmp_path, monkeypatch):
    calls = []

    def nonzero(args, **kwargs):
        calls.append(args)
        if len(calls) == 2:
            raise subprocess.CalledProcessError(4, args, output="failed")
        return subprocess.CompletedProcess(args, 0, _collection(_selected_ids(_policy(), {"setup-check"})), "")

    monkeypatch.setattr("agentic_devtools.cli.ci.windows_specific.run_bounded_process", nonzero)
    with pytest.raises(subprocess.CalledProcessError) as raised:
        run_selected_tests(tmp_path, _policy(), ["setup-check"], junit_path="out.xml")
    assert raised.value.returncode == 4
    assert raised.value.output == "failed"
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.windows_specific.run_bounded_process",
        lambda args, **kwargs: subprocess.CompletedProcess(
            args, 0, _collection(_selected_ids(_policy(), {"setup-check"})), ""
        ),
    )
    with pytest.raises(FileNotFoundError):
        run_selected_tests(tmp_path, _policy(), ["setup-check"], junit_path="missing.xml")
