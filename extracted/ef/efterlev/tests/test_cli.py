"""CLI shape tests.

Verifies the CLI registers every v0 subcommand, that `--help` / `--version` work,
and that stub subcommands raise `NotImplementedError`. Does not yet exercise any
real behavior — that lands with each subcommand's implementation phase.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from typer.testing import CliRunner

from efterlev import __version__
from efterlev.cli.main import app

runner = CliRunner()


def test_root_help_lists_every_v0_subcommand() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    for cmd in ("init", "scan", "agent", "provenance", "mcp"):
        assert cmd in result.output


def test_version_flag_prints_package_version() -> None:
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert __version__ in result.output


def test_v0_1_38_version_flag_warns_on_parallel_installs(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """v0.1.38 fix for S1 (uv-tool symlink shadows pipx, silent
    upgrade-to-old-version): when --version runs and detects multiple
    installs (uv tool + pipx, etc.), print a shadow warning to stderr
    so the user notices BEFORE running into mysterious old-version
    behavior. Pre-v0.1.38 this only surfaced via `efterlev doctor`,
    which the tester didn't run before hitting the silent-shadow
    failure mode.
    """
    from efterlev.cli import doctor as doctor_module

    monkeypatch.setattr(
        doctor_module,
        "_efterlev_manager_installs",
        lambda: [
            ("pipx", "/home/u/.local/pipx/venvs/efterlev", "pipx uninstall efterlev"),
            ("uv tool", "/home/u/.local/share/uv/tools/efterlev", "uv tool uninstall efterlev"),
        ],
    )
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert __version__ in result.stdout
    # Newer click/typer captures stderr separately on result.stderr.
    assert "warning:" in result.stderr
    assert "parallel installs" in result.stderr
    assert "efterlev doctor" in result.stderr


def test_v0_1_38_version_flag_silent_when_one_install(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """No false positives: a single-install host gets the version line
    and nothing else. The shadow warning fires only on the actual
    parallel-install case.
    """
    from efterlev.cli import doctor as doctor_module

    monkeypatch.setattr(
        doctor_module,
        "_efterlev_manager_installs",
        lambda: [("pipx", "/home/u/.local/pipx/venvs/efterlev", "pipx uninstall efterlev")],
    )
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "warning:" not in result.stderr


def test_agent_subtree_lists_three_agents() -> None:
    result = runner.invoke(app, ["agent", "--help"])
    assert result.exit_code == 0
    for sub in ("gap", "document", "remediate"):
        assert sub in result.output


def test_mcp_serve_command_is_registered() -> None:
    """`efterlev mcp serve` is wired up — behavior lives in tests/test_mcp_server.py."""
    result = runner.invoke(app, ["mcp", "serve", "--help"])
    assert result.exit_code == 0
    assert "MCP stdio server" in result.output


def test_detectors_list_lists_all_thirty_detectors(tmp_path: pytest.TempPathFactory) -> None:
    """`efterlev detectors list` was promised by THREAT_MODEL.md but
    didn't exist before 2026-04-25 (round-2 review finding). Now it
    does — this test locks the contract.
    """
    result = runner.invoke(app, ["detectors", "list"])
    assert result.exit_code == 0
    # 66 detectors after github.branch_protection (single-PR detector
    # under v0.1.55, KSI-PIY-RSD + SA-15 + CM-2 at the IaC layer).
    # See CHANGELOG.md for per-release bump history; the prior verbose
    # tier-by-tier comment block here was condensed in v0.1.50 once
    # the WAF arc completed.
    assert "total: 66 detectors" in result.output
    assert "62 KSI-mapped" in result.output
    assert "4 800-53 only" in result.output
    # Spot-check a couple of detector ids appear.
    assert "aws.encryption_s3_at_rest" in result.output
    assert "aws.access_analyzer_enabled" in result.output


def test_detectors_list_tags_supplementary_800_53_only_detectors(
    tmp_path: pytest.TempPathFactory,
) -> None:
    """Supplementary detectors (those with ksis=[]) get a visible tag so a
    reader scanning the list knows which detectors contribute to KSI
    roll-ups vs which provide supplementary 800-53 evidence only.
    Priority 6 (2026-04-27 honesty pass)."""
    result = runner.invoke(app, ["detectors", "list"])
    assert result.exit_code == 0
    # v0.1.42 (DECISIONS 2026-05-08 Tier 1 #4.1): the UCM re-classification
    # audit moved encryption_ebs, encryption_s3_at_rest, and
    # rds_encryption_at_rest OUT of the supplementary cohort by adding
    # KSI-AFR-UCM. The remaining supplementary SC-28 detectors:
    for det_id in (
        "aws.sns_topic_encryption",
        "aws.sqs_queue_encryption",
    ):
        # Each line for one of these detectors should carry the [800-53 only] tag.
        line_with_tag = next(
            (
                line
                for line in result.output.splitlines()
                if det_id in line and "[800-53 only]" in line
            ),
            None,
        )
        assert line_with_tag is not None, (
            f"expected `{det_id}` line to carry `[800-53 only]` tag; output:\n{result.output}"
        )
    # And kms_key_rotation, rehomed in this same pass, should NOT carry the tag.
    line_with_kms = next(
        (line for line in result.output.splitlines() if "aws.kms_key_rotation" in line),
        None,
    )
    assert line_with_kms is not None
    assert "[800-53 only]" not in line_with_kms


def test_provenance_verify_clean_store_passes(tmp_path: pytest.TempPathFactory) -> None:
    """`efterlev provenance verify` was claimed by THREAT_MODEL.md as
    the tamper-detection path. The earlier reality: the command did
    not exist. Now it does; this test locks the clean-store path.
    """
    init_result = runner.invoke(app, ["init", "--target", str(tmp_path)])
    assert init_result.exit_code == 0
    # Empty store — no records to verify against, but the command
    # must still exit cleanly.
    result = runner.invoke(app, ["provenance", "verify", "--target", str(tmp_path)])
    assert result.exit_code == 0
    assert "RESULT: clean" in result.output


def test_provenance_verify_detects_tampered_blob(tmp_path: Path) -> None:
    """A modified blob must surface as a mismatch finding.

    Walks the storage path: write a record, mutate its blob on disk,
    rerun verify, assert the mismatch is reported and exit code is 1.
    """
    from efterlev.provenance import ProvenanceStore

    with ProvenanceStore(tmp_path) as store:
        record = store.write_record(
            payload={"detector_id": "aws.test", "content": {"x": 1}},
            record_type="evidence",
            primitive="scan_terraform@0.1.0",
        )
        blob_path = store.blob_dir / record.content_ref

    # Tamper: rewrite the blob with different content.
    blob_path.write_text('{"detector_id": "aws.test", "content": {"x": 2}}')

    result = runner.invoke(app, ["provenance", "verify", "--target", str(tmp_path)])
    assert result.exit_code == 1
    assert "MISMATCHES" in result.output
    assert record.record_id in result.output


def test_provenance_verify_detects_unresolvable_derived_from(tmp_path: Path) -> None:
    """v0.1.6 referential-integrity sweep — if a record's envelope
    `derived_from` cites an id that doesn't resolve, surface it. The
    write-time validator (`_validate_claim_derived_from`) prevents this
    on the happy path; this post-hoc check catches anything that bypasses
    it (future tooling, manual SQL writes, etc.)."""
    from efterlev.provenance import ProvenanceStore

    with ProvenanceStore(tmp_path) as store:
        ev_record = store.write_record(payload={"x": 1}, record_type="evidence")
        # Bypass the validator by using INSERT directly with a fabricated
        # derived_from. A real-world scenario this guards: a future writer
        # that doesn't go through write_record, or a buggy migration.
        store._conn.execute(
            "INSERT INTO provenance_records "
            "(record_id, record_type, content_ref, derived_from, primitive, "
            " agent, model, prompt_hash, timestamp, metadata) "
            "VALUES (?, 'claim', ?, ?, NULL, 'test', NULL, NULL, ?, '{}')",
            (
                "sha256:" + "f" * 64,
                ev_record.content_ref,  # reuse a real blob to keep blob-hash check happy
                '["sha256:' + "0" * 64 + '"]',
                "2026-05-04T00:00:00+00:00",
            ),
        )
        store._conn.commit()

    result = runner.invoke(app, ["provenance", "verify", "--target", str(tmp_path)])
    assert result.exit_code == 1, result.output
    assert "derived_from cites" in result.output
    assert "does not resolve" in result.output


def test_agent_gap_missing_efterlev_dir_prints_error(tmp_path: pytest.TempPathFactory) -> None:
    result = runner.invoke(app, ["agent", "gap", "--target", str(tmp_path)])
    assert result.exit_code == 1
    assert "no `.efterlev/` directory" in result.output


def test_agent_document_missing_efterlev_dir_prints_error(
    tmp_path: pytest.TempPathFactory,
) -> None:
    result = runner.invoke(app, ["agent", "document", "--target", str(tmp_path)])
    assert result.exit_code == 1
    assert "no `.efterlev/` directory" in result.output


def test_agent_remediate_missing_efterlev_dir_prints_error(
    tmp_path: pytest.TempPathFactory,
) -> None:
    result = runner.invoke(
        app, ["agent", "remediate", "--ksi", "KSI-SVC-VRI", "--target", str(tmp_path)]
    )
    assert result.exit_code == 1
    assert "no `.efterlev/` directory" in result.output


def test_agent_remediate_unknown_ksi_prints_error(tmp_path: pytest.TempPathFactory) -> None:
    init_result = runner.invoke(app, ["init", "--target", str(tmp_path)])
    assert init_result.exit_code == 0, init_result.output
    result = runner.invoke(
        app,
        ["agent", "remediate", "--ksi", "KSI-DOES-NOT-EXIST", "--target", str(tmp_path)],
    )
    assert result.exit_code == 1
    assert "not in the loaded baseline" in result.output


def test_agent_remediate_without_classification_prints_error(
    tmp_path: pytest.TempPathFactory,
) -> None:
    init_result = runner.invoke(app, ["init", "--target", str(tmp_path)])
    assert init_result.exit_code == 0, init_result.output
    # Pick any real KSI from the loaded FRMR; no `agent gap` has run yet.
    result = runner.invoke(
        app, ["agent", "remediate", "--ksi", "KSI-SVC-SNT", "--target", str(tmp_path)]
    )
    assert result.exit_code == 1
    assert "no Gap Agent classification" in result.output


def test_agent_remediate_short_circuits_on_manifest_only_evidence(
    tmp_path: pytest.TempPathFactory,
) -> None:
    """A KSI whose Evidence is exclusively manifest-sourced has no Terraform
    surface to remediate — the CLI must exit cleanly before invoking the LLM
    rather than feeding the YAML manifest to the Remediation Agent as if it
    were Terraform source. This locks in the filter from Phase 1 polish C.
    """
    import json

    from efterlev.models import Claim
    from efterlev.provenance import ProvenanceStore

    root = Path(str(tmp_path))

    # 1. Init the workspace so FRMR cache + provenance store exist.
    init_result = runner.invoke(app, ["init", "--target", str(root)])
    assert init_result.exit_code == 0, init_result.output

    # 2. Drop a manifest attesting to KSI-AFR-FSI (FedRAMP Security Inbox).
    manifests_dir = root / ".efterlev" / "manifests"
    manifests_dir.mkdir(parents=True, exist_ok=True)
    (manifests_dir / "security-inbox.yml").write_text(
        "ksi: KSI-AFR-FSI\n"
        "name: FedRAMP Security Inbox\n"
        "evidence:\n"
        "  - type: attestation\n"
        "    statement: security@example.com monitored 24/7 by SOC team.\n"
        "    attested_by: vp-security@example.com\n"
        "    attested_at: 2026-04-15\n",
        encoding="utf-8",
    )

    # 3. Scan to produce the manifest-sourced Evidence record. No `.tf` files
    #    are present, so no Terraform Evidence lands — only manifest Evidence.
    scan_result = runner.invoke(app, ["scan", "--target", str(root)])
    assert scan_result.exit_code == 0, scan_result.output

    # 4. Persist a `partial` classification for KSI-AFR-FSI directly. We
    #    don't run the Gap Agent (it needs an API key); we just write the
    #    Claim in the shape the reconstruction helper expects, cited by
    #    the manifest Evidence id.
    with ProvenanceStore(root) as store:
        manifest_evidence = [
            p for _rid, p in store.iter_evidence() if p["detector_id"] == "manifest"
        ]
        assert manifest_evidence, "scan should have produced one manifest Evidence record"
        ev_id = manifest_evidence[0]["evidence_id"]
        clf = Claim.create(
            claim_type="classification",
            content={
                "ksi_id": "KSI-AFR-FSI",
                "status": "partial",
                "rationale": "Procedural attestation present; infra layer n/a.",
            },
            confidence="medium",
            derived_from=[ev_id],
            model="stub",
            prompt_hash="stub",
        )
        store.write_record(
            payload=json.loads(clf.model_dump_json()),
            record_type="claim",
            derived_from=[ev_id],
            agent="stub",
            model="stub",
            prompt_hash="stub",
            metadata={"kind": "ksi_classification", "ksi_id": "KSI-AFR-FSI"},
        )

    # 5. Invoke remediate. The CLI must short-circuit with a clean message
    #    before calling any LLM — if it reached the agent, the test would
    #    fail with a missing-API-key error.
    result = runner.invoke(
        app, ["agent", "remediate", "--ksi", "KSI-AFR-FSI", "--target", str(root)]
    )
    assert result.exit_code == 0, result.output
    assert "no Terraform surface to remediate" in result.output
    assert ".efterlev/manifests/" in result.output


def test_agent_document_without_classifications_prints_error(
    tmp_path: pytest.TempPathFactory,
) -> None:
    init_result = runner.invoke(app, ["init", "--target", str(tmp_path)])
    assert init_result.exit_code == 0, init_result.output
    # Init ran but no `agent gap` yet — no classifications in the store,
    # so the CLI should say so rather than calling the LLM.
    result = runner.invoke(app, ["agent", "document", "--target", str(tmp_path)])
    assert result.exit_code == 1
    assert "0 Gap Agent classifications" in result.output


def test_agent_gap_without_evidence_prints_error(tmp_path: pytest.TempPathFactory) -> None:
    init_result = runner.invoke(app, ["init", "--target", str(tmp_path)])
    assert init_result.exit_code == 0, init_result.output
    # init writes a load-receipt evidence record (primitive-invocation shape),
    # but no detector-emitted Evidence until `scan` runs. The CLI should
    # detect the empty evidence set and say so.
    result = runner.invoke(app, ["agent", "gap", "--target", str(tmp_path)])
    assert result.exit_code == 1
    assert "0 evidence records" in result.output


def test_scan_missing_efterlev_dir_prints_error(tmp_path: pytest.TempPathFactory) -> None:
    result = runner.invoke(app, ["scan", "--target", str(tmp_path)])
    assert result.exit_code == 1
    assert "no `.efterlev/` directory" in result.output
    # v0.1.174 / #380: the error hints that --target is the workspace root
    # (scan recurses) so `scan --target <subdir>` confusion self-corrects.
    assert "workspace ROOT" in result.output
    assert "recurses into subdirectories" in result.output


def test_inspector_does_not_leak_provenance_warning(tmp_path: pytest.TempPathFactory) -> None:
    """v0.1.174 / #380: `report inspector` runs the generate primitive
    under an active store, so the @primitive decorator's "no active
    provenance store" warning must NOT leak to the user's output."""
    init_result = runner.invoke(app, ["init", "--target", str(tmp_path)])
    assert init_result.exit_code == 0, init_result.output
    result = runner.invoke(app, ["report", "inspector", "--target", str(tmp_path)])
    assert result.exit_code == 0, result.output
    assert "no active provenance store" not in result.output
    assert "Inspector report:" in result.output


