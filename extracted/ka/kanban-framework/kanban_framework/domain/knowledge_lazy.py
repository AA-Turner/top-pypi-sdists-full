"""Lazy-loaded resources, constants, and helper functions for knowledge module.

Extracted from knowledge.py — zero import side effects. All expensive
initialization (jieba, chromadb, fastembed) is deferred until first use.
"""
from __future__ import annotations

import struct
from datetime import datetime, timezone

# ── Module-level state (lazy singletons) ──────────────────────────────────

_jieba = None
_jieba_dict_loaded = False
_chromadb = None

_EMBED_MODEL = None
_EMBED_FAILED = False
_EMBED_DIM = 512  # bge-small-zh-v1.5


# ── Lazy loaders ─────────────────────────────────────────────────────────

def _get_jieba():
    """Lazy-init jieba with built-in tech dictionary. (#324)"""
    global _jieba, _jieba_dict_loaded
    if _jieba is None:
        try:
            import jieba as _j
            _jieba = _j
        except ImportError:
            _jieba = False
    if _jieba and not _jieba_dict_loaded:
        _load_jieba_dict(_jieba)
        _jieba_dict_loaded = True
    return _jieba if _jieba is not False else None


def _load_jieba_dict(jieba_mod):
    """Load built-in tech dictionary and optional user dict from config. (#324)"""
    from pathlib import Path
    builtin = Path(__file__).parent / "jieba_dict.txt"
    if builtin.is_file():
        try:
            jieba_mod.load_userdict(str(builtin))
        except Exception:
            pass
    try:
        from kanban_framework.infra.config import Config
        from kanban_framework.infra.filesystem import Filesystem
        fs = Filesystem()
        cfg = Config(fs)
        user_dict = cfg._config.get("knowledge", {}).get("jieba_user_dict", "")
        if user_dict:
            user_path = Path(user_dict).expanduser().resolve()
            if user_path.is_file():
                jieba_mod.load_userdict(str(user_path))
    except Exception:
        pass


def _get_chromadb():
    global _chromadb
    if _chromadb is None:
        try:
            import chromadb as _c
            _chromadb = _c
        except ImportError:
            _chromadb = False
    return _chromadb if _chromadb is not False else None


def _get_embed_model():
    """Lazy-load bge-small-zh-v1.5 via fastembed (ONNX, no PyTorch)."""
    global _EMBED_MODEL, _EMBED_FAILED, _EMBED_DIM
    if _EMBED_FAILED:
        return None
    if _EMBED_MODEL is None:
        try:
            from fastembed import TextEmbedding
            _EMBED_MODEL = TextEmbedding(model_name="BAAI/bge-small-zh-v1.5")
            probe = list(_EMBED_MODEL.embed(["dim_probe"]))[0]
            _EMBED_DIM = len(probe)
        except Exception:
            _EMBED_FAILED = True
            return None
    return _EMBED_MODEL


# ── Embedding helpers ─────────────────────────────────────────────────────

def _embed(text: str) -> bytes | None:
    """Compute float32 embedding for text. Returns packed bytes or None."""
    if _EMBED_FAILED or not text:
        return None
    model = _get_embed_model()
    if model is None:
        return None
    try:
        vec = list(model.embed([text]))[0]
        return struct.pack(f"{len(vec)}f", *vec)
    except Exception:
        return None


def _unpack_embedding(blob: bytes) -> list[float]:
    """Unpack BLOB back to float list."""
    n = len(blob) // 4
    return list(struct.unpack(f"{n}f", blob))


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    """Cosine similarity between two vectors (both should be normalized)."""
    return sum(x * y for x, y in zip(a, b))


def _segment(text: str) -> str:
    """Segment Chinese text with jieba. Returns space-separated tokens."""
    if not _get_jieba() or not text:
        return text
    if not any('一' <= c <= '鿿' for c in text):
        return text
    words = _get_jieba().cut(text)
    return " ".join(w for w in words if w.strip())


# ── Constants ─────────────────────────────────────────────────────────────

DEFAULT_DOMAINS = {
    "cli": {"label": "CLI 命令", "keywords": ["argparse", "dispatch", "subcommand", "cli"]},
    "agent": {"label": "Agent 定义", "keywords": ["agent", "prompt", "role", "model"]},
    "testing": {"label": "测试", "keywords": ["pytest", "assert", "mock", "coverage", "test"]},
    "infra": {"label": "基础设施", "keywords": ["filesystem", "git", "config", "worktree", "path"]},
    "workflow": {"label": "工作流", "keywords": ["FSM", "state", "transition", "iteration", "phase"]},
    "dashboard": {"label": "看板仪表盘", "keywords": ["dashboard", "frontend", "js", "css"]},
    "git": {"label": "版本控制", "keywords": ["commit", "branch", "merge", "push", "remote"]},
    "web": {"label": "Web 开发", "keywords": ["fastapi", "flask", "django", "express", "api", "rest", "http", "router", "middleware", "cors"]},
    "database": {"label": "数据库", "keywords": ["sqlite", "sql", "postgresql", "mysql", "orm", "migration", "query", "transaction"]},
    "ui": {"label": "前端界面", "keywords": ["component", "react", "vue", "template", "render", "dom", "event", "async"]},
    "game": {"label": "游戏开发", "keywords": ["game", "pygame", "sprite", "collision", "render", "fps", "input", "animation"]},
    "security": {"label": "安全", "keywords": ["auth", "token", "jwt", "hash", "encrypt", "permission", "xss", "csrf"]},
}

