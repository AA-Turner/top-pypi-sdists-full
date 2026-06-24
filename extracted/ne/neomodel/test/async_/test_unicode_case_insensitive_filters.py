from test._async_compat import mark_async_test

from neomodel import AsyncStructuredNode, StringProperty


class UnicodeFilterNode(AsyncStructuredNode):
    name = StringProperty(unique_index=True)


@mark_async_test
async def test_unicode_case_insensitive_filters():
    node = await UnicodeFilterNode(name="Алиса Тест").save()
    await UnicodeFilterNode(name="Other").save()

    assert (
        await UnicodeFilterNode.nodes.filter(name__iexact="алиса тест").get()
        == node
    )
    assert (
        await UnicodeFilterNode.nodes.filter(name__icontains="лиса").get()
        == node
    )
    assert (
        await UnicodeFilterNode.nodes.filter(name__istartswith="али").get()
        == node
    )
    assert await UnicodeFilterNode.nodes.filter(name__iendswith="еСТ").get() == node
    assert (
        await UnicodeFilterNode.nodes.filter(name__iregex="алиса.*").get()
        == node
    )
