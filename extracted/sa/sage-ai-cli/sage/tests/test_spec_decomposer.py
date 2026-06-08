"""Tests for the spec_decomposer module.

The decomposer is the entry point of the new dynamic builder pipeline.
It takes a free-form task description and produces a `ProjectPlan` with
explicit features and a stack profile, both derived from the spec via
the LLM (with deterministic fallback for malformed output).
"""

from __future__ import annotations

import json
from typing import Callable

import pytest

from sage.core.spec_decomposer import (
    Feature,
    ProjectPlan,
    StackProfile,
    decompose_spec,
    extract_features,
    extract_stack,
    parse_features_json,
    parse_stack_json,
)


def _stub_gen(responses: list[str]) -> Callable[[str], str]:
    """Return a generate() stub that returns each response in order."""
    iterator = iter(responses)

    def fn(prompt: str) -> str:
        try:
            return next(iterator)
        except StopIteration:
            return ""

    return fn


# ────────────────────────────── parse helpers ────────────────────────────


class TestParseFeaturesJson:
    def test_parses_valid_json_array(self) -> None:
        raw = json.dumps(
            [
                {
                    "name": "auth",
                    "description": "User signup/login with JWT",
                    "layer": "backend",
                    "acceptance": ["POST /auth/login returns JWT", "Tokens expire after 24h"],
                },
                {
                    "name": "dashboard",
                    "description": "Campaign metrics view",
                    "layer": "frontend",
                    "acceptance": ["Renders KPI cards", "Filters by date range"],
                },
            ]
        )
        features = parse_features_json(raw)
        assert len(features) == 2
        assert features[0].name == "auth"
        assert features[0].layer == "backend"
        assert "POST /auth/login" in features[0].acceptance[0]
        assert features[1].layer == "frontend"

    def test_extracts_json_from_prose_wrapping(self) -> None:
        raw = (
            "Sure, here are the features:\n\n```json\n"
            + json.dumps(
                [{"name": "x", "description": "y", "layer": "backend", "acceptance": ["z"]}]
            )
            + "\n```\n\nLet me know if you want more."
        )
        features = parse_features_json(raw)
        assert len(features) == 1
        assert features[0].name == "x"

    def test_returns_empty_list_on_garbage(self) -> None:
        assert parse_features_json("not json at all") == []
        assert parse_features_json("") == []
        assert parse_features_json("{}") == []

    def test_normalises_invalid_layer(self) -> None:
        raw = json.dumps(
            [{"name": "a", "description": "b", "layer": "middleware", "acceptance": ["c"]}]
        )
        features = parse_features_json(raw)
        # Unknown layer defaults to "backend" rather than crashing.
        assert features[0].layer == "backend"

    def test_normalises_missing_acceptance(self) -> None:
        raw = json.dumps([{"name": "a", "description": "b", "layer": "frontend"}])
        features = parse_features_json(raw)
        assert features[0].acceptance == []

    def test_skips_entry_missing_name(self) -> None:
        raw = json.dumps(
            [
                {"description": "no name", "layer": "backend", "acceptance": []},
                {"name": "good", "description": "ok", "layer": "backend", "acceptance": []},
            ]
        )
        features = parse_features_json(raw)
        assert len(features) == 1
        assert features[0].name == "good"

    def test_slugifies_name(self) -> None:
        raw = json.dumps(
            [{"name": "Campaign Builder!", "description": "x", "layer": "backend", "acceptance": []}]
        )
        features = parse_features_json(raw)
        assert features[0].name == "campaign_builder"


