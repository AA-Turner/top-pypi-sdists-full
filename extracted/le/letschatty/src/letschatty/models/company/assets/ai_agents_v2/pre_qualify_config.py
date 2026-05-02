"""
Pre-qualification configuration for AI agents.

Defines the data collection, acceptance criteria, and destination actions
for qualifying/disqualifying users.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from enum import StrEnum
from letschatty.models.utils.types.identifier import StrObjectId


class PreQualifyDestination(StrEnum):
    """
    Destination/action when pre-qualification reaches a terminal state.
    """
    SUBSCRIBE_TO_LAUNCH = "subscribe_to_launch"  # Subscribe to launch + welcome kit
    CALENDAR_SCHEDULER = "calendar_scheduler"    # Allow AI agent to schedule meetings
    ESCALATE = "escalate"                        # Escalate to human
    CUSTOM_MESSAGE = "custom_message"            # Send a custom message
    CONTINUE = "continue"                        # Continue normal AI agent flow
    NONE = "none"                                # Do nothing


class PreQualifyFormField(BaseModel):
    """
    Form field reference with required flag.
    The required flag is specific to this pre-qualify config, not the form field itself.
    """
    field_key: str = Field(description="The field_key of the FormField")
    required: bool = Field(default=False, description="Whether this field is required for pre-qualification")


class PreQualifyConfig(BaseModel):
    """
    Configuration for pre-qualification process.
    Embedded in ChattyAIAgent.
    """
    # Form fields to collect (with required flag per field)
    form_fields: List[PreQualifyFormField] = Field(
        default_factory=list,
        description="List of form fields to collect with their required status"
    )

    # Acceptance criteria
    acceptance_criteria: str = Field(
        default="",
        description="Description of criteria for AI to evaluate if user qualifies. Empty = no criteria (auto-qualify on mandatory completion)"
    )

    # On qualified actions
    on_qualified_destination: PreQualifyDestination = Field(
        default=PreQualifyDestination.CONTINUE,
        description="Action when user qualifies"
    )
    on_qualified_message: Optional[str] = Field(
        default=None,
        description="Custom message to send when user qualifies (if destination is custom_message)"
    )

    # On unqualified actions
    on_unqualified_destination: PreQualifyDestination = Field(
        default=PreQualifyDestination.NONE,
        description="Action when user does NOT qualify"
    )
    on_unqualified_message: Optional[str] = Field(
        default=None,
        description="Custom message to send when user does NOT qualify (if destination is custom_message or escalate)"
    )

    @property
    def has_form_fields(self) -> bool:
        """Check if pre-qualify has form fields configured"""
        return len(self.form_fields) > 0

    @property
    def has_acceptance_criteria(self) -> bool:
        """Check if acceptance criteria is configured"""
        return bool(self.acceptance_criteria.strip())

    @property
    def is_configured(self) -> bool:
        """Check if pre-qualify is configured (has form fields)"""
        return self.has_form_fields

    def get_field_keys(self) -> List[str]:
        """Get list of all field_keys"""
        return [f.field_key for f in self.form_fields]

    def get_required_field_keys(self) -> List[str]:
        """Get list of required field_keys"""
        return [f.field_key for f in self.form_fields if f.required]

    def get_optional_field_keys(self) -> List[str]:
        """Get list of optional field_keys"""
        return [f.field_key for f in self.form_fields if not f.required]

    def is_field_required(self, field_key: str) -> bool:
        """Check if a specific field is required"""
        for f in self.form_fields:
            if f.field_key == field_key:
                return f.required
        return False

    def remove_field(self, field_key: str) -> bool:
        """Remove a field from the config. Returns True if field was found and removed."""
        original_len = len(self.form_fields)
        self.form_fields = [f for f in self.form_fields if f.field_key != field_key]
        return len(self.form_fields) < original_len
