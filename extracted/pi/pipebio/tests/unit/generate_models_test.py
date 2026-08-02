"""Unit tests for scripts/generate_models.py."""

import importlib.util
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def _load_generate_models():
    spec = importlib.util.spec_from_file_location(
        "generate_models", REPO_ROOT / "scripts" / "generate_models.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


generate_models = _load_generate_models()


def test_reconcile_excludes_denied_members():
    canonical = [("MigrateToAWSJob", "MigrateToAWSJob"), ("ExportJob", "ExportJob")]
    assert generate_models._reconcile(
        canonical, [], allowlist={"ExportJob"}, denylist={"MigrateToAWSJob"}
    ) == [("ExportJob", "ExportJob")]


def test_reconcile_fails_closed_for_unlisted_canonical_member():
    # A canonical member that is neither allowed nor denied is NOT exposed.
    canonical = [("ExportJob", "ExportJob"), ("SomeNewInternalJob", "SomeNewInternalJob")]
    assert generate_models._reconcile(
        canonical, [], allowlist={"ExportJob"}, denylist=set()
    ) == [("ExportJob", "ExportJob")]


def test_reconcile_expose_all_emits_every_member():
    canonical = [("A", "A"), ("B", "B")]
    assert generate_models._reconcile(
        canonical, [], allowlist=set(), denylist=set(), expose_all=True
    ) == [("A", "A"), ("B", "B")]


def test_reconcile_preserves_sdk_only_members():
    canonical = [("ExportJob", "ExportJob")]
    existing = [("LegacyJob", "LegacyJob")]
    assert generate_models._reconcile(
        canonical, existing, allowlist={"ExportJob"}, denylist=set()
    ) == [
        ("ExportJob", "ExportJob"),
        ("LegacyJob", "LegacyJob"),
    ]


def test_classification_errors_flags_unclassified_members():
    target = generate_models.Target(
        enum_class="JobType",
        source_kind="python",
        source_rel="x",
        output_rel="y",
        module_doc="",
        class_doc="",
        allowlist={"ExportJob"},
        denylist={"MigrateToAWSJob"},
    )
    canonical = [
        ("ExportJob", "ExportJob"),
        ("MigrateToAWSJob", "MigrateToAWSJob"),
        ("BrandNewJob", "BrandNewJob"),
    ]
    assert generate_models._classification_errors(target, canonical) == ["BrandNewJob"]


def test_classification_errors_skipped_when_expose_all():
    target = generate_models.Target(
        enum_class="EntityTypes",
        source_kind="typescript",
        source_rel="x",
        output_rel="y",
        module_doc="",
        class_doc="",
        expose_all=True,
    )
    canonical = [("Anything", "Anything")]
    assert generate_models._classification_errors(target, canonical) == []


def test_generate_fails_closed_on_new_unclassified_member(tmp_path, monkeypatch):
    # A new canonical job type that is neither allowed nor denied must fail.
    source_dir = tmp_path / "jobs" / "shared_python" / "models"
    source_dir.mkdir(parents=True)
    (source_dir / "JobType.py").write_text(
        "from enum import Enum\n\n\nclass JobType(Enum):\n"
        "    ExportJob = 'ExportJob'\n"
        "    BrandNewInternalJob = 'BrandNewInternalJob'\n",
        encoding="utf-8",
    )
    target = generate_models.Target(
        enum_class="JobType",
        source_kind="python",
        source_rel="jobs/shared_python/models/JobType.py",
        output_rel="pipebio/models/job_type.py",
        module_doc="",
        class_doc="",
        allowlist={"ExportJob"},
        denylist=set(),
    )
    monkeypatch.setattr(generate_models, "TARGETS", [target])
    try:
        generate_models._generate(tmp_path)
        assert False, "expected SystemExit for unclassified member"
    except SystemExit as exc:
        assert "BrandNewInternalJob" in str(exc)


def test_existing_sdk_members_fails_on_unparseable_file(tmp_path):
    bad_file = tmp_path / "job_type.py"
    bad_file.write_text("class Other(Enum):\n    X = 'x'\n", encoding="utf-8")
    try:
        generate_models._existing_sdk_members(bad_file, "JobType")
        assert False, "expected SystemExit"
    except SystemExit:
        pass


_TS_DESCRIPTIONS_SOURCE = """
export enum JobType {
  /** Imports data from uploaded files. Runs in Python. */
  ImportJob = 'ImportJob',
  /**
   * @deprecated Legacy job using the disabled "Old (AI)" dialog.
   * Superseded by NewJob.
   */
  OldJob = 'OldJob',
  NoDocsJob = 'NoDocsJob',
  /** Trailing comment. */
  LastJob = 'LastJob',
}
"""


def test_parse_typescript_descriptions_single_and_multiline():
    descriptions = generate_models._parse_typescript_descriptions(
        _TS_DESCRIPTIONS_SOURCE, "JobType"
    )
    assert descriptions["ImportJob"] == "Imports data from uploaded files. Runs in Python."
    # Multi-line JSDoc is collapsed and @deprecated is normalised.
    assert descriptions["OldJob"] == (
        'Deprecated: Legacy job using the disabled "Old (AI)" dialog. Superseded by NewJob.'
    )
    assert descriptions["LastJob"] == "Trailing comment."
    # A member without a JSDoc comment is absent rather than blank.
    assert "NoDocsJob" not in descriptions


def test_parse_typescript_descriptions_missing_enum_returns_empty():
    assert generate_models._parse_typescript_descriptions("export enum Other {}", "JobType") == {}


def test_build_class_doc_appends_members_section():
    target = generate_models.Target(
        enum_class="JobType",
        source_kind="python",
        source_rel="x",
        output_rel="y",
        module_doc="",
        class_doc="The type of job to run.",
    )
    members = [("ImportJob", "ImportJob"), ("UndocumentedJob", "UndocumentedJob")]
    doc = generate_models._build_class_doc(target, members, {"ImportJob": "Imports data."})
    assert "The type of job to run." in doc
    assert "Members:" in doc
    assert "      ImportJob: Imports data." in doc
    # Members without a description are not listed.
    assert "UndocumentedJob" not in doc


def test_build_class_doc_unchanged_without_descriptions():
    target = generate_models.Target(
        enum_class="ExportFormat",
        source_kind="python",
        source_rel="x",
        output_rel="y",
        module_doc="",
        class_doc="A file format.",
    )
    members = [("FASTA", "FASTA")]
    assert generate_models._build_class_doc(target, members, {}) == "A file format."


def test_escape_docstring_neutralises_terminators():
    # A triple-quote run and a trailing backslash must not break the docstring.
    escaped = generate_models._escape_docstring('a """ b \\')
    assert '"""' not in escaped
    assert not escaped.endswith("\\") or escaped.endswith("\\\\")


def test_render_produces_importable_module_for_adversarial_inputs():
    # A value with an embedded quote and a description with a triple-quote run /
    # trailing backslash must still yield syntactically valid Python.
    target = generate_models.Target(
        enum_class="JobType",
        source_kind="python",
        source_rel="x",
        output_rel="y",
        module_doc="Module doc.",
        class_doc="The type of job to run.",
    )
    members = [("WeirdJob", "it's \"weird\"")]
    descriptions = {"WeirdJob": 'Ends with backslash \\ and has """ inside.'}
    rendered = generate_models._render(target, members, descriptions)
    # Must compile without raising SyntaxError.
    compile(rendered, "<generated>", "exec")
    namespace: dict = {}
    exec(rendered, namespace)
    assert namespace["JobType"].WeirdJob.value == "it's \"weird\""
