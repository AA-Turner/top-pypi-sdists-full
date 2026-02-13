######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.19                                                                                #
# Generated on 2026-02-09T14:58:07.159425                                                            #
######################################################################################################

from __future__ import annotations

import typing


def get_repository_info(path: str | os.PathLike) -> typing.Dict[str, str | bool]:
    """
    Get git repository information for a path
    
    Returns:
        dict: Dictionary containing:
            repo_url: Repository URL (converted to HTTPS if from SSH)
            branch_name: Current branch name
            commit_sha: Current commit SHA
            has_uncommitted_changes: Boolean indicating if there are uncommitted changes
    """
    ...

