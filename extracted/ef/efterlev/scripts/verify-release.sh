#!/usr/bin/env bash
# verify-release.sh — end-to-end cryptographic verification of an Efterlev release.
#
# Checks:
#   1. PyPI wheel + sdist are signed by the expected GitHub Actions workflow
#      via Sigstore. PyPI exposes Trusted-Publishing attestations under PEP 740
#      at `/integrity/{project}/{version}/{filename}/provenance` — NOT the old
#      `.sigstore` sidecar path. Pre-v0.1.12 versions of this script checked
#      the sidecar location and reported a false "no .sigstore present" failure
#      against signed releases (F1 from v0.1.11 triage).
#   2. Container images on ghcr.io are signed by the expected workflow via
#      cosign keyless OIDC. Pre-v0.1.12 the script required `docker buildx` for
#      digest resolution; cosign already resolves tag→digest internally, so the
#      explicit lookup was an unnecessary dependency.
#   3. SLSA build provenance is attached to each container image as a cosign-
#      verifiable in-toto attestation. Wired by `actions/attest-build-provenance`
#      in `release-container.yml` since v0.1.13. v0.1.12 added the workflow
#      step but missed the `attestations: write` permission, so the step
#      failed at runtime and v0.1.12's container has no SLSA attestation.
#      v0.1.10 + v0.1.11 have buildx-emitted provenance (verifiable via
#      `docker buildx imagetools inspect --format '{{ json .Provenance }}'`)
#      but no cosign attestation, so this script fails the SLSA check on
#      those tags by design.
#
# Usage:
#   scripts/verify-release.sh v0.1.42
#
# Exit codes:
#   0 — all checks passed
#   1 — one or more checks failed
#   2 — usage error or missing tools

set -euo pipefail

# ---------- argument parsing ----------

