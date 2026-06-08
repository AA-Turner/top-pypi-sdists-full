"""Help documentation for knowledge CLI subcommands."""
from __future__ import annotations

from kanban_framework.domain.knowledge import KnowledgeManager


def handle_help(km: KnowledgeManager, args: list[str]) -> dict:
    """Show help for a specific knowledge subcommand or list all commands."""
    if args:
        return _help_for_command(args[0])
    return {
        "usage": "kanban knowledge <subcommand> [options]",
        "description": "知识库管理 — 搜索、添加、导入、导出、健康检查",
        "token_guide": "search/hybrid/semantic --json 先用 .data.summary 筛选，再用 get <id> 取详情",
        "subcommands": {
            "search": "多模式搜索（--domain/--tag/--task/--intent）",
            "hybrid": "混合搜索 FTS5 + 语义",
            "semantic": "纯语义搜索（embedding 向量）",
            "match": "精确 FTS5 关键词匹配",
            "list": "按 domain/category/status 过滤列表",
            "get": "获取单条完整详情 K001",
            "add": "添加知识条目",
            "edit": "编辑知识条目（--title/--content/--domain/--tags 等）",
            "import": "从 JSON 文件批量导入",
            "learn": "从复盘文档提取知识",
            "teach": "创建步骤化教程条目",
            "delete": "删除条目",
            "domains": "列出所有领域",
            "categories": "列出所有分类",
            "health": "健康检查（过期/重复/低质量）",
            "stale": "标记过期条目",
            "gaps": "知识缺口报告",
            "similar": "检测相似条目",
            "usage": "查询任务引用记录",
            "share": "推送到团队共享知识库",
            "backup": "备份 knowledge.db",
            "conflicts": "合并冲突检测",
            "choose": "冲突解决选择",
            "migrate": "迁移旧格式数据",
            "maintenance": "综合维护（语义去重/过期扫描/索引优化）",
        },
    }


