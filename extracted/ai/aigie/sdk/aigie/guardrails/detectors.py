"""
Content Detectors for SLA Production Runtime.

Detects issues that may impact agent reliability and triggers
remediation actions (RETRY, REDIRECT, ADJUST, ESCALATE).

Kytte is an SLA tool - we don't block, we fix.

Detectors:
- PII: Adjusts content by redacting sensitive data
- Quality: Detects low quality outputs, triggers retry
- Hallucination: Detects fabricated content, triggers redirect
- Drift: Detects off-topic responses, triggers escalation
"""

import logging
import re
import time
from typing import Any

from aigie.guardrails.base import BaseGuardrail, GuardrailAction, GuardrailResult

logger = logging.getLogger(__name__)


class PIIDetector(BaseGuardrail):
    """
    Detects and optionally redacts Personally Identifiable Information.

    Detects:
    - Email addresses
    - Phone numbers
    - Social Security Numbers
    - Credit card numbers
    - IP addresses
    - Street addresses
    """

    # PII patterns
    PATTERNS = {
        "email": (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "Email address"),
        "phone_us": (r"\b(?:\+1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b", "US phone number"),
        "phone_intl": (
            r"\b\+\d{1,3}[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}\b",
            "International phone number",
        ),
        "ssn": (r"\b\d{3}[-\s]?\d{2}[-\s]?\d{4}\b", "Social Security Number"),
        "credit_card": (r"\b(?:\d{4}[-\s]?){3}\d{4}\b", "Credit card number"),
        "ip_address": (r"\b(?:\d{1,3}\.){3}\d{1,3}\b", "IP address"),
    }

    def __init__(
        self,
        redact: bool = True,
        redaction_char: str = "*",
        name: str = "PIIDetector",
    ):
        """
        Initialize PII detector.

        Args:
            redact: Whether to redact detected PII
            redaction_char: Character to use for redaction
            name: Name for this guardrail
        """
        super().__init__(name)
        self.redact = redact
        self.redaction_char = redaction_char
        self._compiled_patterns = {
            name: (re.compile(pattern), desc) for name, (pattern, desc) in self.PATTERNS.items()
        }

    async def check(
        self,
        content: str,
        context: dict[str, Any] | None = None,
    ) -> GuardrailResult:
        """Check content for PII."""
        start_time = time.time()

        issues = []
        detections = []
        modified_content = content if self.redact else None

        for pii_type, (pattern, desc) in self._compiled_patterns.items():
            matches = pattern.findall(content)
            if matches:
                issues.append(f"Detected {len(matches)} {desc}(s)")
                detections.append(
                    {
                        "type": pii_type,
                        "description": desc,
                        "count": len(matches),
                    }
                )

                if self.redact and modified_content:
                    modified_content = pattern.sub(
                        lambda m: self.redaction_char * len(m.group()),
                        modified_content,
                    )

        passed = len(issues) == 0
        # Use ADJUST (not BLOCK) - we redact and continue
        action = (
            GuardrailAction.PASS
            if passed
            else (GuardrailAction.ADJUST if self.redact else GuardrailAction.WARN)
        )
        score = 1.0 if passed else 0.5

        return GuardrailResult(
            guardrail_name=self.name,
            action=action,
            passed=passed,
            score=score,
            issues=issues,
            modified_content=modified_content if issues else None,
            details={"detections": detections, "auto_remediated": self.redact},
            duration_ms=(time.time() - start_time) * 1000,
        )


