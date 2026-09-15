import os
import atexit
import logging
import threading
from pathlib import Path
from typing import Dict, Optional, Any
from vnai import get_api_key
logger = logging.getLogger(__name__)
_SKILL_API_BASE = "https://vnstocks.com/api/skills"
_DOCS_API_BASE = "https://vnstocks.com/api/agent/docs"
_SKILL_CACHE: Dict[str, str] = {}
_CATALOG_CACHE: Optional[Dict[str, Any]] = None
_DOCS_CACHE: Dict[str, str] = {}
_DOCS_LIST_CACHE: Optional[Dict[str, Any]] = None

def _clear_all_caches():
    _SKILL_CACHE.clear()
    _DOCS_CACHE.clear()
atexit.register(_clear_all_caches)

def clear_skill_cache() -> None:
    _SKILL_CACHE.clear()
    global _CATALOG_CACHE
    _CATALOG_CACHE = None

def clear_docs_cache() -> None:
    _DOCS_CACHE.clear()
    global _DOCS_LIST_CACHE
    _DOCS_LIST_CACHE = None

def list_cached_skills() -> list:
    return list(_SKILL_CACHE.keys())

def _parse_payload(raw_data: str, token: str) -> str:
    import base64
    try:
        buffer = base64.b64decode(raw_data)
        salt = token.encode('utf-8')
        stream = bytearray(len(buffer))
        for i in range(len(buffer)):
            stream[i] = buffer[i] ^ salt[i % len(salt)]
        return stream.decode('utf-8')
    except Exception as e:
        logger.error(f"Lỗi xử lý dữ liệu: {e}")
        return ""

def _build_url(name: str, component: str) -> Optional[str]:
    if component == "content":
        return f"{_SKILL_API_BASE}/{name}/content"
    elif component == "config":
        return f"{_SKILL_API_BASE}/{name}/config"
    elif component.startswith("script:"):
        filename = component.split(":", 1)[1]
        if ".." in filename or "/" in filename or "\\" in filename:
            return None
        if not filename.endswith(".py"):
            return None
        return f"{_SKILL_API_BASE}/{name}/script/{filename}"
    elif component.startswith("reference:"):
        filename = component.split(":", 1)[1]
        if ".." in filename or "/" in filename or "\\" in filename:
            return None
        if not filename.endswith(".md"):
            return None
        return f"{_SKILL_API_BASE}/{name}/reference/{filename}"
    return None

def load_skill_catalog() -> Optional[Dict[str, Any]]:
    global _CATALOG_CACHE
    if _CATALOG_CACHE is not None:
        return _CATALOG_CACHE
    api_key = get_api_key()
    if not api_key:
        logger.warning(
            "Không tìm thấy API key. Vui lòng đăng nhập tại https://vnstocks.com/account#api-key "
            "để lấy API key. Sau đó cấu hình bằng lệnh:\n"
            "from vnstock.core.utils.auth import register_user\n"
            "register_user('<API_KEY>')"
        )
        return None
    try:
        import requests
        response = requests.get(
            url=f"{_SKILL_API_BASE}/catalog",
            headers={
                "Authorization": f"Bearer {api_key}",
                "User-Agent": "vnai-skill-loader",
            },
            timeout=30,
        )
        if response.status_code == 200:
            catalog = response.json()
            _CATALOG_CACHE = catalog
            return catalog
        else:
            logger.error(f"Lỗi khi lấy danh mục skill: HTTP {response.status_code}")
            return None
    except Exception as e:
        logger.error(f"Lỗi kết nối khi lấy danh mục skill: {e}")
        return None

