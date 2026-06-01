import ast
from collections import Counter
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


RUN_ENV_VAR = "RUN_REPLACE_TABLES_BACKWARD_COMPAT"
BASELINE_VERSION = os.environ.get("REPLACE_TABLES_BACKWARD_COMPAT_BASELINE_VERSION", "1.5.2")
TARGET_MODE = os.environ.get("REPLACE_TABLES_BACKWARD_COMPAT_TARGET_MODE", "installed")
TARGET_VERSION = os.environ.get("REPLACE_TABLES_BACKWARD_COMPAT_TARGET_VERSION", "2.1.0")
VALIDATION_CPP_PATH = Path("functions/Validation.cpp")


FUNCTION_EXPR_OVERRIDES = {
    "cast": "CAST(1 AS Int32)",
    "exists": "EXISTS(SELECT 1)",
    "in": "in(1, tuple(1))",
    "notin": "notIn(1, tuple(1))",
    "nullin": "nullIn(1, tuple(1))",
    "notnullin": "notNullIn(1, tuple(1))",
    "globalin": "globalIn(1, tuple(1))",
    "globalnotin": "globalNotIn(1, tuple(1))",
    "globalnullin": "globalNullIn(1, tuple(1))",
    "globalnotnullin": "globalNotNullIn(1, tuple(1))",
    "position": "position(1, tuple(1))",
    "substring": "substring(1, tuple(1))",
}


def _venv_python_path(venv_dir):
    if os.name == "nt":
        return venv_dir / "Scripts" / "python.exe"
    return venv_dir / "bin" / "python"


def _ensure_toolset_version(version):
    py_tag = f"py{sys.version_info.major}{sys.version_info.minor}"
    root = Path(
        os.environ.get(
            "REPLACE_TABLES_BACKWARD_COMPAT_VENV_ROOT",
            Path(tempfile.gettempdir()) / "replace_tables_backward_compat_venvs",
        )
    )
    venv_dir = root / f"{py_tag}-tinybird-toolset-{version}"
    python_path = _venv_python_path(venv_dir)
    marker = venv_dir / ".toolset-version"

    if not python_path.exists():
        venv_dir.parent.mkdir(parents=True, exist_ok=True)
        subprocess.check_call([sys.executable, "-m", "venv", str(venv_dir)])

    installed_version = marker.read_text().strip() if marker.exists() else None
    if installed_version != version:
        subprocess.check_call(
            [
                str(python_path),
                "-m",
                "pip",
                "install",
                "--disable-pip-version-check",
                f"tinybird-toolset=={version}",
            ]
        )
        marker.write_text(version)

    return str(python_path)


def _run_replace_tables_cases(python_path, cases):
    script = r"""
import json
import sys
from chtoolset import query as chquery

cases = json.loads(sys.stdin.read())
results = {}

for case in cases:
    replacements = {tuple(k): tuple(v) for k, v in case["replacements"]}
    args = case.get("args", [])
    kwargs = case.get("kwargs", {})

    try:
        value = chquery.replace_tables(case["sql"], replacements, *args, **kwargs)
        results[case["id"]] = {"ok": True, "value": value}
    except Exception as e:
        results[case["id"]] = {
            "ok": False,
            "error_type": type(e).__name__,
            "error_message": str(e),
        }

print(json.dumps(results))
"""
    out = subprocess.check_output(
        [python_path, "-c", script],
        input=json.dumps(cases),
        text=True,
    )
    return json.loads(out)


def _run_format_cases(python_path, sql_by_key):
    script = r"""
import json
import sys
from chtoolset import query as chquery

items = json.loads(sys.stdin.read())
results = {}

for key, sql in items.items():
    try:
        results[key] = {"ok": True, "value": chquery.format(sql)}
    except Exception as e:
        results[key] = {
            "ok": False,
            "error_type": type(e).__name__,
            "error_message": str(e),
        }

print(json.dumps(results))
"""
    out = subprocess.check_output(
        [python_path, "-c", script],
        input=json.dumps(sql_by_key),
        text=True,
    )
    return json.loads(out)


