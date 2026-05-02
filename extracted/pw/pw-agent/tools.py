"""Local tools that the agent can execute on the user's machine."""

import os
import glob as glob_mod
import subprocess
import re
import json
import urllib.parse

import requests


TOOL_DEFINITIONS = [
    {
        "name": "read_file",
        "description": "Read a file. Shows 300 lines by default. For large files, use offset to read further (e.g. offset=300 for next chunk).",
        "parameters": {
            "path": {"type": "string", "description": "File path (relative to working directory)"},
            "offset": {"type": "integer", "description": "Start line (0-based). Default 0."},
            "limit": {"type": "integer", "description": "Max lines to return. Default 300."}
        },
        "required": ["path"]
    },
    {
        "name": "write_file",
        "description": "Create a new file or completely overwrite an existing file with new content.",
        "parameters": {
            "path": {"type": "string", "description": "File path (relative to working directory)"},
            "content": {"type": "string", "description": "The full file content to write"}
        },
        "required": ["path", "content"]
    },
    {
        "name": "edit_file",
        "description": "Replace a specific string in a file. The old_str must match exactly (including whitespace/indentation). Use this for targeted edits instead of rewriting whole files.",
        "parameters": {
            "path": {"type": "string", "description": "File path (relative to working directory)"},
            "old_str": {"type": "string", "description": "The exact string to find and replace"},
            "new_str": {"type": "string", "description": "The replacement string"}
        },
        "required": ["path", "old_str", "new_str"]
    },
    {
        "name": "bash",
        "description": "Run a shell command and return its output. Use for running tests, git commands, installing packages, etc.",
        "parameters": {
            "command": {"type": "string", "description": "The bash command to execute"}
        },
        "required": ["command"]
    },
    {
        "name": "list_files",
        "description": "List files matching a glob pattern. Use to explore project structure.",
        "parameters": {
            "pattern": {"type": "string", "description": "Glob pattern (e.g. '**/*.py', 'src/*.ts')"}
        },
        "required": ["pattern"]
    },
    {
        "name": "str_replace",
        "description": "Replace a block of text in a file with new text. More robust than edit_file for multi-line blocks.",
        "parameters": {
            "path": {"type": "string", "description": "File path"},
            "old_str": {"type": "string", "description": "The exact block of text to replace"},
            "new_str": {"type": "string", "description": "The new text to insert"}
        },
        "required": ["path", "old_str", "new_str"]
    },
    {
        "name": "batch",
        "description": "Execute multiple tool calls in parallel. Useful for reading multiple files or running multiple searches at once.",
        "parameters": {
            "calls": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "tool": {"type": "string"},
                        "args": {"type": "object"}
                    }
                },
                "description": "List of tool calls: [{'tool': 'read_file', 'args': {'path': '...'}}, ...]"
            }
        },
        "required": ["calls"]
    },
    {
        "name": "web_search",
        "description": "Search the web for current information. Use when the user asks about recent events, library docs, error messages, or anything you might not know. Returns a list of results with titles, URLs, and snippets.",
        "parameters": {
            "query": {"type": "string", "description": "Search query (be specific and natural — like a Google search)"},
            "max_results": {"type": "integer", "description": "Max results to return. Default 5, max 10."}
        },
        "required": ["query"]
    },
    {
        "name": "web_fetch",
        "description": "Fetch the contents of a URL and return readable text (HTML stripped). Use after web_search to read a specific result, or to fetch any known URL like API docs.",
        "parameters": {
            "url": {"type": "string", "description": "Full URL to fetch (must start with http:// or https://)"},
            "max_chars": {"type": "integer", "description": "Max chars to return. Default 8000."}
        },
        "required": ["url"]
    },
    {
        "name": "spawn_agent",
        "description": "Delegate a focused task to a fresh subagent. The subagent runs in its own conversation, performs the task, and returns just the final answer. Use for: independent exploration ('find all callers of foo()'), parallelizable work, or tasks with large intermediate results that would clutter your main context.",
        "parameters": {
            "task": {"type": "string", "description": "Self-contained task description. The subagent has no memory of your conversation, so include all needed context."}
        },
        "required": ["task"]
    },
    {
        "name": "spawn_agents",
        "description": "Delegate multiple INDEPENDENT tasks to subagents that run in parallel. Use when you have several unrelated subtasks that can run concurrently. Returns a list of answers in the same order as the input tasks.",
        "parameters": {
            "tasks": {"type": "array", "description": "List of self-contained task descriptions to run in parallel."}
        },
        "required": ["tasks"]
    },
    {
        "name": "search_codebase",
        "description": "Semantic search over the indexed project codebase. Returns the most relevant code chunks for a natural-language query. Faster than grep when you don't know the exact symbol — search by intent ('how does auth work', 'where do we handle errors'). Requires the codebase to be indexed first (the user runs /index).",
        "parameters": {
            "query": {"type": "string", "description": "Natural-language search query (be specific about what you're looking for)"},
            "top_k": {"type": "integer", "description": "Max chunks to return. Default 8, max 20."}
        },
        "required": ["query"]
    },
    {
        "name": "speak_text",
        "description": "Convert text to speech via the user's fleet TTS service and play it through their speakers. Use sparingly — only when the user explicitly asks you to speak, sing, read aloud, or when /voice mode is on. Requires an audio service running on a fleet GPU (audio-chatterbox / audio-fish / audio-qwen-tts / audio-dia).",
        "parameters": {
            "text": {"type": "string", "description": "Text to speak. Keep it under 4000 chars."},
            "voice": {"type": "string", "description": "Optional: specific TTS model (audio-chatterbox, audio-fish, audio-qwen-tts, audio-dia). Defaults to whatever's running."}
        },
        "required": ["text"]
    },
    {
        "name": "query_fleet",
        "description": "Discover other pw-agent instances running on this machine (or shared fleet). Returns each sibling agent's working directory, git branch, active model, recent files, and how long ago they were active. Use when the user asks 'what am I working on elsewhere', 'are there other sessions', or wants to coordinate across terminals.",
        "parameters": {
            "filter": {"type": "string", "description": "Optional filter (currently ignored — returns all live siblings)"}
        },
        "required": []
    },
]

