from agentic_devtools.cli.ci.reconciliation.status_reporter import sync_status_comment


class Provider:
    def __init__(self, existing=None):
        self.existing = existing
        self.updated = []
        self.posted = []

    def find_comment(self, pr_number, marker):
        return self.existing

    def update_comment(self, comment_id, body):
        self.updated.append((comment_id, body))

    def post_comment(self, pr_number, body):
        self.posted.append((pr_number, body))
        return 99


def test_updates_existing_comment(foundation):
    provider = Provider((7, "old"))
    assert sync_status_comment(provider, foundation().state, 42) == 7
    assert provider.updated[0][0] == 7


def test_creates_missing_comment(foundation):
    provider = Provider()
    assert sync_status_comment(provider, foundation().state, 42) == 99
    assert provider.posted[0][0] == 42
