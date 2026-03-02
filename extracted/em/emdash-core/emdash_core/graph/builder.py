"""Graph construction - coordinates entity writing to Kuzu."""

from ..core.models import CodebaseEntities, GitData
from .connection import KuzuConnection
from .writer import GraphWriter
from ..utils.logger import log


class GraphBuilder:
    """Builds the Kuzu knowledge graph from extracted entities."""

    def __init__(self, connection: KuzuConnection, batch_size: int = 1000):
        """Initialize graph builder.

        Args:
            connection: Neo4j connection
            batch_size: Batch size for write operations
        """
        self.connection = connection
        self.batch_size = batch_size

    def build_code_graph(self, entities: CodebaseEntities):
        """Build Layer A: Code structure graph.

        Args:
            entities: Codebase entities to write
        """
        log.info("Building code structure graph (Layer A)...")

        # Use connection directly for Kuzu (no session needed)
        writer = GraphWriter(self.connection, self.batch_size)

        # Pass 1: Create nodes
        log.info("Pass 1: Creating nodes...")
        writer.write_files(entities.files)
        writer.write_modules(entities.modules)
        writer.write_classes(entities.classes)
        writer.write_functions(entities.functions)

        # Pass 2: Create relationships
        log.info("Pass 2: Creating relationships...")
        writer.write_imports(entities.imports)
        writer.write_inheritance(entities.classes)
        writer.write_calls(entities.functions)

        log.info("Code graph construction complete")

    def build_git_graph(self, git_data: GitData):
        """Build Layer B: Git history graph.

        Args:
            git_data: Git data to write
        """
        log.info("Building git history graph (Layer B)...")

        # Use connection directly for Kuzu (no session needed)
        writer = GraphWriter(self.connection, self.batch_size)

        # Create nodes
        writer.write_authors(git_data.authors)
        writer.write_commits(git_data.commits)

        # Create relationships
        writer.write_commit_authorship(git_data.commits)
        writer.write_file_modifications(git_data.modifications)

        log.info("Git graph construction complete")

    def delete_files(self, file_paths: list[str]) -> int:
        """Remove files and their associated entities from graph.

        Deletes:
        1. Classes and Functions belonging to these files
        2. Relationships (CONTAINS_CLASS, CONTAINS_FUNCTION, IMPORTS, etc.)
        3. The File nodes themselves

        Args:
            file_paths: List of file paths to remove

        Returns:
            Number of files deleted
        """
        if not file_paths:
            return 0

        log.info(f"Deleting {len(file_paths)} files from graph...")

        deleted_count = 0
        for file_path in file_paths:
            try:
                # Delete classes belonging to this file
                self.connection.execute_write(
                    "MATCH (c:Class) WHERE c.file_path = $path DETACH DELETE c",
                    {"path": file_path}
                )

                # Delete functions belonging to this file
                self.connection.execute_write(
                    "MATCH (f:Function) WHERE f.file_path = $path DETACH DELETE f",
                    {"path": file_path}
                )

                # Delete the file node itself (and its relationships)
                self.connection.execute_write(
                    "MATCH (f:File {path: $path}) DETACH DELETE f",
                    {"path": file_path}
                )

                deleted_count += 1
            except Exception as e:
                log.warning(f"Failed to delete file {file_path}: {e}")

        log.info(f"Deleted {deleted_count} files from graph")
        return deleted_count

    def clear_repository_data(self, repo_url: str):
        """Clear all data for a specific repository.

        Args:
            repo_url: Repository URL
        """
        log.warning(f"Clearing data for repository: {repo_url}")

        # Use connection directly for Kuzu (no session needed)
        # Delete all nodes related to this repository
        # This is a simplified version - in production you'd want more sophisticated cleanup
        query = """
        MATCH (r:Repository {url: $url})
        OPTIONAL MATCH (r)-[*]-(n)
        DETACH DELETE r, n
        """
        self.connection.execute_write(query, {"url": repo_url})

        log.info("Repository data cleared")
