#!/usr/bin/env bash
# triage.sh — deterministic, zero-LLM post-release validation of a published Efterlev release.
#
# This script runs the same methodology that surfaced F1–H1 across the
# v0.1.12–v0.1.15 patch arc: install the published wheel from PyPI in a
# fresh venv, run sanity checks (--version, doctor shape, detector
# count), invoke verify-release.sh against the wheel + container,
# inspect the container manifest for multi-arch + supply-chain
# attestations, and run check-docs.py against the tagged source. Every
# check is deterministic — no LLM call, no per-PR cost.
#
# Phases (v0.1.22):
#   T1 install (pipx + version sanity)
#   T2 doctor shape (7 expected checks)
#   T3 detector count
#   T4 verify-release.sh (4/4 PEP 740 + cosign signature + SLSA v1
#       attestation, all cryptographically verified — source of truth
#       for "is the release signed and attested correctly")
#   T5 container manifest (multi-arch via OCI registry API; no docker daemon)
#   T6 check-docs.py against the tagged source
#   T7 release-smoke matrix (workflow_run conclusion via GH Actions API).
#       Added in v0.1.22 after release-smoke was found to have been
#       silently failing across v0.1.20 + v0.1.21 — the matrix workflow
#       row stayed "queued" in `gh run list` even though every cell
#       failed on a stale assertion script. T7 surfaces matrix
#       conclusion on the Release page so silent regressions cannot
#       recur. PENDING is a valid status if release-smoke hasn't yet
#       completed by the time post-release-triage fires; the workflow
#       reruns triage on release-smoke completion to repopulate.
#
# v0.1.16 originally had a separate T6 "cosign tree visibility" that
# greped `cosign tree` output for the SLSA attestation. Dropped in
# v0.1.17 because cosign 2.6.x's `cosign tree` doesn't enumerate OCI 1.1
# referrer attestations (which is what `actions/attest-build-provenance`
# writes). It produced false-negative FAILs on v0.1.16's first auto-
# triage even though the SLSA attestation was correctly attached. T4
# already cryptographically verifies attestation presence + validity.
#
# Usage:
#   scripts/triage.sh v0.1.17
#
# Output:
#   GitHub-Flavored-Markdown triage report on stdout, suitable for
#   posting as a GitHub Release notes body. Includes per-check status
#   table + per-finding detail.
#
# Exit codes:
#   0 — every required check passed (release ships clean)
#   1 — at least one required check failed (paper cut to triage)
#   2 — usage error or missing prerequisite tool
#
# Designed to be invoked from `.github/workflows/post-release-triage.yml`
# on every tag push, with the report auto-attached as the GH Release
# body. Also runnable locally for ad-hoc validation of any prior tag.

set -euo pipefail

# ---------- argument parsing ----------

