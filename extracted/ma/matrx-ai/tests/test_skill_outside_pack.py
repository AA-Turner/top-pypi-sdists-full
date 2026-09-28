"""Outside skill packs: faithful, attributed, complete, pack-owned, idempotent.

Witnesses for ``matrx_ai.skills.packs`` (Arman, 2026-09-27: put an outside
expert's skills into our library). Each test pins one promise:

* renamed ids + every cross-reference that names them, never the judgment text;
* a provenance banner on every body, and a LOUD not-runnable notice only where
  the body references the pack's own tooling;
* support files carried verbatim (nothing silently dropped) and an unaccounted
  upstream file refusing the whole run;
* the pinned commit is enforced;
* a pack run writes only its own rows, a repo-mirror ingest never touches them,
  and a second run over the same commit is all ``unchanged``.
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from types import SimpleNamespace
from uuid import uuid4

import pytest

from matrx_ai.skills.ingest import ingest_filesystem
from matrx_ai.skills.packs import (
    PACK_MANIFESTS_DIR,
    PackError,
    ingest_outside_pack,
    load_manifest,
    walk_pack,
)

DETECTOR = """---
name: brandx-detector
description: "Find stories. Hands off to brandx-triage."
when_to_use: "Run on a schedule, after setup, when news breaks"
---

# Brandx Detector

You are **brandx-detector**. Load `skills/brandx-triage/SKILL.md` next.
This skill inherits the ethical floor in `skills/ETHICS.md`.
Run `brandx detector run --profile p.json` and read `~/.brandx/monitors/x/profile.json`.
Details in `references/engine.md`.
"""

TRIAGE = """---
name: brandx-triage
description: Route fresh signals.
---

# Brandx Triage

Judgment: never drop a fresh big story. Called by brandx-detector.
"""

ETHICS = "# ETHICS\n\nDo not fabricate. Every brandx-detector run obeys this.\n"


def _manifest_yaml(commit: str) -> str:
    return f"""
pack_id: test-pack
title: "Test PR skills"
imported_on: "2026-09-27"
visibility: public
source:
  repo_url: https://example.com/upstream
  commit: {commit}
  license: MIT
  authors: ["Ada Author", "Bo Author"]
  skills_dir: skills
category:
  slug: test-pack-category
  name: "Test Pack"
renames:
  brandx-detector: {{skill_id: story-detector, label: Story Detector}}
  brandx-triage: {{skill_id: story-triage, label: Story Triage}}
documents:
  - path: ETHICS.md
    skill_id: test-ethics
    label: Test Ethics
    description: The ethical floor.
path_rewrites:
  "skills/ETHICS.md": "test-ethics"
ignore_files: [".gitkeep"]
tooling_notices:
  - label: "the pack CLI"
    pattern: '\\bbrandx (?:detector|monitor)\\b'
  - label: "local pack files"
    pattern: '~/\\.brandx'
