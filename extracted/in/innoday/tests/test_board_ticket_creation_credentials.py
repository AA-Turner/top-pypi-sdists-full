"""#525 phase 3: ticket creation resolves a board credential from Vault, only.

``BoardTicketCreationService`` kept a pre-Vault fallback that
``BoardSyncService`` never had: when no per-board credential was stored it asked
``CredentialProvider`` for ``~/.innoday/config.json`` + OS-keyring credentials,
and it also injected that lookup into the shared adapter factory as
``legacy_credentials``. Both were deliberate local-dev conveniences, not defects
-- and both are the thing phase 3 deletes, so that *creating* a ticket on a board
resolves its credential exactly the way *syncing* it already does.

Two properties are pinned here, and they fail for different reasons:

1. **The seam is gone.** No ``credential_provider`` on the service, no
   ``legacy_credentials`` parameter on ``build_board_adapter``. A future
   convenience fallback has to re-add a named thing, which review will see.
2. **Nothing but the board's own credential can reach an adapter.** A stored
   keyring credential is ignored, including one whose payload is a GitHub PAT
   rather than a Trello key. That second case is #554's shape -- there, a
   process-env GitHub PAT reached ``TrelloAPI``, which puts its credentials in
   the query string, so the operator's token landed in api.trello.com's request
   logs. The lesson generalises past the one env var that caused it: a board
   adapter must only ever be handed a credential resolved *for that board*.
"""

import inspect

import pytest

from src.domain.board import BoardType
from src.services import board_adapter_factory as factory
from src.services import board_ticket_creation_service as bt
from src.services.board_ticket_creation_service import BoardTicketCreationService

# Distinguishable on sight, so an assertion failure says which store won rather
# than just "tokens differ".
VAULT_API_KEY = "vault-trello-api-key"
VAULT_TOKEN = "vault-trello-token"
KEYRING_API_KEY = "keyring-trello-api-key"
KEYRING_TOKEN = "keyring-trello-token"
GITHUB_TOKEN = "ghp-org-github-token-must-never-reach-a-board"


class _RecordingTrelloAPI:
    """Stands in for TrelloAPI and records exactly what it was constructed with.

    Asserting on this rather than on "no exception was raised" is the point:
    the #554 bug raised nothing at all -- it succeeded, against the wrong
    account, with the credential in a URL.
    """

    constructed = []

    def __init__(self, api_key, token, base_url="https://api.trello.com/1"):
        type(self).constructed.append((api_key, token))
        self.api_key = api_key
        self.token = token


class _FakeProvider:
    """A CredentialProvider that *does* have a credential, and records asks.

    The legacy path only ever returned something on a developer's own machine,
    so a test that merely runs where ~/.innoday is empty cannot tell "we removed
    the fallback" from "the fallback found nothing". This makes the store
    non-empty, so silence is meaningful.
    """

    def __init__(self, credentials=None):
        self.asked = []
        # Default: a plausible per-service local entry. Override to model a
        # mis-scoped one -- e.g. a GitHub PAT filed under the org's alias, whose
        # `token` key is also Trello's, so the old fallback joined it straight in.
        self._credentials = credentials

    def get_integration_credentials(self, alias, service):
        self.asked.append((alias, service))
        if self._credentials is not None:
            return self._credentials
        if service == "trello":
            return {"api_key": KEYRING_API_KEY, "token": KEYRING_TOKEN}
        if service == "jira":
            return {"email": "legacy@example.com", "api_token": KEYRING_TOKEN}
        return None


@pytest.fixture(autouse=True)
def _reset_recorder():
    _RecordingTrelloAPI.constructed = []
    yield
    _RecordingTrelloAPI.constructed = []


class _Board:
    """Minimal stand-in; the service only reads these attributes."""

    def __init__(self, board_type=BoardType.TRELLO):
        self.id = "board-1"
        self.is_active = True
        self.organization_id = "org-1"
        self.board_type = board_type
        self.board_external_id = "trello-board-abc"
        self.board_url = "https://trello.com/b/abc"
        self.project_id = "proj-1"
        self.board_name = "Delivery"


