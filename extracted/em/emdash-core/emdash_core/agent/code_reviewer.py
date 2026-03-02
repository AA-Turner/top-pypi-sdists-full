"""Code reviewer agent for generating PR reviews using learned reviewer profiles."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field, asdict
from typing import Any, Optional

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

from .toolkit import AgentToolkit
from .providers import get_provider
from .providers.factory import DEFAULT_MODEL
from ..templates import load_template_for_agent
from ..utils.logger import log


@dataclass
class ReviewComment:
    """An inline review comment on a specific line of code."""

    path: str           # File path relative to repo root
    line: int           # Line number in the diff
    body: str           # Comment text
    side: str = "RIGHT"  # LEFT (old code) or RIGHT (new code)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ReviewResult:
    """Result of a code review."""

    summary: str                    # Overall review summary
    verdict: str                    # APPROVE, REQUEST_CHANGES, or COMMENT
    comments: list[ReviewComment] = field(default_factory=list)

    @property
    def comments_count(self) -> int:
        return len(self.comments)


REVIEW_SYSTEM_PROMPT = """You are reviewing a pull request as a senior code reviewer. You have access to tools to explore the codebase and verify your understanding.

## Your Reviewer Profile
{profile}

## Your Task
Review the PR thoroughly. You SHOULD use the available tools to:
1. Understand the context of changes (use semantic_search, expand_node)
2. Check how similar patterns are handled elsewhere (use text_search, get_callers)
3. Verify the impact of changes (use get_impact_analysis)
4. Look at related files (use get_file_dependencies)
5. **Verify your comments with grep** - Before making a comment, use the grep tool to verify your claims are accurate

## Review Process
1. First, explore the PR diff provided
2. Use tools to understand the code context and verify your assumptions
3. **IMPORTANT: Before writing each comment, use the grep tool to verify:**
   - The pattern/issue you're commenting on actually exists
   - Similar patterns in the codebase to ensure consistency feedback is accurate
   - Any claims about "missing" code or "unused" variables are correct
4. Once you have verified your findings, generate your review

## Final Output
When you're ready to submit your review, output a JSON block with this EXACT format:

```json
{{
    "summary": "Overall review summary - be constructive and specific",
    "verdict": "APPROVE" | "REQUEST_CHANGES" | "COMMENT",
    "comments": [
        {{
            "path": "path/to/file.py",
            "line": 42,
            "body": "Detailed comment explaining the issue or suggestion",
            "side": "RIGHT"
        }}
    ]
}}
```

Guidelines for comments:
- "verdict" must be exactly one of: APPROVE, REQUEST_CHANGES, COMMENT
- "line" is the line number in the NEW version of the file (side=RIGHT)
- Use "side": "LEFT" only when commenting on deleted lines
- Be specific and constructive
- Only comment where there's something meaningful to say

IMPORTANT: When you're done exploring and ready to submit, output the JSON block. Do NOT wrap it in markdown code fences other than ```json.
"""


class CodeReviewerAgent:
    """Agent that generates PR reviews using a learned reviewer profile and tool access."""

    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        verbose: bool = True,
        enable_posting: bool = False,
        max_iterations: int = 10,
    ):
        """Initialize the code reviewer agent.

        Args:
            model: LLM model to use
            verbose: Whether to print progress
            enable_posting: Whether to allow posting reviews to GitHub
            max_iterations: Maximum tool call iterations
        """
        self.provider = get_provider(model)
        self.toolkit = AgentToolkit(enable_session=False)
        self.model = model
        self.verbose = verbose
        self.enable_posting = enable_posting
        self.max_iterations = max_iterations
        self.console = Console()

        # Load the reviewer profile
        try:
            self.profile = load_template_for_agent("reviewer")
        except FileNotFoundError:
            log.warning("Reviewer profile not found, using default template")
            self.profile = self._get_default_profile()

    def _get_default_profile(self) -> str:
        """Get a minimal default profile if no template exists."""
        return """Focus on:
- Code correctness and potential bugs
- Security issues
- Performance concerns
- Code clarity and maintainability
- Test coverage

