"""Blast Radius and Change Story analysis endpoints."""

import asyncio
import os
import subprocess
from typing import Optional

import httpx
from fastapi import APIRouter, HTTPException, Query, Request
from pydantic import BaseModel, Field

router = APIRouter(prefix="/analysis", tags=["analysis"])
ANALYSIS_TIMEOUT_SECONDS = 90


# ── Graph-based Blast Radius Helper ──


def _expand_blast_radius_with_graph(
    repo_path: str,
    ring0_symbols: list[dict],
    max_hops: int,
) -> list[dict]:
    """Expand blast radius rings using the Kuzu graph database.
    
    Queries the pre-built call graph to find dependents of changed symbols.
    This is fast because it uses the indexed graph instead of re-parsing code.
    
    Args:
        repo_path: Path to the repository
        ring0_symbols: Direct changes from AST diff
        max_hops: Maximum hops to traverse (1 = just ring 0)
        
    Returns:
        List of ring dicts with hop, label, and symbols
    """
    try:
        from ..graph.connection import configure_for_repo, get_read_connection, KUZU_AVAILABLE
        
        if not KUZU_AVAILABLE:
            # Fall back to ring 0 only if Kuzu not available
            return [{"hop": 0, "label": "Direct Changes", "symbols": ring0_symbols}]
        
        # Configure connection for this repo
        from pathlib import Path
        configure_for_repo(Path(repo_path))
        conn = get_read_connection()
        
        # Test connection
        try:
            conn.execute("RETURN 1 AS test")
        except Exception:
            # Graph not available or not initialized
            return [{"hop": 0, "label": "Direct Changes", "symbols": ring0_symbols}]
        
        # Build rings
        rings = [{"hop": 0, "label": "Direct Changes", "symbols": ring0_symbols}]
        
        if max_hops <= 0 or not ring0_symbols:
            return rings
        
        # Get qualified names of changed symbols
        changed_names = {s["qualified_name"] for s in ring0_symbols}
        all_seen = set(changed_names)  # Track all symbols we've seen across rings
        
        # Build hop-by-hop expansion
        current_ring = 0
        current_symbols = set(changed_names)
        
        hop_labels = {
            1: "Direct Dependents",
            2: "Secondary Dependents", 
            3: "Tertiary Dependents",
        }
        
        while current_ring < max_hops and current_symbols:
            next_symbols = set()
            ring_symbols = []
            
            # For each symbol in current ring, find what it calls and what calls it
            for sym_name in current_symbols:
                # Query callers (functions that call this symbol)
                # Also traverse HAS_METHOD to find class methods
                try:
                    # Find functions that CALL this symbol
                    caller_query = """
                        MATCH (caller:Function)-[:CALLS]->(callee:Function {qualified_name: $name})
                        RETURN caller.qualified_name AS qualified_name,
                               caller.file_path AS file_path,
                               caller.line_start AS line_start,
                               caller.line_end AS line_end
                        LIMIT 50
                    """
                    caller_results = conn.execute(caller_query, {"name": sym_name})
                    
                    for row in caller_results:
                        qn = row.get("qualified_name")
                        if qn and qn not in all_seen:
                            all_seen.add(qn)
                            next_symbols.add(qn)
                            ring_symbols.append({
                                "qualified_name": qn,
                                "file_path": row.get("file_path", ""),
                                "change_kind": None,
                                "symbol_kind": "function",
                                "severity": 0.5,  # Default severity for dependents
                                "line_start": row.get("line_start"),
                                "line_end": row.get("line_end"),
                                "relation": "caller",
                                "details": {"called_symbol": sym_name},
                            })
                except Exception:
                    pass
                
                # Find functions this symbol CALLS
                try:
                    callee_query = """
                        MATCH (caller:Function {qualified_name: $name})-[:CALLS]->(callee:Function)
                        RETURN callee.qualified_name AS qualified_name,
                               callee.file_path AS file_path,
                               callee.line_start AS line_start,
                               callee.line_end AS line_end
                        LIMIT 50
                    """
                    callee_results = conn.execute(callee_query, {"name": sym_name})
                    
                    for row in callee_results:
                        qn = row.get("qualified_name")
                        if qn and qn not in all_seen:
                            all_seen.add(qn)
                            next_symbols.add(qn)
                            ring_symbols.append({
                                "qualified_name": qn,
                                "file_path": row.get("file_path", ""),
                                "change_kind": None,
                                "symbol_kind": "function",
                                "severity": 0.4,  # Slightly lower for callees
                                "line_start": row.get("line_start"),
                                "line_end": row.get("line_end"),
                                "relation": "callee",
                                "details": {"called_by": sym_name},
                            })
                except Exception:
                    pass
                
                # Find class methods if this is a class
                try:
                    method_query = """
                        MATCH (c:Class {qualified_name: $name})-[:HAS_METHOD]->(m:Function)
                        RETURN m.qualified_name AS qualified_name,
                               m.file_path AS file_path,
                               m.line_start AS line_start,
                               m.line_end AS line_end
                        LIMIT 50
                    """
                    method_results = conn.execute(method_query, {"name": sym_name})
                    
                    for row in method_results:
                        qn = row.get("qualified_name")
                        if qn and qn not in all_seen:
                            all_seen.add(qn)
                            next_symbols.add(qn)
                            ring_symbols.append({
                                "qualified_name": qn,
                                "file_path": row.get("file_path", ""),
                                "change_kind": None,
                                "symbol_kind": "method",
                                "severity": 0.6,  # Higher for methods of changed class
                                "line_start": row.get("line_start"),
                                "line_end": row.get("line_end"),
                                "relation": "method",
                                "details": {"parent_class": sym_name},
                            })
                except Exception:
                    pass
            
            # Add ring if we found new symbols
            if ring_symbols:
                current_ring += 1
                label = hop_labels.get(current_ring, f"Hop {current_ring} Dependents")
                rings.append({
                    "hop": current_ring,
                    "label": label,
                    "symbols": ring_symbols,
                })
                current_symbols = next_symbols
            else:
                break
        
        return rings
        
    except Exception as e:
        # On any error, fall back to ring 0
        import logging
        logging.getLogger(__name__).warning(f"Graph expansion failed: {e}")
        return [{"hop": 0, "label": "Direct Changes", "symbols": ring0_symbols}]


