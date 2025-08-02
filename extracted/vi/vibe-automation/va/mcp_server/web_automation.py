"""Web automation tools for MCP server."""

import logging

from mcp import types

from va.playwright import create_browser_context_async
from va.playwright.page import Page
from va.playwright.tools import PLAYWRIGHT_TOOLS

log = logging.getLogger(__name__)

# Set the playwright default timeout. 3 seconds. This is so if we don't find a locator
# or some playwright operation fails, it fails early so the agent can continue.
PLAYWRIGHT_TIMEOUT = 3000

# For navigation, we set a longer timeout. 15 seconds.
PLAYWRIGHT_NAVIGATION_TIMEOUT = 15000


class WebAutomationTools:
    """Web automation tools that can be exposed via MCP."""

    def __init__(self):
        self.context = None
        self.browser = None
        self.page = None

    async def _get_or_create_page(self) -> Page:
        """Get or create a page with VibePage functionality."""
        if self.page is None:
            if self.context is None:
                self.context, self.browser = await create_browser_context_async(
                    headless=False
                )
                self.context.set_default_navigation_timeout(
                    PLAYWRIGHT_NAVIGATION_TIMEOUT
                )
                self.context.set_default_timeout(PLAYWRIGHT_TIMEOUT)

            # Get existing page or create new one
            if self.context.pages:
                self.page = self.context.pages[0]
            else:
                self.page = await self.context.new_page()

        return self.page

    async def cleanup(self):
        """Clean up browser resources."""
        if self.context and self.browser:
            await self.context._wait_for_login_tasks()
            await self.context.close()
            await self.browser.close()
            self.context = None
            self.page = None

    async def navigate_to_url(self, url: str) -> str:
        """Navigate to a specific URL."""
        try:
            page = await self._get_or_create_page()
            await page.goto(url)
            return f"Successfully navigated to: {url}"
        except Exception as e:
            log.error(f"Failed to navigate to {url}: {e}")
            return f"Error navigating to {url}: {e}"


EXECUTE_PYTHON_COMMAND_DESCRIPTION = """
Execute Python code. Intended for Playwright automation, but flexible.
Test commands incrementally and build your script from successful ones.
IMPORTANT: Use 'await' for all Playwright operations (page.fill, page.click, etc.) since they are asynchronous. 
Never use refs (like 'e3') directly in Playwright code - always call find_element_by_ref() first to get the proper locator.
Examples: await page.fill('input[name=\"field\"]', 'value'), await page.click('button'), await page.screenshot(path='screenshot.png')
"""

EXECUTE_PYTHON_COMMAND_DESCRIPTION_VISION = """
Execute Python code. Intended for Playwright automation, but flexible.
Test commands incrementally and build your script from successful ones.
YOU ARE NOT ALLOWED TO USE THIS TOOL to exeute playwright operations UNLESS you run inspect_html first to get the locator.
IMPORTANT: Use 'await' for all Playwright operations (page.fill, page.click, etc.) since they are asynchronous. 
Examples: await page.fill('input[name=\"field\"]', 'value'), await page.click('button'), await page.screenshot(path='screenshot.png')
"""


def create_tools(mode: str = "full") -> list[types.Tool]:
    """Create MCP tool definitions based on mode."""
    vision_html_tools = {
        "inspect_html",
        "execute_python_command",
        "get_page_screenshot",
        "navigate_to_url",
    }

    all_tools = [
        *PLAYWRIGHT_TOOLS,
        types.Tool(
            name="navigate_to_url",
            description="Navigate to a specific URL to start web automation.",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "URL to navigate to",
                    }
                },
                "required": ["url"],
            },
        ),
        types.Tool(
            name="execute_python_command",
            description=(
                EXECUTE_PYTHON_COMMAND_DESCRIPTION_VISION
                if mode == "vision-html"
                else EXECUTE_PYTHON_COMMAND_DESCRIPTION
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "Python command to execute",
                    }
                },
                "required": ["command"],
            },
        ),
    ]

    if mode == "vision-html":
        return [tool for tool in all_tools if tool.name in vision_html_tools]
    else:
        return all_tools
