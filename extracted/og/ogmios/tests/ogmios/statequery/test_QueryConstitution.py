import pytest

from tests.ogmios.test_fixtures import client, era
from ogmios.datatypes import Era


def test_QueryConstitution(client, era):
    if Era.get_index(era) < Era.get_index(Era.conway):
        pytest.skip("Test only valid for conway era")

    id_str = "My ID string"
    guardrails, metadata, id = client.query_constitution.execute(id_str)

    if guardrails:
        assert isinstance(guardrails, dict)
        assert guardrails.keys() == {"hash"}
    if metadata:
        assert isinstance(metadata, dict)
        assert metadata.keys() == {"url", "hash"}
    assert id == id_str
