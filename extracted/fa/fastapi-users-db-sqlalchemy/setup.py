# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='fastapi-users-db-sqlalchemy',
    version='7.0.0',
    description='FastAPI Users database adapter for SQLAlchemy',
    long_description='# FastAPI Users - Database adapter for SQLAlchemy ORM\n\n<p align="center">\n  <img src="https://raw.githubusercontent.com/frankie567/fastapi-users/master/logo.svg?sanitize=true" alt="FastAPI Users">\n</p>\n\n<p align="center">\n    <em>Ready-to-use and customizable users management for FastAPI</em>\n</p>\n\n[![build](https://github.com/fastapi-users/fastapi-users-db-sqlalchemy/workflows/Build/badge.svg)](https://github.com/fastapi-users/fastapi-users/actions)\n[![codecov](https://codecov.io/gh/fastapi-users/fastapi-users-db-sqlalchemy/branch/master/graph/badge.svg)](https://codecov.io/gh/fastapi-users/fastapi-users-db-sqlalchemy)\n[![PyPI version](https://badge.fury.io/py/fastapi-users-db-sqlalchemy.svg)](https://badge.fury.io/py/fastapi-users-db-sqlalchemy)\n[![Downloads](https://pepy.tech/badge/fastapi-users-db-sqlalchemy)](https://pepy.tech/project/fastapi-users-db-sqlalchemy)\n<p align="center">\n<a href="https://github.com/sponsors/frankie567"><img src="https://md-buttons.francoisvoron.com/button.svg?text=Buy%20me%20a%20coffee%20%E2%98%95%EF%B8%8F&bg=ef4444&w=200&h=50"></a>\n</p>\n\n---\n\n**Documentation**: <a href="https://fastapi-users.github.io/fastapi-users/" target="_blank">https://fastapi-users.github.io/fastapi-users/</a>\n\n**Source Code**: <a href="https://github.com/fastapi-users/fastapi-users" target="_blank">https://github.com/fastapi-users/fastapi-users</a>\n\n---\n\nAdd quickly a registration and authentication system to your [FastAPI](https://fastapi.tiangolo.com/) project. **FastAPI Users** is designed to be as customizable and adaptable as possible.\n\n**Sub-package for SQLAlchemy ORM support in FastAPI Users.**\n\n## Development\n\n### Setup environment\n\nWe use [Hatch](https://hatch.pypa.io/latest/install/) to manage the development environment and production build. Ensure it\'s installed on your system.\n\n### Run unit tests\n\nYou can run all the tests with:\n\n```bash\nhatch run test\n```\n\n### Format the code\n\nExecute the following command to apply `isort` and `black` formatting:\n\n```bash\nhatch run lint\n```\n\n## License\n\nThis project is licensed under the terms of the MIT license.\n',
    author_email='François Voron <fvoron@gmail.com>',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: AsyncIO',
        'Framework :: FastAPI',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Topic :: Internet :: WWW/HTTP :: Session',
    ],
    install_requires=[
        'fastapi-users>=10.0.0',
        'sqlalchemy[asyncio]<2.1.0,>=2.0.0',
    ],
    packages=[
        'fastapi_users_db_sqlalchemy',
        'tests',
    ],
)
