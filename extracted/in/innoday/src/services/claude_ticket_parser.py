"""
Claude AI Service for Parsing Text into Structured Tickets

This service uses Claude to intelligently parse unstructured text
(like meeting notes, requirements, or conversations) into a structured
list of tickets with titles, descriptions, and metadata.
"""

import json
import logging
from typing import List, Optional

from pydantic import BaseModel, Field

from src.api.claude_api import ClaudeAPI

logger = logging.getLogger(__name__)


class ParsedTicket(BaseModel):
    """A single parsed ticket from Claude's analysis"""

    summary: str = Field(..., description="Brief title for the ticket (max 100 chars)")
    description: str = Field(..., description="Detailed description of the work")
    priority: Optional[str] = Field(
        None, description="Priority level: low, medium, high, critical"
    )
    labels: List[str] = Field(
        default_factory=list, description="Labels/tags for categorization"
    )
    assignee: Optional[str] = Field(
        None, description="Suggested assignee (name or handle)"
    )
    estimated_hours: Optional[float] = Field(
        None, description="Estimated hours to complete"
    )
    epic: Optional[str] = Field(
        None, description="Epic or parent ticket this belongs to"
    )
    release: Optional[str] = Field(None, description="Target release or sprint")
    acceptance_criteria: List[str] = Field(
        default_factory=list, description="Acceptance criteria/checklist"
    )
    dependencies: List[str] = Field(
        default_factory=list, description="Dependencies on other tickets"
    )


class TicketParseRequest(BaseModel):
    """Request to parse text into tickets"""

    text: str = Field(..., description="The text to parse into tickets")
    context: Optional[str] = Field(
        None,
        description="Additional context about the text (e.g., 'sprint planning meeting')",
    )
    board_type: Optional[str] = Field(
        None,
        description="Target board type (trello/jira) for platform-specific formatting",
    )
    default_labels: List[str] = Field(
        default_factory=list, description="Default labels to apply to all tickets"
    )
    default_assignee: Optional[str] = Field(
        None, description="Default assignee if not specified in text"
    )
    default_epic: Optional[str] = Field(
        None, description="Default epic to link tickets to"
    )
    max_tickets: int = Field(10, description="Maximum number of tickets to generate")


class TicketParseResponse(BaseModel):
    """Response from parsing text into tickets"""

    tickets: List[ParsedTicket]
    summary: str = Field(..., description="Brief summary of what was parsed")
    confidence: float = Field(..., description="Confidence score (0-1) in the parsing")
    notes: Optional[str] = Field(
        None, description="Any notes or warnings from the parsing"
    )