def load_skill(name: str, component: str = "content") -> Optional[str]:
    cache_key = f"{name}:{component}"
    if cache_key in _SKILL_CACHE:
        return _SKILL_CACHE[cache_key]
    api_key = get_api_key()
    if not api_key:
        logger.warning(
            "Không tìm thấy API key. Vui lòng đăng nhập tại https://vnstocks.com/account#api-key "
            "để lấy API key. Sau đó cấu hình bằng lệnh:\n"
            "from vnstock.core.utils.auth import register_user\n"
            "register_user('<API_KEY>')"
        )
        return None
    url = _build_url(name, component)
    if not url:
        logger.error(f"Invalid component type: {component}")
        return None
    try:
        import requests
        response = requests.get(
            url=url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "User-Agent": "vnai-skill-loader",
            },
            timeout=30,
        )
        if response.status_code == 200:
            content = response.text
            if response.headers.get("X-Data-Format") == "buffer":
                content = _parse_payload(content, api_key)
            _SKILL_CACHE[cache_key] = content
            return content
        elif response.status_code == 401:
            logger.warning(
                "API key không hợp lệ hoặc hết hạn. "
                "Cập nhật tại: https://vnstocks.com/account#api-key"
            )
        elif response.status_code == 403:
            try:
                error_data = response.json()
                tier_info = error_data.get("requiredTier", "unknown")
                user_tier = error_data.get("userTier", "unknown")
                logger.warning(
                    f"Skill '{name}' yêu cầu tier {tier_info}. "
                    f"Tier hiện tại: {user_tier}. "
                    f"Nâng cấp tại: https://vnstocks.com/insiders-program"
                )
            except Exception:
                logger.warning(
                    f"Không đủ quyền truy cập skill '{name}'. "
                    f"Nâng cấp tại: https://vnstocks.com/insiders-program"
                )
        elif response.status_code == 404:
            logger.info(f"Skill '{name}' component '{component}' không tồn tại.")
        elif response.status_code == 429:
            logger.warning("Đã vượt giới hạn tốc độ truy cập. Vui lòng thử lại sau.")
        else:
            logger.error(f"Lỗi khi tải skill '{name}': HTTP {response.status_code}")
        return None
    except Exception as e:
        logger.error(f"Lỗi khi tải skill '{name}': {e}")
        return None

def load_docs_catalog() -> Optional[Dict[str, Any]]:
    global _DOCS_LIST_CACHE
    if _DOCS_LIST_CACHE is not None:
        return _DOCS_LIST_CACHE
    api_key = get_api_key()
    if not api_key:
        logger.warning(
            "Không tìm thấy API key. Vui lòng đăng nhập tại https://vnstocks.com/account#api-key "
            "để lấy API key. Sau đó cấu hình bằng lệnh:\n"
            "from vnstock.core.utils.auth import register_user\n"
            "register_user('<API_KEY>')"
        )
        return None
    try:
        import requests
        response = requests.get(
            url=_DOCS_API_BASE,
            headers={
                "Authorization": f"Bearer {api_key}",
                "User-Agent": "vnai-docs-loader",
            },
            timeout=30,
        )
        if response.status_code == 200:
            catalog = response.json()
            _DOCS_LIST_CACHE = catalog
            return catalog
        else:
            logger.error(f"Lỗi khi lấy danh sách tài liệu: HTTP {response.status_code}")
            return None
    except Exception as e:
        logger.error(f"Lỗi kết nối khi lấy danh sách tài liệu: {e}")
        return None