# Commands that are always blocked
BLOCKED_COMMANDS = [
    "rm -rf /", "rm -rf /*", "mkfs", "dd if=", ":(){", "fork bomb",
    "chmod -R 777 /", "shutdown", "reboot", "halt", "poweroff",
]

# Global auto-approve flag — set by --yes flag
AUTO_APPROVE = False


def _resolve_path(path: str) -> str:
    """Resolve a path relative to the working directory."""
    if os.path.isabs(path):
        return path
    return os.path.abspath(path)


def read_file(path: str, offset: int = 0, limit: int = 300) -> str:
    """Read a file and return its contents. Supports offset/limit for large files."""
    full_path = _resolve_path(path)
    if not os.path.exists(full_path):
        return f"Error: File not found: {path}"
    if os.path.isdir(full_path):
        return f"Error: {path} is a directory, not a file"
    try:
        with open(full_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
        lines = content.split("\n")
        total = len(lines)

        # Apply offset and limit
        start = max(0, offset)
        end = min(total, start + limit)
        selected = lines[start:end]

        header = ""
        footer = ""
        if start > 0 or end < total:
            header = f"[File has {total} lines, showing {start + 1}-{end}]\n"
            if end < total:
                footer = f"\n... [{total - end} more lines — use read_file with offset={end}]"

        numbered = "\n".join(f"{start + i + 1}: {line}" for i, line in enumerate(selected))
        return f"{header}{numbered}{footer}"
    except Exception as e:
        return f"Error reading {path}: {e}"


def write_file(path: str, content: str) -> str:
    """Write content to a file."""
    full_path = _resolve_path(path)
    try:
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        lines = content.count("\n") + 1
        return f"Wrote {lines} lines to {path}"
    except Exception as e:
        return f"Error writing {path}: {e}"


def _closest_block_hint(content: str, old_str: str, path: str) -> str:
    """Find the line range in `content` most similar to `old_str` and return
    a unified-diff hint so the model can fix whitespace/indent drift on its
    next attempt. Returns "" when nothing is close enough (ratio < 0.6) or
    the file is too small to scan.

    Without this, smaller models (Gemma 26B, DeepSeek V2, qwen-coder ≤32B)
    hit str_replace mismatch → silent ✗ → re-read the same file → conclude
    nothing changed → give up with the edit unshipped.
    """
    try:
        import difflib
        old_lines = old_str.splitlines()
        file_lines = content.splitlines()
        n = len(old_lines)
        if n == 0 or n > len(file_lines):
            return ""
        # Cap the scan to keep the search cheap on large files. 10k line
        # windows at O(n*window) is still sub-second for typical sources.
        max_scan = min(len(file_lines) - n + 1, 10000)
        best_ratio = 0.0
        best_idx = -1
        for i in range(max_scan):
            window = "\n".join(file_lines[i:i + n])
            ratio = difflib.SequenceMatcher(None, old_str, window, autojunk=False).quick_ratio()
            # quick_ratio is an upper bound — only do full compare when it
            # looks promising to avoid O(n^2) on every window.
            if ratio < best_ratio:
                continue
            real_ratio = difflib.SequenceMatcher(None, old_str, window, autojunk=False).ratio()
            if real_ratio > best_ratio:
                best_ratio = real_ratio
                best_idx = i
        if best_ratio < 0.6 or best_idx < 0:
            return ""
        best_block = "\n".join(file_lines[best_idx:best_idx + n])
        diff_lines = difflib.unified_diff(
            old_str.splitlines(keepends=True) if old_str.endswith("\n") else [l + "\n" for l in old_str.splitlines()],
            best_block.splitlines(keepends=True) if best_block.endswith("\n") else [l + "\n" for l in best_block.splitlines()],
            fromfile="your old_str",
            tofile=f"{path}:{best_idx + 1}",
            lineterm="",
            n=2,
        )
        diff_text = "".join(diff_lines).rstrip()
        return (
            f"\nClosest match at line {best_idx + 1} (similarity {best_ratio:.2f}):\n"
            f"{diff_text}\n"
            f"Fix the whitespace/indent in old_str to match exactly, "
            f"or use write_file to overwrite the whole file."
        )
    except Exception:
        return ""


def edit_file(path: str, old_str: str, new_str: str) -> str:
    """Find and replace a string in a file."""
    full_path = _resolve_path(path)
    if not os.path.exists(full_path):
        return f"Error: File not found: {path}"
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()

        count = content.count(old_str)
        if count == 0:
            hint = _closest_block_hint(content, old_str, path)
            return (
                f"Error: old_str not found in {path}. "
                f"Must match EXACTLY including whitespace, tabs vs spaces, "
                f"and trailing newlines.{hint}"
            )
        if count > 1:
            # Build a list of line-number anchors for each match so the
            # model can pick a more specific old_str on retry. Weaker
            # models drop the task entirely on a bare "found N times"
            # message; showing locations + the line of the first few
            # matches gives them something concrete to anchor on.
            match_lines = []
            start = 0
            line_no = 1
            line_starts = [0]
            for i, ch in enumerate(content):
                if ch == "\n":
                    line_starts.append(i + 1)
            while True:
                pos = content.find(old_str, start)
                if pos < 0:
                    break
                ln = sum(1 for s in line_starts if s <= pos)
                line_text = content[line_starts[ln - 1]:line_starts[ln] if ln < len(line_starts) else len(content)].rstrip()
                match_lines.append(f"  line {ln}: {line_text[:80]}")
                start = pos + 1
            anchors = "\n".join(match_lines[:6])
            return (
                f"Error: old_str matches {count} locations in {path}. "
                f"Retry with a more unique old_str that includes surrounding "
                f"lines to disambiguate. Match locations:\n{anchors}"
            )

        new_content = content.replace(old_str, new_str, 1)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        return f"Edited {path}: replaced 1 occurrence"
    except Exception as e:
        return f"Error editing {path}: {e}"


def bash(command: str, auto_approve: bool = False) -> str:
    """Run a bash command with safety checks."""
    # Block dangerous commands
    cmd_lower = command.lower().strip()
    for blocked in BLOCKED_COMMANDS:
        if blocked in cmd_lower:
            return f"Error: Command blocked for safety: {command}"

    # Ask for confirmation unless auto-approved
    if not auto_approve and not AUTO_APPROVE:
        print(f"\n  \033[33m$ {command}\033[0m")
        try:
            confirm = input("  Run this command? [y/N] ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            return "Command cancelled by user."
        if confirm not in ("y", "yes"):
            return "Command cancelled by user."

    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=60, cwd=os.getcwd()
        )
        output = ""
        if result.stdout:
            output += result.stdout
        if result.stderr:
            output += ("\n" if output else "") + result.stderr
        if result.returncode != 0:
            output += f"\n[exit code: {result.returncode}]"
        # Truncate very long output. Old cap (5KB) made the model
        # re-run the same command looking for the "missing" tail — raised
        # to 20KB which covers almost every real command while still
        # preventing a runaway `cat very_big_file` from nuking the context.
        if len(output) > 20000:
            output = output[:20000] + f"\n... [truncated, {len(output)} chars total]"
        return output.strip() or "(no output)"
    except subprocess.TimeoutExpired:
        return "Error: Command timed out after 60 seconds"
    except Exception as e:
        return f"Error running command: {e}"


def list_files(pattern: str) -> str:
    """List files matching a glob pattern."""
    try:
        matches = sorted(glob_mod.glob(pattern, recursive=True))
        if not matches:
            return f"No files found matching: {pattern}"
        if len(matches) > 100:
            return "\n".join(matches[:100]) + f"\n... and {len(matches) - 100} more"
        return "\n".join(matches)
    except Exception as e:
        return f"Error listing files: {e}"


def grep(pattern: str, path: str = ".", include: str = "") -> str:
    """Search for a pattern in files."""
    try:
        cmd = ["grep", "-rn", "--color=never", "-I"]
        if include:
            cmd.extend(["--include", include])
        cmd.extend([pattern, path])

        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=30, cwd=os.getcwd()
        )
        output = result.stdout.strip()
        if not output:
            return f"No matches found for: {pattern}"
        lines = output.split("\n")
        if len(lines) > 50:
            return "\n".join(lines[:50]) + f"\n... and {len(lines) - 50} more matches"
        return output
    except subprocess.TimeoutExpired:
        return "Error: grep timed out after 30 seconds"
    except Exception as e:
        return f"Error running grep: {e}"


