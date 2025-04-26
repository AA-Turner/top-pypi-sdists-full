from typing import Any, List

import click

TAB_SIZE = 2


def format_key(key: str) -> str:
    return click.style(key, fg="green")


def format_data(data: Any, depth: int) -> List[str]:
    indent = " " * (TAB_SIZE * depth + 1)

    if not isinstance(data, dict):
        # `data` is primitive type
        return [f"{indent}{data}"]

    lines = []
    for key, value in data.items():
        if isinstance(value, dict):
            lines.append(f"{indent}{format_key(key)}")
            lines.extend(format_data(value, depth + 1))
        elif isinstance(value, list):
            lines.append(f"{indent}{format_key(key)}")
            for x in value:
                # TODO: find a more elegant way. Perhaps yaml library?
                additional_lines = format_data(x, depth + 1)
                additional_lines[0] = additional_lines[0].lstrip()
                additional_lines[0] = f"{indent}- {additional_lines[0]}"
                lines.extend(additional_lines)
        else:
            lines.append(f"{indent}{format_key(key)} {value}")
    return lines


def format_size(value: int, suffix="B") -> str:
    if value == 0:
        return "0 B"

    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if abs(value) < 1024.0:
            return f"{value:.1f} {unit}{suffix}"
        value /= 1024.0
    return f"{value:.1f} Yi{suffix}"


def format_bool(value: bool, true_value: str = "Y", false_value: str = "N") -> str:
    return true_value if value else false_value


def format_string(value: str, null_value: str = "None", empty_value: str = "-") -> str:
    if value is None:
        return null_value
    if not value:
        return empty_value
    return value


def format_url(url: str) -> str:
    """Prints in url format

    Replace whitespaces with %20. More url rules could be added.
    """
    return url.replace(" ", "%20")


def sizeof_fmt(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"