def test_scan_after_init_produces_evidence(tmp_path: pytest.TempPathFactory) -> None:
    # Write an encrypted bucket then init + scan end-to-end.
    Path(str(tmp_path) + "/main.tf").write_text(
        'resource "aws_s3_bucket" "logs" {\n'
        '  bucket = "logs"\n'
        "  server_side_encryption_configuration {\n"
        "    rule {\n"
        "      apply_server_side_encryption_by_default {\n"
        '        sse_algorithm = "AES256"\n'
        "      }\n"
        "    }\n"
        "  }\n"
        "}\n",
        encoding="utf-8",
    )
    init_result = runner.invoke(app, ["init", "--target", str(tmp_path)])
    assert init_result.exit_code == 0, init_result.output

    # `--verbose` so the per-detector record-ID dump appears in stdout —
    # without it, v0.1.4's quieter default just prints a 1-line summary
    # ("N record(s) written to .efterlev/store.db; pass --verbose...").
    scan_result = runner.invoke(app, ["scan", "--target", str(tmp_path), "--verbose"])
    assert scan_result.exit_code == 0, scan_result.output
    assert "Scanned" in scan_result.output
    assert "resources parsed:" in scan_result.output
    assert "aws.encryption_s3_at_rest" in scan_result.output
    # Manifest loading is now part of `scan`; the record-IDs section is
    # labeled "Detector record IDs" to distinguish from manifest-sourced
    # Evidence (Phase 1, Evidence Manifest landing). Verbose-only as of v0.1.4.
    assert "Detector record IDs" in scan_result.output
    assert "manifest files:" in scan_result.output
    # No `module calls:` line when there are no module declarations — the
    # summary stays terse for the common resource-only case.
    assert "module calls:" not in scan_result.output
    # No plan-JSON warning either.
    assert "module calls detected" not in scan_result.output