def str_replace(path: str, old_str: str, new_str: str) -> str:
    """Multi-line robust find and replace."""
    return edit_file(path, old_str, new_str)


def batch(calls: list[dict]) -> str:
    """Execute multiple tools in sequence."""
    results = []
    for i, call in enumerate(calls, 1):
        name = call.get("tool")
        args = call.get("args", {})
        if name == "batch":
            results.append(f"Call {i}: Error: Cannot nest batch calls.")
            continue

        # We need to import execute_tool here to avoid circular dependency
        # if we moved it, but it's already in this file
        res = execute_tool(name, args)
        results.append(f"--- Call {i} ({name}) ---\n{res}")

    return "\n\n".join(results)


# ─── Web tools ────────────────────────────────────────────────────────────────

def web_search(query: str, max_results: int = 5) -> str:
    """Search the web. Tries Tavily → Brave → DuckDuckGo HTML in that order.

    Configure API keys via env vars:
      - TAVILY_API_KEY (recommended, free 1000/mo at app.tavily.com)
      - BRAVE_API_KEY  (free 2000/mo at api.search.brave.com)
    Falls back to DuckDuckGo HTML scrape if no key is set.
    """
    max_results = max(1, min(int(max_results or 5), 10))

    # Backend 1: Tavily (best quality)
    tavily_key = os.environ.get("TAVILY_API_KEY", "").strip()
    if tavily_key:
        try:
            resp = requests.post(
                "https://api.tavily.com/search",
                json={
                    "api_key": tavily_key,
                    "query": query,
                    "max_results": max_results,
                    "include_answer": True,
                    "search_depth": "basic",
                },
                timeout=15,
            )
            if resp.status_code == 200:
                data = resp.json()
                return _format_search_results(query, data.get("results", []), answer=data.get("answer"))
        except Exception as e:
            pass  # fall through

    # Backend 2: Brave Search
    brave_key = os.environ.get("BRAVE_API_KEY", "").strip()
    if brave_key:
        try:
            resp = requests.get(
                "https://api.search.brave.com/res/v1/web/search",
                headers={"X-Subscription-Token": brave_key, "Accept": "application/json"},
                params={"q": query, "count": max_results},
                timeout=15,
            )
            if resp.status_code == 200:
                data = resp.json()
                results = []
                for r in data.get("web", {}).get("results", [])[:max_results]:
                    results.append({
                        "title": r.get("title", ""),
                        "url": r.get("url", ""),
                        "content": r.get("description", ""),
                    })
                return _format_search_results(query, results)
        except Exception:
            pass

    # Backend 3: DuckDuckGo HTML scrape (no key needed, lowest quality)
    try:
        resp = requests.get(
            "https://html.duckduckgo.com/html/",
            params={"q": query},
            headers={"User-Agent": "Mozilla/5.0 (pw-agent)"},
            timeout=15,
        )
        if resp.status_code == 200:
            results = _parse_ddg_html(resp.text, max_results)
            if results:
                return _format_search_results(query, results)
    except Exception as e:
        return f"Error: web search failed — {e}. Set TAVILY_API_KEY or BRAVE_API_KEY for reliable search."

    return f"Error: web search returned no results for '{query}'. Try a different query or set TAVILY_API_KEY."


