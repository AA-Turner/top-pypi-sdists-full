import typing as t

from pydantic import Field

from dreadnode.agents.tools import Toolset, tool_method
from dreadnode.storage.storage import Storage


def _single_line(text: str) -> str:
    return " ".join(text.split())


class TrajectorySearch(Toolset):
    """Session-scoped transcript search over the persisted local session index."""

    storage: Storage = Field(..., description="Storage manager that owns the session index.")
    session_id: str = Field(..., min_length=1, description="Current session identifier.")

    @tool_method(name="session_search")
    def search_current_session(
        self,
        query: t.Annotated[
            str,
            "Full-text query over the current session transcript. Plain words work best.",
        ],
        *,
        limit: t.Annotated[int, "Maximum number of matching messages to return."] = 10,
        role: t.Annotated[
            t.Literal["user", "assistant", "tool", "system"] | None,
            "Optional role filter applied after transcript search.",
        ] = None,
    ) -> str:
        """
        Search prior messages in the current session transcript.

        This tool only searches the active session, not all sessions. Use it to recover
        earlier findings, commands, or user requirements without asking the user to
        restate them.
        """
        if not query.strip():
            raise ValueError("Query must not be empty.")

        capped_limit = min(max(limit, 1), 25)
        search_limit = capped_limit * 4 if role is not None else capped_limit
        matches = self.storage.session_store.search_messages(
            query,
            session_id=self.session_id,
            limit=search_limit,
        )

        if role is not None:
            matches = [match for match in matches if match.role == role]

        matches = matches[:capped_limit]
        if not matches:
            scope = f" with role '{role}'" if role is not None else ""
            return f"No matches found in the current session{scope}."

        lines = [f"Found {len(matches)} matching messages in the current session:"]
        for match in matches:
            snippet = _single_line(match.snippet or match.content)
            lines.append(f"- #{match.seq} [{match.role}] {snippet}")
        return "\n".join(lines)
