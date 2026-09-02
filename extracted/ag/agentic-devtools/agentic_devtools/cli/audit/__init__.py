"""Audit module for batch PR review analysis and instruction updates.

Provides CLI commands for the two-phase audit workflow:
1. ``agdt-audit-prepare`` — deterministic batch data collection
2. ``agdt-audit-dispatch-evaluation`` — tracking issue + branch push + coding-agent assignment
3. ``agdt-audit-apply`` — apply agent evaluation results
4. ``agdt-audit-takeover-eval-prs`` — reclaim Copilot eval PRs under a human identity
5. ``agdt-audit-on-pr-close`` — threshold check and dispatch trigger
"""