def _format_search_results(query: str, results: list[dict], answer: str = None) -> str:
    """Format search results as readable text for the model."""
    if not results and not answer:
        return f"No results for: {query}"
    lines = [f"Search results for: {query}", ""]
    if answer:
        lines.append(f"Quick answer: {answer}")
        lines.append("")
    for i, r in enumerate(results, 1):
        title = r.get("title", "(no title)")
        url = r.get("url", "")
        snippet = (r.get("content") or r.get("snippet") or "").strip()
        if len(snippet) > 300:
            snippet = snippet[:300] + "..."
        lines.append(f"{i}. {title}")
        lines.append(f"   {url}")
        if snippet:
            lines.append(f"   {snippet}")
        lines.append("")
    return "\n".join(lines).rstrip()


def _parse_ddg_html(html: str, max_results: int) -> list[dict]:
    """Lightweight DuckDuckGo HTML parser. No BeautifulSoup dep."""
    results = []
    # DDG HTML uses <a class="result__a" href="..."> for titles and
    # <a class="result__snippet"> for snippets
    pattern = re.compile(
        r'<a[^>]+class="[^"]*result__a[^"]*"[^>]+href="([^"]+)"[^>]*>(.*?)</a>'
        r'(?:[\s\S]*?<a[^>]+class="[^"]*result__snippet[^"]*"[^>]*>(.*?)</a>)?',
        re.DOTALL,
    )

    def _decode(s: str) -> str:
        s = re.sub(r'<[^>]+>', '', s).strip()
        s = s.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
        s = s.replace('&quot;', '"').replace('&#39;', "'").replace('&apos;', "'")
        s = re.sub(r'&#(\d+);', lambda m: chr(int(m.group(1))), s)
        s = re.sub(r'&#x([0-9a-fA-F]+);', lambda m: chr(int(m.group(1), 16)), s)
        return s

    for match in pattern.finditer(html):
        if len(results) >= max_results:
            break
        url = match.group(1) or ""
        title = _decode(match.group(2) or '')
        snippet = _decode(match.group(3) or '')

        # DDG wraps URLs in /l/?uddg=...
        if url.startswith("/l/") or "uddg=" in url:
            try:
                qs = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
                url = qs.get("uddg", [url])[0]
            except Exception:
                pass

        if url and title:
            results.append({"title": title, "url": url, "content": snippet})
    return results