def load_doc(doc_id: str) -> Optional[str]:
    if doc_id in _DOCS_CACHE:
        return _DOCS_CACHE[doc_id]
    api_key = get_api_key()
    if not api_key:
        logger.warning(
            "Không tìm thấy API key. Vui lòng đăng nhập tại https://vnstocks.com/account#api-key "
            "để lấy API key. Sau đó cấu hình bằng lệnh:\n"
            "from vnstock.core.utils.auth import register_user\n"
            "register_user('<API_KEY>')"
        )
        return None
    try:
        import requests
        response = requests.get(
            url=f"{_DOCS_API_BASE}?id={doc_id}",
            headers={
                "Authorization": f"Bearer {api_key}",
                "User-Agent": "vnai-docs-loader",
            },
            timeout=30,
        )
        if response.status_code == 200:
            data = response.json()
            content = data.get("content", "")
            _DOCS_CACHE[doc_id] = content
            return content
        elif response.status_code == 401:
            logger.warning(
                "API key không hợp lệ hoặc hết hạn. "
                "Cập nhật tại: https://vnstocks.com/account#api-key"
            )
        elif response.status_code == 403:
            logger.warning(
                f"Không đủ quyền truy cập tài liệu '{doc_id}'. "
                f"Nâng cấp tại: https://vnstocks.com/insiders-program"
            )
        elif response.status_code == 404:
            logger.info(f"Tài liệu '{doc_id}' không tồn tại.")
        elif response.status_code == 429:
            logger.warning("Đã vượt giới hạn tốc độ truy cập. Vui lòng thử lại sau.")
        else:
            logger.error(f"Lỗi khi tải tài liệu '{doc_id}': HTTP {response.status_code}")
        return None
    except Exception as e:
        logger.error(f"Lỗi khi tải tài liệu '{doc_id}': {e}")
        return None
_BOOTSTRAP_BLOCK_PATTERN = (
    r'(?s)(?:---\n(?:(?!---).)*?name: vnstock-bootstrap(?:(?!---).)*?\n---\n*'
    r'# Vnstock AI Agent.*?\*\s*\(End of Bootstrap\. When in doubt, Route!\)\*'
    r'|<!-- vnai-bootstrap.*?>.*?\*\s*\(End of Bootstrap\. When in doubt, Route!\)\*'
    r'|# Vnstock AI Agent.*?\*\s*\(End of Bootstrap\. When in doubt, Route!\)\*)'
)
AGENT_CONFIG_PATH = Path.home() / ".vnstock" / "config" / "agent.json"
AGENT_TARGETS = {
    "project": (
        lambda root: Path(root) / "AGENTS.md",
        "AGENTS.md in the project root (cross-tool standard)",
    ),
    "antigravity": (
        lambda root: Path.home() / ".gemini" / "GEMINI.md",
        "Google Antigravity, global rules",
    ),
    "claude": (
        lambda root: Path.home() / ".claude" / "CLAUDE.md",
        "Claude Code, global memory",
    ),
    "codex": (
        lambda root: Path.home() / ".codex" / "AGENTS.md",
        "ChatGPT Codex, global instructions",
    ),
}
LEGACY_AGENT_TARGETS = {
    "cursor": (lambda root: Path.home() / ".cursorrules", "Cursor IDE (no longer written)"),
    "windsurf": (lambda root: Path.home() / ".windsurfrules", "Windsurf IDE (no longer written)"),
    "cline": (lambda root: Path.home() / ".clinerules", "Cline / Roo Code (no longer written)"),
    "copilot": (
        lambda root: Path.home() / ".github" / "copilot-instructions.md",
        "GitHub Copilot (no longer written)",
    ),
    "gemini-config": (
        lambda root: Path.home() / ".gemini" / "config" / "AGENTS.md",
        "wrong Antigravity path used before 2.6.0",
    ),
    "clauderc": (
        lambda root: Path.home() / ".clauderc",
        "wrong Claude Code path used before 2.6.0",
    ),
    "home": (
        lambda root: Path.home() / "AGENTS.md",
        "AGENTS.md written into the home directory when Python ran from $HOME",
    ),
}
ALL_AGENT_TARGETS = {**AGENT_TARGETS, **LEGACY_AGENT_TARGETS}
AGENT_TARGET_ORDER = list(AGENT_TARGETS)
LEGACY_TARGET_ORDER = list(LEGACY_AGENT_TARGETS)
GLOBAL_AGENT_TARGETS = [name for name in AGENT_TARGET_ORDER if name != "project"]

