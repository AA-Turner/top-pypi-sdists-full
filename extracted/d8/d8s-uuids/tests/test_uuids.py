import uuid

from d8s_uuids import is_uuid, uuid3, uuid4, uuid4_examples, uuid5


def test_is_uuid_docs_1():
    assert not is_uuid('foo')
    assert is_uuid(uuid4())
    assert not is_uuid(uuid4(), version=1)


def test_uuid4_examples_1():
    result = uuid4_examples()
    assert len(result) == 10
    assert isinstance(result[0], str)

    result = uuid4_examples(n=100)
    assert len(result) == 100
    assert isinstance(result[0], str)

    result = uuid4_examples(uuids_as_strings=False)
    assert len(result) == 10
    assert isinstance(result[0], uuid.UUID)


def test_uuid4_1():
    result = uuid4()
    assert isinstance(result, str)


def test_uuid3_1():
    result_1 = uuid3('foo')
    result_2 = uuid3('foo')
    assert result_1 == result_2

    result_3 = uuid3('foo', namespace=uuid.NAMESPACE_URL)
    result_4 = uuid3('foo', namespace=uuid.NAMESPACE_URL)
    assert result_3 == result_4
    assert result_3 != result_1


def test_uuid5_1():
    result_1 = uuid5('foo')
    result_2 = uuid5('foo')
    assert result_1 == result_2

    result_3 = uuid5('foo', namespace=uuid.NAMESPACE_URL)
    result_4 = uuid5('foo', namespace=uuid.NAMESPACE_URL)
    assert result_3 == result_4
    assert result_3 != result_1
