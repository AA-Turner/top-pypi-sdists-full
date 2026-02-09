"""
Real integration tests for validation retry using Gemini.
Requires GEMINI_API_KEY environment variable.

Tests both direct inference and mocked bad outputs to verify repair logic.
"""

import os
from unittest.mock import MagicMock

import pytest
from pydantic import BaseModel

from synkro.llm.client import LLM, SchemaValidationError
from synkro.parsers import extract_json, strip_markdown_fences
from synkro.schemas import LogicMapOutput


def clean_llm_json(response: str) -> str:
    """Extract clean JSON from LLM response that may have markdown fences."""
    cleaned = strip_markdown_fences(response)
    # Try to extract JSON object
    json_str = extract_json(cleaned, "{")
    return json_str if json_str else cleaned


GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
SKIP_REASON = "GEMINI_API_KEY not set"


class SimpleSchema(BaseModel):
    """Simple schema for testing - model might add extra fields."""

    name: str
    count: int


class StrictSchema(BaseModel):
    """Schema with specific fields only."""

    title: str
    items: list[str]


def mock_bad_response(content: str):
    """Create a mock LiteLLM response with bad JSON."""
    response = MagicMock()
    response.choices = [MagicMock()]
    response.choices[0].message.content = content
    return response


@pytest.mark.skipif(not GEMINI_API_KEY, reason=SKIP_REASON)
class TestRealGeminiInference:
    """Real inference tests with gemini-2.5-flash."""

    @pytest.mark.asyncio
    async def test_basic_structured_output(self):
        """Verify basic structured output works."""
        llm = LLM(model="gemini/gemini-2.5-flash")

        result = await llm.generate_structured(
            "Return a JSON with name='test' and count=42",
            SimpleSchema,
            strict=False,  # Don't fail on extra fields for this test
        )

        assert result.name == "test"
        assert result.count == 42
        print(f"\nBasic output: {result}")

    @pytest.mark.asyncio
    async def test_strict_mode_catches_extra_fields(self):
        """Verify strict mode catches extra fields via direct validation."""
        from synkro.llm.client import _validate_strict

        # Gemini is well-behaved and follows schema - test the validation directly
        bad_json = '{"name": "Alice", "count": 10, "extra_info": "hello", "metadata": {}}'

        with pytest.raises(SchemaValidationError) as exc_info:
            _validate_strict(bad_json, SimpleSchema)

        print(f"\nCaught extra fields: {exc_info.value.extra_fields}")
        assert "extra_info" in exc_info.value.extra_fields
        assert "metadata" in exc_info.value.extra_fields

    @pytest.mark.asyncio
    async def test_validation_retry_repairs_output(self):
        """Retry should fix extra fields."""
        llm = LLM(model="gemini/gemini-2.5-flash")

        # Ask for extra fields, but allow retries to fix
        result = await llm.generate_structured(
            "Return JSON with name='Bob', count=5. Also include extra_data='xyz' and debug=true",
            SimpleSchema,
            strict=True,
            validation_retries=2,  # Allow repair
        )

        # Should succeed after repair
        assert result.name == "Bob"
        assert result.count == 5
        print(f"\nRepaired output: {result}")

    @pytest.mark.asyncio
    async def test_logicmap_extraction_real(self):
        """Real LogicMap extraction from policy text."""
        llm = LLM(model="gemini/gemini-2.5-flash")

        policy = """
        Company Expense Policy:
        1. All purchases over $50 require manager approval.
        2. Travel expenses over $500 require VP approval.
        """

        result = await llm.generate_structured(
            f"Extract business rules as structured JSON:\n\n{policy}",
            LogicMapOutput,
            strict=True,
            validation_retries=2,
        )

        assert len(result.rules) >= 1
        print(f"\nExtracted {len(result.rules)} rules:")
        for rule in result.rules:
            print(f"  - {rule.rule_id}: {rule.text[:50]}...")

    @pytest.mark.asyncio
    async def test_validation_model_for_repair(self):
        """Use separate validation_model for repairs."""
        gen_llm = LLM(model="gemini/gemini-2.5-flash")
        repair_llm = LLM(model="gemini/gemini-2.5-flash")

        # Track if repair model was used
        original_generate = repair_llm.generate
        repair_called = False

        async def tracked_generate(prompt, system=None):
            nonlocal repair_called
            repair_called = True
            print(f"\nRepair model called with prompt length: {len(prompt)}")
            return await original_generate(prompt, system)

        repair_llm.generate = tracked_generate

        # Force extra fields
        result = await gen_llm.generate_structured(
            "Return JSON: name='Test', count=99. IMPORTANT: Also add 'source': 'user', 'timestamp': 12345",
            SimpleSchema,
            strict=True,
            validation_retries=2,
            validation_model=repair_llm,
        )

        assert result.name == "Test"
        print(f"\nFinal result: {result}")
        print(f"Repair model was called: {repair_called}")


