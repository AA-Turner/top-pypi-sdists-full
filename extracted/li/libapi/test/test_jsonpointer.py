from __future__ import annotations

from pytest import mark, param

from libapi.jsonpointer import JSONPointer

document = {
    'fear': ['denies', 'faith'],
    '': 0,
    'a/b': 1,
    'c%d': 2,
    'e^f': 3,
    'g|h': 4,
    'i\\j': 5,
    'k"l': 6,
    ' ': 7,
    'm~n': 8,
}


@mark.parametrize(
    'a, b',
    [
        param('', document, id='the-whole-document'),
        param('/fear', ['denies', 'faith'], id='object-property'),
        param('/fear/0', 'denies', id='array-index'),
        param('/', 0, id='value-0'),
        param('/a~1b', 1, id='value-1'),
        param('/c%d', 2, id='value-2'),
        param('/e^f', 3, id='value-3'),
        param('/g|h', 4, id='value-4'),
        param('/i\\j', 5, id='value-5'),
        param('/k"l', 6, id='value-6'),
        param('/ ', 7, id='value-7'),
        param('/m~0n', 8, id='value-8'),
    ],
)
def test_jsonpointer_get(a: str, b):
    assert JSONPointer(a).get(document) == b
