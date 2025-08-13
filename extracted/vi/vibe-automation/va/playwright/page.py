import asyncio
from typing import Any, Dict, Optional, Callable, Union, Awaitable, Type
from os import environ
from dataclasses import dataclass
import logging
from pathlib import Path
from pydantic import BaseModel
from playwright._impl._element_handle import ElementHandle as ElementHandleImpl
from playwright._impl._locator import Locator as LocatorImpl
from playwright._impl._page import Page as PageImpl
from playwright.async_api._generated import (
    ElementHandle as ElementHandleAPI,
)
from playwright.async_api._generated import (
    Locator as LocatorAPI,
)
from playwright.async_api._generated import (
    Page as PageAPI,
)
from playwright.async_api import Page as PlaywrightPage
from playwright.sync_api import Route

from .checkpoint import default_checkpoint_callback
from .login import (
    _in_login_handler,
    _wait_for_login_wrapper,
    wait_for_login,
)
from .locator import PromptBasedLocator
from .orby.subtask_agent import perform_task
from .step import AsyncStepContextManager
from .web_agent import WebAgent

from ..agent.agent import Agent
from ..constants import REVIEW_TIMEOUT, VA_DISABLE_LOGIN_REVIEW, VA_ENABLE_SUBTASK_AGENT
from ..review import ReviewStatus, review
from .dom_utils import (
    inspect_element_recursive,
    normalize_locator_string,
)
from .warc_utils import parse_warc_file

log = logging.getLogger("va.playwright")


@dataclass
class ActResult:
    """Result of a Page.act operation."""

    success: bool
    message: str


@dataclass
class ExtractResult:
    """Result of a Page.extract operation."""

    # extraction can return a pydantic model or a string
    extraction: str | BaseModel | None
    success: bool
    message: str


@dataclass
class FormVerifyResult:
    """Result of a Page.verify_form_values operation."""

    form_match_expected: bool
    reason: str
    success: bool


# Monkey patch the Playwright Page implementation to add snapshotForAI method
async def _snapshot_for_ai(self, metadata: Optional[Dict[str, Any]] = None) -> str:
    """
    Take a snapshot of the page optimized for AI consumption.

    This method monkey-patches the missing snapshotForAI method from the server API
    into the Python Playwright Page class.

    Parameters:
    -----------
    metadata (Dict[str, Any], optional): Metadata for the snapshot operation

    Returns:
    --------
    str: A text-based accessibility snapshot of the page optimized for AI analysis
    """
    if metadata is None:
        metadata = {}

    # Call the server-side snapshotForAI method via the internal channel
    return await self._channel.send("snapshotForAI", None, {"metadata": metadata})


# Apply the monkey patch to both implementation and API classes
PageImpl.snapshot_for_ai = _snapshot_for_ai  # type: ignore


# Also add it to the API wrapper class
async def _api_snapshot_for_ai(self, metadata: Optional[Dict[str, Any]] = None) -> str:
    """API wrapper for snapshot_for_ai method."""
    return await self._impl_obj.snapshot_for_ai(metadata)


PageAPI.snapshot_for_ai = _api_snapshot_for_ai  # type: ignore


# Monkey patch the Playwright ElementHandle implementation to add generateLocatorString method
async def _element_generate_locator_string(self) -> Optional[str]:
    """
    Generate a locator string for the element handle.

    This method monkey-patches the missing generateLocatorString method from the server API
    into the Python Playwright ElementHandle class.

    Returns:
    --------
    Optional[str]: A locator string that can be used to locate the element, or None if not found
    """
    result = await self._channel.send("generateLocatorString", None)
    locator_string = result.get("value") if isinstance(result, dict) else result
    return (
        normalize_locator_string(locator_string) if locator_string else locator_string
    )


# Apply the monkey patch to ElementHandle classes
ElementHandleImpl._generate_locator_string = _element_generate_locator_string  # type: ignore


# Also add it to the API wrapper class
async def _api_element_generate_locator_string(self) -> Optional[str]:
    """API wrapper for _generate_locator_string method."""
    return await self._impl_obj._generate_locator_string()


ElementHandleAPI._generate_locator_string = _api_element_generate_locator_string  # type: ignore


