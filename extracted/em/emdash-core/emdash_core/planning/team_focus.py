"""Team focus analyzer using graph data and LLM synthesis."""

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Optional

from ..analytics.engine import AnalyticsEngine
from ..graph.connection import KuzuConnection, get_connection
from ..ingestion.github.pr_fetcher import PRFetcher
from .feature_expander import FeatureExpander, FeatureGraph
from ..agent.providers import get_provider
from ..agent.providers.factory import DEFAULT_MODEL
from ..templates.loader import load_template_for_agent
from ..utils.logger import log


@dataclass
class TeamFocusData:
    """Data collected for team focus analysis."""

    # Repository info for GitHub links
    github_url: Optional[str] = None

    # Area focus (directories)
    hot_areas: list[dict] = field(default_factory=list)

    # File focus (individual files)
    hot_files: list[dict] = field(default_factory=list)

    # Code context for hot files (classes, functions, docstrings)
    hot_file_code_context: list[dict] = field(default_factory=list)

    # Open PRs (work in progress)
    open_prs: list[dict] = field(default_factory=list)

    # Recently merged PRs
    merged_prs: list[dict] = field(default_factory=list)

    # Detailed graph context from PR files (code entities, call graph)
    pr_graph_context: list[dict] = field(default_factory=list)

    # Contributors active in the time window
    active_contributors: list[dict] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "github_url": self.github_url,
            "hot_areas": self.hot_areas,
            "hot_files": self.hot_files,
            "hot_file_code_context": self.hot_file_code_context,
            "open_prs": self.open_prs,
            "merged_prs": self.merged_prs,
            "pr_graph_context": self.pr_graph_context,
            "active_contributors": self.active_contributors,
        }


def _get_system_prompt() -> str:
    """Get the system prompt for team focus analysis.

    Loads the focus template if available, otherwise uses a fallback.
    """
    try:
        return load_template_for_agent("focus")
    except Exception as e:
        log.warning(f"Could not load focus template, using fallback: {e}")
        return """You are a senior engineering manager analyzing your team's recent activity and focus areas.

You have access to DETAILED CODE CONTEXT including:
- What classes and functions are in each hot file
- What code entities each PR is modifying
- Docstrings explaining what the code does
- Call graph relationships showing code flow

YOUR JOB: Use this code context to explain WHAT the team is actually building/changing, not just which files they're touching.

## LINK FORMATTING (REQUIRED)

You MUST use markdown links for PRs and contributors:
- PRs: `[PR #123](https://github.com/owner/repo/pull/123)` - use the GitHub URL provided in the data
- Contributors: `[@username](https://github.com/username)` - always link to their GitHub profile

Example: "[@liorfo](https://github.com/liorfo) opened [PR #1847](https://github.com/wix-private/picasso/pull/1847)"

## ANALYSIS GUIDELINES

For each work stream, explain:
1. **WHAT** is being built/changed (based on class/function names and docstrings)
2. **WHY** it matters (infer from the code purpose)
3. **HOW** it fits together (use call graph info)

Example of GOOD analysis:
"The team is building a **streaming response handler** for the AI coder:
- `StreamProcessor` class handles chunked LLM responses
- `createAppStreamStep()` orchestrates the streaming workflow
- Changes to `WorkflowManager` integrate this into the main pipeline"

Example of BAD analysis (too vague):
"The team is working on packages/picasso-mastra-server/"

When describing PRs, explain WHAT the code change accomplishes based on:
- The PR description
- The function/class names being modified
- Their docstrings

Be specific about the technical changes. Use the code entity information provided.

Output in markdown with these sections:
1. **Executive Summary** - 2-3 sentences on main focus
2. **Work Streams** - Grouped by theme, with specific code details
3. **PR Analysis** - What each is changing (use code context!) - USE PR LINKS
4. **Key Contributors** - Who's working on what - USE CONTRIBUTOR LINKS
5. **Technical Insights** - Patterns, risks, or recommendations"""


