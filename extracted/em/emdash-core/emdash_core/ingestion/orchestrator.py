"""Orchestrates the complete ingestion pipeline."""

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Callable, Optional

from tqdm import tqdm

from ..core.config import get_config
from ..core.models import CodebaseEntities, FileEntities, GitData
from ..graph.connection import get_connection, write_lock_context
from ..graph.builder import GraphBuilder
from ..graph.schema import SchemaManager
from .repository import RepositoryManager
from .parsers.registry import ParserRegistry
from .parsers.base_parser import BaseLanguageParser
from .git.commit_analyzer import CommitAnalyzer
from .github.pr_fetcher import PRFetcher
from .github.task_extractor import TaskExtractor
from .change_detector import ChangeDetector, ChangedFiles
from ..graph.writer import GraphWriter
from ..utils.logger import log


def _parse_file_worker(file_path: Path, repo_root: Path) -> FileEntities:
    """Worker function for parallel file parsing.

    Args:
        file_path: Path to source file
        repo_root: Repository root path

    Returns:
        FileEntities
    """
    # Get parser from registry
    parser_class = ParserRegistry.get_parser(file_path)

    if parser_class is None:
        log.warning(f"No parser available for {file_path.suffix}")
        return FileEntities()

    try:
        parser = parser_class(file_path, repo_root)
        return parser.parse()
    except Exception as e:
        log.warning(f"Failed to parse {file_path}: {e}")
        return FileEntities()


