import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Any, cast

import click
import questionary

from exponent.commands.common import redirect_to_login, run_until_complete
from exponent.commands.settings import use_settings
from exponent.commands.types import exponent_cli_group
from exponent.core.config import Settings
from exponent.core.graphql.client import GraphQLClient
from exponent.core.graphql.generated_client.chats import (
    ChatsChatsChats,
    ChatsChatsChatsChats,
    ChatsChatsChatsChatsPrStatusPRInfo,
    ChatsChatsUnauthenticatedError,
)
from exponent.core.graphql.generated_client.enums import PRStatus


@exponent_cli_group()
def checkout_cli() -> None:
    """Checkout commands for syncing cloud changes to local."""
    pass


async def fetch_chats(
    api_key: str,
    base_api_url: str,
    base_ws_url: str,
) -> list[ChatsChatsChatsChats]:
    graphql_client = GraphQLClient(api_key, base_api_url, base_ws_url)
    result = await graphql_client.get_chats()

    if isinstance(result.chats, ChatsChatsUnauthenticatedError):
        click.secho(f"Error: {result.chats.message}", fg="red")
        sys.exit(1)

    if isinstance(result.chats, ChatsChatsChats):
        return result.chats.chats

    click.secho("Unexpected response from server", fg="red")
    sys.exit(1)


def sort_chats_by_recency(
    chats: list[ChatsChatsChatsChats],
) -> list[ChatsChatsChatsChats]:
    def parse_updated_at(chat: ChatsChatsChatsChats) -> datetime:
        updated_at = chat.updated_at
        if updated_at is None:
            return datetime.min
        if isinstance(updated_at, datetime):
            return updated_at
        try:
            return datetime.fromisoformat(str(updated_at).replace("Z", "+00:00"))
        except (ValueError, TypeError):
            return datetime.min

    return sorted(chats, key=parse_updated_at, reverse=True)


@dataclass
class PRChoice:
    chat: ChatsChatsChatsChats
    pr_number: int
    pr_title: str


def get_all_open_prs(chat: ChatsChatsChatsChats) -> list[tuple[int, str]]:
    return [
        (pr.number, pr.title)
        for pr in chat.pr_status
        if isinstance(pr, ChatsChatsChatsChatsPrStatusPRInfo)
        and pr.status == PRStatus.OPEN
    ]


def collect_all_pr_choices(chats: list[ChatsChatsChatsChats]) -> list[PRChoice]:
    choices: list[PRChoice] = []
    for chat in chats:
        for pr_number, pr_title in get_all_open_prs(chat):
            choices.append(PRChoice(chat=chat, pr_number=pr_number, pr_title=pr_title))
    return choices


def format_pr_choice(pr_choice: PRChoice) -> dict[str, Any]:
    display = f"#{pr_choice.pr_number} {pr_choice.pr_title}"
    return {"name": display, "value": pr_choice}


def check_gh_installed() -> None:
    if shutil.which("gh") is None:
        click.secho("Error: GitHub CLI (gh) is not installed.", fg="red")
        click.echo("Please install it from: https://cli.github.com/")
        sys.exit(1)


MAX_PRS_TO_SHOW = 20
DEFAULT_POLL_INTERVAL = 3


def select_pr_interactive(pr_choices: list[PRChoice]) -> PRChoice:
    if not pr_choices:
        click.secho("No open PRs found.", fg="yellow")
        sys.exit(1)

    if len(pr_choices) == 1:
        selected = pr_choices[0]
        click.secho(f"Using PR: #{selected.pr_number} {selected.pr_title}", fg="cyan")
        return selected

    prs_to_show = pr_choices[:MAX_PRS_TO_SHOW]
    choices = [format_pr_choice(pr) for pr in prs_to_show]

    selected = questionary.select(
        "Select a PR to checkout:",
        choices=choices,
        style=questionary.Style(
            [
                ("question", "bold"),
                ("pointer", "fg:#33ccff bold"),
                ("highlighted", "fg:#33ccff"),
            ]
        ),
    ).ask()

    if selected is None:
        click.secho("\nCancelled", fg="yellow")
        sys.exit(0)

    return cast(PRChoice, selected)


def find_prs_by_chat_id(pr_choices: list[PRChoice], chat_id: str) -> list[PRChoice]:
    return [pr for pr in pr_choices if chat_id in {pr.chat.chat_uuid, pr.chat.id}]


def get_local_head() -> str | None:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0:
        return result.stdout.strip()
    return None


def get_current_branch() -> str | None:
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0:
        return result.stdout.strip()
    return None


