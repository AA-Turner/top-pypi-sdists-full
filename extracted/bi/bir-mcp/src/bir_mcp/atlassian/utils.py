import re


def infer_jira_field_representation(
    value, dict_key_preference=("displayName", "name", "value", "key")
):
    def recursive_infer(value):
        match value:
            case list():
                value = [recursive_infer(i) for i in value]
            case dict():
                for key in dict_key_preference:
                    if key in value:
                        value = value[key]
                        value = recursive_infer(value)
                        return value

        return value

    value = recursive_infer(value)
    return value


def generate_directed_linked_issues(issue_fields: dict):
    for issue_link in issue_fields["issuelinks"]:
        for direction in ["inward", "outward"]:
            if linked_issue := issue_link.get(f"{direction}Issue"):
                directed_link = issue_link["type"][direction]
                yield directed_link, linked_issue


def normalize_line_breaks(string: str) -> str:
    string = re.sub(r"[^\S\n]+", " ", string)  # Replace non-newline whitespaces with single space.
    string = re.sub(r"\s*\n\s*", "\n", string)  # Replace multiple newlines with single newline.
    string = string.strip()
    return string


def collect_jira_issue_keys_in_text(text: str) -> list[str]:
    issue_keys = re.findall(r"[a-zA-Z]+-\d+", text)
    issue_keys = sorted({i.upper() for i in issue_keys})
    return issue_keys


def confluence_highlight_to_markdown_bold(text: str) -> str:
    pattern = r"@@@hl@@@(.*?)@@@endhl@@@"
    text = re.sub(pattern, r"**\1**", text, flags=re.DOTALL)
    return text
