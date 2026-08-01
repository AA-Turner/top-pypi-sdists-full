"""
BingoTools — Native function calling schema for attack loop execution.

Provides tool definitions in both OpenAI-compatible and Anthropic formats.
Models that support function calling receive these schemas; execution results
are injected as tool_result messages, preventing pre-execution hallucination.
"""
from __future__ import annotations

# ── Tool Definitions ─────────────────────────────────────────────────────────

BASH_EXEC = {
    "name": "bash_exec",
    "description": (
        "Execute a bash command and return stdout/stderr. "
        "Use for curl, httpx, sqlmap, nikto, nmap, and any CLI tool. "
        "The command runs in a real shell with network access."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "cmd": {
                "type": "string",
                "description": "The bash command to execute (e.g. curl -D - https://target.com/)",
            },
            "timeout": {
                "type": "integer",
                "description": "Execution timeout in seconds (default: 180)",
                "default": 180,
            },
        },
        "required": ["cmd"],
    },
}

PYTHON_EXEC = {
    "name": "python_exec",
    "description": (
        "Execute Python code and return output. "
        "Use for custom exploitation scripts, data parsing, encoding/decoding, "
        "and multi-step attack logic that bash one-liners can't handle."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "code": {
                "type": "string",
                "description": "Python code to execute (must be complete, runnable script)",
            },
            "timeout": {
                "type": "integer",
                "description": "Execution timeout in seconds (default: 180)",
                "default": 180,
            },
        },
        "required": ["code"],
    },
}

HTTP_REQUEST = {
    "name": "http_request",
    "description": (
        "Send an HTTP request to the TARGET and return full response with headers. "
        "Provide only the path — the target domain is automatically prepended by the executor. "
        "Use when you need precise control over method, headers, body."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "method": {
                "type": "string",
                "enum": ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"],
                "description": "HTTP method",
            },
            "path": {
                "type": "string",
                "description": "Request path on the target (e.g. /api/login, /admin/)",
            },
            "headers": {
                "type": "object",
                "description": "Request headers as key-value pairs",
                "additionalProperties": {"type": "string"},
            },
            "body": {
                "type": "string",
                "description": "Request body (for POST/PUT/PATCH)",
            },
            "follow_redirects": {
                "type": "boolean",
                "description": "Follow HTTP redirects (default: false)",
                "default": False,
            },
            "timeout": {
                "type": "integer",
                "description": "Request timeout in seconds (default: 30)",
                "default": 30,
            },
        },
        "required": ["method", "path"],
    },
}

# ── All tools ────────────────────────────────────────────────────────────────

BINGO_TOOLS = [BASH_EXEC, PYTHON_EXEC, HTTP_REQUEST]


# ── Format converters ────────────────────────────────────────────────────────

def to_openai_format(tools: list[dict] | None = None) -> list[dict]:
    """Convert to OpenAI function calling format (GPT/DeepSeek/Qwen)."""
    source = tools or BINGO_TOOLS
    return [
        {
            "type": "function",
            "function": {
                "name": t["name"],
                "description": t["description"],
                "parameters": t["parameters"],
            },
        }
        for t in source
    ]


def to_anthropic_format(tools: list[dict] | None = None) -> list[dict]:
    """Convert to Anthropic tool_use format (Claude)."""
    source = tools or BINGO_TOOLS
    return [
        {
            "name": t["name"],
            "description": t["description"],
            "input_schema": t["parameters"],
        }
        for t in source
    ]


def supports_function_calling(provider: str, model: str = "", base_url: str = "") -> bool:
    """Check if a provider/model combo supports native function calling."""
    provider_lower = provider.lower()

    # ── International providers ──────────────────────────────────────────────
    if provider_lower in ("claude", "anthropic"):
        return True
    if provider_lower in ("openai", "gpt"):
        return True
    if provider_lower == "deepseek":
        return True
    if provider_lower in ("grok", "xai", "x.ai"):
        return True
    if provider_lower in ("gemini", "google"):
        return True
    if provider_lower in ("mistral", "mistralai"):
        return True
    if provider_lower in ("cohere"):
        return True
    if provider_lower in ("reka"):
        return True

    # ── Chinese providers ────────────────────────────────────────────────────
    if provider_lower in ("glm", "zhipu"):
        return True
    if provider_lower in ("qwen", "alibaba", "dashscope"):
        return True
    if provider_lower in ("baidu", "ernie", "wenxin"):
        return True
    if provider_lower in ("baichuan"):
        return True
    if provider_lower in ("yi", "01ai", "lingyiwanwu"):
        return True
    if provider_lower in ("minimax"):
        return True
    if provider_lower in ("moonshot", "kimi"):
        return True
    if provider_lower in ("sensetime", "sensenova"):
        return True
    if provider_lower in ("iflytek", "spark", "xunfei"):
        return True
    if provider_lower in ("doubao", "bytedance"):
        return True
    if provider_lower in ("tencent", "hunyuan"):
        return True

    model_lower = model.lower()
    base_lower = base_url.lower()

    # ── International models (by name/url) ───────────────────────────────────
    if any(k in model_lower or k in base_lower for k in ("grok", "x.ai", "xai")):
        return True
    if any(k in model_lower for k in ("gpt-4", "gpt-3.5", "claude", "gemini")):
        return True
    if any(k in model_lower or k in base_lower for k in ("mistral", "mixtral")):
        return True
    if any(k in model_lower or k in base_lower for k in ("cohere", "command")):
        return True
    if any(k in model_lower or k in base_lower for k in ("llama", "meta-llama")):
        return True

    # ── Chinese models (by name/url) ─────────────────────────────────────────
    if any(k in model_lower or k in base_lower for k in ("qwen", "alibaba", "dashscope")):
        return True
    if any(k in model_lower or k in base_lower for k in ("glm", "zhipu", "bigmodel")):
        return True
    if any(k in model_lower or k in base_lower for k in ("ernie", "wenxin", "baidu", "aistudio")):
        return True
    if any(k in model_lower or k in base_lower for k in ("baichuan")):
        return True
    if any(k in model_lower or k in base_lower for k in ("yi-", "01.ai", "lingyiwanwu")):
        return True
    if any(k in model_lower or k in base_lower for k in ("minimax", "abab")):
        return True
    if any(k in model_lower or k in base_lower for k in ("moonshot", "kimi")):
        return True
    if any(k in model_lower or k in base_lower for k in ("sensenova", "sensechat")):
        return True
    if any(k in model_lower or k in base_lower for k in ("spark", "iflytek", "xunfei")):
        return True
    if any(k in model_lower or k in base_lower for k in ("doubao", "bytedance", "volcengine")):
        return True
    if any(k in model_lower or k in base_lower for k in ("hunyuan", "tencent")):
        return True

    # ── Custom aggregators ───────────────────────────────────────────────────
    if provider_lower == "custom":
        if any(k in model_lower or k in base_lower for k in (
            "openrouter", "together", "fireworks", "groq", "perplexity",
        )):
            return True

    return False