VALID_CATEGORIES = {
    "架构": {"label": "架构", "desc": "系统设计、模块结构、数据流", "weight": 1.0},
    "踩坑": {"label": "踩坑", "desc": "已知的坑和 workaround", "weight": 1.3},
    "反模式": {"label": "反模式", "desc": "明确的错误做法及其危害", "weight": 1.5},
    "最佳实践": {"label": "最佳实践", "desc": "经过验证的推荐做法", "weight": 1.2},
    "优化": {"label": "优化", "desc": "性能或质量提升方案", "weight": 1.0},
    "流程": {"label": "流程", "desc": "工作流、规范、SOP", "weight": 1.0},
    "接口": {"label": "接口", "desc": "API/协议/数据格式规范", "weight": 1.0},
    "工具": {"label": "工具", "desc": "工具使用技巧", "weight": 1.0},
}

VALID_SEVERITIES = {
    "high": {"label": "high", "desc": "必须遵守，违反会导致严重问题", "pitfall_weight": 1.5},
    "medium": {"label": "medium", "desc": "建议遵守，违反可能导致问题", "pitfall_weight": 1.0},
    "low": {"label": "low", "desc": "参考性质", "pitfall_weight": 0.8},
}

STALE_DAYS = 30

DEFAULT_SCORE_THRESHOLD = 0.0

TECH_ABBREVIATIONS: dict[str, str] = {
    "k8s": "Kubernetes", "k3s": "K3s",
    "ec2": "AWS EC2", "ecs": "AWS ECS", "eks": "AWS EKS",
    "s3": "AWS S3", "rds": "AWS RDS", "vpc": "AWS VPC",
    "cdn": "CDN", "lb": "Load Balancer", "dns": "DNS",
    "tls": "TLS", "ssl": "SSL", "https": "HTTPS", "ssh": "SSH", "vpn": "VPN",
    "jwt": "JWT JSON Web Token", "oauth": "OAuth OAuth2", "oauth2": "OAuth2",
    "sso": "SSO Single Sign-On", "rbac": "RBAC Role-Based Access Control",
    "mfa": "MFA Multi-Factor Authentication",
    "csrf": "CSRF Cross-Site Request Forgery", "xss": "XSS Cross Site Scripting",
    "cors": "CORS Cross Origin Resource Sharing",
    "api": "API", "sdk": "SDK", "cli": "CLI Command Line Interface",
    "ci_cd": "CI/CD", "cicd": "CI/CD Continuous Integration Deployment",
    "orm": "ORM Object-Relational Mapping",
    "mvc": "MVC Model View Controller", "mvvm": "MVVM Model View ViewModel",
    "ddd": "DDD Domain-Driven Design", "tdd": "TDD Test-Driven Development",
    "bdd": "BDD Behavior-Driven Development",
    "db": "Database", "sql": "SQL", "nosql": "NoSQL",
    "crud": "CRUD Create Read Update Delete",
    "rest": "REST Representational State Transfer", "grpc": "gRPC",
    "mq": "Message Queue", "rpc": "RPC Remote Procedure Call",
    "dag": "DAG Directed Acyclic Graph", "fsm": "FSM Finite State Machine",
    "dsl": "DSL Domain-Specific Language",
    "pyqt": "PyQt Qt Python GUI", "pyside": "PySide Qt Python GUI",
    "qt": "Qt Framework C++ GUI", "tkinter": "Tkinter Python GUI",
    "wx": "wxPython wxWidgets GUI",
}


# ── Helper functions ──────────────────────────────────────────────────────

def _expand_abbreviations(query: str) -> str:
    """Expand known tech abbreviations in a search query. (#230)"""
    if not query:
        return query
    import re
    expanded = []
    for word in query.split():
        key = word.lower().rstrip(",.;:")
        if key in TECH_ABBREVIATIONS:
            full = re.sub(r'[^a-zA-Z0-9\s]', ' ', TECH_ABBREVIATIONS[key])
            full = ' '.join(full.split())
            expanded.append(f"{word} OR {full}")
        else:
            expanded.append(word)
    return " ".join(expanded)


def _stale_penalty(stale_at_str: str | None) -> float:
    """Return a score multiplier for stale entries. (#226)"""
    if not stale_at_str:
        return 1.0
    try:
        stale_dt = datetime.fromisoformat(stale_at_str)
        now = datetime.now(timezone.utc)
        if stale_dt.tzinfo is None:
            stale_dt = stale_dt.replace(tzinfo=timezone.utc)
        if now < stale_dt:
            return 1.0
        days_past = (now - stale_dt).days
        if days_past <= 30:
            return 0.7
        elif days_past <= 90:
            return 0.4
        else:
            return 0.2
    except (ValueError, TypeError):
        return 1.0


def _substring_match_score(query: str, text: str) -> float:
    """Check if query appears as substring in text. Returns bonus score. (#224)"""
    if not query or not text:
        return 0.0
    ql = query.lower()
    tl = text.lower()
    if ql in tl:
        return min(0.15, len(ql) / len(tl) * 0.15)
    return 0.0