def get_pr_branch(pr_number: int) -> str | None:
    result = subprocess.run(
        [
            "gh",
            "pr",
            "view",
            str(pr_number),
            "--json",
            "headRefName",
            "--jq",
            ".headRefName",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0:
        return result.stdout.strip()
    return None


def get_remote_head(pr_number: int) -> str | None:
    result = subprocess.run(
        [
            "gh",
            "pr",
            "view",
            str(pr_number),
            "--json",
            "headRefOid",
            "--jq",
            ".headRefOid",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0:
        return result.stdout.strip()
    return None


def get_uncommitted_files() -> list[str]:
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0 and result.stdout.strip():
        return [line[3:] for line in result.stdout.strip().split("\n") if line]
    return []


def get_local_commits_on_pr_branch(pr_number: int) -> list[str]:
    current_branch = get_current_branch()
    pr_branch = get_pr_branch(pr_number)
    if current_branch != pr_branch:
        return []
    remote_head = get_remote_head(pr_number)
    if not remote_head:
        return []
    result = subprocess.run(
        ["git", "log", f"{remote_head}..HEAD", "--oneline"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0 and result.stdout.strip():
        return result.stdout.strip().split("\n")
    return []


def force_checkout_pr(pr_number: int) -> bool:
    result = subprocess.run(
        ["gh", "pr", "checkout", str(pr_number), "--force"],
        check=False,
    )
    return result.returncode == 0


def show_local_changes_and_confirm(pr_number: int) -> bool:
    uncommitted = get_uncommitted_files()
    local_commits = get_local_commits_on_pr_branch(pr_number)

    if not uncommitted and not local_commits:
        return True

    click.secho("\nLocal changes would be lost:", fg="yellow")

    if uncommitted:
        click.echo("\nUncommitted files:")
        for f in uncommitted[:10]:
            click.echo(f"  {f}")
        if len(uncommitted) > 10:
            click.echo(f"  ... and {len(uncommitted) - 10} more")

    if local_commits:
        click.echo("\nLocal commits:")
        for c in local_commits[:10]:
            click.echo(f"  {c}")
        if len(local_commits) > 10:
            click.echo(f"  ... and {len(local_commits) - 10} more")

    return click.confirm("\nForce checkout and discard these changes?")


def live_sync_pr(pr_number: int, poll_interval: int) -> None:
    last_local_head = get_local_head()
    click.echo(
        f"\nLive syncing PR #{pr_number} (polling every {poll_interval}s, Ctrl+C to stop)..."
    )
    click.echo("Will exit if local changes are detected.\n")

    try:
        while True:
            time.sleep(poll_interval)

            uncommitted = get_uncommitted_files()
            if uncommitted:
                click.secho(
                    f"\nLocal changes detected ({len(uncommitted)} files), stopping live sync",
                    fg="yellow",
                )
                break

            current_local_head = get_local_head()
            if current_local_head != last_local_head:
                click.secho("\nLocal commits detected, stopping live sync", fg="yellow")
                break

            remote_head = get_remote_head(pr_number)
            if remote_head is None:
                click.secho(
                    "Could not fetch remote head, PR may be closed", fg="yellow"
                )
                break

            if current_local_head != remote_head:
                click.echo(f"New commits detected ({remote_head[:7]}), syncing...")
                if force_checkout_pr(pr_number):
                    last_local_head = get_local_head()
                    click.secho("Synced successfully", fg="green")
                else:
                    click.secho("Sync failed", fg="red")
                    break
    except KeyboardInterrupt:
        click.echo("\nStopped live sync")


@checkout_cli.command(hidden=True)
@click.argument("chat_id", required=False)
@click.option(
    "-l",
    "--live",
    is_flag=True,
    help="Live mode: keep syncing with remote until local changes are detected",
)
@click.option(
    "--poll-interval",
    default=DEFAULT_POLL_INTERVAL,
    help="Seconds between polls in live mode",
)
@use_settings
def checkout(
    settings: Settings,
    chat_id: str | None = None,
    live: bool = False,
    poll_interval: int = DEFAULT_POLL_INTERVAL,
) -> None:
    """Checkout a PR from a cloud chat locally.

    If CHAT_ID is provided, shows PRs for that specific chat.
    Otherwise, presents an interactive selector of all open PRs.
    """
    if not settings.api_key:
        redirect_to_login(settings)
        return

    api_key = settings.api_key
    base_api_url = settings.get_base_api_url()
    base_ws_url = settings.get_base_ws_url()

    chats = run_until_complete(fetch_chats(api_key, base_api_url, base_ws_url))

    sorted_chats = sort_chats_by_recency(chats)
    all_pr_choices = collect_all_pr_choices(sorted_chats)

    if not all_pr_choices:
        click.secho("No chats with open PRs found.", fg="yellow")
        sys.exit(1)

    if chat_id:
        matching_prs = find_prs_by_chat_id(all_pr_choices, chat_id)
        if not matching_prs:
            click.secho(f"No open PRs found for chat: {chat_id}", fg="red")
            sys.exit(1)
        selected_pr = select_pr_interactive(matching_prs)
    else:
        selected_pr = select_pr_interactive(all_pr_choices)

    check_gh_installed()
    pr_number = selected_pr.pr_number
    pr_title = selected_pr.pr_title
    chat_url = f"{settings.base_url}/chats/{selected_pr.chat.chat_uuid}"
    click.secho(f"\nSelected: #{pr_number} {pr_title}", fg="green")
    click.echo(f"Chat: {chat_url}")

    if not show_local_changes_and_confirm(pr_number):
        click.echo("Cancelled")
        sys.exit(0)

    click.echo(f"\nChecking out PR #{pr_number}...")
    if not force_checkout_pr(pr_number):
        click.secho("Checkout failed", fg="red")
        sys.exit(1)

    click.secho("Checkout successful", fg="green")

    if live:
        live_sync_pr(pr_number, poll_interval)