class _Org:
    id = "org-1"
    alias = "hs"


class _Session:
    """Enough Session for the credential path: .get() and nothing else."""

    def get(self, model, ident):
        return _Org() if ident == "org-1" else _Board()


def _service(
    monkeypatch,
    *,
    vault_payload,
    install_legacy_provider=False,
    legacy_credentials=None,
):
    # Patched on the **factory**, which is where the chain now lives: #643 lifted
    # `_resolve_token` out of this service so a second caller
    # (`ticket_status_service`) shares it rather than making a third private copy.
    # The service's method is a delegate, so every assertion below is still about
    # what ticket creation does -- only the import location of the seam moved.
    monkeypatch.setattr(
        factory, "get_board_credential_payload", lambda session, board_id: vault_payload
    )
    monkeypatch.setattr(factory, "TrelloAPI", _RecordingTrelloAPI)
    provider = _FakeProvider(legacy_credentials)
    if install_legacy_provider:
        # Patched BEFORE construction, because the service used to build its
        # provider eagerly in __init__ -- patch after and the real (empty on any
        # machine but the author's) provider is the one under test, and the test
        # passes for the wrong reason.
        #
        # raising=False deliberately: before phase 3 this replaces the real
        # import, after phase 3 the name is gone and this adds an attribute
        # nothing reads. Either way the assertions below describe behaviour, and
        # the test does not silently turn into an AttributeError once the symbol
        # it is about has been deleted.
        monkeypatch.setattr(
            bt, "get_credential_provider", lambda: provider, raising=False
        )
    service = BoardTicketCreationService(_Session())
    return service, provider


class TestTicketCreationResolvesAPerBoardCredential:
    @pytest.mark.asyncio
    async def test_the_boards_own_vault_credential_reaches_the_adapter(
        self, monkeypatch
    ):
        """The whole point of the phase: Vault → adapter, nothing in between."""
        service, _ = _service(
            monkeypatch,
            vault_payload={"api_key": VAULT_API_KEY, "token": VAULT_TOKEN},
        )
        board, org = _Board(), _Org()

        token = service._resolve_token(board, org)
        await service._get_adapter(board, token)

        assert _RecordingTrelloAPI.constructed == [(VAULT_API_KEY, VAULT_TOKEN)]

    @pytest.mark.asyncio
    async def test_a_caller_supplied_token_still_wins_over_vault(self, monkeypatch):
        """X-Integration-Token is a documented one-off override and stays."""
        service, _ = _service(
            monkeypatch,
            vault_payload={"api_key": VAULT_API_KEY, "token": VAULT_TOKEN},
        )
        board, org = _Board(), _Org()

        token = service._resolve_token(board, org, token="header-key:header-token")
        await service._get_adapter(board, token)

        assert _RecordingTrelloAPI.constructed == [("header-key", "header-token")]

    def test_a_keyring_credential_is_not_a_fallback(self, monkeypatch):
        """No per-board credential means no credential -- not "ask the laptop"."""
        service, provider = _service(
            monkeypatch, vault_payload=None, install_legacy_provider=True
        )

        with pytest.raises(ValueError) as excinfo:
            service._resolve_token(_Board(), _Org())

        assert KEYRING_TOKEN not in str(excinfo.value)
        assert provider.asked == []
        assert _RecordingTrelloAPI.constructed == []

    def test_a_keyring_credential_is_not_a_fallback_for_jira_either(self, monkeypatch):
        """Trello and Jira each had their own copy of the fallback."""
        service, provider = _service(
            monkeypatch, vault_payload=None, install_legacy_provider=True
        )

        with pytest.raises(ValueError):
            service._resolve_token(_Board(BoardType.JIRA), _Org())

        assert provider.asked == []

    def test_the_service_holds_no_credential_provider(self, monkeypatch):
        """The constructor used to build one eagerly, per request."""
        service, _ = _service(monkeypatch, vault_payload=None)
        assert not hasattr(service, "credential_provider")

    def test_the_error_names_the_board_and_the_store_to_fix_it_in(self, monkeypatch):
        """ "No credentials available for BoardType.TRELLO" told an operator
        nothing actionable. The failure has exactly one remedy -- store a
        credential for this board -- so the message has to say that."""
        service, _ = _service(monkeypatch, vault_payload=None)

        with pytest.raises(ValueError) as excinfo:
            service._resolve_token(_Board(), _Org())

        message = str(excinfo.value)
        assert "board-1" in message
        assert "board_credentials" in message