def web_fetch(url: str, max_chars: int = 8000) -> str:
    """Fetch a URL and return readable text (HTML tags stripped)."""
    if not url.startswith(("http://", "https://")):
        return f"Error: URL must start with http:// or https://"

    max_chars = max(500, min(int(max_chars or 8000), 50000))

    try:
        resp = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0 (pw-agent)"},
            timeout=20,
            allow_redirects=True,
        )
    except requests.exceptions.Timeout:
        return f"Error: timeout fetching {url}"
    except requests.exceptions.ConnectionError as e:
        return f"Error: connection failed — {e}"
    except Exception as e:
        return f"Error fetching {url}: {e}"

    if resp.status_code != 200:
        return f"Error: {url} returned HTTP {resp.status_code}"

    content_type = resp.headers.get("Content-Type", "").lower()

    # JSON: return as-is (truncated)
    if "json" in content_type:
        text = resp.text
    # HTML: strip tags
    elif "html" in content_type or url.endswith((".html", ".htm")):
        text = _html_to_text(resp.text)
    # Plain text / markdown / source code
    else:
        text = resp.text

    text = text.strip()
    if len(text) > max_chars:
        text = text[:max_chars] + f"\n\n... [truncated, {len(text)} chars total]"

    return f"[Fetched {url} — {len(text)} chars, {content_type or 'unknown type'}]\n\n{text}"