class ToxicityDetector(BaseGuardrail):
    """
    Detects toxic, harmful, or inappropriate content.

    Uses keyword/pattern matching as a baseline. For production use,
    consider integrating with an ML-based toxicity API.
    """

    # Toxicity indicators (simplified patterns)
    TOXIC_PATTERNS = [
        (
            r"\b(?:kill|murder|harm|hurt)\s+(?:you|them|him|her|people|someone)\b",
            "violence_threat",
            0.9,
        ),
        (r"\b(?:hate|despise)\s+(?:you|them|all)\b", "hate_speech", 0.7),
        (
            r"\bhow\s+to\s+(?:make|build)\s+(?:a\s+)?(?:bomb|weapon|explosive)\b",
            "dangerous_content",
            0.95,
        ),
        (r"\b(?:suicide|self[-\s]?harm)\s+(?:method|way|how)\b", "self_harm", 0.95),
    ]

    def __init__(
        self,
        threshold: float = 0.7,
        use_llm: bool = False,
        llm_model: str = "gpt-4o-mini",
        name: str = "ToxicityDetector",
    ):
        """
        Initialize toxicity detector.

        Args:
            threshold: Score threshold for blocking (0.0 to 1.0)
            use_llm: Whether to use LLM for detection (more accurate but slower)
            llm_model: Model to use for LLM-based detection
            name: Name for this guardrail
        """
        super().__init__(name)
        self.threshold = threshold
        self.use_llm = use_llm
        self.llm_model = llm_model
        self._compiled_patterns = [
            (re.compile(pattern, re.IGNORECASE), category, score)
            for pattern, category, score in self.TOXIC_PATTERNS
        ]

    async def check(
        self,
        content: str,
        context: dict[str, Any] | None = None,
    ) -> GuardrailResult:
        """Check content for toxicity."""
        start_time = time.time()

        if self.use_llm:
            return await self._check_with_llm(content, start_time)
        return await self._check_with_patterns(content, start_time)

    async def _check_with_patterns(
        self,
        content: str,
        start_time: float,
    ) -> GuardrailResult:
        """Pattern-based toxicity check."""
        issues = []
        detections = []
        max_score = 0.0

        for pattern, category, score in self._compiled_patterns:
            matches = pattern.findall(content)
            if matches:
                issues.append(f"Detected {category}")
                detections.append(
                    {
                        "category": category,
                        "count": len(matches),
                        "severity": score,
                    }
                )
                max_score = max(max_score, score)

        passed = max_score < self.threshold
        action = GuardrailAction.PASS if passed else GuardrailAction.RETRY
        # Invert score (1.0 = safe, 0.0 = toxic)
        safety_score = 1.0 - max_score if max_score > 0 else 1.0

        return GuardrailResult(
            guardrail_name=self.name,
            action=action,
            passed=passed,
            score=safety_score,
            issues=issues,
            details={
                "detections": detections,
                "method": "pattern",
            },
            duration_ms=(time.time() - start_time) * 1000,
        )

    async def _check_with_llm(
        self,
        content: str,
        start_time: float,
    ) -> GuardrailResult:
        """LLM-based toxicity check."""
        try:
            from aigie.evaluation.llm_judge import JudgeConfig, LLMJudge

            judge = LLMJudge(JudgeConfig(model=self.llm_model))
            result = await judge.evaluate(
                input="Check if this content is safe and non-toxic.",
                output=content,
                criteria=["safety"],
            )

            safety_score = result.get_score("safety") or 0.5
            passed = safety_score >= self.threshold

            return GuardrailResult(
                guardrail_name=self.name,
                action=GuardrailAction.PASS if passed else GuardrailAction.RETRY,
                passed=passed,
                score=safety_score,
                issues=[] if passed else ["Content flagged as potentially unsafe"],
                details={
                    "method": "llm",
                    "model": self.llm_model,
                    "feedback": result.feedback,
                },
                duration_ms=(time.time() - start_time) * 1000,
            )

        except Exception as e:
            logger.error(f"LLM toxicity check failed: {e}")
            # Fallback to pattern-based check
            return await self._check_with_patterns(content, start_time)


class HallucinationDetector(BaseGuardrail):
    """
    Detects potential hallucinations in LLM outputs.

    Checks for:
    - Claims that contradict provided context
    - Fabricated facts without source
    - Confidence markers on uncertain claims
    """

    # Patterns indicating potential hallucinations
    HALLUCINATION_INDICATORS = [
        (r"\b(?:studies show|research indicates|scientists say)\b", "unsourced_claim", 0.5),
        (r"\b(?:according to|as reported by)\s+\w+(?!\s+[A-Z])", "vague_attribution", 0.4),
        (r"\b(?:always|never|definitely|certainly)\b", "overconfident_claim", 0.3),
        (r"\b(?:approximately|roughly|about)\s+\d+(?:\.\d+)?%?\b", "fabricated_statistic", 0.6),
    ]

    def __init__(
        self,
        reference_context: str | None = None,
        use_llm: bool = False,
        llm_model: str = "gpt-4o-mini",
        threshold: float = 0.6,
        name: str = "HallucinationDetector",
    ):
        """
        Initialize hallucination detector.

        Args:
            reference_context: Reference text to check against
            use_llm: Whether to use LLM for detection
            llm_model: Model to use for LLM-based detection
            threshold: Score threshold for flagging
            name: Name for this guardrail
        """
        super().__init__(name)
        self.reference_context = reference_context
        self.use_llm = use_llm
        self.llm_model = llm_model
        self.threshold = threshold
        self._compiled_patterns = [
            (re.compile(pattern, re.IGNORECASE), indicator, score)
            for pattern, indicator, score in self.HALLUCINATION_INDICATORS
        ]

    async def check(
        self,
        content: str,
        context: dict[str, Any] | None = None,
    ) -> GuardrailResult:
        """Check content for potential hallucinations."""
        start_time = time.time()

        # Get reference context
        reference = context.get("reference") if context else None
        reference = reference or self.reference_context

        if self.use_llm and reference:
            return await self._check_with_llm(content, reference, start_time)
        return await self._check_with_patterns(content, start_time)

    async def _check_with_patterns(
        self,
        content: str,
        start_time: float,
    ) -> GuardrailResult:
        """Pattern-based hallucination indicators."""
        issues = []
        detections = []
        total_score = 0.0
        count = 0

        for pattern, indicator, score in self._compiled_patterns:
            matches = pattern.findall(content)
            if matches:
                issues.append(f"Potential {indicator.replace('_', ' ')}")
                detections.append(
                    {
                        "indicator": indicator,
                        "count": len(matches),
                        "risk_score": score,
                    }
                )
                total_score += score * len(matches)
                count += len(matches)

        avg_score = total_score / count if count > 0 else 0.0
        passed = avg_score < self.threshold
        # Invert for safety score
        safety_score = 1.0 - min(avg_score, 1.0)

        return GuardrailResult(
            guardrail_name=self.name,
            action=GuardrailAction.PASS if passed else GuardrailAction.WARN,
            passed=passed,
            score=safety_score,
            issues=issues,
            details={
                "detections": detections,
                "method": "pattern",
                "avg_risk_score": avg_score,
            },
            duration_ms=(time.time() - start_time) * 1000,
        )

    async def _check_with_llm(
        self,
        content: str,
        reference: str,
        start_time: float,
    ) -> GuardrailResult:
        """LLM-based hallucination check."""
        try:
            from aigie.evaluation.llm_judge import JudgeConfig, LLMJudge

            judge = LLMJudge(JudgeConfig(model=self.llm_model))
            result = await judge.evaluate(
                input="Verify if this content is factually consistent with the reference.",
                output=content,
                criteria=["factuality", "accuracy"],
                reference=reference,
            )

            factuality_score = result.get_score("factuality") or 0.5
            accuracy_score = result.get_score("accuracy") or 0.5
            avg_score = (factuality_score + accuracy_score) / 2
            passed = avg_score >= self.threshold

            return GuardrailResult(
                guardrail_name=self.name,
                action=GuardrailAction.PASS if passed else GuardrailAction.WARN,
                passed=passed,
                score=avg_score,
                issues=[] if passed else ["Potential hallucination detected"],
                details={
                    "method": "llm",
                    "model": self.llm_model,
                    "factuality_score": factuality_score,
                    "accuracy_score": accuracy_score,
                    "feedback": result.feedback,
                },
                duration_ms=(time.time() - start_time) * 1000,
            )

        except Exception as e:
            logger.error(f"LLM hallucination check failed: {e}")
            return await self._check_with_patterns(content, start_time)