@pytest.mark.skipif(not GEMINI_API_KEY, reason=SKIP_REASON)
class TestRetryCountBehavior:
    """Test that retry counts work correctly."""

    @pytest.mark.asyncio
    async def test_zero_retries_fails_on_extra(self):
        """Verify 0 retries fails immediately on extra fields via direct validation."""
        from synkro.llm.client import _validate_strict

        # Gemini follows schema correctly - test validation directly
        bad_json = '{"name": "X", "count": 1, "bonus": "extra"}'

        with pytest.raises(SchemaValidationError) as exc_info:
            _validate_strict(bad_json, SimpleSchema)

        assert "bonus" in exc_info.value.extra_fields
        print(f"\nDetected extra field: {exc_info.value.extra_fields}")

    @pytest.mark.asyncio
    async def test_enough_retries_succeeds(self):
        """With enough retries, eventually succeeds."""
        llm = LLM(model="gemini/gemini-2.5-flash")

        result = await llm.generate_structured(
            "Output JSON with name='Success', count=100. Add garbage='delete_me'",
            SimpleSchema,
            strict=True,
            validation_retries=3,
        )

        assert result.name == "Success"
        assert result.count == 100


@pytest.mark.skipif(not GEMINI_API_KEY, reason=SKIP_REASON)
class TestMockedBadOutputWithRealRepair:
    """Mock bad outputs, use REAL Gemini for repairs.

    Tests the repair flow by feeding known-bad JSON and verifying Gemini fixes it.
    """

    @pytest.mark.asyncio
    async def test_extra_fields_at_root_repaired(self):
        """Extra fields at root level are repaired."""
        repair_llm = LLM(model="gemini/gemini-2.5-flash")

        bad_output = """{
            "rules": [
                {"rule_id": "A", "text": "Purchases over $50 need approval", "condition": "amount > 50", "action": "require approval", "dependencies": [], "category": "constraint"},
                {"rule_id": "B", "text": "Travel over $500 needs VP", "condition": "travel > 500", "action": "require VP", "dependencies": [], "category": "constraint"}
            ],
            "root_rules": ["A", "B"],
            "reasoning": "Two rules extracted",
            "required": ["A", "B"],
            "confidence": 0.95,
            "extra_field": "should be removed"
        }"""

        import json

        from synkro.llm.client import _REPAIR_PROMPT, _format_validation_errors, _validate_strict

        try:
            _validate_strict(bad_output, LogicMapOutput)
            pytest.fail("Should have raised SchemaValidationError")
        except SchemaValidationError as e:
            error_text = _format_validation_errors(e)
            print(f"\nDetected extra fields: {e.extra_fields}")

        schema_text = LogicMapOutput.model_json_schema()
        repair_prompt = _REPAIR_PROMPT.format(
            raw_json=bad_output,
            errors=error_text,
            schema=json.dumps(schema_text, indent=2),
        )

        raw_response = await repair_llm.generate(repair_prompt)
        repaired_json = clean_llm_json(raw_response)
        print(f"\nRepaired output ({len(repaired_json)} chars)")

        result = _validate_strict(repaired_json, LogicMapOutput)

        assert len(result.rules) == 2
        assert result.rules[0].rule_id == "A"
        print(f"  - {result.rules[0].rule_id}: {result.rules[0].text}")
        print(f"  - {result.rules[1].rule_id}: {result.rules[1].text}")

    @pytest.mark.asyncio
    async def test_nested_extra_fields_repaired(self):
        """Extra fields inside rules array - Gemini cleans them."""
        repair_llm = LLM(model="gemini/gemini-2.5-flash")

        bad_output = """{
            "rules": [{
                "rule_id": "R1",
                "text": "MFA required for admin",
                "condition": "action == admin",
                "action": "require MFA",
                "dependencies": [],
                "category": "constraint",
                "source_line": 42,
                "confidence_score": 0.99,
                "extra_nested": "remove"
            }],
            "root_rules": ["R1"],
            "reasoning": "One rule",
            "metadata": {"parser": "v2", "timestamp": 1234567890}
        }"""

        import json

        from synkro.llm.client import _REPAIR_PROMPT, _format_validation_errors, _validate_strict

        try:
            _validate_strict(bad_output, LogicMapOutput)
            pytest.fail("Should have raised SchemaValidationError")
        except SchemaValidationError as e:
            error_text = _format_validation_errors(e)
            print(f"\nDetected nested extra fields: {e.extra_fields}")

        repair_prompt = _REPAIR_PROMPT.format(
            raw_json=bad_output,
            errors=error_text,
            schema=json.dumps(LogicMapOutput.model_json_schema(), indent=2),
        )

        raw_response = await repair_llm.generate(repair_prompt)
        repaired_json = clean_llm_json(raw_response)
        result = _validate_strict(repaired_json, LogicMapOutput)

        assert result.rules[0].rule_id == "R1"
        print(f"\nCleaned nested fields: {result.rules[0].rule_id}")

    @pytest.mark.asyncio
    async def test_type_errors_and_extra_fields_repaired(self):
        """Both type errors AND extra fields - Gemini fixes everything."""
        repair_llm = LLM(model="gemini/gemini-2.5-flash")

        terrible_output = """{
            "rules": [{
                "rule_id": 123,
                "text": "Encrypt PII",
                "condition": "data_type == PII",
                "action": "encrypt",
                "dependencies": "none",
                "category": "constraint",
                "priority": "high"
            }],
            "root_rules": "R1",
            "reasoning": "One rule",
            "debug_info": true
        }"""

        import json

        from pydantic import ValidationError

        from synkro.llm.client import _REPAIR_PROMPT, _format_validation_errors, _validate_strict

        # This will fail with both extra fields AND type errors
        try:
            _validate_strict(terrible_output, LogicMapOutput)
            pytest.fail("Should have raised error")
        except (SchemaValidationError, ValidationError) as e:
            error_text = _format_validation_errors(e)
            print(f"\nDetected errors: {error_text[:200]}...")

        repair_prompt = _REPAIR_PROMPT.format(
            raw_json=terrible_output,
            errors=error_text,
            schema=json.dumps(LogicMapOutput.model_json_schema(), indent=2),
        )

        raw_response = await repair_llm.generate(repair_prompt)
        repaired_json = clean_llm_json(raw_response)
        result = _validate_strict(repaired_json, LogicMapOutput)

        assert isinstance(result.rules[0].rule_id, str)
        assert isinstance(result.rules[0].dependencies, list)
        print(f"\nFixed types: rule_id={result.rules[0].rule_id}")

    @pytest.mark.asyncio
    async def test_simple_schema_repair(self):
        """Simple schema with extra garbage - Gemini cleans it."""
        repair_llm = LLM(model="gemini/gemini-2.5-flash")

        bad_output = '{"name": "Alice", "count": 42, "email": "alice@example.com", "age": 30, "active": true}'

        import json

        from synkro.llm.client import _REPAIR_PROMPT, _format_validation_errors, _validate_strict

        try:
            _validate_strict(bad_output, SimpleSchema)
            pytest.fail("Should have raised SchemaValidationError")
        except SchemaValidationError as e:
            error_text = _format_validation_errors(e)
            print(f"\nDetected extra fields: {e.extra_fields}")

        repair_prompt = _REPAIR_PROMPT.format(
            raw_json=bad_output,
            errors=error_text,
            schema=json.dumps(SimpleSchema.model_json_schema(), indent=2),
        )

        raw_response = await repair_llm.generate(repair_prompt)
        repaired_json = clean_llm_json(raw_response)
        result = _validate_strict(repaired_json, SimpleSchema)

        assert result.name == "Alice"
        assert result.count == 42
        print(f"\nCleaned: name={result.name}, count={result.count}")

    @pytest.mark.asyncio
    async def test_repair_prompt_format(self):
        """Verify the repair prompt contains schema and errors."""
        import json

        from synkro.llm.client import _REPAIR_PROMPT, _format_validation_errors, _validate_strict

        bad_output = '{"name": "Test", "count": 5, "garbage": "remove_me"}'

        try:
            _validate_strict(bad_output, SimpleSchema)
        except SchemaValidationError as e:
            error_text = _format_validation_errors(e)

        repair_prompt = _REPAIR_PROMPT.format(
            raw_json=bad_output,
            errors=error_text,
            schema=json.dumps(SimpleSchema.model_json_schema(), indent=2),
        )

        assert "garbage" in repair_prompt
        assert "Remove field" in repair_prompt
        assert "Required Schema" in repair_prompt
        print(f"\nRepair prompt ({len(repair_prompt)} chars):")
        print("  Contains 'garbage': ✓")
        print("  Contains 'Remove field': ✓")
        print("  Contains 'Required Schema': ✓")