def _html_to_text(html: str) -> str:
    """Strip HTML to readable text. No BeautifulSoup dep — regex-based."""
    # Drop scripts, styles, nav, footer
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<nav[^>]*>.*?</nav>', '', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<footer[^>]*>.*?</footer>', '', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<header[^>]*>.*?</header>', '', html, flags=re.DOTALL | re.IGNORECASE)

    # Convert <br>, <p>, <div>, <li>, <h*> to newlines
    html = re.sub(r'<br\s*/?>', '\n', html, flags=re.IGNORECASE)
    html = re.sub(r'</(p|div|li|h[1-6]|tr|article|section)>', '\n', html, flags=re.IGNORECASE)

    # Strip remaining tags
    text = re.sub(r'<[^>]+>', '', html)

    # Decode common HTML entities
    entities = {
        '&nbsp;': ' ', '&amp;': '&', '&lt;': '<', '&gt;': '>',
        '&quot;': '"', '&#39;': "'", '&apos;': "'",
        '&mdash;': '—', '&ndash;': '–', '&hellip;': '…',
    }
    for ent, ch in entities.items():
        text = text.replace(ent, ch)
    # Numeric entities (decimal and hex)
    text = re.sub(r'&#(\d+);', lambda m: chr(int(m.group(1))), text)
    text = re.sub(r'&#x([0-9a-fA-F]+);', lambda m: chr(int(m.group(1), 16)), text)

    # Collapse whitespace
    text = re.sub(r'\n[ \t]+', '\n', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]{2,}', ' ', text)
    return text.strip()


# Map tool names to functions
TOOL_MAP = {
    "read_file": lambda args: read_file(args["path"], offset=int(args.get("offset", 0)), limit=int(args.get("limit", 300))),
    "write_file": lambda args: write_file(args["path"], args["content"]),
    "edit_file": lambda args: edit_file(args["path"], args["old_str"], args["new_str"]),
    "str_replace": lambda args: str_replace(args["path"], args["old_str"], args["new_str"]),
    "bash": lambda args: bash(args["command"]),
    "list_files": lambda args: list_files(args["pattern"]),
    "grep": lambda args: grep(args["pattern"], args.get("path", "."), args.get("include", "")),
    "batch": lambda args: batch(args["calls"]),
    "web_search": lambda args: web_search(args["query"], max_results=int(args.get("max_results", 5))),
    "web_fetch": lambda args: web_fetch(args["url"], max_chars=int(args.get("max_chars", 8000))),
}


def execute_tool(name: str, args: dict) -> str:
    """Execute a tool by name with the given arguments."""
    if name not in TOOL_MAP:
        return f"Error: Unknown tool '{name}'. Available: {', '.join(TOOL_MAP.keys())}"
    try:
        return TOOL_MAP[name](args)
    except KeyError as e:
        return f"Error: Missing required argument {e} for tool '{name}'"
    except Exception as e:
        return f"Error executing {name}: {e}"
