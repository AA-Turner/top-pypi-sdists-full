"""Knowledge ingestion: add, import, learn, teach from code and files."""
from __future__ import annotations

import json
from pathlib import Path

from kanban_framework.domain.knowledge import KnowledgeManager


def _check_scope(km: KnowledgeManager) -> dict | None:
    """Check if knowledge.scope is configured."""
    import os
    if os.environ.get("KANBAN_KNOWLEDGE_SCOPE"):
        return None
    scope = getattr(km, '_scope', '')
    if not scope:
        return {
            "error": "knowledge.scope 未配置。请先执行 kanban init 或手动设置 config.json 中 knowledge.scope 字段。",
            "code": "SCOPE_REQUIRED",
            "hint": "config.json: {\"knowledge\": {\"scope\": \"your-name\"}}",
            "env_override": "KANBAN_KNOWLEDGE_SCOPE=ci kanban knowledge add ...",
        }
    return None


def _title_similarity(a: str, b: str) -> float:
    """Simple character-level common prefix ratio for duplicate detection."""
    if not a or not b:
        return 0.0
    matches = 0
    bi = 0
    for ch in a:
        pos = b.find(ch, bi)
        if pos >= 0:
            matches += 1
            bi = pos + 1
    return 2.0 * matches / (len(a) + len(b))


def handle_add(km: KnowledgeManager, args: list[str]) -> dict:
    kwargs: dict = {"domain": "infra", "category": "工具", "title": "", "content": "",
                     "code_example": "", "source": {}, "status": "pending"}
    ttl_days = None
    verify = False
    benchmark_raw = None
    biz = None
    i = 0
    while i < len(args):
        if args[i] == "--verify":
            verify = True; i += 1
        elif args[i] == "--benchmark" and i + 1 < len(args):
            benchmark_raw = args[i + 1]; i += 2
        elif args[i] == "--ttl" and i + 1 < len(args):
            try:
                ttl_days = int(args[i + 1])
            except ValueError:
                pass
            i += 2
        elif args[i] == "--biz" and i + 1 < len(args):
            biz = args[i + 1]; i += 2
        elif args[i] in ("--domain", "--category", "--title", "--severity", "--status"):
            key = args[i][2:]
            kwargs[key] = args[i + 1]; i += 2
        elif args[i] == "--tags":
            raw_tags = args[i + 1]
            try:
                parsed = json.loads(raw_tags)
                kwargs["tags"] = parsed if isinstance(parsed, list) else [parsed]
            except (json.JSONDecodeError, ValueError):
                kwargs["tags"] = raw_tags.split(",")
            i += 2
        elif args[i] == "--content":
            kwargs["content"] = args[i + 1]; i += 2
        elif args[i] == "--code-example":
            kwargs["code_example"] = args[i + 1]; i += 2
        elif args[i] == "--source" and i + 1 < len(args):
            try:
                kwargs["source"] = json.loads(args[i + 1])
            except json.JSONDecodeError:
                kwargs["source"] = {"raw": args[i + 1]}
            i += 2
        else:
            if not kwargs.get("_positional_used"):
                if not kwargs["content"]:
                    kwargs["content"] = args[i]
                elif not kwargs["title"]:
                    kwargs["title"] = args[i]
                kwargs["_positional_used"] = True
            i += 1
    kwargs.pop("_positional_used", None)
    if ttl_days is not None and ttl_days > 0:
        kwargs["ttl_days"] = ttl_days
    if benchmark_raw is not None:
        try:
            kwargs["benchmark"] = json.loads(benchmark_raw)
        except json.JSONDecodeError:
            return {"error": f"--benchmark must be valid JSON: {benchmark_raw[:80]}"}
    if biz is not None:
        kwargs["biz_context"] = biz
    scope_err = _check_scope(km)
    if scope_err:
        return scope_err
    try:
        entry = km.add_entry(**kwargs)
    except ValueError as e:
        return {"error": str(e)}
    if entry.get("skipped"):
        return {"skipped": True, "existing_id": entry.get("existing_id"), "reason": entry.get("reason")}
    result = {"added": entry["id"], "title": entry.get("title", ""), "ttl_days": ttl_days}
    if verify:
        stored = km.get_entry(entry["id"])
        result["verify"] = {
            "title_ok": bool(stored.get("title", "").strip()),
            "content_ok": bool(stored.get("content", "").strip()),
            "tags_ok": isinstance(stored.get("tags"), list),
            "all_ok": bool(stored.get("title", "").strip() or stored.get("content", "").strip()),
        }
    return result


