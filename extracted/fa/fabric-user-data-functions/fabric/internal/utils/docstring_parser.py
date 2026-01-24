from typing import Optional


def extract_summary_description(docstring: str) -> tuple[Optional[str], Optional[str]]:
    """
    Retrieves the Summary and Description from a multiline comment string.

    Args:
        docstring: A multiline string containing Summary and Description.

    Returns:
        A tuple containing two strings: (summary, description).
        If Summary or Description is not found, the corresponding value will be None.
    """
    summary_lines = []
    description_lines = []
    in_summary = False
    in_description = False

    # Proceed if docstring is not None
    if docstring is None:
        return None, None
    for line in docstring.splitlines():
        stripped_line = line.strip()

        if stripped_line.startswith("Summary:"):
            in_summary = True
            in_description = False
            summary_lines.append(stripped_line[len("Summary:"):].strip())
        elif stripped_line.startswith("Description:"):
            in_summary = False
            in_description = True
            description_lines.append(stripped_line[len("Description:"):].strip())
        elif in_summary:
            summary_lines.append(stripped_line)
        elif in_description:
            description_lines.append(stripped_line)

    summary = None
    if summary_lines:
        summary = "\n".join(summary_lines).strip()
    description = None
    if description_lines:
        description = "\n".join(description_lines).strip()
    return summary, description
