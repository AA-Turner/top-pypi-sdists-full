"""Reviewer profile agent for analyzing repository reviewers and generating profiles."""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from .toolkit import AgentToolkit
from .providers import get_provider
from .providers.factory import DEFAULT_MODEL
from ..graph.connection import get_connection
from ..utils.logger import log


@dataclass
class ReviewerData:
    """Data about a reviewer's patterns."""

    username: str
    review_count: int
    prs_reviewed: list[int] = field(default_factory=list)
    review_comments: list[dict] = field(default_factory=list)
    review_verdicts: list[str] = field(default_factory=list)  # APPROVED, CHANGES_REQUESTED, etc.


@dataclass
class ContributorData:
    """Data about a cross-team contributor."""

    name: str
    email: str
    communities_touched: int
    commit_count: int


SYNTHESIS_PROMPT = """You are analyzing code review patterns from a repository to create a reviewer profile template.

Based on the following data about top reviewers and cross-team contributors, create a comprehensive reviewer profile that captures:

1. **Review Focus Areas**: What aspects of code do reviewers commonly focus on?
2. **Feedback Patterns**: What types of issues do they commonly point out?
3. **Code Quality Expectations**: What standards do they enforce?
4. **Style Preferences**: What coding patterns do they prefer?
5. **Tone & Communication**: How do they phrase their feedback?
6. **Example Comments**: Representative examples of good review comments
7. **Review Checklist**: Key items reviewers check before approving

IMPORTANT:
- Extract patterns from the actual review comments provided
- Be specific about the types of issues raised
- Capture the tone and phrasing style
- Generate a checklist based on what reviewers actually check
- The output should be markdown that can be used as a template for future reviews

OUTPUT FORMAT:
Return a complete markdown document that follows this structure:

# Reviewer Profile

## Identity
- Primary reviewers analyzed: {list of usernames}
- Cross-team contributors analyzed: {list of names}
- PRs analyzed: {count}

## Review Focus Areas
{bullet points of what reviewers focus on}

## Feedback Patterns
### What they commonly comment on:
{patterns}

### Code quality expectations:
{expectations}

### Style preferences:
{preferences}

## Tone & Communication
{description of tone and communication style}

## Example Comments
{3-5 representative example comments from the data}

## Review Checklist
{checklist items based on what reviewers check}
"""


