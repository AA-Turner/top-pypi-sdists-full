"""
Tests for validation retry with strict schema enforcement.
Uses synkro's actual schemas and abstractions.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from synkro.generation.logic_extractor import LogicExtractor
from synkro.llm.client import LLM, SchemaValidationError, _find_extra_fields, _validate_strict
from synkro.schemas import LogicMapOutput


class TestExtraFieldDetection:
    """Tests for detecting schema drift in synkro's actual schemas."""

    def test_logicmap_extra_fields_detected(self):
        """Extra fields at root level are detected."""
        schema = LogicMapOutput.model_json_schema()
        data = {
            "rules": [
                {
                    "rule_id": "R1",
                    "text": "Manager approval for $50+",
                    "condition": "amount > 50",
                    "action": "require manager approval",
                    "dependencies": [],
                    "category": "constraint",
                }
            ],
            "root_rules": ["R1"],
            "reasoning": "Extracted from policy",
            "extra_field": "garbage",
        }
        extras = _find_extra_fields(data, schema)
        assert "extra_field" in extras

    def test_rule_extraction_extra_fields_detected(self):
        """Extra fields in individual rules are detected."""
        schema = LogicMapOutput.model_json_schema()
        data = {
            "rules": [
                {
                    "rule_id": "R1",
                    "text": "Manager approval",
                    "condition": "amount > 50",
                    "action": "approve",
                    "dependencies": [],
                    "category": "constraint",
                    "confidence": 0.95,
                    "source_line": 42,
                }
            ],
            "root_rules": ["R1"],
            "reasoning": "test",
        }
        extras = _find_extra_fields(data, schema)
        assert "rules[0].confidence" in extras
        assert "rules[0].source_line" in extras

    def test_valid_logicmap_passes(self):
        """Valid LogicMapOutput passes strict validation."""
        content = """{
            "rules": [{
                "rule_id": "R1",
                "text": "Manager approval for $50+",
                "condition": "amount > 50",
                "action": "require approval",
                "dependencies": [],
                "category": "constraint"
            }],
            "root_rules": ["R1"],
            "reasoning": "Extracted one rule"
        }"""
        result = _validate_strict(content, LogicMapOutput)
        assert len(result.rules) == 1
        assert result.rules[0].rule_id == "R1"


class TestLogicExtractorWithValidation:
    """Tests for LogicExtractor with validation retry."""

    @pytest.mark.asyncio
    async def test_extractor_with_strict_validation(self):
        """LogicExtractor uses LLM.generate_structured which has strict=True by default."""
        llm = LLM(model="gpt-4o-mini")

        bad_response = MagicMock()
        bad_response.choices = [MagicMock()]
        bad_response.choices[0].message.content = """{
            "rules": [{
                "rule_id": "R1",
                "text": "Manager approval",
                "condition": "amount > 50",
                "action": "approve",
                "dependencies": [],
                "category": "constraint"
            }],
            "root_rules": ["R1"],
            "reasoning": "test",
            "extra_field": "this should fail"
        }"""

        with patch("synkro.llm.client._get_litellm") as mock_get:
            mock_get.return_value = (
                MagicMock(),
                AsyncMock(return_value=bad_response),
                MagicMock(),
                lambda **k: True,
            )

            extractor = LogicExtractor(llm=llm)

            with pytest.raises(SchemaValidationError) as exc_info:
                await extractor.extract("Test policy")

            assert "extra_field" in exc_info.value.extra_fields

    @pytest.mark.asyncio
    async def test_extractor_with_validation_retry_and_repair(self):
        """Configure LLM with validation_retries to auto-fix output."""
        gen_llm = LLM(model="gpt-4o-mini")
        repair_llm = LLM(model="gpt-4o")

        bad_response = MagicMock()
        bad_response.choices = [MagicMock()]
        bad_response.choices[0].message.content = """{
            "rules": [{
                "rule_id": "R1",
                "text": "Manager approval",
                "condition": "amount > 50",
                "action": "approve",
                "dependencies": [],
                "category": "constraint"
            }],
            "root_rules": ["R1"],
            "reasoning": "test",
            "required": ["R1"],
            "confidence_score": 0.99
        }"""

        async def mock_repair(prompt, system=None):
            return """{
                "rules": [{
                    "rule_id": "R1",
                    "text": "Manager approval",
                    "condition": "amount > 50",
                    "action": "approve",
                    "dependencies": [],
                    "category": "constraint"
                }],
                "root_rules": ["R1"],
                "reasoning": "Fixed output"
            }"""

        with patch("synkro.llm.client._get_litellm") as mock_get:
            mock_get.return_value = (
                MagicMock(),
                AsyncMock(return_value=bad_response),
                MagicMock(),
                lambda **k: True,
            )
            repair_llm.generate = mock_repair

            result = await gen_llm.generate_structured(
                "Extract rules from: All purchases over $50 require approval",
                LogicMapOutput,
                validation_retries=2,
                validation_model=repair_llm,
                strict=True,
            )

            assert len(result.rules) == 1
            assert result.rules[0].rule_id == "R1"


