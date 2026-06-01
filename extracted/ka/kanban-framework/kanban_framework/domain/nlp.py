from __future__ import annotations
import re
from kanban_framework.types import NLPResult


def extract_task_id(text: str) -> str | None:
    """Extract TASK-NNN from natural language text. Useful utility for LLM-assisted routing."""
    m = re.search(r"TASK-(\d{1,3})", text, re.IGNORECASE)
    if m:
        return f"TASK-{int(m.group(1)):03d}"
    return None


# Work-intent patterns: verbs that imply "do/create/implement something"
_WORK_VERBS = re.compile(
    r"(?:帮我|处理|实现|做|开发|写|添加|增加|修复|fix|create|build|implement|add|refactor|重构|改进|优化|新增|搭建)",
    re.IGNORECASE,
)

# Query-intent patterns: verbs that imply "show/check status"
_QUERY_VERBS = re.compile(
    r"(?:看看|查看|状态|进度|怎么样|什么|有没有|show|status|list|list)",
    re.IGNORECASE,
)

# Knowledge-management patterns: phrases that imply knowledge base operations (#313)
_KNOWLEDGE_PATTERNS = re.compile(
    r"(?:添加知识|补充知识|记录经验|知识条目|知识库|knowledge\s+(?:add|import|teach|learn))",
    re.IGNORECASE,
)


def detect_work_intent(text: str) -> dict:
    """Detect whether natural language input expresses work/query/knowledge intent.

    Returns dict with:
      - intent: "work" | "query" | "knowledge" | "ambiguous"
      - suggested_command: "create" | "status" | "knowledge add" | None
      - has_task_id: bool
      - needs_active_task_check: bool — when True, orchestrator should check
        for existing active tasks via `kanban status` before creating a new one.
    """
    lower = text.lower()
    has_task_id = extract_task_id(text) is not None
    is_work = bool(_WORK_VERBS.search(lower))
    is_query = bool(_QUERY_VERBS.search(lower))
    is_knowledge = bool(_KNOWLEDGE_PATTERNS.search(lower))

    # Knowledge intent overrides work when both match (#313)
    if is_knowledge:
        return {
            "intent": "knowledge", "suggested_command": "knowledge add",
            "has_task_id": False, "needs_active_task_check": False,
        }
    if has_task_id and is_work:
        return {"intent": "work", "suggested_command": "run", "has_task_id": True, "needs_active_task_check": False}
    if is_work and not is_query:
        return {
            "intent": "work", "suggested_command": "create",
            "has_task_id": has_task_id,
            "needs_active_task_check": not has_task_id,
        }
    if is_query and not is_work:
        return {"intent": "query", "suggested_command": "status", "has_task_id": has_task_id, "needs_active_task_check": False}
    return {"intent": "ambiguous", "suggested_command": None, "has_task_id": has_task_id, "needs_active_task_check": False}


def parse_nlp(text: str) -> NLPResult:
    """Deprecated: keyword matching replaced by LLM inference via cmd_nlp."""
    return NLPResult(success=False, command="unknown", task_id=extract_task_id(text))
