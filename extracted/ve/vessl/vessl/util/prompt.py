from typing import List, Any, Callable

import click
import inquirer

from vessl.util.echo import style_prompt


def prompt_confirm(text: str, default: bool = False) -> bool:
    """Prompt confirmation"""
    key = "question"
    inquiry = inquirer.Confirm(key, message=style_prompt(text), default=default)
    return inquirer.prompt([inquiry], raise_keyboard_interrupt=True).get(key)


def prompt_text(text: str, default: str = None) -> str:
    """Prompt text"""
    key = "question"
    inquiry = inquirer.Text(key, message=style_prompt(text), default=default)
    return inquirer.prompt([inquiry], raise_keyboard_interrupt=True).get(key)


def prompt_choices(text: str, choices: List[Any], default: Any = None) -> Any:
    """Prompt choices

    Args:
        choices (list): A list of choices to display, or a list of 2-tuples where
                        the first element is the choice to display and the second
                        element is return value.
    """
    key = "question"
    inquiry = inquirer.List(key, message=style_prompt(text), default=default, choices=choices)
    return inquirer.prompt([inquiry], raise_keyboard_interrupt=True).get(key)


def prompt_checkbox(text: str, choices: List[Any], default: Any = None) -> Any:
    key = "question"
    inquiry = inquirer.Checkbox(key, message=style_prompt(text), default=default, choices=choices)
    return inquirer.prompt([inquiry], raise_keyboard_interrupt=True).get(key)


def generic_prompter(text: str, type: click.ParamType = click.STRING, default=None) -> Callable:
    def prompter(ctx: click.Context, param: click.Parameter, value: str):
        return click.prompt(style_prompt(text), type=type, default=default)

    return prompter


def choices_prompter(text: str, choices: List[Any], default: Any = None) -> Callable:
    def prompter(ctx: click.Context, param: click.Parameter, value: str):
        return prompt_choices(style_prompt(text), choices, default)

    return prompter
