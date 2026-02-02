from collections.abc import Callable, Sequence
from gettext import gettext
from typing import Any

import click
import questionary

from exponent.core.types.generated.strategy_info import StrategyInfo


class AutoCompleteOption(click.Option):
    prompt: str

    def __init__(
        self,
        param_decls: Sequence[str] | None = None,
        prompt: bool | str = True,
        choices: list[str] | None = None,
        **kwargs: Any,
    ):
        super().__init__(param_decls, prompt=prompt, **kwargs)
        if isinstance(self.type, click.Choice):
            self.choices = self.type.choices
        else:
            self.choices = choices or []

    def prompt_for_value(self, ctx: click.core.Context) -> Any:
        choices_list: list[str] = [str(c) for c in self.choices]
        return questionary.autocomplete(
            self.prompt,
            choices_list,
            style=questionary.Style(
                [
                    ("question", "bold"),  # question text
                    (
                        "answer",
                        "fg:#33ccff bold",
                    ),  # submitted answer text behind the question
                    (
                        "answer",
                        "bg:#000066",
                    ),  # submitted answer text behind the question
                ]
            ),
        ).unsafe_ask()


class StrategyChoice(click.Choice[str]):
    def __init__(self, choices: Sequence[StrategyInfo]) -> None:
        self.strategy_choices = choices
        self.choices = [strategy.strategy_name.value for strategy in choices]
        self.case_sensitive = True


class StrategyOption(AutoCompleteOption):
    def __init__(self, *args: Any, type: StrategyChoice, **kwargs: Any):
        super().__init__(*args, type=type, **kwargs)
        self.default = self.default_choice(type.strategy_choices)
        self.strategy_choices = type.strategy_choices

    def _format_strategy_info(
        self, strategy_info: StrategyInfo, formatter: click.HelpFormatter
    ) -> None:
        row = (strategy_info.strategy_name.value, strategy_info.display_name)
        formatter.write_dl([row])
        with formatter.indentation():
            formatter.write_text(strategy_info.description)

    def help_extra_hook(self, formatter: click.HelpFormatter) -> None:
        with formatter.section("Strategies"):
            for strategy_info in self.strategy_choices:
                formatter.write_paragraph()
                self._format_strategy_info(strategy_info, formatter)

    @staticmethod
    def default_choice(choices: Sequence[StrategyInfo]) -> str:
        return min(choices, key=lambda x: x.display_order).strategy_name.value


class ExponentCommand(click.Command):
    def format_options(
        self, ctx: click.Context, formatter: click.HelpFormatter
    ) -> None:
        """Writes all the options into the formatter if they exist."""
        opts = []
        for param in self.get_params(ctx):
            rv = param.get_help_record(ctx)
            hook = getattr(param, "help_extra_hook", None)
            if rv is not None:
                opts.append((rv, hook))

        if not opts:
            return

        with formatter.section(gettext("Options")):
            for opt, hook in opts:
                formatter.write_dl([opt])
                if hook is not None:
                    hook(formatter)
                    formatter.write_paragraph()


class ExponentGroup(click.Group):
    command_class = ExponentCommand
    group_class = type


def exponent_cli_group(
    name: str | None = None,
    **attrs: Any,
) -> Callable[[Callable[..., Any]], ExponentGroup]:
    return click.command(name, ExponentGroup, **attrs)
