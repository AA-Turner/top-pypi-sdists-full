from yamloom.actions.types import Ostrlike
from collections.abc import Sequence


def validate_choice(
    option_name: str, option_value: Ostrlike, choices: Sequence[str]
) -> Ostrlike:
    if option_value is not None:
        if isinstance(option_value, str):
            lowered = option_value.lower()
            if option_value not in choices:
                quoted_choices = [f"'{c}'" for c in choices]
                if len(choices) > 2:
                    choices_str = (
                        f'{", ".join(quoted_choices[:-1])}, or {quoted_choices[-1]}'
                    )
                else:
                    choices_str = ' or '.join(quoted_choices)
                msg = f"'{option_name}' must be {choices_str}"
                raise ValueError(msg)
            return lowered
        else:
            return option_value
    else:
        return None


def check_string(s: object | None) -> str | None:
    if isinstance(s, str):
        if '${{' not in s:
            return s
    return None