def _freeze_replacements(replacements):
    return tuple(sorted((tuple(k), tuple(v)) for k, v in replacements.items()))


def _stable_case_id(case):
    payload = json.dumps(case, sort_keys=True, separators=(",", ":"))
    return hashlib.sha1(payload.encode("utf-8")).hexdigest()[:12]


def _build_case(sql, replacements, args=(), kwargs=None, source=None, function_name=None):
    case = {
        "sql": sql,
        "replacements": [[list(k), list(v)] for k, v in _freeze_replacements(replacements)],
    }
    if args:
        case["args"] = list(args)
    if kwargs:
        case["kwargs"] = kwargs
    if source:
        case["source"] = source
    if function_name:
        case["function_name"] = function_name

    case["id"] = _stable_case_id(case)
    return case


def _casefold_unique(names):
    seen = set()
    result = []
    for name in names:
        key = name.lower()
        if key in seen:
            continue
        seen.add(key)
        result.append(name)
    return result


def _function_expression(name):
    return FUNCTION_EXPR_OVERRIDES.get(name.lower(), f"{name}(1)")


def _parse_validation_cpp_functions():
    if not VALIDATION_CPP_PATH.exists():
        raise AssertionError(f"Missing {VALIDATION_CPP_PATH}")

    text = VALIDATION_CPP_PATH.read_text()
    pattern = re.compile(
        r'TB::(CH_GENERAL_FUNCTIONS|CH_GENERAL_FUNCTIONS_INSENSITIVE|CH_AGGREGATE_FUNCTIONS|CH_AGGREGATE_FUNCTIONS_INSENSITIVE|CH_TABLE_FUNCTIONS)\.emplace\((?:Poco::toLower\()?std::string\("([^"]+)"\)\)?\);'
    )

    grouped = {
        "CH_GENERAL_FUNCTIONS": [],
        "CH_GENERAL_FUNCTIONS_INSENSITIVE": [],
        "CH_AGGREGATE_FUNCTIONS": [],
        "CH_AGGREGATE_FUNCTIONS_INSENSITIVE": [],
        "CH_TABLE_FUNCTIONS": [],
    }

    for set_name, function_name in pattern.findall(text):
        grouped[set_name].append(function_name)
    return grouped


def _collect_validation_cpp_function_cases():
    grouped = _parse_validation_cpp_functions()
    source_table = "compat_source_table"
    replacement = {("", source_table): ("", "compat_target_table")}

    general_functions = _casefold_unique(
        grouped["CH_GENERAL_FUNCTIONS"] + grouped["CH_GENERAL_FUNCTIONS_INSENSITIVE"]
    )
    aggregate_functions = _casefold_unique(
        grouped["CH_AGGREGATE_FUNCTIONS"] + grouped["CH_AGGREGATE_FUNCTIONS_INSENSITIVE"]
    )
    table_functions = _casefold_unique(grouped["CH_TABLE_FUNCTIONS"])

    cases = []
    for function_name in general_functions:
        cases.append(
            _build_case(
                f"SELECT {_function_expression(function_name)} FROM {source_table}",
                replacement,
                source="validation_cpp_general_function",
                function_name=function_name,
            )
        )

    for function_name in aggregate_functions:
        cases.append(
            _build_case(
                f"SELECT {_function_expression(function_name)} FROM {source_table}",
                replacement,
                source="validation_cpp_aggregate_function",
                function_name=function_name,
            )
        )

    for function_name in table_functions:
        cases.append(
            _build_case(
                f"SELECT 1 FROM {function_name}(1)",
                {},
                source="validation_cpp_table_function",
                function_name=function_name,
            )
        )

    return cases


