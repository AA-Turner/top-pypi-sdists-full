"""Gap detector — find unfamiliar terms in user input.

A "gap" is a token in a user message that looks like a named entity or
identifier the agent probably has no context for: paper titles, library
names, API identifiers, file paths, multi-word Title Case phrases,
ALL-CAPS acronyms, version-like tokens.

The detector is HEURISTIC, not exhaustive. False positives are cheap
(an extra retrieve call) and false negatives are the failure mode the
PRD §5.7 calls out (Gemma 4 answers from prior on a general-knowledge
HLE question because it never noticed there was something to look up).
Bias the heuristics toward firing.

Public surface:

    gaps: list[str] = detect_gaps(user_text)
"""
from __future__ import annotations

import re
from typing import Iterable

# Common English words that look like Title Case but aren't entities.
# Keep small — the goal is "minimize false positives on conversational
# openers", not exhaustive linguistic filtering.
_STOPWORDS: frozenset[str] = frozenset({
    # Sentence-start common Title-Case words.
    "The", "A", "An", "I", "We", "You", "It", "He", "She", "They",
    "This", "That", "These", "Those", "What", "When", "Where", "Why",
    "How", "Who", "Which", "If", "But", "And", "Or", "So", "Yes", "No",
    "Please", "Can", "Could", "Would", "Should", "Will", "Let", "Do",
    "Does", "Did", "Is", "Are", "Was", "Were", "Be", "Been", "Being",
    "Have", "Has", "Had", "Get", "Got", "Make", "Made", "Take", "Took",
    # Common imperative openers for drydock tasks.
    "Build", "Fix", "Add", "Remove", "Update", "Refactor", "Test",
    "Run", "Check", "Review", "Show", "List", "Explain", "Find", "Look",
    # Sentence-starting verbs that appear after periods in numbered lists
    # ("scratch.Step 1", "fail.Step 2") — dotted-identifier regex treats
    # these as module.attr but they're sentence boundaries.
    "Step", "Stop", "Start", "Read", "Write", "Open", "Use", "See",
    "Try", "Note", "Save", "Load", "Copy", "Move", "Call", "Pass",
    # HLE/exam prose openers — flagged in 2026-05-14 queue audit
    # because they always lead a Title-Case phrase ("Consider the X").
    "Consider", "Suppose", "Given", "Let", "Define", "Compute",
    "Determine", "Evaluate", "Prove", "Recall", "Note", "Assume",
    "Render", "Parse", "Scan", "Detect", "Match", "Merge",
    "Insert", "Delete", "Select", "Update", "Create", "Drop",
})

