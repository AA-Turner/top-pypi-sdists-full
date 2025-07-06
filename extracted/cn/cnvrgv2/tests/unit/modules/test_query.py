import pytest

from cnvrgv2.proxy import Proxy
from cnvrgv2.errors import CnvrgError
from cnvrgv2.modules.queries.query import Query


class TestQuery:
    def test_query_bad_init(self, empty_context):
        with pytest.raises(CnvrgError):
            Query(None)

    def test_delete_query(self, mocker, empty_context):
        slug = "test-slug"

        model = Query(context=empty_context, slug=slug)

        mocked_delete = mocker.patch.object(Proxy, 'call_api')
        model.delete()
        assert mocked_delete.call_count == 1
