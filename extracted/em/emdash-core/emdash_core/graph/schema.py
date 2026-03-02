"""Kuzu schema initialization and management."""

from .connection import KuzuConnection, get_connection
from ..utils.logger import log


class SchemaManager:
    """Manages Kuzu database schema (tables, indexes)."""

    # Node table definitions
    NODE_TABLES = {
        "File": """
            CREATE NODE TABLE File (
                path STRING,
                name STRING,
                extension STRING,
                size_bytes INT64,
                lines_of_code INT64,
                hash STRING,
                last_modified TIMESTAMP,
                commit_importance DOUBLE,
                commit_count INT64,
                author_count INT64,
                PRIMARY KEY (path)
            )
        """,
        "Class": """
            CREATE NODE TABLE Class (
                qualified_name STRING,
                name STRING,
                file_path STRING,
                line_start INT64,
                line_end INT64,
                docstring STRING,
                is_abstract BOOL,
                decorators STRING[],
                base_classes STRING[],
                attributes STRING[],
                methods STRING[],
                pagerank DOUBLE,
                betweenness DOUBLE,
                community INT64,
                embedding DOUBLE[],
                PRIMARY KEY (qualified_name)
            )
        """,
        "Function": """
            CREATE NODE TABLE Function (
                qualified_name STRING,
                name STRING,
                file_path STRING,
                line_start INT64,
                line_end INT64,
                docstring STRING,
                parameters STRING[],
                return_annotation STRING,
                is_async BOOL,
                is_method BOOL,
                is_static BOOL,
                is_classmethod BOOL,
                decorators STRING[],
                cyclomatic_complexity INT64,
                calls STRING[],
                pagerank DOUBLE,
                betweenness DOUBLE,
                community INT64,
                embedding DOUBLE[],
                PRIMARY KEY (qualified_name)
            )
        """,
        "Community": """
            CREATE NODE TABLE Community (
                community_id INT64,
                description STRING,
                source STRING,
                embedding DOUBLE[],
                PRIMARY KEY (community_id)
            )
        """,
        "Module": """
            CREATE NODE TABLE Module (
                name STRING,
                import_path STRING,
                is_external BOOL,
                package STRING,
                PRIMARY KEY (name)
            )
        """,
        "Repository": """
            CREATE NODE TABLE Repository (
                url STRING,
                name STRING,
                owner STRING,
                default_branch STRING,
                last_ingested TIMESTAMP,
                last_indexed_commit STRING,
                ingestion_status STRING,
                commit_count INT64,
                file_count INT64,
                primary_language STRING,
                PRIMARY KEY (url)
            )
        """,
        "Commit": """
            CREATE NODE TABLE Commit (
                sha STRING,
                message STRING,
                timestamp TIMESTAMP,
                author_name STRING,
                author_email STRING,
                committer_name STRING,
                committer_email STRING,
                insertions INT64,
                deletions INT64,
                files_changed INT64,
                is_merge BOOL,
                parent_shas STRING[],
                PRIMARY KEY (sha)
            )
        """,
        "Author": """
            CREATE NODE TABLE Author (
                email STRING,
                name STRING,
                first_commit TIMESTAMP,
                last_commit TIMESTAMP,
                total_commits INT64,
                total_lines_added INT64,
                total_lines_deleted INT64,
                PRIMARY KEY (email)
            )
        """,
        "PullRequest": """
            CREATE NODE TABLE PullRequest (
                number INT64,
                title STRING,
                state STRING,
                created_at TIMESTAMP,
                author STRING,
                description STRING,
                merged_at TIMESTAMP,
                reviewers STRING[],
                labels STRING[],
                additions INT64,
                deletions INT64,
                files_changed INT64,
                commit_shas STRING[],
                base_branch STRING,
                head_branch STRING,
                embedding DOUBLE[],
                PRIMARY KEY (number)
            )
        """,
        "Task": """
            CREATE NODE TABLE Task (
                id STRING,
                pr_number INT64,
                description STRING,
                is_completed BOOL,
                task_order INT64,
                PRIMARY KEY (id)
            )
        """,
    }

    # Relationship table definitions
    REL_TABLES = {
        "CONTAINS_CLASS": """
            CREATE REL TABLE CONTAINS_CLASS (
                FROM File TO Class,
                line_start INT64
            )
        """,
        "CONTAINS_FUNCTION": """
            CREATE REL TABLE CONTAINS_FUNCTION (
                FROM File TO Function,
                line_start INT64
            )
        """,
        "HAS_METHOD": """
            CREATE REL TABLE HAS_METHOD (
                FROM Class TO Function
            )
        """,
        "INHERITS_FROM": """
            CREATE REL TABLE INHERITS_FROM (
                FROM Class TO Class
            )
        """,
        "CALLS": """
            CREATE REL TABLE CALLS (
                FROM Function TO Function
            )
        """,
        "IMPORTS": """
            CREATE REL TABLE IMPORTS (
                FROM File TO Module,
                import_type STRING,
                line_number INT64,
                alias STRING
            )
        """,
        "AUTHORED_BY": """
            CREATE REL TABLE AUTHORED_BY (
                FROM Commit TO Author
            )
        """,
        "COMMIT_MODIFIES": """
            CREATE REL TABLE COMMIT_MODIFIES (
                FROM Commit TO File,
                change_type STRING,
                insertions INT64,
                deletions INT64,
                old_path STRING
            )
        """,
        "PR_CONTAINS": """
            CREATE REL TABLE PR_CONTAINS (
                FROM PullRequest TO Commit
            )
        """,
        "PR_MODIFIES": """
            CREATE REL TABLE PR_MODIFIES (
                FROM PullRequest TO File
            )
        """,
        "HAS_TASK": """
            CREATE REL TABLE HAS_TASK (
                FROM PullRequest TO Task
            )
        """,
    }

    def __init__(self, connection: KuzuConnection = None):
        """Initialize schema manager.

        Args:
            connection: Kuzu connection. If None, uses global connection.
        """
        self.connection = connection or get_connection()

    def initialize_schema(self):
        """Initialize the complete database schema."""
        log.info("Initializing Kuzu schema...")

        self.create_node_tables()
        self.create_rel_tables()
        self.create_indexes()

        log.info("Schema initialization complete")

    def create_node_tables(self):
        """Create all node tables."""
        log.info("Creating node tables...")

        conn = self.connection.connect()
        for table_name, ddl in self.NODE_TABLES.items():
            try:
                conn.execute(ddl)
                log.debug(f"Created node table: {table_name}")
            except Exception as e:
                # Table might already exist
                if "already exists" not in str(e).lower():
                    log.warning(f"Failed to create node table {table_name}: {e}")

        log.info("Node tables created successfully")

    def create_rel_tables(self):
        """Create all relationship tables."""
        log.info("Creating relationship tables...")

        conn = self.connection.connect()
        for table_name, ddl in self.REL_TABLES.items():
            try:
                conn.execute(ddl)
                log.debug(f"Created relationship table: {table_name}")
            except Exception as e:
                # Table might already exist
                if "already exists" not in str(e).lower():
                    log.warning(f"Failed to create rel table {table_name}: {e}")

        log.info("Relationship tables created successfully")

    def create_indexes(self):
        """Create performance indexes."""
        log.info("Creating indexes...")

        # Kuzu index creation - no IF NOT EXISTS support
        # Format: CREATE INDEX idx_name ON TableName(property)
        indexes = [
            # File indexes
            ("idx_file_name", "File", "name"),
            ("idx_file_extension", "File", "extension"),

            # Class indexes
            ("idx_class_name", "Class", "name"),
            ("idx_class_file_path", "Class", "file_path"),
            ("idx_class_qualified_name", "Class", "qualified_name"),

            # Function indexes
            ("idx_func_name", "Function", "name"),
            ("idx_func_file_path", "Function", "file_path"),
            ("idx_func_qualified_name", "Function", "qualified_name"),

            # Module indexes
            ("idx_module_import_path", "Module", "import_path"),

            # Commit indexes
            ("idx_commit_timestamp", "Commit", "timestamp"),
            ("idx_commit_author", "Commit", "author_name"),

            # Author indexes
            ("idx_author_name", "Author", "name"),

            # Pull Request indexes
            ("idx_pr_state", "PullRequest", "state"),
            ("idx_pr_created", "PullRequest", "created_at"),

            # Task indexes
            ("idx_task_pr", "Task", "pr_number"),
            ("idx_task_completed", "Task", "is_completed"),
        ]

        conn = self.connection.connect()
        for idx_name, table, prop in indexes:
            try:
                conn.execute(f"CREATE INDEX {idx_name} ON {table}({prop})")
                log.debug(f"Created index: {idx_name}")
            except Exception as e:
                # Index might already exist
                if "already exists" not in str(e).lower():
                    log.debug(f"Index {idx_name} skipped: {e}")

        log.info("Indexes created successfully")

    def drop_all_tables(self):
        """Drop all tables in the database."""
        log.warning("Dropping all tables...")

        conn = self.connection.connect()

        # Get all tables
        result = conn.execute("CALL show_tables() RETURN *")
        tables = []
        while result.has_next():
            row = result.get_next()
            tables.append((row[0], row[1] if len(row) > 1 else "NODE"))

        # Drop relationship tables first (they depend on node tables)
        for table_name, table_type in tables:
            if table_type == "REL":
                try:
                    conn.execute(f"DROP TABLE {table_name}")
                    log.debug(f"Dropped table: {table_name}")
                except Exception as e:
                    log.warning(f"Failed to drop table {table_name}: {e}")

        # Then drop node tables
        for table_name, table_type in tables:
            if table_type == "NODE":
                try:
                    conn.execute(f"DROP TABLE {table_name}")
                    log.debug(f"Dropped table: {table_name}")
                except Exception as e:
                    log.warning(f"Failed to drop table {table_name}: {e}")

        log.info("All tables dropped")

    def reset_schema(self):
        """Reset the entire schema (drop and recreate)."""
        log.warning("Resetting schema...")
        self.drop_all_tables()
        self.initialize_schema()
        log.info("Schema reset complete")

    def get_schema_info(self) -> dict:
        """Get information about the current schema.

        Returns:
            Dictionary with table information
        """
        conn = self.connection.connect()

        # Get all tables
        result = conn.execute("CALL show_tables() RETURN *")
        node_tables = []
        rel_tables = []

        while result.has_next():
            row = result.get_next()
            table_name = row[0]
            table_type = row[1] if len(row) > 1 else "NODE"

            if table_type == "NODE":
                node_tables.append(table_name)
            elif table_type == "REL":
                rel_tables.append(table_name)

        return {
            "node_tables": node_tables,
            "rel_tables": rel_tables,
        }


def initialize_database():
    """Initialize the Kuzu database with schema.

    This is a convenience function that can be called from CLI.
    """
    connection = get_connection()
    connection.connect()

    schema_manager = SchemaManager(connection)
    schema_manager.initialize_schema()

    log.info("Database initialized successfully")
