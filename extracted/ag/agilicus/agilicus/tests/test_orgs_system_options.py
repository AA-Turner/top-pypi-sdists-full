"""``update-system-options`` allowed-domain semantics (IAF-2383).

The atomic domain change requires the new domain in the organisation's
``system_options.allowed_domains`` before it runs. ``--allowed-domains`` is a
repeatable option, so an empty value means the caller did not pass it (click
cannot express zero values): it must leave the stored list untouched instead
of wiping it, and ``--add-allowed-domain`` must append without duplicating.
"""

from types import SimpleNamespace

from agilicus import orgs


class FakeSystemOptions:
    def __init__(self, allowed_domains):
        self.allowed_domains = allowed_domains
        self.license_constraints = []
        self.constraint_variables = None


class FakeResult:
    def __init__(self, options):
        self.options = options

    def to_dict(self):
        return {"allowed_domains": list(self.options.allowed_domains)}


class FakeOrgApi:
    def __init__(self, options):
        self.options = options
        self.calls = []

    def replace_system_options(self, **kwargs):
        self.calls.append(kwargs)
        return FakeResult(self.options)


def _patch(monkeypatch, allowed_domains):
    options = FakeSystemOptions(allowed_domains)
    org_api = FakeOrgApi(options)
    monkeypatch.setattr(orgs, "get_system_options", lambda ctx, org_id: options)
    monkeypatch.setattr(
        orgs.context,
        "get_apiclient",
        lambda ctx: SimpleNamespace(org_api=org_api),
    )
    return options, org_api


def test_absent_allowed_domains_leaves_the_stored_list(monkeypatch):
    options, org_api = _patch(monkeypatch, ["old.example.com"])

    orgs.replace_system_options(None, "org-1")

    assert options.allowed_domains == ["old.example.com"]
    assert org_api.calls[0]["org_id"] == "org-1"


def test_allowed_domains_replaces_the_stored_list(monkeypatch):
    options, _ = _patch(monkeypatch, ["old.example.com"])

    orgs.replace_system_options(
        None, "org-1", allowed_domains=("a.example.com", "b.example.com")
    )

    assert options.allowed_domains == ["a.example.com", "b.example.com"]


def test_add_allowed_domain_appends_without_duplicating(monkeypatch):
    options, _ = _patch(monkeypatch, ["old.example.com"])

    orgs.replace_system_options(
        None, "org-1", add_allowed_domains=("new.example.com", "old.example.com")
    )

    assert options.allowed_domains == ["old.example.com", "new.example.com"]