def test_scan_warns_about_module_density_when_module_heavy(
    tmp_path: pytest.TempPathFactory,
) -> None:
    """When a codebase is module-composed (the dominant ICP-A pattern),
    `efterlev scan` (HCL mode) must surface a structured warning recommending
    plan-JSON expansion."""
    Path(str(tmp_path) + "/main.tf").write_text(
        'module "vpc" {\n  source = "terraform-aws-modules/vpc/aws"\n}\n'
        'module "eks" {\n  source = "terraform-aws-modules/eks/aws"\n}\n'
        'module "iam" {\n  source = "terraform-aws-modules/iam/aws"\n}\n',
        encoding="utf-8",
    )
    init_result = runner.invoke(app, ["init", "--target", str(tmp_path)])
    assert init_result.exit_code == 0, init_result.output

    scan_result = runner.invoke(app, ["scan", "--target", str(tmp_path)])
    assert scan_result.exit_code == 0, scan_result.output
    # Module-call count is surfaced in the summary block.
    assert "module calls:        3" in scan_result.output
    # Warning fires.
    assert "3 module calls detected" in scan_result.output
    assert "detector coverage is limited in HCL mode" in scan_result.output
    # Remediation is the copy-pasteable plan-JSON command.
    assert "efterlev scan --plan plan.json" in scan_result.output


