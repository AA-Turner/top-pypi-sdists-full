import hashlib
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse


@dataclass
class ActionOutcome:
    action: str
    action_input: str
    page_signature: str
    success: bool
    observation_snippet: str
    element_type: Optional[str] = None
    step_number: int = 0


@dataclass
class ActionAdvice:
    risk_score: float
    recommended_actions: List[str]
    actions_to_avoid: List[str]
    reasoning: str
    successful_patterns: List[str]


class ActionIntelligence:
    def __init__(self) -> None:
        self.outcomes: List[ActionOutcome] = []
        self.action_stats: Dict[str, Dict[str, int]] = defaultdict(
            lambda: {"success": 0, "failure": 0}
        )
        self.page_action_stats: Dict[str, Dict[str, Dict[str, int]]] = defaultdict(
            lambda: defaultdict(lambda: {"success": 0, "failure": 0})
        )
        self.successful_sequences: List[Tuple[str, str]] = []
        self.loop_causing_actions: Dict[str, int] = defaultdict(int)
        self.element_success: Dict[str, List[str]] = defaultdict(list)

    def get_page_signature(
        self,
        url: str,
        element_count: int,
        key_elements: Optional[List[Dict]] = None,  # type: ignore[type-arg]
    ) -> str:
        parsed = urlparse(url)
        domain = parsed.netloc
        path_parts = [p for p in parsed.path.split("/") if p]
        normalized_path = "/".join(
            "{id}" if p.isdigit() or len(p) > 20 else p for p in path_parts[:3]
        )
        element_bucket = (element_count // 50) * 50
        element_types = ""
        if key_elements:
            types = sorted(set(e.get("tag", "unknown") for e in key_elements[:10]))
            element_types = ",".join(types[:5])
        signature = f"{domain}|{normalized_path}|{element_bucket}|{element_types}"
        return hashlib.md5(signature.encode()).hexdigest()[:12]

    def record_outcome(
        self,
        action: str,
        action_input: str,
        page_signature: str,
        success: bool,
        observation: str,
        element_type: Optional[str] = None,
        step_number: int = 0,
    ) -> None:
        outcome = ActionOutcome(
            action=action,
            action_input=action_input,
            page_signature=page_signature,
            success=success,
            observation_snippet=observation[:200],
            element_type=element_type,
            step_number=step_number,
        )
        self.outcomes.append(outcome)

        key = "success" if success else "failure"
        self.action_stats[action][key] += 1
        self.page_action_stats[page_signature][action][key] += 1

        if success and len(self.outcomes) >= 2:
            prev = self.outcomes[-2]
            if prev.success:
                self.successful_sequences.append((prev.action, action))

        if success and element_type:
            if action not in self.element_success[element_type]:
                self.element_success[element_type].append(action)

        self._check_loop_pattern(action, action_input)

    def _check_loop_pattern(self, action: str, action_input: str) -> None:
        if len(self.outcomes) < 3:
            return
        recent = self.outcomes[-3:]
        action_sig = f"{action}:{action_input}"
        if all(f"{o.action}:{o.action_input}" == action_sig for o in recent):
            self.loop_causing_actions[action] += 1
        if len(self.outcomes) >= 4:
            last_four = self.outcomes[-4:]
            sigs = [f"{o.action}:{o.action_input}" for o in last_four]
            if sigs[0] == sigs[2] and sigs[1] == sigs[3]:
                self.loop_causing_actions[last_four[0].action] += 1
                self.loop_causing_actions[last_four[1].action] += 1

    def predict_loop_risk(
        self, proposed_action: str, proposed_input: str, page_signature: str
    ) -> float:
        risk = 0.0
        if proposed_action in self.loop_causing_actions:
            loop_count = self.loop_causing_actions[proposed_action]
            risk += min(0.3 * loop_count, 0.6)
        if self.outcomes:
            last = self.outcomes[-1]
            if last.action == proposed_action and last.action_input == proposed_input:
                risk += 0.4
            elif last.action == proposed_action:
                risk += 0.2
        if len(self.outcomes) >= 2:
            prev_prev = self.outcomes[-2]
            if prev_prev.action == proposed_action:
                risk += 0.3
        page_stats = self.page_action_stats.get(page_signature, {})
        action_stat = page_stats.get(proposed_action, {"success": 0, "failure": 0})
        total = action_stat["success"] + action_stat["failure"]
        if total > 0 and action_stat["failure"] / total > 0.5:
            risk += 0.2
        return min(risk, 1.0)

    def get_recommendations(
        self,
        page_signature: str,
        last_action: Optional[str] = None,
        last_observation: Optional[str] = None,
        available_actions: Optional[List[str]] = None,
    ) -> ActionAdvice:
        recommended: List[str] = []
        to_avoid: List[str] = []
        successful_patterns: List[str] = []
        reasoning_parts: List[str] = []

        page_stats = self.page_action_stats.get(page_signature, {})
        for action, stats in page_stats.items():
            total = stats["success"] + stats["failure"]
            if total > 0:
                rate = stats["success"] / total
                if rate > 0.7 and stats["success"] >= 2:
                    recommended.append(action)
                    successful_patterns.append(
                        f"{action} worked {stats['success']}/{total} times on similar pages"
                    )
                elif rate < 0.3 and stats["failure"] >= 2:
                    to_avoid.append(action)

        if last_action:
            good_followups = [
                next_a
                for prev, next_a in self.successful_sequences
                if prev == last_action
            ]
            for followup in set(good_followups):
                if followup not in recommended:
                    recommended.append(followup)
                    count = good_followups.count(followup)
                    successful_patterns.append(
                        f"{followup} often succeeds after {last_action} ({count}x)"
                    )

        for action, count in self.loop_causing_actions.items():
            if count >= 2 and action not in to_avoid:
                to_avoid.append(action)
                reasoning_parts.append(f"Avoid {action} - caused {count} loops")

        if last_observation and self.outcomes and not self.outcomes[-1].success:
            reasoning_parts.append(
                f"Last action {self.outcomes[-1].action} failed, consider alternatives"
            )

        if recommended:
            reasoning_parts.insert(
                0, f"Recommended based on past success: {', '.join(recommended[:3])}"
            )
        if to_avoid:
            reasoning_parts.append(f"Actions to avoid: {', '.join(to_avoid[:3])}")
        if not reasoning_parts:
            reasoning_parts.append("No strong patterns detected yet, exploring...")

        risk_score = 0.0
        if last_action and last_action in self.loop_causing_actions:
            risk_score += 0.3
        if self.outcomes and not self.outcomes[-1].success:
            risk_score += 0.2

        return ActionAdvice(
            risk_score=min(risk_score, 1.0),
            recommended_actions=recommended[:5],
            actions_to_avoid=to_avoid[:5],
            reasoning=" | ".join(reasoning_parts),
            successful_patterns=successful_patterns[:5],
        )

    def was_action_successful(
        self, observation: str, action: Optional[str] = None
    ) -> bool:
        obs_lower = observation.lower()
        failure_indicators = [
            "error:",
            "failed",
            "not found",
            "timeout",
            "exception",
            "blocked",
            "captcha",
            "invalid",
            "cannot",
            "unable",
            "traceback",
            "syntaxerror",
            "typeerror",
            "valueerror",
        ]
        success_indicators = [
            "success",
            "completed",
            "navigated",
            "clicked",
            "typed",
            "extracted",
            "downloaded",
            "found",
            "loaded",
            "submitted",
            "saved",
        ]
        stagnation_indicators = [
            "same result",
            "no change",
            "already",
            "still waiting",
            "empty result",
        ]
        failure_score = sum(1 for ind in failure_indicators if ind in obs_lower)
        success_score = sum(1 for ind in success_indicators if ind in obs_lower)
        stagnation_score = sum(1 for ind in stagnation_indicators if ind in obs_lower)

        if action in ("run_python", "run_javascript"):
            if len(observation.strip()) < 20:
                return False
            code_errors = [
                "traceback",
                "syntaxerror",
                "error:",
                "exception",
                "referenceerror",
            ]
            if any(err in obs_lower for err in code_errors):
                return False

        if failure_score > 0 and success_score == 0:
            return False
        if stagnation_score > 0 and success_score == 0:
            return False
        if success_score > 0 and failure_score == 0:
            return True
        # When no indicators match (both scores are 0), assume success —
        # normal page summaries and neutral output should not count as failure.
        if failure_score == 0 and success_score == 0:
            return True
        return success_score > failure_score + stagnation_score

    def get_context_for_prompt(self) -> str:
        if not self.outcomes:
            return ""
        parts: List[str] = []
        recent = self.outcomes[-5:]
        success_count = sum(1 for o in recent if o.success)
        parts.append(f"Recent: {success_count}/{len(recent)} actions succeeded")

        working_actions = [
            action
            for action, stats in self.action_stats.items()
            if stats["success"] > stats["failure"] and stats["success"] >= 2
        ]
        if working_actions:
            parts.append(f"Working well: {', '.join(working_actions[:3])}")
        if self.loop_causing_actions:
            avoid = list(self.loop_causing_actions.keys())[:3]
            parts.append(f"Avoid (caused loops): {', '.join(avoid)}")

        last = self.outcomes[-1]
        status = "succeeded" if last.success else "FAILED"
        parts.append(f"Last: {last.action} {status}")

        return "\n\n## Action Intelligence\n" + "\n".join(f"- {p}" for p in parts)
