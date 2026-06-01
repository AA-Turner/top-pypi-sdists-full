"""Runtime-evidence imports — consume pre-existing tool output.

Detectors PARSE local IaC + workflows. Imports CONSUME runtime tool
output the customer already has (AWS Security Hub, AWS Config, Prowler).

Both layers emit `Evidence` records into the same provenance store, so
the Gap Agent reasons over IaC + runtime evidence uniformly. This is
the M1 arc per the v0.1.111 technical roadmap — closes the FedRAMP 20x
70% threshold story by making the runtime layer a workflow instead of
a manual Evidence-Manifest authoring step.

M1 arc complete at v0.1.124: Security Hub (ASFF), AWS Config evaluations,
and Prowler native JSON all default-on. The `--allow-import` opt-in flag
that gated Stages 1-5 was removed at graduation (mirrors the v0.1.102
removal of `--allow-cfn`).

Honest scope:
- File-based ingestion only (path arg, no AWS API calls). Customer is
  still the one running `aws securityhub get-findings` / `prowler aws -M
  json` / `aws configservice get-compliance-details-by-config-rule`.
  Efterlev consumes; never originates the cloud call. Local-first
  posture intact.
"""
