# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Slack operations: Block Kit construction, validation, and message formatting.

This package provides utilities for building well-formatted Slack messages
using Block Kit. It handles markdown-to-Block-Kit translation, content
validation (rejecting Slack-incompatible patterns like tables), and
block construction using the official `slack_sdk` models.

Modules:
    `blocks` — Block Kit block building and validation
"""
