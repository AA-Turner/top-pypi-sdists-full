"""
Unified AI Router for Claude and AI-Powered Features

This module consolidates all AI-related endpoints including:
- Text parsing to tickets
- Conversation summarization
- Board analysis and summaries
- Temporal pattern analysis
- General Claude interactions

All endpoints follow the pattern: /api/v1/ai/...
"""

import logging
import random
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlmodel import Session, select

from src.api.claude_api import ClaudeAPI
from src.database import get_session
from src.domain.board import BoardRegistration
from src.domain.summary import Summary, SummaryType
from src.domain.ticket import Ticket
from src.domain.user import User
from src.middleware.rbac import get_current_user

# The one pool of quotes, owned by the boards router that has always written
# this column. Importing it keeps the two persisting paths from drifting apart.
from src.routers.boards import MOTIVATIONAL_QUOTES
from src.services.claude_ticket_parser import (
    ClaudeTicketParser,
    TicketParseRequest,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/ai", tags=["ai"])


# =============================================================================
# Request/Response Models
# =============================================================================


class TextParseRequest(BaseModel):
    """Request for parsing text into structured data"""

    text: str = Field(..., description="Text to parse")
    parse_type: str = Field("tickets", pattern="^(tickets|requirements|summary)$")
    context: Optional[str] = Field(None, description="Additional context")
    max_items: int = Field(10, ge=1, le=50, description="Maximum items to extract")
    organization_id: Optional[str] = Field(None, description="Organization context")


class ConversationMessage(BaseModel):
    """Single message in a conversation"""

    role: str = Field(..., pattern="^(user|assistant|system)$")
    content: str = Field(..., description="Message content")
    timestamp: Optional[datetime] = Field(None, description="Message timestamp")


class SummarizeRequest(BaseModel):
    """Request for summarizing content"""

    messages: List[ConversationMessage] = Field(
        ..., description="Messages to summarize"
    )
    summary_type: str = Field(
        "general", pattern="^(general|technical|executive|daily|sprint)$"
    )
    max_length: int = Field(500, ge=100, le=2000, description="Maximum summary length")
    include_action_items: bool = Field(True, description="Extract action items")


class AnalysisRequest(BaseModel):
    """Request for analyzing patterns or trends"""

    data: List[Dict[str, Any]] = Field(..., description="Data to analyze")
    analysis_type: str = Field(
        "temporal", pattern="^(temporal|sentiment|complexity|velocity)$"
    )
    time_window: Optional[str] = Field(None, description="Time window for analysis")
    group_by: Optional[str] = Field(None, description="Field to group analysis by")


class BoardSummaryRequest(BaseModel):
    """Request for summarizing a board's tickets"""

    board_id: str = Field(..., description="Board registration ID")
    summary_type: SummaryType = Field(SummaryType.STATUS, description="Type of summary")
    time_period: Optional[str] = Field(None, description="Time period to summarize")
    include_metrics: bool = Field(True, description="Include statistical metrics")
    tone: str = Field(
        "professional", pattern="^(professional|casual|motivational|technical)$"
    )


class AIResponse(BaseModel):
    """Standard response from AI operations"""

    success: bool = Field(..., description="Whether operation succeeded")
    result: Any = Field(..., description="Operation result")
    confidence: float = Field(..., ge=0, le=1, description="Confidence score")
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )
    usage: Optional[Dict[str, int]] = Field(None, description="Token usage statistics")


# =============================================================================
# Helper Functions
# =============================================================================


def get_motivational_message() -> str:
    """Get a random motivational message for summaries"""
    messages = [
        "🚀 Your team is making stellar progress!",
        "💪 Strong momentum detected in your workflow!",
        "🎯 Targets are being hit with precision!",
        "⚡ Lightning-fast progress on multiple fronts!",
        "🌟 Excellence is becoming a habit here!",
        "🏆 Championship-level teamwork in action!",
        "🔥 The productivity is off the charts!",
        "🎪 The greatest development show on Earth!",
        "🦸 Superhero-level problem solving detected!",
        "🎨 Masterpiece in the making!",
    ]
    return random.choice(messages)


# =============================================================================
# Text Parsing Endpoints
# =============================================================================