def _help_for_command(sub: str) -> dict:
    """Detailed help for a single knowledge subcommand."""
    helps = {
        "search": {
            "usage": "kanban knowledge search [keyword] [--domain D] [--tag T] [--task ID] [--intent I] [--json]",
            "description": "多模式搜索。无参数时默认 hybrid 搜索。intent 选项: pitfall_check / constraint_lookup / experience_reuse / general",
            "examples": [
                "kanban knowledge search 架构",
                "kanban knowledge search --domain python 性能",
                "kanban knowledge search --intent pitfall_check auth",
                "kanban knowledge search --tag biz:rpg",
                "kanban knowledge search --task TASK-001",
            ],
        },
        "hybrid": {
            "usage": "kanban knowledge hybrid <query> [--json]",
            "description": "混合搜索 — FTS5 关键词 + 语义向量 RRF 融合排序。默认 limit=20",
            "examples": ["kanban knowledge hybrid Python PyQt 任务管理"],
        },
        "semantic": {
            "usage": "kanban knowledge semantic <query> [--json]",
            "description": "语义搜索 — 基于 embedding 向量的 ANN 检索。即使关键词不匹配也能召回语义相关条目",
            "examples": ["kanban knowledge semantic 组件化架构设计"],
        },
        "match": {
            "usage": "kanban knowledge match <text>",
            "description": "精确 FTS5 关键词匹配，跳过缩写展开，直接分词查询。返回匹配的领域",
            "examples": ["kanban knowledge match combat module"],
        },
        "list": {
            "usage": "kanban knowledge list [--domain D] [--category C] [--status active|draft|stale]",
            "description": "按过滤条件列出条目。默认 status=active，最多 50 条",
            "examples": [
                "kanban knowledge list",
                "kanban knowledge list --domain python --category 架构",
                "kanban knowledge list --status draft",
            ],
        },
        "get": {
            "usage": "kanban knowledge get <id>",
            "description": "获取单条知识条目的完整详情（含 content/code_example/tags/source 等全字段）",
            "examples": ["kanban knowledge get K001", "kanban knowledge get K021"],
        },
        "add": {
            "usage": "kanban knowledge add [--domain D] [--category C] [--title T] [--content C] [--tags T1,T2] [--severity S] [--status active|draft] [--ttl N] [--code-example E] [--source JSON]",
            "description": "添加知识条目到 knowledge.db。domain 默认 infra，category 默认 工具",
            "examples": [
                'kanban knowledge add --domain python --category 踩坑 --title "GIL 死锁" --content "多线程注意..." --severity high --ttl 90',
                'kanban knowledge add --title "SQL 优化" --content "EXPLAIN 分析..." --tags sql,performance',
            ],
        },
        "edit": {
            "usage": "kanban knowledge edit <id> [--title T] [--content C] [--domain D] [--category C] [--severity S] [--status S] [--tags T1,T2] [--code-example E] [--biz B]",
            "description": "编辑已有知识条目。只更新指定的字段，id 和 created_at 不变",
            "examples": [
                'kanban knowledge edit K001 --title "新标题" --content "新内容"',
                'kanban knowledge edit K002 --domain arch --severity high',
                'kanban knowledge edit K003 --tags "sql,performance,index"',
            ],
        },
        "import": {
            "usage": "kanban knowledge import <file.json>",
            "description": "从 JSON 文件批量导入知识条目。格式: [{\"domain\":..., \"title\":..., \"content\":...}, ...]",
            "examples": ["kanban knowledge import extracted.json"],
        },
        "learn": {
            "usage": "kanban knowledge learn <path> --task-id TASK-NNN",
            "description": "从复盘文档或代码目录提取结构化知识条目",
            "examples": ["kanban knowledge learn .kanban/tasks/TASK-001/iteration-1/retrospective.md --task-id TASK-001"],
        },
        "teach": {
            "usage": "kanban knowledge teach --title T --domain D --category C --step S1 --step S2 ...",
            "description": "创建步骤化教程条目（type=procedure），适用于操作流程类知识",
            "examples": ["kanban knowledge teach --title \"部署流程\" --domain infra --category 工具 --step \"构建镜像\" --step \"推送仓库\" --step \"重启服务\""],
        },
        "delete": {
            "usage": "kanban knowledge delete <id>",
            "description": "删除指定条目",
            "examples": ["kanban knowledge delete K001"],
        },
        "domains": {
            "usage": "kanban knowledge domains",
            "description": "列出所有已注册的知识领域及标签",
            "examples": ["kanban knowledge domains"],
        },
        "categories": {
            "usage": "kanban knowledge categories",
            "description": "列出所有标准分类（架构/踩坑/工具/最佳实践 等）",
            "examples": ["kanban knowledge categories"],
        },
        "health": {
            "usage": "kanban knowledge health",
            "description": "健康检查 — 分类分布、过期条目、即将过期、疑似重复、低质量条目",
            "examples": ["kanban knowledge health"],
        },
        "stale": {
            "usage": "kanban knowledge stale",
            "description": "标记已超过 stale_at 的条目为 stale 状态",
            "examples": ["kanban knowledge stale"],
        },
        "gaps": {
            "usage": "kanban knowledge gaps",
            "description": "知识缺口报告 — 各 domain 的条目密度和缺失分析",
            "examples": ["kanban knowledge gaps"],
        },
        "similar": {
            "usage": "kanban knowledge similar --title T --content C",
            "description": "检测与给定内容相似的已有条目，用于去重参考",
            "examples": ["kanban knowledge similar --title \"JWT 认证\" --content \"使用 PyJWT 实现 token 刷新\""],
        },
        "usage": {
            "usage": "kanban knowledge usage <id>",
            "description": "查询哪些任务引用过该条目",
            "examples": ["kanban knowledge usage K001"],
        },
        "share": {
            "usage": "kanban knowledge share --init <path> | --status | --list | --push",
            "description": "共享知识库管理。--init 创建共享库，--list 预览，--push 推送",
            "examples": [
                "kanban knowledge share --init /shared/team/knowledge.db",
                "kanban knowledge share --list",
                "kanban knowledge share --push --all --domain testing --dry-run",
            ],
        },
        "backup": {
            "usage": "kanban knowledge backup",
            "description": "手动备份 knowledge.db（最多保留 5 个轮转备份）",
            "examples": ["kanban knowledge backup"],
        },
        "conflicts": {
            "usage": "kanban knowledge conflicts --task-id TASK-NNN",
            "description": "检测任务关联的知识条目合并冲突",
            "examples": ["kanban knowledge conflicts --task-id TASK-001"],
        },
        "choose": {
            "usage": "kanban knowledge choose --task-id TASK-NNN --choice-id C --selected K001 --rationale R",
            "description": "解决知识条目合并冲突，选择一个版本",
            "examples": ["kanban knowledge choose --task-id TASK-001 --choice-id C01 --selected K005 --rationale \"版本更新\""],
        },
        "migrate": {
            "usage": "kanban knowledge migrate",
            "description": "迁移旧格式数据（legacy logs → knowledge.db 条目）",
            "examples": ["kanban knowledge migrate"],
        },
        "maintenance": {
            "usage": "kanban knowledge maintenance [--scan-duplicates] [--scan-stale] [--vacuum] [--report] [--confirm] [--threshold 0.85]",
            "description": "综合维护命令。无参数时默认 --report（仅展示）。--scan-duplicates: 语义去重扫描；--scan-stale: 过期候选扫描；--vacuum: 索引优化(VACUUM+FTS rebuild)；--report: 完整报告；--confirm: 输出操作建议供人工确认",
            "examples": [
                "kanban knowledge maintenance --report",
                "kanban knowledge maintenance --scan-duplicates --threshold 0.9",
                "kanban knowledge maintenance --scan-stale --confirm",
                "kanban knowledge maintenance --vacuum",
            ],
        },
    }
    info = helps.get(sub, {"error": f"unknown subcommand: {sub}", "hint": "kanban knowledge help 查看全部"})
    if "subcommand" not in info:
        info["subcommand"] = sub
    return info
