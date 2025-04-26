# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jetblack_serialization',
 'jetblack_serialization.json',
 'jetblack_serialization.xml']

package_data = \
{'': ['*']}

install_requires = \
['jetblack-iso8601>=1.0,<2.0',
 'lxml>=4.9,<5.0',
 'typing-extensions>=4,<5',
 'typing_inspect>=0.8,<0.9']

setup_kwargs = {
    'name': 'jetblack-serialization',
    'version': '3.1.1',
    'description': 'Serialization for JSON and XML using typing',
    'long_description': '# jetblack-serialization\n\nSerialization for JSON and XML in Python using typing annotations\n(read the [docs](https://rob-blackbourn.github.io/jetblack-serialization/)).\n\n## Status\n\nIt has been tested with Python 3.7 used the `typing_extensions`\npackage for `TypedDict` and `Annotated`. In Python 3.8 the `TypedDict`\nclass is available in the standard `typing` package.\n\n## Installation\n\nThe package can be installed with pip.\n\n```bash\npip install jetblack-serialization\n```\n\n## Overview\n\nThe package adds support for type annotations when serializing or deserializing\nJSON or XML.\n\n\n### JSON\n\nGiven a typed dictionary:\n\n```python\nfrom datetime import datetime\nfrom typing import List, Optional, TypedDict, Union\n\nclass Book(TypedDict, total=False):\n    book_id: int\n    title: str\n    author: str\n    publication_date: datetime\n    keywords: List[str]\n    phrases: List[str]\n    age: Optional[Union[datetime, int]]\n    pages: Optional[int]\n```\n\n#### Serializing\n\nThis could be serialized to JSON as:\n\n```python\nfrom stringcase import camelcase, snakecase\nfrom jetblack_serialization import SerializerConfig\nfrom jetblack_serialization.json import serialize\n\nobj: Book = {\n    \'author\': \'Chairman Mao\',\n    \'book_id\': 42,\n    \'title\': \'Little Red Book\',\n    \'publication_date\': datetime(1973, 1, 1, 21, 52, 13),\n    \'keywords\': [\'Revolution\', \'Communism\'],\n    \'phrases\': [\n        \'Revolutionary wars are inevitable in class society\',\n        \'War is the continuation of politics\'\n    ],\n    \'age\': 24,\n}\ntext = serialize(\n    obj,\n    Book,\n    SerializerConfig(camelcase, snakecase, pretty_print=True)\n)\nprint(text)\n```\n\ngiving:\n\n```json\n{\n    "bookId": 42,\n    "title": "Little Red Book",\n    "author": "Chairman Mao",\n    "publicationDate": "1973-01-01T21:52:13.00Z",\n    "keywords": ["Revolution", "Communism"],\n    "phrases": ["Revolutionary wars are inevitable in class society", "War is the continuation of politics"],\n    "age": 24,\n    "pages": null\n}\n```\n\nNote the fields have been camel cased, and the publication date has been turned\ninto an ISO 8601 date.\n\n#### Deserializing\n\nWe can deserialize the data as follows:\n\n```python\nfrom stringcase import camelcase, snakecase\nfrom jetblack_serialization import SerializerConfig\nfrom jetblack_serialization.json import deserialize\n\ndct = deserialize(\n    text,\n    Annotated[Book, JSONValue()],\n    SerializerConfig(camelcase, snakecase)\n)\n```\n\n### XML\n\nThe XML version of the typed dictionary might look like this:\n\n```python\nfrom datetime import datetime\nfrom typing import List, Optional, TypedDict, Union\nfrom typing_extensions import Annotated\nfrom jetblack_serialization.xml import XMLEntity, XMLAttribute\n\nclass Book(TypedDict, total=False):\n    book_id: Annotated[int, XMLAttribute("bookId")]\n    title: str\n    author: str\n    publication_date: datetime\n    keywords: Annotated[List[Annotated[str, XMLEntity("Keyword")]], XMLEntity("Keywords")]\n    phrases: List[str]\n    age: Optional[Union[datetime, int]]\n    pages: Optional[int]\n```\n\nNote we have introduced some annotations to control the serialization.\nFor XML we have used pascal-case to serialized the keys and snake-case\nfor deserialization.\n\n#### Serializing\n\nTo serialize we need to provide the containing tag `Book`:\n\n```python\nfrom stringcase import pascalcase, snakecase\nfrom jetblack_serialization import SerializerConfig\nfrom jetblack_serialization.xml import serialize\n\nbook: Book = {\n    \'author\': \'Chairman Mao\',\n    \'book_id\': 42,\n    \'title\': \'Little Red Book\',\n    \'publication_date\': datetime(1973, 1, 1, 21, 52, 13),\n    \'keywords\': [\'Revolution\', \'Communism\'],\n    \'phrases\': [\n        \'Revolutionary wars are inevitable in class society\',\n        \'War is the continuation of politics\'\n    ],\n    \'age\': 24,\n    \'pages\': None\n}\ntext = serialize(\n    book,\n    Annotated[Book, XMLEntity("Book")],\n    SerializerConfig(pascalcase, snakecase)\n)\nprint(text)\n```\n\nProducing:\n\n```xml\n<Book bookId="42">\n    <Title>Little Red Book</Title>\n    <Author>Chairman Mao</Author>\n    <PublicationDate>1973-01-01T21:52:13.00Z</PublicationDate>\n    <Keywords>\n        <Keyword>Revolution</Keyword>\n        <Keyword>Communism</Keyword>\n    </Keywords>\n    <Phrase>Revolutionary wars are inevitable in class society</Phrase>\n    <Phrase>War is the continuation of politics</Phrase>\n    <Age>24</Age>\n</Book>\'\n```\n\nThe annotations are more elaborate here. However, much of the typed dictionary\nrequires no annotation.\n\nFirst we needed the outer document wrapper `XMLEntity("Book")`.\n\nNext we annotated the `book_id` to be an `XMLAttribute`.\n\nFinally we annotated the two lists differently. The `keywords` list used\na nested structure, which we indicated by giving the list a different\n`XMLEntity` tag to the list items. For the phrases we used the default\nin-line behaviour.\n\n#### Deserializing\n\nWe can deserialize the XML as follows:\n\n```python\nfrom stringcase import pascalcase, snakecase\nfrom jetblack_serialization import SerializerConfig\nfrom jetblack_serialization.xml import deserialize\n\ndct = deserialize(\n    text,\n    Annotated[Book, XMLEntity("Book")],\n    SerializerConfig(pascalcase, snakecase)\n)\n```\n\n## Attributes\n\nFor JSON, attributes are typically not required. However\n`JSONProperty(tag: str)` and `JSONValue()` are provided for\ncompleteness.',
    'author': 'Rob Blackbourn',
    'author_email': 'rob.blackbourn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rob-blackbourn/jetblack-serialization',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
