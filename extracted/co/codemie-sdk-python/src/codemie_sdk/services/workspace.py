"""Agent workspace service implementation."""

from __future__ import annotations

from ..models.workspace import (
    ExecuteWorkspaceScriptResponse,
    Workspace,
    WorkspaceDeleteFileResponse,
    WorkspaceFileContent,
    WorkspaceFileItem,
)
from ..utils.http import ApiRequestHandler, TokenSource


class WorkspaceService:
    """Service for the files of agent workspaces (one workspace per conversation)."""

    def __init__(self, api_domain: str, token: TokenSource, verify_ssl: bool = True):
        """Initialize the workspace service.

        Args:
            api_domain: Base URL for the CodeMie API
            token: Authentication token
            verify_ssl: Whether to verify SSL certificates. Default: True
        """
        self._api = ApiRequestHandler(api_domain, token, verify_ssl)

    def create(self, conversation_id: str, name: str | None = None) -> Workspace:
        """Create the workspace of a conversation, or return the existing one.

        Args:
            conversation_id: Conversation (or workflow execution) identifier
            name: Optional display name

        Returns:
            The workspace of the conversation
        """
        return self._api.post(
            "/v1/workspaces",
            Workspace,
            json_data={"conversation_id": conversation_id, "name": name},
        )

    def get_by_conversation(self, conversation_id: str) -> Workspace:
        """Get the workspace of a conversation.

        Args:
            conversation_id: Conversation (or workflow execution) identifier

        Returns:
            The workspace of the conversation

        Raises:
            requests.HTTPError: 400 when the conversation has no workspace
        """
        return self._api.get(
            f"/v1/workspaces/conversations/{conversation_id}", Workspace
        )

    def list_files(
        self, workspace_id: str, glob: str | None = None
    ) -> list[WorkspaceFileItem]:
        """List the files of a workspace.

        Args:
            workspace_id: Workspace identifier
            glob: Optional glob filter on the file path

        Returns:
            Files currently in the workspace (deleted files are not listed)
        """
        return self._api.get(
            f"/v1/workspaces/{workspace_id}/files",
            list[WorkspaceFileItem],
            params={"glob": glob} if glob else None,
        )

    def write_file(
        self, workspace_id: str, file_path: str, content: str
    ) -> WorkspaceFileItem:
        """Create or overwrite a text file in a workspace.

        Args:
            workspace_id: Workspace identifier
            file_path: Workspace-relative path
            content: UTF-8 text content

        Returns:
            The written file

        Raises:
            requests.HTTPError: 400 when the path is invalid or reserved
        """
        return self._api.put(
            f"/v1/workspaces/{workspace_id}/files",
            WorkspaceFileItem,
            json_data={"file_path": file_path, "content": content},
        )

    def read_file(self, workspace_id: str, file_path: str) -> WorkspaceFileContent:
        """Read a file of a workspace.

        Args:
            workspace_id: Workspace identifier
            file_path: Workspace-relative path

        Returns:
            The file with its content

        Raises:
            requests.HTTPError: 400 when the file does not exist
        """
        return self._api.get(
            f"/v1/workspaces/{workspace_id}/files/content",
            WorkspaceFileContent,
            params={"file_path": file_path},
        )

    def delete_file(
        self, workspace_id: str, file_path: str
    ) -> WorkspaceDeleteFileResponse:
        """Delete a file from a workspace (the file stays deleted for later requests).

        Args:
            workspace_id: Workspace identifier
            file_path: Workspace-relative path

        Returns:
            Whether a file was deleted

        Raises:
            requests.HTTPError: 400 when the path is invalid or reserved
        """
        return self._api.delete(
            f"/v1/workspaces/{workspace_id}/files",
            WorkspaceDeleteFileResponse,
            params={"file_path": file_path},
        )

    def execute_script(
        self,
        workspace_id: str,
        script_path: str,
        export_files: list[str] | None = None,
    ) -> ExecuteWorkspaceScriptResponse:
        """Run a Python script stored in a workspace.

        Args:
            workspace_id: Workspace identifier
            script_path: Workspace-relative path of the script
            export_files: Optional workspace files to export from the run

        Returns:
            Script output, exported files and warnings about skipped workspace files
        """
        return self._api.post(
            f"/v1/workspaces/{workspace_id}/execute",
            ExecuteWorkspaceScriptResponse,
            json_data={"script_path": script_path, "export_files": export_files},
        )
