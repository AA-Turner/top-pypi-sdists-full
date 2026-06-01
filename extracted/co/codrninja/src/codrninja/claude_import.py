"""Import sessions from Claude Code (~/.claude/projects/) into codrninja."""

import json
import os
from typing import Any, Dict, List, Optional


def _extract_text_content(message: Dict[str, Any]) -> str:
    """Pull text content out of Anthropic API message format."""
    content = message.get('message', {}).get('content', '')
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts: List[str] = []
        for block in content:
            if isinstance(block, dict):
                if block.get('type') == 'text':
                    parts.append(block.get('text', ''))
                elif block.get('type') == 'tool_result':
                    pass  # skip tool results
            elif isinstance(block, str):
                parts.append(block)
        return '\n'.join(p for p in parts if p).strip()
    return ''


def _reconstruct_chain(lines: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Reconstruct the main conversation chain from a Claude Code JSONL.
    Uses parentUuid linked-list traversal to find the canonical path.
    """
    if not lines:
        return []

    by_uuid: Dict[str, Dict] = {m['uuid']: m for m in lines if m.get('uuid')}
    referenced_as_parent = {m['parentUuid'] for m in lines if m.get('parentUuid')}

    # Leaf nodes: no other message points to them as parent, not sidechains
    leaves = [
        m for m in lines
        if m.get('uuid') not in referenced_as_parent
        and not m.get('isSidechain', False)
        and m.get('type') in ('user', 'assistant')
    ]

    if not leaves:
        # Fallback: sequential order
        result = []
        for m in lines:
            if m.get('type') in ('user', 'assistant') and not m.get('isSidechain', False):
                content = _extract_text_content(m)
                if content:
                    result.append({'role': m['type'], 'content': content})
        return result

    # Walk backwards from the newest leaf
    leaves.sort(key=lambda m: m.get('timestamp', ''), reverse=True)
    current: Optional[Dict] = leaves[0]
    chain: List[Dict] = []
    visited: set = set()

    while current and current.get('uuid') not in visited:
        visited.add(current.get('uuid'))
        if current.get('type') in ('user', 'assistant'):
            content = _extract_text_content(current)
            if content:
                chain.append({
                    'role': current['type'],
                    'content': content,
                    'timestamp': current.get('timestamp', ''),
                })
        parent_id = current.get('parentUuid')
        current = by_uuid.get(parent_id) if parent_id else None

    chain.reverse()
    return chain


def _read_jsonl(path: str) -> List[Dict[str, Any]]:
    lines: List[Dict] = []
    try:
        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            for raw in f:
                raw = raw.strip()
                if not raw:
                    continue
                try:
                    lines.append(json.loads(raw))
                except json.JSONDecodeError:
                    pass
    except (FileNotFoundError, PermissionError, OSError):
        pass
    return lines


def summarize_session(path: str) -> Optional[Dict[str, Any]]:
    """Quick scan of a JSONL file to get a session preview (first user msg + metadata)."""
    lines = _read_jsonl(path)
    if not lines:
        return None

    first_user_preview = ''
    msg_count = 0
    latest_ts = ''

    for m in lines:
        ts = m.get('timestamp', '')
        if ts and ts > latest_ts:
            latest_ts = ts
        if m.get('type') in ('user', 'assistant') and not m.get('isSidechain', False):
            msg_count += 1
        if m.get('type') == 'user' and not first_user_preview and not m.get('isSidechain', False):
            first_user_preview = _extract_text_content(m)[:120]

    if msg_count == 0:
        return None

    session_id = os.path.splitext(os.path.basename(path))[0]
    return {
        'session_id': session_id,
        'path': path,
        'preview': first_user_preview or '(no preview)',
        'message_count': msg_count,
        'updated_at': latest_ts,
        'project_hash': os.path.basename(os.path.dirname(path)),
    }


def list_claude_sessions() -> List[Dict[str, Any]]:
    """Scan ~/.claude/projects/ and return all importable sessions."""
    base = os.path.expanduser('~/.claude/projects')
    if not os.path.isdir(base):
        return []

    sessions: List[Dict[str, Any]] = []
    for proj_dir in os.listdir(base):
        proj_path = os.path.join(base, proj_dir)
        if not os.path.isdir(proj_path):
            continue
        for fname in os.listdir(proj_path):
            if not fname.endswith('.jsonl'):
                continue
            summary = summarize_session(os.path.join(proj_path, fname))
            if summary:
                sessions.append(summary)

    sessions.sort(key=lambda s: s.get('updated_at', ''), reverse=True)
    return sessions


def import_session(path: str) -> List[Dict[str, Any]]:
    """
    Parse a Claude Code JSONL file and return a list of
    { role, content, timestamp } dicts in chronological order.
    """
    lines = _read_jsonl(path)
    return _reconstruct_chain(lines)
