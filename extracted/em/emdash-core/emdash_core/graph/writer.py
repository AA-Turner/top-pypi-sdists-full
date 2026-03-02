"""Batch write operations for Kuzu graph construction."""

from typing import List
from datetime import datetime

# Lazy import for kuzu - it's an optional dependency
try:
    import kuzu
    KUZU_AVAILABLE = True
except ImportError:
    kuzu = None  # type: ignore
    KUZU_AVAILABLE = False

from ..core.models import (
    FileEntity,
    ClassEntity,
    FunctionEntity,
    ModuleEntity,
    ImportStatement,
    CommitEntity,
    AuthorEntity,
    FileModification,
    PullRequestEntity,
    TaskEntity,
)
from .connection import KuzuConnection
from ..utils.logger import log


class GraphWriter:
    """Handles batch writes to Kuzu database."""

    def __init__(self, connection: KuzuConnection, batch_size: int = 1000):
        """Initialize graph writer.

        Args:
            connection: Kuzu connection
            batch_size: Number of entities to write per batch
        """
        self.connection = connection
        self.batch_size = batch_size

    def _batch_iter(self, items: list):
        """Yield batches of items.

        Args:
            items: List of items to batch

        Yields:
            Batches of items
        """
        for i in range(0, len(items), self.batch_size):
            yield items[i:i + self.batch_size]

    def write_files(self, files: List[FileEntity]):
        """Write file nodes to the graph (batched).

        Args:
            files: List of FileEntity objects
        """
        if not files:
            return
        log.info(f"Writing {len(files)} file nodes...")

        for batch in self._batch_iter(files):
            rows = []
            for file in batch:
                file_dict = self._entity_to_dict(file)
                rows.append({
                    'path': str(file_dict['path']),
                    'name': str(file_dict['name']),
                    'extension': file_dict.get('extension'),
                    'size_bytes': int(file_dict.get('size_bytes') or 0),
                    'lines_of_code': int(file_dict.get('lines_of_code') or 0),
                    'hash': file_dict.get('hash'),
                    'last_modified': file_dict.get('last_modified'),
                })
            try:
                self.connection.execute_write("""
                    UNWIND $rows AS row
                    MERGE (f:File {path: row.path})
                    SET f.name = row.name,
                        f.extension = row.extension,
                        f.size_bytes = row.size_bytes,
                        f.lines_of_code = row.lines_of_code,
                        f.hash = row.hash
                """, {"rows": rows})
            except Exception as e:
                log.warning(f"Failed to write file batch: {e}")

        log.info(f"Wrote {len(files)} file nodes")

    def write_classes(self, classes: List[ClassEntity]):
        """Write class nodes and CONTAINS relationships (batched).

        Args:
            classes: List of ClassEntity objects
        """
        if not classes:
            return
        log.info(f"Writing {len(classes)} class nodes...")

        for batch in self._batch_iter(classes):
            rows = []
            for cls in batch:
                cls_dict = self._entity_to_dict(cls)
                rows.append({
                    'qualified_name': str(cls_dict['qualified_name']),
                    'name': str(cls_dict['name']),
                    'file_path': str(cls_dict['file_path']),
                    'line_start': int(cls_dict['line_start']),
                    'line_end': int(cls_dict['line_end']),
                    'docstring': cls_dict.get('docstring'),
                    'is_abstract': bool(cls_dict.get('is_abstract', False)),
                    'decorators': list(cls_dict.get('decorators') or []),
                    'base_classes': list(cls_dict.get('base_classes') or []),
                    'attributes': list(cls_dict.get('attributes') or []),
                    'methods': list(cls_dict.get('methods') or []),
                })
            try:
                # Batch create class nodes
                self.connection.execute_write("""
                    UNWIND $rows AS row
                    MERGE (c:Class {qualified_name: row.qualified_name})
                    SET c.name = row.name,
                        c.file_path = row.file_path,
                        c.line_start = row.line_start,
                        c.line_end = row.line_end,
                        c.docstring = row.docstring,
                        c.is_abstract = row.is_abstract,
                        c.decorators = row.decorators,
                        c.base_classes = row.base_classes,
                        c.attributes = row.attributes,
                        c.methods = row.methods
                """, {"rows": rows})

                # Batch create CONTAINS_CLASS relationships
                self.connection.execute_write("""
                    UNWIND $rows AS row
                    MATCH (f:File {path: row.file_path})
                    MATCH (c:Class {qualified_name: row.qualified_name})
                    MERGE (f)-[:CONTAINS_CLASS {line_start: row.line_start}]->(c)
                """, {"rows": rows})
            except Exception as e:
                log.warning(f"Failed to write class batch: {e}")

        log.info(f"Wrote {len(classes)} class nodes")

    def write_functions(self, functions: List[FunctionEntity]):
        """Write function nodes and relationships (batched).

        Args:
            functions: List of FunctionEntity objects
        """
        if not functions:
            return
        log.info(f"Writing {len(functions)} function nodes...")

        for batch in self._batch_iter(functions):
            rows = []
            method_rows = []
            for func in batch:
                func_dict = self._entity_to_dict(func)
                row = {
                    'qualified_name': str(func_dict['qualified_name']),
                    'name': str(func_dict['name']),
                    'file_path': str(func_dict['file_path']),
                    'line_start': int(func_dict['line_start']),
                    'line_end': int(func_dict['line_end']),
                    'docstring': func_dict.get('docstring'),
                    'parameters': list(func_dict.get('parameters') or []),
                    'return_annotation': func_dict.get('return_annotation'),
                    'is_async': bool(func_dict.get('is_async', False)),
                    'is_method': bool(func_dict.get('is_method', False)),
                    'is_static': bool(func_dict.get('is_static', False)),
                    'is_classmethod': bool(func_dict.get('is_classmethod', False)),
                    'decorators': list(func_dict.get('decorators') or []),
                    'cyclomatic_complexity': int(func_dict.get('cyclomatic_complexity') or 1),
                    'calls': list(func_dict.get('calls') or []),
                }
                rows.append(row)

                # Collect method relationships
                if func.is_method:
                    parts = func.qualified_name.rsplit('.', 1)
                    if len(parts) > 1:
                        method_rows.append({
                            'class_name': parts[0],
                            'func_name': func.qualified_name,
                        })

            try:
                # Batch create function nodes
                self.connection.execute_write("""
                    UNWIND $rows AS row
                    MERGE (f:Function {qualified_name: row.qualified_name})
                    SET f.name = row.name,
                        f.file_path = row.file_path,
                        f.line_start = row.line_start,
                        f.line_end = row.line_end,
                        f.docstring = row.docstring,
                        f.parameters = row.parameters,
                        f.return_annotation = row.return_annotation,
                        f.is_async = row.is_async,
                        f.is_method = row.is_method,
                        f.is_static = row.is_static,
                        f.is_classmethod = row.is_classmethod,
                        f.decorators = row.decorators,
                        f.cyclomatic_complexity = row.cyclomatic_complexity,
                        f.calls = row.calls
                """, {"rows": rows})

                # Batch create CONTAINS_FUNCTION relationships
                self.connection.execute_write("""
                    UNWIND $rows AS row
                    MATCH (file:File {path: row.file_path})
                    MATCH (f:Function {qualified_name: row.qualified_name})
                    MERGE (file)-[:CONTAINS_FUNCTION {line_start: row.line_start}]->(f)
                """, {"rows": rows})

                # Batch create HAS_METHOD relationships
                if method_rows:
                    self.connection.execute_write("""
                        UNWIND $rows AS row
                        MATCH (c:Class {qualified_name: row.class_name})
                        MATCH (f:Function {qualified_name: row.func_name})
                        MERGE (c)-[:HAS_METHOD]->(f)
                    """, {"rows": method_rows})
            except Exception as e:
                log.warning(f"Failed to write function batch: {e}")

        log.info(f"Wrote {len(functions)} function nodes")

    def write_inheritance(self, classes: List[ClassEntity]):
        """Write inheritance relationships between classes (batched).

        Args:
            classes: List of ClassEntity objects
        """
        # Collect all inheritance pairs
        rows = []
        for cls in classes:
            if not cls.base_classes:
                continue
            for base_name in cls.base_classes:
                rows.append({
                    'child_name': cls.qualified_name,
                    'base_name': base_name,
                })

        if not rows:
            log.info("No inheritance relationships to write")
            return

        log.info(f"Writing {len(rows)} inheritance relationships...")

        for batch in self._batch_iter(rows):
            try:
                self.connection.execute_write("""
                    UNWIND $rows AS row
                    MATCH (child:Class {qualified_name: row.child_name})
                    MATCH (parent:Class)
                    WHERE parent.qualified_name = row.base_name OR parent.name = row.base_name
                    MERGE (child)-[:INHERITS_FROM]->(parent)
                """, {"rows": batch})
            except Exception as e:
                log.warning(f"Failed to write inheritance batch: {e}")

        log.info(f"Wrote {len(rows)} inheritance relationships")

    def write_calls(self, functions: List[FunctionEntity]):
        """Write CALLS relationships between functions (batched).

        Args:
            functions: List of FunctionEntity objects
        """
        # Collect all call pairs
        rows = []
        for func in functions:
            if not func.calls:
                continue
            for called_name in func.calls:
                rows.append({
                    'caller_name': func.qualified_name,
                    'called_name': called_name,
                })

        if not rows:
            log.info("No call relationships to write")
            return

        log.info(f"Writing {len(rows)} call relationships...")

        for batch in self._batch_iter(rows):
            try:
                self.connection.execute_write("""
                    UNWIND $rows AS row
                    MATCH (caller:Function {qualified_name: row.caller_name})
                    MATCH (callee:Function)
                    WHERE callee.qualified_name = row.called_name OR callee.name = row.called_name
                    MERGE (caller)-[:CALLS]->(callee)
                """, {"rows": batch})
            except Exception as e:
                log.warning(f"Failed to write calls batch: {e}")

        log.info(f"Wrote {len(rows)} call relationships")

    def write_modules(self, modules: List[ModuleEntity]):
        """Write module nodes (batched).

        Args:
            modules: List of ModuleEntity objects
        """
        if not modules:
            return
        log.info(f"Writing {len(modules)} module nodes...")

        for batch in self._batch_iter(modules):
            rows = []
            for mod in batch:
                mod_dict = self._entity_to_dict(mod)
                rows.append({
                    'name': str(mod_dict['name']),
                    'import_path': mod_dict.get('import_path'),
                    'is_external': bool(mod_dict.get('is_external', False)),
                    'package': mod_dict.get('package'),
                })
            try:
                self.connection.execute_write("""
                    UNWIND $rows AS row
                    MERGE (m:Module {name: row.name})
                    SET m.import_path = row.import_path,
                        m.is_external = row.is_external,
                        m.package = row.package
                """, {"rows": rows})
            except Exception as e:
                log.warning(f"Failed to write module batch: {e}")

        log.info(f"Wrote {len(modules)} module nodes")

    def write_imports(self, imports: List[ImportStatement]):
        """Write IMPORTS relationships from files to modules (batched).

        Args:
            imports: List of ImportStatement objects
        """
        if not imports:
            return
        log.info(f"Writing {len(imports)} import relationships...")

        for batch in self._batch_iter(imports):
            rows = []
            for imp in batch:
                imp_dict = self._entity_to_dict(imp)
                rows.append({
                    'file_path': str(imp_dict['file_path']),
                    'module': str(imp_dict['module']),
                    'import_type': imp_dict.get('import_type', 'import'),
                    'line_number': int(imp_dict.get('line_number') or 0),
                    'alias': imp_dict.get('alias'),
                })
            try:
                self.connection.execute_write("""
                    UNWIND $rows AS row
                    MATCH (f:File {path: row.file_path})
                    MATCH (m:Module {name: row.module})
                    MERGE (f)-[:IMPORTS {
                        import_type: row.import_type,
                        line_number: row.line_number,
                        alias: row.alias
                    }]->(m)
                """, {"rows": rows})
            except Exception as e:
                log.warning(f"Failed to write imports batch: {e}")

        log.info(f"Wrote {len(imports)} import relationships")

    def write_commits(self, commits: List[CommitEntity]):
        """Write commit nodes.

        Args:
            commits: List of CommitEntity objects
        """
        log.info(f"Writing {len(commits)} commit nodes...")

        for commit in commits:
            commit_dict = self._entity_to_dict(commit)
            try:
                self.connection.execute_write("""
                    MERGE (c:Commit {sha: $sha})
                    SET c.message = $message,
                        c.timestamp = timestamp($timestamp),
                        c.author_name = $author_name,
                        c.author_email = $author_email,
                        c.committer_name = $committer_name,
                        c.committer_email = $committer_email,
                        c.insertions = $insertions,
                        c.deletions = $deletions,
                        c.files_changed = $files_changed,
                        c.is_merge = $is_merge,
                        c.parent_shas = $parent_shas
                """, commit_dict)
            except Exception as e:
                log.warning(f"Failed to write commit {commit.sha}: {e}")

        log.info(f"Wrote {len(commits)} commit nodes")

    def write_authors(self, authors: List[AuthorEntity]):
        """Write author nodes.

        Args:
            authors: List of AuthorEntity objects
        """
        log.info(f"Writing {len(authors)} author nodes...")

        for author in authors:
            author_dict = self._entity_to_dict(author)
            try:
                self.connection.execute_write("""
                    MERGE (a:Author {email: $email})
                    SET a.name = $name,
                        a.first_commit = timestamp($first_commit),
                        a.last_commit = timestamp($last_commit),
                        a.total_commits = $total_commits,
                        a.total_lines_added = $total_lines_added,
                        a.total_lines_deleted = $total_lines_deleted
                """, author_dict)
            except Exception as e:
                log.warning(f"Failed to write author {author.email}: {e}")

        log.info(f"Wrote {len(authors)} author nodes")

    def write_file_modifications(self, modifications: List[FileModification]):
        """Write file modification relationships.

        Args:
            modifications: List of FileModification objects
        """
        log.info(f"Writing {len(modifications)} file modifications...")

        count = 0

        for mod in modifications:
            mod_dict = self._entity_to_dict(mod)
            try:
                self.connection.execute_write("""
                    MATCH (c:Commit {sha: $commit_sha})
                    MATCH (f:File {path: $file_path})
                    MERGE (c)-[:COMMIT_MODIFIES {
                        change_type: $change_type,
                        insertions: $insertions,
                        deletions: $deletions,
                        old_path: $old_path
                    }]->(f)
                """, mod_dict)
                count += 1
            except Exception as e:
                log.debug(f"Could not create modification: {mod.commit_sha} -> {mod.file_path}: {e}")

        log.info(f"Wrote {count} file modification relationships")

    def write_commit_authorship(self, commits: List[CommitEntity]):
        """Write AUTHORED_BY relationships from commits to authors.

        Args:
            commits: List of CommitEntity objects
        """
        log.info("Writing commit authorship relationships...")

        count = 0

        for commit in commits:
            try:
                self.connection.execute_write("""
                    MATCH (c:Commit {sha: $sha})
                    MATCH (a:Author {email: $author_email})
                    MERGE (c)-[:AUTHORED_BY]->(a)
                """, {"sha": commit.sha, "author_email": commit.author_email})
                count += 1
            except Exception as e:
                log.debug(f"Could not create authorship: {commit.sha} -> {commit.author_email}: {e}")

        log.info(f"Wrote {count} authorship relationships")

    def write_pull_requests(self, prs: List[PullRequestEntity]):
        """Write pull request nodes.

        Args:
            prs: List of PullRequestEntity objects
        """
        log.info(f"Writing {len(prs)} pull request nodes...")

        for pr in prs:
            pr_dict = self._entity_to_dict(pr)
            try:
                # Handle nullable timestamps
                created_at = pr_dict.get('created_at')
                merged_at = pr_dict.get('merged_at')

                self.connection.execute_write("""
                    MERGE (p:PullRequest {number: $number})
                    SET p.title = $title,
                        p.description = $description,
                        p.state = $state,
                        p.author = $author,
                        p.reviewers = $reviewers,
                        p.labels = $labels,
                        p.additions = $additions,
                        p.deletions = $deletions,
                        p.files_changed = $files_changed,
                        p.base_branch = $base_branch,
                        p.head_branch = $head_branch,
                        p.embedding = $embedding
                """, pr_dict)

                # Set timestamps separately if not null
                if created_at:
                    self.connection.execute_write("""
                        MATCH (p:PullRequest {number: $number})
                        SET p.created_at = timestamp($created_at)
                    """, {"number": pr.number, "created_at": created_at})

                if merged_at:
                    self.connection.execute_write("""
                        MATCH (p:PullRequest {number: $number})
                        SET p.merged_at = timestamp($merged_at)
                    """, {"number": pr.number, "merged_at": merged_at})

            except Exception as e:
                log.warning(f"Failed to write PR {pr.number}: {e}")

        log.info(f"Wrote {len(prs)} pull request nodes")

    def write_pr_commit_links(self, prs: List[PullRequestEntity]):
        """Write relationships from PRs to their commits.

        Args:
            prs: List of PullRequestEntity objects with commit_shas
        """
        log.info("Writing PR-Commit relationships...")

        count = 0

        for pr in prs:
            if not pr.commit_shas:
                continue

            for sha in pr.commit_shas:
                try:
                    self.connection.execute_write("""
                        MATCH (p:PullRequest {number: $number})
                        MATCH (c:Commit {sha: $sha})
                        MERGE (p)-[:PR_CONTAINS]->(c)
                    """, {"number": pr.number, "sha": sha})
                    count += 1
                except Exception as e:
                    log.debug(f"Could not link PR {pr.number} to commit {sha}: {e}")

        log.info(f"Wrote {count} PR-Commit relationships")

    def write_pr_file_links(self, prs: List[PullRequestEntity]):
        """Write relationships from PRs to modified files.

        Args:
            prs: List of PullRequestEntity objects with files_changed
        """
        log.info("Writing PR-File relationships...")

        count = 0

        for pr in prs:
            if not pr.files_changed:
                continue

            # files_changed could be a count or a list of paths
            if isinstance(pr.files_changed, (int, float)):
                continue

            for file_path in pr.files_changed:
                try:
                    self.connection.execute_write("""
                        MATCH (p:PullRequest {number: $number})
                        MATCH (f:File)
                        WHERE f.path ENDS WITH $file_path
                        MERGE (p)-[:PR_MODIFIES]->(f)
                    """, {"number": pr.number, "file_path": file_path})
                    count += 1
                except Exception as e:
                    log.debug(f"Could not link PR {pr.number} to file {file_path}: {e}")

        log.info(f"Wrote {count} PR-File relationships")

    def write_tasks(self, tasks: List[TaskEntity]):
        """Write task nodes and link to PRs.

        Args:
            tasks: List of TaskEntity objects
        """
        log.info(f"Writing {len(tasks)} task nodes...")

        for task in tasks:
            task_dict = self._entity_to_dict(task)
            # Rename 'order' to 'task_order' to match schema
            if 'order' in task_dict:
                task_dict['task_order'] = task_dict.pop('order')

            try:
                self.connection.execute_write("""
                    MERGE (t:Task {id: $id})
                    SET t.pr_number = $pr_number,
                        t.description = $description,
                        t.is_completed = $is_completed,
                        t.task_order = $task_order
                """, task_dict)

                # Link to PR
                self.connection.execute_write("""
                    MATCH (pr:PullRequest {number: $pr_number})
                    MATCH (t:Task {id: $id})
                    MERGE (pr)-[:HAS_TASK]->(t)
                """, task_dict)
            except Exception as e:
                log.warning(f"Failed to write task {task.id}: {e}")

        log.info(f"Wrote {len(tasks)} task nodes")

    def _entity_to_dict(self, entity) -> dict:
        """Convert an entity to a dictionary for Kuzu.

        Args:
            entity: Entity object (dataclass)

        Returns:
            Dictionary representation
        """
        if hasattr(entity, '__dataclass_fields__'):
            # It's a dataclass
            result = {}
            for field_name, field in entity.__dataclass_fields__.items():
                try:
                    value = getattr(entity, field_name)

                    # Convert datetime to ISO format string for Kuzu timestamp()
                    if isinstance(value, datetime):
                        value = value.isoformat()
                    elif hasattr(value, 'isoformat'):
                        value = value.isoformat()

                    # Convert None lists to empty lists for Kuzu arrays
                    if value is None and 'list' in str(field.type).lower():
                        value = []

                    result[field_name] = value
                except AttributeError as e:
                    log.warning(f"DEBUG: Missing attribute {field_name} on entity {type(entity)}: {e}")
                    # Set default based on type hint
                    if 'list' in str(field.type).lower():
                        result[field_name] = []
                    elif 'bool' in str(field.type).lower():
                        result[field_name] = False
                    elif 'int' in str(field.type).lower():
                        result[field_name] = 0
                    else:
                        result[field_name] = None

            return result
        elif isinstance(entity, dict):
            # Already a dict - return it directly
            return entity
        else:
            # Fallback to __dict__
            log.warning(f"DEBUG: Entity is not a dataclass: type={type(entity)}, hasattr __dict__={hasattr(entity, '__dict__')}")
            return entity.__dict__
