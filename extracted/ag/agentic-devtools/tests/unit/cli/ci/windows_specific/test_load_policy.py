"""Synthetic inputs for the trusted Windows selector policy."""

import json
from collections import Counter
from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci import windows_specific as windows
from agentic_devtools.cli.ci.windows_selector_policy import V2_EXTENSION_SELECTORS


def _v2_source():
    selectors = (
        *windows._FROZEN_V1_SELECTORS[:-1],
        *V2_EXTENSION_SELECTORS,
        windows._FROZEN_V1_SELECTORS[-1],
    )
    expansions = {
        **windows._FROZEN_V1_EXPANSIONS,
        V2_EXTENSION_SELECTORS[1]: ("consumer_names0", "consumer_names1"),
    }
    return (
        selectors,
        expansions,
        (f"EXPECTED_SELECTORS = {selectors!r}\nEXPECTED_EXPANSIONS = {expansions!r}\nSELECTOR_POLICY_VERSION = 2\n"),
    )


def _v1_source():
    return (
        f"EXPECTED_SELECTORS = {windows._FROZEN_V1_SELECTORS!r}\n"
        f"EXPECTED_EXPANSIONS = {windows._FROZEN_V1_EXPANSIONS!r}\n"
    )


@pytest.fixture
def policy_files(tmp_path):
    source = _v1_source()
    base, head, manifest = (tmp_path / name for name in ("base.py", "head.py", "manifest.json"))
    base.write_text(source, encoding="utf-8")
    head.write_text(source, encoding="utf-8")
    manifest.write_text(
        json.dumps({"selectors": windows._FROZEN_V1_SELECTORS, "expansions": windows._FROZEN_V1_EXPANSIONS}),
        encoding="utf-8",
    )
    return manifest, base, head


def test_matching_policy_is_immutable_named_pair_from_base(policy_files):
    manifest, base, head = policy_files
    base_policy = windows._parse_registered_source(base.read_text(encoding="utf-8"))
    with patch.object(windows, "_parse_registered_source", return_value=base_policy) as parse_source:
        policy = windows.load_policy(manifest, base, head, applicable_groups={"benchmark"}, bootstrap=False)
    parse_source.assert_called_once()
    assert policy[0] is policy.selectors
    assert policy[1] is policy.expansions
    assert policy == base_policy
    assert policy.selectors == windows._FROZEN_V1_SELECTORS
    assert policy.expansions == tuple(windows._FROZEN_V1_EXPANSIONS.items())
    assert len(policy.selectors) == 15
    assert len(policy.selectors) - len(policy.expansions) + sum(len(ids) for _, ids in policy.expansions) == 21
    with pytest.raises(AttributeError):
        policy.selectors = ()


def test_exact_v2_candidate_is_validated_against_trusted_registration(policy_files):
    manifest, _base, head = policy_files
    selectors, expansions, source = _v2_source()
    head.write_text(source, encoding="utf-8")
    manifest.write_text(
        json.dumps(
            {
                "selectors": selectors,
                "expansions": expansions,
                "policy_version": 2,
            }
        ),
        encoding="utf-8",
    )
    policy = windows.load_policy(manifest, policy_files[1], head, applicable_groups=(), bootstrap=False)
    assert policy.selectors == selectors
    assert policy.expansions == tuple(expansions.items())
    assert len(policy.selectors) == 19
    assert len(policy.selectors) - len(policy.expansions) + sum(len(ids) for _, ids in policy.expansions) == 26


def test_registered_v2_base_and_head_load_with_exact_v2_manifest(policy_files):
    manifest, base, head = policy_files
    selectors, expansions, source = _v2_source()
    base.write_text(source, encoding="utf-8")
    head.write_text(source, encoding="utf-8")
    manifest.write_text(
        json.dumps({"selectors": selectors, "expansions": expansions, "policy_version": 2}),
        encoding="utf-8",
    )

    policy = windows.load_policy(manifest, base, head, applicable_groups=(), bootstrap=False)

    assert policy.selectors == selectors
    assert policy.expansions == tuple(expansions.items())
    assert len(policy.selectors) == 19
    assert len(policy.selectors) - len(policy.expansions) + sum(len(ids) for _, ids in policy.expansions) == 26


@pytest.mark.parametrize("version", [1, 3, True, "2", None])
def test_registered_base_rejects_unapproved_version_markers(policy_files, version):
    policy_files[1].write_text(f"{_v1_source()}SELECTOR_POLICY_VERSION = {version!r}\n", encoding="utf-8")
    with pytest.raises(ValueError):
        windows.load_policy(*policy_files, applicable_groups=(), bootstrap=False)


