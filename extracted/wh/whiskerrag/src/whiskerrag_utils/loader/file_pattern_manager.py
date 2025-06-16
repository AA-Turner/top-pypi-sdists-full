import fnmatch
import os
import re
from functools import lru_cache
from pathlib import Path, PurePath
from typing import List, Optional, Set


class FilePatternManager:
    """文件模式匹配管理器"""

    DEFAULT_IGNORE_PATTERNS = [
        "*.pyc",
        "__pycache__/*",
        ".git/*",
        ".github/*",
        ".gitignore",
        ".DS_Store",
        "*.swp",
        "*.log",
        "node_modules/*",
        "*.class",
        "*.jar",
        "*.war",
        "*.ear",
        "*.zip",
        "*.tar.gz",
        "*.rar",
    ]

    def __init__(self, config: dict, repo_path: Optional[str] = None):
        """
        初始化文件模式匹配管理器
        Args:
            config: GithubRepoParseConfig 配置实例
            repo_path: 仓库本地路径
        """
        self.include_patterns = self._normalize_patterns(
            getattr(config, "include_patterns", []) or []
        )
        self.ignore_patterns = self._normalize_patterns(
            getattr(config, "ignore_patterns", []) or []
        )
        self.use_gitignore = getattr(config, "use_gitignore", True)
        self.use_default_patterns = getattr(config, "use_default_ignore", True)
        self.repo_path = repo_path
        self.gitignore_patterns: Set[str] = set()

        # 添加默认忽略模式（最低优先级）
        if self.use_default_patterns:
            self._default_ignore_patterns = self._normalize_patterns(
                self.DEFAULT_IGNORE_PATTERNS
            )
        else:
            self._default_ignore_patterns = []

        # 加载 .gitignore 模式（次低优先级）
        if self.use_gitignore and repo_path:
            self._load_gitignore(repo_path)

    def _normalize_patterns(self, patterns: List[str]) -> List[str]:
        """标准化模式字符串"""
        normalized = []
        for pattern in patterns:
            if not pattern or not isinstance(pattern, str):
                continue
            pattern = pattern.strip()
            if not pattern:
                continue
            pattern = pattern.replace("\\", "/")
            pattern = re.sub(r"^\.?/?", "", pattern)
            normalized.append(pattern)
        return normalized

    def _load_gitignore(self, repo_path: str) -> None:
        """加载 .gitignore 文件中的模式"""
        gitignore_path = Path(repo_path) / ".gitignore"
        if gitignore_path.exists():
            with open(gitignore_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        self.gitignore_patterns.add(self._normalize_patterns([line])[0])

    @lru_cache(maxsize=1024)
    def should_include_file(self, file_path: str) -> bool:
        """
        VSCode/gitignore风格的文件包含/忽略判断：
        1. ignore_patterns（最高优先级，命中即排除）
        2. .gitignore（命中即排除）
        3. include_patterns（命中即包含）
        4. default_ignore_patterns
        """
        file_path = str(Path(file_path)).replace("\\", "/")
        basename = os.path.basename(file_path)

        def expand_patterns(patterns: List[str]) -> List[str]:
            expanded = []
            for pat in patterns:
                expanded.append(pat)
                # VSCode/gitignore风格：*.md 匹配所有子目录下的.md
                if pat.startswith("*.") and not pat.startswith("**/"):
                    expanded.append(f"**/{pat}")
            return expanded

        def matches(path: str, pattern: str) -> bool:
            # pathlib.PurePath.match 支持 **/*.md 递归
            return PurePath(path).match(pattern)

        # 1. ignore_patterns 优先级最高
        for pattern in expand_patterns(self.ignore_patterns):
            if matches(file_path, pattern) or matches(basename, pattern):
                return False
        # 2. .gitignore
        if self.use_gitignore:
            for pattern in expand_patterns(list(self.gitignore_patterns)):
                if matches(file_path, pattern) or matches(basename, pattern):
                    return False
        # 3. include_patterns 命中即包含
        if self.include_patterns:
            for pattern in expand_patterns(self.include_patterns):
                if matches(file_path, pattern) or matches(basename, pattern):
                    return True
            return False
        # 4. default_ignore_patterns
        if self.use_default_patterns:
            for pattern in expand_patterns(self._default_ignore_patterns):
                if matches(file_path, pattern) or matches(basename, pattern):
                    return False
        return True

    def validate_patterns(self) -> List[str]:
        """
        验证模式配置，返回警告信息

        Returns:
            List[str]: 警告信息列表
        """
        warnings = []

        # 检查包含模式
        if self.include_patterns:
            # 检查可能过于宽泛的包含模式
            broad_patterns = [
                p for p in self.include_patterns if p == "*" or p == "**/*"
            ]
            if broad_patterns:
                warnings.append(
                    f"Broad include patterns found: {broad_patterns}. "
                    "This might include unwanted files."
                )

        # 检查忽略模式是否有效
        if self.include_patterns and self.ignore_patterns:
            for ignore_pattern in self.ignore_patterns:
                # 检查是否有忽略模式会覆盖所有包含模式
                if all(
                    self._pattern_matches_all(ignore_pattern, include_pattern)
                    for include_pattern in self.include_patterns
                ):
                    warnings.append(
                        f"Ignore pattern '{ignore_pattern}' might override "
                        f"all include patterns: {self.include_patterns}"
                    )

        return warnings

    def _pattern_matches_all(self, pattern1: str, pattern2: str) -> bool:
        """检查 pattern1 是否完全覆盖 pattern2"""
        regex1 = fnmatch.translate(pattern1)
        regex2 = fnmatch.translate(pattern2)

        # 生成测试字符串
        test_str = re.sub(r"\\\*|\\\?|\\\[.*?\\\]", "a", regex2)
        return bool(re.match(regex1, test_str))
