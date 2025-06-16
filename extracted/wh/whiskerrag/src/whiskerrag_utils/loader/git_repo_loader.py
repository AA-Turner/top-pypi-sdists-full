import logging
import os
import shutil
import subprocess
import tempfile
from typing import Any, Dict, List, Optional, Tuple, Union
from urllib.parse import urlparse

from langchain_text_splitters import Language
from openai import BaseModel

from whiskerrag_types.interface.loader_interface import BaseLoader
from whiskerrag_types.model.knowledge import (
    Knowledge,
    KnowledgeSourceEnum,
    KnowledgeTypeEnum,
)
from whiskerrag_types.model.knowledge_source import GithubRepoSourceConfig
from whiskerrag_types.model.multi_modal import Text
from whiskerrag_types.model.splitter import (
    BaseCodeSplitConfig,
    BaseSplitConfig,
    JSONSplitConfig,
    MarkdownSplitConfig,
    PDFSplitConfig,
    TextSplitConfig,
)
from whiskerrag_utils.loader.file_pattern_manager import FilePatternManager
from whiskerrag_utils.registry import RegisterTypeEnum, register

logger = logging.getLogger(__name__)


class GitFileElementType(BaseModel):
    content: str
    path: str
    mode: str
    url: str
    branch: str
    repo_name: str
    size: int
    sha: str
    position: dict = {}  # VSCode position information


def _check_git_installation() -> bool:
    """check git installation"""
    try:
        subprocess.run(["git", "--version"], check=True, capture_output=True, text=True)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False


def _get_temp_git_env() -> Dict[str, str]:
    """
    get temporary git environment configuration

    Returns:
        Dict[str, str]: git config
    """
    return {
        "GIT_AUTHOR_NAME": "temp",
        "GIT_AUTHOR_EMAIL": "temp@example.com",
        "GIT_COMMITTER_NAME": "temp",
        "GIT_COMMITTER_EMAIL": "temp@example.com",
        "GIT_TERMINAL_PROMPT": "0",  # disable interactive prompt
    }


def _lazy_import_git() -> Tuple[Any, Any, Any]:
    """Lazy import git modules to avoid direct dependency"""
    try:
        from git import Repo
        from git.exc import GitCommandNotFound, InvalidGitRepositoryError

        return Repo, GitCommandNotFound, InvalidGitRepositoryError
    except ImportError as e:
        raise ImportError(
            "GitPython is required for Git repository loading. "
            "Please install it with: pip install GitPython"
        ) from e


