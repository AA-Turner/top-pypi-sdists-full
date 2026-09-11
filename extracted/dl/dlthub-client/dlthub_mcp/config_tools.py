"""Read-only tools over a workspace's variables and configuration files.

Variable **values are never served**, secret or not. The agent's own file tools
are denied credential files while this server inherits the credential
environment, so serving a value here would route around that. These answer which
variables exist and which files a configuration version holds — not what is in
them.
"""

from __future__ import annotations

# Python internals
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

# Other libraries
from dlt.common.typing import Annotated

# Current package
from dlthub_mcp._access import CONTEXT_READ
from dlthub_mcp._client import tool, workspace
from dlthub_sdk import FileEntry


@dataclass(frozen=True)
class VariableInfo:
    """One variable's existence and shape. Carries no value by construction.

    Attributes:
        name: The variable's name, unique within its scope.
        secret: Whether the platform stores it as a secret. A plain variable's
            value is withheld here too — the flag says how it is stored, not
            whether it could have been read.
        updated_at: When it was last changed.
        updated_by: Who last changed it.
    """

    name: str
    secret: bool
    updated_at: datetime
    updated_by: str


@dataclass(frozen=True)
class VariableScopeInfo:
    """The variables one scope holds.

    Attributes:
        profile: The profile these belong to, or ``None`` for the
            workspace-level scope every profile inherits.
        variables: The scope's variables, in the platform's order.
    """

    profile: str | None
    variables: tuple[VariableInfo, ...]


@dataclass(frozen=True)
class ConfigurationFiles:
    """One configuration version and the files it holds.

    Attributes:
        version: Which version this is, counting up from 1 per workspace.
        id: Its uuid.
        profiles: The profiles the configuration files define.
        file_count: How many files it holds, as the platform recorded it.
        size: Total size in bytes.
        content_hash: Hash of the uploaded content, so two versions can be told
            apart without reading them.
        created_at: When it was uploaded.
        created_by: Who uploaded it.
        files: One entry per file — path, size and hash, never content.
    """

    version: int
    id: str
    profiles: tuple[str, ...]
    file_count: int
    size: int
    content_hash: str
    created_at: datetime
    created_by: str
    files: tuple[FileEntry, ...]


@tool
def dlthub_list_variables(
    profile: Optional[str] = None, workspace_scope: bool = False
) -> Annotated[tuple[VariableScopeInfo, ...], CONTEXT_READ]:
    """Which variables this workspace defines, in which scope, VALUES WITHHELD.

    Reach for this to find out whether a job's configuration is even present —
    a run failing on a missing credential shows up here as a name that is not
    set, in a scope you can name. It never returns a value, so it cannot tell
    you whether one is *correct*, only whether it exists.

    A workspace has one scope per profile plus a workspace-level scope that
    every profile inherits, so a name can be set in one and not another.

    Args:
        profile: Limit to one profile's scope, by name. Omit for every scope.
        workspace_scope: Read only the workspace-level scope every profile
            inherits. Ignored when ``profile`` is given.

    Returns:
        One entry per scope, each listing its variables' names, whether they
        are stored as secrets, and when they last changed.

    Raises:
        Exception: A ``ToolError`` when the caller may not read this
            workspace's variables.
    """
    if profile is not None:
        scopes = workspace().variables.list(profile=profile)
    elif workspace_scope:
        scopes = workspace().variables.list(profile=None)
    else:
        scopes = workspace().variables.list()
    return tuple(
        VariableScopeInfo(
            profile=scope.profile,
            variables=tuple(
                VariableInfo(
                    name=variable.name,
                    secret=variable.secret,
                    updated_at=variable.updated_at,
                    updated_by=variable.updated_by,
                )
                for variable in scope.variables
            ),
        )
        for scope in scopes
    )


@tool
def dlthub_get_configuration_files(
    version: Optional[int] = None,
) -> Annotated[ConfigurationFiles, CONTEXT_READ]:
    """Which files a configuration version holds, and which profiles it defines.

    Reach for this to see what configuration a run had available — the file
    paths and the profiles, which is what tells you whether a profile a job
    names is actually defined. File contents are never served.

    Args:
        version: The configuration version, counting from 1. Omit for the
            latest, which is what a new run uses.

    Returns:
        The version's metadata and one entry per file, each with its path, size
        and content hash.

    Raises:
        Exception: A ``ToolError`` when no such version exists, or the
            workspace has no configuration at all.
    """
    configurations = workspace().configurations
    configuration = (
        configurations.latest()
        if version is None
        else configurations.get(version=version)
    )
    return ConfigurationFiles(
        version=configuration.version,
        id=configuration.id,
        profiles=configuration.profiles,
        file_count=configuration.file_count,
        size=configuration.size,
        content_hash=configuration.content_hash,
        created_at=configuration.created_at,
        created_by=configuration.created_by,
        files=configuration.files(),
    )


__tools__ = (dlthub_list_variables, dlthub_get_configuration_files)