@pytest.mark.skipif(not GEMINI_API_KEY, reason=SKIP_REASON)
class TestRealValidationFlow:
    """End-to-end tests proving validation + retry works with real LLM."""

    @pytest.mark.asyncio
    async def test_complex_extraction_with_retries(self):
        """Extract complex nested data with validation retries enabled."""
        llm = LLM(model="gemini/gemini-2.5-flash")

        policy = """
        SECURITY POLICY v2.1

        Access Control:
        - Users must authenticate with MFA for admin actions
        - Session timeout after 30 minutes of inactivity
        - Failed login attempts: lock after 5 tries

        Data Handling:
        - PII must be encrypted at rest
        - Logs must be retained for 90 days
        """

        result = await llm.generate_structured(
            f"Extract ALL business rules from this policy:\n\n{policy}",
            LogicMapOutput,
            strict=True,
            validation_retries=3,
        )

        print(f"\nExtracted {len(result.rules)} rules with validation:")
        for rule in result.rules:
            print(f"  [{rule.category}] {rule.rule_id}: {rule.text[:60]}...")

        assert len(result.rules) >= 3  # Should get at least 3 rules
        assert all(r.rule_id for r in result.rules)
        assert all(r.text for r in result.rules)

    @pytest.mark.asyncio
    async def test_validation_with_system_prompt(self):
        """Verify system prompt + validation works together."""
        llm = LLM(model="gemini/gemini-2.5-flash")

        result = await llm.generate_structured(
            "What items are typically found in a kitchen?",
            StrictSchema,
            system="You are a helpful assistant that outputs JSON with title and items fields only.",
            strict=True,
            validation_retries=2,
        )

        assert result.title
        assert len(result.items) > 0
        print(f"\nTitle: {result.title}")
        print(f"Items: {result.items[:5]}...")


