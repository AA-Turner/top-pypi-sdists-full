"""
Workspace Manager - 파일 시스템 관리
Cursor/OpenCode 스타일 파일 트리 및 편집
"""
import os
import json
from pathlib import Path
from typing import List, Dict, Any, Optional


class WorkspaceManager:
    """작업 공간 파일 관리"""

    def __init__(self, root_path: Optional[str] = None):
        if root_path:
            self.root = Path(root_path).resolve()
        else:
            self.root = Path.cwd()

        if not self.root.exists():
            self.root.mkdir(parents=True, exist_ok=True)

    def get_current_workspace(self) -> str:
        """현재 작업 공간 경로"""
        return str(self.root)

    def get_file_tree(self, max_depth: int = 5) -> List[Dict[str, Any]]:
        """파일 트리 구조 반환"""
        def build_tree(path: Path, depth: int = 0) -> Dict[str, Any]:
            if depth > max_depth:
                return None

            item = {
                "name": path.name,
                "path": str(path.relative_to(self.root)),
                "type": "directory" if path.is_dir() else "file",
            }

            if path.is_file():
                item["size"] = path.stat().st_size
                item["extension"] = path.suffix

            if path.is_dir():
                children = []
                try:
                    for child in sorted(path.iterdir()):
                        # 숨김 파일 및 특정 디렉토리 제외
                        if child.name.startswith('.') or child.name in ['node_modules', '__pycache__', 'venv']:
                            continue

                        child_tree = build_tree(child, depth + 1)
                        if child_tree:
                            children.append(child_tree)

                    item["children"] = children
                except PermissionError:
                    pass

            return item

        return [build_tree(self.root)]

    def read_file(self, relative_path: str) -> str:
        """파일 읽기"""
        file_path = self.root / relative_path
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {relative_path}")

        if not file_path.is_file():
            raise IsADirectoryError(f"Not a file: {relative_path}")

        # 안전성 체크: root 밖으로 나가는지 확인
        if not str(file_path.resolve()).startswith(str(self.root)):
            raise PermissionError("Access denied")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            # 바이너리 파일
            return "[Binary file]"

    def write_file(self, relative_path: str, content: str):
        """파일 쓰기"""
        file_path = self.root / relative_path

        # 안전성 체크
        if not str(file_path.resolve()).startswith(str(self.root)):
            raise PermissionError("Access denied")

        # 디렉토리 생성
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def create_file(self, relative_path: str, content: str = ""):
        """빈 파일 생성"""
        self.write_file(relative_path, content)

    def create_directory(self, relative_path: str):
        """디렉토리 생성"""
        dir_path = self.root / relative_path

        if not str(dir_path.resolve()).startswith(str(self.root)):
            raise PermissionError("Access denied")

        dir_path.mkdir(parents=True, exist_ok=True)

    def delete_file(self, relative_path: str):
        """파일 삭제"""
        file_path = self.root / relative_path

        if not str(file_path.resolve()).startswith(str(self.root)):
            raise PermissionError("Access denied")

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {relative_path}")

        if file_path.is_dir():
            import shutil
            shutil.rmtree(file_path)
        else:
            file_path.unlink()

    def rename_file(self, old_path: str, new_path: str):
        """파일 이름 변경"""
        old_file = self.root / old_path
        new_file = self.root / new_path

        # 안전성 체크
        if not str(old_file.resolve()).startswith(str(self.root)):
            raise PermissionError("Access denied")
        if not str(new_file.resolve()).startswith(str(self.root)):
            raise PermissionError("Access denied")

        if not old_file.exists():
            raise FileNotFoundError(f"File not found: {old_path}")

        # 새 경로의 디렉토리 생성
        new_file.parent.mkdir(parents=True, exist_ok=True)

        old_file.rename(new_file)

    def search_files(self, query: str, extensions: Optional[List[str]] = None) -> List[str]:
        """파일 검색"""
        results = []

        for path in self.root.rglob("*"):
            # 숨김 파일 제외
            if any(part.startswith('.') for part in path.parts):
                continue

            # 특정 디렉토리 제외
            if any(exc in path.parts for exc in ['node_modules', '__pycache__', 'venv']):
                continue

            if path.is_file():
                # 확장자 필터
                if extensions and path.suffix not in extensions:
                    continue

                # 파일명 또는 내용 검색
                if query.lower() in path.name.lower():
                    results.append(str(path.relative_to(self.root)))

        return results