# HLE / harness prompt-template tokens that the detector kept flagging
# as "unknown terms" — 2026-05-14 queue audit found FINAL (45×),
# ANSWER (44×), QUESTION (44×), FINAL ANSWER: (47×) all in the curiosity
# queue as false positives. Compared case-insensitively. Any candidate
# whose stripped form (case-folded, trailing colon stripped) is in this
# set is dropped before enqueue.
_TEMPLATE_NOISE: frozenset[str] = frozenset(
    s.lower() for s in {
        "FINAL", "ANSWER", "QUESTION", "FINAL ANSWER",
        "GROUND TRUTH", "PREDICTED ANSWER", "VERDICT",
        # autonomous_review / admiral output tokens
        "CONSIDER", "RESPONSE", "RESULT", "VERIFIED",
        # Common prose openers that pass acronym + title-case regexes
        "CHAPTER", "SECTION", "PART", "INTRODUCTION", "CONCLUSION",
        # HLE multiple-choice format boilerplate — 2026-05-16 queue audit
        # found "Answer Choices" (95×), "None of the" (13×), etc. leaking
        # through because they match the title-case phrase regex.
        "ANSWER CHOICES", "ANSWER CHOICE",
        "NONE OF THE", "NONE OF THE ABOVE", "NONE OF THESE",
        "ALL OF THE", "ALL OF THE ABOVE", "ALL OF THESE",
        "ALL OF ABOVE", "NONE OF ABOVE",
        "CHOOSE ONE", "SELECT ONE", "WHICH OF THE",
        "WHICH OF THE FOLLOWING",
        # Python keywords — match _RE_ACRONYM (≥3 uppercase) but are never
        # unknown to a coding assistant. 2026-05-22 queue audit: CLI (300×),
        # NOT (200×), README (102×) in top false positives.
        "NOT", "AND", "OR", "FOR", "DEF", "CLASS", "PASS", "RETURN",
        "IMPORT", "FROM", "WITH", "TRY", "EXCEPT", "RAISE", "YIELD",
        "ASYNC", "AWAIT", "TRUE", "FALSE", "NONE",
        # Common coding / CLI abbreviations always known in coding context
        "CLI", "GUI", "TUI", "URL", "HTTP", "HTTPS", "TCP", "UDP",
        "README", "CHANGELOG", "LICENSE", "TODO", "FIXME", "HACK",
        "ENV", "DIR", "STR", "INT", "BOOL", "DICT", "LIST", "SET",
        "OBJ", "ERR", "MSG", "NUM", "VAR", "FMT", "RES", "REQ",
        "LOG", "PID", "CWD", "SRC", "LIB", "BIN", "TMP",
        # File formats and data interchange standards — always known
        "JSON", "CSV", "TSV", "XML", "HTML", "YAML", "YML", "TOML",
        "SQL", "SQLITE", "POSTGRESQL", "MYSQL", "REDIS",
        "PDF", "SVG", "PNG", "JPG", "JPEG", "GIF", "ICO", "WEBP",
        "ISO", "ASCII", "UTF", "UTF8", "UTF16", "BASE64",
        "API", "SDK", "REST", "SOAP", "RPC", "GRPC", "CRUD",
        "ORM", "MVC", "MVP", "MVVM", "OOP", "FP",
        "CI", "CD", "PR", "MR", "WIP",
        "SSH", "SSL", "TLS", "JWT", "OAUTH", "SAML",
        "CPU", "GPU", "RAM", "SSD", "HDD", "NFS",
        # Date/time format placeholders — appear in PRD prompts as template
        # strings, never a meaningful GraphRAG ingest target.
        "YYYY", "YY", "MM", "DD", "HH", "SS", "UTC", "GMT",
        # Open-source license / protocol names — always known in coding context
        "APACHE", "APACHE2", "MIT", "BSD", "GPL", "LGPL", "MPL", "ISC",
        # Generic status/signal words that match _RE_ACRONYM but carry no
        # knowledge gap — 2026-06-04 queue audit top false positives.
        "ERROR", "WARNING", "INFO", "DEBUG", "CRITICAL", "FATAL",
        "TRACE", "VERBOSE", "NOTICE",
        # HTTP methods — always known in coding context.
        "GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS", "CONNECT",
        # HTTP/web protocol abbreviations.
        "SSE", "WS", "WSS", "RPC", "JSONRPC",
        # Web/style formats.
        "CSS", "SASS", "SCSS", "LESS",
        # Common programming concepts always known in coding context.
        "AST", "CFG", "DAG", "FSM", "DSL", "BNF", "EBNF", "REPL",
        # Caching strategies.
        "LRU", "LFU", "FIFO", "LIFO", "MRU",
        # Encoding names with hyphen variants.
        "UTF-8", "UTF-16", "UTF-32",
        # Common placeholder / schema column-type words.
        "VALUE", "DATE", "TIME", "SIZE", "HASH", "RANK",
        # Project doc file names always known to a coding assistant.
        "FAQ", "CONTRIBUTING", "AUTHORS", "CODEOWNERS", "SECURITY",
        "MAINTAINERS", "NOTICE",
        # Connector prepositions that match short-string regexes but are prose.
        "IN", "OF", "AT", "ON", "BY", "AS",
        # PRD section headers — always prose in template specs, not entities.
        "OPEN QUESTIONS", "USE CASES", "NON-GOALS", "NON GOALS",
        "EDGE CASES", "GETTING STARTED", "QUICK START", "OVERVIEW",
        "BACKGROUND", "MOTIVATION", "RATIONALE", "OBJECTIVES", "SCOPE",
        # Pytest / CI test-status words — appear as "pytest is RED / GREEN"
        # in task prompts but are never GraphRAG-retrievable knowledge.
        "RED", "GREEN", "PASS", "FAIL", "SKIP", "XFAIL",
        "PASSED", "FAILED", "SKIPPED", "BROKEN", "XPASS",
        "STATUS", "STATE", "MODE", "TYPE", "KIND", "FLAG", "OPTION",
        "FINDINGS", "PATTERNS", "REGEXES", "FIELDS", "METHODS",
        "VERSION", "NAME", "PATH", "DATA", "OUTPUT", "INPUT",
        "CONFIG", "SCHEMA", "FORMAT", "TEMPLATE", "LAYOUT",
        # SQL DDL keywords — written in ALL-CAPS in schema code but never
        # a GraphRAG knowledge gap for a coding assistant.
        "TEXT", "INTEGER", "REAL", "BLOB", "BOOLEAN", "NUMERIC",
        "PRIMARY", "KEY", "UNIQUE", "INDEX", "FOREIGN", "REFERENCES",
        "CONSTRAINT", "DEFAULT", "NOT NULL", "NULL", "AUTO INCREMENT",
        "CREATE", "TABLE", "SELECT", "INSERT", "UPDATE", "DELETE",
        "FROM", "WHERE", "JOIN", "LEFT", "RIGHT", "INNER", "OUTER",
        "GROUP BY", "ORDER BY", "HAVING", "LIMIT", "OFFSET",
        "BEGIN", "COMMIT", "ROLLBACK", "TRANSACTION",
        # Common English words used in ALL-CAPS for emphasis in user specs —
        # they match _RE_ACRONYM (≥3 uppercase) but carry no knowledge gap.
        "OFFLINE", "ONLINE", "LOCAL", "REMOTE", "ALWAYS", "NEVER",
        "ONLY", "ALSO", "MUST", "SHOULD", "WILL", "FULL", "EMPTY",
        "DONE", "NEXT", "LAST", "FIRST", "EACH", "BOTH", "SAME",
        "EVERY", "KEEP", "NEED", "ABLE", "MAKE", "WRITE", "READ",
        "STORE", "CACHE", "DISK", "FILE", "PARSE", "LOAD", "CALL",
        "SEND", "RECV", "OPEN", "CLOSE", "INIT", "STOP", "WAIT",
        "SYNC", "ASYNC", "COPY", "MOVE", "PUSH", "PULL", "FETCH",
        # Temporal conjunctions/prepositions used for emphasis in specs
        "BEFORE", "AFTER", "DURING", "WHILE", "SINCE", "UNTIL",
        "WHEN", "THEN", "ONCE", "ALREADY", "STILL", "AGAIN",
        "ACROSS", "BETWEEN", "WITHIN", "WITHOUT", "THROUGH",
        "ABOVE", "BELOW", "UNDER", "OVER", "INTO", "ONTO", "FROM",
        "AGAINST", "BEYOND", "DESPITE", "EXCEPT", "INSTEAD",
        "CLARIFICATION", "IMPLEMENTATION", "REQUIREMENT", "SPECIFICATION",
        "DEFINITION", "DESCRIPTION", "DOCUMENTATION", "EXAMPLE",
        "FEATURE", "FUNCTION", "INTERFACE", "PROPERTY", "ATTRIBUTE",
        "INSTANCE", "OBJECT", "CLASS", "MODULE", "PACKAGE", "LIBRARY",
        "MILK",  # from "buy milk" test prompt — common English word
        # Single-word emphasis — match _RE_ACRONYM (≥3 uppercase) but are
        # common English words used for stress in PRD specs, not identifiers.
        "ONE", "OLD", "END", "POST", "MOSTLY", "QUITE", "VERY",
        # Networking / infra abbreviations always known in coding context.
        "TTL", "ACL", "NAT", "DNS", "VPN", "LAN", "WAN",
        # Product / project management abbreviations used in PRD prompts.
        "PRD", "RFC", "ADR", "SLA", "SLO", "SLI", "KPI", "OKR",
        # iCalendar (RFC 5545) protocol keywords — appear in iCal-format PRDs.
        "VCALENDAR", "VEVENT", "VTODO", "VJOURNAL", "VALARM",
        "DTSTART", "DTEND", "DTSTAMP", "DURATION", "RRULE",
        # Common English nouns used as PRD field / attribute names — never a
        # GraphRAG knowledge gap. 2026-06-04 queue audit: recency (215×),
        # tasks (188×), untitled (67×), username (65×).
        "recency", "tasks", "untitled", "username", "summary",
        "legacy", "snapshot", "artifact", "payload", "metadata",
        "endpoint", "workflow", "pipeline", "plugin", "widget",
        "sidebar", "toolbar", "viewport", "canvas", "panel",
        "dialog", "modal", "popup", "tooltip", "banner", "badge",
        # Well-known infrastructure / framework names always known to a coding
        # assistant — appear as lowercase terms in stress-run sessions where
        # the model is asked to add support for common servers/tools.
        "nginx", "gunicorn", "uwsgi", "celery", "supervisor",
        "flask", "django", "fastapi", "tornado", "aiohttp", "bottle",
        "pytest", "unittest", "nose", "tox",
        "pandas", "numpy", "scipy", "matplotlib", "seaborn", "sklearn",
        "docker", "kubernetes", "helm", "terraform", "ansible",
        "webpack", "vite", "rollup", "esbuild", "babel",
        # Generic technical snake_case nouns that are code-artifact names,
        # not external library knowledge gaps.
        "stack_trace", "word_count", "line_count", "byte_count", "char_count",
        "legacy_modules", "legacy_module", "legacy_code",
        "drydock_lifecycle", "drydock_test",
    }
)