class TestExtraFieldScenarios:
    """Real-world scenarios with extra fields in output."""

    @pytest.mark.asyncio
    async def test_extra_required_array_at_root(self):
        """Extra 'required' array at top level is detected and repaired."""
        llm = LLM(model="gpt-4o-mini")
        repair_llm = LLM(model="gpt-4o")

        bad_response = MagicMock()
        bad_response.choices = [MagicMock()]
        bad_response.choices[0].message.content = """{
            "rules": [
                {"rule_id": "A", "text": "Purchases > $50 need manager approval", "condition": "purchase > 50", "action": "require manager", "dependencies": [], "category": "constraint"},
                {"rule_id": "B", "text": "Travel > $500 needs VP approval", "condition": "travel > 500", "action": "require VP", "dependencies": [], "category": "constraint"}
            ],
            "root_rules": ["A", "B"],
            "reasoning": "Two approval rules",
            "required": ["A", "B"]
        }"""

        async def repair(prompt, system=None):
            assert "Remove field: 'required'" in prompt
            return """{
                "rules": [
                    {"rule_id": "A", "text": "Purchases > $50 need manager approval", "condition": "purchase > 50", "action": "require manager", "dependencies": [], "category": "constraint"},
                    {"rule_id": "B", "text": "Travel > $500 needs VP approval", "condition": "travel > 500", "action": "require VP", "dependencies": [], "category": "constraint"}
                ],
                "root_rules": ["A", "B"],
                "reasoning": "Two approval rules"
            }"""

        with patch("synkro.llm.client._get_litellm") as mock_get:
            mock_get.return_value = (
                MagicMock(),
                AsyncMock(return_value=bad_response),
                MagicMock(),
                lambda **k: True,
            )
            repair_llm.generate = repair

            result = await llm.generate_structured(
                "Extract rules",
                LogicMapOutput,
                validation_retries=2,
                validation_model=repair_llm,
            )

            assert len(result.rules) == 2

    @pytest.mark.asyncio
    async def test_extra_fields_in_nested_rules(self):
        """Extra 'confidence', 'source' fields in rules are detected."""
        llm = LLM(model="gpt-4o-mini")
        repair_llm = LLM(model="gpt-4o")

        bad_response = MagicMock()
        bad_response.choices = [MagicMock()]
        bad_response.choices[0].message.content = """{
            "rules": [{
                "rule_id": "R1",
                "text": "Approval required",
                "condition": "always",
                "action": "approve",
                "dependencies": [],
                "category": "constraint",
                "confidence": 0.95,
                "source": "paragraph 1",
                "line_number": 5
            }],
            "root_rules": ["R1"],
            "reasoning": "one rule"
        }"""

        async def repair(prompt, system=None):
            assert "rules[0].confidence" in prompt or "confidence" in prompt
            return """{
                "rules": [{
                    "rule_id": "R1",
                    "text": "Approval required",
                    "condition": "always",
                    "action": "approve",
                    "dependencies": [],
                    "category": "constraint"
                }],
                "root_rules": ["R1"],
                "reasoning": "one rule"
            }"""

        with patch("synkro.llm.client._get_litellm") as mock_get:
            mock_get.return_value = (
                MagicMock(),
                AsyncMock(return_value=bad_response),
                MagicMock(),
                lambda **k: True,
            )
            repair_llm.generate = repair

            result = await llm.generate_structured(
                "Extract",
                LogicMapOutput,
                validation_retries=2,
                validation_model=repair_llm,
            )

            assert result.rules[0].rule_id == "R1"

    @pytest.mark.asyncio
    async def test_combined_type_and_extra_field_errors(self):
        """Model returns wrong types AND extra fields."""
        llm = LLM(model="gpt-4o-mini")
        repair_llm = LLM(model="gpt-4o")

        bad_response = MagicMock()
        bad_response.choices = [MagicMock()]
        bad_response.choices[0].message.content = """{
            "rules": [{
                "rule_id": 123,
                "text": "Approval",
                "condition": "always",
                "action": "approve",
                "dependencies": "none",
                "category": "constraint",
                "extra": true
            }],
            "root_rules": ["R1"],
            "reasoning": "test",
            "metadata": {"foo": "bar"}
        }"""

        repair_count = 0

        async def repair(prompt, system=None):
            nonlocal repair_count
            repair_count += 1
            if repair_count == 1:
                return """{
                    "rules": [{
                        "rule_id": "R1",
                        "text": "Approval",
                        "condition": "always",
                        "action": "approve",
                        "dependencies": [],
                        "category": "constraint"
                    }],
                    "root_rules": ["R1"],
                    "reasoning": "fixed",
                    "still_extra": true
                }"""
            else:
                return """{
                    "rules": [{
                        "rule_id": "R1",
                        "text": "Approval",
                        "condition": "always",
                        "action": "approve",
                        "dependencies": [],
                        "category": "constraint"
                    }],
                    "root_rules": ["R1"],
                    "reasoning": "fully fixed"
                }"""

        with patch("synkro.llm.client._get_litellm") as mock_get:
            mock_get.return_value = (
                MagicMock(),
                AsyncMock(return_value=bad_response),
                MagicMock(),
                lambda **k: True,
            )
            repair_llm.generate = repair

            result = await llm.generate_structured(
                "Extract",
                LogicMapOutput,
                validation_retries=3,
                validation_model=repair_llm,
            )

            assert result.rules[0].rule_id == "R1"
            assert repair_count == 2


