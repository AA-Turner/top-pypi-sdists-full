"""
Printer classes for formatting and displaying PullApprove output.
"""

from __future__ import annotations

import hashlib
import json
from typing import TYPE_CHECKING

import click

from .config import ScopeModel
from .schemas import matches_schema

if TYPE_CHECKING:
    from .matches import ChangeMatches

# Base colors for scope names (cycle through these)
SCOPE_COLORS = ["green", "yellow", "blue", "magenta", "cyan", "red"]


def get_color_for_name(name: str) -> str:
    """Get a consistent color for a given name using deterministic hash."""
    # Use MD5 for a deterministic hash across Python invocations
    name_hash = int(hashlib.md5(name.encode()).hexdigest()[:8], 16)
    return SCOPE_COLORS[name_hash % len(SCOPE_COLORS)]


def get_scope_display(scope: ScopeModel) -> str:
    """Get a colored display string for a scope.

    Ownership is carried by the printed marker alone, never by brightness --
    dimming `global` made the one scope that can pass a file by itself the
    faintest thing on screen. Same rule as the web UI (see ownership.ts).
    """
    color = get_color_for_name(scope.name)

    return click.style(scope.printed_name(), fg=color)


def print_scope_badge(scope_name: str, scopes: dict[str, ScopeModel]) -> str:
    """Print a scope badge with a dimmed arrow prefix."""
    arrow = click.style("→ ", dim=True)
    if scope_name in scopes:
        return arrow + get_scope_display(scopes[scope_name])
    return arrow + scope_name