def test_scan_hard_errors_when_target_sits_below_github_workflows_ancestor(
    tmp_path: pytest.TempPathFactory,
) -> None:
    """v0.1.59: real-customer repos lay out `infra/terraform/` below the
    repo root that holds `.github/workflows/`. Pre-v0.1.12 silently dropped
    every GitHub-source detector with no warning; v0.1.12 added a post-scan
    warning; v0.1.59 promotes that to a pre-scan hard error so a first-run
    user can't accidentally see "20 evidence records" and conclude the tool
    covered their repo when github-source detectors contributed zero.
    `--allow-subdir-target` opts back into the prior behavior."""
    repo = Path(str(tmp_path)) / "repo"
    workflows_dir = repo / ".github" / "workflows"
    workflows_dir.mkdir(parents=True)
    # Make the walk stop at the repo root, not climb to /tmp.
    (repo / ".git").mkdir()
    # A non-empty workflow file so the ancestor check sees a real
    # `.github/workflows/` directory shape.
    (workflows_dir / "ci.yml").write_text("name: ci\non: push\njobs: {}\n")
    target = repo / "infra" / "terraform"
    target.mkdir(parents=True)
    (target / "main.tf").write_text('resource "aws_s3_bucket" "logs" { bucket = "logs" }\n')

    init_result = runner.invoke(app, ["init", "--target", str(target)])
    assert init_result.exit_code == 0, init_result.output

    scan_result = runner.invoke(app, ["scan", "--target", str(target)])
    assert scan_result.exit_code == 2, scan_result.output
    assert "sits below" in scan_result.output
    assert ".github/workflows/" in scan_result.output
    # The two-remediation-paths error message:
    assert f"efterlev scan --target {repo.resolve()}" in scan_result.output
    assert "--allow-subdir-target" in scan_result.output


def test_scan_proceeds_with_warning_when_allow_subdir_target_passed(
    tmp_path: pytest.TempPathFactory,
) -> None:
    """The legitimate monorepo-with-multiple-Terraform-roots case opts in
    via `--allow-subdir-target` and still gets the post-scan warning so the
    coverage trade-off is acknowledged in the output."""
    repo = Path(str(tmp_path)) / "repo"
    workflows_dir = repo / ".github" / "workflows"
    workflows_dir.mkdir(parents=True)
    (repo / ".git").mkdir()
    (workflows_dir / "ci.yml").write_text("name: ci\non: push\njobs: {}\n")
    target = repo / "infra" / "terraform"
    target.mkdir(parents=True)
    (target / "main.tf").write_text('resource "aws_s3_bucket" "logs" { bucket = "logs" }\n')

    init_result = runner.invoke(app, ["init", "--target", str(target)])
    assert init_result.exit_code == 0, init_result.output

    scan_result = runner.invoke(app, ["scan", "--target", str(target), "--allow-subdir-target"])
    assert scan_result.exit_code == 0, scan_result.output
    # Post-scan warning still fires (acknowledges the trade-off the user
    # explicitly opted into).
    assert "GitHub-source detectors skipped this scan" in scan_result.output