# Words that are only ever connectors — a Title-Case phrase composed
# entirely of these (after stripping the leading word) is prose filler.
_CONNECTOR_WORDS: frozenset[str] = frozenset({
    "of", "the", "and", "for", "in", "de", "von", "a", "an",
})

# Snake-case identifiers that start with a common action verb are generated
# code artifacts (CRUD methods, helpers), not external knowledge gaps.
_VERB_PREFIXES: frozenset[str] = frozenset({
    "get_", "set_", "add_", "put_", "has_", "is_",
    "list_", "count_", "delete_", "remove_", "create_", "make_",
    "build_", "update_", "edit_", "save_", "load_", "read_", "write_",
    "parse_", "format_", "render_", "handle_", "process_", "compute_",
    "calc_", "check_", "validate_", "fetch_", "send_", "recv_",
    "run_", "exec_", "init_", "reset_", "clear_", "close_", "open_",
    "find_", "search_", "query_", "filter_", "sort_", "group_",
    "encode_", "decode_", "serialize_", "deserialize_", "convert_",
    "show_", "hide_", "display_", "print_", "log_", "report_",
    "sample_", "generate_", "emit_", "merge_", "patch_", "register_",
    "unregister_", "subscribe_", "publish_", "notify_", "watch_",
    "require_", "resolve_", "dispatch_", "route_", "map_", "reduce_",
    "collect_", "gather_", "aggregate_", "transform_", "extract_",
    "inject_", "wrap_", "unwrap_", "clone_", "copy_", "move_",
    "import_", "export_", "upload_", "download_", "stream_",
    "test_", "assert_", "expect_", "mock_", "stub_", "spy_",
    # Architecture-layer prefixes — snake_case with these prefixes are
    # internal variables/types, not external library knowledge gaps.
    "backend_", "frontend_", "status_", "top_", "base_", "main_",
    "core_", "util_", "helper_", "common_", "shared_", "default_",
    "current_", "prev_", "next_", "max_", "min_", "total_", "avg_",
    "num_", "idx_", "pos_", "key_", "val_", "src_", "dst_", "tmp_",
    "raw_", "cached_", "parsed_", "formatted_", "rendered_", "computed_",
    # Format-sniffing / detection / request-field prefixes — code artifacts
    # generated by the agent, not external library knowledge gaps.
    "sniff_", "detect_", "infer_", "guess_",
    "req_", "resp_", "res_", "body_", "header_", "param_",
    "source_", "target_", "dest_", "output_", "input_",
})


