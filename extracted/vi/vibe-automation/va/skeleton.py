import typer
from pathlib import Path


def create_workflow_skeleton(file: Path) -> None:
    """Create a skeleton workflow file by asking user's high-level goal."""
    typer.echo(
        f"File '{file}' does not exist. Starting interactive workflow development mode."
    )

    # Prompt user for high-level goal
    goal = typer.prompt("What is the high-level goal of your workflow?")

    # Create skeleton workflow file
    skeleton_content = _generate_skeleton_workflow(goal)

    # Write the skeleton to the file
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text(skeleton_content)

    typer.echo(f"Created skeleton workflow file: {file}")


def _generate_skeleton_workflow(goal: str) -> str:
    """Generate a skeleton workflow file with basic structure."""
    return f'''import asyncio
import logging

from va import step, workflow, assert_workflow_completion
from va.playwright import get_browser_context


@workflow()
async def main():
    """{goal}"""
    async with get_browser_context(headless=False, slow_mo=1000) as browser:
        page = await browser.new_page()

        await assert_workflow_completion(page)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
'''