tooling_note: "Being rebuilt natively; not runnable here."
"""


def _git(root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(root), *args], capture_output=True, text=True, check=True
    ).stdout.strip()


@pytest.fixture()
def pack(tmp_path: Path):
    src = tmp_path / "upstream"
    skills = src / "skills"
    (skills / "brandx-detector" / "references").mkdir(parents=True)
    (skills / "brandx-triage").mkdir(parents=True)
    (skills / "brandx-detector" / "SKILL.md").write_text(DETECTOR)
    (skills / "brandx-detector" / "references" / "engine.md").write_text(
        "# Engine\n\nThe `brandx-detector` skill owns judgment.\n```sh\nbrandx detector run\n```\n"
    )
    (skills / "brandx-detector" / "clip.mjs").write_text("export const x = 1;\n")
    (skills / "brandx-triage" / "SKILL.md").write_text(TRIAGE)
    (skills / "ETHICS.md").write_text(ETHICS)
    (skills / ".gitkeep").write_text("")
    _git(src, "init", "-q")
    _git(src, "-c", "user.email=t@t", "-c", "user.name=t", "add", "-A")
    _git(src, "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "init")
    head = _git(src, "rev-parse", "HEAD")
    manifest = tmp_path / "manifest.yaml"
    manifest.write_text(_manifest_yaml(head[:7]))
    return SimpleNamespace(src=src, skills=skills, manifest=manifest, head=head)


def _by_id(walk):
    return {s.skill_id: s for s in walk.skills}


def test_renames_rewrite_references_and_keep_judgment(pack):
    walk = walk_pack(load_manifest(pack.manifest), pack.src)
    assert walk.errors == []
    skills = _by_id(walk)
    assert set(skills) == {"story-detector", "story-triage", "test-ethics"}

    det = skills["story-detector"]
    assert det.label == "Story Detector"
    assert "\n# Story Detector\n" in det.body
    assert "You are **story-detector**." in det.body
    assert "Load `story-triage` next." in det.body
    assert "ethical floor in `test-ethics`" in det.body
    assert det.description == "Find stories. Hands off to story-triage."
    # when_to_use stays ONE trigger — never comma-chopped into fragments.
    assert det.trigger_patterns == ["Run on a schedule, after setup, when news breaks"]
    # The old id survives only in the provenance banner, never as a live name.
    after_banner = det.body.split("\n# Story Detector\n", 1)[1]
    assert "brandx-detector" not in after_banner.split("## Imported supporting files")[0]

    triage = skills["story-triage"]
    assert "Judgment: never drop a fresh big story. Called by story-detector." in triage.body
    assert "brandx-detector" not in skills["test-ethics"].body.split("\n# ETHICS\n", 1)[1]


def test_banner_provenance_everywhere_and_loud_tooling_only_where_referenced(pack):
    walk = walk_pack(load_manifest(pack.manifest), pack.src)
    skills = _by_id(walk)
    for s in skills.values():
        assert s.body.startswith("> **Imported outside")
        assert "Ada Author and Bo Author" in s.body
        assert "https://example.com/upstream" in s.body
        assert "MIT License" in s.body
        assert s.visibility == "public"
        assert s.ingested_from == "outside_pack"
        cfg = s.extra_config
        assert cfg["pack_id"] == "test-pack"
        assert cfg["source_commit_full"] == pack.head
        assert cfg["source_authors"] == ["Ada Author", "Bo Author"]
        assert cfg["source_license"] == "MIT"
    det = skills["story-detector"]
    assert "Warning — not yet runnable here" in det.body
    assert "the pack CLI" in det.body and "local pack files" in det.body
    # The tooling instructions are the rebuild spec: kept, never deleted.
    assert "brandx detector run --profile p.json" in det.body
    assert "not yet runnable" not in skills["story-triage"].body


def test_support_files_carried_verbatim(pack):
    walk = walk_pack(load_manifest(pack.manifest), pack.src)
    det = _by_id(walk)["story-detector"]
    assert "## Imported supporting files" in det.body
    assert "### `references/engine.md`" in det.body
    assert "The `story-detector` skill owns judgment." in det.body  # md prose refs resolve
    assert "### `clip.mjs`" in det.body and "export const x = 1;" in det.body
    # A nested ``` fence inside a carried file cannot break out of its block.
    assert "````markdown" in det.body
    assert sorted(walk.carried_support_files) == [
        "story-detector: clip.mjs",
        "story-detector: references/engine.md",
    ]


def test_unaccounted_upstream_file_is_an_error_not_a_silent_drop(pack):
    # A file the UPSTREAM commit carries that the manifest never declared.
    (pack.skills / "NEW-DOCTRINE.md").write_text("# New\n")
    _git(pack.src, "-c", "user.email=t@t", "-c", "user.name=t", "add", "-A")
    _git(
        pack.src,
        "-c",
        "user.email=t@t",
        "-c",
        "user.name=t",
        "commit",
        "-qm",
        "upstream adds a doc",
    )
    manifest = load_manifest(pack.manifest)
    manifest.commit = _git(pack.src, "rev-parse", "HEAD")[:7]
    walk = walk_pack(manifest, pack.src)
    assert any("NEW-DOCTRINE.md" in e for e in walk.errors)


def test_edited_skill_at_the_pinned_commit_is_refused(pack):
    # HEAD still matches the manifest, but the body on disk is not the experts'.
    path = pack.skills / "brandx-triage" / "SKILL.md"
    path.write_text(path.read_text().replace("never drop", "always drop"))
    with pytest.raises(PackError, match="local changes"):
        walk_pack(load_manifest(pack.manifest), pack.src)


def test_untracked_file_in_a_skill_folder_is_refused(pack):
    (pack.skills / "brandx-triage" / "notes.md").write_text("not upstream\n")
    with pytest.raises(PackError, match="local changes"):
        walk_pack(load_manifest(pack.manifest), pack.src)


def test_changes_outside_the_pack_paths_do_not_block(pack):
    (pack.src / "README.local").write_text("scratch\n")
    assert walk_pack(load_manifest(pack.manifest), pack.src).errors == []


def test_wrong_commit_refuses(pack, tmp_path):
    (pack.skills / "brandx-triage" / "SKILL.md").write_text(TRIAGE + "\nmore\n")
    _git(pack.src, "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qam", "drift")
    with pytest.raises(PackError, match="pins"):
        walk_pack(load_manifest(pack.manifest), pack.src)


def test_shipped_manifests_load():
    manifests = sorted(PACK_MANIFESTS_DIR.glob("*.yaml"))
    assert manifests
    for path in manifests:
        m = load_manifest(path)
        for spec in m.renames.values():
            # The upstream product name is trademarked: never a library name.
            assert (
                "newsjack" not in spec["skill_id"]
                and "newsjack" not in spec.get("label", "").lower()
            )
        for doc in m.documents:
            assert "newsjack" not in doc.skill_id and "newsjack" not in doc.label.lower()


# ---------------------------------------------------------------------------
# DB leg: ownership + idempotency against an in-memory table
# ---------------------------------------------------------------------------


class _Row(SimpleNamespace):
    pass


class _Defs:
    def __init__(self, rows=None):
        self.rows: list[_Row] = list(rows or [])
        self.creates = 0
        self.updates = 0

    async def filter_items(self, **_kw):
        return list(self.rows)

    async def create_item(self, **kw):
        self.creates += 1
        row = _Row(id=uuid4(), **kw)
        self.rows.append(row)
        return row

    async def update_item(self, row_id, **kw):
        self.updates += 1
        for r in self.rows:
            if str(r.id) == str(row_id):
                for k, v in kw.items():
                    setattr(r, k, v)
                return r
        raise AssertionError("update of unknown row")


class _Cats:
    def __init__(self):
        self.rows: list[_Row] = []

    async def filter_items(self, **_kw):
        return list(self.rows)

    async def create_item(self, **kw):
        row = _Row(id=uuid4(), **kw)
        self.rows.append(row)
        return row


def _patch(monkeypatch, defs, cats):
    import matrx_ai.db._registry as registry

    monkeypatch.setattr(
        registry,
        "get_instance",
        lambda name: {"skl_definitions_manager": defs, "skl_categories_manager": cats}[name],
    )


@pytest.mark.asyncio
async def test_pack_ingest_is_idempotent_public_system_and_categorised(pack, monkeypatch):
    from matrx_orm.session.fallback import SYSTEM_ORGANIZATION_ID

    defs, cats = _Defs(), _Cats()
    _patch(monkeypatch, defs, cats)
    admin = str(uuid4())

    first = await ingest_outside_pack(pack.manifest, pack.src, admin_user_id=admin)
    assert first["errors"] == []
    assert first["created"] == 3 and first["category"]["status"] == "created"
    cat_id = cats.rows[0].id
    assert cats.rows[0].metadata["is_active"] is True
    for row in defs.rows:
        assert row.organization_id == SYSTEM_ORGANIZATION_ID
        assert row.is_system is True and row.visibility == "public"
        assert str(row.category_id) == str(cat_id)
        assert row.config["ingested_from"] == "outside_pack"

    second = await ingest_outside_pack(pack.manifest, pack.src, admin_user_id=admin)
    assert second["errors"] == []
    assert (second["created"], second["updated"], second["unchanged"]) == (0, 0, 3)
    assert second["category"]["status"] == "exists"
    assert defs.creates == 3 and defs.updates == 0


@pytest.mark.asyncio
async def test_pack_and_repo_mirror_never_write_each_others_rows(pack, monkeypatch, tmp_path):
    # A repo mirror already owns `story-triage`; the pack must not overwrite it.
    mirror_row = _Row(
        id=uuid4(),
        skill_id="story-triage",
        body="repo body",
        is_active=True,
        visibility="internal",
        config={
            "ingested_from": "filesystem",
            "source_path": "/repo/.claude/skills/story-triage/SKILL.md",
        },
    )
    defs, cats = _Defs([mirror_row]), _Cats()
    _patch(monkeypatch, defs, cats)
    report = await ingest_outside_pack(pack.manifest, pack.src, admin_user_id=str(uuid4()))
    assert report["skipped_foreign"] == 1
    assert mirror_row.body == "repo body"

    # And a repo-mirror ingest that finds a same-named pack row leaves it alone.
    pack_row = next(r for r in defs.rows if r.skill_id == "story-detector")
    before = pack_row.body
    repo = tmp_path / "repo" / ".claude" / "skills" / "story-detector"
    repo.mkdir(parents=True)
    (repo / "SKILL.md").write_text("---\nname: story-detector\ndescription: d\n---\n# x\n")
    fs_report = await ingest_filesystem([repo.parent], admin_user_id=str(uuid4()))
    assert fs_report["skipped_foreign"] == 1
    assert pack_row.body == before


# ---------------------------------------------------------------------------
# Documents outside the skills dir, skipped skills, tool map, product name
# ---------------------------------------------------------------------------

PLAYBOOK = """---
title: "One page per intent"
description: "A keyword list is not a strategy."
---