def _is_template_noise(candidate: str) -> bool:
    """True if the candidate is HLE/admiral boilerplate, not a real term."""
    norm = candidate.strip(" :.,;").lower()
    if not norm:
        return True
    if norm in _TEMPLATE_NOISE:
        return True
    # Drop bare English stopword tokens too (the user prompt sometimes
    # gets fragmented and "the" / "is" leak through the quoted-string
    # path with 3-char minimum length).
    if norm in {sw.lower() for sw in _STOPWORDS}:
        return True
    # A multi-word phrase whose non-first words are all connectors is
    # prose filler, not an entity ("None of the", "All of the", etc.).
    words = norm.split()
    if len(words) >= 2 and all(w in _CONNECTOR_WORDS for w in words[1:]):
        return True
    # Python source filenames (cli.py, __init__.py, main.py, etc.) are
    # never unknown to a coding assistant — they're being written. Matched
    # by _RE_DOTTED_IDENT because "name.py" has a dot. 2026-05-22 audit:
    # __init__.py (100×), cli.py (80×), renderer.py (69×) top false
    # positives.
    # Bare filenames (no directory separator) with common extensions are
    # always known in a coding context — filter them to prevent spam.
    # Full paths ("/data3/foo/bar.csv") are kept as they reference specific
    # resources worth looking up.
    _CODE_EXTS = (
        ".py", ".md", ".txt", ".csv", ".json", ".yaml", ".yml",
        ".toml", ".log", ".html", ".xml", ".sql", ".sh", ".rs",
        ".go", ".ts", ".js", ".jsx", ".tsx", ".css", ".scss",
        ".bak", ".tmp", ".lock", ".pid", ".gz", ".zip", ".tar",
        ".db", ".sqlite3", ".cache", ".dat", ".bin",
    )
    if "/" not in norm and any(norm.endswith(ext) for ext in _CODE_EXTS):
        return True
    # Dotted identifier where the post-dot component is a common English
    # word OR starts with a verb-prefix → sentence boundary artifact or
    # code artifact ("scratch.Step", "fail.Stop", "parser.sniff_format").
    if "." in norm:
        parts = norm.split(".")
        _sw_lower = {w.lower() for w in _STOPWORDS}
        if any(p in _sw_lower for p in parts[1:]):
            return True
        if any(any(p.startswith(vp) for vp in _VERB_PREFIXES) for p in parts[1:]):
            return True
        # Python stdlib module dotted names (json.loads, http.server, os.path)
        # are always known to a coding assistant.
        _STDLIB_MODULES: frozenset[str] = frozenset({
            "os", "sys", "re", "io", "json", "csv", "xml", "html", "http",
            "urllib", "email", "logging", "threading", "multiprocessing",
            "subprocess", "socket", "ssl", "hashlib", "hmac", "uuid",
            "datetime", "time", "calendar", "random", "math", "statistics",
            "collections", "itertools", "functools", "operator", "copy",
            "abc", "typing", "dataclasses", "enum", "pathlib", "shutil",
            "tempfile", "glob", "fnmatch", "pickle", "shelve", "sqlite3",
            "struct", "array", "queue", "heapq", "bisect", "weakref",
            "contextlib", "inspect", "ast", "dis", "gc", "traceback",
            "warnings", "unittest", "doctest", "pprint", "textwrap",
            "string", "difflib", "argparse", "configparser", "platform",
            "signal", "asyncio", "base64", "binascii", "codecs",
        })
        if parts[0] in _STDLIB_MODULES:
            return True
    # LaTeX math expressions — false positives from HLE/academic prompts.
    # A term starting with $ or a LaTeX command backslash is math notation,
    # not a GraphRAG-retrievable identifier.
    if norm.startswith("$") or norm.startswith("\\"):
        return True
    # Pure numeric/punctuation strings — quoted answer-choice values like
    # "33,1" or "0.5" from HLE prompts; never a meaningful ingest target.
    if re.match(r"^[\d\s,./\-+%()]+$", norm):
        return True
    # Python dunder attributes (__all__, __init__.__all__, etc.) are always
    # known in a coding context — never a GraphRAG gap.
    if "__" in norm:
        return True
    # Test file / function names (test_cli, test_routes) are project artifacts
    # produced by the agent, not external knowledge worth retrieving.
    if norm.startswith("test_") or norm.startswith("tests_"):
        return True
    # Type-conversion function names (to_int, to_roman, to_snake_case) —
    # generic utility patterns, not external library gaps.
    if norm.startswith("to_"):
        return True
    # Snake_case names ending in common implementation-pattern suffixes are
    # code artifacts generated by the agent, not external knowledge gaps.
    # E.g. stack_trace, error_handler, config_manager, log_formatter.
    _NOUN_SUFFIXES: frozenset[str] = frozenset({
        "_trace", "_count", "_handler", "_manager", "_parser",
        "_formatter", "_reader", "_writer", "_builder", "_factory",
        "_registry", "_provider", "_consumer", "_producer",
        "_iterator", "_generator", "_validator", "_serializer",
        "_deserializer", "_encoder", "_decoder", "_processor",
        "_executor", "_scheduler", "_dispatcher", "_router",
        "_resolver", "_collector", "_aggregator", "_transformer",
        "_extractor", "_injector", "_wrapper", "_observer",
        "_listener", "_emitter", "_subscriber", "_publisher",
        "_module", "_modules", "_helper", "_util", "_utils",
        "_config", "_settings", "_options", "_params",
        "_result", "_results", "_response", "_request",
        "_context", "_session", "_client", "_server",
        "_queue", "_stack", "_buffer", "_cache", "_store",
        "_pool", "_cluster", "_node", "_worker", "_runner",
        "_loop", "_cycle", "_tick", "_batch", "_chunk",
    })
    if "_" in norm and any(norm.endswith(s) for s in _NOUN_SUFFIXES):
        return True
    # Common action-verb prefixed snake_case names are code artifacts.
    if any(norm.startswith(p) for p in _VERB_PREFIXES):
        return True
    # Roman numerals (MCMXCIV, XIV, etc.) — matched by _RE_ACRONYM but
    # carry no knowledge gap for a coding assistant.
    if len(norm) > 2 and re.match(
        r'^m{0,4}(?:cm|cd|d?c{0,3})(?:xc|xl|l?x{0,3})(?:ix|iv|v?i{0,3})$',
        norm
    ) and norm:
        return True
    # Sentence fragments starting with a single lowercase letter then a space
    # are contraction tails ("Don't" → "t ...", "Let's" → "s ...").  These
    # are never retrievable identifiers.
    if re.match(r"^[a-z] ", norm):
        return True
    # All-lowercase multi-word phrases (e.g. "buy milk", "sample logs") —
    # quoted prose from task prompts, not identifiers worth retrieving.
    # Only filter if the *original* candidate is already lowercase — Title Case
    # phrases like "Attention Is All You Need" must still be detected.
    # Strip punctuation before the regex so commas/periods don't block matches.
    orig = candidate.strip(" :.,;")
    norm_alphanum = re.sub(r"[^a-z0-9 _-]", "", norm)
    if " " in norm and orig == orig.lower() and re.match(r"^[a-z][a-z0-9 _-]+$", norm_alphanum) and len(norm_alphanum) > 3:
        return True
    # Date format strings like "YYYY-MM", "YYYY-MM-DD", "/DD/YYYY" — these
    # are template tokens that contain YYYY/MM/DD components (now in
    # TEMPLATE_NOISE) separated by punctuation but the combined string isn't.
    if re.match(r"^[/\-]?(?:yyyy|mm|dd|hh|ss)(?:[/\-](?:yyyy|mm|dd|hh|ss))+$", norm):
        return True
    # Hyphenated lowercase adjective phrases from PRD prose
    # ("tab-separated", "human-readable", "newline-delimited") — these are
    # format descriptors, not library identifiers worth retrieving.
    if re.match(r"^[a-z][a-z0-9]+-[a-z][a-z0-9]+(?:-[a-z][a-z0-9]+)*$", norm):
        return True
    # Paths that contain known test-run or lifecycle directories — these are
    # ephemeral artifacts from stress/lifecycle sessions, not real projects.
    if re.search(r"(/drydock_lifecycle/|/pytest-of-|/pytest-\d|/tmp/drydock_|/swe_bench_|/test_harness_)", norm):
        return True
    # Latin abbreviations used as prose connectors ("i.e", "e.g", "etc").
    if norm in ("i.e", "e.g", "etc", "i.e.", "e.g.", "etc.", "cf.", "cf", "vs", "vs."):
        return True
    # Snake_case identifiers containing _to_ in the middle are converter helpers
    # (csv_to_json, rgb_to_hex) — project-generated code artifacts, not gaps.
    if re.match(r"^[a-z][a-z0-9]*_to_[a-z][a-z0-9_]*$", norm):
        return True
    return False

