"""Path discovery module for finding C++ modules in specific directories."""

import os
from pathlib import Path
from typing import List, Set


class PathDiscovery:
    """Discover C++ modules (.cp files) in specific paths."""

    def __init__(self, project_root: Path, config):
        self.project_root = project_root
        self.config = config
        self.plugins_dir = config.resolve_path(config.config.get('plugins', '/plugins'))

    def discover_modules_in_path(self, search_path: Path) -> List[str]:
        """Discover module names from .cp files in given path.

        Args:
            search_path: Directory or file path to search

        Returns:
            List of module names (without .cp extension)
        """
        modules = []

        if not search_path.is_absolute():
            search_path = (self.project_root / search_path).resolve()

        if search_path.is_file():
            if search_path.suffix == '.cp':
                module_name = search_path.stem
                modules.append(module_name)
            return modules

        if search_path.is_dir():
            for cp_file in search_path.glob('*.cp'):
                module_name = cp_file.stem
                modules.append(module_name)

            cpp_files = list(search_path.glob('*.cpp'))
            h_files = list(search_path.glob('*.h'))

            for cpp_file in cpp_files:
                potential_cp = self.plugins_dir / f"{cpp_file.stem}.cp"
                if potential_cp.exists() and cpp_file.stem not in modules:
                    modules.append(cpp_file.stem)

            for h_file in h_files:
                potential_cp = self.plugins_dir / f"{h_file.stem}.cp"
                if potential_cp.exists() and h_file.stem not in modules:
                    modules.append(h_file.stem)

        return modules

    def find_cp_files_in_paths(self, paths: List[Path]) -> Set[Path]:
        """Find all .cp files in given paths.

        Args:
            paths: List of directories or files to search

        Returns:
            Set of .cp file paths
        """
        cp_files = set()

        for path in paths:
            if not path.is_absolute():
                path = (self.project_root / path).resolve()

            if path.is_file() and path.suffix == '.cp':
                cp_files.add(path)
            elif path.is_dir():
                for cp_file in path.glob('*.cp'):
                    cp_files.add(cp_file)

        return cp_files