class TeamFocusAnalyzer:
    """Analyzes team focus and work-in-progress using graph data and LLM."""

    def __init__(
        self,
        connection: Optional[KuzuConnection] = None,
        model: str = DEFAULT_MODEL,
    ):
        """Initialize team focus analyzer.

        Args:
            connection: Neo4j connection. If None, uses global connection.
            model: LLM model to use for synthesis.
        """
        self.connection = connection or get_connection()
        self.model = model
        self.analytics = AnalyticsEngine(self.connection)
        self.expander = FeatureExpander(self.connection)
        self._provider = None

    @property
    def provider(self):
        """Get LLM provider lazily."""
        if self._provider is None:
            self._provider = get_provider(self.model)
        return self._provider

    def _get_github_url(self) -> Optional[str]:
        """Get the GitHub repository URL from the database.

        Returns:
            GitHub URL like 'https://github.com/owner/repo' or None if not found
        """
        import re

        with self.connection.session() as session:
            result = session.run(
                """
                MATCH (r:Repository)
                RETURN r.owner as owner, r.name as name, r.url as url
                LIMIT 1
                """
            )
            record = result.single()
            if not record:
                return None

            # Try owner/name first
            if record["owner"] and record["name"]:
                return f"https://github.com/{record['owner']}/{record['name']}"

            # Fall back to parsing the URL
            url = record.get("url", "")
            if not url:
                return None

            # Parse SSH format: git@github.com:owner/repo.git
            ssh_match = re.match(r"git@github\.com:([^/]+)/([^/]+?)(?:\.git)?$", url)
            if ssh_match:
                return f"https://github.com/{ssh_match.group(1)}/{ssh_match.group(2)}"

            # Parse HTTPS format: https://github.com/owner/repo.git
            https_match = re.match(r"https://github\.com/([^/]+)/([^/]+?)(?:\.git)?/?$", url)
            if https_match:
                return f"https://github.com/{https_match.group(1)}/{https_match.group(2)}"

            return None

    def gather_data(
        self,
        days: int = 14,
        top_areas: int = 8,
        top_files: int = 25,
        max_prs: int = 20,
        include_graph_context: bool = True,
    ) -> TeamFocusData:
        """Gather all data needed for team focus analysis.

        Args:
            days: Time window for recency scoring
            top_areas: Number of top areas to include
            top_files: Number of top files to include (primary focus)
            max_prs: Maximum number of PRs to include
            include_graph_context: Whether to expand PR files through graph

        Returns:
            TeamFocusData with all gathered information
        """
        log.info(f"Gathering team focus data (last {days} days)...")

        data = TeamFocusData()

        # Get GitHub URL for generating links
        data.github_url = self._get_github_url()
        if data.github_url:
            log.info(f"GitHub repo: {data.github_url}")

        # 1. Get hot files FIRST (sorted by recent activity) - this is the primary data
        files = self.analytics.compute_file_importance(days=days, limit=top_files * 2)
        # Sort by recent commits
        files_with_recent = [f for f in files if f.get("recent_commits", 0) > 0]
        files_with_recent.sort(key=lambda x: x.get("recent_commits", 0), reverse=True)
        data.hot_files = files_with_recent[:top_files]
        log.info(f"Found {len(data.hot_files)} hot files")

        # 2. Get hot areas (sorted by focus) - secondary/summary data
        areas = self.analytics.compute_area_importance(
            depth=2, days=days, limit=top_areas * 2
        )
        # Sort by focus percentage and filter to those with recent activity
        areas_with_focus = [a for a in areas if a.get("focus_pct", 0) > 0]
        areas_with_focus.sort(key=lambda x: x.get("focus_pct", 0), reverse=True)
        data.hot_areas = areas_with_focus[:top_areas]
        log.info(f"Found {len(data.hot_areas)} hot areas")

        # 3. Get open PRs
        data.open_prs = self._get_prs(state="open", limit=max_prs)
        log.info(f"Found {len(data.open_prs)} open PRs")

        # 4. Get recently merged PRs
        data.merged_prs = self._get_prs(state="merged", limit=max_prs)
        log.info(f"Found {len(data.merged_prs)} merged PRs")

        # 5. Get active contributors
        data.active_contributors = self._get_active_contributors(days=days)
        log.info(f"Found {len(data.active_contributors)} active contributors")

        # 6. Optionally expand PR files through graph for context
        if include_graph_context:
            # Get detailed PR context
            data.pr_graph_context = self._get_pr_graph_context(
                data.open_prs + data.merged_prs[:10]  # More PRs for better coverage
            )
            log.info(f"Gathered graph context for {len(data.pr_graph_context)} PRs")

            # Get code context for hot files
            data.hot_file_code_context = self._get_hot_file_code_context(
                data.hot_files, limit=12
            )
            log.info(f"Gathered code context for {len(data.hot_file_code_context)} hot files")

        return data

    def _get_prs(self, state: str = "all", limit: int = 20) -> list[dict]:
        """Get PRs from the graph database, with GitHub fallback.

        Args:
            state: PR state (open, merged, closed, all)
            limit: Maximum PRs to return

        Returns:
            List of PR dictionaries
        """
        # First try database
        prs = self._get_prs_from_db(state, limit)

        # If database is empty, try fetching from GitHub
        if not prs:
            log.info(f"No PRs in database, fetching from GitHub...")
            prs = self._fetch_prs_from_github(state, limit)

        return prs

    def _get_prs_from_db(self, state: str, limit: int) -> list[dict]:
        """Get PRs from the graph database."""
        with self.connection.session() as session:
            state_filter = ""
            if state == "open":
                state_filter = "AND pr.state = 'open'"
            elif state == "merged":
                state_filter = "AND pr.state = 'merged'"
            elif state == "closed":
                state_filter = "AND pr.state IN ['closed', 'merged']"

            result = session.run(
                f"""
                MATCH (pr:PullRequest)
                WHERE pr.number IS NOT NULL
                {state_filter}
                OPTIONAL MATCH (pr)-[:PR_MODIFIES]->(f:File)
                WITH pr, collect(DISTINCT f.path) as files
                RETURN pr.number as number,
                       pr.title as title,
                       pr.author as author,
                       pr.state as state,
                       pr.created_at as created_at,
                       pr.merged_at as merged_at,
                       pr.additions as additions,
                       pr.deletions as deletions,
                       pr.description as description,
                       size(files) as files_count,
                       files[0:10] as files
                ORDER BY COALESCE(pr.merged_at, pr.created_at) DESC
                LIMIT $limit
                """,
                limit=limit,
            )

            return [dict(record) for record in result]

    def _fetch_prs_from_github(self, state: str, limit: int) -> list[dict]:
        """Fetch PRs directly from GitHub using gh CLI.

        Falls back to this when database has no PR data.
        """
        # Get GitHub URL to extract owner/repo
        github_url = self._get_github_url()
        if not github_url:
            log.warning("Cannot fetch PRs: GitHub URL not available")
            return []

        # Extract owner/repo from URL
        # URL format: https://github.com/owner/repo
        parts = github_url.replace("https://github.com/", "").split("/")
        if len(parts) < 2:
            log.warning(f"Cannot parse GitHub URL: {github_url}")
            return []

        owner, repo = parts[0], parts[1]

        try:
            fetcher = PRFetcher(owner=owner, repo=repo)
            if not fetcher.gh_path:
                log.warning("gh CLI not available, cannot fetch PRs")
                return []

            # Fetch PRs from GitHub
            pr_entities = fetcher.fetch_prs(state=state, limit=limit)

            # Convert to dict format expected by the analyzer
            prs = []
            for pr in pr_entities:
                files = pr.files_changed or []
                prs.append({
                    "number": pr.number,
                    "title": pr.title,
                    "author": pr.author,
                    "state": pr.state,
                    "created_at": pr.created_at,
                    "merged_at": pr.merged_at,
                    "additions": pr.additions,
                    "deletions": pr.deletions,
                    "description": pr.description,
                    "files_count": len(files),
                    "files": files[:10],
                })

            log.info(f"Fetched {len(prs)} PRs from GitHub")
            return prs

        except Exception as e:
            log.warning(f"Failed to fetch PRs from GitHub: {e}")
            return []

    def _get_active_contributors(self, days: int = 14) -> list[dict]:
        """Get contributors active in the time window.

        Args:
            days: Time window in days

        Returns:
            List of contributor dictionaries
        """
        # Calculate cutoff timestamp
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)

        with self.connection.session() as session:
            # Get contributors from recent commits
            result = session.run(
                """
                MATCH (c:GitCommit)-[:AUTHORED_BY]->(a:Author)
                WHERE c.timestamp >= $cutoff
                WITH a, count(c) as commit_count
                OPTIONAL MATCH (c2:GitCommit)-[:AUTHORED_BY]->(a)
                WHERE c2.timestamp >= $cutoff
                OPTIONAL MATCH (c2)-[:COMMIT_MODIFIES]->(f:File)
                WITH a, commit_count, collect(DISTINCT f.path) as files
                RETURN a.name as name,
                       a.email as email,
                       commit_count,
                       size(files) as files_touched,
                       files[0:5] as sample_files
                ORDER BY commit_count DESC
                LIMIT 15
                """,
                cutoff=cutoff,
            )

            contributors = [dict(record) for record in result]

            # Also get contributors from PRs
            pr_result = session.run(
                """
                MATCH (pr:PullRequest)
                WHERE pr.created_at >= $cutoff
                   OR pr.merged_at >= $cutoff
                WITH pr.author as author, count(pr) as pr_count
                WHERE author IS NOT NULL
                RETURN author as name, pr_count
                ORDER BY pr_count DESC
                LIMIT 10
                """,
                cutoff=cutoff,
            )

            # Merge PR authors into contributors
            pr_authors = {r["name"]: r["pr_count"] for r in pr_result}
            for contrib in contributors:
                name = contrib.get("name", "")
                if name in pr_authors:
                    contrib["pr_count"] = pr_authors[name]

            return contributors

    def _get_pr_graph_context(self, prs: list[dict], max_files_per_pr: int = 5) -> list[dict]:
        """Get detailed graph context for PR files including code insights.

        Args:
            prs: List of PR dictionaries
            max_files_per_pr: Maximum files to expand per PR

        Returns:
            List of detailed context dictionaries per PR
        """
        contexts = []

        for pr in prs[:15]:  # Process more PRs for better coverage
            pr_context = {
                "pr_number": pr.get("number"),
                "pr_title": pr.get("title"),
                "pr_description": pr.get("description", ""),
                "pr_author": pr.get("author", "unknown"),
                "files_changed": pr.get("files", [])[:10],
                "additions": pr.get("additions", 0),
                "deletions": pr.get("deletions", 0),
                "code_entities": [],
                "call_graph_samples": [],
            }

            files = pr.get("files", [])[:max_files_per_pr]

            for file_path in files:
                if not file_path:
                    continue

                try:
                    graph = self.expander.expand_from_file(file_path, max_hops=1)

                    # Extract filename for context
                    filename = file_path.split("/")[-1] if "/" in file_path else file_path

                    # Extract classes with more detail
                    for cls in graph.classes[:3]:
                        pr_context["code_entities"].append({
                            "type": "Class",
                            "name": cls.get("name"),
                            "file": filename,
                            "docstring": (cls.get("docstring") or "")[:200],
                            "qualified_name": cls.get("qualified_name", ""),
                        })

                    # Extract functions with more detail
                    for func in graph.functions[:6]:
                        pr_context["code_entities"].append({
                            "type": "Function",
                            "name": func.get("name"),
                            "file": filename,
                            "docstring": (func.get("docstring") or "")[:200],
                            "qualified_name": func.get("qualified_name", ""),
                        })

                    # Extract call graph samples to understand code flow
                    for call in graph.call_graph[:5]:
                        pr_context["call_graph_samples"].append({
                            "caller": call.get("caller", ""),
                            "callee": call.get("callee", ""),
                        })

                except Exception as e:
                    log.debug(f"Could not expand file {file_path}: {e}")
                    continue

            contexts.append(pr_context)

        return contexts

    def _get_hot_file_code_context(self, hot_files: list[dict], limit: int = 10) -> list[dict]:
        """Get code context for the hottest files.

        Args:
            hot_files: List of hot file dictionaries
            limit: Maximum files to analyze

        Returns:
            List of file context with code entities
        """
        file_contexts = []

        for f in hot_files[:limit]:
            file_path = f.get("file_path", "")
            if not file_path:
                continue

            file_ctx = {
                "file_path": file_path,
                "filename": file_path.split("/")[-1] if "/" in file_path else file_path,
                "recent_commits": f.get("recent_commits", 0),
                "classes": [],
                "functions": [],
            }

            try:
                graph = self.expander.expand_from_file(file_path, max_hops=1)

                for cls in graph.classes[:3]:
                    file_ctx["classes"].append({
                        "name": cls.get("name"),
                        "docstring": (cls.get("docstring") or "")[:150],
                    })

                for func in graph.functions[:5]:
                    file_ctx["functions"].append({
                        "name": func.get("name"),
                        "docstring": (func.get("docstring") or "")[:150],
                    })

                if file_ctx["classes"] or file_ctx["functions"]:
                    file_contexts.append(file_ctx)

            except Exception as e:
                log.debug(f"Could not get context for {file_path}: {e}")
                continue

        return file_contexts

    def _build_prompt(self, data: TeamFocusData, days: int) -> str:
        """Build the LLM prompt from gathered data.

        Args:
            data: TeamFocusData with all gathered information
            days: Time window for context

        Returns:
            Formatted prompt string
        """
        sections = []

        sections.append(f"# Team Focus Analysis (Last {days} Days)\n")

        # Add GitHub URL for link generation
        if data.github_url:
            sections.append(f"**Repository:** {data.github_url}")
            sections.append("")
            sections.append("**IMPORTANT - Use these link formats in your output:**")
            sections.append(f"- PRs: `[PR #123]({data.github_url}/pull/123)`")
            sections.append(f"- Contributors: `[@username](https://github.com/username)`")
            sections.append("")

        # Hot Files FIRST - this is the PRIMARY data, most specific and actionable
        if data.hot_files:
            sections.append("## HOT FILES - Most Active Individual Files")
            sections.append("")
            sections.append("**IMPORTANT: These specific files have the most recent activity. Reference these in your summary!**")
            sections.append("")
            sections.append("| File | Recent Commits | Total Commits | Authors |")
            sections.append("|------|----------------|---------------|---------|")
            for f in data.hot_files[:20]:  # Show up to 20 files
                path = f.get("file_path", "unknown")
                # Shorten path for display but keep enough context
                if "/" in path:
                    parts = path.split("/")
                    # Keep last 4 parts for better context
                    path = "/".join(parts[-4:]) if len(parts) > 4 else path
                recent = f.get("recent_commits", 0)
                total = f.get("commits", 0)
                authors = f.get("authors", 0)
                sections.append(f"| `{path}` | {recent} | {total} | {authors} |")
            sections.append("")

        # Hot Areas - summary view
        if data.hot_areas:
            sections.append("## Hot Areas (Directory Summary)")
            sections.append("")
            sections.append("Aggregated view of where activity is concentrated:")
            sections.append("")
            for area in data.hot_areas:
                path = area.get("path", "unknown")
                focus = area.get("focus_pct", 0)
                commits = area.get("total_commits", 0)
                authors = area.get("unique_authors", 0)
                file_count = area.get("file_count", 0)
                sections.append(
                    f"- **{path}**: {focus:.1f}% of recent commits, "
                    f"{commits} total commits, {file_count} files, {authors} contributors"
                )
            sections.append("")

        # Code context for hot files - what's IN those files
        if data.hot_file_code_context:
            sections.append("## Code Context for Hot Files")
            sections.append("")
            sections.append("What code entities are in the most active files:")
            sections.append("")
            for fctx in data.hot_file_code_context[:10]:
                filename = fctx.get("filename", "unknown")
                recent = fctx.get("recent_commits", 0)
                sections.append(f"### `{filename}` ({recent} recent commits)")

                classes = fctx.get("classes", [])
                if classes:
                    for cls in classes[:2]:
                        name = cls.get("name", "")
                        doc = cls.get("docstring", "")
                        if doc:
                            sections.append(f"- **Class `{name}`**: {doc}")
                        else:
                            sections.append(f"- **Class `{name}`**")

                funcs = fctx.get("functions", [])
                if funcs:
                    for func in funcs[:4]:
                        name = func.get("name", "")
                        doc = func.get("docstring", "")
                        if doc:
                            sections.append(f"- `{name}()`: {doc}")
                        else:
                            sections.append(f"- `{name}()`")
                sections.append("")

        # Detailed PR context with code entities
        if data.pr_graph_context:
            sections.append("## PR Deep Dive - What Code is Being Changed")
            sections.append("")
            sections.append("Detailed analysis of what each PR is modifying:")
            sections.append("")

            for pr_ctx in data.pr_graph_context[:12]:
                pr_num = pr_ctx.get("pr_number", "?")
                pr_title = pr_ctx.get("pr_title", "Unknown")
                pr_desc = pr_ctx.get("pr_description", "")
                pr_author = pr_ctx.get("pr_author", "unknown")
                additions = pr_ctx.get("additions", 0)
                deletions = pr_ctx.get("deletions", 0)
                files = pr_ctx.get("files_changed", [])

                sections.append(f"### PR #{pr_num}: {pr_title}")
                sections.append(f"**Author:** @{pr_author} | **Changes:** +{additions}/-{deletions}")

                if pr_desc:
                    # Clean and truncate description
                    desc = pr_desc.replace("\n", " ").strip()[:300]
                    sections.append(f"**Description:** {desc}")

                if files:
                    file_names = [f.split("/")[-1] for f in files[:5]]
                    sections.append(f"**Files:** {', '.join(file_names)}")

                entities = pr_ctx.get("code_entities", [])
                if entities:
                    sections.append("**Code being modified:**")
                    for ent in entities[:6]:
                        etype = ent.get("type", "")
                        ename = ent.get("name", "")
                        efile = ent.get("file", "")
                        edoc = ent.get("docstring", "")
                        if edoc:
                            sections.append(f"  - {etype} `{ename}` in {efile}: {edoc[:100]}")
                        else:
                            sections.append(f"  - {etype} `{ename}` in {efile}")

                # Show call graph if available
                calls = pr_ctx.get("call_graph_samples", [])
                if calls:
                    call_strs = [f"{c['caller']}->{c['callee']}" for c in calls[:3]]
                    sections.append(f"**Call flow:** {', '.join(call_strs)}")

                sections.append("")

        # Open PRs summary (shorter, since we have deep dive above)
        if data.open_prs:
            sections.append("## Open PRs Summary")
            sections.append("")
            for pr in data.open_prs[:8]:
                number = pr.get("number", "?")
                title = pr.get("title", "Unknown")[:50]
                author = pr.get("author", "unknown")
                sections.append(f"- **#{number}**: {title} (@{author})")
            sections.append("")

        # Merged PRs summary
        if data.merged_prs:
            sections.append("## Recently Merged PRs")
            sections.append("")
            for pr in data.merged_prs[:8]:
                number = pr.get("number", "?")
                title = pr.get("title", "Unknown")[:50]
                author = pr.get("author", "unknown")
                sections.append(f"- **#{number}**: {title} (@{author})")
            sections.append("")

        # Graph Context (entities touched by PRs)
        if data.pr_graph_context:
            sections.append("## Key Code Entities Affected by PRs")
            sections.append("")
            for ctx in data.pr_graph_context[:5]:
                pr_num = ctx.get("pr_number", "?")
                pr_title = ctx.get("pr_title", "")[:40]
                entities = ctx.get("entities", [])
                if entities:
                    sections.append(f"**PR #{pr_num}** ({pr_title}...):")
                    for ent in entities[:4]:
                        etype = ent.get("type", "?")
                        ename = ent.get("name", "?")
                        edoc = ent.get("docstring", "")
                        if edoc:
                            sections.append(f"  - {etype} `{ename}`: {edoc}")
                        else:
                            sections.append(f"  - {etype} `{ename}`")
            sections.append("")

        # Active Contributors
        if data.active_contributors:
            sections.append("## Active Contributors")
            sections.append("")
            for contrib in data.active_contributors[:8]:
                name = contrib.get("name", "unknown")
                commits = contrib.get("commit_count", 0)
                files = contrib.get("files_touched", 0)
                pr_count = contrib.get("pr_count", 0)
                parts = [f"{commits} commits"]
                if files:
                    parts.append(f"{files} files")
                if pr_count:
                    parts.append(f"{pr_count} PRs")
                sections.append(f"- **{name}**: {', '.join(parts)}")
            sections.append("")

        # Final instruction
        sections.append("---")
        sections.append("")
        sections.append(
            "Based on the CODE CONTEXT above, provide a technical analysis:\n\n"
            "## Executive Summary\n"
            "2-3 sentences: What is the team primarily building/improving?\n\n"
            "## Work Streams (Use Code Context!)\n"
            "Group related work and explain WHAT is being built using the class/function info:\n"
            "- Name the actual classes and functions being modified\n"
            "- Explain what they do (use the docstrings provided)\n"
            "- Show how they connect (use call graph info)\n\n"
            "## PR Analysis\n"
            "For each major PR, explain the technical change:\n"
            "- What code entities are being modified?\n"
            "- What capability is being added/changed?\n\n"
            "## Key Contributors\n"
            "Who's working on what technical areas?\n\n"
            "## Technical Insights\n"
            "Patterns, architectural changes, or areas needing attention."
        )

        return "\n".join(sections)

    def analyze(
        self,
        days: int = 14,
        include_graph_context: bool = True,
    ) -> str:
        """Analyze team focus and generate LLM summary.

        Args:
            days: Time window for recency scoring
            include_graph_context: Whether to expand PR files through graph

        Returns:
            LLM-generated summary in markdown format
        """
        # Gather all data
        data = self.gather_data(
            days=days,
            include_graph_context=include_graph_context,
        )

        # Build prompt
        prompt = self._build_prompt(data, days)

        # Call LLM
        log.info("Generating team focus summary with LLM...")

        response = self.provider.chat(
            messages=[{"role": "user", "content": prompt}],
            system=_get_system_prompt(),
        )

        return response.content or ""

    def get_raw_data(self, days: int = 14) -> dict:
        """Get raw data without LLM synthesis (for JSON output).

        Args:
            days: Time window for recency scoring

        Returns:
            Dictionary with all gathered data
        """
        data = self.gather_data(days=days, include_graph_context=False)
        return data.to_dict()