class ClaudeTicketParser:
    """Service for parsing text into structured tickets using Claude AI"""

    def __init__(self, organization_alias: Optional[str] = None):
        """
        Initialize the ticket parser service

        Args:
            organization_alias: Organization to get Claude credentials for
        """
        self.claude_api = ClaudeAPI(organization_alias=organization_alias)

    async def parse_text_to_tickets(
        self, request: TicketParseRequest
    ) -> TicketParseResponse:
        """
        Parse unstructured text into structured tickets using Claude

        Args:
            request: The parse request with text and options

        Returns:
            TicketParseResponse with parsed tickets
        """
        # Build the prompt for Claude
        prompt = self._build_parsing_prompt(request)

        # System message to guide Claude's behavior
        system_message = """You are an expert project manager and requirements analyst. 
Your task is to parse unstructured text (like meeting notes, conversations, or requirements documents) 
into well-structured tickets/tasks for project management boards.

You should:
1. Identify distinct work items that can be tracked as separate tickets
2. Write clear, actionable ticket titles (summaries)
3. Provide detailed descriptions with context
4. Suggest appropriate metadata (priority, labels, assignees) based on context
5. Extract acceptance criteria when mentioned
6. Identify dependencies between tickets
7. Group related tickets under epics when appropriate

Return your response as valid JSON matching the specified schema."""

        try:
            # Call Claude API with structured output
            response = await self.claude_api.generate_completion(
                prompt=prompt,
                system_prompt=system_message,
                max_tokens=4000,
                temperature=0.3,  # Lower temperature for more consistent parsing
            )

            # Parse Claude's response
            parsed_response = self._parse_claude_response(response, request)
            return parsed_response

        except Exception as e:
            logger.error(f"Error parsing text with Claude: {str(e)}")
            raise

    def _build_parsing_prompt(self, request: TicketParseRequest) -> str:
        """Build the prompt for Claude to parse tickets"""

        prompt_parts = [
            "Please parse the following text into structured tickets/tasks:"
        ]

        if request.context:
            prompt_parts.append(f"\nContext: {request.context}")

        if request.board_type:
            prompt_parts.append(f"Target board type: {request.board_type}")

        if request.default_labels:
            prompt_parts.append(
                f"Apply these labels to all tickets: {', '.join(request.default_labels)}"
            )

        if request.default_assignee:
            prompt_parts.append(f"Default assignee: {request.default_assignee}")

        if request.default_epic:
            prompt_parts.append(f"Parent epic: {request.default_epic}")

        prompt_parts.append(f"\nMaximum tickets to generate: {request.max_tickets}")

        prompt_parts.append(f"\n\nText to parse:\n{request.text}")

        prompt_parts.append("""

Please return a JSON response with this structure:
{
  "tickets": [
    {
      "summary": "Brief ticket title (max 100 chars)",
      "description": "Detailed description",
      "priority": "low|medium|high|critical",
      "labels": ["label1", "label2"],
      "assignee": "suggested assignee name",
      "estimated_hours": 8.0,
      "epic": "parent epic name",
      "release": "target release/sprint",
      "acceptance_criteria": ["criteria 1", "criteria 2"],
      "dependencies": ["depends on ticket X"]
    }
  ],
  "summary": "Brief summary of what was parsed",
  "confidence": 0.85,
  "notes": "Any warnings or notes about the parsing"
}""")

        return "\n".join(prompt_parts)

    def _parse_claude_response(
        self, claude_response: str, request: TicketParseRequest
    ) -> TicketParseResponse:
        """Parse Claude's response into structured tickets"""

        try:
            # Try to extract JSON from the response
            # Claude might include markdown code blocks
            if "```json" in claude_response:
                json_start = claude_response.find("```json") + 7
                json_end = claude_response.find("```", json_start)
                json_str = claude_response[json_start:json_end].strip()
            elif "```" in claude_response:
                json_start = claude_response.find("```") + 3
                json_end = claude_response.find("```", json_start)
                json_str = claude_response[json_start:json_end].strip()
            else:
                # Assume the entire response is JSON
                json_str = claude_response.strip()

            # Parse the JSON
            data = json.loads(json_str)

            # Convert to ParsedTicket objects
            tickets = []
            for ticket_data in data.get("tickets", [])[: request.max_tickets]:
                # Apply defaults if not specified
                if request.default_labels and "labels" in ticket_data:
                    ticket_data["labels"].extend(request.default_labels)
                elif request.default_labels:
                    ticket_data["labels"] = request.default_labels

                if not ticket_data.get("assignee") and request.default_assignee:
                    ticket_data["assignee"] = request.default_assignee

                if not ticket_data.get("epic") and request.default_epic:
                    ticket_data["epic"] = request.default_epic

                # Ensure required fields
                if "summary" not in ticket_data:
                    ticket_data["summary"] = "Untitled Ticket"
                if "description" not in ticket_data:
                    ticket_data["description"] = "No description provided"

                # Truncate summary if too long
                if len(ticket_data["summary"]) > 100:
                    ticket_data["summary"] = ticket_data["summary"][:97] + "..."

                tickets.append(ParsedTicket(**ticket_data))

            return TicketParseResponse(
                tickets=tickets,
                summary=data.get("summary", f"Parsed {len(tickets)} tickets from text"),
                confidence=data.get("confidence", 0.75),
                notes=data.get("notes"),
            )

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from Claude response: {e}")
            # Return a fallback response
            return TicketParseResponse(
                tickets=[],
                summary="Failed to parse tickets from text",
                confidence=0.0,
                notes=f"Error parsing Claude's response: {str(e)}",
            )
        except Exception as e:
            logger.error(f"Unexpected error parsing Claude response: {e}")
            raise

    async def enhance_ticket_description(
        self,
        summary: str,
        context: Optional[str] = None,
        board_type: Optional[str] = None,
    ) -> str:
        """
        Enhance a brief ticket summary into a detailed description

        Args:
            summary: Brief ticket title
            context: Additional context
            board_type: Target board type

        Returns:
            Enhanced description text
        """
        prompt = f"""Given this ticket summary: "{summary}"
        
{f"Context: {context}" if context else ""}
{f"Board type: {board_type}" if board_type else ""}

Please write a detailed ticket description that includes:
1. Clear explanation of what needs to be done
2. Why this is important (business value)
3. Technical considerations if applicable
4. Suggested implementation approach
5. Definition of done

Keep it concise but comprehensive."""

        try:
            response = await self.claude_api.generate_completion(
                prompt=prompt, max_tokens=1000, temperature=0.7
            )
            return response.strip()
        except Exception as e:
            logger.error(f"Error enhancing ticket description: {e}")
            return summary  # Fallback to original summary