## Method

Group by intent. Check with `get_serp_results` and `get_ranked_keywords`.
![chart](/library/chart.png)
"""


def _site_manifest_yaml(commit: str, *, extra: str = "") -> str:
    return f"""
pack_id: site-pack
title: "Site skills"
imported_on: "2026-09-27"
visibility: public
source:
  repo_url: https://example.com/site
  commit: {commit}
  license: MIT
  authors: ["Solo Author"]
  skills_dir: skills
  product_name: Brandz
category: {{slug: site-cat, name: "Site"}}
renames:
  audit: {{label: Site Audit}}
skip_skills:
  internal-tool: "their repo tooling"
document_dirs:
  - dir: web/library
    skip:
      thin.mdx: "thin"
documents:
  - repo_path: web/library/hubs.mdx
    skill_id: playbook-hubs
    label: "Playbook: Hubs"
    note: "Overlaps the Site Audit skill."
path_rewrites:
  "](/": "](https://example.com/"
edits_note: "Site-relative links now point to the source website."
tool_equivalents:
  get_serp_results: "`seo` action `collect_rank`"
  get_ranked_keywords: null
tool_equivalents_note: "They do not exist here under these names."
{extra}
"""


@pytest.fixture()
def site_pack(tmp_path: Path):
    src = tmp_path / "site"
    (src / "skills" / "audit").mkdir(parents=True)
    (src / "skills" / "internal-tool").mkdir(parents=True)
    (src / "web" / "library").mkdir(parents=True)
    (src / "skills" / "audit" / "SKILL.md").write_text(
        "---\nname: audit\ndescription: Audit a site.\n---\n\n# Brandz Audit\n\nCall `get_ranked_keywords`.\n"
    )
    (src / "skills" / "internal-tool" / "SKILL.md").write_text(
        "---\nname: internal-tool\ndescription: x\n---\n# T\n"
    )
    (src / "web" / "library" / "hubs.mdx").write_text(PLAYBOOK)
    (src / "web" / "library" / "thin.mdx").write_text("---\ntitle: Thin\n---\nthin\n")
    _git(src, "init", "-q")
    _git(src, "-c", "user.email=t@t", "-c", "user.name=t", "add", "-A")
    _git(src, "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "init")
    head = _git(src, "rev-parse", "HEAD")
    manifest = tmp_path / "site.yaml"
    manifest.write_text(_site_manifest_yaml(head[:7]))
    return SimpleNamespace(src=src, manifest=manifest, head=head, tmp=tmp_path)


def test_document_outside_skills_dir_is_imported_with_its_frontmatter(site_pack):
    walk = walk_pack(load_manifest(site_pack.manifest), site_pack.src)
    assert walk.errors == []
    skills = _by_id(walk)
    # The skipped folder is accounted for and never imported.
    assert set(skills) == {"audit", "playbook-hubs"}
    doc = skills["playbook-hubs"]
    assert doc.description == "A keyword list is not a strategy."
    assert "\n# One page per intent\n\n*A keyword list is not a strategy.*\n\n## Method" in doc.body
    assert "file `web/library/hubs.mdx`" in doc.body
    assert "](https://example.com/library/chart.png)" in doc.body
    assert "> Overlaps the Site Audit skill." in doc.body
    assert (
        "Written by an outside expert" not in doc.body
        and "written by an outside expert" in doc.body
    )
    assert doc.extra_config["source_path"] == "web/library/hubs.mdx"


def test_tool_map_banner_names_what_exists_and_what_does_not(site_pack):
    walk = walk_pack(load_manifest(site_pack.manifest), site_pack.src)
    doc = _by_id(walk)["playbook-hubs"]
    assert ">   - `get_serp_results` → `seo` action `collect_rank`" in doc.body
    assert "**No AI Matrx equivalent yet:** `get_ranked_keywords`" in doc.body
    assert doc.extra_config["source_tools_with_equivalent"] == {
        "get_serp_results": "`seo` action `collect_rank`"
    }
    assert doc.extra_config["source_tools_without_equivalent"] == ["get_ranked_keywords"]
    audit = _by_id(walk)["audit"]
    assert "Has an AI Matrx equivalent" not in audit.body
    assert audit.extra_config["source_tools_without_equivalent"] == ["get_ranked_keywords"]
    # Label-only rename: the id stays, the displayed heading drops the product name.
    assert audit.label == "Site Audit" and "\n# Site Audit\n" in audit.body


def test_unaccounted_file_in_a_document_dir_is_an_error(site_pack):
    (site_pack.src / "web" / "library" / "new.mdx").write_text("---\ntitle: New\n---\n")
    _git(site_pack.src, "-c", "user.email=t@t", "-c", "user.name=t", "add", "-A")
    _git(
        site_pack.src,
        "-c",
        "user.email=t@t",
        "-c",
        "user.name=t",
        "commit",
        "-qm",
        "upstream adds one",
    )
    manifest = load_manifest(site_pack.manifest)
    manifest.commit = _git(site_pack.src, "rev-parse", "HEAD")[:7]
    walk = walk_pack(manifest, site_pack.src)
    assert any("web/library/new.mdx" in e for e in walk.errors)


def test_edited_document_outside_skills_dir_is_refused(site_pack):
    path = site_pack.src / "web" / "library" / "hubs.mdx"
    path.write_text(path.read_text().replace("Group by intent", "Group by volume"))
    with pytest.raises(PackError, match="local changes"):
        walk_pack(load_manifest(site_pack.manifest), site_pack.src)


def test_product_name_can_never_be_a_library_name(site_pack):
    bad = site_pack.tmp / "bad.yaml"
    bad.write_text(
        _site_manifest_yaml("abc1234").replace("label: Site Audit", "label: Brandz Audit")
    )
    with pytest.raises(PackError, match="product name"):
        load_manifest(bad)
    # A skill with no manifest label keeps its own H1 — which here carries the name.
    unlabeled = site_pack.tmp / "unlabeled.yaml"
    unlabeled.write_text(
        _site_manifest_yaml(site_pack.head[:7]).replace(
            "renames:\n  audit: {label: Site Audit}\n", ""
        )
    )
    walk = walk_pack(load_manifest(unlabeled), site_pack.src)
    assert any("product name" in e for e in walk.errors)


def test_shipped_manifests_never_use_the_source_product_name():
    for path in sorted(PACK_MANIFESTS_DIR.glob("*.yaml")):
        m = load_manifest(path)  # load_manifest itself refuses a product-named id/label
        if m.product_name:
            assert all(m.product_name.lower() not in d.skill_id for d in m.documents)


NARRATIVE_ONLY = """---
title: "Narrative"
description: "Mentions the pack CLI in passing."
---