def _extract_scenarios_from_test_replace_tables():
    path = Path("tests/test_replace_tables.py")
    tree = ast.parse(path.read_text(), filename=str(path))

    scenarios = None
    for node in tree.body:
        if not isinstance(node, ast.ClassDef) or node.name != "TestReplaceTables":
            continue
        for stmt in node.body:
            if not isinstance(stmt, ast.Assign):
                continue
            if not any(isinstance(t, ast.Name) and t.id == "scenarios" for t in stmt.targets):
                continue
            scenarios = ast.literal_eval(stmt.value)
            break

    if scenarios is None:
        raise AssertionError("Could not extract TestReplaceTables.scenarios")

    cases = []
    for sql, replacements, _ in scenarios:
        cases.append(_build_case(sql, replacements, source="test_replace_tables_scenarios"))
        cases.append(
            _build_case(
                sql,
                replacements,
                kwargs={"one_line": True},
                source="test_replace_tables_scenarios",
            )
        )
    return cases


def _manual_compat_cases():
    return [
        _build_case(
            'SELECT TRIM(BOTH \'"\' FROM api_key) FROM my_table',
            {("", "my_table"): ("", "other_table")},
            source="manual",
        ),
        _build_case(
            "SELECT json.^a.b, json.^d.e.f FROM test;",
            {("d_012345", "test"): ("", "(SELECT * FROM d_012345.t_012345)")},
            kwargs={"default_database": "d_012345"},
            source="manual",
        ),
        _build_case(
            "SELECT json.a.b.:Float64, json.a.g.:Date, json.c.:String, json.d.:UInt8 FROM test",
            {("d_012345", "test"): ("", "(SELECT * FROM d_012345.t_012345)")},
            kwargs={"default_database": "d_012345"},
            source="manual",
        ),
        _build_case(
            "SELECT sleepEachRow(number) FROM numbers(10)",
            {},
            kwargs={
                "default_database": "default",
                "function_allow_list": ["sleepEachRow"],
            },
            source="manual",
        ),
        _build_case(
            "SELECT * FROM a SETTINGS join_algorithm='tinybird'",
            {("default", "a"): ("", "(SELECT 1)")},
            kwargs={"default_database": "default"},
            source="manual",
        ),
    ]


def _dedupe_cases(cases):
    by_id = {}
    for case in cases:
        by_id[case["id"]] = case
    return list(by_id.values())


def _log_cases(cases):
    sorted_cases = sorted(
        cases,
        key=lambda case: (
            case.get("source", ""),
            case.get("function_name") or "",
            case["id"],
        ),
    )
    source_counts = Counter(case.get("source", "unknown") for case in sorted_cases)

    print(
        "[replace_tables_backward_compat] collected "
        f"{len(sorted_cases)} validation cases",
        flush=True,
    )
    source_summary = ", ".join(
        f"{source}:{count}"
        for source, count in sorted(source_counts.items(), key=lambda item: item[0])
    )
    print(
        f"[replace_tables_backward_compat] source counts: {source_summary}",
        flush=True,
    )

    total = len(sorted_cases)
    for idx, case in enumerate(sorted_cases, start=1):
        payload = {
            "index": idx,
            "total": total,
            "id": case["id"],
            "source": case.get("source", "unknown"),
            "function_name": case.get("function_name"),
            "sql": case["sql"],
            "args": case.get("args", []),
            "kwargs": case.get("kwargs", {}),
        }
        print(
            f"[replace_tables_backward_compat] validation_case {json.dumps(payload, ensure_ascii=False)}",
            flush=True,
        )


def _results_match(baseline, target, function_name=None):
    # Allow specific functions to transition from blocked to allowed
    ALLOWED_UNBLOCKS = {"getSetting"}

    if baseline.get("ok") != target.get("ok"):
        # Check if this is an allowed unblock (was blocked, now allowed)
        is_unblock = (not baseline.get("ok") and target.get("ok"))
        is_allowed = function_name in ALLOWED_UNBLOCKS
        is_restriction = "is restricted" in baseline.get("error_message", "")
        if is_unblock and is_allowed and is_restriction:
            return True  # This is an expected breaking change
        return False
    if baseline.get("ok"):
        return baseline.get("value") == target.get("value")
    # Error messages between CH versions are noisy; fail/fail is considered stable here.
    return True


