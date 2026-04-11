from pathlib import Path
from typing import List

import html5lib

from abstra_internals.repositories.linter.models import LinterIssue, LinterRule
from abstra_internals.services.fs import FileSystemService
from abstra_internals.settings import Settings


class HtmlSyntaxErrorFound(LinterIssue):
    def __init__(self, error_message: str, file_path: Path):
        self.label = f"HTML error in {file_path.name}: {error_message}"
        self.fixes = []


# parse() expects a full document with <!DOCTYPE html>. Since user HTML files
# may be fragments or simply omit the doctype, we ignore these errors.
IGNORED_ERRORS = {
    "expected-doctype-but-got-start-tag",
    "expected-doctype-but-got-chars",
    "expected-doctype-but-got-eof",
}


class HtmlSyntax(LinterRule):
    label = "HTML syntax errors"
    type = "bug"
    fix_with_ai = True

    def find_issues(self) -> List[LinterIssue]:
        issues = []
        root = Settings.root_path

        for html_file in FileSystemService.list_files(root, allowed_suffixes=[".html"]):
            try:
                content = html_file.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue

            parser = html5lib.HTMLParser()
            parser.parse(content)

            for (line, col), error_code, details in parser.errors:
                if error_code in IGNORED_ERRORS:
                    continue
                msg = f"{error_code} at line {line}, col {col}"
                if details:
                    msg += f" ({', '.join(f'{k}={v}' for k, v in details.items())})"
                issues.append(HtmlSyntaxErrorFound(msg, html_file))

        return issues
