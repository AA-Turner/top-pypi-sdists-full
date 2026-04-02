import os
import fnmatch
from pathlib import Path

from seshat.general.exceptions import InvalidJobIgnore

DEFAULT_JOBIGNORE_PATTERNS = [
    "**/__pycache__",
    "__pycache__/",
    "*.py[cod]",
    ".venv",
    ".idea",
    ".vscode",
    ".Python",
    "build/",
    "dist/",
]


class JobIgnoreHandler:
    def __init__(self, ignore_file: str | Path = None):
        self.ignore_file = ignore_file
        self.ignore_patterns = list(DEFAULT_JOBIGNORE_PATTERNS)
        if self.ignore_file:
            self.ignore_patterns += self.read_job_ignore()

    def read_job_ignore(self) -> list[str]:
        """Read and parse .jobignore file, handling special characters and comments."""
        if not os.path.exists(self.ignore_file):
            raise FileNotFoundError(".jobignore file not found")
        if not os.path.isfile(self.ignore_file):
            raise IsADirectoryError("The provided .jobignore is not a file")

        try:
            with open(self.ignore_file, "r") as f:
                patterns = []
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        line = line.encode().decode("unicode_escape")
                        patterns.append(line)
                return patterns
        except Exception as e:
            raise InvalidJobIgnore(f"Error reading .jobignore: {str(e)}")

    def match_gitignore_like_path(self, path: str) -> bool:
        """Check if a path matches any .gitignore-style pattern, supporting negations."""
        if not path:
            return False

        normalized = path.replace("\\", "/").lstrip("/")
        path_components = normalized.split("/")
        result = False

        for pattern in self.ignore_patterns:
            if not pattern:
                continue

            is_negation = pattern.startswith("!")
            if is_negation:
                pattern = pattern[1:]
                if not pattern:
                    continue

            if pattern.startswith("#"):
                if len(pattern) > 1 and pattern[1] != "*":
                    continue
                if pattern == "#*":
                    if len(path_components) == 1 and path_components[0].startswith("#"):
                        result = True
                    continue
                pattern = pattern.lstrip("#")

            if pattern.startswith("\\#"):
                pattern = pattern[1:]

            is_root_only = pattern.startswith("/")
            is_dir_pattern = pattern.endswith("/")
            pat = pattern.rstrip("/").replace("\\", "/").lstrip("/")

            if not pat:
                continue

            pat_components = pat.split("/")
            match = False

            if is_root_only and len(path_components) > 1:
                continue

            if len(pat_components) == 1:
                for i, component in enumerate(path_components):
                    if fnmatch.fnmatch(component, pat):
                        if is_dir_pattern:
                            if i < len(path_components) - 1 or normalized.endswith("/"):
                                match = True
                                break
                        else:
                            match = True
                            break

            else:
                if len(pat_components) > len(path_components):
                    continue

                match = True
                for i, pc in enumerate(pat_components):
                    if pc == "**":
                        continue
                    if i >= len(path_components):
                        match = False
                        break
                    if not fnmatch.fnmatch(path_components[i], pc):
                        match = False
                        break

                if (
                    match
                    and "**" not in pat
                    and len(pat_components) != len(path_components)
                ):
                    match = False

                if match and is_dir_pattern:
                    if not (
                        len(path_components) > len(pat_components)
                        or normalized.endswith("/")
                    ):
                        match = False

            if not match and "**" in pat:
                base_path = (
                    "/".join(path_components[:-1]) if len(path_components) > 1 else ""
                )
                file_name = path_components[-1]

                if fnmatch.fnmatch(file_name, pat.replace("**", "*")):
                    match = True
                elif base_path and fnmatch.fnmatch(normalized, pat.replace("**", "*")):
                    match = True

            if not match and not is_dir_pattern and normalized.endswith("/"):
                if fnmatch.fnmatch(normalized.rstrip("/"), pat):
                    match = True

            if is_negation:
                if match:
                    result = False
            elif match:
                result = True

        return result
