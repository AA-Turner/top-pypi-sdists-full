# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydantic_sqlalchemy']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.5.1,<2.0.0', 'sqlalchemy>=1.3.16,<2.0.0']

extras_require = \
{'dev': ['jupyter[dev]>=1.0.0,<2.0.0',
         'autoflake[dev]>=1.3.1,<2.0.0',
         'flake8[dev]>=3.7.9,<4.0.0']}

setup_kwargs = {
    'name': 'pydantic-sqlalchemy',
    'version': '0.0.9',
    'description': 'Tools to convert SQLAlchemy models to Pydantic models',
    'long_description': '# Pydantic-SQLAlchemy\n\n<a href="https://github.com/tiangolo/pydantic-sqlalchemy/actions?query=workflow%3ATest" target="_blank">\n    <img src="https://github.com/tiangolo/pydantic-sqlalchemy/workflows/Test/badge.svg" alt="Test">\n</a>\n<a href="https://github.com/tiangolo/pydantic-sqlalchemy/actions?query=workflow%3APublish" target="_blank">\n    <img src="https://github.com/tiangolo/pydantic-sqlalchemy/workflows/Publish/badge.svg" alt="Publish">\n</a>\n<a href="https://codecov.io/gh/tiangolo/pydantic-sqlalchemy" target="_blank">\n    <img src="https://img.shields.io/codecov/c/github/tiangolo/pydantic-sqlalchemy?color=%2334D058" alt="Coverage">\n</a>\n<a href="https://pypi.org/project/pydantic-sqlalchemy" target="_blank">\n    <img src="https://img.shields.io/pypi/v/pydantic-sqlalchemy?color=%2334D058&label=pypi%20package" alt="Package version">\n</a>\n\nTools to generate Pydantic models from SQLAlchemy models.\n\nStill experimental.\n\n## How to use\n\nQuick example:\n\n```Python\nfrom typing import List\n\nfrom pydantic_sqlalchemy import sqlalchemy_to_pydantic\nfrom sqlalchemy import Column, ForeignKey, Integer, String, create_engine\nfrom sqlalchemy.ext.declarative import declarative_base\nfrom sqlalchemy.orm import Session, relationship, sessionmaker\n\nBase = declarative_base()\n\nengine = create_engine("sqlite://", echo=True)\n\n\nclass User(Base):\n    __tablename__ = "users"\n\n    id = Column(Integer, primary_key=True)\n    name = Column(String)\n    fullname = Column(String)\n    nickname = Column(String)\n\n    addresses = relationship(\n        "Address", back_populates="user", cascade="all, delete, delete-orphan"\n    )\n\n\nclass Address(Base):\n    __tablename__ = "addresses"\n    id = Column(Integer, primary_key=True)\n    email_address = Column(String, nullable=False)\n    user_id = Column(Integer, ForeignKey("users.id"))\n\n    user = relationship("User", back_populates="addresses")\n\n\nPydanticUser = sqlalchemy_to_pydantic(User)\nPydanticAddress = sqlalchemy_to_pydantic(Address)\n\n\nclass PydanticUserWithAddresses(PydanticUser):\n    addresses: List[PydanticAddress] = []\n\n\nBase.metadata.create_all(engine)\n\n\nLocalSession = sessionmaker(bind=engine)\n\ndb: Session = LocalSession()\n\ned_user = User(name="ed", fullname="Ed Jones", nickname="edsnickname")\n\naddress = Address(email_address="ed@example.com")\naddress2 = Address(email_address="eddy@example.com")\ned_user.addresses = [address, address2]\ndb.add(ed_user)\ndb.commit()\n\n\ndef test_pydantic_sqlalchemy():\n    user = db.query(User).first()\n    pydantic_user = PydanticUser.from_orm(user)\n    data = pydantic_user.dict()\n    assert data == {\n        "fullname": "Ed Jones",\n        "id": 1,\n        "name": "ed",\n        "nickname": "edsnickname",\n    }\n    pydantic_user_with_addresses = PydanticUserWithAddresses.from_orm(user)\n    data = pydantic_user_with_addresses.dict()\n    assert data == {\n        "fullname": "Ed Jones",\n        "id": 1,\n        "name": "ed",\n        "nickname": "edsnickname",\n        "addresses": [\n            {"email_address": "ed@example.com", "id": 1, "user_id": 1},\n            {"email_address": "eddy@example.com", "id": 2, "user_id": 1},\n        ],\n    }\n```\n\n## Release Notes\n\n### Latest Changes\n\n\n### 0.0.9\n\n* ✨ Add `poetry-version-plugin`, remove `importlib-metadata` dependency. PR [#32](https://github.com/tiangolo/pydantic-sqlalchemy/pull/32) by [@tiangolo](https://github.com/tiangolo).\n\n### 0.0.8.post1\n\n* 💚 Fix setting up Poetry for GitHub Action Publish. PR [#23](https://github.com/tiangolo/pydantic-sqlalchemy/pull/23) by [@tiangolo](https://github.com/tiangolo).\n\n### 0.0.8\n\n* ⬆️ Upgrade `importlib-metadata` to 3.0.0. PR [#22](https://github.com/tiangolo/pydantic-sqlalchemy/pull/22) by [@tiangolo](https://github.com/tiangolo).\n* 👷 Add GitHub Action latest-changes. PR [#20](https://github.com/tiangolo/pydantic-sqlalchemy/pull/20) by [@tiangolo](https://github.com/tiangolo).\n* 💚 Fix GitHub Actions Poetry setup. PR [#21](https://github.com/tiangolo/pydantic-sqlalchemy/pull/21) by [@tiangolo](https://github.com/tiangolo).\n\n### 0.0.7\n\n* Update requirements of `importlib-metadata` to support the latest version `2.0.0`. PR [#11](https://github.com/tiangolo/pydantic-sqlalchemy/pull/11).\n\n### 0.0.6\n\n* Add support for SQLAlchemy extended types like [sqlalchemy-utc: UtcDateTime](https://github.com/spoqa/sqlalchemy-utc). PR [#9](https://github.com/tiangolo/pydantic-sqlalchemy/pull/9).\n\n### 0.0.5\n\n* Exclude columns before checking their Python types. PR [#5](https://github.com/tiangolo/pydantic-sqlalchemy/pull/5) by [@ZachMyers3](https://github.com/ZachMyers3).\n\n### 0.0.4\n\n* Do not include SQLAlchemy defaults in Pydantic models. PR [#4](https://github.com/tiangolo/pydantic-sqlalchemy/pull/4).\n\n### 0.0.3\n\n* Add support for `exclude` to exclude columns from Pydantic model. PR [#3](https://github.com/tiangolo/pydantic-sqlalchemy/pull/3).\n* Add support for overriding the Pydantic `config`. PR [#1](https://github.com/tiangolo/pydantic-sqlalchemy/pull/1) by [@pyropy](https://github.com/pyropy).\n* Add CI with GitHub Actions. PR [#2](https://github.com/tiangolo/pydantic-sqlalchemy/pull/2).\n\n## License\n\nThis project is licensed under the terms of the MIT license.\n',
    'author': 'Sebastián Ramírez',
    'author_email': 'tiangolo@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