class TestAGitHubCredentialCannotReachABoardAdapter:
    """#554's class of bug, at the seam phase 3 removes.

    In #554 a credential resolved from a store that was not the board's reached
    ``TrelloAPI``, which puts its credentials in the query string, so the
    operator's GitHub PAT landed in api.trello.com's request logs. The legacy
    lookup deleted here had the same reach: it string-joined whatever
    ``~/.innoday/config.json`` held under the org's alias and handed the result to
    the adapter, without checking that the value belonged to that board -- or even
    to that service.

    Two earlier tests lived here and were **deleted rather than kept**: they
    monkeypatched ``org_credential_service.get_github_credentials`` /
    ``get_org_credential_payload`` (functions this service has never called) and
    grepped this module's source for their names. Both pass identically against
    the pre-phase-3 code, so they attested to nothing this change established
    while reading like a regression test -- and the source-string one fired on a
    mere *comment* mentioning the module. The test below patches the name the
    service actually resolved (``bt.get_credential_provider``) and asserts on what
    reached the adapter, so reverting phase 3 fails it.
    """

    @pytest.mark.asyncio
    async def test_a_github_pat_in_local_config_never_reaches_trelloapi(
        self, monkeypatch
    ):
        """A GitHub PAT keyed under `token` -- Trello's key too -- is not a
        Trello credential, and the pre-Vault fallback could not tell.

        Before phase 3 this resolved to ``"None:<pat>"`` and constructed
        ``TrelloAPI`` with the PAT as its token; now there is nothing to resolve
        and the store is never consulted.
        """
        service, provider = _service(
            monkeypatch,
            vault_payload=None,
            install_legacy_provider=True,
            legacy_credentials={"token": GITHUB_TOKEN},
        )
        board, org = _Board(), _Org()

        with pytest.raises(ValueError) as excinfo:
            token = service._resolve_token(board, org)
            await service._get_adapter(board, token)

        assert GITHUB_TOKEN not in str(excinfo.value)
        assert provider.asked == []
        assert _RecordingTrelloAPI.constructed == []


class TestTheAdapterFactoryHasNoLegacyCredentialSeam:
    def test_build_board_adapter_takes_no_legacy_credential_lookup(self):
        """The injected keyring lookup was phase 3's "deliberate part".

        Sync never passed one, so removing the parameter leaves sync byte-for-byte
        identical and makes the two paths the same path.
        """
        params = inspect.signature(factory.build_board_adapter).parameters
        assert "legacy_credentials" not in params

    def test_the_factory_defines_no_legacy_lookup_type(self):
        assert not hasattr(factory, "LegacyCredentialLookup")

    @pytest.mark.asyncio
    async def test_a_non_colon_jira_token_still_fails_loudly(self, monkeypatch):
        """Without the legacy lookup, the Jira branch's else must still raise
        rather than building a JiraAPI out of half a credential."""
        monkeypatch.setattr(factory, "TrelloAPI", _RecordingTrelloAPI)
        with pytest.raises(ValueError, match="email:api_token"):
            await factory.build_board_adapter(
                _Board(BoardType.JIRA), "not-colon-joined", _Session()
            )