def test_scan_does_not_warn_when_target_is_repo_root(
    tmp_path: pytest.TempPathFactory,
) -> None:
    """When `--target` IS the directory containing `.github/workflows/`, no
    warning fires — workflows are scanned in-place. Guards against a regression
    where the F2 helper accidentally treats `--target .` from repo root as a
    subdir miss."""
    repo = Path(str(tmp_path)) / "repo"
    workflows_dir = repo / ".github" / "workflows"
    workflows_dir.mkdir(parents=True)
    (repo / ".git").mkdir()
    (workflows_dir / "ci.yml").write_text("name: ci\non: push\njobs: {}\n")
    (repo / "main.tf").write_text('resource "aws_s3_bucket" "logs" { bucket = "logs" }\n')
    init_result = runner.invoke(app, ["init", "--target", str(repo)])
    assert init_result.exit_code == 0, init_result.output

    scan_result = runner.invoke(app, ["scan", "--target", str(repo)])
    assert scan_result.exit_code == 0, scan_result.output
    assert "found `.github/workflows/`" not in scan_result.output


def test_scan_surfaces_plan_json_hint_when_unparseable_evidence_present(
    tmp_path: pytest.TempPathFactory,
) -> None:
    """F4 (v0.1.12): an `aws_iam_policy` whose `policy` attribute is a
    `jsonencode(...)` expression (the dominant Terraform idiom) emits
    `mfa_required="unparseable"` because python-hcl2 doesn't evaluate
    function calls. Pre-v0.1.12 the unparseable status was buried inside
    individual Evidence records; the fix surfaces a CLI hint pointing
    at plan-JSON mode the first time the user sees the failure pattern."""
    target = Path(str(tmp_path))
    (target / "main.tf").write_text(
        'resource "aws_iam_policy" "x" {\n'
        '  name = "x"\n'
        "  policy = jsonencode({\n"
        '    Version = "2012-10-17"\n'
        "    Statement = []\n"
        "  })\n"
        "}\n"
    )
    init_result = runner.invoke(app, ["init", "--target", str(target)])
    assert init_result.exit_code == 0, init_result.output

    scan_result = runner.invoke(app, ["scan", "--target", str(target)])
    assert scan_result.exit_code == 0, scan_result.output
    assert "evidence record(s) contain unparseable" in scan_result.output
    assert "efterlev scan --plan plan.json" in scan_result.output


def test_scan_does_not_surface_unparseable_hint_in_plan_mode(
    tmp_path: pytest.TempPathFactory,
) -> None:
    """In plan-JSON mode the recommendation makes no sense — guard against
    a regression where the F4 hint fires for plan-mode scans too."""
    target = Path(str(tmp_path))
    # Empty .tf so no detectors fire and no unparseable evidence appears.
    (target / "main.tf").write_text("")
    plan = target / "plan.json"
    # Minimal valid plan-JSON shape — empty resource set, no providers required.
    plan.write_text(
        '{"format_version":"1.2","terraform_version":"1.5.0",'
        '"planned_values":{"root_module":{}},"resource_changes":[],'
        '"configuration":{"root_module":{}}}\n'
    )
    init_result = runner.invoke(app, ["init", "--target", str(target)])
    assert init_result.exit_code == 0, init_result.output

    scan_result = runner.invoke(app, ["scan", "--target", str(target), "--plan", str(plan)])
    assert scan_result.exit_code == 0, scan_result.output
    assert "evidence record(s) contain unparseable" not in scan_result.output


def test_init_succeeds_and_prints_summary(tmp_path: pytest.TempPathFactory) -> None:
    result = runner.invoke(app, ["init", "--target", str(tmp_path)])
    assert result.exit_code == 0, result.output
    assert "Initialized" in result.output
    assert "FRMR:" in result.output
    assert "NIST SP 800-53 Rev 5:" in result.output


def test_init_claude_code_backend_pins_sonnet_model_v0_1_175(
    tmp_path: pytest.TempPathFactory,
) -> None:
    """v0.1.175 / #381: --llm-backend=claude_code pins the workspace model
    to claude-sonnet-4-6 (NOT the gap agent's Opus default). Large Opus-4.7
    calls via `claude --print` are pathologically slow on the subscription,
    so the gap stage couldn't finish; Sonnet is validated-equivalent and
    fast. Supersedes the v0.1.158 'Opus is free upside' default.
    """
    result = runner.invoke(app, ["init", "--target", str(tmp_path), "--llm-backend=claude_code"])
    assert result.exit_code == 0, result.output
    config_text = (Path(str(tmp_path)) / ".efterlev" / "config.toml").read_text()
    assert 'backend = "claude_code"' in config_text
    assert 'model = "claude-sonnet-4-6"' in config_text
    # fallback is also Sonnet now (claude_code client ignores it anyway).
    assert 'fallback_model = "claude-sonnet-4-6"' in config_text
    assert "claude-opus-4-7" not in config_text


def test_init_claude_code_respects_explicit_llm_model_v0_1_175(
    tmp_path: pytest.TempPathFactory,
) -> None:
    """An explicit --llm-model still wins over the Sonnet default — a user
    who wants Opus on subscription (and accepts the latency) can ask."""
    result = runner.invoke(
        app,
        [
            "init",
            "--target",
            str(tmp_path),
            "--llm-backend=claude_code",
            "--llm-model=claude-opus-4-7",
        ],
    )
    assert result.exit_code == 0, result.output
    config_text = (Path(str(tmp_path)) / ".efterlev" / "config.toml").read_text()
    assert 'model = "claude-opus-4-7"' in config_text


