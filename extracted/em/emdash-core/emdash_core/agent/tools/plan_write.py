"""WritePlan tool for Plan sub-agents.

Allows writing implementation plans to a restricted directory (.emdash/plans/).
This is the only write operation available to Plan agents.
"""

from pathlib import Path
import re

from .base import BaseTool, ToolResult, ToolCategory
from ...utils.logger import log


class WritePlanTool(BaseTool):
    """Write implementation plan to .emdash/plans/ directory only.

    This tool is restricted to writing markdown files only to the
    .emdash/plans/ directory. It cannot write to any other location.
    """

    name = "write_plan"
    description = """Write or update an implementation plan markdown file.

Plans are saved to .emdash/plans/<filename>.md in the repository.
Use this to document implementation strategies, architectural decisions,
and step-by-step plans.

Example filenames: "auth-refactor.md", "api-redesign.md", "feature-plan.md"
"""
    category = ToolCategory.PLANNING

    def __init__(self, repo_root: Path, connection=None):
        """Initialize with repo root.

        Args:
            repo_root: Root directory of the repository
            connection: Optional connection (not used)
        """
        self.repo_root = repo_root.resolve()
        self.plans_dir = self.repo_root / ".emdash" / "plans"
        self.connection = connection

    def execute(
        self,
        filename: str = "",
        content: str = "",
        **kwargs,
    ) -> ToolResult:
        """Write a plan file.

        Args:
            filename: Plan filename (e.g., "auth-refactor.md")
            content: Markdown content for the plan

        Returns:
            ToolResult indicating success or error
        """
        # Validate filename
        if not filename:
            return ToolResult.error_result("Filename is required")

        # Ensure .md extension
        if not filename.endswith(".md"):
            filename = f"{filename}.md"

        # Sanitize filename - remove path components and invalid chars
        safe_filename = Path(filename).name
        safe_filename = re.sub(r'[<>:"/\\|?*]', '-', safe_filename)

        if not safe_filename or safe_filename.startswith('.'):
            return ToolResult.error_result(
                f"Invalid filename: {filename}",
                suggestions=["Use alphanumeric characters, hyphens, underscores"],
            )

        # Build full path
        plan_path = self.plans_dir / safe_filename

        # Validate path is within plans directory (prevent traversal)
        try:
            plan_path.resolve().relative_to(self.plans_dir.resolve())
        except ValueError:
            return ToolResult.error_result(
                "Path traversal not allowed",
                suggestions=["Provide a simple filename without directory paths"],
            )

        try:
            # Create plans directory if needed
            self.plans_dir.mkdir(parents=True, exist_ok=True)

            # Check if updating existing file
            is_update = plan_path.exists()

            # Write the plan
            plan_path.write_text(content)

            log.info(
                "Plan {} written: {}",
                "updated" if is_update else "created",
                plan_path,
            )

            return ToolResult.success_result(
                data={
                    "path": str(plan_path.relative_to(self.repo_root)),
                    "filename": safe_filename,
                    "bytes_written": len(content),
                    "is_update": is_update,
                },
            )

        except PermissionError:
            return ToolResult.error_result(
                f"Permission denied writing to {plan_path}",
            )
        except Exception as e:
            log.exception("Failed to write plan")
            return ToolResult.error_result(f"Failed to write plan: {e}")

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "filename": {
                    "type": "string",
                    "description": "Plan filename (e.g., 'auth-refactor.md', 'feature-plan')",
                },
                "content": {
                    "type": "string",
                    "description": "Markdown content for the implementation plan",
                },
            },
            required=["filename", "content"],
        )