def test_registered_base_rejects_non_json_literal_values(policy_files):
    policy_files[1].write_text("EXPECTED_SELECTORS = 1j\nEXPECTED_EXPANSIONS = {}\n", encoding="utf-8")
    with pytest.raises(ValueError, match="JSON-compatible"):
        windows.load_policy(*policy_files, applicable_groups=(), bootstrap=False)


def test_candidate_source_and_manifest_are_each_read_once(policy_files):
    reads = Counter()
    real_open = Path.open

    def counting_open(path, *args, **kwargs):
        reads[path] += 1
        return real_open(path, *args, **kwargs)

    with patch.object(Path, "open", counting_open):
        windows.load_policy(*policy_files, applicable_groups=(), bootstrap=False)
    assert reads == Counter({path: 1 for path in policy_files})


def test_matching_str_paths(policy_files):
    assert windows.load_policy(*(str(p) for p in policy_files), applicable_groups=(), bootstrap=False)


@pytest.mark.parametrize("which", [1, 2])
def test_source_payload_never_executes(policy_files, tmp_path, which):
    source_path = policy_files[which]
    marker = tmp_path / "executed"
    with source_path.open("a", encoding="utf-8") as stream:
        stream.write(
            f"\nfrom pathlib import Path\nPath({str(marker)!r}).touch()\n"
            "def unrelated():\n    raise RuntimeError('never run')\n"
            "raise RuntimeError('never run')\n"
        )
    windows.load_policy(*policy_files, applicable_groups=(), bootstrap=False)
    assert not marker.exists()


@pytest.mark.parametrize("which", [1, 2])
@pytest.mark.parametrize("source", ["not valid Python !", "EXPECTED_SELECTORS = ()", ""])
def test_bad_source_fails(policy_files, which, source):
    policy_files[which].write_text(source, encoding="utf-8")
    with pytest.raises(ValueError):
        windows.load_policy(*policy_files, applicable_groups=(), bootstrap=False)


def test_missing_base_without_bootstrap(policy_files):
    policy_files[1].unlink()
    with pytest.raises(FileNotFoundError):
        windows.load_policy(*policy_files, applicable_groups=(), bootstrap=False)


def test_absent_base_bootstrap_returns_seed(policy_files):
    policy_files[1].unlink()
    policy = windows.load_policy(*policy_files, applicable_groups=(), bootstrap=True)
    assert policy.selectors is windows._FROZEN_V1_SELECTORS
    assert policy.expansions == tuple(windows._FROZEN_V1_EXPANSIONS.items())


def test_absent_base_bootstrap_rejects_v2_candidate(policy_files):
    manifest, base, head = policy_files
    base.unlink()
    selectors, expansions, source = _v2_source()
    head.write_text(source, encoding="utf-8")
    manifest.write_text(
        json.dumps({"selectors": selectors, "expansions": expansions, "policy_version": 2}),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="Bootstrap"):
        windows.load_policy(manifest, base, head, applicable_groups=(), bootstrap=True)


@pytest.mark.parametrize("groups", [(), ("setup-check",), ("portability",), ("benchmark",)])
def test_existing_base_never_bootstraps(policy_files, groups):
    with pytest.raises(ValueError):
        windows.load_policy(*policy_files, applicable_groups=groups, bootstrap=True)


@pytest.mark.parametrize("group", ["setup-check", "portability", "benchmark"])
def test_absent_base_cannot_bootstrap_products(policy_files, group):
    policy_files[1].unlink()
    with pytest.raises(ValueError):
        windows.load_policy(*policy_files, applicable_groups=[group], bootstrap=True)


@pytest.mark.parametrize("which", [0, 2])
def test_bootstrap_rejects_bad_verification_input(policy_files, which):
    policy_files[1].unlink()
    policy_files[which].write_text("{}", encoding="utf-8")
    with pytest.raises(ValueError):
        windows.load_policy(*policy_files, applicable_groups=(), bootstrap=True)


@pytest.mark.parametrize("bootstrap", [False, True])
@pytest.mark.parametrize("error", [PermissionError, IsADirectoryError, OSError])
def test_base_open_errors_do_not_enable_bootstrap(policy_files, bootstrap, error):
    real_open = Path.open

    def failing_open(path, *args, **kwargs):
        if path == policy_files[1]:
            raise error("base cannot be opened")
        return real_open(path, *args, **kwargs)

    with patch.object(Path, "open", failing_open), pytest.raises(error):
        windows.load_policy(*policy_files, applicable_groups=(), bootstrap=bootstrap)


def test_base_read_file_not_found_is_not_absence(policy_files):
    with patch.object(Path, "open") as open_mock:
        open_mock.return_value.__enter__.return_value.read.side_effect = FileNotFoundError("read failed")
        with pytest.raises(FileNotFoundError, match="read failed"):
            windows.load_policy(*policy_files, applicable_groups=(), bootstrap=True)