@unittest.skipUnless(
    os.environ.get(RUN_ENV_VAR) == "1",
    f"Set {RUN_ENV_VAR}=1 to run the cross-version replace_tables compatibility test",
)
class TestReplaceTablesBackwardCompat(unittest.TestCase):
    maxDiff = None

    def test_replace_tables_output_compatibility(self):
        validation_cpp_cases = _collect_validation_cpp_function_cases()
        self.assertGreater(
            len(validation_cpp_cases),
            1000,
            "Expected to generate a broad compatibility corpus from Validation.cpp functions",
        )

        cases = _extract_scenarios_from_test_replace_tables()
        cases.extend(_manual_compat_cases())
        cases.extend(validation_cpp_cases)
        cases = _dedupe_cases(cases)

        _log_cases(cases)

        baseline_python = _ensure_toolset_version(BASELINE_VERSION)
        print(
            "[replace_tables_backward_compat] running baseline replace_tables "
            f"with tinybird-toolset=={BASELINE_VERSION}",
            flush=True,
        )
        baseline_results = _run_replace_tables_cases(baseline_python, cases)

        if TARGET_MODE == "installed":
            target_label = "installed"
            target_python = sys.executable
        elif TARGET_MODE == "pypi":
            target_label = TARGET_VERSION
            target_python = _ensure_toolset_version(TARGET_VERSION)
        else:
            raise AssertionError(
                "REPLACE_TABLES_BACKWARD_COMPAT_TARGET_MODE must be one of: installed, pypi"
            )

        print(
            "[replace_tables_backward_compat] running target replace_tables "
            f"with target={target_label} (mode={TARGET_MODE})",
            flush=True,
        )
        target_results = _run_replace_tables_cases(target_python, cases)

        # Canonicalize successful outputs with the baseline formatter to accept
        # representational differences that remain parsable/compatible in baseline.
        format_inputs = {}
        for case in cases:
            case_id = case["id"]
            baseline = baseline_results[case_id]
            target = target_results[case_id]
            if not (baseline.get("ok") and target.get("ok")):
                continue
            format_inputs[f"{case_id}:baseline"] = baseline["value"]
            format_inputs[f"{case_id}:target"] = target["value"]

        formatted = _run_format_cases(baseline_python, format_inputs)

        unexpected_diffs = []
        for case in cases:
            case_id = case["id"]
            baseline = baseline_results[case_id]
            target = target_results[case_id]

            if _results_match(baseline, target, case.get("function_name")):
                continue

            if baseline.get("ok") and target.get("ok"):
                baseline_fmt = formatted[f"{case_id}:baseline"]
                target_fmt = formatted[f"{case_id}:target"]
                if baseline_fmt.get("ok") and target_fmt.get("ok") and baseline_fmt.get("value") == target_fmt.get("value"):
                    continue

            unexpected_diffs.append(
                {
                    "id": case_id,
                    "sql": case["sql"],
                    "args": case.get("args", []),
                    "kwargs": case.get("kwargs", {}),
                    "source": case.get("source", "unknown"),
                    "function_name": case.get("function_name"),
                    "baseline": baseline,
                    "target": target,
                }
            )

        print(
            "[replace_tables_backward_compat] unexpected differences found: "
            f"{len(unexpected_diffs)}",
            flush=True,
        )

        self.assertEqual(
            [],
            unexpected_diffs,
            "Unexpected replace_tables output differences between versions "
            f"{BASELINE_VERSION} and {target_label}:\n"
            f"{json.dumps(unexpected_diffs, indent=2, ensure_ascii=False)}",
        )