## Background

People used to run brandx detector by hand; this article is about judgment.
"""

WITH_RUN_SECTION = """---
title: "Runnable"
description: "Has a run section."
---

## Background

Nothing to run here.

## Run this with the tool

Open ~/.brandx first.

### Details

Still inside the run section: brandx detector run.

## After

brandx monitor is mentioned in passing again.

```text
Using brandx detector, check it.
```
"""


def _scoped_pack(tmp_path: Path, scope: str):
    src = tmp_path / "scoped"
    (src / "skills" / "one").mkdir(parents=True)
    (src / "docs").mkdir(parents=True)
    (src / "skills" / "one" / "SKILL.md").write_text(
        "---\nname: one\ndescription: d\n---\n# One\n\nMentioned in passing: brandx detector.\n"
    )
    (src / "docs" / "narrative.md").write_text(NARRATIVE_ONLY)
    (src / "docs" / "runnable.md").write_text(WITH_RUN_SECTION)
    _git(src, "init", "-q")
    _git(src, "-c", "user.email=t@t", "-c", "user.name=t", "add", "-A")
    _git(src, "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "init")
    head = _git(src, "rev-parse", "HEAD")
    manifest = tmp_path / "scoped.yaml"
    manifest.write_text(f"""
pack_id: scoped
title: "Scoped"
imported_on: "2026-09-27"
source: {{repo_url: https://example.com/s, commit: {head[:7]}, license: MIT, authors: ["A"], skills_dir: skills}}
category: {{slug: s, name: S}}
document_dirs: [{{dir: docs}}]
documents:
  - {{repo_path: docs/narrative.md, skill_id: doc-narrative, label: Narrative}}
  - {{repo_path: docs/runnable.md, skill_id: doc-runnable, label: Runnable}}
tooling_notices:
  - label: "the pack CLI"
    pattern: '\\bbrandx (?:detector|monitor)\\b'
  - label: "local pack files"
    pattern: '~/\\.brandx'
tooling_note: "Not here."
{scope}
""")
    return _by_id(walk_pack(load_manifest(manifest), src))


def test_document_passing_mention_is_not_flagged_but_run_steps_are(tmp_path):
    skills = _scoped_pack(
        tmp_path,
        "document_instruction_scope: {headings: '^(?:Run this|Do it with)', fenced_blocks: true}",
    )
    # A document that only NARRATES the tooling carries no not-runnable flag or warning.
    narrative = skills["doc-narrative"]
    assert narrative.extra_config["tooling_not_runnable"] == []
    assert "not yet runnable" not in narrative.body
    # One whose run section and ready-made prompt use it is flagged — counting only those parts.
    runnable = skills["doc-runnable"]
    assert runnable.extra_config["tooling_not_runnable"] == ["the pack CLI", "local pack files"]
    assert (
        "the pack CLI (2 mentions)" in runnable.body
    )  # sub-section + fenced prompt, not "## After"
    assert "Its how-to-run steps and ready-made prompts tells" not in runnable.body
    # A skill is instructions end to end: always scanned whole.
    assert skills["one"].extra_config["tooling_not_runnable"] == ["the pack CLI"]


def test_without_a_declared_scope_documents_are_scanned_whole(tmp_path):
    skills = _scoped_pack(tmp_path, "")
    assert skills["doc-narrative"].extra_config["tooling_not_runnable"] == ["the pack CLI"]