if [ $# -ne 1 ]; then
  echo "Usage: $0 <version>" >&2
  echo "Example: $0 v0.1.16" >&2
  exit 2
fi

VERSION="${1#v}"
TAG="v${VERSION}"
EXPECTED_DETECTORS=66  # Updated alongside detector additions; tests/test_triage_constant_alignment.py locks this against `len(get_registry())` so drift fails the suite at PR time.

# ---------- tool checks ----------

missing=0
need() {
  command -v "$1" >/dev/null 2>&1 || { echo "  missing: $1" >&2; missing=1; }
}
need curl
need python3
need pipx
need cosign
if ! python3 -c "import sigstore" >/dev/null 2>&1; then
  echo "  missing: sigstore Python package" >&2
  missing=1
fi
if [ "$missing" -ne 0 ]; then
  echo "" >&2
  echo "Install missing tools:" >&2
  echo "  pipx:     https://pipx.pypa.io/stable/installation/" >&2
  echo "  cosign:   https://docs.sigstore.dev/system_config/installation" >&2
  echo "  sigstore: python3 -m pip install sigstore" >&2
  exit 2
fi

# ---------- locate verify-release.sh + check-docs.py ----------
# Resolve relative to this script so the triage works whether invoked from
# a checkout or from a workflow runner.
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VERIFY_RELEASE="$SCRIPT_DIR/verify-release.sh"
CHECK_DOCS="$SCRIPT_DIR/check-docs.py"

# ---------- shared state ----------

WORKDIR="$(mktemp -d)"
trap 'rm -rf "$WORKDIR"' EXIT
PIPX_HOME="$WORKDIR/pipx"
PIPX_BIN_DIR="$WORKDIR/pipx_bin"
mkdir -p "$PIPX_HOME" "$PIPX_BIN_DIR"
export PIPX_HOME PIPX_BIN_DIR
export PATH="$PIPX_BIN_DIR:$PATH"

declare -a CHECK_NAMES=()
declare -a CHECK_STATUS=()
declare -a CHECK_DETAIL=()

record() {
  CHECK_NAMES+=("$1")
  CHECK_STATUS+=("$2")
  CHECK_DETAIL+=("$3")
}

# ---------- T1: install via pipx into isolated workdir ----------

t1_install() {
  # Capture stderr (don't swallow with `>/dev/null 2>&1`) so the failure
  # detail surfaces in the report. v0.1.18's first auto-triage hit a
  # pipx-install failure where the swallowed-stderr fallback message
  # ("the wheel may not be on PyPI yet") was wrong — the wheel WAS on
  # PyPI (T4 verified the Sigstore signature), the actual failure was
  # something else. Surfacing real stderr makes the next pipx hiccup
  # immediately diagnosable instead of guess-worky.
  install_log="$WORKDIR/pipx_install.log"
  if pipx install --pip-args="--no-cache-dir" "efterlev==${VERSION}" >"$install_log" 2>&1; then
    actual_version="$(efterlev --version 2>&1 | awk '{print $2}')"
    if [ "$actual_version" = "$VERSION" ]; then
      record "T1 install" "PASS" "wheel installed; \`efterlev --version\` → $actual_version"
    else
      record "T1 install" "FAIL" "version mismatch: pipx installed efterlev==$VERSION but \`efterlev --version\` → $actual_version"
    fi
  else
    # Truncate captured output to the last 5 lines (markdown-table-safe;
    # full log lives in $WORKDIR if a maintainer reruns locally).
    last_lines="$(tail -5 "$install_log" 2>/dev/null | tr '\n' ';' | sed 's/  */ /g' | sed 's/|/\\|/g')"
    record "T1 install" "FAIL" "\`pipx install efterlev==$VERSION\` exited non-zero. Tail of pipx output: ${last_lines:-<empty>}"
  fi
}

# ---------- T2: doctor shape sanity ----------

t2_doctor() {
  out="$(efterlev doctor 2>&1 || true)"
  expected_checks=(
    "python_version"
    "install_uniqueness"
    "efterlev_dir"
    "frmr_cache"
    "anthropic_api_key"
    "bedrock_credentials"
    "boundary_declared"
  )
  missing=()
  for c in "${expected_checks[@]}"; do
    grep -q "$c" <<< "$out" || missing+=("$c")
  done
  if [ ${#missing[@]} -eq 0 ]; then
    record "T2 doctor shape" "PASS" "all 7 checks present (python_version, install_uniqueness, efterlev_dir, frmr_cache, anthropic_api_key, bedrock_credentials, boundary_declared)"
  else
    record "T2 doctor shape" "FAIL" "missing checks: ${missing[*]}"
  fi
}

# ---------- T3: detector count ----------

t3_detectors() {
  out="$(efterlev detectors list 2>&1 || true)"
  if grep -q "total: ${EXPECTED_DETECTORS} detectors" <<< "$out"; then
    record "T3 detector count" "PASS" "registry reports ${EXPECTED_DETECTORS} detectors"
  else
    actual="$(grep -oE 'total: [0-9]+ detectors' <<< "$out" | head -1 || echo 'unknown')"
    record "T3 detector count" "FAIL" "expected ${EXPECTED_DETECTORS} detectors; actual: $actual"
  fi
}

# ---------- T4: verify-release.sh (PyPI Sigstore + cosign + SLSA) ----------

t4_verify_release() {
  if [ ! -x "$VERIFY_RELEASE" ]; then
    record "T4 verify-release.sh" "FAIL" "$VERIFY_RELEASE not found or not executable"
    return
  fi
  out="$(bash "$VERIFY_RELEASE" "$TAG" 2>&1 || true)"
  passed="$(grep -oE 'passed: [0-9]+' <<< "$out" | tail -1 | awk '{print $2}' || echo 0)"
  failed="$(grep -oE 'failed: [0-9]+' <<< "$out" | tail -1 | awk '{print $2}' || echo 0)"
  if [ "${failed:-0}" -eq 0 ] && [ "${passed:-0}" -ge 4 ]; then
    record "T4 verify-release.sh" "PASS" "$passed/4 checks passed (PyPI PEP 740 + cosign + SLSA v1)"
  else
    record "T4 verify-release.sh" "FAIL" "$passed passed, $failed failed — see verify-release.sh output for detail"
  fi
}

# ---------- T5: container manifest sanity (multi-arch) ----------

t5_container_manifest() {
  token="$(curl -sfL "https://ghcr.io/token?scope=repository:efterlev/efterlev:pull&service=ghcr.io" | python3 -c "import json,sys; print(json.load(sys.stdin)['token'])" 2>/dev/null || echo)"
  if [ -z "$token" ]; then
    record "T5 container manifest" "FAIL" "could not obtain ghcr.io pull token"
    return
  fi
  manifest="$(curl -sfL -H "Authorization: Bearer $token" -H "Accept: application/vnd.oci.image.index.v1+json" "https://ghcr.io/v2/efterlev/efterlev/manifests/$TAG" 2>/dev/null || echo)"
  if [ -z "$manifest" ]; then
    record "T5 container manifest" "FAIL" "manifest fetch returned empty (image not pushed for $TAG?)"
    return
  fi
  # Extract platforms; expect linux/amd64 + linux/arm64.
  platforms="$(python3 -c "
import json, sys
m = json.loads('''$manifest''')
seen = set()
for s in m.get('manifests', []):
    p = s.get('platform', {})
    if p.get('os') and p.get('architecture') and p.get('os') != 'unknown':
        seen.add(p['os'] + '/' + p['architecture'])
print(' '.join(sorted(seen)))
" 2>/dev/null || echo)"
  if [[ "$platforms" == *"linux/amd64"* && "$platforms" == *"linux/arm64"* ]]; then
    record "T5 container manifest" "PASS" "multi-arch image present: $platforms"
  else
    record "T5 container manifest" "FAIL" "expected linux/amd64 + linux/arm64; got: $platforms"
  fi
}

# T6 (cosign tree visibility) was DROPPED in v0.1.17. Reason: cosign 2.6.x's
# `cosign tree` doesn't enumerate OCI 1.1 referrer attestations (which is
# what `actions/attest-build-provenance` writes). The check produced false-
# negative FAILs in v0.1.16's first auto-triage even though the SLSA
# attestation was correctly attached. T4 (verify-release.sh) already covers
# both signature presence/validity and attestation presence/validity via
# `cosign verify-attestation --type slsaprovenance1` — that's the
# cryptographic source of truth. T6 was a redundant lightweight inventory
# check whose mechanism failed in 2.6.x while T4's mechanism worked. v0.1.17
# drops T6; T1-T5 + T7 (now T6) carry forward.

# ---------- T7: release-smoke matrix conclusion ----------

t7_release_smoke() {
  # Surface release-smoke matrix conclusion on the Release page. v0.1.20 +
  # v0.1.21 had release-smoke silently red across every matrix cell because
  # `gh run list` collapses workflow_run state to a single column that stayed
  # "queued" while individual matrix jobs failed. T7 closes that gap by
  # querying the GH Actions API and reporting matrix conclusion explicitly.
  token="${GH_TOKEN:-${GITHUB_TOKEN:-}}"
  if [ -z "$token" ]; then
    record "T7 release-smoke" "SKIP" "no GH token in env; skipping matrix-status query"
    return
  fi
  runs_json="$WORKDIR/release_smoke_runs.json"
  if ! curl -sfL -H "Authorization: Bearer $token" \
      -H "Accept: application/vnd.github+json" \
      "https://api.github.com/repos/efterlev/efterlev/actions/workflows/release-smoke.yml/runs?per_page=20" \
      > "$runs_json" 2>/dev/null; then
    record "T7 release-smoke" "FAIL" "could not query release-smoke workflow runs API"
    return
  fi
  parsed="$(python3 - "$runs_json" "$TAG" <<'PY'
import json, sys
runs_path, tag = sys.argv[1], sys.argv[2]
try:
    data = json.load(open(runs_path))
except Exception as e:
    print(f"PARSE_ERROR|{e}|0")
    sys.exit(0)
candidates = [
    r for r in data.get("workflow_runs", [])
    if r.get("head_branch") == tag and r.get("event") == "push"
]
if not candidates:
    print("NOT_FOUND|no matching run|0")
else:
    r = sorted(candidates, key=lambda x: x.get("updated_at", ""), reverse=True)[0]
    status = r.get("status") or "unknown"
    conclusion = r.get("conclusion") or "pending"
    rid = r.get("id") or 0
    print(f"{status}|{conclusion}|{rid}")
PY
)"
  status="${parsed%%|*}"
  rest="${parsed#*|}"
  conclusion="${rest%%|*}"
  run_id="${rest##*|}"
  case "$status" in
    NOT_FOUND)
      record "T7 release-smoke" "SKIP" "no release-smoke push run found for $TAG yet"
      return
      ;;
    PARSE_ERROR)
      record "T7 release-smoke" "FAIL" "could not parse workflow_runs API response: $conclusion"
      return
      ;;
  esac
  if [ "$status" != "completed" ]; then
    record "T7 release-smoke" "PENDING" "release-smoke run #$run_id still $status; T7 repopulates when it completes (post-release-triage reruns on release-smoke completion)"
    return
  fi
  if [ "$conclusion" = "success" ]; then
    record "T7 release-smoke" "PASS" "matrix green across all cells (run #$run_id)"
    return
  fi
  jobs_json="$WORKDIR/release_smoke_jobs.json"
  if curl -sfL -H "Authorization: Bearer $token" \
      -H "Accept: application/vnd.github+json" \
      "https://api.github.com/repos/efterlev/efterlev/actions/runs/$run_id/jobs?per_page=100" \
      > "$jobs_json" 2>/dev/null; then
    failed_cells="$(python3 - "$jobs_json" <<'PY'
import json, sys
try:
    d = json.load(open(sys.argv[1]))
except Exception:
    print("<could not parse jobs API response>")
    sys.exit(0)
fails = [j["name"] for j in d.get("jobs", []) if j.get("conclusion") == "failure"]
print(", ".join(fails) if fails else "<no failed jobs returned by API>")
PY
)"
  else
    failed_cells="<could not query jobs API>"
  fi
  record "T7 release-smoke" "FAIL" "matrix conclusion: $conclusion (run #$run_id); failed cells: $failed_cells"
}