def test_init_anthropic_backend_keeps_sonnet_fallback_v0_1_158(
    tmp_path: pytest.TempPathFactory,
) -> None:
    """v0.1.158 / #363: Anthropic API (and Bedrock) keep the
    `DEFAULT_FALLBACK_MODEL = claude-sonnet-4-6` default — Opus is ~5x
    the spend on those backends, Sonnet stays the cost/quality sweet spot.
    """
    result = runner.invoke(app, ["init", "--target", str(tmp_path), "--llm-backend=anthropic"])
    assert result.exit_code == 0, result.output
    config_text = (Path(str(tmp_path)) / ".efterlev" / "config.toml").read_text()
    assert 'backend = "anthropic"' in config_text
    assert 'fallback_model = "claude-sonnet-4-6"' in config_text


def test_init_rejects_unknown_llm_backend_with_clear_error_v0_1_158(
    tmp_path: pytest.TempPathFactory,
) -> None:
    """v0.1.158 / #363: the rejection message names all valid backends so the
    user can correct the typo without re-reading docs. v0.1.211 added openai;
    v0.1.216 added bedrock_openai."""
    result = runner.invoke(app, ["init", "--target", str(tmp_path), "--llm-backend=foo"])
    assert result.exit_code == 2
    assert (
        "must be 'anthropic', 'bedrock', 'claude_code', 'openai', or 'bedrock_openai'"
        in result.output
    )


def test_init_rejects_region_with_claude_code_backend_v0_1_158(
    tmp_path: pytest.TempPathFactory,
) -> None:
    """v0.1.158 / #363: --llm-region is Bedrock-only. Pre-v0.1.158 the
    check only mentioned the anthropic case; now mentions both anthropic
    and claude_code."""
    result = runner.invoke(
        app,
        [
            "init",
            "--target",
            str(tmp_path),
            "--llm-backend=claude_code",
            "--llm-region=us-east-1",
        ],
    )
    assert result.exit_code == 2
    assert "--llm-region is only valid with --llm-backend=bedrock" in result.output


def test_init_refuses_existing_workspace(tmp_path: pytest.TempPathFactory) -> None:
    first = runner.invoke(app, ["init", "--target", str(tmp_path)])
    assert first.exit_code == 0
    second = runner.invoke(app, ["init", "--target", str(tmp_path)])
    assert second.exit_code == 1
    assert "already exists" in second.output


def test_provenance_show_missing_efterlev_dir_prints_error(
    tmp_path: pytest.TempPathFactory,
) -> None:
    # tmp_path has no `.efterlev/` — the CLI should error cleanly, not explode.
    result = runner.invoke(app, ["provenance", "show", "sha256:abc", "--target", str(tmp_path)])
    assert result.exit_code == 1
    assert "no `.efterlev/` directory" in result.output


def test_provenance_show_resolves_short_prefix_from_rationale(tmp_path: Path) -> None:
    """Rationales / POA&Ms print 8-char SHA prefixes for readability; the CLI
    must accept both the prefix and the full id so users can paste either."""
    init_result = runner.invoke(app, ["init", "--target", str(tmp_path)])
    assert init_result.exit_code == 0, init_result.output

    from efterlev.provenance import ProvenanceStore

    with ProvenanceStore(tmp_path) as store:
        record = store.write_record(payload={"x": 1}, record_type="evidence")
    short = record.record_id[len("sha256:") : len("sha256:") + 8]

    result = runner.invoke(app, ["provenance", "show", short, "--target", str(tmp_path)])
    assert result.exit_code == 0, result.output
    # Resolution banner makes the substitution observable.
    assert f"resolved {short}" in result.output
    assert record.record_id in result.output


def test_provenance_show_unknown_prefix_prints_error(tmp_path: Path) -> None:
    init_result = runner.invoke(app, ["init", "--target", str(tmp_path)])
    assert init_result.exit_code == 0
    result = runner.invoke(
        app, ["provenance", "show", "sha256:deadbeef", "--target", str(tmp_path)]
    )
    assert result.exit_code == 1
    assert "no record matches" in result.output


def test_provenance_show_surfaces_dual_key_for_evidence_records(tmp_path: Path) -> None:
    """v0.1.11 (3PAO finding): when the resolved record is an Evidence
    record, surface BOTH `record_id` (envelope hash — what the store
    walks) AND `evidence_id` (content hash — what reports cite). Reviewers
    were unable to verify that POA&M/gap-report citations matched what
    `provenance show` walked because the dual-key reality was hidden."""
    init_result = runner.invoke(app, ["init", "--target", str(tmp_path)])
    assert init_result.exit_code == 0, init_result.output

    from efterlev.models import Evidence, SourceRef
    from efterlev.provenance import ProvenanceStore

    with ProvenanceStore(tmp_path) as store:
        # Build an Evidence-shaped payload so the record's payload.evidence_id
        # is structurally distinct from the envelope record_id.
        ev = Evidence.create(
            detector_id="aws.encryption_s3_at_rest",
            source_ref=SourceRef(file=Path("main.tf"), line_start=1, line_end=10),
            ksis_evidenced=["KSI-SVC-VRI"],
            controls_evidenced=["SC-28"],
            content={"resource_name": "audit", "encryption_state": "present"},
        )
        record = store.write_record(
            payload=ev.model_dump(mode="json"),
            record_type="evidence",
            primitive="aws.encryption_s3_at_rest@0.1.0",
        )

    result = runner.invoke(app, ["provenance", "show", record.record_id, "--target", str(tmp_path)])
    assert result.exit_code == 0, result.output
    # Both labels visible so the reviewer can match a gap-report citation
    # (printed by `evidence_id`) against the walker output (keyed by
    # `record_id`).
    assert "record_id:" in result.output
    assert "evidence_id:" in result.output
    assert ev.evidence_id in result.output
    assert record.record_id in result.output