# ── PR Resolution Helper ──


def _get_github_token(request: Optional[Request] = None) -> Optional[str]:
    """Get a GitHub token from available sources, in priority order:

    1. Session cookie (web OAuth login)
    2. GITHUB_TOKEN / GH_TOKEN environment variable
    3. gh CLI auth token (local file, no network needed)
    """
    # 1. From web session
    if request:
        from .auth_github import get_github_token_from_session

        token = get_github_token_from_session(request)
        if token:
            return token

    # 2. From environment
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        return token

    # 3. From gh CLI config (reads local file, no TLS needed)
    try:
        import shutil

        gh_path = shutil.which("gh") or "/opt/homebrew/bin/gh"
        if gh_path and os.path.isfile(gh_path):
            result = subprocess.run(
                [gh_path, "auth", "token"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
    except Exception:
        pass

    return None


def _resolve_pr_refs(
    repo_path: str, pr_number: int, request: Optional[Request] = None
) -> tuple[str, str, str]:
    """Resolve a PR number to (base_ref, head_ref, pr_title) via GitHub REST API.

    Uses Python httpx to call the GitHub API directly, avoiding the gh CLI
    TLS issues on macOS. Falls back through multiple token sources.

    Returns branch names prefixed with ``origin/`` so they work as git refs.
    """
    from ..ingestion.github.pr_fetcher import PRFetcher

    # Get owner/repo from git remote
    try:
        remote_url = subprocess.check_output(
            ["git", "-C", repo_path, "remote", "get-url", "origin"],
            text=True,
        ).strip()
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(f"Could not read git remote: {exc}") from exc

    owner, repo = PRFetcher.extract_repo_info(remote_url)
    if not owner or not repo:
        raise RuntimeError(f"Could not extract owner/repo from remote URL: {remote_url}")

    # Get a GitHub token
    token = _get_github_token(request)
    if not token:
        raise RuntimeError(
            "No GitHub token available. Log in via the web app, "
            "set GITHUB_TOKEN env var, or run 'gh auth login'."
        )

    # Call GitHub REST API directly (no gh CLI, no TLS issues)
    api_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    resp = httpx.get(api_url, headers=headers, timeout=15)
    if resp.status_code == 404:
        raise RuntimeError(f"PR #{pr_number} not found in {owner}/{repo}")
    if resp.status_code == 401:
        raise RuntimeError("GitHub token is invalid or expired. Please re-authenticate.")
    if resp.status_code != 200:
        raise RuntimeError(
            f"GitHub API error ({resp.status_code}): {resp.text[:200]}"
        )

    data = resp.json()
    base_branch = data["base"]["ref"]
    head_branch = data["head"]["ref"]
    title = data.get("title", "")

    return f"origin/{base_branch}", f"origin/{head_branch}", title


def _ensure_git_ref_available(repo_path: str, ref: str) -> None:
    """Ensure a git ref exists locally; fetch from origin when needed."""
    try:
        subprocess.run(
            ["git", "-C", repo_path, "rev-parse", "--verify", f"{ref}^{{commit}}"],
            capture_output=True,
            text=True,
            timeout=10,
            check=True,
        )
        return
    except subprocess.CalledProcessError:
        pass

    # Try to fetch missing remote-tracking refs.
    if ref.startswith("origin/"):
        branch = ref.removeprefix("origin/")
        fetch = subprocess.run(
            ["git", "-C", repo_path, "fetch", "--quiet", "origin", branch],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if fetch.returncode != 0:
            raise RuntimeError(
                f"Failed to fetch ref '{ref}' from origin: {fetch.stderr.strip() or fetch.stdout.strip()}"
            )

        verify = subprocess.run(
            ["git", "-C", repo_path, "rev-parse", "--verify", f"{ref}^{{commit}}"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if verify.returncode == 0:
            return

    raise RuntimeError(
        f"Git ref '{ref}' not found locally. Try fetching the repository and retry."
    )


# ── Request Models ──


class BlastRadiusRequest(BaseModel):
    repo_path: str
    base_ref: str = "HEAD~1"
    head_ref: str = "HEAD"
    max_hops: int = 3
    pr_number: Optional[int] = None


class ChangeStoryRequest(BaseModel):
    repo_path: str
    base_ref: str = "HEAD~1"
    head_ref: str = "HEAD"
    pr_number: Optional[int] = None


# ── Response Models ──


class BlastRadiusSymbol(BaseModel):
    qualified_name: str
    file_path: str = ""
    change_kind: Optional[str] = None
    symbol_kind: Optional[str] = None
    severity: float = 0.0
    line_start: Optional[int] = None
    line_end: Optional[int] = None
    relation: Optional[str] = None
    details: dict = Field(default_factory=dict)


class BlastRadiusRing(BaseModel):
    hop: int
    label: str
    symbols: list[BlastRadiusSymbol]


class BlastRadiusResponse(BaseModel):
    rings: list[BlastRadiusRing]
    total_affected: int
    risk_level: str
    suggestions: list[str] = Field(default_factory=list)
    pr_title: Optional[str] = None


class ChangeStoryChange(BaseModel):
    qualified_name: str
    file_path: str
    change_kind: str
    symbol_kind: str
    severity: float = 0.0
    line_start: Optional[int] = None
    line_end: Optional[int] = None
    old_qualified_name: Optional[str] = None
    details: dict = Field(default_factory=dict)


class ChangeStoryConsumer(BaseModel):
    qualified_name: str
    file_path: str = ""


class ChangeStory(BaseModel):
    kind: str
    title: str
    severity: str
    icon: str
    changes: list[ChangeStoryChange]
    affected_consumers: list[ChangeStoryConsumer] = Field(default_factory=list)
    summary: str


class ChangeStoryResponse(BaseModel):
    stories: list[ChangeStory]
    total_changes: int
    files_analyzed: int = 0
    summary: str
    pr_title: Optional[str] = None


class AnalysisRepoPR(BaseModel):
    number: int
    title: str
    state: str
    url: str
    base_ref: str
    head_ref: str
    updated_at: Optional[str] = None
    author: Optional[str] = None


class AnalysisRepoContextResponse(BaseModel):
    repo_path: Optional[str] = None
    github_repo: Optional[str] = None
    prs: list[AnalysisRepoPR] = Field(default_factory=list)
    token_available: bool = False
    error: Optional[str] = None


# ── Shared service logic ──


def _compute_blast_radius(repo_path: str, base_ref: str, head_ref: str, max_hops: int) -> dict:
    """Compute blast radius using AST diff engine and graph expansion.

    This is the shared implementation used by both the API endpoint and MCP tool.
    
    1. First, get direct changes via AST diff (Ring 0)
    2. Then, expand using the Kuzu graph database to find dependents (Rings 1+)
    """
    from ..ingestion.ast_diff import ASTDiffEngine

    _ensure_git_ref_available(repo_path, base_ref)
    _ensure_git_ref_available(repo_path, head_ref)

    engine = ASTDiffEngine(repo_path)
    symbol_diff = engine.diff(base_ref=base_ref, head_ref=head_ref)

    if not symbol_diff.changes:
        return {
            "rings": [],
            "total_affected": 0,
            "risk_level": "low",
            "suggestions": ["No symbol-level changes detected between the refs."],
        }

    ring0_symbols = []
    for change in symbol_diff.changes:
        ring0_symbols.append({
            "qualified_name": change.qualified_name,
            "file_path": change.file_path,
            "change_kind": change.change_kind.value,
            "symbol_kind": change.symbol_kind.value,
            "severity": change.severity,
            "line_start": change.line_start,
            "line_end": change.line_end,
            "details": change.details,
        })

    # Expand using graph database for multi-hop analysis
    rings = _expand_blast_radius_with_graph(repo_path, ring0_symbols, max_hops)
    
    # Calculate total affected across all rings
    total_affected = sum(len(r["symbols"]) for r in rings)

    # Calculate risk based on all affected symbols
    all_severities = [s["severity"] for r in rings for s in r["symbols"]]
    max_severity = max(all_severities, default=0.0)
    
    if total_affected > 50 or max_severity >= 1.0:
        risk_level = "high"
    elif total_affected > 10:
        risk_level = "medium"
    else:
        risk_level = "low"

    suggestions = []
    sig_changes = [c for c in symbol_diff.changes if c.change_kind.value == "signature_changed"]
    if sig_changes:
        suggestions.append(
            f"{len(sig_changes)} signature change(s) detected. All callers must be updated."
        )
    removed = [c for c in symbol_diff.changes if c.change_kind.value == "removed"]
    if removed:
        suggestions.append(f"{len(removed)} symbol(s) removed. Check for broken references.")
    if symbol_diff.parse_errors:
        suggestions.append(f"{len(symbol_diff.parse_errors)} file(s) had parse errors.")
    
    # Add graph-based suggestions
    if len(rings) > 1:
        ring1_count = len(rings[1]["symbols"]) if len(rings) > 1 else 0
        if ring1_count > 0:
            suggestions.append(
                f"{ring1_count} direct dependent(s) may be affected by these changes."
            )
        if len(rings) > 2:
            total_dependents = sum(len(r["symbols"]) for r in rings[1:])
            suggestions.append(
                f"Total blast radius: {total_dependents} dependent symbol(s) across {len(rings)-1} hop(s)."
            )
    else:
        suggestions.append(
            "Run 'emdash ingest' to build the call graph for full transitive analysis."
        )

    return {
        "rings": rings,
        "total_affected": total_affected,
        "risk_level": risk_level,
        "suggestions": suggestions,
    }


def _compute_change_story(repo_path: str, base_ref: str, head_ref: str) -> dict:
    """Compute change story using AST diff engine."""
    from ..ingestion.ast_diff import ASTDiffEngine

    _ensure_git_ref_available(repo_path, base_ref)
    _ensure_git_ref_available(repo_path, head_ref)

    engine = ASTDiffEngine(repo_path)
    symbol_diff = engine.diff(base_ref=base_ref, head_ref=head_ref)

    if not symbol_diff.changes:
        return {
            "stories": [],
            "total_changes": 0,
            "files_analyzed": 0,
            "summary": "No symbol-level changes detected.",
        }

    STORY_KINDS = {
        "CONTRACT_CHANGE": {"label": "Contract Changes", "severity": "high", "icon": "!"},
        "NEW_CAPABILITY": {"label": "New Capabilities", "severity": "low", "icon": "+"},
        "INTERNAL_CHANGE": {"label": "Internal Changes", "severity": "medium", "icon": "~"},
        "REMOVED": {"label": "Removals", "severity": "high", "icon": "-"},
        "TEST_COVERAGE": {"label": "Test Coverage", "severity": "info", "icon": "T"},
    }

    def _classify(change_kind: str, file_path: str) -> str:
        is_test = any(
            m in file_path
            for m in ("test_", "_test.", "tests/", "test/", "__tests__", ".test.", ".spec.")
        )
        if is_test:
            return "TEST_COVERAGE"
        if change_kind == "signature_changed":
            return "CONTRACT_CHANGE"
        elif change_kind == "added":
            return "NEW_CAPABILITY"
        elif change_kind in ("body_changed", "renamed", "moved"):
            return "INTERNAL_CHANGE"
        elif change_kind == "removed":
            return "REMOVED"
        return "INTERNAL_CHANGE"

    buckets: dict[str, list[dict]] = {k: [] for k in STORY_KINDS}
    for change in symbol_diff.changes:
        kind = _classify(change.change_kind.value, change.file_path)
        buckets[kind].append({
            "qualified_name": change.qualified_name,
            "file_path": change.file_path,
            "change_kind": change.change_kind.value,
            "symbol_kind": change.symbol_kind.value,
            "severity": change.severity,
            "line_start": change.line_start,
            "line_end": change.line_end,
            "old_qualified_name": change.old_qualified_name,
            "details": change.details,
        })

    stories = []
    for kind, changes_list in buckets.items():
        if not changes_list:
            continue
        meta = STORY_KINDS[kind]
        files = sorted({c["file_path"] for c in changes_list})
        title = (
            f"{meta['label']} in {files[0]}"
            if len(files) == 1
            else f"{meta['label']} across {len(files)} files"
        )
        stories.append({
            "kind": kind,
            "title": title,
            "severity": meta["severity"],
            "icon": meta["icon"],
            "changes": changes_list,
            "affected_consumers": [],
            "summary": f"{len(changes_list)} {meta['label'].lower()}.",
        })

    kind_counts = {k: len(v) for k, v in buckets.items() if v}
    parts = [f"{cnt} {STORY_KINDS[k]['label'].lower()}" for k, cnt in kind_counts.items()]
    overall_summary = "; ".join(parts) if parts else "No changes."

    return {
        "stories": stories,
        "total_changes": len(symbol_diff.changes),
        "files_analyzed": symbol_diff.files_analyzed,
        "summary": overall_summary,
    }


def _resolve_repo_path(path: Optional[str]) -> str:
    """Resolve to a git repository root path."""
    from ..config import get_config

    candidate = path or get_config().repo_root or os.getcwd()
    candidate = os.path.abspath(os.path.expanduser(candidate))
    if not os.path.isdir(candidate):
        raise RuntimeError(f"Path does not exist: {candidate}")

    try:
        return subprocess.check_output(
            ["git", "-C", candidate, "rev-parse", "--show-toplevel"],
            text=True,
        ).strip()
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(
            f"Path is not inside a git repository: {candidate}"
        ) from exc


def _resolve_github_repo(repo_path: str) -> tuple[str, str, str]:
    """Resolve owner/repo from a repo's origin remote."""
    from ..ingestion.github.pr_fetcher import PRFetcher

    try:
        remote_url = subprocess.check_output(
            ["git", "-C", repo_path, "remote", "get-url", "origin"],
            text=True,
        ).strip()
    except subprocess.CalledProcessError as exc:
        raise RuntimeError("Could not read git remote 'origin'.") from exc

    owner, repo = PRFetcher.extract_repo_info(remote_url)
    if not owner or not repo:
        raise RuntimeError(f"Origin remote is not a GitHub URL: {remote_url}")

    return owner, repo, f"{owner}/{repo}"


def _list_open_prs(
    repo_path: str, request: Optional[Request], limit: int = 20
) -> tuple[list[dict], bool]:
    """List open PRs for the repo using GitHub REST API."""
    owner, repo, _ = _resolve_github_repo(repo_path)
    token = _get_github_token(request)
    if not token:
        return [], False

    limit = max(1, min(limit, 100))
    api_url = (
        f"https://api.github.com/repos/{owner}/{repo}/pulls"
        f"?state=open&sort=updated&direction=desc&per_page={limit}"
    )
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    resp = httpx.get(api_url, headers=headers, timeout=15)
    if resp.status_code in (401, 403):
        return [], False
    if resp.status_code != 200:
        raise RuntimeError(f"GitHub API error ({resp.status_code}): {resp.text[:200]}")

    data = resp.json()
    prs = []
    for item in data:
        prs.append({
            "number": item.get("number"),
            "title": item.get("title") or "",
            "state": item.get("state") or "",
            "url": item.get("html_url") or "",
            "base_ref": item.get("base", {}).get("ref") or "",
            "head_ref": item.get("head", {}).get("ref") or "",
            "updated_at": item.get("updated_at"),
            "author": (item.get("user") or {}).get("login"),
        })
    return prs, True


# ── Endpoints ──


@router.get("/context", response_model=AnalysisRepoContextResponse)
async def analysis_context(
    request: Request,
    path: Optional[str] = Query(default=None),
    pr_limit: int = Query(default=20, ge=1, le=100),
):
    """Return repository context and open PRs for the analysis UI."""
    try:
        repo_path = _resolve_repo_path(path)
        _, _, github_repo = _resolve_github_repo(repo_path)
        prs, token_available = _list_open_prs(repo_path, request, limit=pr_limit)
        return AnalysisRepoContextResponse(
            repo_path=repo_path,
            github_repo=github_repo,
            prs=prs,
            token_available=token_available,
        )
    except Exception as e:
        return AnalysisRepoContextResponse(error=str(e))


@router.post("/blast-radius", response_model=BlastRadiusResponse)
async def blast_radius(req: BlastRadiusRequest, request: Request):
    """Compute the blast radius of changes between two git refs or a PR number.

    Returns rings of affected symbols expanding outward from direct changes.
    Uses the authenticated user's GitHub token (from session cookie) for PR lookups.
    """
    try:
        pr_title = None
        base_ref, head_ref = req.base_ref, req.head_ref
        if req.pr_number is not None:
            base_ref, head_ref, pr_title = _resolve_pr_refs(
                req.repo_path, req.pr_number, request
            )
        result = await asyncio.wait_for(
            asyncio.to_thread(_compute_blast_radius, req.repo_path, base_ref, head_ref, req.max_hops),
            timeout=ANALYSIS_TIMEOUT_SECONDS,
        )
        result["pr_title"] = pr_title
        return BlastRadiusResponse(**result)
    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=504,
            detail=(
                "Blast radius analysis timed out after "
                f"{ANALYSIS_TIMEOUT_SECONDS}s. Try using refs mode with a smaller change range."
            ),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/change-story", response_model=ChangeStoryResponse)
async def change_story(req: ChangeStoryRequest, request: Request):
    """Generate a structured narrative of code changes between two git refs or a PR number.

    Groups changes into stories by kind: contract changes, new capabilities,
    internal changes, removals, and test coverage.
    Uses the authenticated user's GitHub token (from session cookie) for PR lookups.
    """
    try:
        pr_title = None
        base_ref, head_ref = req.base_ref, req.head_ref
        if req.pr_number is not None:
            base_ref, head_ref, pr_title = _resolve_pr_refs(
                req.repo_path, req.pr_number, request
            )
        result = await asyncio.wait_for(
            asyncio.to_thread(_compute_change_story, req.repo_path, base_ref, head_ref),
            timeout=ANALYSIS_TIMEOUT_SECONDS,
        )
        result["pr_title"] = pr_title
        return ChangeStoryResponse(**result)
    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=504,
            detail=(
                "Change story analysis timed out after "
                f"{ANALYSIS_TIMEOUT_SECONDS}s. Try using refs mode with a smaller change range."
            ),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── SSE Streaming Endpoints ──


@router.post("/blast-radius/stream")
async def blast_radius_stream(req: BlastRadiusRequest, request: Request):
    """Stream blast radius analysis with real-time progress updates.
    
    Uses SSE to send progress events during analysis:
    - progress: Status updates during processing
    - ring_complete: When each ring is computed
    - result: Final result with all rings
    - error: If an error occurs
    """
    from fastapi.responses import StreamingResponse
    from datetime import datetime
    import json
    
    async def generate():
        try:
            # Resolve PR refs if needed
            pr_title = None
            base_ref, head_ref = req.base_ref, req.head_ref
            if req.pr_number is not None:
                yield f"event: progress\ndata: {json.dumps({'message': f'Resolving PR #{req.pr_number}...'})}\n\n"
                base_ref, head_ref, pr_title = _resolve_pr_refs(
                    req.repo_path, req.pr_number, request
                )
                yield f"event: progress\ndata: {json.dumps({'message': f'Comparing {base_ref} → {head_ref}'})}\n\n"
            
            # Ensure git refs are available
            yield f"event: progress\ndata: {json.dumps({'message': 'Fetching git refs...'})}\n\n"
            _ensure_git_ref_available(req.repo_path, base_ref)
            _ensure_git_ref_available(req.repo_path, head_ref)
            
            # Get changed files
            yield f"event: progress\ndata: {json.dumps({'message': 'Finding changed files...'})}\n\n"
            import git
            repo = git.Repo(req.repo_path)
            base_commit = repo.commit(base_ref)
            head_commit = repo.commit(head_ref)
            diff = base_commit.diff(head_ref)
            changed_files = [item.b_path or item.a_path for item in diff if item.change_type in ('A', 'M', 'R')]
            
            yield f"event: progress\ndata: {json.dumps({'message': f'Found {len(changed_files)} changed file(s)'})}\n\n"
            
            # Parse and diff (Ring 0)
            yield f"event: progress\ndata: {json.dumps({'message': 'Analyzing direct changes (Ring 0)...'})}\n\n"
            from ..ingestion.ast_diff import ASTDiffEngine
            engine = ASTDiffEngine(req.repo_path)
            symbol_diff = engine.diff(base_ref=base_ref, head_ref=head_ref)
            
            ring0_count = len(symbol_diff.changes)
            yield f"event: progress\ndata: {json.dumps({'message': f'Found {ring0_count} symbol-level change(s)'})}\n\n"
            
            if not symbol_diff.changes:
                result = {
                    "rings": [],
                    "total_affected": 0,
                    "risk_level": "low",
                    "suggestions": ["No symbol-level changes detected between the refs."],
                    "pr_title": pr_title,
                }
                yield f"event: result\ndata: {json.dumps(result)}\n\n"
                return
            
            # Build ring 0
            ring0_symbols = []
            for change in symbol_diff.changes:
                ring0_symbols.append({
                    "qualified_name": change.qualified_name,
                    "file_path": change.file_path,
                    "change_kind": change.change_kind.value,
                    "symbol_kind": change.symbol_kind.value,
                    "severity": change.severity,
                    "line_start": change.line_start,
                    "line_end": change.line_end,
                    "details": change.details,
                })
            
            rings = [{"hop": 0, "label": "Direct Changes", "symbols": ring0_symbols}]
            yield f"event: ring_complete\ndata: {json.dumps({'hop': 0, 'count': len(ring0_symbols)})}\n\n"
            
            # Expand rings if max_hops > 0
            if req.max_hops > 0:
                yield f"event: progress\ndata: {json.dumps({'message': f'Expanding to {req.max_hops} hop(s) via graph database...'})}\n\n"
                
                # Use graph expansion with progress
                rings = _expand_blast_radius_with_graph_progress(
                    req.repo_path, ring0_symbols, req.max_hops, 
                    lambda msg: None  # Could yield progress here too
                )
                
                for ring in rings[1:]:  # Skip ring 0, already sent
                    yield f"event: ring_complete\ndata: {json.dumps({'hop': ring['hop'], 'count': len(ring['symbols'])})}\n\n"
            
            # Calculate final result
            total_affected = sum(len(r["symbols"]) for r in rings)
            all_severities = [s["severity"] for r in rings for s in r["symbols"]]
            max_severity = max(all_severities, default=0.0)
            
            if total_affected > 50 or max_severity >= 1.0:
                risk_level = "high"
            elif total_affected > 10:
                risk_level = "medium"
            else:
                risk_level = "low"
            
            # Build suggestions
            suggestions = []
            sig_changes = [c for c in symbol_diff.changes if c.change_kind.value == "signature_changed"]
            if sig_changes:
                suggestions.append(f"{len(sig_changes)} signature change(s) detected. All callers must be updated.")
            removed = [c for c in symbol_diff.changes if c.change_kind.value == "removed"]
            if removed:
                suggestions.append(f"{len(removed)} symbol(s) removed. Check for broken references.")
            if symbol_diff.parse_errors:
                suggestions.append(f"{len(symbol_diff.parse_errors)} file(s) had parse errors.")
            if len(rings) > 1:
                total_dependents = sum(len(r["symbols"]) for r in rings[1:])
                suggestions.append(f"Total blast radius: {total_dependents} dependent symbol(s) across {len(rings)-1} hop(s).")
            else:
                suggestions.append("Run 'emdash ingest' to build the call graph for full transitive analysis.")
            
            result = {
                "rings": rings,
                "total_affected": total_affected,
                "risk_level": risk_level,
                "suggestions": suggestions,
                "pr_title": pr_title,
            }
            
            yield f"event: result\ndata: {json.dumps(result)}\n\n"
            
        except Exception as e:
            yield f"event: error\ndata: {json.dumps({'message': str(e)})}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # Disable nginx buffering
        },
    )


def _expand_blast_radius_with_graph_progress(
    repo_path: str,
    ring0_symbols: list[dict],
    max_hops: int,
    progress_callback: Optional[callable],
) -> list[dict]:
    """Expand blast radius with optional progress callback."""
    try:
        from ..graph.connection import configure_for_repo, get_read_connection, KUZU_AVAILABLE
        
        if not KUZU_AVAILABLE:
            return [{"hop": 0, "label": "Direct Changes", "symbols": ring0_symbols}]
        
        from pathlib import Path
        configure_for_repo(Path(repo_path))
        conn = get_read_connection()
        
        try:
            conn.execute("RETURN 1 AS test")
        except Exception:
            return [{"hop": 0, "label": "Direct Changes", "symbols": ring0_symbols}]
        
        rings = [{"hop": 0, "label": "Direct Changes", "symbols": ring0_symbols}]
        
        if max_hops <= 0 or not ring0_symbols:
            return rings
        
        changed_names = {s["qualified_name"] for s in ring0_symbols}
        all_seen = set(changed_names)
        current_ring = 0
        current_symbols = set(changed_names)
        
        hop_labels = {
            1: "Direct Dependents",
            2: "Secondary Dependents", 
            3: "Tertiary Dependents",
        }
        
        while current_ring < max_hops and current_symbols:
            next_symbols = set()
            ring_symbols = []
            
            for sym_name in current_symbols:
                # Find callers
                try:
                    caller_query = """
                        MATCH (caller:Function)-[:CALLS]->(callee:Function {qualified_name: $name})
                        RETURN caller.qualified_name AS qualified_name,
                               caller.file_path AS file_path,
                               caller.line_start AS line_start,
                               caller.line_end AS line_end
                        LIMIT 50
                    """
                    for row in conn.execute(caller_query, {"name": sym_name}):
                        qn = row.get("qualified_name")
                        if qn and qn not in all_seen:
                            all_seen.add(qn)
                            next_symbols.add(qn)
                            ring_symbols.append({
                                "qualified_name": qn,
                                "file_path": row.get("file_path", ""),
                                "change_kind": None,
                                "symbol_kind": "function",
                                "severity": 0.5,
                                "line_start": row.get("line_start"),
                                "line_end": row.get("line_end"),
                                "relation": "caller",
                                "details": {"called_symbol": sym_name},
                            })
                except Exception:
                    pass
                
                # Find callees
                try:
                    callee_query = """
                        MATCH (caller:Function {qualified_name: $name})-[:CALLS]->(callee:Function)
                        RETURN callee.qualified_name AS qualified_name,
                               callee.file_path AS file_path,
                               callee.line_start AS line_start,
                               callee.line_end AS line_end
                        LIMIT 50
                    """
                    for row in conn.execute(callee_query, {"name": sym_name}):
                        qn = row.get("qualified_name")
                        if qn and qn not in all_seen:
                            all_seen.add(qn)
                            next_symbols.add(qn)
                            ring_symbols.append({
                                "qualified_name": qn,
                                "file_path": row.get("file_path", ""),
                                "change_kind": None,
                                "symbol_kind": "function",
                                "severity": 0.4,
                                "line_start": row.get("line_start"),
                                "line_end": row.get("line_end"),
                                "relation": "callee",
                                "details": {"called_by": sym_name},
                            })
                except Exception:
                    pass
                
                # Find class methods
                try:
                    method_query = """
                        MATCH (c:Class {qualified_name: $name})-[:HAS_METHOD]->(m:Function)
                        RETURN m.qualified_name AS qualified_name,
                               m.file_path AS file_path,
                               m.line_start AS line_start,
                               m.line_end AS line_end
                        LIMIT 50
                    """
                    for row in conn.execute(method_query, {"name": sym_name}):
                        qn = row.get("qualified_name")
                        if qn and qn not in all_seen:
                            all_seen.add(qn)
                            next_symbols.add(qn)
                            ring_symbols.append({
                                "qualified_name": qn,
                                "file_path": row.get("file_path", ""),
                                "change_kind": None,
                                "symbol_kind": "method",
                                "severity": 0.6,
                                "line_start": row.get("line_start"),
                                "line_end": row.get("line_end"),
                                "relation": "method",
                                "details": {"parent_class": sym_name},
                            })
                except Exception:
                    pass
            
            if ring_symbols:
                current_ring += 1
                label = hop_labels.get(current_ring, f"Hop {current_ring} Dependents")
                rings.append({
                    "hop": current_ring,
                    "label": label,
                    "symbols": ring_symbols,
                })
                if progress_callback:
                    progress_callback(f"Ring {current_ring}: {len(ring_symbols)} symbols")
                current_symbols = next_symbols
            else:
                break
        
        return rings
        
    except Exception:
        return [{"hop": 0, "label": "Direct Changes", "symbols": ring0_symbols}]