# Monkey patch the Playwright Locator implementation to add generateLocatorString method
async def _generate_locator_string(self) -> Optional[str]:
    """
    Generate a locator string for the element.

    This method monkey-patches the missing generateLocatorString method from the server API
    into the Python Playwright Locator class.

    Returns:
    --------
    Optional[str]: A locator string that can be used to locate the element, or None if not found
    """

    async def task(handle, timeout):
        return await handle._generate_locator_string()

    return await self._with_element(task)


# Apply the monkey patch to both implementation and API classes
LocatorImpl.generate_locator_string = _generate_locator_string  # type: ignore


# Also add it to the API wrapper class
async def _api_generate_locator_string(self) -> Optional[str]:
    """API wrapper for generate_locator_string method."""
    return await self._impl_obj.generate_locator_string()


LocatorAPI.generate_locator_string = _api_generate_locator_string  # type: ignore


class Page:
    def __init__(self, page: PlaywrightPage):
        self._playwright_page = page
        self._login_handler = None
        self._agent = Agent()
        # Track any background login tasks (only for fallback case)
        self._current_login_task = None
        # WARC serving state
        self._warc_responses: Optional[Dict[str, Dict[str, Any]]] = None
        self._warc_route_handler = None
        # Checkpoint review configuration
        self._checkpoint_review_callback = None
        self._web_agent = WebAgent(self)  # type: ignore

        # Set longer navigation timeout (Playwright default is 3s)
        self._playwright_page.set_default_navigation_timeout(5000)  # Custom 5s timeout

        # Register default login handler upon page creation
        if not VA_DISABLE_LOGIN_REVIEW:
            self.on("login_required")

        # enable checkpoint review in test mode for all pages by default
        # See https://github.com/orby-ai-engineering/vibe-automation-server/pull/313/files
        is_test_run = "VA_TEST_RUN" in environ
        if is_test_run:
            log.info("Enabling checkpoint review under test run")
            self.enable_checkpoint_review()
        else:
            log.info("Checkpoint review is not enabled for the page")

    @wait_for_login
    def get_by_prompt(
        self,
        prompt: str,
    ) -> PromptBasedLocator:
        """
        Returns a PromptBasedLocator that can be used with or without fallback locators

        Parameters:
        -----------
        prompt (str): The natural language description of the element to locate.
        timeout (int) (optional): Timeout value in seconds for the connection with backend API service.
        wait_for_network_idle (bool) (optional): Whether to wait for network reaching full idle state before querying the page. If set to `False`, this method will only check for whether page has emitted [`load` event](https://developer.mozilla.org/en-US/docs/Web/API/Window/load_event).
        include_hidden (bool) (optional): Whether to include hidden elements on the page. Defaults to `True`.
        mode (ResponseMode) (optional): The response mode. Can be either `standard` or `fast`. Defaults to `fast`.
        experimental_query_elements_enabled (bool) (optional): Whether to use the experimental implementation of the query elements feature. Defaults to `False`.

        Returns:
        --------
        PromptBasedLocator: A locator that uses prompt-based element finding
        """
        return PromptBasedLocator(self, prompt)

    async def _check_login_and_handle(self, login_handler):
        """Check if login is required and handle it"""
        try:
            # Set context variable to prevent circular dependency during extract
            _in_login_handler.set(True)
            # Use extract() to get a text response
            result = await self.extract(
                "Is login required to access all the content on this page? Make sure to look for secure areas where login might be required or login pages. Answer with exactly 'yes' or 'no' (lowercase, no additional text)."
            )
            if result.extraction is None:
                log.info(
                    "Extract returned None for login check, assuming no login required"
                )
                answer = "no"
            else:
                answer = result.extraction.lower()
            if answer == "yes":
                log.info("Login required detected, calling handler")
                if login_handler:
                    log.info("Calling login handler")
                    # Always pass the page to the handler
                    if asyncio.iscoroutinefunction(login_handler):
                        await login_handler(self)
                    else:
                        login_handler(self)
                    log.info("Login handler completed")
                else:
                    log.warning("Login required but no handler available")
            else:
                log.info("No login required")
        except Exception as e:
            log.error(f"Error in login check: {e}")
            raise Exception(f"Login check failed: {e}") from e
        finally:
            # Reset context variable when done
            _in_login_handler.set(False)

    def enable_checkpoint_review(self, callback=None):
        """
        Enable checkpoint review for potentially destructive actions like form submissions and navigation.

        When enabled, the system will pause execution and create a review before performing
        actions that are likely to submit forms or navigate to different pages.

        Args:
            callback: Optional custom callback function that takes (command, intent_result, screenshot, code_context)
                     If not provided, uses default callback that creates a review and waits for completion.
        """
        self._checkpoint_review_callback = (
            callback if callback else default_checkpoint_callback
        )
        log.info("Checkpoint review enabled for this page")

    def disable_checkpoint_review(self):
        """Disable checkpoint review for this page."""
        self._checkpoint_review_callback = None
        log.info("Checkpoint review disabled for this page")

    def step(
        self,
        command: str,
        context: Optional[Dict[str, Any]] = None,
        max_retries: int = 16,
    ) -> AsyncStepContextManager:
        """
        Execute a natural language command by generating and running Python code.

        This method returns a context manager that can be used with 'async with'.
        The LLM action generation is only triggered if the with block is empty (contains only pass).

        To enable checkpoint reviews for form submissions and navigation, call page.enable_checkpoint_review() first.

        Parameters:
        -----------
        command (str): Natural language description of the action to perform
        context (Dict[str, Any], optional): Context variables available to the generated script
        max_retries (int): Maximum number of retry attempts. Defaults to 16.

        Returns:
        --------
        AsyncStepContextManager: Context manager for the step execution
        """
        if context is None:
            context = {}
        return AsyncStepContextManager(self, command, context, max_retries, self._agent)

    def _check_login_and_handle_on_page_load(self, *args, **kwargs):
        """Run the login handler if registered as a background task to block pending actions"""
        if self._login_handler:
            log.info("Page load detected, running login handler")
            self._current_login_task = asyncio.create_task(
                self._check_login_and_handle(self._login_handler)
            )
            self._current_login_task.add_done_callback(
                lambda t: setattr(self, "_current_login_task", None)
            )
        else:
            log.info("Page load detected but no login handler registered")

    async def _wait_for_login_task(self):
        """Wait for any background login task to complete"""
        if self._current_login_task:
            await self._current_login_task
            log.info("Background login task completed")

    def __getattr__(self, name):
        """Forward attribute lookups to the underlying Playwright page."""
        attr = getattr(self._playwright_page, name)

        # Only wrap callable attributes
        if not callable(attr):
            return attr

        # If we're in a login handler, return the method directly without waiting for login task
        if _in_login_handler.get(False):
            return attr

        return _wait_for_login_wrapper(self, attr, name)

    def on(
        self,
        event: str,
        handler: Optional[
            Union[Callable[[Any], None], Callable[[Any], Awaitable[None]]]
        ] = None,
    ):
        """
        Register event handler for page.

        For "login_required" event, if no handler is provided, uses the default login handler
        that starts a HITL review. For other events, a handler is required.

        Parameters:
        -----------
        event (str): The event to listen for
        handler (Optional[Union[...]], optional): The handler function to call when the event occurs.
                   Can be sync or async and will receive the page as a parameter.
                   If not provided for "login_required" event, uses the default login handler.

        Examples:
        ---------
        # Use default login handler (HITL review)
        page.on("login_required")

        # Use custom login handler
        page.on("login_required", custom_login_handler)

        # Other events require a handler
        page.on("page_event", page_event_handler)
        """
        if event == "login_required":
            # Use default handler if none provided
            if handler is None:
                handler = self.default_login_handler

            # Only add page load listener if we don't have a handler yet
            if self._login_handler is None:
                self._playwright_page.on(
                    "load", self._check_login_and_handle_on_page_load
                )
            # if handler is not the same as the existing handler, replace it
            if self._login_handler and handler != self._login_handler:
                log.info("Replacing existing login handler")
            self._login_handler = handler
        else:
            # For other events, handler is required
            if handler is None:
                raise ValueError(f"Handler is required for event '{event}'")
            self._playwright_page.on(event, handler)

    def remove_listener(
        self,
        event: str,
        handler: Optional[
            Union[Callable[[Any], None], Callable[[Any], Awaitable[None]]]
        ] = None,
    ):
        """
        Remove event handler for page. If the event is "login_required", we will remove the listener that checks if login is required on page loads.

        Parameters:
        -----------
        event (str): The event to remove listener for
        handler (Optional[Union[...]], optional): The handler function to remove.
                   Can be sync or async and will receive the page as a parameter.
        """
        if event == "login_required":
            self._playwright_page.remove_listener(
                "load", self._check_login_and_handle_on_page_load
            )
            self._login_handler = None
            log.info("Login handler removed")
        else:
            self._playwright_page.remove_listener(event, handler)

    async def default_login_handler(self, page):
        """Default login handler that starts HITL review"""
        r = review("review-for-login", "Please log in to continue.")
        await r.wait(REVIEW_TIMEOUT)  # 1000s timeout
        if r.status != ReviewStatus.READY:
            raise Exception("Login review not completed")

    @wait_for_login
    async def act(
        self, prompt: str, context: Optional[Dict[str, Any]] = None
    ) -> ActResult:
        """
        Execute a natural language action on the page.

        Parameters:
        -----------
        prompt (str): Natural language description of the action to perform
        context (Dict[str, Any], optional): Context variables available to the generated script

        Returns:
        --------
        ActResult: Result with success status and message
        """
        try:
            if VA_ENABLE_SUBTASK_AGENT:
                print(f"Using Orby ActIO subtask agent to perform page.act('{prompt}')")
                await perform_task(self, prompt)
                result = {
                    "success": True,
                    "message": "Action successfully executed",
                }
            else:
                # Create a web agent for this page
                web_agent = WebAgent(self)

                # Use provided context or empty dict
                if context is None:
                    context = {}

                # Execute the action using the web agent (use the newly created one!)
                result = await web_agent.execute_interactive_step(prompt, context)

            # Return ActResult based on the web agent's result
            return ActResult(success=result["success"], message=result["message"])

        except Exception as e:
            log.error(f"Error executing act command '{prompt}': {e}")
            return ActResult(
                success=False, message=f"Error executing command: {str(e)}"
            )

    @wait_for_login
    async def extract(
        self,
        prompt: str,
        schema: Optional[Type[BaseModel]] = None,
        include_snapshot: bool = True,
        include_screenshot: bool = False,
    ) -> ExtractResult:
        """
        Extract data from the page using natural language. By detault, it uses snapshot only.

        Parameters:
        -----------
        prompt (str): Natural language description of what to extract
        schema (Optional[Type[BaseModel]]): Schema for structured extraction
        include_snapshot (bool): Whether to include DOM/accessibility tree snapshot (default: True)
        include_screenshot (bool): Whether to include screenshot for visual analysis (default: False)

        Returns:
        --------
        ExtractResult: Result with extraction, success status, and message
        """
        # TODO: Currently, we take full-page screenshots. This has limitations on scrollable iframes and when fields are blocked by other elements.
        # Not urgent for now, but we should consider better screenshot strategies if we rely on screenshots more.
        try:
            if include_snapshot and include_screenshot:
                # Use regular extract with screenshot
                result = await self._web_agent.extract(
                    prompt, schema, include_screenshot=True
                )
            elif include_snapshot and not include_screenshot:
                # Use regular extract without screenshot
                result = await self._web_agent.extract(
                    prompt, schema, include_screenshot=False
                )
            elif not include_snapshot and include_screenshot:
                # Use vision-only extract
                result = await self._web_agent.extract_vision_only(prompt, schema)
            else:
                # Neither snapshot nor screenshot - this is invalid
                raise ValueError(
                    "At least one of include_snapshot or include_screenshot must be True"
                )

            # Return ExtractResult based on the web agent's result
            return ExtractResult(extraction=result, success=True, message="")
        except Exception as e:
            log.error(f"Error in extract: {e}")
            return ExtractResult(
                extraction=None, success=False, message=f"Error in extract: {e}"
            )

    @wait_for_login
    async def inspect_element(self, x: int, y: int, num_ancestors: int = 3) -> str:
        """
        Inspect an element by coordinates.

        This method handles both regular elements and elements within iframes,
        including nested iframes and cross-origin iframes by using Playwright's frame API.

        Cross-origin iframe behavior:
        - Uses Playwright's frame API to bypass browser same-origin policy restrictions
        - Coordinates are automatically translated from main page to iframe coordinate system
        - Falls back to inspecting the iframe element itself if the frame cannot be accessed
        - Supports both same-origin and cross-origin iframes seamlessly
        - Recursively handles nested iframes (iframe inside iframe)

        Args:
            x: X coordinate of the element
            y: Y coordinate of the element
            num_ancestors: Number of ancestors to inspect (default: 3)

        Returns:
            A condensed path representation of the element and its container
        """
        return await inspect_element_recursive(
            self._playwright_page, x, y, num_ancestors, mode="element"
        )

    @wait_for_login
    async def inspect_html(
        self, x: int, y: int, num_ancestors: int = 3, max_characters: int = 1024
    ) -> str:
        """
        Inspect an element by coordinates and return raw HTML like Chrome DevTools.

        This method handles both regular elements and elements within iframes,
        including nested iframes and cross-origin iframes by using Playwright's frame API.

        Cross-origin iframe behavior:
        - Uses Playwright's frame API to bypass browser same-origin policy restrictions
        - Coordinates are automatically translated from main page to iframe coordinate system
        - Falls back to inspecting the iframe element itself if the frame cannot be accessed
        - Supports both same-origin and cross-origin iframes seamlessly
        - Recursively handles nested iframes (iframe inside iframe)

        Args:
            x: X coordinate of the element
            y: Y coordinate of the element
            num_ancestors: Number of ancestors to inspect (default: 3)
            max_characters: Maximum characters in response.

        Returns:
            Raw HTML content of the element and its container, formatted like Chrome DevTools
        """
        return await inspect_element_recursive(
            self._playwright_page,
            x,
            y,
            num_ancestors,
            mode="html",
            max_characters=max_characters,
        )

    @wait_for_login
    async def serve_from_warc(
        self, warc_file_path: Path, fallback_to_live: bool = False
    ):
        """
        Configure the page to serve responses from a WARC file.
        Args:
            warc_file_path: Path to the WARC file
            fallback_to_live: If True, fall back to live requests for URLs not in WARC.
                             If False, return 404 for missing URLs.
        """
        # Parse the WARC file
        self._warc_responses = parse_warc_file(warc_file_path)

        # Set up request interception
        async def warc_route_handler(route: Route):
            request_url = route.request.url

            # Check if URL exists in WARC
            if self._warc_responses and request_url in self._warc_responses:
                warc_response = self._warc_responses[request_url]
                await route.fulfill(
                    status=warc_response["status"],
                    headers=warc_response["headers"],
                    body=warc_response["body"],
                )
            elif fallback_to_live:
                # Allow live request
                await route.continue_()
            else:
                # Abort request for URLs not in WARC (follows Playwright default behavior)
                await route.abort("failed")

        # Store handler reference for cleanup
        self._warc_route_handler = warc_route_handler

        # Register the route handler
        await self.route("**/*", warc_route_handler)

    @wait_for_login
    async def clear_warc_serving(self):
        """Clear WARC serving configuration and remove route handler."""
        if self._warc_route_handler:
            await self.unroute("**/*", self._warc_route_handler)
            self._warc_route_handler = None
            self._warc_responses = None

    @wait_for_login
    async def get_page_snapshot(self):
        return await self.snapshot_for_ai()

    @wait_for_login
    async def verify_form_values(self, expected_form_data: str) -> FormVerifyResult:
        try:
            result = await self._web_agent.verify_form_values(expected_form_data)
            return FormVerifyResult(
                form_match_expected=result.form_match_expected,
                reason=result.reason,
                success=True,
            )
        except Exception as e:
            log.error(f"Error in verify_form_values: {e}")
            return FormVerifyResult(
                form_match_expected=False,
                reason=f"Error in verify_form_values: {e}",
                success=False,
            )