def handle_import(km: KnowledgeManager, args: list[str]) -> dict:
    file_path = None
    i = 0
    while i < len(args):
        if args[i] == "--entry-file" and i + 1 < len(args):
            file_path = args[i + 1]; i += 2
        else:
            i += 1
    if not file_path:
        return {"error": "--entry-file required"}
    data = json.loads(Path(file_path).read_text(encoding="utf-8"))
    if isinstance(data, list):
        entries = data
    elif isinstance(data, dict) and "entries" in data:
        entries = data["entries"]
    elif isinstance(data, dict):
        entries = [data]
    else:
        entries = []
    added = []
    skipped = []
    for e in entries:
        add_kwargs: dict = dict(
            domain=e.get("domain", "infra"), category=e.get("category", "工具"),
            title=e["title"], content=e["content"],
            tags=e.get("tags", []), severity=e.get("severity", "medium"),
            source=e.get("source", {}),
        )
        if e.get("biz_context"):
            add_kwargs["biz_context"] = e["biz_context"]
        if e.get("id"):
            add_kwargs["entry_id"] = e["id"]
        if e.get("status"):
            add_kwargs["status"] = e["status"]
        entry = km.add_entry(**add_kwargs)
        if entry.get("skipped"):
            skipped.append({"id": e.get("id"), "reason": entry.get("reason")})
        else:
            added.append(entry["id"])
    return {"imported": len(added), "ids": added, "skipped": len(skipped), "skip_details": skipped}


