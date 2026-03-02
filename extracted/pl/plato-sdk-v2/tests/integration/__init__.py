"""Integration tests for the Plato agent framework.

These tests run full end-to-end scenarios with real Docker containers,
Plato sessions, and storage. They are NOT intended to run in CI.

Run locally with:
    pytest tests/integration/ -v -s

Requirements:
- Docker running locally
- PLATO_API_KEY environment variable set
- ANTHROPIC_API_KEY for OpenHands tests
"""
