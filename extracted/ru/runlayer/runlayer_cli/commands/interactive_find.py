from collections.abc import Callable, Sequence
from typing import Literal, Protocol, TypeVar

import questionary
import typer

T = TypeVar("T")


class _ChoiceDetail(Protocol):
    name: str
    namespace: str | None
    description: str | None


def cancelled() -> None:
    typer.echo("Cancelled.")
    raise typer.Exit(0)


def format_choice(item: _ChoiceDetail) -> str:
    line = item.name
    if item.namespace:
        line += f"  ({item.namespace})"
    if item.description:
        line += f"  - {item.description}"
    return line


def prompt_items(
    items: Sequence[T],
    *,
    noun: str,
    format_item: Callable[[T], str],
) -> list[T]:
    if not items:
        typer.echo(f"No {noun} available.")
        raise typer.Exit(0)

    selected = questionary.checkbox(
        f"Select {noun} to install:",
        choices=[
            questionary.Choice(title=format_item(item), value=item) for item in items
        ],
        use_search_filter=True,
        use_jk_keys=False,
        instruction="(type to search, space to select)",
    ).ask()
    if not selected:
        cancelled()
    return list(selected)


def prompt_clients(client_names: Sequence[str]) -> list[str]:
    selected = questionary.checkbox(
        "Select clients:",
        choices=[
            questionary.Choice(
                title=client_name.replace("_", " ").title(),
                value=client_name,
                checked=client_name == "claude_code",
            )
            for client_name in sorted(client_names)
        ],
        use_search_filter=True,
        use_jk_keys=False,
        instruction="(type to search, space to select)",
    ).ask()
    if not selected:
        cancelled()
    return [str(client_name) for client_name in selected]


def prompt_scope() -> Literal["project", "global"]:
    selected = questionary.select(
        "Install scope:",
        choices=[
            questionary.Choice(title="Project", value="project"),
            questionary.Choice(title="Global", value="global"),
        ],
        use_jk_keys=False,
        default="project",
    ).ask()
    if selected is None:
        cancelled()
    return selected


def confirm_install(
    *,
    item_count: int,
    client_count: int,
    item_label: str,
) -> None:
    confirmed = questionary.confirm(
        f"Install {item_count} {item_label} to {client_count} client(s)?",
        default=True,
    ).ask()
    if not confirmed:
        cancelled()