class IngestionOrchestrator:
    """Coordinates the full ingestion pipeline."""

    def __init__(self):
        """Initialize orchestrator."""
        self.config = get_config()
        self.repo_manager = RepositoryManager()
        self.connection = get_connection()
        self.graph_builder = GraphBuilder(
            self.connection,
            batch_size=self.config.ingestion.batch_size
        )

    def index(
        self,
        repo_path: str,
        incremental: bool = False,
        changed_only: bool = False,
        skip_git: Optional[bool] = None,
        pr_limit: int = 100,
        progress_callback: Optional[Callable[[str, float], None]] = None,
    ):
        """Execute the full indexing pipeline.

        Args:
            repo_path: URL or local path to repository
            incremental: Whether to perform incremental update (legacy)
            changed_only: Only index files changed since last index (uses git diff)
            skip_git: Whether to skip git history analysis (and GitHub analysis).
                      Defaults to config.ingestion.ast_only (AST_ONLY env var).
            pr_limit: Maximum number of PRs to fetch per state (open/merged)
            progress_callback: Optional callback(step: str, percent: float) for progress

        Raises:
            Various exceptions if indexing fails
        """
        # Use config ast_only as default if skip_git not explicitly set
        if skip_git is None:
            skip_git = self.config.ingestion.ast_only

        # Store callback for use in parsing
        self._progress_callback = progress_callback

        # Acquire write lock for the entire indexing operation
        with write_lock_context("indexing", timeout=120):
            return self._run_index(repo_path, incremental, changed_only, skip_git, pr_limit)

    def _run_index(
        self,
        repo_path: str,
        incremental: bool,
        changed_only: bool,
        skip_git: bool,
        pr_limit: int,
    ):
        """Internal indexing implementation (called with write lock held)."""
        log.info(f"Starting indexing: {repo_path}")
        if changed_only:
            log.info("Incremental mode: only indexing changed files")
        if skip_git:
            log.info("AST_ONLY mode: skipping Layer B (git) and Layer C (analytics)")

        # Ensure Kuzu connection and schema
        self._ensure_database_ready()

        # Step 1: Get or clone repository
        log.info("Step 1: Fetching repository...")
        repo, repo_entity = self.repo_manager.get_or_clone(
            repo_path,
            skip_commit_count=skip_git
        )

        # For incremental indexing, detect changes
        changed_files: Optional[ChangedFiles] = None
        current_commit = None
        if changed_only:
            last_indexed_commit = self._get_last_indexed_commit(repo_entity.url)
            current_commit = repo.head.commit.hexsha

            if not last_indexed_commit:
                log.info("No previous index found - performing full index")
                changed_only = False
            elif last_indexed_commit == current_commit:
                log.info("No changes since last index - nothing to do")
                return {"files": 0, "functions": 0, "classes": 0, "modules": 0, "commits": 0, "authors": 0, "prs": 0, "message": "No changes since last index"}
            else:
                extensions = ParserRegistry.get_all_extensions()
                detector = ChangeDetector(repo, last_indexed_commit)
                changed_files = detector.get_changed_files(extensions)

                if not changed_files:
                    log.info("No relevant file changes detected - nothing to do")
                    return {"files": 0, "functions": 0, "classes": 0, "modules": 0, "commits": 0, "authors": 0, "prs": 0, "message": "No relevant file changes"}

                log.info(f"Changes detected: {changed_files.total_changes} files")

        # Step 2: Parse codebase (Layer A)
        if changed_only and changed_files:
            log.info("Step 2: Parsing changed files (Layer A)...")

            # Delete removed files from graph first
            if changed_files.deleted:
                deleted_paths = [str(p) for p in changed_files.deleted]
                self.graph_builder.delete_files(deleted_paths)

            # Parse only added and modified files
            entities = self._parse_codebase(repo, file_filter=changed_files.all_to_index)
        else:
            log.info("Step 2: Indexing codebase (Layer A)...")
            entities = self._parse_codebase(repo)

        # Step 3: Extract git history (Layer B)
        if skip_git:
            log.info("Step 3: Skipping git history (code-only mode)")
            git_data = GitData(repository=repo_entity)
        else:
            log.info("Step 3: Analyzing git history (Layer B)...")
            git_data = self._analyze_git_history(repo, repo_entity)

        # Step 4: Build graph
        log.info("Step 4: Building graph...")
        self.graph_builder.build_code_graph(entities)
        if not skip_git:
            self.graph_builder.build_git_graph(git_data)

        # Step 5: Fetch PRs from GitHub (if token available and not skipped)
        prs = []
        tasks = []
        if not skip_git and self.config.github.is_available and repo_entity.owner and pr_limit > 0:
            log.info(f"Step 5: Fetching pull requests from GitHub (limit: {pr_limit} per state)...")
            prs, tasks = self._fetch_pull_requests(repo_entity, pr_limit=pr_limit)
        else:
            if skip_git:
                log.info("Step 5: Skipping GitHub layer (code-only mode)")
            elif not self.config.github.is_available:
                log.info("Step 5: Skipping PR fetch (no GitHub token)")
            elif pr_limit == 0:
                log.info("Step 5: Skipping PR fetch (pr_limit=0)")
            else:
                log.info("Step 5: Skipping PR fetch (not a GitHub repo)")

        # Step 6: Update repository metadata
        log.info("Step 6: Updating repository metadata...")
        self._update_repository_metadata(
            repo_entity,
            len(entities.files),
            last_indexed_commit=current_commit or repo.head.commit.hexsha
        )

        log.info("✓ Indexing complete!")
        self._print_summary(entities, git_data, prs)

        # Return stats for API response
        return {
            "files": len(entities.files),
            "functions": len(entities.functions),
            "classes": len(entities.classes),
            "modules": len(entities.modules),
            "commits": len(git_data.commits) if git_data else 0,
            "authors": len(git_data.authors) if git_data else 0,
            "prs": len(prs) if prs else 0,
        }

    def _ensure_database_ready(self):
        """Ensure database connection and schema are ready."""
        log.info("Connecting to Kuzu and ensuring schema...")

        self.connection.connect()

        # Initialize schema if needed
        schema_manager = SchemaManager(self.connection)

        # Check if schema exists (check for tables)
        try:
            result = self.connection.execute("CALL show_tables()")
            if not result:
                log.info("Schema not found, initializing...")
                schema_manager.initialize_schema()
        except Exception:
            # If we can't check tables, try to initialize anyway
            schema_manager.initialize_schema()

    def _get_last_indexed_commit(self, repo_url: str) -> Optional[str]:
        """Get the commit SHA from the last successful index.

        Args:
            repo_url: Repository URL

        Returns:
            Commit SHA or None if not found
        """
        try:
            result = self.connection.execute(
                "MATCH (r:Repository {url: $url}) RETURN r.last_indexed_commit",
                {"url": repo_url}
            )
            if result and result.has_next():
                row = result.get_next()
                return row[0] if row[0] else None
            return None
        except Exception as e:
            log.debug(f"Could not get last indexed commit: {e}")
            return None

    def _parse_codebase(
        self,
        repo,
        file_filter: Optional[list[Path]] = None
    ) -> CodebaseEntities:
        """Parse source files in the repository.

        Args:
            repo: Git repository
            file_filter: Optional list of specific files to parse (for incremental mode)

        Returns:
            CodebaseEntities
        """
        repo_root = Path(repo.working_dir)

        # Use file filter if provided (incremental mode)
        if file_filter is not None:
            source_files = [f for f in file_filter if f.exists()]
            if not source_files:
                log.info("No files to parse (all filtered files may have been deleted)")
                return CodebaseEntities()
        else:
            # Get all supported extensions from registry
            extensions = ParserRegistry.get_all_extensions()

            if not extensions:
                log.warning("No parsers registered")
                return CodebaseEntities()

            # Get source files (multi-language)
            source_files = self.repo_manager.get_source_files(
                repo,
                extensions,
                self.config.ingestion.ignore_patterns
            )

            if not source_files:
                log.warning(f"No source files found (supported: {', '.join(extensions)})")
                return CodebaseEntities()

        log.info(f"Parsing {len(source_files)} source files...")

        # Parse files (with optional parallelization)
        if self.config.ingestion.max_workers > 1:
            entities = self._parse_files_parallel(source_files, repo_root)
        else:
            entities = self._parse_files_sequential(source_files, repo_root)

        log.info(f"Extracted: {len(entities.files)} files, {len(entities.classes)} classes, "
                f"{len(entities.functions)} functions")

        return entities

    def _parse_single_file(self, file_path: Path, repo_root: Path) -> FileEntities:
        """Parse a single file using appropriate parser.

        Args:
            file_path: Path to source file
            repo_root: Repository root path

        Returns:
            FileEntities
        """
        # Get parser from registry
        parser_class = ParserRegistry.get_parser(file_path)

        if parser_class is None:
            log.warning(f"No parser available for {file_path.suffix}")
            return FileEntities()

        try:
            parser = parser_class(file_path, repo_root)
            return parser.parse()
        except Exception as e:
            log.warning(f"Failed to parse {file_path}: {e}")
            return FileEntities()

    def _parse_files_sequential(
        self,
        source_files: list[Path],
        repo_root: Path
    ) -> CodebaseEntities:
        """Parse files sequentially with progress bar.

        Args:
            source_files: List of source files to parse
            repo_root: Repository root path

        Returns:
            CodebaseEntities
        """
        results = []
        total = len(source_files)
        last_reported_percent = 0

        for i, file_path in enumerate(tqdm(source_files, desc="Parsing", unit="file")):
            file_entities = self._parse_single_file(file_path, repo_root)
            results.append(file_entities)

            # Report progress every 10%
            if total > 0 and hasattr(self, '_progress_callback') and self._progress_callback:
                current_percent = int((i + 1) / total * 100)
                # Report at 10% intervals (10, 20, 30, etc.)
                if current_percent >= last_reported_percent + 10:
                    last_reported_percent = (current_percent // 10) * 10
                    # Map parsing progress (0-100) to overall progress (10-70)
                    overall_percent = 10 + (last_reported_percent * 0.6)
                    self._progress_callback("Parsing files", overall_percent)

        return CodebaseEntities.merge(results)

    def _parse_files_parallel(
        self,
        source_files: list[Path],
        repo_root: Path
    ) -> CodebaseEntities:
        """Parse files in parallel with progress bar.

        Args:
            source_files: List of source files to parse
            repo_root: Repository root path

        Returns:
            CodebaseEntities
        """
        results = []
        total = len(source_files)
        last_reported_percent = 0
        completed = 0

        with ThreadPoolExecutor(max_workers=self.config.ingestion.max_workers) as executor:
            # Submit all tasks
            futures = {
                executor.submit(_parse_file_worker, file_path, repo_root): file_path
                for file_path in source_files
            }

            # Process results with progress bar
            for future in tqdm(
                as_completed(futures),
                total=len(futures),
                desc="Parsing",
                unit="file"
            ):
                try:
                    file_entities = future.result()
                    results.append(file_entities)
                except Exception as e:
                    file_path = futures[future]
                    log.warning(f"Failed to parse {file_path}: {e}")

                # Report progress every 10%
                completed += 1
                if total > 0 and hasattr(self, '_progress_callback') and self._progress_callback:
                    current_percent = int(completed / total * 100)
                    if current_percent >= last_reported_percent + 10:
                        last_reported_percent = (current_percent // 10) * 10
                        overall_percent = 10 + (last_reported_percent * 0.6)
                        self._progress_callback("Parsing files", overall_percent)

        return CodebaseEntities.merge(results)

    def _analyze_git_history(self, repo, repo_entity):
        """Analyze Git commit history.

        Args:
            repo: Git repository
            repo_entity: Repository entity

        Returns:
            GitData
        """
        analyzer = CommitAnalyzer(repo, max_commits=self.config.ingestion.git_depth)
        return analyzer.analyze(repo_entity)

    def _update_repository_metadata(
        self,
        repo_entity,
        file_count: int,
        last_indexed_commit: Optional[str] = None
    ):
        """Update repository metadata in the graph.

        Args:
            repo_entity: Repository entity
            file_count: Number of files processed
            last_indexed_commit: Commit SHA at time of indexing
        """
        from datetime import datetime

        query = """
        MERGE (r:Repository {url: $url})
        SET r.name = $name,
            r.owner = $owner,
            r.default_branch = $default_branch,
            r.last_ingested = timestamp($last_ingested),
            r.last_indexed_commit = $last_indexed_commit,
            r.ingestion_status = 'completed',
            r.commit_count = $commit_count,
            r.file_count = $file_count,
            r.primary_language = 'Python'
        """

        self.connection.execute_write(
            query,
            {
                "url": repo_entity.url,
                "name": repo_entity.name,
                "owner": repo_entity.owner,
                "default_branch": repo_entity.default_branch,
                "last_ingested": datetime.now().isoformat(),
                "last_indexed_commit": last_indexed_commit,
                "commit_count": repo_entity.commit_count,
                "file_count": file_count,
            }
        )

    def _fetch_pull_requests(self, repo_entity, pr_limit: int = 100):
        """Fetch pull requests from GitHub.

        Args:
            repo_entity: Repository entity with owner and name
            pr_limit: Maximum PRs to fetch per state (open/merged)

        Returns:
            Tuple of (list[PullRequestEntity], list[TaskEntity])
        """
        try:
            # Initialize fetcher and get PRs
            fetcher = PRFetcher(
                owner=repo_entity.owner,
                repo=repo_entity.name,
                token=self.config.github.token
            )

            # Fetch open and merged PRs separately with the limit
            open_prs = fetcher.fetch_prs(state="open", limit=pr_limit)
            merged_prs = fetcher.fetch_prs(state="merged", limit=pr_limit)
            prs = open_prs + merged_prs
            log.info(f"Fetched {len(open_prs)} open + {len(merged_prs)} merged PRs")

            if not prs:
                log.info("No pull requests found")
                return [], []

            # Extract tasks from PR descriptions
            extractor = TaskExtractor()
            all_tasks = []
            for pr in prs:
                tasks = extractor.extract_tasks(pr)
                all_tasks.extend(tasks)

            if all_tasks:
                log.info(f"Extracted {len(all_tasks)} tasks from PR descriptions")

            # Write to graph using connection directly
            writer = GraphWriter(self.connection)
            writer.write_pull_requests(prs)
            writer.write_tasks(all_tasks)

            # Link PRs to commits and files
            for pr in prs:
                if pr.commit_shas:
                    writer.write_pr_commit_links(pr.number, pr.commit_shas)
                if pr.files_changed:
                    writer.write_pr_file_links(pr.number, pr.files_changed)

            return prs, all_tasks

        except Exception as e:
            log.warning(f"Failed to fetch pull requests: {e}")
            return [], []

    def _print_summary(self, entities: CodebaseEntities, git_data, prs=None):
        """Print indexing summary.

        Args:
            entities: Codebase entities
            git_data: Git data
            prs: Optional list of pull requests
        """
        log.info("\n" + "=" * 60)
        log.info("INDEXING SUMMARY")
        log.info("=" * 60)
        log.info(f"Files:     {len(entities.files)}")
        log.info(f"Classes:   {len(entities.classes)}")
        log.info(f"Functions: {len(entities.functions)}")
        log.info(f"Modules:   {len(entities.modules)}")
        log.info(f"Commits:   {len(git_data.commits)}")
        log.info(f"Authors:   {len(git_data.authors)}")
        if prs:
            log.info(f"PRs:       {len(prs)}")
        else:
            log.info("PRs:       0 (GitHub layer skipped)")
        log.info("=" * 60)