@router.post("/parse", response_model=AIResponse)
async def parse_text(
    request: TextParseRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Parse unstructured text into structured data using Claude AI.

    Supports parsing into:
    - Tickets: Extract actionable items with titles and descriptions
    - Requirements: Extract requirement statements
    - Summary: Create a structured summary
    """
    try:
        if request.parse_type == "tickets":
            # Use existing ticket parser
            parser = ClaudeTicketParser(
                organization_alias=request.organization_id or "default"
            )

            parse_request = TicketParseRequest(
                text=request.text,
                context=request.context,
                max_tickets=request.max_items,
            )

            response = await parser.parse_text_to_tickets(parse_request)

            return AIResponse(
                success=True,
                result={
                    "tickets": [t.model_dump() for t in response.tickets],
                    "summary": response.summary,
                    "notes": response.notes,
                },
                confidence=response.confidence,
                metadata={
                    "parse_type": "tickets",
                    "count": len(response.tickets),
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                },
            )

        elif request.parse_type == "requirements":
            # Parse requirements (simplified for now)
            claude_api = ClaudeAPI()

            prompt = f"""
            Extract requirement statements from the following text.
            Each requirement should be clear, testable, and actionable.
            
            Text: {request.text}
            
            Context: {request.context or "General requirements extraction"}
            
            Format as a list of requirement objects with:
            - id: Unique identifier (REQ-001, REQ-002, etc.)
            - statement: The requirement statement
            - priority: high/medium/low
            - category: functional/non-functional/technical
            """

            result = await claude_api.generate_response(
                prompt=prompt,
                max_tokens=2000,
            )

            return AIResponse(
                success=True,
                result=result,
                confidence=0.85,
                metadata={
                    "parse_type": "requirements",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                },
            )

        else:
            # General summary parsing
            claude_api = ClaudeAPI()

            result = await claude_api.summarize_text(
                text=request.text,
                max_length=request.max_items * 50,  # Rough estimate
            )

            return AIResponse(
                success=True,
                result=result,
                confidence=0.9,
                metadata={
                    "parse_type": "summary",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                },
            )

    except Exception as e:
        logger.error(f"Error parsing text: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to parse text: {str(e)}",
        )


# =============================================================================
# Summarization Endpoints
# =============================================================================


@router.post("/summarize", response_model=AIResponse)
async def summarize_content(
    request: SummarizeRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Summarize conversations or content using Claude AI.

    Supports different summary types:
    - General: Overall summary
    - Technical: Focus on technical details
    - Executive: High-level business summary
    - Daily: Daily standup format
    - Sprint: Sprint review format
    """
    try:
        claude_api = ClaudeAPI()

        # Convert messages to format expected by Claude API
        formatted_messages = [
            {"role": msg.role, "content": msg.content, "timestamp": msg.timestamp}
            for msg in request.messages
        ]

        # Generate summary based on type
        if request.summary_type == "daily":
            template = """
            Create a daily standup summary:
            1. What was accomplished
            2. What's planned for today
            3. Any blockers or concerns
            """
        elif request.summary_type == "sprint":
            template = """
            Create a sprint review summary:
            1. Sprint goals and achievements
            2. Velocity and metrics
            3. Challenges faced
            4. Improvements for next sprint
            """
        elif request.summary_type == "executive":
            template = """
            Create an executive summary:
            1. Key decisions and outcomes
            2. Business impact
            3. Resource requirements
            4. Next steps and timeline
            """
        else:
            template = "Create a clear, concise summary of the key points."

        result = await claude_api.summarize_conversation(
            messages=formatted_messages,
            max_length=request.max_length,
            include_action_items=request.include_action_items,
            template=template,
        )

        return AIResponse(
            success=True,
            result=result,
            confidence=0.9,
            metadata={
                "summary_type": request.summary_type,
                "message_count": len(request.messages),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        )

    except Exception as e:
        logger.error(f"Error summarizing content: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to summarize content: {str(e)}",
        )


# =============================================================================
# Analysis Endpoints
# =============================================================================


@router.post("/analyze", response_model=AIResponse)
async def analyze_patterns(
    request: AnalysisRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Analyze patterns and trends in data using Claude AI.

    Supports different analysis types:
    - Temporal: Time-based patterns
    - Sentiment: Emotional tone analysis
    - Complexity: Task complexity trends
    - Velocity: Work velocity patterns
    """
    try:
        claude_api = ClaudeAPI()

        # Prepare analysis based on type
        if request.analysis_type == "temporal":
            prompt = f"""
            Analyze temporal patterns in the following data:
            {request.data}
            
            Focus on:
            1. Time-based trends
            2. Recurring patterns
            3. Anomalies or outliers
            4. Predictions for future periods
            
            Time window: {request.time_window or "All available data"}
            Group by: {request.group_by or "No grouping"}
            """

        elif request.analysis_type == "velocity":
            prompt = f"""
            Analyze work velocity patterns in the following data:
            {request.data}
            
            Calculate and explain:
            1. Average velocity
            2. Velocity trends
            3. Factors affecting velocity
            4. Recommendations for improvement
            """

        else:
            prompt = f"""
            Perform {request.analysis_type} analysis on the following data:
            {request.data}
            
            Provide insights, patterns, and recommendations.
            """

        result = await claude_api.generate_response(
            prompt=prompt,
            max_tokens=1500,
        )

        return AIResponse(
            success=True,
            result=result,
            confidence=0.85,
            metadata={
                "analysis_type": request.analysis_type,
                "data_points": len(request.data),
                "time_window": request.time_window,
                "group_by": request.group_by,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        )

    except Exception as e:
        logger.error(f"Error analyzing patterns: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze patterns: {str(e)}",
        )


# =============================================================================
# Board Summary Endpoints
# =============================================================================


@router.post("/boards/summarize", response_model=AIResponse)
async def summarize_board(
    request: BoardSummaryRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Generate AI-powered summary of a board's tickets.

    Creates intelligent summaries with:
    - Status overview
    - Progress metrics
    - Team performance insights
    - Actionable recommendations
    """
    try:
        # Get board and verify it exists
        board = session.get(BoardRegistration, request.board_id)
        if not board:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Board not found",
            )

        # Get tickets for the board (exclude soft-deleted -- they must not
        # surface in the AI board summary).
        tickets = session.exec(
            select(Ticket)
            .where(Ticket.board_registration_id == request.board_id)
            .where(Ticket.organization_id == board.organization_id)
            .where(Ticket.deleted_at.is_(None))
        ).all()

        if not tickets:
            return AIResponse(
                success=True,
                result={
                    "summary": "No tickets found for this board.",
                    "metrics": {},
                },
                confidence=1.0,
                metadata={"ticket_count": 0},
            )

        # Prepare ticket data for Claude
        ticket_data = []
        status_counts = {}
        assignee_counts = {}

        for ticket in tickets:
            ticket_data.append(
                {
                    "id": ticket.id,
                    "summary": ticket.summary,
                    "description": ticket.description,
                    "status": ticket.status.value if ticket.status else "unknown",
                    "assignee": ticket.assignee,
                    "created": (
                        ticket.created_at.isoformat() if ticket.created_at else None
                    ),
                    "updated": (
                        ticket.updated_at.isoformat() if ticket.updated_at else None
                    ),
                }
            )

            # Count by status
            # NOTE: must not be named `status` -- that shadows the
            # `fastapi.status` module imported at the top of this file,
            # which is referenced later in this function's `except` block
            # (status.HTTP_500_INTERNAL_SERVER_ERROR). Shadowing it here
            # turned every error path after this loop into an unhandled
            # AttributeError instead of a clean HTTPException.
            ticket_status = ticket.status.value if ticket.status else "unknown"
            status_counts[ticket_status] = status_counts.get(ticket_status, 0) + 1

            # Count by assignee
            assignee = ticket.assignee or "unassigned"
            assignee_counts[assignee] = assignee_counts.get(assignee, 0) + 1

        # Generate summary with Claude
        claude_api = ClaudeAPI()

        if request.tone == "motivational":
            tone_instruction = "Use an encouraging, motivational tone with emojis."
            intro = get_motivational_message()
        elif request.tone == "casual":
            tone_instruction = "Use a friendly, casual tone."
            intro = "Hey team! Here's what's happening:"
        elif request.tone == "technical":
            tone_instruction = "Use a precise, technical tone focusing on metrics."
            intro = "Technical Analysis:"
        else:
            tone_instruction = "Use a professional, clear tone."
            intro = "Board Summary:"

        prompt = f"""
        Create a {request.summary_type.value} summary for a project board.
        
        Board: {board.board_name}
        Total Tickets: {len(tickets)}
        Status Distribution: {status_counts}
        Team Distribution: {assignee_counts}
        
        Ticket Details:
        {ticket_data[:20]}  # Limit to first 20 for context
        
        Instructions:
        - {tone_instruction}
        - Focus on {request.summary_type.value} aspects
        - Include key metrics and insights
        - Provide actionable recommendations
        - Keep it concise but informative
        
        Start with: {intro}
        """

        summary_text = await claude_api.generate_response(
            prompt=prompt,
            max_tokens=1000,
        )

        # Create and save summary record
        board_summary = Summary(
            board_registration_id=request.board_id,
            organization_id=board.organization_id,
            project_id=board.project_id,
            # The board-scoped sentinel: this route appends one summary per
            # call and has no window to key uniqueness on. See src/domain/summary.py.
            window_spec="",
            summary_type=request.summary_type,
            # Two separate reasons this insert used to fail, both of which had
            # to be fixed before the route could persist anything at all:
            # `summary_text=` matched no field on the model, so the prose was
            # never stored; and `motivational_quote` is NOT NULL, so omitting it
            # raised inside the `try` and the route answered 500.
            body_markdown=summary_text,
            motivational_quote=random.choice(MOTIVATIONAL_QUOTES),
            ticket_stats={
                "total": len(tickets),
                "by_status": status_counts,
                "by_assignee": assignee_counts,
            },
            created_by=current_user.id if current_user else None,
        )

        session.add(board_summary)
        session.commit()
        session.refresh(board_summary)

        return AIResponse(
            success=True,
            result={
                "summary_id": board_summary.id,
                "summary": summary_text,
                "metrics": (
                    board_summary.ticket_stats if request.include_metrics else {}
                ),
                "board_name": board.board_name,
            },
            confidence=0.9,
            metadata={
                "summary_type": request.summary_type.value,
                "tone": request.tone,
                "ticket_count": len(tickets),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        )

    except Exception as e:
        logger.error(f"Error summarizing board: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to summarize board: {str(e)}",
        )


# =============================================================================
# General Claude Interaction Endpoints
# =============================================================================


@router.post("/chat", response_model=AIResponse)
async def chat_with_claude(
    messages: List[ConversationMessage],
    max_tokens: int = Query(1000, ge=100, le=4000),
    temperature: float = Query(0.7, ge=0, le=1),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Have a general conversation with Claude AI.

    This endpoint allows direct interaction with Claude
    for general-purpose AI assistance.
    """
    try:
        claude_api = ClaudeAPI()

        # Convert messages to Claude format
        formatted_messages = [
            {"role": msg.role, "content": msg.content} for msg in messages
        ]

        response = await claude_api.chat(
            messages=formatted_messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )

        return AIResponse(
            success=True,
            result=response,
            confidence=0.95,
            metadata={
                "message_count": len(messages),
                "max_tokens": max_tokens,
                "temperature": temperature,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        )

    except Exception as e:
        logger.error(f"Error in Claude chat: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to communicate with Claude: {str(e)}",
        )


@router.get("/health")
async def check_ai_health():
    """
    Check if AI services are configured and accessible.

    Returns the health status of Claude API and related services.
    """
    try:
        claude_api = ClaudeAPI()
        is_configured = claude_api.is_configured()

        if is_configured:
            # Try a simple test request
            try:
                test_response = await claude_api.generate_response(
                    prompt="Say 'OK' if you're working.",
                    max_tokens=10,
                )
                is_healthy = bool(test_response)
            except Exception:
                is_healthy = False
        else:
            is_healthy = False

        return {
            "service": "ai",
            "status": "healthy" if is_healthy else "unhealthy",
            "configured": is_configured,
            "provider": "Claude (Anthropic)",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        return {
            "service": "ai",
            "status": "error",
            "configured": False,
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
