from typing import Any

import click

from vessl import VESSL_ENV


def print_warning(text: str, stderr: bool = True) -> Any:
    click.echo(style_warning(text), err=stderr)


def style_warning(text: str) -> Any:
    return click.style(text, fg="magenta")


def print_debug(text: str, stderr: bool = True) -> Any:
    if VESSL_ENV == "dev":
        click.echo(f"DEBUG>> {style_info(text)}", err=stderr)


def print_info(text: str, stderr: bool = True) -> Any:
    click.echo(style_info(text), err=stderr)


def print_prompt_style(text: str, stderr: bool = True) -> Any:
    """
    Prints prompt style text not a prompt itself. Use for multi-line explanations on a prompt.
    """
    click.echo(style_prompt(text), err=stderr)


def print_success(text: str, stderr: bool = True) -> Any:
    click.echo(style_success(text), err=stderr)


def print_success_result(text: str, stderr: bool = True) -> Any:
    click.echo(style_success_result(text), err=stderr)


def print_error(text: str, stderr: bool = True) -> Any:
    click.echo(style_error(text), err=stderr)


def print_error_result(text: str, stderr: bool = True) -> Any:
    click.echo(style_error_result(text), err=stderr)


def style_info(text: str) -> Any:
    return click.style(text, fg="cyan")


def style_prompt(text: str) -> Any:
    return click.style(text, fg="yellow")


def style_error(text: str) -> Any:
    return click.style(text, fg="red")


def style_success(text: str) -> Any:
    return click.style(text, fg="green")


def style_success_result(text: str) -> Any:
    return click.style(text, bg="green")


def style_error_result(text: str) -> Any:
    return click.style(text, bg="red", fg="white")