class TestValidationRetries:
    """Tests for validation_retries parameter."""

    @pytest.mark.asyncio
    async def test_zero_retries_fails_immediately(self):
        """validation_retries=0 means no retries, fail on first error."""
        llm = LLM(model="gpt-4o-mini")

        bad_response = MagicMock()
        bad_response.choices = [MagicMock()]
        bad_response.choices[
            0
        ].message.content = '{"rules": [], "root_rules": [], "reasoning": "x", "extra": 1}'

        with patch("synkro.llm.client._get_litellm") as mock_get:
            mock_get.return_value = (
                MagicMock(),
                AsyncMock(return_value=bad_response),
                MagicMock(),
                lambda **k: True,
            )

            with pytest.raises(SchemaValidationError):
                await llm.generate_structured(
                    "test",
                    LogicMapOutput,
                    validation_retries=0,
                )

    @pytest.mark.asyncio
    async def test_retries_count_is_exact(self):
        """Repair is called exactly validation_retries times before giving up."""
        llm = LLM(model="gpt-4o-mini")
        repair_llm = LLM(model="gpt-4o")

        bad_response = MagicMock()
        bad_response.choices = [MagicMock()]
        bad_response.choices[
            0
        ].message.content = '{"rules": [], "root_rules": [], "reasoning": "x", "extra": 1}'

        repair_count = 0

        async def always_bad_repair(prompt, system=None):
            nonlocal repair_count
            repair_count += 1
            return '{"rules": [], "root_rules": [], "reasoning": "x", "still_bad": 1}'

        with patch("synkro.llm.client._get_litellm") as mock_get:
            mock_get.return_value = (
                MagicMock(),
                AsyncMock(return_value=bad_response),
                MagicMock(),
                lambda **k: True,
            )
            repair_llm.generate = always_bad_repair

            with pytest.raises(SchemaValidationError):
                await llm.generate_structured(
                    "test",
                    LogicMapOutput,
                    validation_retries=3,
                    validation_model=repair_llm,
                )

            assert repair_count == 3

    @pytest.mark.asyncio
    async def test_succeeds_on_second_retry(self):
        """First retry fails, second succeeds."""
        llm = LLM(model="gpt-4o-mini")
        repair_llm = LLM(model="gpt-4o")

        bad_response = MagicMock()
        bad_response.choices = [MagicMock()]
        bad_response.choices[
            0
        ].message.content = '{"rules": [], "root_rules": [], "reasoning": "x", "bad": 1}'

        repair_count = 0

        async def eventually_good_repair(prompt, system=None):
            nonlocal repair_count
            repair_count += 1
            if repair_count < 2:
                return '{"rules": [], "root_rules": [], "reasoning": "x", "still_bad": 1}'
            return '{"rules": [], "root_rules": [], "reasoning": "fixed"}'

        with patch("synkro.llm.client._get_litellm") as mock_get:
            mock_get.return_value = (
                MagicMock(),
                AsyncMock(return_value=bad_response),
                MagicMock(),
                lambda **k: True,
            )
            repair_llm.generate = eventually_good_repair

            result = await llm.generate_structured(
                "test",
                LogicMapOutput,
                validation_retries=5,
                validation_model=repair_llm,
            )

            assert result.reasoning == "fixed"
            assert repair_count == 2

    @pytest.mark.asyncio
    async def test_uses_self_when_no_validation_model(self):
        """When validation_model is None, uses self.generate for repair."""
        llm = LLM(model="gpt-4o-mini")

        bad_response = MagicMock()
        bad_response.choices = [MagicMock()]
        bad_response.choices[
            0
        ].message.content = '{"rules": [], "root_rules": [], "reasoning": "x", "bad": 1}'

        generate_calls = []

        async def tracking_generate(prompt, system=None):
            generate_calls.append(prompt)
            return '{"rules": [], "root_rules": [], "reasoning": "fixed"}'

        with patch("synkro.llm.client._get_litellm") as mock_get:
            mock_get.return_value = (
                MagicMock(),
                AsyncMock(return_value=bad_response),
                MagicMock(),
                lambda **k: True,
            )
            llm.generate = tracking_generate

            await llm.generate_structured(
                "test",
                LogicMapOutput,
                validation_retries=1,
                validation_model=None,
            )

            assert len(generate_calls) == 1
            assert "Remove field" in generate_calls[0]

    @pytest.mark.asyncio
    async def test_repair_prompt_contains_error_details(self):
        """Repair prompt includes the schema, raw JSON, and specific errors."""
        llm = LLM(model="gpt-4o-mini")
        repair_llm = LLM(model="gpt-4o")

        bad_response = MagicMock()
        bad_response.choices = [MagicMock()]
        bad_response.choices[
            0
        ].message.content = '{"rules": [], "root_rules": [], "reasoning": "x", "drift_field": 123}'

        captured_prompt = None

        async def capture_repair(prompt, system=None):
            nonlocal captured_prompt
            captured_prompt = prompt
            return '{"rules": [], "root_rules": [], "reasoning": "ok"}'

        with patch("synkro.llm.client._get_litellm") as mock_get:
            mock_get.return_value = (
                MagicMock(),
                AsyncMock(return_value=bad_response),
                MagicMock(),
                lambda **k: True,
            )
            repair_llm.generate = capture_repair

            await llm.generate_structured(
                "test",
                LogicMapOutput,
                validation_retries=1,
                validation_model=repair_llm,
            )

            assert "drift_field" in captured_prompt
            assert "Remove field" in captured_prompt
            assert "Required Schema" in captured_prompt
            assert "Original JSON" in captured_prompt


