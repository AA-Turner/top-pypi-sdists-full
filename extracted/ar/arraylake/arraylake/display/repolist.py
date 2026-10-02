"""
RepoList class with rich table representations for Arraylake repositories.
"""

import textwrap
from collections.abc import Sequence
from typing import Union, overload

from arraylake.types import Repo as RepoModel


def create_html_table(repos: Sequence[RepoModel], org: str) -> str:
    """Create an HTML table for displaying repositories in Jupyter notebooks."""
    if not repos:
        return f"<p>No repositories found for organization <strong>{org}</strong></p>"

    html_parts = [
        f"<h4>Arraylake Repositories for <strong>{org}</strong></h4>",
        '<table style="border-collapse: collapse; width: 100%;">',
        "<thead>",
        '<tr style="background-color: #f0f0f0;">',
        '<th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Name</th>',
        '<th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Created</th>',
        '<th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Updated</th>',
        '<th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Kind</th>',
        '<th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Description</th>',
        '<th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Metadata</th>',
        '<th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Status</th>',
        "</tr>",
        "</thead>",
        "<tbody>",
    ]

    mode_colors = {"online": "#28a745", "maintenance": "#ffc107", "offline": "#dc3545"}

    for repo in repos:
        status_color = mode_colors.get(repo.status.mode, "#6c757d")

        # Format metadata for HTML
        metadata_html = ""
        if repo.metadata:
            metadata_items = []
            for k, v in repo.metadata.items():
                v_str = ", ".join(map(str, v)) if isinstance(v, list) else str(v)
                metadata_items.append(f"<strong>{k}:</strong> {v_str}")
            metadata_html = "<br>".join(metadata_items)

        html_parts.extend(
            [
                "<tr>",
                f'<td style="border: 1px solid #ddd; padding: 8px;">{repo.name}</td>',
                f'<td style="border: 1px solid #ddd; padding: 8px;">{repo.created.isoformat()}</td>',
                f'<td style="border: 1px solid #ddd; padding: 8px;">{repo.updated.isoformat()}</td>',
                f'<td style="border: 1px solid #ddd; padding: 8px;">{repo.kind}</td>',
                f'<td style="border: 1px solid #ddd; padding: 8px;">{repo.description or ""}</td>',
                f'<td style="border: 1px solid #ddd; padding: 8px; font-size: 0.9em;">{metadata_html}</td>',
                f'<td style="border: 1px solid #ddd; padding: 8px; color: {status_color}; font-weight: bold;">{repo.status.mode}</td>',
                "</tr>",
            ]
        )

    html_parts.extend(["</tbody>", "</table>"])

    return "\n".join(html_parts)


class RepoList(Sequence[RepoModel]):
    """
    A sequence of Repo objects with rich display representations.

    Repos are sorted by most recently updated first.

    To get an actual python list of `Repo` objects simply call `list()` on this object.
    """

    def __init__(self, repos: Sequence[RepoModel], *, org: str):
        """Initialize RepoList with repositories and organization name.

        Args:
            repos: Sequence of RepoModel objects
            org: Organization name for display purposes
        """

        # sort by most recently updated
        sorted_items = sorted(repos, key=lambda item: item.updated, reverse=True)

        self._items = sorted_items
        self._org = org

    def _repr_html_(self) -> str:
        """Return an HTML representation for Jupyter notebooks."""
        return create_html_table(self, self._org)

    def __repr__(self) -> str:
        header = f"<RepoList> org='{self._org}', num_repos={len(self._items)}"

        if not self._items:
            return header

        repo_reprs = [textwrap.indent(repr(repo), "  ") for repo in self._items]
        return "\n".join([header] + repo_reprs)

    # list-like methods (Sequence provides the rest via mixins)

    @overload
    def __getitem__(self, index: int) -> RepoModel: ...

    @overload
    def __getitem__(self, index: slice) -> "RepoList": ...

    def __getitem__(self, index: int | slice) -> Union[RepoModel, "RepoList"]:
        result = self._items[index]
        if isinstance(result, RepoModel):
            # selection of a single item in a list returns the item, not a length-1 list
            return result
        else:
            # preserve RepoList class if user slices into it
            return RepoList(repos=result, org=self._org)

    def __len__(self):
        return len(self._items)
