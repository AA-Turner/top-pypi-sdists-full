"""
Configuration for Instructor integration.
"""

import os
from dataclasses import dataclass


@dataclass
class InstructorConfig:
    """
    Configuration for Instructor integration.

    Attributes:
        enabled: Whether tracing is enabled
        capture_schemas: Whether to capture Pydantic model schemas
        capture_outputs: Whether to capture structured outputs
        capture_retries: Whether to capture validation retry details
        max_output_length: Maximum length of captured outputs
    """

    enabled: bool = True
    capture_schemas: bool = True
    capture_outputs: bool = True
    capture_retries: bool = True
    max_output_length: int = 2000

    @classmethod
    def from_env(cls) -> "InstructorConfig":
        """
        Create configuration from environment variables.

        Environment variables:
            AIGIE_INSTRUCTOR_ENABLED: Enable/disable tracing (default: true)
            AIGIE_INSTRUCTOR_CAPTURE_SCHEMAS: Capture schemas (default: true)
            AIGIE_INSTRUCTOR_CAPTURE_OUTPUTS: Capture outputs (default: true)
            AIGIE_INSTRUCTOR_CAPTURE_RETRIES: Capture retries (default: true)
            AIGIE_INSTRUCTOR_MAX_OUTPUT_LENGTH: Max output length (default: 2000)
        """
        return cls(
            enabled=os.getenv("AIGIE_INSTRUCTOR_ENABLED", "true").lower() == "true",
            capture_schemas=os.getenv("AIGIE_INSTRUCTOR_CAPTURE_SCHEMAS", "true").lower() == "true",
            capture_outputs=os.getenv("AIGIE_INSTRUCTOR_CAPTURE_OUTPUTS", "true").lower() == "true",
            capture_retries=os.getenv("AIGIE_INSTRUCTOR_CAPTURE_RETRIES", "true").lower() == "true",
            max_output_length=int(os.getenv("AIGIE_INSTRUCTOR_MAX_OUTPUT_LENGTH", "2000")),
        )