# Acronyms shorter than this are too noisy to chase ("ID", "OK", "OS").
_MIN_ACRONYM_LEN = 3

# Maximum gaps to return per call. The retrieve consumer can only act
# on so many before context bloats; truncate at the source.
_MAX_GAPS = 8

_RE_ACRONYM = re.compile(r"\b[A-Z]{%d,}(?:-?[A-Z0-9]+)?\b" % _MIN_ACRONYM_LEN)
_RE_TITLE_CASE_PHRASE = re.compile(
    r"\b(?:[A-Z][a-z]+(?:[-'][A-Z][a-z]+)?)(?:\s+(?:[A-Z][a-z]+(?:[-'][A-Z][a-z]+)?|of|the|and|for|in|de|von)){1,4}"
)
_RE_DOTTED_IDENT = re.compile(r"\b[a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*){1,}\b")
_RE_SNAKE_IDENT = re.compile(r"\b[a-z][a-z0-9_]*_[a-z0-9_]+\b")
_RE_VERSIONED = re.compile(r"\b[a-zA-Z][a-zA-Z0-9_-]*-\d+(?:\.\d+)+\b")
_RE_QUOTED = re.compile(r'"([^"\n]{3,80})"|\'([^\'\n]{3,80})\'')
_RE_PATH = re.compile(r"\b(?:/[A-Za-z0-9_.-]+){2,}\b")