# ---------- T6 (was T7): check-docs.py against the tagged source ----------

t6_check_docs() {
  if [ ! -f "$CHECK_DOCS" ]; then
    record "T6 check-docs" "SKIP" "$CHECK_DOCS not found (running outside a repo checkout?)"
    return
  fi
  # check-docs.py must run from a checkout root; locate that as the parent of scripts/.
  repo_root="$(cd "$SCRIPT_DIR/.." && pwd)"
  out="$(cd "$repo_root" && uv run python "$CHECK_DOCS" 2>&1 || true)"
  if grep -q "RESULT: clean" <<< "$out"; then
    record "T6 check-docs" "PASS" "no doc-vs-code drift detected"
  else
    findings="$(grep -E "^  [^[:space:]]+\.md:" <<< "$out" | head -3 | tr '\n' '; ' || echo)"
    record "T6 check-docs" "FAIL" "drift detected: $findings"
  fi
}

# ---------- run all checks ----------

t1_install
t2_doctor
t3_detectors
t4_verify_release
t5_container_manifest
t6_check_docs
t7_release_smoke

# ---------- emit markdown report ----------

cat <<EOF
# Efterlev $TAG — post-release triage

Deterministic, zero-LLM validation of the published wheel + container.
Generated by \`scripts/triage.sh\` on every tag push (see
\`.github/workflows/post-release-triage.yml\`).

## Summary

| Check | Status | Detail |
|---|---|---|
EOF

passed_count=0
failed_count=0
for i in "${!CHECK_NAMES[@]}"; do
  name="${CHECK_NAMES[i]}"
  status="${CHECK_STATUS[i]}"
  detail="${CHECK_DETAIL[i]}"
  case "$status" in
    PASS)    marker="✅ PASS"; passed_count=$((passed_count + 1));;
    FAIL)    marker="❌ FAIL"; failed_count=$((failed_count + 1));;
    SKIP)    marker="⏭️ SKIP";;
    PENDING) marker="⏳ PENDING";;
    *)       marker="❓ $status";;
  esac
  # Pipe-escape detail so markdown table doesn't break.
  detail_md="${detail//|/\\|}"
  printf "| %s | %s | %s |\n" "$name" "$marker" "$detail_md"
done

cat <<EOF

**Result:** ${passed_count} passed, ${failed_count} failed.

EOF

if [ "$failed_count" -gt 0 ]; then
  cat <<EOF
## Findings

EOF
  for i in "${!CHECK_NAMES[@]}"; do
    if [ "${CHECK_STATUS[i]}" = "FAIL" ]; then
      # Use printf '%s\n' ... rather than `printf "- ..."` because the
      # literal `-` at the start of the format string is interpreted as
      # a printf flag and produces an "invalid option" error.
      printf '%s\n' "- **${CHECK_NAMES[i]}**: ${CHECK_DETAIL[i]}"
    fi
  done
  echo ""
  echo "Triage report indicates **$failed_count finding(s)** to address before the next release."
  exit 1
fi

cat <<EOF
## Methodology

This triage runs the same shape that surfaced F1–H1 across the v0.1.12–v0.1.15
arc: install the published wheel from PyPI in a fresh venv, run sanity checks,
invoke \`verify-release.sh\` against PyPI + ghcr, inspect container manifest
+ supply-chain artifacts, run \`check-docs.py\` against tagged source. Every
check is deterministic — no LLM call, no per-release cost beyond CI minutes.

Release **$TAG ships clean.**
EOF
exit 0