class ReviewerProfileAgent:
    """Agent that analyzes repository reviewers and generates a profile template."""

    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        verbose: bool = True,
    ):
        self.provider = get_provider(model)
        self.toolkit = AgentToolkit(enable_session=False)
        self.model = model
        self.verbose = verbose
        self.console = Console()

        # Graph connection for Neo4j queries
        try:
            self.graph = get_connection()
        except Exception:
            self.graph = None
            log.warning("Neo4j connection not available - cross-team contributor analysis will be skipped")

    def analyze(
        self,
        top_n_reviewers: int = 5,
        top_n_contributors: int = 5,
        max_prs: int = 100,
    ) -> str:
        """Analyze repository reviewers and generate a profile.

        Args:
            top_n_reviewers: Number of top reviewers to analyze
            top_n_contributors: Number of cross-team contributors to include
            max_prs: Maximum PRs to fetch for analysis

        Returns:
            Generated reviewer profile as markdown
        """
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
            disable=not self.verbose,
        ) as progress:
            # 1. Fetch all PRs
            task = progress.add_task("Fetching PRs...", total=None)
            prs = self._fetch_all_prs(max_prs=max_prs)
            progress.update(task, description=f"Fetched {len(prs)} PRs")

            # 2. Count reviews, get top reviewers
            progress.update(task, description="Identifying top reviewers...")
            top_reviewers = self._get_top_reviewers(prs, top_n_reviewers)
            progress.update(task, description=f"Found {len(top_reviewers)} top reviewers")

            # 3. Fetch review comments for each top reviewer
            progress.update(task, description="Fetching review comments...")
            reviewer_data = self._fetch_reviewer_details(top_reviewers, prs)

            # 4. Query Neo4j for multi-community contributors
            cross_team = []
            if self.graph:
                progress.update(task, description="Finding cross-team contributors...")
                cross_team = self._get_cross_team_contributors(top_n_contributors)

            # 5. Synthesize with LLM
            progress.update(task, description="Synthesizing reviewer profile...")
            profile = self._synthesize_profile(reviewer_data, cross_team, len(prs))

            progress.update(task, description="Done!")

        return profile

    def _fetch_all_prs(self, max_prs: int = 100) -> list[dict]:
        """Fetch PRs from the repository.

        Args:
            max_prs: Maximum number of PRs to fetch

        Returns:
            List of PR data dictionaries
        """
        all_prs = []

        # Fetch closed/merged PRs (more likely to have reviews)
        for state in ["closed", "open"]:
            result = self.toolkit.execute(
                "github_list_prs",
                state=state,
                per_page=min(100, max_prs - len(all_prs)),
            )

            if result.success:
                prs = result.data.get("prs", [])
                all_prs.extend(prs)

                if len(all_prs) >= max_prs:
                    break

        return all_prs[:max_prs]

    def _get_top_reviewers(
        self,
        prs: list[dict],
        top_n: int = 5,
    ) -> list[tuple[str, int, list[int]]]:
        """Identify top reviewers by counting reviews across PRs.

        Args:
            prs: List of PR data
            top_n: Number of top reviewers to return

        Returns:
            List of (username, review_count, pr_numbers) tuples
        """
        reviewer_counts: Counter = Counter()
        reviewer_prs: dict[str, list[int]] = {}

        for pr in prs:
            pr_number = pr.get("number")
            if not pr_number:
                continue

            # Fetch PR details to get reviewers
            details = self.toolkit.execute(
                "github_pr_details",
                pull_number=pr_number,
                include_diff=False,
                include_comments=False,
                include_reviews=True,
                include_review_comments=False,
            )

            if not details.success:
                continue

            reviews = details.data.get("reviews", [])
            if not isinstance(reviews, list):
                continue

            seen_reviewers = set()
            for review in reviews:
                if not isinstance(review, dict):
                    continue
                user = review.get("user", {})
                if isinstance(user, dict):
                    username = user.get("login")
                    if username and username not in seen_reviewers:
                        reviewer_counts[username] += 1
                        if username not in reviewer_prs:
                            reviewer_prs[username] = []
                        reviewer_prs[username].append(pr_number)
                        seen_reviewers.add(username)

        # Get top N reviewers
        top = reviewer_counts.most_common(top_n)
        return [(username, count, reviewer_prs.get(username, [])) for username, count in top]

    def _fetch_reviewer_details(
        self,
        top_reviewers: list[tuple[str, int, list[int]]],
        prs: list[dict],
    ) -> list[ReviewerData]:
        """Fetch detailed review data for top reviewers.

        Args:
            top_reviewers: List of (username, count, pr_numbers) tuples
            prs: List of PR data

        Returns:
            List of ReviewerData objects
        """
        reviewer_data = []

        for username, count, pr_numbers in top_reviewers:
            data = ReviewerData(
                username=username,
                review_count=count,
                prs_reviewed=pr_numbers,
            )

            # Fetch review comments for each PR they reviewed
            for pr_number in pr_numbers[:10]:  # Limit to 10 PRs per reviewer
                details = self.toolkit.execute(
                    "github_pr_details",
                    pull_number=pr_number,
                    include_diff=False,
                    include_comments=False,
                    include_reviews=True,
                    include_review_comments=True,
                )

                if not details.success:
                    continue

                # Get their reviews
                reviews = details.data.get("reviews", [])
                for review in reviews:
                    if not isinstance(review, dict):
                        continue
                    user = review.get("user", {})
                    if isinstance(user, dict) and user.get("login") == username:
                        state = review.get("state")
                        if state:
                            data.review_verdicts.append(state)
                        body = review.get("body")
                        if body:
                            data.review_comments.append({
                                "type": "review",
                                "pr": pr_number,
                                "body": body,
                                "state": state,
                            })

                # Get their inline comments
                review_comments = details.data.get("review_comments", [])
                for comment in review_comments:
                    if not isinstance(comment, dict):
                        continue
                    user = comment.get("user", {})
                    if isinstance(user, dict) and user.get("login") == username:
                        data.review_comments.append({
                            "type": "inline",
                            "pr": pr_number,
                            "path": comment.get("path"),
                            "line": comment.get("line") or comment.get("position"),
                            "body": comment.get("body"),
                        })

            reviewer_data.append(data)

        return reviewer_data

    def _get_cross_team_contributors(self, top_n: int = 5) -> list[ContributorData]:
        """Query Neo4j for contributors who touch multiple communities.

        Args:
            top_n: Number of contributors to return

        Returns:
            List of ContributorData objects
        """
        if not self.graph:
            return []

        try:
            with self.graph.session() as session:
                result = session.run(
                    """
                    MATCH (c:GitCommit)-[:AUTHORED_BY]->(a:Author)
                    MATCH (c)-[:COMMIT_MODIFIES]->(f:File)
                    MATCH (f)-[:CONTAINS_CLASS|CONTAINS_FUNCTION]->(entity)
                    WHERE entity.community IS NOT NULL
                    WITH a, count(DISTINCT entity.community) as communities, count(DISTINCT c) as commits
                    WHERE communities >= 2
                    RETURN a.name as name, a.email as email, communities, commits
                    ORDER BY communities DESC, commits DESC
                    LIMIT $top_n
                    """,
                    top_n=top_n,
                )

                contributors = []
                for record in result:
                    contributors.append(ContributorData(
                        name=record["name"],
                        email=record["email"],
                        communities_touched=record["communities"],
                        commit_count=record["commits"],
                    ))

                return contributors

        except Exception as e:
            log.warning(f"Failed to query cross-team contributors: {e}")
            return []

    def _synthesize_profile(
        self,
        reviewer_data: list[ReviewerData],
        cross_team: list[ContributorData],
        pr_count: int,
    ) -> str:
        """Use LLM to synthesize a reviewer profile from the data.

        Args:
            reviewer_data: Data about top reviewers
            cross_team: Data about cross-team contributors
            pr_count: Total number of PRs analyzed

        Returns:
            Generated reviewer profile markdown
        """
        # Build context for the LLM
        context = {
            "pr_count": pr_count,
            "reviewers": [],
            "cross_team_contributors": [],
        }

        for data in reviewer_data:
            context["reviewers"].append({
                "username": data.username,
                "review_count": data.review_count,
                "verdicts": dict(Counter(data.review_verdicts)),
                "sample_comments": data.review_comments[:20],  # Limit to 20 comments
            })

        for contrib in cross_team:
            context["cross_team_contributors"].append({
                "name": contrib.name,
                "communities_touched": contrib.communities_touched,
                "commit_count": contrib.commit_count,
            })

        # Call LLM
        response = self.provider.chat(
            [
                {"role": "system", "content": SYNTHESIS_PROMPT},
                {"role": "user", "content": f"Analyze this reviewer data and generate a profile:\n\n{json.dumps(context, indent=2)}"},
            ]
        )

        return response.content or ""

    def save_template(
        self,
        profile: str,
        output_path: Optional[Path] = None,
    ) -> Path:
        """Save the generated profile to .emdash-rules/reviewer.md.template.

        Args:
            profile: Generated profile markdown
            output_path: Optional custom output path

        Returns:
            Path where the template was saved
        """
        if output_path is None:
            output_path = Path.cwd() / ".emdash-rules" / "reviewer.md.template"

        # Ensure directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Write the template
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(profile)

        return output_path

    # Alias for API compatibility
    def build(
        self,
        top_reviewers: int = 5,
        top_contributors: int = 10,
        max_prs: int = 50,
    ) -> dict:
        """Build reviewer profile (API compatibility method).

        Args:
            top_reviewers: Number of top reviewers to analyze
            top_contributors: Number of cross-team contributors to include
            max_prs: Maximum PRs to fetch for analysis

        Returns:
            Dictionary with profile results
        """
        profile = self.analyze(
            top_n_reviewers=top_reviewers,
            top_n_contributors=top_contributors,
            max_prs=max_prs,
        )
        return {
            "profile": profile,
            "reviewers_analyzed": top_reviewers,
            "contributors_analyzed": top_contributors,
            "prs_analyzed": max_prs,
        }


# Alias for backwards compatibility with API
ReviewerProfileBuilder = ReviewerProfileAgent
