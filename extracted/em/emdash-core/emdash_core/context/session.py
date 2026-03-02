"""Session context manager for Kuzu persistence."""

import os
import uuid
from datetime import datetime
from typing import Optional

from .models import ContextItem, SessionContext
from ..graph.connection import KuzuConnection
from ..utils.logger import log


class SessionContextManager:
    """Manages session context persistence in Kuzu.

    Handles:
    - Creating and retrieving sessions by terminal ID
    - Storing and updating context items
    - Applying score decay to existing items
    - Filtering items by minimum score
    """

    def __init__(self, connection: KuzuConnection):
        """Initialize session context manager.

        Args:
            connection: Kuzu database connection
        """
        self.connection = connection
        self._decay_factor = float(os.getenv("CONTEXT_DECAY_FACTOR", "0.8"))
        self._ensure_schema()

    def _ensure_schema(self):
        """Ensure Session and ContextItem tables exist."""
        try:
            # Try to create tables (IF NOT EXISTS handles idempotency)
            log.debug("Ensuring Session table exists...")
            self.connection.execute_write(
                """
                CREATE NODE TABLE IF NOT EXISTS Session (
                    session_id STRING,
                    terminal_id STRING,
                    created_at TIMESTAMP,
                    last_active TIMESTAMP,
                    PRIMARY KEY (session_id)
                )
                """
            )

            log.debug("Ensuring ContextItem table exists...")
            self.connection.execute_write(
                """
                CREATE NODE TABLE IF NOT EXISTS ContextItem (
                    id STRING,
                    session_id STRING,
                    qualified_name STRING,
                    entity_type STRING,
                    description STRING,
                    file_path STRING,
                    score DOUBLE,
                    touch_count INT64,
                    last_touched TIMESTAMP,
                    neighbors STRING[],
                    PRIMARY KEY (id)
                )
                """
            )

            log.debug("Ensuring SESSION_HAS_CONTEXT relationship exists...")
            self.connection.execute_write(
                """
                CREATE REL TABLE IF NOT EXISTS SESSION_HAS_CONTEXT (
                    FROM Session TO ContextItem
                )
                """
            )

        except Exception as e:
            log.warning(f"Failed to ensure schema (may already exist): {e}")

    def get_or_create_session(self, terminal_id: str) -> SessionContext:
        """Get existing session for terminal or create a new one.

        Args:
            terminal_id: Unique identifier for the terminal

        Returns:
            SessionContext for the terminal
        """
        # Try to find existing session
        results = self.connection.execute(
            """
            MATCH (s:Session {terminal_id: $terminal_id})
            RETURN s.session_id as session_id,
                   s.terminal_id as terminal_id,
                   s.created_at as created_at,
                   s.last_active as last_active
            ORDER BY s.last_active DESC
            LIMIT 1
            """,
            {"terminal_id": terminal_id},
        )

        if results:
            row = results[0]
            # Update last_active
            self.connection.execute_write(
                """
                MATCH (s:Session {session_id: $session_id})
                SET s.last_active = timestamp($now)
                """,
                {"session_id": row["session_id"], "now": datetime.now().isoformat()},
            )

            return SessionContext(
                session_id=row["session_id"],
                terminal_id=row["terminal_id"],
                created_at=row.get("created_at"),
                last_active=datetime.now(),
            )

        # Create new session
        session_id = str(uuid.uuid4())
        now = datetime.now()

        self.connection.execute_write(
            """
            CREATE (s:Session {
                session_id: $session_id,
                terminal_id: $terminal_id,
                created_at: timestamp($created_at),
                last_active: timestamp($last_active)
            })
            """,
            {
                "session_id": session_id,
                "terminal_id": terminal_id,
                "created_at": now.isoformat(),
                "last_active": now.isoformat(),
            },
        )

        log.info(f"Created new session {session_id} for terminal {terminal_id}")

        return SessionContext(
            session_id=session_id,
            terminal_id=terminal_id,
            created_at=now,
            last_active=now,
        )

    def add_context_items(self, session_id: str, items: list[ContextItem]):
        """Add new context items, applying decay to existing ones.

        Args:
            session_id: Session to add items to
            items: Context items to add
        """
        if not items:
            return

        # First, decay existing items
        self._decay_existing(session_id)

        # Then upsert new items
        for item in items:
            self._upsert_item(session_id, item)

        log.info(f"Added {len(items)} context items to session {session_id}")

    def _decay_existing(self, session_id: str):
        """Apply decay factor to existing context items.

        Args:
            session_id: Session to decay items for
        """
        try:
            self.connection.execute_write(
                """
                MATCH (s:Session {session_id: $session_id})-[:SESSION_HAS_CONTEXT]->(c:ContextItem)
                SET c.score = c.score * $factor
                """,
                {"session_id": session_id, "factor": self._decay_factor},
            )
        except Exception as e:
            log.warning(f"Failed to decay existing items: {e}")

    def _upsert_item(self, session_id: str, item: ContextItem):
        """Insert or update a context item.

        Args:
            session_id: Session ID
            item: Context item to upsert
        """
        item_id = f"{session_id}:{item.qualified_name}"
        now = datetime.now()

        try:
            # Check if item exists
            existing = self.connection.execute(
                """
                MATCH (c:ContextItem {id: $id})
                RETURN c.touch_count as touch_count
                """,
                {"id": item_id},
            )

            if existing:
                # Update existing - increment touch count and reset score
                touch_count = (existing[0].get("touch_count") or 0) + 1
                self.connection.execute_write(
                    """
                    MATCH (c:ContextItem {id: $id})
                    SET c.score = 1.0,
                        c.touch_count = $touch_count,
                        c.last_touched = timestamp($now),
                        c.description = $description,
                        c.neighbors = $neighbors
                    """,
                    {
                        "id": item_id,
                        "touch_count": touch_count,
                        "now": now.isoformat(),
                        "description": item.description,
                        "neighbors": item.neighbors or [],
                    },
                )
            else:
                # Create new item
                self.connection.execute_write(
                    """
                    CREATE (c:ContextItem {
                        id: $id,
                        session_id: $session_id,
                        qualified_name: $qualified_name,
                        entity_type: $entity_type,
                        description: $description,
                        file_path: $file_path,
                        score: $score,
                        touch_count: $touch_count,
                        last_touched: timestamp($last_touched),
                        neighbors: $neighbors
                    })
                    """,
                    {
                        "id": item_id,
                        "session_id": session_id,
                        "qualified_name": item.qualified_name,
                        "entity_type": item.entity_type,
                        "description": item.description,
                        "file_path": item.file_path,
                        "score": item.score,
                        "touch_count": item.touch_count,
                        "last_touched": now.isoformat(),
                        "neighbors": item.neighbors or [],
                    },
                )

                # Create relationship
                self.connection.execute_write(
                    """
                    MATCH (s:Session {session_id: $session_id})
                    MATCH (c:ContextItem {id: $item_id})
                    CREATE (s)-[:SESSION_HAS_CONTEXT]->(c)
                    """,
                    {"session_id": session_id, "item_id": item_id},
                )

        except Exception as e:
            log.warning(f"Failed to upsert context item {item.qualified_name}: {e}")

    def get_context(self, session_id: str, min_score: float = 0.3) -> list[ContextItem]:
        """Get context items above minimum score.

        Args:
            session_id: Session to get items for
            min_score: Minimum score threshold

        Returns:
            List of context items
        """
        try:
            results = self.connection.execute(
                """
                MATCH (s:Session {session_id: $session_id})-[:SESSION_HAS_CONTEXT]->(c:ContextItem)
                WHERE c.score >= $min_score
                RETURN c.qualified_name as qualified_name,
                       c.entity_type as entity_type,
                       c.description as description,
                       c.file_path as file_path,
                       c.score as score,
                       c.touch_count as touch_count,
                       c.last_touched as last_touched,
                       c.neighbors as neighbors
                ORDER BY c.score DESC
                """,
                {"session_id": session_id, "min_score": min_score},
            )

            items = []
            for row in results:
                items.append(
                    ContextItem(
                        qualified_name=row["qualified_name"],
                        entity_type=row["entity_type"],
                        description=row.get("description"),
                        file_path=row.get("file_path"),
                        score=row.get("score", 0.0),
                        touch_count=row.get("touch_count", 1),
                        last_touched=row.get("last_touched"),
                        neighbors=row.get("neighbors") or [],
                    )
                )

            return items

        except Exception as e:
            log.warning(f"Failed to get context for session {session_id}: {e}")
            return []

    def clear_session(self, session_id: str):
        """Clear all context items for a session.

        Args:
            session_id: Session to clear
        """
        try:
            # Delete context items
            self.connection.execute_write(
                """
                MATCH (s:Session {session_id: $session_id})-[:SESSION_HAS_CONTEXT]->(c:ContextItem)
                DETACH DELETE c
                """,
                {"session_id": session_id},
            )
            log.info(f"Cleared context for session {session_id}")
        except Exception as e:
            log.warning(f"Failed to clear session {session_id}: {e}")

    def cleanup_old_sessions(self, max_age_days: int = 7):
        """Remove sessions older than max_age_days.

        Args:
            max_age_days: Maximum age in days for sessions
        """
        try:
            # This is a simplified cleanup - proper implementation would use
            # timestamp comparison, but Kuzu's timestamp handling varies
            log.info(f"Cleaning up sessions older than {max_age_days} days")
            # TODO: Implement proper date-based cleanup
        except Exception as e:
            log.warning(f"Failed to cleanup old sessions: {e}")