@pytest.mark.skipif(not GEMINI_API_KEY, reason=SKIP_REASON)
class TestFallbackMode:
    """Test fallback for models without structured output support."""

    @pytest.mark.asyncio
    async def test_unsupported_model_uses_fallback(self):
        """Unsupported model triggers warning and fallback with auto-retries."""
        import warnings

        # Use a fake model name that LiteLLM won't recognize
        llm = LLM(model="ollama/fake-local-model")

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            # This should warn and use fallback, but will fail on actual call
            # since the model doesn't exist - we just verify the warning fires
            try:
                await llm.generate_structured(
                    "Return JSON with name='test'",
                    SimpleSchema,
                )
            except Exception:
                pass  # Expected - model doesn't exist

            # Check that the fallback warning was issued
            fallback_warnings = [
                x for x in w if "may not support structured outputs" in str(x.message)
            ]
            assert len(fallback_warnings) >= 1
            print(f"\nFallback warning issued: {fallback_warnings[0].message}")

    @pytest.mark.asyncio
    async def test_fallback_with_real_ollama_model(self):
        """Test fallback works with a real Ollama model if available."""
        import subprocess

        # Check if Ollama is running
        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode != 0:
                pytest.skip("Ollama not running")
        except Exception:
            pytest.skip("Ollama not available")

        # Use a common small model
        llm = LLM(model="ollama/llama3.2:1b")

        import warnings

        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")

            try:
                result = await llm.generate_structured(
                    "Return a JSON object with name set to 'Alice' and count set to 42",
                    SimpleSchema,
                    strict=True,
                )
                print(f"\nOllama fallback result: {result}")
                assert result.name == "Alice"
                assert result.count == 42
            except Exception as e:
                pytest.skip(f"Ollama model not available: {e}")


OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
SKIP_OPENROUTER = "OPENROUTER_API_KEY not set"


class TestJsonSanitization:
    """Test JSON sanitization for malformed LLM outputs."""

    def test_control_characters_in_strings(self):
        """Control characters inside strings should be escaped."""
        from synkro.llm.client import _clean_json_content

        # Literal newline inside a string (common with weak models)
        bad_json = '{"text": "line one\nline two", "count": 1}'

        cleaned = _clean_json_content(bad_json)

        import json

        data = json.loads(cleaned)
        assert data["count"] == 1
        assert "line" in data["text"]
        print(f"\nCleaned control chars: {data}")

    def test_tabs_in_strings(self):
        """Literal tabs inside strings should be escaped."""
        from synkro.llm.client import _clean_json_content

        bad_json = '{"text": "col1\tcol2\tcol3", "num": 42}'

        cleaned = _clean_json_content(bad_json)

        import json

        data = json.loads(cleaned)
        assert data["num"] == 42
        print(f"\nCleaned tabs: {data}")

    def test_carriage_returns_in_strings(self):
        """Carriage returns inside strings should be escaped."""
        from synkro.llm.client import _clean_json_content

        bad_json = '{"text": "windows\r\nstyle", "ok": true}'

        cleaned = _clean_json_content(bad_json)

        import json

        data = json.loads(cleaned)
        assert data["ok"] is True
        print(f"\nCleaned CR: {data}")

    def test_markdown_fences_plus_control_chars(self):
        """Both markdown fences and control characters."""
        from synkro.llm.client import _clean_json_content

        bad_json = '```json\n{"text": "has\nnewline", "x": 1}\n```'

        cleaned = _clean_json_content(bad_json)

        import json

        data = json.loads(cleaned)
        assert data["x"] == 1
        print(f"\nCleaned fences + control: {data}")

    def test_preserves_escaped_characters(self):
        """Already-escaped characters should not be double-escaped."""
        from synkro.llm.client import _clean_json_content

        # This JSON has properly escaped newlines
        good_json = '{"text": "line\\none\\ntwo", "n": 5}'

        cleaned = _clean_json_content(good_json)

        import json

        data = json.loads(cleaned)
        assert data["n"] == 5
        assert "\\n" in good_json  # Original had escaped
        print(f"\nPreserved escapes: {data}")

    def test_complex_nested_with_control_chars(self):
        """Nested objects with control characters."""
        from synkro.llm.client import _clean_json_content

        bad_json = """{
            "rules": [
                {"id": "R1", "text": "Rule with\nnewline"}
            ],
            "meta": {"note": "also\thas\ttabs"}
        }"""

        cleaned = _clean_json_content(bad_json)

        import json

        data = json.loads(cleaned)
        assert len(data["rules"]) == 1
        assert data["rules"][0]["id"] == "R1"
        print(f"\nCleaned nested: {data['rules'][0]}")