Be constructive and specific in your feedback."""

    def review(self, pr_number: int) -> ReviewResult:
        """Generate a review for a pull request.

        Args:
            pr_number: The PR number to review

        Returns:
            ReviewResult with summary, verdict, and inline comments
        """
        if self.verbose:
            self.console.print(f"\n[bold cyan]Reviewing PR #{pr_number}[/bold cyan]\n")

        # 1. Fetch PR details
        pr_data = self._fetch_pr(pr_number)
        if not pr_data:
            raise ValueError(f"Failed to fetch PR #{pr_number}")

        # 2. Build initial context
        context = self._build_review_context(pr_data)

        # 3. Run agent loop with tool access
        result = self._run_review_loop(context)

        if self.verbose:
            self._print_review_summary(result)

        return result

    def _fetch_pr(self, pr_number: int) -> Optional[dict]:
        """Fetch PR details including diff."""
        result = self.toolkit.execute(
            "github_pr_details",
            pull_number=pr_number,
            include_diff=True,
            include_comments=True,
            include_reviews=True,
            include_review_comments=True,
        )

        if not result.success:
            log.error(f"Failed to fetch PR: {result.error}")
            return None

        return result.data

    def _build_review_context(self, pr_data: dict) -> str:
        """Build context string for the LLM review."""
        pr = pr_data.get("pr", {})
        diff = pr_data.get("diff", "")

        # Parse diff to get file-level context
        files = self._parse_diff_files(diff)

        context_parts = [
            f"# PR #{pr.get('number')}: {pr.get('title')}",
            f"\n**Author:** {pr.get('user', {}).get('login', 'unknown')}",
            f"**State:** {pr.get('state')}",
            f"**Changes:** +{pr.get('additions', 0)} / -{pr.get('deletions', 0)}",
        ]

        # Add PR description if available
        body = pr.get("body")
        if body:
            context_parts.append(f"\n## Description\n{body[:2000]}")

        # Add existing review comments for context
        existing_comments_data = pr_data.get("review_comments", {})
        existing_comments = []
        if isinstance(existing_comments_data, dict):
            existing_comments = existing_comments_data.get("nodes", [])
        elif isinstance(existing_comments_data, list):
            existing_comments = existing_comments_data

        if existing_comments:
            context_parts.append(f"\n## Existing Review Comments ({len(existing_comments)})")
            for c in existing_comments[:5]:
                if isinstance(c, dict):
                    user = c.get("user", {}).get("login", "unknown")
                    path = c.get("path", "")
                    body = c.get("body", "")[:200]
                    context_parts.append(f"- **{user}** on `{path}`: {body}")

        # Add diff with file structure
        context_parts.append("\n## Changes\n")
        for file_info in files[:20]:  # Limit to 20 files
            context_parts.append(f"\n### {file_info['path']}\n```diff")
            context_parts.append(file_info["content"][:8000])  # Limit per file
            context_parts.append("```")

        return "\n".join(context_parts)

    def _parse_diff_files(self, diff: str) -> list[dict]:
        """Parse unified diff into file-level chunks."""
        if not diff:
            return []

        files = []
        current_file = None
        current_lines = []

        for line in diff.splitlines():
            if line.startswith("diff --git"):
                if current_file and current_lines:
                    files.append({
                        "path": current_file,
                        "content": "\n".join(current_lines),
                    })
                current_file = None
                current_lines = []
            elif line.startswith("+++ b/"):
                current_file = line[6:]
            elif current_file:
                current_lines.append(line)

        # Don't forget the last file
        if current_file and current_lines:
            files.append({
                "path": current_file,
                "content": "\n".join(current_lines),
            })

        return files

    def _run_review_loop(self, context: str) -> ReviewResult:
        """Run the agent loop with tool access."""
        # Build system prompt with profile
        system_prompt = REVIEW_SYSTEM_PROMPT.format(profile=self.profile)

        # Get tool schemas
        tools = self.toolkit.get_all_schemas()

        # Initialize messages
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Please review this pull request:\n\n{context}"},
        ]

        iterations = 0
        while iterations < self.max_iterations:
            iterations += 1

            # Call LLM
            response = self.provider.chat(messages, tools=tools)

            # Add assistant message
            messages.append(self.provider.format_assistant_message(response))

            # Check for tool calls
            if response.tool_calls:
                for tool_call in response.tool_calls:
                    result = self._execute_tool_call(tool_call)
                    result_json = json.dumps(result, default=str)

                    # Truncate large results
                    if len(result_json) > 10000:
                        result_json = result_json[:10000] + "...[TRUNCATED]"

                    messages.append(
                        self.provider.format_tool_result(tool_call.id, result_json)
                    )
            else:
                # No tool calls - try to parse the review
                content = response.content or ""
                result = self._parse_review_response(content)

                # If we got a valid result, return it
                if result.summary or result.comments:
                    return result

                # Otherwise, ask the LLM to provide the final review
                messages.append({
                    "role": "user",
                    "content": "Please provide your final review in the JSON format specified.",
                })

        # Max iterations reached - return what we have
        messages.append({
            "role": "user",
            "content": (
                "Tool budget reached. Provide your final review now in the JSON format specified. "
                "Do not call any tools."
            ),
        })
        final_response = self.provider.chat(messages, tools=None)
        final_content = final_response.content or ""
        final_result = self._parse_review_response(final_content)
        if final_result.summary or final_result.comments:
            return final_result

        log.warning("Max iterations reached, returning partial review")
        return ReviewResult(
            summary="Review incomplete - max iterations reached",
            verdict="COMMENT",
            comments=[],
        )

    def _execute_tool_call(self, tool_call) -> dict:
        """Execute a tool call and return the result."""
        name = tool_call.name
        try:
            args = json.loads(tool_call.arguments)
        except json.JSONDecodeError:
            args = {}

        if self.verbose:
            self.console.print(f"[dim]Using tool: {name}[/dim]")

        result = self.toolkit.execute(name, **args)

        if result.success:
            return {
                "success": True,
                "data": result.data,
            }
        else:
            return {
                "success": False,
                "error": result.error,
            }

    def _parse_review_response(self, content: str) -> ReviewResult:
        """Parse LLM response into ReviewResult."""
        try:
            # Remove markdown code blocks if present
            json_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", content)
            if json_match:
                content = json_match.group(1)

            # Try to find JSON object in the content
            json_start = content.find("{")
            json_end = content.rfind("}") + 1
            if json_start >= 0 and json_end > json_start:
                content = content[json_start:json_end]

            data = json.loads(content.strip())

            comments = []
            for c in data.get("comments", []):
                comments.append(ReviewComment(
                    path=c.get("path", ""),
                    line=c.get("line", 1),
                    body=c.get("body", ""),
                    side=c.get("side", "RIGHT"),
                ))

            return ReviewResult(
                summary=data.get("summary", ""),
                verdict=data.get("verdict", "COMMENT"),
                comments=comments,
            )

        except json.JSONDecodeError as e:
            log.debug(f"Failed to parse review JSON: {e}")
            return ReviewResult(summary="", verdict="COMMENT", comments=[])

    def _print_review_summary(self, result: ReviewResult):
        """Print a summary of the review to console."""
        # Verdict color
        verdict_colors = {
            "APPROVE": "green",
            "REQUEST_CHANGES": "red",
            "COMMENT": "yellow",
        }
        color = verdict_colors.get(result.verdict, "white")

        # Print summary panel
        self.console.print(Panel(
            f"[bold {color}]{result.verdict}[/bold {color}]\n\n{result.summary}",
            title="Review Summary",
            border_style=color,
        ))

        # Print each comment in full
        if result.comments:
            self.console.print(f"\n[bold]Inline Comments ({len(result.comments)}):[/bold]\n")

            for i, comment in enumerate(result.comments, 1):
                self.console.print(Panel(
                    f"[cyan]{comment.path}[/cyan]:[magenta]{comment.line}[/magenta]\n\n{comment.body}",
                    title=f"Comment {i}",
                    border_style="dim",
                ))

    def post_review(self, pr_number: int, result: ReviewResult) -> bool:
        """Post the review to GitHub.

        Args:
            pr_number: The PR number
            result: The review result to post

        Returns:
            True if successful, False otherwise
        """
        if not self.enable_posting:
            log.error("Posting is disabled. Initialize with enable_posting=True")
            return False

        # Convert comments to dict format
        comments = [c.to_dict() for c in result.comments] if result.comments else None

        post_result = self.toolkit.execute(
            "github_create_review",
            pull_number=pr_number,
            body=result.summary,
            event=result.verdict,
            comments=comments,
        )

        if not post_result.success:
            log.error(f"Failed to post review: {post_result.error}")
            return False

        if self.verbose:
            self.console.print(
                f"\n[bold green]✓[/bold green] Review posted to PR #{pr_number}"
            )

        return True

    def review_and_post(self, pr_number: int) -> tuple[ReviewResult, bool]:
        """Generate and post a review.

        Args:
            pr_number: The PR number to review

        Returns:
            Tuple of (ReviewResult, success_bool)
        """
        result = self.review(pr_number)
        success = self.post_review(pr_number, result)
        return result, success


# Alias for backwards compatibility with API that imports CodeReviewer
CodeReviewer = CodeReviewerAgent
