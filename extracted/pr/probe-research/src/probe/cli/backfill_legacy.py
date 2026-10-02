"""Read-only legacy reconciliation; counts never establish delivery."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import unicodedata

from .backfill_coverage import Coverage
from .backfill_ledger import Ledger
from .backfill_manifest import validate_manifest

PAGE_SIZE = 100
MAX_REMOTE_ARTIFACTS = 20_000
MAX_VERIFY_BYTES = 2 * 1024 * 1024 * 1024


def _remote(client, project_id: str) -> list[dict]:
    result = []
    seen = set()
    pending = [("", 0)]
    requested = set()
    folders = {""}
    while pending and len(requested) < 4000:
        prefix, offset = pending.pop()
        if (prefix, offset) in requested:
            raise ValueError("artifact tree pagination repeated; coverage remains unverified")
        requested.add((prefix, offset))
        page = client.transport.get(f"/v1/projects/{project_id}/artifacts/tree",
                                    params={"prefix": prefix, "limit": PAGE_SIZE, "offset": offset})
        for row in page["files"]:
            if str(row.get("id")) in seen:
                continue
            seen.add(str(row.get("id")))
            result.append({key: row.get(key) for key in (
                "id", "name", "customer_id", "project_id", "experiment_id", "run_id",
                "content_hash", "size_bytes", "is_reference", "uri", "status")})
        if len(result) > MAX_REMOTE_ARTIFACTS:
            raise ValueError("artifact reconciliation exceeded its bounded listing; narrow the target")
        for child in page["folders"]:
            if child["path"] not in folders:
                folders.add(child["path"])
                pending.append((child["path"], 0))
        next_offset = page.get("next_offset")
        if next_offset is not None:
            if next_offset <= offset:
                raise ValueError("artifact tree offset did not advance")
            pending.append((prefix, next_offset))
        elif page.get("truncated"):
            raise ValueError("artifact tree is truncated without a continuation")
    if pending:
        raise ValueError("artifact tree exceeds the reconciliation request budget")
    return result


def reconcile(coverage: Coverage, client, folder: Path) -> dict[str, dict]:
    """Adopt only exact destination/path/hash/mode matches, preserving original IDs."""
    previous = coverage.meta("legacy", {})
    if previous.get("finished"):
        return previous.get("unresolved", {})
    legacy = Ledger.for_folder(folder)
    if not legacy.path.exists():
        coverage.put_meta("legacy", {"finished": True, "unresolved": {}})
        return {}
    state = legacy.read()
    if not state.planned:
        unresolved = {row["path"]: {"reason": "legacy plan unreadable", "ledger": str(legacy.path)}
                      for row in coverage.rows() if row["present"]}
        coverage.put_meta("legacy", {"finished": False, "unresolved": unresolved})
        return unresolved
    manifests = legacy.path.parent / f"{legacy.path.stem}-manifests"
    current = {row["path"]: row for row in coverage.rows()}
    claims: dict[str, list[tuple[str, dict | None]]] = defaultdict(list)
    for record in state.units.values():
        checked = validate_manifest(manifests / f"{record.unit.unit_id}.jsonl", record.unit.paths, root=folder)
        valid = {row["path"]: row for row in checked.rows}
        for path in record.unit.paths:
            if path in current:
                claims[path].append((record.unit.project, valid.get(path)))
    projects: dict[str, dict] = {}
    remote: dict[str, dict[str, list[dict]]] = {}
    unresolved = {}
    adopted = {row["path"]: row for row in previous.get("adopted", [])}
    verified_bytes = 0
    for path, entries in claims.items():
        row = current[path]
        if path in adopted:
            continue
        if len(entries) != 1 or entries[0][1] is None:
            unresolved[path] = {"reason": "ambiguous assignment or missing valid legacy manifest"}
            continue
        slug, manifest = entries[0]
        try:
            if slug not in projects:
                project = client.resolve_project(slug, strict=True)
                if (not project or project.get("customer_id") != coverage.scope.customer_id
                        or str(project.get("workspace_id")) != coverage.scope.workspace_id
                        or (coverage.scope.project_id and str(project["id"]) != coverage.scope.project_id)):
                    raise ValueError("legacy destination is not the selected current destination")
                projects[slug] = project
            project = projects[slug]
            project_id = str(project["id"])
            if project_id not in remote:
                by_hash = defaultdict(list)
                for item in _remote(client, project_id):
                    by_hash[item["content_hash"]].append(item)
                remote[project_id] = by_hash
            wanted_ref = manifest.get("reference", False)
            candidates = remote[project_id].get(row["observed_hash"], []) if row["observed_hash"] else []
            exact = [item for item in candidates if item["name"] == unicodedata.normalize("NFC", path)
                     and str(item["project_id"]) == project_id
                     and item["customer_id"] == coverage.scope.customer_id
                     and not item["experiment_id"] and not item["run_id"]
                     and item["status"] == "complete"
                     and item["size_bytes"] == row["size"]
                     and bool(item["is_reference"]) == wanted_ref
                     and (not wanted_ref or item["uri"] == (folder / path).resolve().as_uri())]
            if len(exact) != 1:
                unresolved[path] = {"reason": "no unique exact path/hash/destination/mode match",
                                    "candidates": [{"id": item["id"], "name": item["name"]}
                                                   for item in candidates[:10]]}
                continue
            item = exact[0]
            if not wanted_ref:
                if verified_bytes + row["size"] > MAX_VERIFY_BYTES:
                    raise ValueError("legacy byte-verification budget reached; re-run to continue")
                # Failed/corrupt downloads spend budget too. The stream itself
                # may never exceed the declared source version's byte count.
                verified_bytes += row["size"]
                temporary = coverage.directory / "legacy-download.partial"
                try:
                    downloaded = client.download_artifact_to(str(item["id"]), str(temporary), max_bytes=row["size"])
                    if downloaded["sha256"] != row["observed_hash"] or downloaded["size_bytes"] != row["size"]:
                        raise ValueError("remote artifact bytes differ from the local source")
                finally:
                    temporary.unlink(missing_ok=True)
            coverage.approve({path: project})
            coverage.remember_manifest(path, manifest)
            approved = {**row, "approved_hash": row["observed_hash"], "project_id": project_id}
            intent = coverage.intend(approved, reference=wanted_ref,
                                     uri=item["uri"] if wanted_ref else None)
            coverage.accept_receipt(intent["correlation"], {
                "correlation": intent["correlation"], "state": "delivered", "status": "complete",
                "artifact_id": str(item["id"]), "anchor": "project", "anchor_id": project_id,
                "name": intent["artifact_name"], "content_hash": row["observed_hash"], "size_bytes": row["size"],
                "is_reference": wanted_ref, "uri": item["uri"], "readable": not wanted_ref,
                "provenance": "legacy_reference_reconciliation" if wanted_ref else "legacy_download_verified",
            })
            adopted[path] = {"path": path, "artifact_id": str(item["id"])}
        except Exception as exc:
            unresolved[path] = {"reason": str(exc)[:512]}
    coverage.put_meta("legacy", {"finished": not unresolved, "unresolved": unresolved,
                                 "adopted": list(adopted.values()), "ledger": str(legacy.path)})
    return unresolved