class TestStrictModeToggle:
    """Tests for strict=True/False behavior."""

    @pytest.mark.asyncio
    async def test_strict_false_ignores_extra_fields(self):
        """With strict=False, Pydantic ignores extra fields."""
        llm = LLM(model="gpt-4o-mini")

        response = MagicMock()
        response.choices = [MagicMock()]
        response.choices[0].message.content = """{
            "rules": [{
                "rule_id": "R1",
                "text": "test",
                "condition": "c",
                "action": "a",
                "dependencies": [],
                "category": "constraint"
            }],
            "root_rules": ["R1"],
            "reasoning": "r",
            "garbage": "ignored"
        }"""

        with patch("synkro.llm.client._get_litellm") as mock_get:
            mock_get.return_value = (
                MagicMock(),
                AsyncMock(return_value=response),
                MagicMock(),
                lambda **k: True,
            )

            result = await llm.generate_structured(
                "Extract",
                LogicMapOutput,
                strict=False,
            )

            assert result.rules[0].rule_id == "R1"

    @pytest.mark.asyncio
    async def test_strict_true_is_default(self):
        """Strict mode is on by default."""
        llm = LLM(model="gpt-4o-mini")

        response = MagicMock()
        response.choices = [MagicMock()]
        response.choices[0].message.content = """{
            "rules": [{
                "rule_id": "R1",
                "text": "t",
                "condition": "c",
                "action": "a",
                "dependencies": [],
                "category": "constraint"
            }],
            "root_rules": ["R1"],
            "reasoning": "r",
            "bad_field": 123
        }"""

        with patch("synkro.llm.client._get_litellm") as mock_get:
            mock_get.return_value = (
                MagicMock(),
                AsyncMock(return_value=response),
                MagicMock(),
                lambda **k: True,
            )

            with pytest.raises(SchemaValidationError):
                await llm.generate_structured("Extract", LogicMapOutput)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