class TestParseStackJson:
    def test_parses_valid_stack(self) -> None:
        raw = json.dumps(
            {
                "frontend": "react-native-web",
                "backend": "fastapi",
                "database": "postgres",
                "cache": "redis",
            }
        )
        s = parse_stack_json(raw)
        assert s.frontend == "react-native-web"
        assert s.backend == "fastapi"
        assert s.database == "postgres"
        assert s.cache == "redis"

    def test_returns_defaults_on_garbage(self) -> None:
        s = parse_stack_json("not json")
        # Defaults make the rest of the pipeline runnable without crashing
        assert s.frontend is None
        assert s.backend is None

    def test_handles_partial_stack(self) -> None:
        raw = json.dumps({"backend": "fastapi"})
        s = parse_stack_json(raw)
        assert s.backend == "fastapi"
        assert s.frontend is None


# ────────────────────────────── extract features ─────────────────────────


class TestExtractFeatures:
    def test_extracts_features_from_llm(self) -> None:
        raw = json.dumps(
            [
                {"name": "login", "description": "x", "layer": "frontend", "acceptance": ["a"]},
                {"name": "campaigns", "description": "y", "layer": "backend", "acceptance": ["b"]},
            ]
        )
        features = extract_features("build login + campaigns", _stub_gen([raw]))
        assert len(features) == 2

    def test_retries_on_malformed_json(self) -> None:
        good = json.dumps(
            [{"name": "ok", "description": "x", "layer": "backend", "acceptance": []}]
        )
        features = extract_features("task", _stub_gen(["broken {", "still broken", good]))
        assert len(features) == 1
        assert features[0].name == "ok"

    def test_falls_back_to_keyword_extraction_when_llm_fails(self) -> None:
        # All retries return garbage → fall back to keyword features
        features = extract_features(
            "Build an app with login, registration, and a dashboard",
            _stub_gen(["", "", "", ""]),
        )
        # Keyword fallback must produce SOMETHING so the pipeline never aborts
        assert len(features) >= 1


class TestExtractStack:
    def test_extracts_stack_from_llm(self) -> None:
        raw = json.dumps({"frontend": "react", "backend": "fastapi"})
        s = extract_stack("build x", _stub_gen([raw]))
        assert s.frontend == "react"
        assert s.backend == "fastapi"

    def test_falls_back_to_heuristic_detection(self) -> None:
        # LLM returns garbage → falls back to keyword stack detection
        s = extract_stack(
            "Build a FastAPI backend with React Native frontend",
            _stub_gen(["", "", ""]),
        )
        assert s.backend == "fastapi"
        assert s.frontend == "react-native-web"


class TestDecomposeSpec:
    def test_returns_full_plan(self) -> None:
        features_raw = json.dumps(
            [{"name": "auth", "description": "x", "layer": "backend", "acceptance": ["a"]}]
        )
        stack_raw = json.dumps({"frontend": "react", "backend": "fastapi"})
        plan = decompose_spec(
            "build auth with fastapi + react",
            _stub_gen([features_raw, stack_raw]),
        )
        assert isinstance(plan, ProjectPlan)
        assert len(plan.features) == 1
        assert plan.stack.backend == "fastapi"
        assert plan.title  # title is derived from spec, must not be empty

    def test_plan_features_always_non_empty(self) -> None:
        # Even with totally broken LLM, fallback ensures features ≥ 1
        plan = decompose_spec(
            "Build a chat app with login and messaging",
            _stub_gen(["", "", "", "", "", ""]),
        )
        assert len(plan.features) >= 1

    def test_each_numbered_section_in_spec_becomes_a_feature(self) -> None:
        # When the spec is structured with numbered sections, the fallback
        # extractor produces a feature per section. This is the guarantee
        # the user cares about most — a 15-section spec must NOT collapse
        # into 2 features.
        spec = """Build an AI advertising platform:
1. AI Campaign Builder for ad networks
2. AI Ad Content Generator
3. Social Media Management
4. Website & Mobile App Traffic Growth
5. SEO & Content Marketing
6. App Store Optimization
7. Analytics Dashboard
8. AI Optimization Agent
"""
        plan = decompose_spec(spec, _stub_gen(["", "", "", ""]))  # all LLM calls fail
        assert len(plan.features) >= 8, (
            f"Expected ≥8 features from 8 numbered sections, got {len(plan.features)}"
        )
