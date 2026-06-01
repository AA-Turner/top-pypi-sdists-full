"""
Configuration for Semantic Kernel integration.
"""

import os
from dataclasses import dataclass


@dataclass
class SemanticKernelConfig:
    """
    Configuration for Semantic Kernel integration.

    Attributes:
        enabled: Whether tracing is enabled
        capture_function_results: Whether to capture function results
        capture_plan_details: Whether to capture planner details
        capture_prompts: Whether to capture rendered prompts
        max_result_length: Maximum length of captured results
    """

    enabled: bool = True
    capture_function_results: bool = True
    capture_plan_details: bool = True
    capture_prompts: bool = True
    max_result_length: int = 2000

    @classmethod
    def from_env(cls) -> "SemanticKernelConfig":
        """
        Create configuration from environment variables.

        Environment variables:
            AIGIE_SK_ENABLED: Enable/disable tracing (default: true)
            AIGIE_SK_CAPTURE_RESULTS: Capture function results (default: true)
            AIGIE_SK_CAPTURE_PLANS: Capture plan details (default: true)
            AIGIE_SK_CAPTURE_PROMPTS: Capture prompts (default: true)
            AIGIE_SK_MAX_RESULT_LENGTH: Max result length (default: 2000)
        """
        return cls(
            enabled=os.getenv("AIGIE_SK_ENABLED", "true").lower() == "true",
            capture_function_results=os.getenv("AIGIE_SK_CAPTURE_RESULTS", "true").lower()
            == "true",
            capture_plan_details=os.getenv("AIGIE_SK_CAPTURE_PLANS", "true").lower() == "true",
            capture_prompts=os.getenv("AIGIE_SK_CAPTURE_PROMPTS", "true").lower() == "true",
            max_result_length=int(os.getenv("AIGIE_SK_MAX_RESULT_LENGTH", "2000")),
        )
