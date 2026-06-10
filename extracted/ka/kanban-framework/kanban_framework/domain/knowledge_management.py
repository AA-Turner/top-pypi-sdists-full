"""Management and analysis methods for knowledge DB.

Extracted from knowledge.py — functions receive KnowledgeManager instance
for access to _conn, _fs, _row_to_dict, and other internal state.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone, timedelta


def record_usage(km, entry_id, task_id):
    now = datetime.now(timezone.utc).isoformat()
    km._conn.execute(
        "UPDATE entries SET referenced_count=referenced_count+1,"
        " last_referenced_at=?, last_referenced_by=?, stale_at=NULL,"
        " status='active' WHERE id=?",
        (now, task_id, entry_id),
    )
    km._conn.execute(
        "INSERT INTO usage_log(entry_id, task_id, timestamp) VALUES(?,?,?)",
        (entry_id, task_id, now),
    )
    km._conn.commit()


def mark_stale_entries(km, threshold_days=None):
    from kanban_framework.domain.knowledge_lazy import STALE_DAYS

    days = threshold_days if threshold_days is not None else STALE_DAYS
    threshold = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
    rows = km._conn.execute(
        """SELECT id FROM entries WHERE status='active'
           AND COALESCE(last_referenced_at, created_at) < ?""",
        (threshold,),
    ).fetchall()
    stale_ids = [r[0] for r in rows]
    if stale_ids:
        now = datetime.now(timezone.utc).isoformat()
        placeholders = ",".join("?" * len(stale_ids))
        km._conn.execute(
            f"UPDATE entries SET status='stale', stale_at=? WHERE id IN ({placeholders})",
            [now] + stale_ids,
        )
        km._conn.commit()
    return stale_ids


def get_domains(km):
    from kanban_framework.domain.knowledge_lazy import DEFAULT_DOMAINS

    try:
        rows = km._conn.execute("SELECT name, label, keywords FROM domains").fetchall()
    except Exception:
        return {"domains": DEFAULT_DOMAINS}
    domains = {}
    for r in rows:
        domains[r[0]] = {"label": r[1], "keywords": json.loads(r[2])}
    return {"domains": domains or DEFAULT_DOMAINS}


def match_domain(km, text):
    from kanban_framework.domain.knowledge_lazy import DEFAULT_DOMAINS

    domains = km.get_domains()
    text_lower = text.lower()
    scores = {}
    for name, info in domains.get("domains", DEFAULT_DOMAINS).items():
        for kw in info.get("keywords", []):
            if kw.lower() in text_lower:
                scores[name] = scores.get(name, 0) + 1
    return sorted(scores, key=scores.get, reverse=True)


def find_similar_pitfalls(km, tags, min_tag_overlap=2):
    rows = km._conn.execute(
        "SELECT * FROM entries WHERE category='踩坑' AND status='active'"
    ).fetchall()
    tags_set = set(tags)
    results = []
    for r in rows:
        entry = km._row_to_dict(r)
        overlap = len(tags_set & set(entry.get("tags", [])))
        if overlap >= min_tag_overlap:
            results.append({**entry, "tag_overlap": overlap})
    results.sort(key=lambda x: x["tag_overlap"], reverse=True)
    return results


def find_conflicting_solutions(km, task_id=""):
    rows = km._conn.execute(
        "SELECT * FROM entries WHERE category!='踩坑' AND status='active'"
    ).fetchall()
    entries = [km._row_to_dict(r) for r in rows]
    by_domain = {}
    for e in entries:
        by_domain.setdefault(e["domain"], []).append(e)
    conflicts = []
    for domain, ents in by_domain.items():
        n = len(ents)
        for i in range(n):
            for j in range(i + 1, n):
                a, b = ents[i], ents[j]
                tags_a = set(a.get("tags", []))
                tags_b = set(b.get("tags", []))
                overlap = len(tags_a & tags_b)
                if overlap < 2:
                    continue
                if a.get("category") != "架构" and b.get("category") != "架构":
                    continue
                conflicts.append({
                    "entry_a": a["id"], "entry_b": b["id"],
                    "title_a": a["title"], "title_b": b["title"],
                    "domain": domain,
                    "shared_tags": sorted(tags_a & tags_b),
                    "tag_overlap": overlap,
                    "content_a": a["content"][:200],
                    "content_b": b["content"][:200],
                })
    return conflicts


def get_knowledge_gap_report(km):
    rows = km._conn.execute("SELECT domain, category FROM entries WHERE status='active'").fetchall()
    domain_counts = {}
    domain_pitfalls = {}
    for r in rows:
        d, c = r[0], r[1]
        domain_counts[d] = domain_counts.get(d, 0) + 1
        if c == "踩坑":
            domain_pitfalls[d] = domain_pitfalls.get(d, 0) + 1
    gaps = {}
    for d, pitfall_count in domain_pitfalls.items():
        if domain_counts.get(d, 1) < pitfall_count * 2:
            gaps[d] = {"total_entries": domain_counts.get(d, 0), "pitfalls": pitfall_count}
    return gaps


def find_semantic_duplicates(km, threshold=0.85):
    """Find semantically similar entries using embedding cosine similarity."""
    from kanban_framework.domain.knowledge_lazy import (
        _embed, _unpack_embedding, _cosine_similarity,
    )
    rows = km._conn.execute(
        "SELECT id, title, domain, content, embedding FROM entries WHERE status='active'"
    ).fetchall()
    if len(rows) < 2:
        return []
    entries = []
    for r in rows:
        eid, title, domain, content, emb_blob = r[0], r[1], r[2], r[3], r[4]
        if emb_blob:
            vec = _unpack_embedding(emb_blob)
        else:
            vec_raw = _embed(f"{title} {content[:200]}")
            if vec_raw is None:
                continue
            vec = _unpack_embedding(vec_raw)
            km._conn.execute("UPDATE entries SET embedding=? WHERE id=?", (vec_raw, eid))
            km._conn.commit()
        entries.append({"id": eid, "title": title, "domain": domain, "vec": vec})
    # Union-find for grouping similar entries
    n = len(entries)
    parent = list(range(n))
    def _find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    pair_scores: dict[tuple, float] = {}
    for i in range(n):
        for j in range(i + 1, n):
            sim = _cosine_similarity(entries[i]["vec"], entries[j]["vec"])
            if sim >= threshold:
                pair_scores[(i, j)] = round(sim, 4)
                ri, rj = _find(i), _find(j)
                if ri != rj:
                    parent[ri] = rj
    if not pair_scores:
        return []
    groups: dict[int, list] = {}
    for idx in range(n):
        root = _find(idx)
        groups.setdefault(root, []).append(idx)
    result = []
    gid = 1
    for members in groups.values():
        if len(members) < 2:
            continue
        group_entries = [{"id": entries[m]["id"], "title": entries[m]["title"],
                          "domain": entries[m]["domain"]} for m in members]
        best_sim = max(pair_scores.get((a, b), 0.0) for a in members for b in members if a < b)
        result.append({
            "group_id": gid, "entries": group_entries,
            "max_similarity": best_sim,
            "reason": f"语义相似度 {best_sim} >= {threshold}",
        })
        gid += 1
    result.sort(key=lambda g: g["max_similarity"], reverse=True)
    return result


def scan_stale_candidates(km, threshold_days=None):
    """List stale candidates without marking them, for human review.

    Returns entries that would be marked stale, with days_since_ref info.
    """
    from kanban_framework.domain.knowledge_lazy import STALE_DAYS

    days = threshold_days if threshold_days is not None else STALE_DAYS
    threshold = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
    rows = km._conn.execute(
        """SELECT id, title, domain, referenced_count,
                  last_referenced_at, created_at, stale_at
           FROM entries WHERE status='active'
           AND COALESCE(last_referenced_at, created_at) < ?""",
        (threshold,),
    ).fetchall()

    now = datetime.now(timezone.utc).replace(tzinfo=None)
    candidates = []
    for r in rows:
        eid, title, domain, ref_count, last_ref, created, stale_at = (
            r[0], r[1], r[2], r[3], r[4], r[5], r[6])
        ref_time = last_ref or created
        if ref_time:
            dt = datetime.fromisoformat(ref_time)
            if dt.tzinfo is not None:
                dt = dt.replace(tzinfo=None)
            days = (now - dt).days
        else:
            days = STALE_DAYS + 1
        candidates.append({
            "id": eid, "title": title, "domain": domain,
            "referenced_count": ref_count,
            "last_referenced_at": last_ref,
            "created_at": created,
            "days_since_reference": days,
        })
    candidates.sort(key=lambda c: c["days_since_reference"], reverse=True)
    return {"stale_days_threshold": days, "candidates": candidates}


def cleanup_zombies(km, min_age_days=60):
    """Remove zombie entries (never referenced + older than threshold).

    Returns list of deleted entry IDs. Called during archive to keep knowledge
    base healthy. min_age_days defaults to 60 to avoid deleting fresh entries.
    """
    threshold = (datetime.now(timezone.utc) - timedelta(days=min_age_days)).isoformat()
    rows = km._conn.execute(
        """SELECT id FROM entries WHERE status='active'
           AND (referenced_count IS NULL OR referenced_count=0)
           AND created_at < ?""",
        (threshold,),
    ).fetchall()
    zombie_ids = [r[0] for r in rows]
    if not zombie_ids:
        return []
    # Delete usage_log first (no triggers), then entries (FTS triggers handle sync).
    # Do NOT manually delete from entries_fts — FTS5 external content triggers
    # (entries_ad) fire on DELETE FROM entries and sync automatically.
    placeholders = ",".join("?" * len(zombie_ids))
    km._conn.execute(f"DELETE FROM usage_log WHERE entry_id IN ({placeholders})", zombie_ids)
    km._conn.execute(f"DELETE FROM entries WHERE id IN ({placeholders})", zombie_ids)
    km._conn.commit()
    return zombie_ids


def vacuum_database(km):
    """Optimize SQLite storage: VACUUM + rebuild FTS5 index."""
    results = {}
    try:
        before = km._conn.execute("SELECT page_count * page_size FROM pragma_page_count(), pragma_page_size()").fetchone()
    except Exception:
        before = None
    results["page_count_before"] = before

    km._conn.execute("INSERT INTO entries_fts(entries_fts) VALUES('rebuild')")
    km._conn.commit()
    results["fts_rebuilt"] = True

    km._conn.execute("VACUUM")
    km._conn.commit()
    results["vacuumed"] = True

    return results


def migrate_legacy_log(km):
    """Migrate old knowledge-log.md files to SQLite entries."""
    import re
    log_files = []
    root_log = km._fs.kanban_dir / "knowledge-log.md"
    if km._fs.file_exists(root_log):
        log_files.append((root_log, None))
    for task_dir in sorted(km._fs.kanban_dir.glob("tasks/TASK-*")):
        if task_dir.is_dir():
            task_log = task_dir / "knowledge-log.md"
            if km._fs.file_exists(task_log):
                log_files.append((task_log, task_dir.name))

    pattern = re.compile(r'###\s+(\S+):\s*(.+?)\n\s*\n(.*?)(?=\n###|\Z)', re.DOTALL)
    count = 0
    for log_path, task_id in log_files:
        text = log_path.read_text(encoding="utf-8")
        for m in pattern.finditer(text):
            category = m.group(1)
            title = m.group(2).strip()
            content = m.group(3).strip()
            source = {"migrated_from": str(log_path.relative_to(km._fs.kanban_dir))}
            if task_id:
                source["task_id"] = task_id
            km.add_entry(
                domain=km.match_domain(f"{title} {content}")[0] if km.match_domain(title) else "infra",
                category=category, title=title, content=content,
                tags=[category], source=source,
            )
            count += 1
        log_path.rename(log_path.with_suffix(".md.bak"))
    return count