if [ $# -ne 1 ]; then
  echo "Usage: $0 <version>" >&2
  echo "Example: $0 v0.1.42" >&2
  exit 2
fi

VERSION="${1#v}"
TAG="v${VERSION}"
EXPECTED_REPO="efterlev/efterlev"
OIDC_ISSUER="https://token.actions.githubusercontent.com"

# ---------- tool-availability checks ----------

missing=0
need() {
  command -v "$1" >/dev/null 2>&1 || { echo "  missing: $1" >&2; missing=1; }
}
echo "Checking prerequisites..."
need curl
need python3
need cosign

if ! python3 -c "import sigstore" >/dev/null 2>&1; then
  echo "  missing: sigstore Python package" >&2
  missing=1
fi

if [ "$missing" -ne 0 ]; then
  echo
  echo "Install missing tools:" >&2
  echo "  cosign:   https://docs.sigstore.dev/system_config/installation" >&2
  echo "  sigstore: python3 -m pip install sigstore" >&2
  exit 2
fi
echo "  all tools available"
echo

# ---------- shared state ----------

WORKDIR="$(mktemp -d)"
trap 'rm -rf "$WORKDIR"' EXIT

pass=0
fail=0

pass_line() { printf "  \033[32m✓\033[0m %s\n" "$1"; pass=$((pass + 1)); }
fail_line() { printf "  \033[31m✗\033[0m %s\n" "$1"; fail=$((fail + 1)); }
info_line() { printf "    %s\n" "$1"; }

# ---------- check 1: PyPI wheel + sdist via PEP 740 ----------

echo "[1/3] PyPI artifacts — Sigstore signatures via PEP 740 Trusted Publishing"

# Query PyPI for the artifact filenames + URLs at this version.
pypi_json="$WORKDIR/pypi.json"
if ! curl -sfL -o "$pypi_json" "https://pypi.org/pypi/efterlev/${VERSION}/json"; then
  fail_line "PyPI version $VERSION not found"
else
  filenames=$(python3 -c "
import json
d = json.load(open('$pypi_json'))
for f in d['urls']:
    print(f['filename'] + '\t' + f['url'])
")
  while IFS=$'\t' read -r name url; do
    [ -z "$name" ] && continue
    curl -sfL -o "$WORKDIR/$name" "$url"

    # PEP 740: the attestation set lives at /integrity/{project}/{version}/{filename}/provenance.
    # The response is a JSON with `attestation_bundles[].attestations[]` where each
    # attestation carries an `envelope` + `verification_material` — i.e. a Sigstore
    # bundle by another name. Repack as a Sigstore v0.3 bundle and hand to sigstore-python.
    integrity_url="https://pypi.org/integrity/efterlev/${VERSION}/${name}/provenance"
    integrity_json="$WORKDIR/${name}.integrity.json"
    if ! curl -sfL -o "$integrity_json" "$integrity_url"; then
      fail_line "$name: PEP 740 attestation set not found at $integrity_url"
      continue
    fi

    bundle_path="$WORKDIR/${name}.sigstore.json"
    if ! python3 - "$integrity_json" "$bundle_path" <<'PY'
import json, sys
src, dst = sys.argv[1], sys.argv[2]
with open(src) as f:
    body = json.load(f)
bundles = body.get("attestation_bundles") or []
if not bundles or not bundles[0].get("attestations"):
    print("no attestations in PEP 740 response", file=sys.stderr)
    sys.exit(1)
att = bundles[0]["attestations"][0]
# PEP 740 → Sigstore v0.3 bundle reshape:
#   - certificate (string) → {"rawBytes": <string>}
#   - transparency_entries → tlogEntries (PEP 740 uses snake_case)
#   - envelope.{statement,signature} → DSSE {payload, payloadType, signatures[0].sig}
# Payload type for Trusted Publishing attestations is in-toto v1.
vm = att["verification_material"]
sigstore_bundle = {
    "mediaType": "application/vnd.dev.sigstore.bundle.v0.3+json",
    "verificationMaterial": {
        "certificate": {"rawBytes": vm["certificate"]},
        "tlogEntries": vm["transparency_entries"],
    },
    "dsseEnvelope": {
        "payload": att["envelope"]["statement"],
        "payloadType": "application/vnd.in-toto+json",
        "signatures": [{"sig": att["envelope"]["signature"]}],
    },
}
with open(dst, "w") as f:
    json.dump(sigstore_bundle, f)
PY
    then
      fail_line "$name: failed to repack PEP 740 attestation into Sigstore bundle"
      continue
    fi

    if python3 -m sigstore verify identity \
        --bundle "$bundle_path" \
        --cert-identity "https://github.com/${EXPECTED_REPO}/.github/workflows/release-pypi.yml@refs/tags/${TAG}" \
        --cert-oidc-issuer "$OIDC_ISSUER" \
        "$WORKDIR/$name" >/dev/null 2>&1; then
      pass_line "$name: Sigstore signature valid (PEP 740)"
    else
      fail_line "$name: PEP 740 attestation present but signature failed verification"
    fi
  done <<< "$filenames"
fi
echo

# ---------- check 2: container signature via cosign ----------

echo "[2/3] Container image — cosign keyless-OIDC signature"

for registry in ghcr.io/efterlev/efterlev; do
  image="${registry}:${TAG}"
  # cosign verify resolves the tag→digest internally and binds the signature
  # to the underlying digest. No need for `docker buildx imagetools inspect`
  # or `docker manifest inspect` here — cosign returns a clear error if the
  # image isn't pullable.
  #
  # Retry-and-wait for ghcr propagation (v0.1.101): when this script runs
  # in CI right after a release tag fires, the cosign sig + image manifest
  # may not yet be visible at ghcr.io — we'd race the release-container.yml
  # workflow's push. Hit ~1 in 5 releases (v0.1.87, v0.1.99 caught this).
  # The smoke matrix's `docker pull` retry loop handles the same class of
  # propagation race; mirror that shape here. 10 attempts × 30s = 5min.
  cosign_ok=0
  for attempt in $(seq 1 10); do
    if cosign verify "$image" \
        --certificate-identity-regexp "^https://github\.com/${EXPECTED_REPO}/" \
        --certificate-oidc-issuer "$OIDC_ISSUER" \
        >"$WORKDIR/cosign.json" 2>/dev/null; then
      cosign_ok=1
      break
    fi
    if [ "$attempt" -lt 10 ]; then
      info_line "ghcr.io not yet serving $image (attempt $attempt/10); waiting 30s..."
      sleep 30
    fi
  done
  if [ "$cosign_ok" = "1" ]; then
    digest=$(python3 -c "
import json
d = json.load(open('$WORKDIR/cosign.json'))
print(d[0]['critical']['image']['docker-manifest-digest'])
" 2>/dev/null || echo "(unknown)")
    pass_line "$image: cosign signature valid"
    info_line "digest: $digest"
  else
    fail_line "$image: cosign verification failed after 5min retry (image not pullable, or signature missing/invalid)"
  fi
done
echo

# ---------- check 3: SLSA provenance via cosign attestation ----------

echo "[3/3] SLSA build provenance — cosign-verifiable in-toto attestation"

for registry in ghcr.io/efterlev/efterlev; do
  image="${registry}:${TAG}"

  # `slsaprovenance` matches SLSA v0.2 (buildx-emitted, in the OCI image
  # manifest, not cosign-verifiable). `slsaprovenance1` matches SLSA v1,
  # which is what `actions/attest-build-provenance` emits as a separate
  # cosign attestation. Until v0.1.13 the script used the v0.2 alias and
  # therefore failed against v0.1.13's correctly-attached v1 attestation.
  #
  # Same retry-and-wait shape as check [2/3] — the SLSA attestation
  # propagates separately from the cosign sig and may also race a freshly-
  # released tag. 10 attempts × 30s = 5min.
  slsa_ok=0
  for attempt in $(seq 1 10); do
    if cosign verify-attestation --type slsaprovenance1 \
        "$image" \
        --certificate-identity-regexp "^https://github\.com/${EXPECTED_REPO}/" \
        --certificate-oidc-issuer "$OIDC_ISSUER" \
        >/dev/null 2>&1; then
      slsa_ok=1
      break
    fi
    if [ "$attempt" -lt 10 ]; then
      info_line "SLSA attestation not yet served for $image (attempt $attempt/10); waiting 30s..."
      sleep 30
    fi
  done
  if [ "$slsa_ok" = "1" ]; then
    pass_line "$image: SLSA build provenance present and valid"
  else
    fail_line "$image: SLSA cosign-verifiable attestation missing or invalid (after 5min retry)"
    info_line "Pre-v0.1.13 releases either attached buildx provenance to the OCI"
    info_line "image manifest only (v0.1.10 + v0.1.11) or had the attest-build-"
    info_line "provenance step misconfigured (v0.1.12: missing attestations: write)."
    info_line "Cosign-verifiable SLSA attestations land via release-container.yml from v0.1.13."
  fi
done
echo

# ---------- summary ----------

echo "---"
echo "Verification summary for efterlev $TAG"
echo "  passed: $pass"
echo "  failed: $fail"

if [ "$fail" -gt 0 ]; then
  echo
  echo "Release $TAG FAILED verification. Do not install."
  exit 1
fi

echo
echo "Release $TAG is cryptographically verified."
exit 0