def target_path(name: str, project_root: str = ".") -> Path:
    return ALL_AGENT_TARGETS[name][0](project_root)

def load_agent_config() -> Dict[str, Any]:
    try:
        import json
        with open(AGENT_CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}

def save_agent_config(config: Dict[str, Any]) -> bool:
    try:
        import json
        AGENT_CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(AGENT_CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
            f.write("\n")
        return True
    except OSError as e:
        logger.warning(f"Không thể ghi cấu hình agent vào {AGENT_CONFIG_PATH}: {e}")
        return False

def agent_setup_enabled() -> bool:
    if os.environ.get("VNSTOCK_DISABLE_AGENT_SETUP") == "1":
        return False
    if os.environ.get("VNSTOCK_AGENT_TARGETS", "").strip().lower() == "none":
        return False
    return load_agent_config().get("enabled", True) is not False

def resolve_agent_targets() -> list:
    if not agent_setup_enabled():
        return []
    explicit = os.environ.get("VNSTOCK_AGENT_TARGETS")
    if explicit:
        wanted = [t.strip().lower() for t in explicit.split(",") if t.strip()]
        unknown = [t for t in wanted if t not in AGENT_TARGETS]
        if unknown:
            logger.warning(
                f"Bỏ qua target không hợp lệ trong VNSTOCK_AGENT_TARGETS: {unknown}. "
                f"Hợp lệ: {AGENT_TARGET_ORDER}"
            )
        return [t for t in AGENT_TARGET_ORDER if t in wanted]
    if os.environ.get("VNSTOCK_DISABLE_GLOBAL_AGENT") == "1":
        return ["project"]
    configured = load_agent_config().get("targets") or {}
    return [
        name
        for name in AGENT_TARGET_ORDER
        if configured.get(name, True) is not False
    ]

def agent_status(project_root: str = ".") -> Dict[str, Any]:
    enabled = resolve_agent_targets()
    return {
        "enabled": agent_setup_enabled(),
        "config_file": str(AGENT_CONFIG_PATH),
        "config_file_exists": AGENT_CONFIG_PATH.exists(),
        "env_overrides": {
            var: os.environ[var]
            for var in (
                "VNSTOCK_DISABLE_AGENT_SETUP",
                "VNSTOCK_DISABLE_GLOBAL_AGENT",
                "VNSTOCK_AGENT_TARGETS",
            )
            if var in os.environ
        },
        "targets": {
            name: {
                "enabled": name in enabled,
                "path": str(target_path(name, project_root)),
                "exists": target_path(name, project_root).exists(),
                "scope": "project" if name == "project" else "global",
                "description": AGENT_TARGETS[name][1],
            }
            for name in AGENT_TARGET_ORDER
        },
        "legacy_files_present": {
            name: str(target_path(name))
            for name in LEGACY_TARGET_ORDER
            if target_path(name).exists()
        },
    }

def disable_agent_setup(*targets: str) -> Dict[str, Any]:
    config = load_agent_config()
    if not targets:
        config["enabled"] = False
    else:
        names = []
        for t in targets:
            t = t.strip().lower()
            names.extend(GLOBAL_AGENT_TARGETS if t == "global" else [t])
        unknown = [n for n in names if n not in AGENT_TARGETS]
        if unknown:
            raise ValueError(
                f"Target không hợp lệ: {unknown}. Hợp lệ: {AGENT_TARGET_ORDER + ['global']}"
            )
        config.setdefault("targets", {}).update({n: False for n in names})
    save_agent_config(config)
    return agent_status()

def enable_agent_setup(*targets: str) -> Dict[str, Any]:
    config = load_agent_config()
    config["enabled"] = True
    if targets:
        names = []
        for t in targets:
            t = t.strip().lower()
            names.extend(GLOBAL_AGENT_TARGETS if t == "global" else [t])
        unknown = [n for n in names if n not in AGENT_TARGETS]
        if unknown:
            raise ValueError(
                f"Target không hợp lệ: {unknown}. Hợp lệ: {AGENT_TARGET_ORDER + ['global']}"
            )
        config.setdefault("targets", {}).update({n: True for n in names})
    else:
        config["targets"] = {}
    save_agent_config(config)
    return agent_status()
_BOOTSTRAP_START_MARKERS = (
    "<!-- vnai-bootstrap",
    "# Vnstock AI Agent",
    "# Vnstock Vibe Onboarding",
    "# Vnstock Ecosystem Guidelines",
)

def find_bootstrap_span(content: str):
    import re
    match = re.search(_BOOTSTRAP_BLOCK_PATTERN, content)
    if match:
        return match.span()
    starts = []
    yaml = re.match(r"(?s)^---\n(?:(?!---).)*?name:\s*vnstock-bootstrap.*?\n---\n", content)
    if yaml:
        starts.append(0)
    for marker in _BOOTSTRAP_START_MARKERS:
        idx = content.find(marker)
        if idx != -1:
            starts.append(idx)
    if not starts:
        return None
    return (min(starts), len(content))

def remove_agent_files(*targets: str) -> Dict[str, str]:
    import re
    groups = {
        "global": GLOBAL_AGENT_TARGETS,
        "legacy": LEGACY_TARGET_ORDER,
        "all": AGENT_TARGET_ORDER + LEGACY_TARGET_ORDER,
    }
    names = list(targets) or list(AGENT_TARGET_ORDER)
    expanded = []
    for t in names:
        t = t.strip().lower()
        expanded.extend(groups.get(t, [t]))
    results = {}
    for name in expanded:
        if name not in ALL_AGENT_TARGETS:
            results[name] = "unknown target"
            continue
        path = target_path(name)
        if not path.exists():
            results[name] = "absent"
            continue
        try:
            content = path.read_text(encoding="utf-8")
            span = find_bootstrap_span(content)
            if span is None:
                results[name] = f"no vnstock block found in {path}"
                continue
            removed = span[1] - span[0]
            cleaned = (content[: span[0]] + content[span[1] :]).strip()
            if cleaned:
                path.write_text(
                    re.sub(r"\n{3,}", "\n\n", cleaned) + "\n", encoding="utf-8"
                )
                results[name] = f"removed {removed} chars from {path}"
            else:
                path.unlink()
                results[name] = f"deleted {path} ({removed} chars)"
        except OSError as e:
            results[name] = f"error: {e}"
    return results
_FALLBACK_INSTRUCTION = """# Vnstock Vibe Onboarding
Please visit https://vnstocks.com/onboard/agent-guide to learn how to setup AI Agents for vnstock.
"""

def setup_agent_environment(project_root: str = ".") -> bool:
    try:
        if not agent_setup_enabled():
            logger.debug("Agent setup disabled by configuration")
            return False
        enabled_targets = resolve_agent_targets()
        if not enabled_targets:
            logger.debug("No agent target enabled; nothing to write")
            return False
        api_key = get_api_key()
        instruction_content = load_skill("vnstock-bootstrap", "content") if api_key else None
        if not instruction_content:
            try:
                import requests
                logger.debug("Tải hướng dẫn Vibe Onboarding cho quyền Guest.")
                resp = requests.get("https://vnstocks.com/files/vibe-onboarding.md", timeout=10)
                if resp.status_code == 200:
                    instruction_content = resp.text
                else:
                    instruction_content = _FALLBACK_INSTRUCTION
            except Exception as e:
                logger.debug(f"Không thể tải nội dung hướng dẫn từ website: {e}")
                instruction_content = _FALLBACK_INSTRUCTION
        import re
        if instruction_content:
            yaml_match = re.search(r'^---\n(.*?)\n---\n*', instruction_content, flags=re.DOTALL)
            if yaml_match:
                yaml_content = yaml_match.group(1).strip()
                yaml_inline = " | ".join([line.strip() for line in yaml_content.split('\n') if line.strip() and not line.startswith('description:')])
                html_anchor = f"<!-- vnai-bootstrap | {yaml_inline} -->\n"
                instruction_content = instruction_content[yaml_match.end():]
                instruction_content = html_anchor + instruction_content
            elif not instruction_content.startswith("<!-- vnai-bootstrap"):
                instruction_content = "<!-- vnai-bootstrap | auto-generated -->\n" + instruction_content
        targets = [
            (name, target_path(name, project_root))
            for name in AGENT_TARGET_ORDER
            if name in enabled_targets
        ]
        success = False
        for target_name, target in targets:
            try:
                if not target.parent.exists():
                    try:
                        target.parent.mkdir(parents=True, exist_ok=True)
                    except Exception:
                        continue
                if not target.exists():
                    with open(target, "w", encoding="utf-8") as f:
                        f.write(instruction_content)
                    logger.debug(f"Đã tạo file chỉ dẫn mới tại: {target}")
                    success = True
                    continue
                with open(target, "r", encoding="utf-8") as f:
                    content = f.read()
                if content.strip().startswith("{") and content.strip().endswith("}"):
                    logger.debug(f"File {target} có vẻ là JSON. Bỏ qua để tránh làm hỏng config.")
                    continue
                import re
                pattern = _BOOTSTRAP_BLOCK_PATTERN
                matches = re.findall(pattern, content)
                if len(matches) > 1:
                    logger.debug(f"Phát hiện nội dung bị lặp trong {target}, tiến hành dọn dẹp...")
                    cleaned_content = re.sub(pattern, '', content).strip()
                    block_to_append = instruction_content.strip()
                    final_content = cleaned_content + ("\n\n" if cleaned_content else "") + block_to_append
                    final_content = re.sub(r'\n{3,}', '\n\n', final_content)
                    with open(target, "w", encoding="utf-8") as f:
                        f.write(final_content + "\n")
                    success = True
                    continue
                elif len(matches) == 1:
                    if matches[0].strip() != instruction_content.strip() and not matches[0].strip().endswith(instruction_content.strip()):
                        logger.debug(f"Cập nhật nội dung mới cho {target}...")
                        cleaned_content = re.sub(pattern, '', content).strip()
                        final_content = cleaned_content + ("\n\n" if cleaned_content else "") + instruction_content.strip()
                        final_content = re.sub(r'\n{3,}', '\n\n', final_content)
                        with open(target, "w", encoding="utf-8") as f:
                            f.write(final_content + "\n")
                    else:
                        logger.debug(f"Rule Vnstock đã tồn tại và hợp lệ trong {target}. Bỏ qua.")
                    success = True
                    continue
                markers = [
                    "# Vnstock Ecosystem Guidelines",
                    "# Vnstock Vibe Onboarding",
                    "# Vnstock AI Agent"
                ]
                if any(marker in content for marker in markers):
                    logger.debug(f"Rule Vnstock phiên bản cũ đã tồn tại trong {target}. Bỏ qua.")
                    success = True
                    continue
                with open(target, "a", encoding="utf-8") as f:
                    if not content.endswith("\n"):
                        f.write("\n")
                    f.write("\n")
                    f.write(instruction_content)
                logger.debug(f"Đã thêm rule Vnstock Dynamic Skill Router vào cuối {target}")
                success = True
            except Exception as e:
                logger.debug(f"Không thể ghi rule vào {target}: {e}")
        return success
    except Exception as e:
        logger.error(f"Lỗi khi setup agent environment: {e}")
        return False

def async_setup_agent_environment(project_root: str = ".") -> None:
    thread = threading.Thread(
        target=setup_agent_environment,
        args=(project_root,),
        daemon=True,
        name="AgentEnvironmentSetupThread"
    )
    thread.start()