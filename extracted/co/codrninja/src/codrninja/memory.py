"""Ninja memory system — CLAUDE.md stack + persistent fact store."""

import json
import os
import re
from datetime import datetime
from typing import List, Dict, Any, Optional


# ── CLAUDE.md loading ─────────────────────────────────────────────────────────

_INCLUDE_RE = re.compile(r'^@([^\s]+)', re.MULTILINE)
_MAX_INCLUDE_DEPTH = 5


def _read_file_safe(path: str) -> str:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except (FileNotFoundError, PermissionError, OSError):
        return ''


def _resolve_includes(content: str, base_dir: str, depth: int = 0) -> str:
    """Expand @path/to/file.md directives (max 5 levels deep)."""
    if depth >= _MAX_INCLUDE_DEPTH:
        return content

    def replace_include(m: re.Match) -> str:
        inc_path = os.path.join(base_dir, m.group(1))
        inc_content = _read_file_safe(inc_path)
        if inc_content:
            return _resolve_includes(inc_content, os.path.dirname(inc_path), depth + 1)
        return ''

    return _INCLUDE_RE.sub(replace_include, content)


def _load_claudemd_file(path: str) -> str:
    """Load a CLAUDE.md file, resolving @includes."""
    content = _read_file_safe(path)
    if not content:
        return ''
    return _resolve_includes(content, os.path.dirname(os.path.abspath(path)))


def load_claudemd_stack() -> Optional[str]:
    """
    Load the CODRNINJA.md stack:
      1. User global   — ~/.codrninja/CODRNINJA.md
      2. Project       — ./CODRNINJA.md  and  ./.codrninja/CODRNINJA.md
      3. Local private — ./CODRNINJA.local.md  (gitignored)

    Later layers take precedence (higher weight for the model).
    Returns None if no CODRNINJA.md files found.
    """
    cwd = os.getcwd()
    home = os.path.expanduser('~')

    candidates = [
        os.path.join(home, '.codrninja', 'CODRNINJA.md'),     # user global
        os.path.join(cwd, 'CODRNINJA.md'),                    # project root
        os.path.join(cwd, '.codrninja', 'CODRNINJA.md'),      # project .codrninja/
        os.path.join(cwd, 'CODRNINJA.local.md'),              # local private
    ]

    parts: List[str] = []
    for path in candidates:
        text = _load_claudemd_file(path)
        if text.strip():
            parts.append(text.strip())

    if not parts:
        return None

    return '\n\n'.join(parts)


# ── Fact store (remember/recall/forget tools) ─────────────────────────────────

def _project_memory_path() -> str:
    return os.path.join(os.getcwd(), '.codrninja', 'memory.json')


def _global_memory_path() -> str:
    return os.path.expanduser('~/.codrninja/memory/global.json')


def _load_facts(path: str) -> List[Dict[str, Any]]:
    try:
        with open(path, 'r') as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def _save_facts(path: str, facts: List[Dict[str, Any]]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        json.dump(facts, f, indent=2)


def remember(fact: str, scope: str = 'project') -> str:
    """Store an important fact to remember across sessions."""
    path = _project_memory_path() if scope == 'project' else _global_memory_path()
    facts = _load_facts(path)
    key = fact[:60].replace(' ', '-').lower()
    facts.append({'key': key, 'fact': fact, 'scope': scope, 'created_at': datetime.utcnow().isoformat()})
    _save_facts(path, facts)
    return f'Remembered ({scope}): {fact}'


def recall(scope: str = 'all') -> str:
    """List all remembered facts."""
    parts: List[str] = []
    if scope in ('project', 'all'):
        proj = _load_facts(_project_memory_path())
        if proj:
            parts.append('## Project Memory')
            parts.extend(f'- {m["fact"]}' for m in proj)
    if scope in ('global', 'all'):
        glob = _load_facts(_global_memory_path())
        if glob:
            parts.append('## Global Memory')
            parts.extend(f'- {m["fact"]}' for m in glob)
    return '\n'.join(parts) if parts else 'No memories stored yet.'


def forget(fact_key_or_text: str, scope: str = 'project') -> str:
    """Remove a remembered fact by key or matching text."""
    path = _project_memory_path() if scope == 'project' else _global_memory_path()
    facts = _load_facts(path)
    before = len(facts)
    facts = [
        m for m in facts
        if m.get('key') != fact_key_or_text and fact_key_or_text.lower() not in m.get('fact', '').lower()
    ]
    _save_facts(path, facts)
    removed = before - len(facts)
    return f'Removed {removed} memory entry(ies).' if removed else 'No matching memory found.'


def load_memory_context() -> Optional[str]:
    """
    Build the full memory context string injected at start of each agent run:
      - CLAUDE.md stack (project + user instructions)
      - Remembered facts (JSON store)
    """
    parts: List[str] = []

    claudemd = load_claudemd_stack()
    if claudemd:
        parts.append(claudemd)

    proj = _load_facts(_project_memory_path())
    glob = _load_facts(_global_memory_path())
    if proj or glob:
        fact_parts = ['## Ninja Memory (remembered facts from previous sessions)']
        for m in glob:
            fact_parts.append(f'- {m["fact"]}')
        for m in proj:
            fact_parts.append(f'- {m["fact"]}')
        parts.append('\n'.join(fact_parts))

    return '\n\n'.join(parts) if parts else None
