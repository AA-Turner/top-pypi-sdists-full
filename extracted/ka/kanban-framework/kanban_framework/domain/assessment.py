"""Auto-detect task complexity and recommend mode — lighter by default."""
from __future__ import annotations

from kanban_framework.infra.consts import Consts

# Keywords that signal "just do it, no planning needed"
_QUICK_SIGNALS = [
    "typo", "拼写", "错别字",
    "fix", "修复", "hotfix",
    "patch", "补丁",
    "rename", "重命名",
    "bump", "版本号",
    "format", "格式化", "lint",
    "comment", "注释",
    "whitespace", "空格",
    "import", "导入",
    "config change", "改配置",
    "单行", "一行", "one-liner",
    "version", "版本",
    "同步", "sync",
    "常量", "constant",
    "添加常量", "add constant",
]

# Keywords that signal "this needs full FSM with multi-role review"
_HEAVY_SIGNALS = [
    "游戏", "game", "重构", "refactor", "系统", "system", "引擎", "engine",
    "数据库", "database", "迁移", "migration", "微服务", "microservice",
    "分布式", "distributed", "机器学习", "machine learning",
    "多模块", "multi-module", "完整项目", "full project", "框架", "framework",
    "编译器", "compiler", "解析器", "parser",
    "前端", "frontend", "后端", "backend", "认证", "auth system",
    "实时", "realtime", "websocket", "dashboard", "web",
]

# Biz domain inference: keyword → biz_tag mapping.
# Scans task text + project src/ structure to infer the business domain.
_BIZ_DOMAIN_KEYWORDS = {
    "rpg": ["rpg", "角色", "战斗", "combat", "技能", "skill", "怪物", "enemy",
            "装备", "equipment", "回合制", "turn-based", "character", "职业"],
    "web": ["web", "前端", "frontend", "dashboard", "页面", "page", "ui",
            "html", "css", "react", "vue", "api", "rest", "接口"],
    "game": ["game", "游戏", "pygame", "unity", "渲染", "render", "sprite",
             "动画", "animation", "帧", "frame"],
    "data": ["数据", "data", "数据库", "database", "sql", "etl", "分析",
             "analytics", "报表", "report", "csv", "json"],
    "cli": ["cli", "命令行", "command", "脚本", "script", "终端", "terminal",
            "shell", "bash"],
    "security": ["安全", "security", "认证", "auth", "加密", "encrypt",
                 "权限", "permission", "漏洞", "vulnerability"],
}


def _scan_project_domains(src_dir: str | None = None) -> list[str]:
    """Scan project src/ directory to detect business domains from file structure."""
    from pathlib import Path
    if src_dir is None:
        try:
            from kanban_framework.infra.filesystem import Filesystem
            root = Filesystem.find_project_root()
            src_dir = str(root / "src")
        except Exception:
            return []

    src = Path(src_dir)
    if not src.is_dir():
        return []

    domains = []
    for child in sorted(src.iterdir()):
        if child.is_dir() and not child.name.startswith((".", "_", "__")):
            domains.append(child.name.lower())
    return domains


def _infer_biz_tag(title: str, desc: str = "", src_dir: str | None = None) -> str | None:
    """Infer biz_tag from task text and project structure.

    Returns None when no clear domain signal is found — caller should
    leave biz_tag unset rather than guessing.
    """
    text = f"{title} {desc}".lower()

    # 1. Check explicit keyword matches
    scores: dict[str, int] = {}
    for tag, keywords in _BIZ_DOMAIN_KEYWORDS.items():
        score = 0
        for kw in keywords:
            if kw in text:
                score += 1
        if score > 0:
            scores[tag] = score

    # 2. Boost with project structure domains (only amplifies existing signals)
    if scores:
        project_domains = _scan_project_domains(src_dir)
        for d in project_domains:
            for tag in scores:
                keywords = _BIZ_DOMAIN_KEYWORDS.get(tag, [])
                if d in keywords or any(kw in d for kw in keywords):
                    scores[tag] += 2

    if not scores:
        return None

    return max(scores, key=scores.get)


# Keywords that signal "lightweight is fine"
_LIGHT_SIGNALS = [
    "脚本", "script", "工具函数", "utility", "单文件", "single file",
    "文档", "doc", "调整", "tweak", "换", "改一下",
    "优化", "optimize", "性能", "performance",
    "新增", "add", "功能", "feature",
    "修复", "fix", "补丁", "patch", "配置", "config",
    "格式化", "format", "注释", "comment",
    "小改",
]


def assess_task(title: str, description: str) -> dict:
    """Return {recommended_mode, reason, risk_factors, complexity_score}.

    Three tiers: quick (0-0.3) → lightweight (0.3-0.7) → full (0.7+).
    Defaults to lightweight — only promotes to quick for obvious trivial fixes,
    and to full for complex multi-module work.
    """
    text = f"{title} {description}".lower()

    quick = [kw for kw in _QUICK_SIGNALS if kw in text]
    heavy = [kw for kw in _HEAVY_SIGNALS if kw in text]
    light = [kw for kw in _LIGHT_SIGNALS if kw in text]

    # Description length heuristic
    desc_len = len(description.strip()) if description else 0
    short_desc = desc_len < 30

    # Compute complexity score (0-1)
    score = 0.5  # baseline
    if quick:
        score -= 0.3
    if light:
        score -= 0.1
    if heavy:
        score += 0.3
    if short_desc:
        score -= 0.1
    elif desc_len > 100:
        score += 0.1
    score = max(0.0, min(1.0, score))

    # Map score to mode
    default_mode = Consts.DEFAULT_MODE
    if score < 0.35 and (quick or (light and score < 0.2)):
        mode = "quick"
        reason = f"检测到简单信号: {', '.join((quick or light)[:3])} → 建议 quick 模式，直接执行"
        _is_quick = True
    elif heavy:
        mode = default_mode
        reason = f"检测到重度信号: {', '.join(heavy[:3])} → 建议 {default_mode} 模式，含完整评审"
    elif light or score < 0.6:
        mode = default_mode
        reason = f"检测到轻量信号: {', '.join(light[:3])} → 建议 {default_mode} 模式，快速迭代"
    else:
        mode = default_mode
        reason = f"无明显重度信号 → 默认 {default_mode} 模式"
    _is_quick = locals().get('_is_quick', False)

    risk_factors = []
    if any(kw in text for kw in ["数据库", "database", "data migration"]):
        risk_factors.append("数据完整性")
    if any(kw in text for kw in ["认证", "auth", "权限", "permission", "安全", "security"]):
        risk_factors.append("安全风险")
    if any(kw in text for kw in ["性能", "performance", "优化", "optimize"]):
        risk_factors.append("性能要求")

    biz_tag = _infer_biz_tag(title, description)

    return {
        "recommended_mode": mode,
        "reason": reason,
        "complexity_score": round(score, 2),
        "quick_signals": quick,
        "heavy_signals": heavy,
        "risk_factors": risk_factors,
        "biz_tag": biz_tag,
        "quick_requires": {
            "target_file": None,
            "change_type": None,
            "expected_lines": 10,
        } if _is_quick else None,
    }
