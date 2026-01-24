from pathlib import Path
import json
import platform
import os
from typing import Dict, Any

class CppProjectConfig:
    def __init__(self, config_path: Path = None):
        self.config_path = config_path or Path.cwd() / "cpp.proj"
        self.project_root = self.config_path.parent
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        if not self.config_path.exists():
            return self._default_config()
        try:
            with open(self.config_path, encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    print(f"[WARNING] {self.config_path} is empty, using default config")
                    return self._default_config()
                return json.loads(content)
        except json.JSONDecodeError as e:
            print(f"[ERROR] Invalid JSON in {self.config_path}: {e}")
            print("[INFO] Using default configuration")
            return self._default_config()

    def _default_config(self) -> Dict[str, Any]:
        project_name = self.project_root.name if self.project_root else "MyProject"
        return {
            "project": project_name,
            "version": "1.0.0",
            "include": "/include",
            "plugins": "/plugins",
            "compiler": {
                "standard": "c++17",
                "optimization": "O3",
                "flags": ["-Wall", "-pthread"]
            },
            "types": {
                "common": ["int", "float", "double", "string"]
            },
            "threading": {
                "enabled": True,
                "max_workers": 8
            },
            "intellisense": {
                "enabled": True,
                "extract_signatures": True,
                "include_docs": True
            }
        }

    @staticmethod
    def create_default(path: str):
        config = CppProjectConfig()._default_config()
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)

        Path("include").mkdir(exist_ok=True)
        Path("plugins").mkdir(exist_ok=True)

    def _get_appdata_path(self) -> Path:
        if platform.system() == "Windows":
            base = Path(os.getenv('APPDATA', Path.home() / 'AppData' / 'Roaming'))
        else:
            base = Path.home() / ".local" / "share" / "includecpp"
        return base

    def get_build_dir(self, compiler: str) -> Path:
        project_name = self.config.get('project', 'unnamed')
        build_dir_name = f"{project_name}-{compiler}-build-proj"
        build_dir = self._get_appdata_path() / build_dir_name
        build_dir.mkdir(parents=True, exist_ok=True)
        return build_dir

    def update_base_dir(self, base_dir: Path):
        self.config['BaseDir'] = str(base_dir)
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2)

    def resolve_path(self, path: str) -> Path:
        r"""Resolve path relative to project root.

        Paths like '/plugins' or '/include' are treated as relative to project_root.
        True absolute paths like '/home/user/...' or 'C:\...' are kept absolute.
        """
        path_obj = Path(path)

        # Simple heuristic: If path starts with '/' but has only one component (like /plugins),
        # treat as project-relative. Multi-component paths like /home/user/... are absolute.
        if path.startswith('/'):
            stripped = path.lstrip('/')

            # Single component like "plugins" or "include" -> project-relative
            if '/' not in stripped:
                return (self.project_root / stripped).resolve()

            # Multi-component like "home/user/project" -> check if it's truly absolute
            # On Linux, /home/user/... is absolute. On Windows in config, it shouldn't happen.
            # If the absolute path exists, use it. Otherwise treat as project-relative.
            if path_obj.exists():
                return path_obj
            else:
                # Doesn't exist as absolute, treat as project-relative
                return (self.project_root / stripped).resolve()

        # Windows absolute paths (has drive letter like C:\)
        if path_obj.is_absolute() and path_obj.drive:
            return path_obj

        # Relative path (no leading slash)
        return (self.project_root / path).resolve()

    @property
    def include_dir(self) -> Path:
        return self.resolve_path(self.config['include'])

    @property
    def plugins_dir(self) -> Path:
        return self.resolve_path(self.config['plugins'])

    @property
    def base_dir(self) -> Path:
        if 'BaseDir' in self.config:
            return Path(self.config['BaseDir'])
        return self.get_build_dir('gcc')
