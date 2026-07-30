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
from ..tools.function_schema import BINGO_TOOLS, to_openai_format, to_anthropic_format
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

        self._max_loops = 0
        self._nudge_max = 5
        self._loop_count = 0
        # Stagnation detection — 도구 호출은 계속하는데 새 발견이 없는 경우
        self._no_progress_streak = 0
        self._NO_PROGRESS_MAX = 40  # 40 연속 no-progress → finalize
        self._tool_sig_window: collections.deque = collections.deque(maxlen=30)
        self._prev_finding_count = 0

        # Zero Hallucination Engine — model text claim validation
        from ..core.zero_hal_v5 import ZeroHalEngine
        self.zero_hal = ZeroHalEngine(session_target=target, lang=self.lang)
        # Rolling window of recent exec outputs fed into the HAL gate (up to 20 × 2 KB)
        self._recent_exec_outputs: list[str] = []
        # Pending user-turn injections: HAL corrections + depth nudges, drained before each _call_model()
        self._pending_injections: list[str] = []
        # Track which finding IDs already triggered a depth nudge (avoid duplicate spam)
        self._nudged_finding_ids: set[str] = set()

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
                # Track signatures before execution
                for tc in tool_calls:
                    self._tool_sig_window.append(self._make_tool_sig(tc))
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
                # Stagnation check — new findings reset streak
                current_count = len(self.findings._findings) + len(self.findings._quarantined)
                if current_count > self._prev_finding_count:
                    self._no_progress_streak = 0
                    self._prev_finding_count = current_count
                else:
                    self._no_progress_streak += 1
                if self._is_stagnating():
                    self.console.print(
                        f"\n[#ffd600]⚡ Stagnation: {self._no_progress_streak} loops with no new findings — generating report.[/]"
                    )
                    self._finalize()
                    return
                self._maybe_compact()
                continue

            # 3. Text only → HAL gate then add to history, continue
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
                    continue  # retry without counting as nudge
                elif _hal.warned and _hal.inject_message:
                    if self._event_bus:
                        self._event_bus.push_event("hal_event", {"reason": "warned", "blocked": False, "loop": self._loop_count})
                    self._pending_injections.append(_hal.inject_message)
            nudge_count += 1
            if nudge_count > self._nudge_max:
                self._finalize()
                return
            continue

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
        if self._is_claude:
            return to_anthropic_format(BINGO_TOOLS)
        return BINGO_TOOLS

    @staticmethod
    def _make_tool_sig(tc) -> str:
        """Tool call signature for duplicate detection."""
        args_str = _json.dumps(tc.arguments, sort_keys=True, ensure_ascii=False, default=str)[:200]
        return hashlib.md5(f"{tc.name}:{args_str}".encode()).hexdigest()[:8]

    def _is_stagnating(self) -> bool:
        """True when the loop is stuck — no new findings and repeated tool calls."""
        if self._no_progress_streak >= self._NO_PROGRESS_MAX:
            return True
        # 30-call window: if < 20% unique signatures → model repeating same calls
        if len(self._tool_sig_window) >= 20:
            window = list(self._tool_sig_window)
            if len(set(window)) / len(window) < 0.2:
                return True
        return False

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
        return self.findings.process(
            result.output,
            code_snippet=code_snippet,
            execution_context={"tool_name": result.name, "executed": True},
        )

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
        """Background thread: summarize only actual tool results — discard model text."""
        tool_facts = [
            f"[{m.name or 'tool'}] {m.content[:400]}"
            for m in messages if m.role == "tool"
        ]
        if not tool_facts:
            self.context.set_compaction_summary(
                "[No tool results in this segment — nothing confirmed by execution]"
            )
            return
        prompt = (
            "Summarize ONLY these actual tool execution results as bullet facts. "
            "Do NOT include any model analysis or unconfirmed claims. "
            "Each bullet = one confirmed tool observation:\n\n"
            + "\n".join(f"- {f}" for f in tool_facts[:40])
        )
        try:
            summary_parts = []
            for chunk in self._model.chat_stream([
                {"role": "user", "content": prompt}
            ]):
                if chunk.text:
                    summary_parts.append(chunk.text)
            self.context.set_compaction_summary("".join(summary_parts))
        except Exception:
            self.context.set_compaction_summary("[Compaction failed — continuing with recent context]")

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

        Prevents the model from drifting to new test vectors immediately after
        discovering a high-value candidate that still needs verification/exploitation.
        """
        from ..tools.findings_exporter import CONF_CONFIRMED, CONF_PROBABLE
        if finding.confidence not in (CONF_CONFIRMED, CONF_PROBABLE):
            return
        if finding.id in self._nudged_finding_ids:
            return  # already queued for this finding
        self._nudged_finding_ids.add(finding.id)
        _TOOL_HINTS: dict[str, str] = {
            "sqli": "sqli_autoexploit — require boolean TRUE≠FALSE ≥200B diff OR ≥3 time-delay samples >2s above baseline",
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
                f"证据: {evidence_snip}\n\n"
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

    def _load_skills(self, target: str) -> str:
        """Load relevant skills for target."""
        try:
            from ..skills.engine import SkillEngine
            se = SkillEngine()
            results = se.search(target)
            if results:
                snippets = []
                for r in results[:3]:
                    prompt = se.get_skill_prompt(r.get("id", ""))
                    if prompt:
                        snippets.append(prompt[:1000])
                return "\n".join(snippets)
        except Exception:
            pass
        return ""

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