def handle_export(km: KnowledgeManager, args: list[str]) -> dict:
    """Export knowledge entries to a JSON file."""
    output_file = None
    domain = None
    status_filter = "active"
    i = 0
    while i < len(args):
        if args[i] == "--output" and i + 1 < len(args):
            output_file = args[i + 1]; i += 2
        elif args[i] == "--domain" and i + 1 < len(args):
            domain = args[i + 1]; i += 2
        elif args[i] == "--status" and i + 1 < len(args):
            status_filter = args[i + 1]; i += 2
        else:
            i += 1
    entries = km.list_entries(domain=domain, status=status_filter)
    export_data = {"entries": entries, "count": len(entries)}
    if output_file:
        Path(output_file).write_text(
            json.dumps(export_data, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        return {"exported": len(entries), "output_file": output_file}
    return {"exported": len(entries), "entries": entries}


def _auto_extract_entry(file_path: str, content: str, domain: str, status: str) -> dict | None:
    """Static analysis: extract module knowledge from Python source code."""
    import re

    module_name = Path(file_path).stem
    if module_name in ("__init__", "__pycache__"):
        return None
    doc_match = re.search(r'(?:"""(.*?)"""|\'\'\'(.*?)\'\'\')', content, re.DOTALL)
    doc = ""
    if doc_match:
        doc = (doc_match.group(1) or doc_match.group(2) or "").strip()
        doc = " ".join(doc.split())[:300]
    funcs = re.findall(r'^\s*def\s+(\w+)', content, re.MULTILINE)
    classes = re.findall(r'^\s*class\s+(\w+)', content, re.MULTILINE)
    imports = re.findall(r'^\s*(?:from|import)\s+(\S+)', content, re.MULTILINE)
    _STDLIB = frozenset((
        "__future__", "os", "sys", "json", "re", "math", "pathlib", "datetime",
        "time", "collections", "typing", "dataclasses", "random", "enum", "abc",
        "itertools", "functools", "io", "subprocess", "logging", "hashlib",
        "shutil", "tempfile", "argparse",
    ))
    local_imports = [m for m in imports if m.split(".")[0] not in _STDLIB]

    parts = []
    if doc:
        parts.append(doc)
    if funcs:
        parts.append(f"关键函数({len(funcs)}): {', '.join(funcs[:6])}")
    if classes:
        parts.append(f"关键类({len(classes)}): {', '.join(classes[:4])}")
    if local_imports:
        parts.append(f"依赖模块: {', '.join(local_imports[:8])}")
    if not parts:
        return None
    content_text = "。".join(parts) + "。"

    tags = [f"biz:{domain}", f"module:{module_name}", "stack:python"]
    if "test" in module_name.lower():
        tags.append("pattern:testing")

    code_example = ""
    import re as _re
    for fn in funcs[:2]:
        sig = _re.search(rf'def {fn}\((.*?)\):', content)
        if sig:
            code_example += f"def {fn}({sig.group(1)}): ...\n"
    if not code_example and classes:
        code_example = f"class {classes[0]}(...): ..."

    return {
        "domain": domain, "category": "架构", "title": f"{module_name} 模块",
        "content": content_text, "code_example": code_example.strip(), "tags": tags,
    }


def handle_learn(km: KnowledgeManager, args: list[str]) -> dict:
    path = ""
    domain = ""
    follow_deps = True
    activate = False
    auto = False
    i = 0
    while i < len(args):
        if args[i] == "--path" and i + 1 < len(args):
            path = args[i + 1]; i += 2
        elif args[i] == "--domain" and i + 1 < len(args):
            domain = args[i + 1]; i += 2
        elif args[i] == "--no-follow-deps":
            follow_deps = False; i += 1
        elif args[i] == "--activate":
            activate = True; i += 1
        elif args[i] == "--auto":
            auto = True; i += 1
        else:
            i += 1
    if not path:
        return {"error": "--path required"}
    if not domain:
        return {"error": "--domain required"}

    p = Path(path)
    if not p.exists():
        return {"error": f"path not found: {path}"}

    code_files: list[dict] = []
    deps_found: list[str] = []
    if p.is_file():
        code_files.append({"path": str(p), "content": p.read_text(encoding="utf-8")[:3000]})
        deps_found = find_imports(p.read_text(encoding="utf-8"), p.parent)
    elif p.is_dir():
        for f in sorted(p.rglob("*.py")):
            if f.is_file():
                content = f.read_text(encoding="utf-8")[:3000]
                code_files.append({"path": str(f), "content": content})
                if follow_deps:
                    deps_found.extend(find_imports(content, f.parent))

    deps_found = sorted(set(deps_found))
    dep_files: list[dict] = []
    for dep_path in deps_found:
        dep_p = Path(dep_path)
        if dep_p.is_file() and dep_p.suffix == ".py":
            dep_files.append({"path": dep_path, "content": dep_p.read_text(encoding="utf-8")[:3000]})

    known_modules: list[str] = []
    new_modules: list[str] = []
    for cf in code_files + dep_files:
        module_name = Path(cf["path"]).stem
        existing = km.search_by_tag(f"module:{module_name}")
        if existing:
            known_modules.append(module_name)
        else:
            new_modules.append(module_name)

    entry_status = "active" if activate else "draft"
    added_ids: list[str] = []
    if auto and new_modules:
        for cf in code_files + dep_files:
            module_name = Path(cf["path"]).stem
            if module_name in known_modules:
                continue
            entry = _auto_extract_entry(cf["path"], cf["content"], domain, entry_status)
            if entry:
                try:
                    eid = km.add_entry(
                        domain=entry["domain"], category=entry["category"],
                        title=entry["title"], content=entry["content"],
                        code_example=entry.get("code_example", ""),
                        tags=entry.get("tags", []), status=entry_status, upsert=True,
                    )
                    added_ids.append(eid)
                except Exception:
                    pass

    return {
        "action": "learn", "domain": domain, "path": str(p),
        "target_files": len(code_files), "dependency_files": len(dep_files),
        "deps_found": deps_found[:20], "known_modules": known_modules,
        "new_modules": new_modules,
        "code_files": code_files + dep_files if not auto else [],
        "activate": activate, "auto": auto, "auto_added": added_ids,
        "instruction": (
            f"Read the code files above. For each file, check if the module is already in known_modules. "
            f"Only extract NEW understanding for modules in new_modules={new_modules}. "
            f"For each new module, call knowledge add with domain='{domain}', status='{entry_status}', "
            f"category=架构, title='<module_name> 模块结构与职责', "
            f"content='模块职责、关键函数/类、依赖关系', "
            f"tags=['biz:{domain}', 'module:<name>', 'stack:python'], "
            f"code_example='关键接口代码片段'. "
            f"Follow knowledge-accumulation-guide.md boundary rules."
        ),
    }


def find_imports(content: str, parent_dir) -> list[str]:
    """Find local/relative module imports in Python code. Returns resolved file paths."""
    import re
    root = parent_dir
    while root.parent != root and not (root / ".kanban").is_dir():
        root = root.parent

    _STDLIB = frozenset((
        "__future__", "os", "sys", "json", "re", "math", "pathlib", "datetime",
        "time", "collections", "typing", "dataclasses", "random", "enum", "abc",
        "itertools", "functools", "io", "subprocess", "logging", "hashlib",
        "shutil", "tempfile",
    ))
    deps = []
    for m in re.finditer(
        r'(?:^from\s+(\S+)\s+import)|(?:^import\s+(\S+))', content, re.MULTILINE
    ):
        mod_path = m.group(1) or m.group(2)
        if not mod_path:
            continue
        if mod_path.split(".")[0] in _STDLIB:
            continue
        if mod_path.startswith("."):
            clean = mod_path.lstrip(".")
            candidate = parent_dir / f"{clean}.py"
            if candidate.is_file():
                deps.append(str(candidate))
                continue
            candidate = parent_dir / clean / "__init__.py"
            if candidate.is_file():
                deps.append(str(candidate))
                continue
        parts = mod_path.split(".")
        candidate = root.parent / f"{'/'.join(parts)}.py"
        if candidate.is_file():
            deps.append(str(candidate))
            continue
        if len(parts) == 1:
            candidate = parent_dir / f"{parts[0]}.py"
            if candidate.is_file():
                deps.append(str(candidate))
    return deps


def handle_teach(km: KnowledgeManager, args: list[str]) -> dict:
    """Teach the framework a procedural business workflow. (#239)"""
    import re

    title = ""
    steps = []
    domain = "infra"
    category = "流程"
    biz = None
    i = 0
    while i < len(args):
        if args[i] == "--domain" and i + 1 < len(args):
            domain = args[i + 1]; i += 2
        elif args[i] == "--category" and i + 1 < len(args):
            category = args[i + 1]; i += 2
        elif args[i] == "--title" and i + 1 < len(args):
            title = args[i + 1]; i += 2
        elif args[i] == "--step" and i + 1 < len(args):
            steps.append(args[i + 1]); i += 2
        elif args[i] == "--biz" and i + 1 < len(args):
            biz = args[i + 1]; i += 2
        elif not title:
            title = args[i]; i += 1
        else:
            i += 1

    if not title or not steps:
        return {"error": "usage: kanban knowledge teach \"<title>\" --step \"<step1>\" --step \"<step2>\" ..."}

    scope_err = _check_scope(km)
    if scope_err:
        return scope_err

    content_lines = [f"# {title}", "", "## 步骤"]
    for j, s in enumerate(steps, 1):
        clean = re.sub(r'^\d+[\.\)、]\s*', '', s)
        content_lines.append(f"{j}. {clean}")
    content = "\n".join(content_lines)

    add_kwargs: dict = dict(
        domain=domain, category=category, title=title,
        content=content, severity="medium", status="active",
        entry_type="procedure", steps=steps,
    )
    if biz is not None:
        add_kwargs["biz_context"] = biz
    entry = km.add_entry(**add_kwargs)
    return {"taught": entry["id"], "title": title, "steps": len(steps)}


# ── Benchmark evaluation (#397 Phase 2) ──────────────────────────────────

_EVAL_REPORT_SCHEMA = """```json
{
  "solution": "基于知识库给出的解决方案（代码或文字描述）",
  "score": 8.5,
  "verdict": "pass",
  "evidence": "具体说明为什么这个分数",
  "used_knowledge": true,
  "concerns": []
}
```

其中 verdict 必须为: "pass"（符合期望）、"partial"（部分符合）、"fail"（仍为错误行为）"""

_BENCHMARK_PROMPT_TEMPLATE = """\
## 知识库 Benchmark 评估任务

### 评估目标
验证知识条目「{title}」是否能指导你正确处理以下需求。

### 原始需求（用户视角）
{user_requirement}

### AI 历史错误行为
{ai_error}

### 期望的正确行为
{expected_behavior}

### 知识库参考内容
{content}

### 你的任务
1. 仅基于上述知识库内容，解决原始需求
2. 自评你的输出是否符合「期望的正确行为」
3. 输出 JSON 评估报告，保存为 benchmark_eval_report.json：

{report_schema}

### 评分标准
- 10分：完全符合期望行为，无遗漏
- 7-9分：基本符合，有小偏差
- 4-6分：部分符合，有明显不足
- 0-3分：仍为错误行为或未利用知识库
"""

_VALID_VERDICTS = frozenset({"pass", "partial", "fail"})


def handle_benchmark(km: KnowledgeManager, args: list[str]) -> dict:
    """Generate evaluation prompt or submit evaluation report for a benchmark entry."""
    if not args:
        return {"error": "entry_id required"}

    entry_id = ""
    generate_prompt = False
    submit_report = ""
    output_file = ""
    i = 0
    while i < len(args):
        if args[i] == "--generate-prompt":
            generate_prompt = True
            i += 1
        elif args[i] == "--submit-report" and i + 1 < len(args):
            submit_report = args[i + 1]
            i += 2
        elif args[i] == "--output" and i + 1 < len(args):
            output_file = args[i + 1]
            i += 2
        elif not args[i].startswith("-"):
            entry_id = args[i]
            i += 1
        else:
            i += 1

    if not entry_id:
        return {"error": "entry_id required"}

    entry = km.get_entry(entry_id)
    if not entry:
        return {"error": f"entry {entry_id} not found"}

    benchmark = entry.get("benchmark")
    if not benchmark or not isinstance(benchmark, dict):
        return {
            "error": f"entry {entry_id} has no benchmark data",
            "hint": "Add benchmark when creating the entry: --benchmark '{\"user_requirement\":\"...\",\"ai_error\":\"...\",\"expected_behavior\":\"...\"}'"
        }

    if generate_prompt:
        return _generate_benchmark_prompt(entry, benchmark, output_file)

    if submit_report:
        return _submit_benchmark_report(km, entry_id, submit_report)

    return {"error": "specify --generate-prompt or --submit-report"}


def _generate_benchmark_prompt(entry: dict, benchmark: dict, output_file: str) -> dict:
    prompt = _BENCHMARK_PROMPT_TEMPLATE.format(
        title=entry.get("title", ""),
        user_requirement=benchmark.get("user_requirement", "(未提供)"),
        ai_error=benchmark.get("ai_error", "(未提供)"),
        expected_behavior=benchmark.get("expected_behavior", "(未提供)"),
        content=entry.get("content", "(未提供)"),
        report_schema=_EVAL_REPORT_SCHEMA,
    )

    if output_file:
        Path(output_file).write_text(prompt, encoding="utf-8")
        return {"generated": True, "output_file": output_file}

    return {"generated": True, "prompt": prompt}


def _submit_benchmark_report(km: KnowledgeManager, entry_id: str, report_path: str) -> dict:
    path = Path(report_path)
    if not path.is_file():
        return {"error": f"report file not found: {report_path}"}

    try:
        report = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        return {"error": f"invalid JSON in report: {e}"}

    verdict = report.get("verdict", "")
    if verdict not in _VALID_VERDICTS:
        return {"error": f"invalid verdict: {verdict}. Must be one of: {sorted(_VALID_VERDICTS)}"}

    score = report.get("score", 0)
    try:
        score = float(score)
    except (TypeError, ValueError):
        return {"error": f"invalid score: {score}. Must be a number 0-10"}
    if not (0 <= score <= 10):
        return {"error": f"score out of range: {score}. Must be 0-10"}

    evaluation = {
        "score": score,
        "verdict": verdict,
        "evidence": report.get("evidence", "")[:500],
        "used_knowledge": bool(report.get("used_knowledge", False)),
        "ai_output": report.get("solution", "")[:500],
    }
    if report.get("concerns"):
        evaluation["concerns"] = report["concerns"][:5]

    result = km.update_benchmark_evaluation(entry_id, evaluation)
    return {"submitted": True, **result}