class MatchesPrinter:
    """Handles printing of file/scope matches."""

    def __init__(self, *, matches: ChangeMatches, all_files: list[str]) -> None:
        self.matches = matches
        # Every file that was looked at, including the ones no scope owns
        self.all_files = all_files

    def print_by_path(self, scope_filter: tuple[str, ...] | None = None) -> None:
        """Print matches organized by file path."""
        all_paths = self.all_files

        if not all_paths:
            click.echo("No files found.")
            return

        if scope_filter:
            all_paths = self._paths_matching_scopes(
                paths=all_paths, scope_filter=scope_filter
            )

            if not all_paths:
                click.echo(f"No files found matching scopes: {', '.join(scope_filter)}")
                return

        # Sort paths for consistent output
        for path in sorted(all_paths):
            line = path

            # Get scope badges if file has scopes
            if path in self.matches.paths:
                path_match = self.matches.paths[path]
                if path_match.scopes:
                    badges = []
                    for scope_name in path_match.scopes:
                        badges.append(
                            print_scope_badge(scope_name, self.matches.scopes)
                        )
                    line += " " + " ".join(badges)
                    click.echo(line)
                else:
                    # Dim files without scopes
                    click.echo(click.style(line, dim=True))
            else:
                # Dim files without scopes
                click.echo(click.style(line, dim=True))

            # Print code patterns for this file if any
            code_patterns = self._get_file_code_patterns_simple(path)
            for pattern_line in code_patterns:
                click.echo("  " + pattern_line)

    def _paths_matching_scopes(
        self, *, paths: list[str], scope_filter: tuple[str, ...]
    ) -> list[str]:
        """The paths where any path or code match has a scope in the filter."""
        matching_paths = set()
        for path, path_match in self.matches.paths.items():
            if any(s in scope_filter for s in path_match.scopes):
                matching_paths.add(path)
        for code_match in self.matches.code.values():
            if any(s in scope_filter for s in code_match.scopes):
                matching_paths.add(code_match.path)

        return [path for path in paths if path in matching_paths]

    def print_json(self) -> None:
        """Print matches as JSON for other tools to read (see schemas.py)."""
        output = matches_schema(matches=self.matches, all_paths=self.all_files)
        click.echo(json.dumps(output, indent=2))

    def print_by_scope(self, scope_filter: tuple[str, ...] | None = None) -> None:
        """Print matches organized by scope."""
        printed_any = False

        # Filter scopes if a filter is provided
        scopes_to_show = sorted(self.matches.scopes.keys())
        if scope_filter:
            scopes_to_show = [s for s in scopes_to_show if s in scope_filter]
            if not scopes_to_show:
                click.echo(f"No scopes found matching: {', '.join(scope_filter)}")
                return

        for scope_name in scopes_to_show:
            paths_for_scope = self._get_paths_for_scope(scope_name)
            code_only_files = (
                self._get_code_only_files_for_scope(scope_name)
                if not paths_for_scope
                else []
            )

            if paths_for_scope or code_only_files:
                printed_any = True
                # Use the scope's color for the header, and its printed name --
                # the badges below spell it with the ownership marker, so the
                # header has to as well.
                scope = self.matches.scopes.get(scope_name)
                if scope:
                    color = get_color_for_name(scope_name)
                    click.secho(f"\n{scope.printed_name()}", bold=True, fg=color)
                else:
                    click.secho(f"\n{scope_name}", bold=True, fg="cyan")
                # Combine path matches and code-only files
                all_files_for_scope = paths_for_scope + code_only_files

                # Sort and print paths
                for path in sorted(all_files_for_scope):
                    # Always show the current scope badge
                    badges = []
                    badges.append(print_scope_badge(scope_name, self.matches.scopes))

                    # Show if file belongs to OTHER scopes too
                    if path in self.matches.paths:
                        path_match = self.matches.paths[path]
                        other_scopes = [s for s in path_match.scopes if s != scope_name]
                        if other_scopes:
                            badges.append(click.style("(also: ", dim=True))
                            for other_scope in sorted(other_scopes):
                                badges.append(
                                    print_scope_badge(other_scope, self.matches.scopes)
                                )
                            badges.append(click.style(")", dim=True))

                    line = path + " " + "".join(badges)
                    click.echo(line)

                    # Print code patterns for this file if any
                    code_patterns = self._get_file_code_patterns_simple_for_scope(
                        path, scope_name
                    )
                    for pattern_line in code_patterns:
                        click.echo("  " + pattern_line)

        if not printed_any:
            click.echo("No scopes found with matching files.")

    def _get_paths_for_scope(self, scope_name: str) -> list[str]:
        """Get all paths that match a specific scope."""
        paths = []
        for path, path_match in self.matches.paths.items():
            if scope_name in path_match.scopes:
                paths.append(path)
        return paths

    def _get_code_only_files_for_scope(self, scope_name: str) -> list[str]:
        """Get files that only match this scope via code patterns, not paths."""
        code_files = set()
        for code_match in self.matches.code.values():
            if scope_name in code_match.scopes:
                code_files.add(code_match.path)

        # Remove files that already match via paths
        path_files = set(self._get_paths_for_scope(scope_name))
        return sorted(code_files - path_files)

    def _get_file_code_patterns_simple(self, path: str) -> list[str]:
        """Get code pattern lines for a file by its full path."""
        code_patterns = []
        for code_match in self.matches.code.values():
            if code_match.path == path:
                location = f"line {code_match.start_line}"
                if code_match.start_line != code_match.end_line:
                    location += f"-{code_match.end_line}"

                badges = []
                for scope_name in code_match.scopes:
                    badges.append(print_scope_badge(scope_name, self.matches.scopes))

                code_patterns.append(
                    (code_match.start_line, f"{location} " + " ".join(badges))
                )

        # Sort by line number and return just the strings
        return [pattern[1] for pattern in sorted(code_patterns, key=lambda x: x[0])]

    def _get_file_code_patterns_simple_for_scope(
        self, path: str, scope_name: str
    ) -> list[str]:
        """Get code pattern lines for a file filtered by a specific scope."""
        code_patterns = []
        for code_match in self.matches.code.values():
            if code_match.path == path and scope_name in code_match.scopes:
                location = f"line {code_match.start_line}"
                if code_match.start_line != code_match.end_line:
                    location += f"-{code_match.end_line}"

                badges = []
                # Always show the current scope first
                badges.append(print_scope_badge(scope_name, self.matches.scopes))

                # Show other scopes if any
                other_scopes = [s for s in code_match.scopes if s != scope_name]
                if other_scopes:
                    badges.append(click.style("(also: ", dim=True))
                    for other_scope in sorted(other_scopes):
                        badges.append(
                            print_scope_badge(other_scope, self.matches.scopes)
                        )
                    badges.append(click.style(")", dim=True))

                code_patterns.append(
                    (code_match.start_line, f"{location} " + "".join(badges))
                )

        # Sort by line number and return just the strings
        return [pattern[1] for pattern in sorted(code_patterns, key=lambda x: x[0])]
