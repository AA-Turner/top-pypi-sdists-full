from docutils import nodes

from sphinx.application import Sphinx
from sphinx.roles import ReferenceRole
from sphinx.util.typing import ExtensionMetadata


BASE_URL = 'https://gitlab.com/warsaw/public/-/issues/'


class IssueRole(ReferenceRole):
    """A role to hyperlink GitLab issues.

    Use like this: :GL:`16`
    """

    def run(self) -> tuple[list[nodes.Node], list[nodes.system_message]]:
        try:
            issue_number = int(self.target)
        except ValueError:
            message = self.inliner.reporter.error(
                f'Role target must be an integer :GL:{self.target}'
            )
            problem = self.inliner.problematic(self.rawtext, self.rawtext, message)
            return [problem], [message]

        issue_uri = BASE_URL + self.target
        title = self.title if self.has_explicit_title else f'GL#{self.target}'

        return [
            nodes.reference(
                '',
                title,
                internal=True,
                refuri=issue_uri,
                classes=['issue'],
                _title_tuple=(issue_number,),
            )
        ], []


def setup(app: Sphinx) -> ExtensionMetadata:
    app.add_role('GL', IssueRole())

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