def _strip_punct(s: str) -> str:
    return s.strip(" \t\n.,;:!?\"'()[]{}<>")


def _dedup_preserve_order(items: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for it in items:
        k = it.lower()
        if k in seen:
            continue
        seen.add(k)
        out.append(it)
    return out


def detect_gaps(text: str, max_gaps: int = _MAX_GAPS) -> list[str]:
    """Extract candidate unfamiliar terms from `text`.

    The agent_loop's curiosity hook calls this on every new user
    message. Anything returned becomes a retrieve target before the
    first LLM turn.
    """
    if not text or not text.strip():
        return []

    candidates: list[str] = []

    # Quoted strings of meaningful length — strongest signal (user
    # explicitly delimited a name).
    for m in _RE_QUOTED.finditer(text):
        val = m.group(1) or m.group(2) or ""
        val = val.strip()
        if val:
            candidates.append(val)

    # Filesystem paths — almost always worth knowing about.
    for m in _RE_PATH.finditer(text):
        candidates.append(m.group(0))

    # Versioned package-like tokens ("django-4.2", "torch-2.0.1").
    for m in _RE_VERSIONED.finditer(text):
        candidates.append(m.group(0))

    # Dotted identifiers (module.path or Type.method).
    for m in _RE_DOTTED_IDENT.finditer(text):
        candidates.append(m.group(0))

    # Snake-case identifiers (likely function or symbol names).
    for m in _RE_SNAKE_IDENT.finditer(text):
        candidates.append(m.group(0))

    # ALL-CAPS acronyms (RAG, MCP, GraphRAG-style).
    for m in _RE_ACRONYM.finditer(text):
        tok = m.group(0)
        if tok not in _STOPWORDS:
            candidates.append(tok)

    # Title-Case multi-word phrases (paper titles, product names).
    for m in _RE_TITLE_CASE_PHRASE.finditer(text):
        phrase = _strip_punct(m.group(0))
        if not phrase:
            continue
        first = phrase.split()[0]
        if first in _STOPWORDS:
            # Drop the leading stopword — "The Curiosity Layer" → "Curiosity Layer"
            phrase = " ".join(phrase.split()[1:])
            if not phrase:
                continue
        candidates.append(phrase)

    return _dedup_preserve_order(
        c for c in candidates if c and not _is_template_noise(c)
    )[:max_gaps]
