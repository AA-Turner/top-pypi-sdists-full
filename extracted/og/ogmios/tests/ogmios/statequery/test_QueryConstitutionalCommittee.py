import pytest

from tests.ogmios.test_fixtures import client, era
from ogmios.datatypes import Era


def test_QueryConstitutionalCommittee(client, era):
    if Era.get_index(era) < Era.get_index(Era.conway):
        pytest.skip("Test only valid for conway era")

    id_str = "My ID string"
    result, id = client.query_constitutional_committee.execute(id_str)

    if result:
        assert isinstance(result, dict)
        assert result.keys() == {"members", "quorum"}
    assert id == id_str