@pytest.mark.parametrize("which", [0, 2])
def test_verification_file_access_failures_propagate(policy_files, which):
    policy_files[which].unlink()
    with pytest.raises(FileNotFoundError):
        windows.load_policy(*policy_files, applicable_groups=(), bootstrap=False)


@pytest.mark.parametrize(
    "text",
    [
        "not JSON",
        "null",
        "[]",
        "{}",
        '{"selectors": [], "expansions": {}, "extra": true}',
        '{"selectors": [], "selectors": [], "expansions": {}}',
        '{"selectors": [], "expansions": {"same": [], "same": []}}',
    ],
)
def test_invalid_manifest(policy_files, text):
    policy_files[0].write_text(text, encoding="utf-8")
    with pytest.raises(ValueError):
        windows.load_policy(*policy_files, applicable_groups=(), bootstrap=False)


@pytest.mark.parametrize("groups", ["benchmark", b"benchmark", None, 3, ["unknown"], [None], [[]]])
def test_invalid_groups(policy_files, groups):
    with pytest.raises(ValueError):
        windows.load_policy(*policy_files, applicable_groups=groups, bootstrap=False)


@pytest.mark.parametrize("bootstrap", [None, 0, 1, "false"])
def test_invalid_bootstrap(policy_files, bootstrap):
    with pytest.raises(ValueError):
        windows.load_policy(*policy_files, applicable_groups=(), bootstrap=bootstrap)


@pytest.mark.parametrize("which", [0, 1, 2])
@pytest.mark.parametrize("path", [None, 123, b"policy.py", ""])
def test_invalid_policy_paths(policy_files, which, path):
    paths = list(policy_files)
    paths[which] = path
    with pytest.raises(ValueError):
        windows.load_policy(*paths, applicable_groups=(), bootstrap=False)


@pytest.mark.parametrize("which", [0, 1, 2])
@pytest.mark.parametrize(
    "drift",
    ["selector-order", "selector-count", "selector-duplicate", "expansion-order", "expansion-id", "expansion-count"],
)
def test_each_verification_input_rejects_drift(policy_files, which, drift):
    baseline = windows.load_policy(*policy_files, applicable_groups=(), bootstrap=False)
    assert baseline.selectors == windows._FROZEN_V1_SELECTORS
    assert baseline.expansions == tuple(windows._FROZEN_V1_EXPANSIONS.items())
    selectors = windows._FROZEN_V1_SELECTORS
    expansions = windows._FROZEN_V1_EXPANSIONS.copy()
    if drift == "selector-order":
        selectors = selectors[::-1]
    elif drift == "selector-count":
        selectors = selectors[:-1]
    elif drift == "selector-duplicate":
        selectors = (selectors[0],) * len(selectors)
    elif drift == "expansion-order":
        expansions = dict(reversed(expansions.items()))
    elif drift == "expansion-id":
        expansions[selectors[0]] = ("linux", "tampered")
    else:
        expansions[selectors[0]] = ("linux",)
    source = f"EXPECTED_SELECTORS = {selectors!r}\nEXPECTED_EXPANSIONS = {expansions!r}\n"
    text = json.dumps({"selectors": selectors, "expansions": expansions}) if which == 0 else source
    policy_files[which].write_text(text, encoding="utf-8")
    expected_errors = {
        "selector-order": "Selectors must exactly match the frozen ordered policy",
        "selector-count": "Selectors must exactly match the frozen ordered policy",
        "selector-duplicate": "Selectors must exactly match the frozen ordered policy",
        "expansion-order": "Expansion keys must exactly match the frozen ordered policy",
        "expansion-id": "Expansion IDs must exactly match the frozen ordered policy",
        "expansion-count": "Expansion IDs must exactly match the frozen ordered policy",
    }
    with pytest.raises(ValueError) as exc_info:
        windows.load_policy(*policy_files, applicable_groups=(), bootstrap=False)
    assert str(exc_info.value) == expected_errors[drift]


def test_agreement_between_inputs_cannot_change_frozen_seed(policy_files):
    selectors = windows._FROZEN_V1_SELECTORS[:-1]
    expansions = windows._FROZEN_V1_EXPANSIONS
    source = f"EXPECTED_SELECTORS = {selectors!r}\nEXPECTED_EXPANSIONS = {expansions!r}\n"
    policy_files[1].write_text(source, encoding="utf-8")
    policy_files[2].write_text(source, encoding="utf-8")
    policy_files[0].write_text(json.dumps({"selectors": selectors, "expansions": expansions}), encoding="utf-8")
    with pytest.raises(ValueError):
        windows.load_policy(*policy_files, applicable_groups=(), bootstrap=False)
