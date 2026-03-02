"""Main API router combining all routes."""

from fastapi import APIRouter

from . import (
    health,
    agent,
    agents,
    analysis,
    auth,
    auth_github,
    automation,
    board,
    channels,
    db,
    files,
    graph,
    index,
    search,
    query,
    analyze,
    spec,
    tasks,
    plan,
    team,
    research,
    review,
    embed,
    rules,
    context,
    feature,
    projectmd,
    skills,
    stats,
    agent_teams,
    multiuser,
    registry,
    mcp,
    workflows,
)

api_router = APIRouter(prefix="/api")

# Health & status
api_router.include_router(health.router)

# Authentication
api_router.include_router(auth.router)
api_router.include_router(auth_github.router)

# Board persistence
api_router.include_router(board.router)

# Agent operations
api_router.include_router(agent.router)
api_router.include_router(agents.router)
api_router.include_router(skills.router)

# Database management
api_router.include_router(db.router)

# Graph queries (for MCP server proxy)
api_router.include_router(graph.router)

# Indexing
api_router.include_router(index.router)

# Search & queries
api_router.include_router(search.router)
api_router.include_router(query.router)

# Analytics
api_router.include_router(analyze.router)
api_router.include_router(analysis.router)

# Planning & specifications
api_router.include_router(spec.router)
api_router.include_router(tasks.router)
api_router.include_router(plan.router)
api_router.include_router(feature.router)

# Team & collaboration
api_router.include_router(team.router)
api_router.include_router(agent_teams.router)
api_router.include_router(research.router)
api_router.include_router(review.router)

# Embeddings
api_router.include_router(embed.router)

# Configuration
api_router.include_router(rules.router)
api_router.include_router(context.router)

# Documentation generation
api_router.include_router(projectmd.router)

# Statistics
api_router.include_router(stats.router)

# Multiuser collaboration
api_router.include_router(multiuser.router)

# File serving (artifacts)
api_router.include_router(files.router)

# Community registry
api_router.include_router(registry.router)

# MCP servers
api_router.include_router(mcp.router)

# Workflows
api_router.include_router(workflows.router)

# Channel management (Telegram, etc.)
api_router.include_router(channels.router)

# Automation (cron, heartbeat, webhooks)
api_router.include_router(automation.router)
api_router.include_router(automation.hooks_router)
