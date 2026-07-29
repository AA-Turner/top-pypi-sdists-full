"""Agent Loop — Claude Code CLI style execution loop.

Model → tool_use → executor runs → results fed back → repeat.
No legacy code block parsing. No heuristic drift detection.
Structure prevents hallucination and drift by design.
"""
from __future__ import annotations

import threading
from typing import Iterator

from rich.console import Console

from ..models.base import StreamChunk
from ..models.base import ToolCall as ModelToolCall
from ..models.registry import ModelRegistry
from ..tools.function_schema import BINGO_TOOLS, to_openai_format, to_anthropic_format
from ..tools.findings_exporter import FindingsExporter
from ..config import BingoConfig
from .context import ContextManager, Message
from .executor import ToolExecutor, ToolCall, ToolResult
from .system_prompt import build_system_prompt
from .reporter import generate_report, generate_html_report, save_report, save_html_report


class AgentLoop:
    """Claude Code CLI architecture agent loop for penetration testing."""

    def __init__(self, target: str, config: BingoConfig, console: Console | None = None):
        self.target = target
        self.config = config
        self.console = console or Console()
        self.lang = config.lang or "en"

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

    def run(self, user_message: str) -> None:
        """Execute the full agent loop for a user message."""
        self.context.append_user(user_message)
        nudge_count = 0

        while True:
            self._loop_count += 1

            # 1. Call model
            response_text, tool_calls = self._call_model()

            # 2. If tool calls → execute and continue
            if tool_calls:
                nudge_count = 0
                if response_text:
                    self.context.append_assistant(response_text)
                results = self.executor.run_tools([
                    ToolCall(id=tc.id, name=tc.name, arguments=tc.arguments)
                    for tc in tool_calls
                ])
                for r in results:
                    self.context.append_tool_result(r.tool_call_id, r.name, r.content)
                    self._process_evidence(r)
                    self._extract_related_domains(r)
                    self._display_tool_result(r)
                self._maybe_compact()
                continue

            # 3. Text only → add to history, continue loop (model will call tools next)
            self.context.append_assistant(response_text)
            nudge_count += 1
            if nudge_count > self._nudge_max:
                self._finalize()
                return
            # No nudge injection — just loop back and call model again
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

    def _process_evidence(self, result: ToolResult) -> None:
        """Feed tool output through the evidence ladder."""
        if result.error:
            return
        self.findings.process(
            result.output,
            code_snippet=f"{result.name}",
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
        else:
            preview = result.output[:100].replace("\n", " ")
            self.console.print(Text(f"  ✓ {result.name}: {preview}...", style="#546e7a"))

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
        """Background thread: summarize old messages."""
        content = "\n".join(
            f"[{m.role}] {m.content[:500]}" for m in messages
        )
        prompt = (
            "Summarize the following conversation history in 500 words or less. "
            "Focus on: target information discovered, actions taken, findings, "
            "and current attack state. Be factual — only include what the tool results showed.\n\n"
            + content[:30000]
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