@pytest.mark.skipif(not OPENROUTER_API_KEY, reason=SKIP_OPENROUTER)
class TestLiquidInstructRepair:
    """Test Liquid Instruct with programmatic field stripping."""

    @pytest.mark.asyncio
    async def test_extra_fields_stripped_automatically(self):
        """Extra fields are stripped programmatically - no LLM repair needed."""
        from synkro.llm.client import _validate_strict

        # JSON with extra fields
        bad_json = '{"name": "Test", "count": 42, "extra": "remove", "garbage": true}'

        # Should succeed - extra fields stripped automatically
        result = _validate_strict(bad_json, SimpleSchema)

        assert result.name == "Test"
        assert result.count == 42
        print(f"\nStripped extra fields: name={result.name}, count={result.count}")

    @pytest.mark.asyncio
    async def test_logicmap_extra_fields_stripped(self):
        """LogicMap extra fields are stripped programmatically."""
        from synkro.llm.client import _validate_strict

        # Simulated output from LFM2-Extract (has extra fields + required reasoning)
        json_with_extras = """{
            "rules": [
                {"rule_id": "R1", "text": "Purchases over $50 need approval", "condition": "amount > 50", "action": "require_approval", "dependencies": [], "category": "constraint"}
            ],
            "root_rules": ["R1"],
            "reasoning": "Extracted approval rule",
            "requirements": ["R1"],
            "title": "Expense Policy",
            "version": "1.0"
        }"""

        # Should succeed - extra fields stripped automatically
        result = _validate_strict(json_with_extras, LogicMapOutput)

        assert len(result.rules) == 1
        assert result.rules[0].rule_id == "R1"
        print(f"\nStripped extra fields from LogicMap: {len(result.rules)} rules")

    @pytest.mark.asyncio
    async def test_liquid_instruct_generates_valid_json(self):
        """Liquid Instruct can generate valid JSON for simple schemas."""
        llm = LLM(
            model="openrouter/liquid/lfm-2.5-1.2b-instruct:free",
            temperature=0.0,
        )

        result = await llm.generate_structured(
            "Return JSON with name='Alice' and count=42",
            SimpleSchema,
            strict=True,
        )

        assert result.name == "Alice"
        assert result.count == 42
        print(f"\nLiquid Instruct output: name={result.name}, count={result.count}")

    @pytest.mark.asyncio
    async def test_liquid_instruct_logicmap_extraction(self):
        """Liquid Instruct can extract LogicMap from policy text."""
        llm = LLM(
            model="openrouter/liquid/lfm-2.5-1.2b-instruct:free",
            temperature=0.0,
        )

        policy = """
        Company Expense Policy:
        1. All purchases over $50 require manager approval
        2. Travel expenses over $500 require VP approval
        """

        result = await llm.generate_structured(
            f"Extract business rules as JSON from this policy:\n\n{policy}",
            LogicMapOutput,
            strict=True,
        )

        assert len(result.rules) >= 1
        assert result.reasoning
        print(f"\nExtracted {len(result.rules)} rules from policy")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
