# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Agent Message Bus: webhook relay service for Devin sessions.

This package implements a Cloud Run FastAPI service that receives GitHub and Slack
webhooks and relays notifications to subscribed Devin sessions via the Devin API.

Components:
- `app`: FastAPI application with webhook and subscription endpoints
- `models`: Pydantic models for subscriptions and API requests/responses
- `firestore`: Firestore client for subscription state management
- `github_handler`: GitHub webhook event processing
- `slack_handler`: Slack Block Kit interaction processing
- `devin_client`: Devin API client for session message injection
"""
