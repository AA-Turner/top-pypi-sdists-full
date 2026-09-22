from docutils import nodes

from sphinx.application import Sphinx
from sphinx.roles import ReferenceRole
from sphinx.util.typing import ExtensionMetadata


# GitLab renamed issues to work items, and both /-/issues/<n> and /-/work_items/<n> serve an
# existing issue.  They part company on one that does not exist: /-/issues/ answers 404, while
# /-/work_items/ answers 200 with a JavaScript shell for any number at all, including 99999.  Only
# the first of those can be checked, and `hatch run docs:linkcheck` is the whole reason to care --
# pointed at /-/work_items/ it fetched every link here and could never fail on one, which is how a
# reference to a nonexistent GL#32 survived in NEWS.rst.
ISSUE_URL = 'https://gitlab.com/flufl/public/-/issues/'

# Merge requests are numbered separately from issues, so !32 and GL#32 are different things and
# only one of them may exist.  This route 404s properly too.
MERGE_REQUEST_URL = 'https://gitlab.com/flufl/public/-/merge_requests/'


class GitLabRole(ReferenceRole):
    """Base class for the roles that hyperlink a numbered GitLab reference.

    A subclass supplies the route to build the URL from and the sigil its default link text
    starts with; `role_name` names the role in the error message, so it matches what was typed.
    """

    base_url: str
    sigil: str
    role_name: str

    def run(self) -> tuple[list[nodes.Node], list[nodes.system_message]]:
        try:
            reference_number = int(self.target)
        except ValueError:
            message = self.inliner.reporter.error(
                f'Role target must be an integer :{self.role_name}:{self.target}'
            )
            problem = self.inliner.problematic(self.rawtext, self.rawtext, message)
            return [problem], [message]

        reference_uri = self.base_url + self.target
        title = self.title if self.has_explicit_title else f'{self.sigil}{self.target}'

        return [
            nodes.reference(
                '',
                title,
                # These point at gitlab.com, so they are external references and are marked as
                # such.  The flag does not gate linkcheck -- it checked them either way -- it just
                # decides which of docutils' two classes the writer emits.
                internal=False,
                refuri=reference_uri,
                classes=['issue'],
                _title_tuple=(reference_number,),
            )
        ], []


class IssueRole(GitLabRole):
    """A role to hyperlink GitLab issues.

    Use like this: :GL:`16`
    """

    base_url = ISSUE_URL
    sigil = 'GL#'
    role_name = 'GL'


class MergeRequestRole(GitLabRole):
    """A role to hyperlink GitLab merge requests.

    Use like this: :MR:`32`
    """

    base_url = MERGE_REQUEST_URL
    sigil = '!'
    role_name = 'MR'


def setup(app: Sphinx) -> ExtensionMetadata:
    app.add_role('GL', IssueRole())
    app.add_role('MR', MergeRequestRole())

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
