"""
Configuration for browser-use tracing.
"""

import os
from dataclasses import dataclass, field
from typing import Any


@dataclass
class BrowserUseConfig:
    """Configuration for browser-use tracing behavior.

    Attributes:
        trace_screenshots: Whether to capture screenshots as span attachments
        trace_dom: Whether to capture DOM snapshots (can be large)
        trace_browser_actions: Whether to trace individual browser actions
        trace_llm_calls: Whether to trace LLM calls
        trace_agent_steps: Whether to trace each agent step
        compress_screenshots: Whether to compress screenshot images
        screenshot_quality: JPEG quality for screenshots (1-100)
        max_screenshot_size: Maximum screenshot size in bytes before downscaling
        include_action_selectors: Whether to include CSS selectors in action spans
        mask_sensitive_data: Whether to mask potentially sensitive data in traces
        action_timeout: Timeout in seconds for browser actions
        llm_timeout: Timeout in seconds for LLM calls
        step_timeout: Timeout in seconds for agent steps
        max_retries: Maximum number of retries for failed operations
        retry_delay: Initial delay between retries in seconds (exponential backoff)
        retry_on_errors: List of error types to retry on (empty = retry all)
    """

    # Tracing toggles
    trace_screenshots: bool = True
    trace_dom: bool = False
    trace_browser_actions: bool = True
    trace_llm_calls: bool = True
    trace_agent_steps: bool = True

    # Screenshot settings
    compress_screenshots: bool = True
    screenshot_quality: int = 80
    max_screenshot_size: int = 500_000  # 500KB

    # Action tracing
    include_action_selectors: bool = True

    # Privacy
    mask_sensitive_data: bool = False

    # Span naming
    span_prefix: str = "browser_use"

    # Timeout settings (in seconds)
    action_timeout: float = 30.0  # 30 seconds for browser actions
    llm_timeout: float = 120.0  # 2 minutes for LLM calls
    step_timeout: float = 300.0  # 5 minutes for agent steps

    # Retry settings
    max_retries: int = 3
    retry_delay: float = 1.0  # Initial delay, doubles each retry
    retry_on_errors: list = field(default_factory=list)  # Empty = retry all transient errors

    # Metadata
    default_tags: dict[str, str] = field(default_factory=dict)
    default_metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate configuration."""
        if not 1 <= self.screenshot_quality <= 100:
            raise ValueError("screenshot_quality must be between 1 and 100")
        if self.max_screenshot_size < 10_000:
            raise ValueError("max_screenshot_size must be at least 10KB")
        if self.action_timeout <= 0:
            raise ValueError("action_timeout must be positive")
        if self.llm_timeout <= 0:
            raise ValueError("llm_timeout must be positive")
        if self.step_timeout <= 0:
            raise ValueError("step_timeout must be positive")
        if self.max_retries < 0:
            raise ValueError("max_retries must be non-negative")
        if self.retry_delay < 0:
            raise ValueError("retry_delay must be non-negative")

    @classmethod
    def from_env(cls) -> "BrowserUseConfig":
        """
        Create configuration from environment variables.

        Environment variables:
            AIGIE_BROWSER_USE_TRACE_SCREENSHOTS: Capture screenshots (default: true)
            AIGIE_BROWSER_USE_TRACE_DOM: Capture DOM snapshots (default: false)
            AIGIE_BROWSER_USE_TRACE_ACTIONS: Trace browser actions (default: true)
            AIGIE_BROWSER_USE_TRACE_LLM: Trace LLM calls (default: true)
            AIGIE_BROWSER_USE_TRACE_STEPS: Trace agent steps (default: true)
            AIGIE_BROWSER_USE_COMPRESS_SCREENSHOTS: Compress screenshots (default: true)
            AIGIE_BROWSER_USE_SCREENSHOT_QUALITY: Screenshot quality 1-100 (default: 80)
            AIGIE_BROWSER_USE_MAX_SCREENSHOT_SIZE: Max screenshot size in bytes (default: 500000)
            AIGIE_BROWSER_USE_INCLUDE_SELECTORS: Include CSS selectors (default: true)
            AIGIE_BROWSER_USE_MASK_SENSITIVE: Mask sensitive data (default: false)
            AIGIE_BROWSER_USE_ACTION_TIMEOUT: Action timeout in seconds (default: 30)
            AIGIE_BROWSER_USE_LLM_TIMEOUT: LLM timeout in seconds (default: 120)
            AIGIE_BROWSER_USE_STEP_TIMEOUT: Step timeout in seconds (default: 300)
            AIGIE_BROWSER_USE_MAX_RETRIES: Max retry attempts (default: 3)
            AIGIE_BROWSER_USE_RETRY_DELAY: Initial retry delay in seconds (default: 1.0)
        """
        return cls(
            trace_screenshots=os.getenv("AIGIE_BROWSER_USE_TRACE_SCREENSHOTS", "true").lower()
            == "true",
            trace_dom=os.getenv("AIGIE_BROWSER_USE_TRACE_DOM", "false").lower() == "true",
            trace_browser_actions=os.getenv("AIGIE_BROWSER_USE_TRACE_ACTIONS", "true").lower()
            == "true",
            trace_llm_calls=os.getenv("AIGIE_BROWSER_USE_TRACE_LLM", "true").lower() == "true",
            trace_agent_steps=os.getenv("AIGIE_BROWSER_USE_TRACE_STEPS", "true").lower() == "true",
            compress_screenshots=os.getenv("AIGIE_BROWSER_USE_COMPRESS_SCREENSHOTS", "true").lower()
            == "true",
            screenshot_quality=int(os.getenv("AIGIE_BROWSER_USE_SCREENSHOT_QUALITY", "80")),
            max_screenshot_size=int(os.getenv("AIGIE_BROWSER_USE_MAX_SCREENSHOT_SIZE", "500000")),
            include_action_selectors=os.getenv(
                "AIGIE_BROWSER_USE_INCLUDE_SELECTORS", "true"
            ).lower()
            == "true",
            mask_sensitive_data=os.getenv("AIGIE_BROWSER_USE_MASK_SENSITIVE", "false").lower()
            == "true",
            action_timeout=float(os.getenv("AIGIE_BROWSER_USE_ACTION_TIMEOUT", "30.0")),
            llm_timeout=float(os.getenv("AIGIE_BROWSER_USE_LLM_TIMEOUT", "120.0")),
            step_timeout=float(os.getenv("AIGIE_BROWSER_USE_STEP_TIMEOUT", "300.0")),
            max_retries=int(os.getenv("AIGIE_BROWSER_USE_MAX_RETRIES", "3")),
            retry_delay=float(os.getenv("AIGIE_BROWSER_USE_RETRY_DELAY", "1.0")),
        )

    def merge(self, **overrides) -> "BrowserUseConfig":
        """
        Create a new config with overridden values.

        Args:
            **overrides: Values to override

        Returns:
            New BrowserUseConfig with overrides applied
        """
        return BrowserUseConfig(
            trace_screenshots=overrides.get("trace_screenshots", self.trace_screenshots),
            trace_dom=overrides.get("trace_dom", self.trace_dom),
            trace_browser_actions=overrides.get(
                "trace_browser_actions", self.trace_browser_actions
            ),
            trace_llm_calls=overrides.get("trace_llm_calls", self.trace_llm_calls),
            trace_agent_steps=overrides.get("trace_agent_steps", self.trace_agent_steps),
            compress_screenshots=overrides.get("compress_screenshots", self.compress_screenshots),
            screenshot_quality=overrides.get("screenshot_quality", self.screenshot_quality),
            max_screenshot_size=overrides.get("max_screenshot_size", self.max_screenshot_size),
            include_action_selectors=overrides.get(
                "include_action_selectors", self.include_action_selectors
            ),
            mask_sensitive_data=overrides.get("mask_sensitive_data", self.mask_sensitive_data),
            span_prefix=overrides.get("span_prefix", self.span_prefix),
            action_timeout=overrides.get("action_timeout", self.action_timeout),
            llm_timeout=overrides.get("llm_timeout", self.llm_timeout),
            step_timeout=overrides.get("step_timeout", self.step_timeout),
            max_retries=overrides.get("max_retries", self.max_retries),
            retry_delay=overrides.get("retry_delay", self.retry_delay),
            retry_on_errors=overrides.get("retry_on_errors", self.retry_on_errors),
            default_tags=overrides.get("default_tags", self.default_tags),
            default_metadata=overrides.get("default_metadata", self.default_metadata),
        )
