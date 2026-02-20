import json
from collections import OrderedDict, deque
from typing import Dict, List, Optional, Tuple


class ActionTracker:
    def __init__(self, window_size: int = 10) -> None:
        self.window_size = window_size
        self.action_history: deque = deque(maxlen=window_size)  # type: ignore[type-arg]
        self.action_outcomes: Dict[str, List[str]] = {}
        self.consecutive_repeats = 0
        self.last_action_sig: Optional[str] = None
        self.failed_actions: OrderedDict[str, None] = OrderedDict()
        self.request_urls: OrderedDict[str, int] = OrderedDict()

    def _action_signature(self, action: str, action_input: str) -> str:
        normalized_input = str(action_input).strip("\"'")
        return f"{action}:{normalized_input}"

    def _extract_request_url(self, action: str, action_input: str) -> Optional[str]:
        if action != "make_request":
            return None
        try:
            args = json.loads(action_input)
            return args.get("url")
        except (json.JSONDecodeError, AttributeError):
            return None

    def _is_failure_outcome(self, outcome: str) -> bool:
        outcome_stripped = outcome.strip()
        if outcome_stripped.startswith("Error"):
            return True
        outcome_lower = outcome_stripped.lower()
        failure_prefixes = [
            "failed to ",
            "request failed",
            "extraction failed",
            "download waiting failed",
            "wait failed",
            "screenshot failed",
            "python execution failed",
        ]
        return any(outcome_lower.startswith(prefix) for prefix in failure_prefixes)

    def record_action(
        self,
        action: str,
        action_input: str,
        outcome: str,
        state_hash: Optional[str] = None,
        element_text: Optional[str] = None,
    ) -> None:
        action_sig = self._action_signature(action, action_input)
        self.action_history.append(
            {
                "action": action,
                "input": action_input,
                "signature": action_sig,
                "outcome": outcome,
                "state": state_hash,
                "element_text": element_text,
            }
        )

        if action_sig not in self.action_outcomes:
            self.action_outcomes[action_sig] = []
        self.action_outcomes[action_sig].append(outcome)

        max_tracked = self.window_size * 2
        if self._is_failure_outcome(outcome):
            self.failed_actions.pop(action_sig, None)
            self.failed_actions[action_sig] = None
            while len(self.failed_actions) > max_tracked:
                self.failed_actions.popitem(last=False)

        request_url = self._extract_request_url(action, action_input)
        if request_url:
            self.request_urls[request_url] = self.request_urls.get(request_url, 0) + 1
            while len(self.request_urls) > max_tracked:
                self.request_urls.popitem(last=False)

        if action_sig == self.last_action_sig:
            self.consecutive_repeats += 1
        else:
            self.consecutive_repeats = 1
            self.last_action_sig = action_sig

    def detect_loop(self) -> Tuple[bool, str]:
        if len(self.action_history) < 3:
            return False, ""

        if self.consecutive_repeats >= 3:
            return (
                True,
                f"Action '{self.last_action_sig}' repeated {self.consecutive_repeats} times consecutively",
            )

        if len(self.action_history) >= 6:
            last_six = list(self.action_history)[-6:]
            sigs = [h["signature"] for h in last_six]
            if (
                sigs[0] == sigs[2] == sigs[4]
                and sigs[1] == sigs[3] == sigs[5]
                and sigs[0] != sigs[1]
            ):
                return True, f"Cyclic pattern detected: {sigs[0]} <-> {sigs[1]}"

        if len(self.action_history) >= 4:
            recent_actions = [h["action"] for h in list(self.action_history)[-4:]]
            if recent_actions.count("wait_for_download") >= 3:
                has_click = any(
                    h["action"] == "click" for h in list(self.action_history)[-4:]
                )
                if not has_click:
                    return (
                        True,
                        "Repeated wait_for_download without clicking new elements",
                    )

        if self.action_history:
            last = self.action_history[-1]
            request_url = self._extract_request_url(last["action"], last["input"])
            if request_url and self.request_urls.get(request_url, 0) >= 3:
                return (
                    True,
                    f"make_request to '{request_url}' called {self.request_urls[request_url]} times",
                )

        if len(self.action_history) >= 3:
            last_three = list(self.action_history)[-3:]
            if all(self._is_failure_outcome(h["outcome"]) for h in last_three):
                return True, "Last 3 actions all failed"

        return False, ""

    def should_try_different_action(self) -> Tuple[bool, str]:
        is_loop, reason = self.detect_loop()
        if not is_loop:
            return False, ""
        if not self.action_history:
            return False, ""

        current_action = self.action_history[-1]["action"]
        suggestions = {
            "click": "Try run_javascript to click via JS, press_key (Tab/Enter), or a different element.",
            "navigate": "Stop re-navigating. Interact with the current page content instead.",
            "wait_for_download": "Click a different download element before waiting again.",
            "make_request": "This URL has been requested multiple times. Try a different approach.",
        }
        suggestion = suggestions.get(
            current_action, "Try a completely different tool/action."
        )
        return True, f"{reason}. {suggestion}"

    def should_force_wait_for_download(self) -> Tuple[bool, str]:
        if not self.action_history:
            return False, ""

        download_keywords = [
            "download",
            "baixar",
            "export",
            "pdf",
            "csv",
            "xml",
            "report",
            "file",
            "arquivo",
        ]
        recent = list(self.action_history)[-5:]
        download_clicks = []
        wait_attempts = 0

        for entry in recent:
            if entry["action"] == "click":
                element_text = (entry.get("element_text") or "").lower()
                if any(kw in element_text for kw in download_keywords):
                    download_clicks.append(entry)
            elif entry["action"] == "wait_for_download":
                wait_attempts += 1

        if len(download_clicks) > 0 and wait_attempts == 0:
            return True, "Clicked download button but never tried wait_for_download."

        if len(download_clicks) >= 2 and wait_attempts < len(download_clicks):
            return (
                True,
                f"Clicked {len(download_clicks)} download buttons but only waited {wait_attempts} times.",
            )

        return False, ""

    def get_context_for_prompt(self) -> str:
        if not self.action_history:
            return ""

        is_loop, loop_reason = self.detect_loop()
        parts: List[str] = []

        action_counts: Dict[str, int] = {}
        for entry in self.action_history:
            sig = entry["signature"]
            action_counts[sig] = action_counts.get(sig, 0) + 1

        summary_lines = ["Recent actions:"]
        for sig, count in action_counts.items():
            action, input_val = sig.split(":", 1)
            if count > 1:
                summary_lines.append(f"  - {action}({input_val}) x {count} times")
            else:
                summary_lines.append(f"  - {action}({input_val})")
        parts.append("\n## Action History\n" + "\n".join(summary_lines))

        if is_loop:
            _, suggestion = self.should_try_different_action()
            parts.append(f"\nLOOP DETECTED: {loop_reason}")
            parts.append(f"SUGGESTION: {suggestion}")

        if self.consecutive_repeats >= 2:
            parts.append(
                f"\nWARNING: '{self.last_action_sig}' repeated {self.consecutive_repeats} times. "
                f"You MUST try something different."
            )

        if self.failed_actions:
            recent_sigs = [h["signature"] for h in list(self.action_history)[-3:]]
            relevant = [sig for sig in recent_sigs if sig in self.failed_actions]
            if relevant:
                parts.append(
                    f"\nFAILED ACTIONS (avoid repeating): {', '.join(set(relevant))}"
                )

        repeated_urls = {
            url: count for url, count in self.request_urls.items() if count >= 2
        }
        if repeated_urls:
            url_warnings = [f"{url} ({count}x)" for url, count in repeated_urls.items()]
            parts.append(
                f"\nREPEATED REQUEST URLs (do not request again): {', '.join(url_warnings)}"
            )

        should_force, force_reason = self.should_force_wait_for_download()
        if should_force:
            parts.append(f"\nREQUIRED ACTION: {force_reason}")

        return "\n".join(parts)