def test_poam_default_output_lands_under_reports_poam_subdir(tmp_path: Path) -> None:
    """v0.1.6: POA&M output goes under `.efterlev/reports/poam/poam-<ts>.md`,
    not the flat `.efterlev/reports/poam-<ts>.md` path. Locks alignment with
    the runbook docs and clusters per-report-type artifacts."""
    from efterlev.agents.gap import KsiClassification
    from efterlev.models import Claim
    from efterlev.provenance import ProvenanceStore

    init_result = runner.invoke(app, ["init", "--target", str(tmp_path)])
    assert init_result.exit_code == 0, init_result.output

    # Seed a synthetic Gap classification so `efterlev poam` has something
    # to write. We bypass the LLM by writing a Claim record directly — the
    # poam reader only needs ksi_classification claims to exist.
    with ProvenanceStore(tmp_path) as store:
        clf = KsiClassification(
            ksi_id="KSI-SVC-VRI",
            status="not_implemented",
            rationale="Synthetic classification for path-locking test.",
            evidence_ids=[],
        )
        claim = Claim.create(
            claim_type="classification",
            content={
                "ksi_id": clf.ksi_id,
                "status": clf.status,
                "rationale": clf.rationale,
            },
            confidence="medium",
            derived_from=[],
            model="stub",
            prompt_hash="x" * 64,
        )
        store.write_record(
            payload=claim.model_dump(mode="json"),
            record_type="claim",
            agent="gap_agent@0.1.0",
            metadata={"kind": "ksi_classification", "ksi_id": clf.ksi_id},
        )

    result = runner.invoke(app, ["poam", "--target", str(tmp_path)])
    assert result.exit_code == 0, result.output

    # v0.1.160 / #365 visible-output split: POA&M lands under
    # efterlev-out/reports/poam/ instead of .efterlev/reports/poam/.
    # v0.1.6 sub-directory convention preserved (poam-<ts>.md under
    # reports/poam/, not flat reports/poam-<ts>.md).
    poam_subdir = tmp_path / "efterlev-out" / "reports" / "poam"
    assert poam_subdir.is_dir(), f"expected {poam_subdir} to exist after poam run"
    files = list(poam_subdir.glob("poam-*.md"))
    assert files, f"expected at least one poam-*.md file in {poam_subdir}"
    # And NOT in the flat (old) location.
    flat_files = list((tmp_path / "efterlev-out" / "reports").glob("poam-*.md"))
    assert not flat_files, (
        f"v0.1.5 wrote to flat reports/poam-*.md; v0.1.6+ must only "
        f"write under reports/poam/. Found stragglers: {flat_files}"
    )


def test_remediate_requires_ksi_option() -> None:
    result = runner.invoke(app, ["agent", "remediate"])
    # Missing required --ksi should fail at Typer's argument parser (exit 2),
    # not reach the stub body.
    assert result.exit_code == 2
    assert result.exception is None or not isinstance(result.exception, NotImplementedError)


# --- boundary CLI verbs (Priority 4.2, 2026-04-27) ------------------------


def test_boundary_show_on_undeclared_workspace(tmp_path: Path) -> None:
    """Fresh workspace has no boundary; `boundary show` says so + suggests next step."""
    init_result = runner.invoke(app, ["init", "--target", str(tmp_path)])
    assert init_result.exit_code == 0, init_result.output

    show = runner.invoke(app, ["boundary", "show", "--target", str(tmp_path)])
    assert show.exit_code == 0, show.output
    assert "No boundary declared" in show.output
    assert "boundary_undeclared" in show.output
    assert "boundary set --include" in show.output


def test_boundary_set_then_show_round_trips(tmp_path: Path) -> None:
    """`set` writes patterns; `show` reads them back including counts."""
    init_result = runner.invoke(app, ["init", "--target", str(tmp_path)])
    assert init_result.exit_code == 0

    set_result = runner.invoke(
        app,
        [
            "boundary",
            "set",
            "--target",
            str(tmp_path),
            "--include",
            "boundary/**",
            "--include",
            "infra/prod/**",
            "--exclude",
            "**/test/**",
        ],
    )
    assert set_result.exit_code == 0, set_result.output
    assert "include (2)" in set_result.output
    assert "exclude (1)" in set_result.output

    show = runner.invoke(app, ["boundary", "show", "--target", str(tmp_path)])
    assert show.exit_code == 0
    assert "boundary/**" in show.output
    assert "infra/prod/**" in show.output
    assert "**/test/**" in show.output
    assert "exclude wins over include" in show.output


