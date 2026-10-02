import os
import re

from kacl.version import KACLVersion


def extract_issue_ids(
    version: KACLVersion,
    search_patterns: dict[str : list[str]] = {"jira": [r"[A-Z]+-[0-9]+"]},
) -> dict[str : list[str]]:
    """
    Extract JIRA IDs from a version object.

    Args:
        version (KACLVersion): The version object to extract JIRA IDs from.
        search_patterns (list[str], optional): A list of search patterns to use. Defaults to ["[A-Z]+-[0-9]+"].

    Returns:
        list[str]: A list of JIRA IDs.
    """
    issue_ids = {}
    for key in search_patterns.keys():
        ids = []
        for pattern in search_patterns[key]:
            ids.extend(re.findall(pattern, (version.body())))
        issue_ids[key] = list(set(ids))
    return issue_ids


def replace_env_variables(text):
    """
    Parses a given text and replaces occurrences of {env.VAR} with the value of the environment
    variable VAR if it exists, or with an empty string if it does not.

    Args:
        text (str): The text to parse and replace environment variables in.

    Returns:
        str: The text with environment variables replaced.
    """
    # Regular expression to find {env.VAR} patterns
    pattern = re.compile(r"\{env\.([A-Za-z_][A-Za-z0-9_]*)\}")

    # Function to replace each match
    def replace_match(match):
        # Extract the environment variable name from the match
        env_var = match.group(1)
        # Return the environment variable's value if it exists, else return an empty string
        return os.getenv(env_var, "")

    # Replace all occurrences of the pattern in the text
    return pattern.sub(replace_match, text)


def convert_markdown_to_jira(markdown_text):
    # Convert markdown headings to JIRA headings
    def replace_heading(match):
        heading_level = len(match.group(1))
        return f"h{heading_level}. {match.group(2)}"

    # Convert markdown links to JIRA links
    def replace_link(match):
        link_text = match.group(1)
        url = match.group(2)
        return f"[{link_text}|{url}]"

    # Convert markdown inline code to JIRA inline code
    def replace_inline_code(match):
        code_text = match.group(1)
        return "{{" + code_text + "}}"

    # Convert markdown bold text to JIRA bold text
    def replace_bold_text(match):
        bold_text = match.group(1)
        return f"*{bold_text}*"

    converted_text = re.sub(
        r"^(#{1,6})\s+(.*)", replace_heading, markdown_text, flags=re.MULTILINE
    )
    converted_text = re.sub(r"\[(.*?)\]\((.*?)\)", replace_link, converted_text)

    # Apply the inline code conversion
    converted_text = re.sub(r"`(.*?)`", replace_inline_code, converted_text)

    # Apply the bold text conversion
    converted_text = re.sub(r"\*\*(.*?)\*\*", replace_bold_text, converted_text)

    return converted_text
