"""Tests for IssueProvider protocol compliance and verification."""

from __future__ import annotations

import ast
import inspect
from pathlib import Path

from agentic_devtools.adapters.issue_provider import (
    IssueProvider,
    ProviderIssueResult,
    ProviderLinkResult,
)


class _MockProvider:
    """Minimal IssueProvider implementation for protocol verification."""

    def create_issue(
        self, title, body, issue_type, *, parent_id=None, labels=None, idempotency_key=None, dry_run=False
    ):
        return ProviderIssueResult(identifier="1", url="http://x", status="created")

    def set_issue_type(self, identifier, issue_type, *, dry_run=False):
        return ProviderIssueResult(identifier=identifier, url="", status="updated", metadata={"issue_type": issue_type})

    def resolve_identifier(self, identifier, *, dry_run=False):
        return ProviderIssueResult(identifier=identifier, url="", status="resolved")

    def link_subissue(self, parent_id, child_id, *, dry_run=False):
        return ProviderLinkResult(source_id=parent_id, target_id=child_id, status="linked")

    def add_blocked_by(self, issue_id, blocked_by_id, *, dry_run=False):
        return ProviderLinkResult(source_id=blocked_by_id, target_id=issue_id, status="linked")

    def apply_labels(self, identifier, labels, *, dry_run=False):
        return ProviderIssueResult(identifier=identifier, url="", status="updated", metadata={"labels": labels})

    def normalize_identifier(self, identifier):
        return identifier.lstrip("#")

    def format_identifier(self, identifier):
        return f"#{identifier}" if not identifier.startswith("#") else identifier


class TestIssueProviderProtocol:
    """Verify that a conforming class satisfies the IssueProvider protocol."""

    def test_mock_provider_is_instance_of_protocol(self):
        provider = _MockProvider()
        assert isinstance(provider, IssueProvider)

    def test_create_issue_returns_provider_issue_result(self):
        provider = _MockProvider()
        result = provider.create_issue("title", "body", "task")
        assert isinstance(result, ProviderIssueResult)
        assert result.status == "created"

    def test_set_issue_type_returns_provider_issue_result(self):
        provider = _MockProvider()
        result = provider.set_issue_type("1", "bug")
        assert isinstance(result, ProviderIssueResult)
        assert result.status == "updated"

    def test_resolve_identifier_returns_provider_issue_result(self):
        provider = _MockProvider()
        result = provider.resolve_identifier("42")
        assert isinstance(result, ProviderIssueResult)
        assert result.status == "resolved"

    def test_link_subissue_returns_provider_link_result(self):
        provider = _MockProvider()
        result = provider.link_subissue("1", "2")
        assert isinstance(result, ProviderLinkResult)
        assert result.status == "linked"

    def test_add_blocked_by_returns_provider_link_result(self):
        provider = _MockProvider()
        result = provider.add_blocked_by("2", "1")
        assert isinstance(result, ProviderLinkResult)
        assert result.status == "linked"

    def test_apply_labels_returns_provider_issue_result(self):
        provider = _MockProvider()
        result = provider.apply_labels("1", ["bug"])
        assert isinstance(result, ProviderIssueResult)
        assert result.status == "updated"

    def test_normalize_identifier(self):
        provider = _MockProvider()
        assert provider.normalize_identifier("#42") == "42"

    def test_format_identifier(self):
        provider = _MockProvider()
        assert provider.format_identifier("42") == "#42"


class TestIssueProviderSC002NoProviderImports:
    """SC-002: Verify issue_provider.py has no provider-specific imports."""

    def test_no_provider_specific_imports(self):
        """Parse issue_provider.py with AST and assert no imports from provider-specific libraries."""
        source_path = Path(__file__).resolve().parents[4] / "agentic_devtools" / "adapters" / "issue_provider.py"
        source_code = source_path.read_text(encoding="utf-8")
        tree = ast.parse(source_code)

        forbidden_modules = {"jira", "github", "requests", "atlassian", "pygithub"}
        violations = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    root_module = alias.name.split(".")[0].lower()
                    if root_module in forbidden_modules:
                        violations.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    root_module = node.module.split(".")[0].lower()
                    if root_module in forbidden_modules:
                        violations.append(node.module)

        assert violations == [], f"Provider-specific imports found: {violations}"


class TestIssueProviderSC005DocstringCoverage:
    """SC-005: Verify all public classes and methods have docstrings."""

    def test_all_public_symbols_have_docstrings(self):
        """Every public class/method in issue_provider.py must have a docstring with ≥3 lines.

        Protocol methods (on IssueProvider) and class-level docstrings are
        checked for ≥3 lines.  Utility methods on dataclasses (e.g., to_dict)
        only require a non-empty docstring.
        """
        import agentic_devtools.adapters.issue_provider as mod

        public_classes = [
            name
            for name, obj in inspect.getmembers(mod, inspect.isclass)
            if not name.startswith("_") and obj.__module__ == mod.__name__
        ]

        protocol_methods = {
            "create_issue",
            "link_subissue",
            "add_blocked_by",
            "apply_labels",
            "set_issue_type",
            "resolve_identifier",
            "normalize_identifier",
            "format_identifier",
        }

        for cls_name in public_classes:
            cls = getattr(mod, cls_name)
            docstring = inspect.getdoc(cls)
            assert docstring is not None, f"{cls_name} has no docstring"
            assert len(docstring.strip().splitlines()) >= 3, f"{cls_name} docstring has fewer than 3 lines"

            for method_name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
                if method_name.startswith("_"):
                    continue
                method_doc = inspect.getdoc(method)
                assert method_doc is not None, f"{cls_name}.{method_name} has no docstring"
                # Protocol methods require ≥3 lines; utility methods just need a docstring
                if method_name in protocol_methods:
                    assert len(method_doc.strip().splitlines()) >= 3, (
                        f"{cls_name}.{method_name} docstring has fewer than 3 lines"
                    )


class TestIssueProviderSC006ReturnTypeConsistency:
    """SC-006: Verify protocol methods use structured result return types."""

    def test_protocol_methods_return_structured_results(self):
        """At least 6 of 8 protocol methods return ProviderIssueResult or ProviderLinkResult."""
        import typing

        # __protocol_attrs__ contains exactly the methods declared on IssueProvider,
        # excluding inherited helpers (like `register`) from typing.Protocol.
        method_names = sorted(IssueProvider.__protocol_attrs__)  # type: ignore[attr-defined]

        structured_count = 0
        for name in method_names:
            method = getattr(IssueProvider, name)
            method_hints = typing.get_type_hints(method)
            return_type = method_hints.get("return")
            if return_type in (ProviderIssueResult, ProviderLinkResult):
                structured_count += 1

        assert structured_count >= 6, (
            f"Only {structured_count} of {len(method_names)} protocol methods "
            f"return ProviderIssueResult or ProviderLinkResult (need ≥6)"
        )