@register(RegisterTypeEnum.KNOWLEDGE_LOADER, KnowledgeSourceEnum.GITHUB_REPO)
class GithubRepoLoader(BaseLoader):
    repo_name: str
    branch_name: Optional[str] = None
    token: Optional[str] = None
    local_repo: Optional[Any] = (
        None  # Use Any instead of object to avoid mypy attr-defined errors
    )
    knowledge: Knowledge

    @property
    def repos_dir(self) -> str:
        """get runtime root folder path"""
        # use system tempdir instead of current dir
        return os.path.join(tempfile.gettempdir(), "repo_download")

    def __init__(
        self,
        knowledge: Knowledge,
    ):
        """
        init GithubRepoLoader

        Args:
            knowledge: Knowledge instance,which include repo source config

        Raises:
            ValueError: invalid repo config
        """
        if not isinstance(knowledge.source_config, GithubRepoSourceConfig):
            raise ValueError("source_config should be GithubRepoSourceConfig")

        self.knowledge = knowledge
        self.repo_name = knowledge.source_config.repo_name
        self.branch_name = knowledge.source_config.branch
        self.token = knowledge.source_config.auth_info
        self.base_url = knowledge.source_config.url.rstrip("/")

        os.makedirs(self.repos_dir, exist_ok=True)

        self.repo_path: Optional[str] = os.path.join(
            self.repos_dir, self.repo_name.replace("/", "_")
        )

        try:
            self._load_repo()
        except Exception as e:
            logger.error(f"Failed to load repo: {e}")
            raise ValueError(
                f"Failed to load repo {self.repo_name} with branch "
                f"{self.branch_name}. Error: {str(e)}"
            )

    def _load_repo(self) -> None:
        Repo, GitCommandNotFound, InvalidGitRepositoryError = _lazy_import_git()

        if not _check_git_installation():
            raise ValueError("Git is not installed in the system")

        if not self.repo_path:
            raise ValueError("Repository path not initialized")

        try:
            parsed_url = urlparse(self.base_url)
            if not parsed_url.scheme or parsed_url.scheme != "https":
                raise ValueError(
                    f"Invalid URL scheme: {self.base_url}. "
                    "Only HTTPS URLs are supported"
                )

            clone_url = f"{self.base_url}/{self.repo_name}.git"

            git_env = _get_temp_git_env()

            if self.token:
                git_env.update(
                    {
                        "GIT_ASKPASS": "echo",
                        "GIT_USERNAME": "git",
                        "GIT_PASSWORD": self.token,
                    }
                )

            if os.path.exists(self.repo_path):
                try:
                    self.local_repo = Repo(self.repo_path)
                    self._update_repo()
                except Exception as e:
                    logger.warning(f"Failed to update existing repo: {e}")
                    shutil.rmtree(self.repo_path)
                    self._clone_repo(clone_url, git_env)
            else:
                self._clone_repo(clone_url, git_env)

            if not self.branch_name and self.local_repo:
                try:
                    self.branch_name = self.local_repo.active_branch.name
                except Exception as e:
                    logger.warning(f"Failed to get default branch name: {str(e)}")
                    self.branch_name = "main"

            logger.info(f"Successfully loaded repository at {self.repo_path}")

        except Exception as e:
            raise ValueError(
                f"Failed to load repo {self.repo_name} with branch "
                f"{self.branch_name}. Error: {str(e)}"
            )

    def _clone_repo(self, clone_url: str, git_env: Dict[str, str]) -> None:
        Repo, GitCommandNotFound, InvalidGitRepositoryError = _lazy_import_git()

        if not self.repo_path:
            raise ValueError("Repository path not initialized")

        try:
            if self.branch_name:
                self.local_repo = Repo.clone_from(
                    url=clone_url,
                    to_path=self.repo_path,
                    depth=1,
                    single_branch=True,
                    env=git_env,
                    branch=self.branch_name,
                )
            else:
                self.local_repo = Repo.clone_from(
                    url=clone_url,
                    to_path=self.repo_path,
                    depth=1,
                    single_branch=True,
                    env=git_env,
                )
        except GitCommandNotFound:
            raise ValueError("Git command not found. Please ensure git is installed.")
        except InvalidGitRepositoryError as e:
            raise ValueError(f"Invalid git repository: {str(e)}")
        except Exception as e:
            if "Authentication failed" in str(e):
                raise ValueError("Authentication failed. Please check your token.")
            raise

    def _update_repo(self) -> None:
        # Ensure git is available before proceeding
        if not _check_git_installation():
            raise ValueError("Git is not installed in the system")

        if not self.local_repo:
            raise ValueError("Repository not initialized")

        if self.branch_name:
            self.local_repo.git.checkout(self.branch_name)
        self.local_repo.remotes.origin.pull()

    @staticmethod
    def get_knowledge_type_by_ext(ext: str) -> KnowledgeTypeEnum:
        ext = ext.lower()
        ext_to_type = {
            ".md": KnowledgeTypeEnum.MARKDOWN,
            ".mdx": KnowledgeTypeEnum.MARKDOWN,
            ".txt": KnowledgeTypeEnum.TEXT,
            ".json": KnowledgeTypeEnum.JSON,
            ".pdf": KnowledgeTypeEnum.PDF,
            ".docx": KnowledgeTypeEnum.DOCX,
            ".rst": KnowledgeTypeEnum.RST,
            ".py": KnowledgeTypeEnum.PYTHON,
            ".js": KnowledgeTypeEnum.JS,
            ".ts": KnowledgeTypeEnum.TS,
            ".go": KnowledgeTypeEnum.GO,
            ".java": KnowledgeTypeEnum.JAVA,
            ".cpp": KnowledgeTypeEnum.CPP,
            ".c": KnowledgeTypeEnum.C,
            ".h": KnowledgeTypeEnum.C,
            ".hpp": KnowledgeTypeEnum.CPP,
            ".cs": KnowledgeTypeEnum.CSHARP,
            ".kt": KnowledgeTypeEnum.KOTLIN,
            ".swift": KnowledgeTypeEnum.SWIFT,
            ".php": KnowledgeTypeEnum.PHP,
            ".rb": KnowledgeTypeEnum.RUBY,
            ".rs": KnowledgeTypeEnum.RUST,
            ".scala": KnowledgeTypeEnum.SCALA,
            ".sol": KnowledgeTypeEnum.SOL,
            ".html": KnowledgeTypeEnum.HTML,
            ".css": KnowledgeTypeEnum.TEXT,
            ".lua": KnowledgeTypeEnum.LUA,
            ".m": KnowledgeTypeEnum.TEXT,  # Objective-C/MATLAB等
            ".sh": KnowledgeTypeEnum.TEXT,
            ".yml": KnowledgeTypeEnum.TEXT,
            ".yaml": KnowledgeTypeEnum.TEXT,
            ".tex": KnowledgeTypeEnum.LATEX,
            ".jpg": KnowledgeTypeEnum.IMAGE,
            ".jpeg": KnowledgeTypeEnum.IMAGE,
            ".png": KnowledgeTypeEnum.IMAGE,
            ".gif": KnowledgeTypeEnum.IMAGE,
            ".bmp": KnowledgeTypeEnum.IMAGE,
            ".svg": KnowledgeTypeEnum.IMAGE,
        }
        return ext_to_type.get(ext, KnowledgeTypeEnum.TEXT)

    def _get_split_config_for_knowledge_type(
        self, knowledge_type: KnowledgeTypeEnum
    ) -> Union[
        MarkdownSplitConfig,
        JSONSplitConfig,
        PDFSplitConfig,
        BaseCodeSplitConfig,
        TextSplitConfig,
        BaseSplitConfig,
    ]:
        """
        Generate appropriate split_config based on knowledge type

        Args:
            knowledge_type: The type of knowledge

        Returns:
            Appropriate split configuration for the knowledge type
        """
        # Use default chunk_size and chunk_overlap from GithubRepoParseConfig
        default_chunk_size = 1500
        default_chunk_overlap = 200

        if knowledge_type == KnowledgeTypeEnum.MARKDOWN:
            return MarkdownSplitConfig(
                chunk_size=default_chunk_size,
                chunk_overlap=default_chunk_overlap,
                separators=[
                    "\n#{1,6} ",
                    "```\n",
                    "\n\\*\\*\\*+\n",
                    "\n---+\n",
                    "\n___+\n",
                    "\n\n",
                    "\n",
                    " ",
                    "",
                ],
                is_separator_regex=True,
                keep_separator="start",
                extract_header_first=True,
            )
        elif knowledge_type == KnowledgeTypeEnum.JSON:
            return JSONSplitConfig(
                max_chunk_size=default_chunk_size,
                min_chunk_size=min(200, default_chunk_size - 200),
            )
        elif knowledge_type == KnowledgeTypeEnum.PDF:
            return PDFSplitConfig(
                chunk_size=default_chunk_size,
                chunk_overlap=default_chunk_overlap,
                extract_images=False,
                table_extract_mode="text",
            )
        elif knowledge_type in [
            KnowledgeTypeEnum.PYTHON,
            KnowledgeTypeEnum.JS,
            KnowledgeTypeEnum.TS,
            KnowledgeTypeEnum.GO,
            KnowledgeTypeEnum.JAVA,
            KnowledgeTypeEnum.CPP,
            KnowledgeTypeEnum.C,
            KnowledgeTypeEnum.CSHARP,
            KnowledgeTypeEnum.KOTLIN,
            KnowledgeTypeEnum.SWIFT,
            KnowledgeTypeEnum.PHP,
            KnowledgeTypeEnum.RUBY,
            KnowledgeTypeEnum.RUST,
            KnowledgeTypeEnum.SCALA,
            KnowledgeTypeEnum.SOL,
            KnowledgeTypeEnum.LUA,
        ]:
            # Map knowledge types to Language enum
            language_map = {
                KnowledgeTypeEnum.PYTHON: Language.PYTHON,
                KnowledgeTypeEnum.JS: Language.JS,
                KnowledgeTypeEnum.TS: Language.TS,
                KnowledgeTypeEnum.GO: Language.GO,
                KnowledgeTypeEnum.JAVA: Language.JAVA,
                KnowledgeTypeEnum.CPP: Language.CPP,
                KnowledgeTypeEnum.C: Language.C,
                KnowledgeTypeEnum.CSHARP: Language.CSHARP,
                KnowledgeTypeEnum.KOTLIN: Language.KOTLIN,
                KnowledgeTypeEnum.SWIFT: Language.SWIFT,
                KnowledgeTypeEnum.PHP: Language.PHP,
                KnowledgeTypeEnum.RUBY: Language.RUBY,
                KnowledgeTypeEnum.RUST: Language.RUST,
                KnowledgeTypeEnum.SCALA: Language.SCALA,
                KnowledgeTypeEnum.SOL: Language.SOL,
                KnowledgeTypeEnum.LUA: Language.LUA,
            }
            return BaseCodeSplitConfig(
                language=language_map.get(knowledge_type, Language.MARKDOWN),
                chunk_size=default_chunk_size,
                chunk_overlap=default_chunk_overlap,
            )
        elif knowledge_type == KnowledgeTypeEnum.TEXT:
            return TextSplitConfig(
                chunk_size=default_chunk_size,
                chunk_overlap=default_chunk_overlap,
                separators=["\n\n", "\n", " ", ""],
                is_separator_regex=False,
                keep_separator=False,
            )
        else:
            # For other types (HTML, RST, LATEX, etc.), use BaseSplitConfig
            return BaseSplitConfig(
                chunk_size=default_chunk_size,
                chunk_overlap=default_chunk_overlap,
            )

    def _get_file_position_info(self, file_path: str, relative_path: str) -> dict:
        """
        Get position information that can be used for URL construction and remote jumping

        Args:
            file_path: Full path to the file
            relative_path: Relative path from repo root

        Returns:
            dict: Position information for remote repository jumping
        """
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
                total_lines = len(lines)

            return {
                "file_path": relative_path,
                "start_line": 1,
                "end_line": total_lines,
                "total_lines": total_lines,
            }
        except Exception as e:
            logger.warning(
                f"Could not read file for position info {relative_path}: {e}"
            )
            return {
                "file_path": relative_path,
                "start_line": 1,
                "end_line": None,
                "total_lines": None,
            }

    def generate_jump_url(
        self,
        relative_path: str,
        line: Optional[int] = None,
        end_line: Optional[int] = None,
    ) -> str:
        """
        Generate a jump URL for external systems to create clickable links

        Args:
            relative_path: Relative path to the file
            line: Optional line number to jump to
            end_line: Optional end line for range jumping

        Returns:
            str: Complete URL that can be used for jumping to the file/line
        """
        base_url = (
            f"{self.base_url}/{self.repo_name}/blob/{self.branch_name}/{relative_path}"
        )

        if line is not None:
            if end_line is not None and end_line != line:
                return f"{base_url}#L{line}-L{end_line}"
            else:
                return f"{base_url}#L{line}"
        return base_url

    async def decompose(self) -> List[Knowledge]:
        """
        decompose knowledge units in the repository

        Returns:
            List[Knowledge]: knowledge list

        Raises:
            ValueError: when the repository is not properly initialized
        """
        if not self.local_repo or not self.repo_path:
            raise ValueError("Repository not properly initialized")

        # Ensure git is available before proceeding with git operations
        if not _check_git_installation():
            raise ValueError("Git is not installed in the system")

        # count the total file size of the repo
        total_size = 0
        for root, _, files in os.walk(self.repo_path):
            if ".git" in root:
                continue
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    total_size += os.path.getsize(file_path)
                except Exception:
                    continue

        # initialize file pattern manager
        split_config = getattr(self.knowledge, "split_config", None)
        if split_config and getattr(split_config, "type", None) == "github_repo":
            pattern_manager = FilePatternManager(
                config=split_config, repo_path=self.repo_path
            )
            warnings = pattern_manager.validate_patterns()
            if warnings:
                logger.warning(
                    "Pattern configuration warnings:\n" + "\n".join(warnings)
                )
        else:
            # create a compatible configuration dictionary
            dummy_config = {
                "include_patterns": ["*.md", "*.mdx"],
                "ignore_patterns": [],
                "no_gitignore": True,
                "no_default_ignore_patterns": False,
            }
            pattern_manager = FilePatternManager(
                config=dummy_config, repo_path=self.repo_path
            )

        current_commit = self.local_repo.head.commit

        github_repo_list: List[Knowledge] = []

        for root, _, files in os.walk(self.repo_path):
            if ".git" in root:
                continue

            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, self.repo_path)

                if not pattern_manager.should_include_file(relative_path):
                    continue

                try:
                    file_size = os.path.getsize(file_path)
                    git_file_path = relative_path.replace("\\", "/")
                    blob = current_commit.tree / git_file_path
                    file_sha = blob.hexsha
                    ext = os.path.splitext(relative_path)[1].lower()
                    knowledge_type = self.get_knowledge_type_by_ext(ext)
                    file_url = (
                        f"{self.base_url}/{self.repo_name}/blob/"
                        f"{self.branch_name}/{relative_path}"
                    )
                    # Generate appropriate split_config for this knowledge type
                    knowledge_split_config = self._get_split_config_for_knowledge_type(
                        knowledge_type
                    )
                    # Get accurate position information
                    position_info = self._get_file_position_info(
                        file_path, relative_path
                    )

                    knowledge = Knowledge(
                        source_type=KnowledgeSourceEnum.GITHUB_FILE,
                        knowledge_type=knowledge_type,
                        knowledge_name=f"{self.repo_name}/{relative_path}",
                        embedding_model_name=self.knowledge.embedding_model_name,
                        source_config={
                            **self.knowledge.source_config.model_dump(),
                            "path": relative_path,
                        },
                        tenant_id=self.knowledge.tenant_id,
                        file_size=file_size,
                        file_sha=file_sha,
                        space_id=self.knowledge.space_id,
                        split_config=knowledge_split_config,
                        parent_id=self.knowledge.knowledge_id,
                        enabled=True,
                        metadata={
                            "_reference_url": file_url,
                            "branch": self.branch_name,
                            "repo_name": self.repo_name,
                            "path": relative_path,
                            # Position information for remote jumping
                            "position": position_info,
                        },
                    )
                    github_repo_list.append(knowledge)

                except Exception as e:
                    logger.warning(f"Error processing file {relative_path}: {e}")
                    continue

        return github_repo_list

    async def load(self) -> List[Text]:
        """
        返回项目的文件目录树结构信息和作者信息，便于大模型理解
        """
        if not self.repo_path:
            raise ValueError("Repository not properly initialized")

        def build_tree(path: str, prefix: str = "") -> str:
            entries = sorted(os.listdir(path))
            tree_lines = []
            for idx, entry in enumerate(entries):
                full_path = os.path.join(path, entry)
                connector = "└── " if idx == len(entries) - 1 else "├── "
                tree_lines.append(f"{prefix}{connector}{entry}")
                if os.path.isdir(full_path) and entry != ".git":
                    extension = "    " if idx == len(entries) - 1 else "│   "
                    tree_lines.append(build_tree(full_path, prefix + extension))
            return "\n".join(tree_lines)

        root_name = os.path.basename(self.repo_path.rstrip(os.sep))
        tree_str = (
            f"repo: {root_name}\n" + "project tree: " + build_tree(self.repo_path)
        )

        try:
            if not self.local_repo:
                raise ValueError("Repository not initialized")

            # Ensure git is available before accessing git objects
            if not _check_git_installation():
                raise ValueError("Git is not installed in the system")

            first_commit = next(
                self.local_repo.iter_commits(
                    rev=self.branch_name, max_count=1, reverse=True
                )
            )
            author_name = first_commit.author.name
            author_email = first_commit.author.email
        except Exception:
            author_name = None
            author_email = None

        return [
            Text(
                content=tree_str,
                metadata={
                    **self.knowledge.metadata,
                    "repo_name": self.repo_name,
                    "author_name": author_name,
                    "author_email": author_email,
                },
            )
        ]

    async def on_load_finished(self) -> None:
        """clean resource"""
        try:
            if self.repo_path and os.path.exists(self.repo_path):
                shutil.rmtree(self.repo_path)
                self.repo_path = None
                self.local_repo = None
                logger.info(f"Cleaned up temporary directory for {self.repo_name}")
        except Exception as e:
            logger.error(f"Error cleaning up resources: {e}")

    async def get_file_by_path(self, path: str) -> GitFileElementType:
        if not self.local_repo:
            raise ValueError("Repository not initialized")

        if not self.repo_path:
            raise ValueError("Repository path not initialized")

        # Ensure git is available before accessing git objects
        if not _check_git_installation():
            raise ValueError("Git is not installed in the system")

        full_path = os.path.join(self.repo_path, path)
        if not os.path.exists(full_path):
            raise ValueError(f"File not found: {path}")

        try:
            blob = self.local_repo.head.commit.tree[path]
            # type check to ensure source_config is GithubRepoSourceConfig
            if not isinstance(self.knowledge.source_config, GithubRepoSourceConfig):
                raise ValueError("Invalid source config type")
            base_url = self.knowledge.source_config.url.rstrip("/")
            file_url = f"{base_url}/{self.repo_name}/blob/{self.branch_name}/{path}"

            # read file content
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except UnicodeDecodeError:
                # if not a text file, try binary reading and convert to base64
                with open(full_path, "rb") as f:
                    import base64

                    content = base64.b64encode(f.read()).decode("utf-8")

            return GitFileElementType(
                content=content,
                path=path,
                mode=blob.mode_str,
                url=file_url,
                branch=self.branch_name or "main",
                repo_name=self.repo_name,
                size=blob.size,
                sha=blob.hexsha,
            )
        except Exception as e:
            logger.error(f"Error getting file info: {e}")
            raise ValueError(f"Failed to get file info for {path}: {str(e)}")
