from __future__ import annotations


def view_response(path: str, numbered_content: str) -> str:
    return f"Here's the result of running `cat -n` on {path}:\n{numbered_content}"


def view_empty_warning() -> str:
    return "<system-reminder>Warning: the file exists but the contents are empty.</system-reminder>"


def create_success(path: str) -> str:
    return f"File created successfully at: {path}"


def edit_success(path: str, numbered_diff_window: str) -> str:
    return (
        f"The file {path} has been edited. Here's the result of running `cat -n` on "
        f"{path}:\n{numbered_diff_window}\nReview the changes and make sure they are as "
        f"expected. Edit the file again if necessary."
    )


def edit_no_match(old_str: str, path: str) -> str:
    return f"No replacement was performed, old_str `{old_str}` did not appear verbatim in {path}."


def edit_multiple_matches(old_str: str, line_numbers: list[int]) -> str:
    return (
        f"No replacement was performed. Multiple occurrences of old_str `{old_str}` in "
        f"lines {line_numbers}. Please ensure it is unique"
    )


def edit_not_found() -> str:
    return "Error: File not found"


def edit_perm_denied() -> str:
    return "Error: Permission denied. Cannot write to file."


def path_not_absolute(path: str, suggested: str) -> str:
    return (
        f"The path {path} is not an absolute path, it should start with `/`. Maybe you "
        f"meant {suggested}?"
    )


def path_is_directory(path: str) -> str:
    return f"The path {path} is a directory and only the `view` command can be used on directories"


def create_file_exists(path: str) -> str:
    return f"File already exists at: {path}. Cannot overwrite files using command `create`."


def edit_string_not_found() -> str:
    return "String to replace not found in file."


def edit_n_matches(n: int) -> str:
    return (
        f"Found {n} matches of the string to replace, but replace_all is false. To "
        f"replace all occurrences, set replace_all to true. To replace only one "
        f"occurrence, please provide more context to uniquely identify the instance."
    )
