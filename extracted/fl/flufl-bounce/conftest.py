import email

from doctest import ELLIPSIS, NORMALIZE_WHITESPACE, REPORT_NDIFF
from sybil import Sybil
from sybil.parsers.codeblock import PythonCodeBlockParser
from sybil.parsers.doctest import DocTestParser


DOCTEST_FLAGS = ELLIPSIS | NORMALIZE_WHITESPACE | REPORT_NDIFF


def print_emails(recipients):
    if recipients is None:
        print('None')
        return
    if len(recipients) == 0:
        print('No addresses')
    for email in sorted(recipients):
        # Remove the extraneous b'' prefixes.
        email = repr(email)[2:-1]
        print(email)


class DoctestNamespace:
    def setup(self, namespace):
        namespace['parse'] = email.message_from_bytes
        namespace['print_emails'] = print_emails


namespace = DoctestNamespace()


pytest_collect_file = Sybil(
    parsers=[
        DocTestParser(optionflags=DOCTEST_FLAGS),
        PythonCodeBlockParser(),
    ],
    pattern='*.rst',
    setup=namespace.setup,
).pytest()