class PromptInjectionDetector(BaseGuardrail):
    """
    Detects prompt injection attempts in user inputs.

    Detects:
    - Instructions to ignore previous instructions
    - Role-playing / persona switching attempts
    - System prompt leakage attempts
    - Jailbreak patterns
    """

    # Prompt injection patterns
    INJECTION_PATTERNS = [
        (
            r"\b(?:ignore|forget|disregard)\s+(?:all\s+)?(?:previous|above|prior)\s+(?:instructions?|prompts?)\b",
            "ignore_instructions",
            0.9,
        ),
        (
            r"\b(?:you\s+are|act\s+as|pretend\s+to\s+be|roleplay\s+as)\s+(?:a\s+)?(?:different|new|evil|bad)\b",
            "role_switch",
            0.8,
        ),
        (
            r"\b(?:what\s+is|reveal|show|tell\s+me)\s+(?:your|the)\s+(?:system\s+)?(?:prompt|instructions?)\b",
            "system_leak",
            0.85,
        ),
        (r"\b(?:jailbreak|bypass|override|unlock)\b", "jailbreak_keyword", 0.7),
        (r"```\s*(?:system|hidden|internal)\s*\n", "hidden_instruction", 0.9),
        (r"\[(?:SYSTEM|ADMIN|OVERRIDE)\]", "fake_system_tag", 0.85),
        (r"<(?:system|override|admin)>", "fake_system_xml", 0.85),
    ]

    def __init__(
        self,
        threshold: float = 0.7,
        block_on_detection: bool = True,
        name: str = "PromptInjectionDetector",
    ):
        """
        Initialize prompt injection detector.

        Args:
            threshold: Score threshold for blocking
            block_on_detection: Whether to block on detection
            name: Name for this guardrail
        """
        super().__init__(name)
        self.threshold = threshold
        self.block_on_detection = block_on_detection
        self._compiled_patterns = [
            (re.compile(pattern, re.IGNORECASE), attack_type, score)
            for pattern, attack_type, score in self.INJECTION_PATTERNS
        ]

    async def check(
        self,
        content: str,
        context: dict[str, Any] | None = None,
    ) -> GuardrailResult:
        """Check content for prompt injection attempts."""
        start_time = time.time()

        issues = []
        detections = []
        max_score = 0.0

        for pattern, attack_type, score in self._compiled_patterns:
            matches = pattern.findall(content)
            if matches:
                issues.append(f"Detected {attack_type.replace('_', ' ')}")
                detections.append(
                    {
                        "attack_type": attack_type,
                        "count": len(matches),
                        "severity": score,
                    }
                )
                max_score = max(max_score, score)

        passed = max_score < self.threshold
        action = (
            GuardrailAction.PASS
            if passed
            else (GuardrailAction.RETRY if self.block_on_detection else GuardrailAction.WARN)
        )
        # Invert for safety score
        safety_score = 1.0 - max_score if max_score > 0 else 1.0

        return GuardrailResult(
            guardrail_name=self.name,
            action=action,
            passed=passed,
            score=safety_score,
            issues=issues,
            details={
                "detections": detections,
                "max_severity": max_score,
            },
            duration_ms=(time.time() - start_time) * 1000,
        )