def test_boundary_set_replaces_by_default(tmp_path: Path) -> None:
    """v0.1.9: `set` REPLACES by default (matches the verb's intuition).
    Calling `set` twice without `--append` discards the first pattern set
    and keeps only the latest. Pre-v0.1.9 this would have appended,
    accumulating patterns silently — surprised users."""
    init_result = runner.invoke(app, ["init", "--target", str(tmp_path)])
    assert init_result.exit_code == 0
    runner.invoke(app, ["boundary", "set", "--target", str(tmp_path), "--include", "old/**"])
    runner.invoke(app, ["boundary", "set", "--target", str(tmp_path), "--include", "new/**"])

    show = runner.invoke(app, ["boundary", "show", "--target", str(tmp_path)])
    assert "new/**" in show.output
    assert "old/**" not in show.output
    assert "include (1)" in show.output


def test_boundary_set_append_flag_keeps_existing_patterns(tmp_path: Path) -> None:
    """v0.1.9: `--append` opts into accumulating patterns (the pre-v0.1.9
    default). Useful for scripts that want to layer patterns without
    restating the full list."""
    init_result = runner.invoke(app, ["init", "--target", str(tmp_path)])
    assert init_result.exit_code == 0
    runner.invoke(app, ["boundary", "set", "--target", str(tmp_path), "--include", "a/**"])
    runner.invoke(
        app,
        ["boundary", "set", "--target", str(tmp_path), "--append", "--include", "b/**"],
    )

    show = runner.invoke(app, ["boundary", "show", "--target", str(tmp_path)])
    assert "a/**" in show.output
    assert "b/**" in show.output
    assert "include (2)" in show.output


def test_boundary_set_replace_flag_is_deprecated_noop(tmp_path: Path) -> None:
    """v0.1.9: `--replace` is now a no-op (replace is the default). Kept
    for backwards-compat with pre-v0.1.9 scripts that passed it explicitly;
    surfaces a one-line deprecation note."""
    init_result = runner.invoke(app, ["init", "--target", str(tmp_path)])
    assert init_result.exit_code == 0
    runner.invoke(app, ["boundary", "set", "--target", str(tmp_path), "--include", "old/**"])
    result = runner.invoke(
        app,
        [
            "boundary",
            "set",
            "--target",
            str(tmp_path),
            "--replace",
            "--include",
            "new/**",
        ],
    )
    # Behavior is correct (replace happened — that's the default).
    show = runner.invoke(app, ["boundary", "show", "--target", str(tmp_path)])
    assert "new/**" in show.output
    assert "old/**" not in show.output
    # Deprecation note surfaces on stderr.
    assert "--replace is now the default" in result.output


def test_boundary_set_with_no_patterns_errors(tmp_path: Path) -> None:
    """`boundary set` with no --include/--exclude is a usage error.

    Typer can't catch this (both options are list-typed and default to []),
    so the command checks at runtime and exits with code 2."""
    init_result = runner.invoke(app, ["init", "--target", str(tmp_path)])
    assert init_result.exit_code == 0
    result = runner.invoke(app, ["boundary", "set", "--target", str(tmp_path)])
    assert result.exit_code == 2
    assert "at least one --include or --exclude" in result.output


def test_boundary_check_classifies_path(tmp_path: Path) -> None:
    """`boundary check <path>` echoes the resolved state."""
    init_result = runner.invoke(app, ["init", "--target", str(tmp_path)])
    assert init_result.exit_code == 0
    runner.invoke(
        app,
        [
            "boundary",
            "set",
            "--target",
            str(tmp_path),
            "--include",
            "boundary/**",
            "--exclude",
            "**/test/**",
        ],
    )

    in_check = runner.invoke(
        app, ["boundary", "check", "--target", str(tmp_path), "boundary/main.tf"]
    )
    assert in_check.exit_code == 0
    assert "in_boundary" in in_check.output

    out_check = runner.invoke(
        app, ["boundary", "check", "--target", str(tmp_path), "commercial/eks.tf"]
    )
    assert out_check.exit_code == 0
    assert "out_of_boundary" in out_check.output

    excluded_check = runner.invoke(
        app, ["boundary", "check", "--target", str(tmp_path), "boundary/test/iam.tf"]
    )
    assert excluded_check.exit_code == 0
    assert "out_of_boundary" in excluded_check.output


def test_boundary_set_missing_workspace_errors(tmp_path: Path) -> None:
    """Without a workspace at the target, `boundary set` exits cleanly."""
    result = runner.invoke(
        app,
        ["boundary", "set", "--target", str(tmp_path), "--include", "boundary/**"],
    )
    assert result.exit_code == 1
    assert "config not found" in result.output


def test_display_path_keeps_user_target_form_for_symlinked_dirs(tmp_path: Path) -> None:
    # On macOS /tmp is a symlink to /private/tmp; the same paper-cut shows
    # up anywhere a user passes a path under a symlinked directory. Verify
    # the helper reconstructs the path under the un-resolved target form.
    from efterlev.cli.main import _display_path

    real_dir = tmp_path / "real"
    real_dir.mkdir()
    (real_dir / ".efterlev" / "reports").mkdir(parents=True)
    report = real_dir / ".efterlev" / "reports" / "gap-1.html"
    report.write_text("<html/>", encoding="utf-8")

    symlink_target = tmp_path / "link"
    symlink_target.symlink_to(real_dir)

    # User passed `tmp/link/...`; canonical form lives under `tmp/real/...`.
    # Display should re-stitch the path under the user-supplied form.
    displayed = _display_path(report, symlink_target)
    assert str(symlink_target) in displayed
    assert str(real_dir) not in displayed

    # Sanity: a path not under target.resolve() falls back to its own str().
    outside = tmp_path / "elsewhere.txt"
    outside.write_text("", encoding="utf-8")
    assert _display_path(outside, symlink_target) == str(outside)
