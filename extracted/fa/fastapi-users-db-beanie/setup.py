# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='fastapi-users-db-beanie',
    version='5.0.0',
    description='FastAPI Users database adapter for Beanie',
    long_description='# FastAPI Users - Database adapter for Beanie\n\n<p align="center">\n  <img src="https://raw.githubusercontent.com/frankie567/fastapi-users/master/logo.svg?sanitize=true" alt="FastAPI Users">\n</p>\n\n<p align="center">\n    <em>Ready-to-use and customizable users management for FastAPI</em>\n</p>\n\n> [!NOTE]\n> **This project is now in maintenance mode.** While we\'ll continue to provide security updates and dependency maintenance, no new features will be added. We encourage you to explore the project and use it as-is, knowing it will remain stable and secure.\n>\n> We\'re currently working on a new Python authentication toolkit that will ultimately supersede FastAPI Users. Stay tuned for updates!\n\n[![build](https://github.com/fastapi-users/fastapi-users-db-beanie/workflows/Build/badge.svg)](https://github.com/fastapi-users/fastapi-users/actions)\n[![codecov](https://codecov.io/gh/fastapi-users/fastapi-users-db-beanie/branch/master/graph/badge.svg)](https://codecov.io/gh/fastapi-users/fastapi-users-db-beanie)\n[![PyPI version](https://badge.fury.io/py/fastapi-users-db-beanie.svg)](https://badge.fury.io/py/fastapi-users-db-beanie)\n[![Downloads](https://pepy.tech/badge/fastapi-users-db-beanie)](https://pepy.tech/project/fastapi-users-db-beanie)\n\n---\n\n**Documentation**: <a href="https://fastapi-users.github.io/fastapi-users/" target="_blank">https://fastapi-users.github.io/fastapi-users/</a>\n\n**Source Code**: <a href="https://github.com/fastapi-users/fastapi-users" target="_blank">https://github.com/fastapi-users/fastapi-users</a>\n\n---\n\nAdd quickly a registration and authentication system to your [FastAPI](https://fastapi.tiangolo.com/) project. **FastAPI Users** is designed to be as customizable and adaptable as possible.\n\n**Sub-package for Beanie support in FastAPI Users.**\n\n## Development\n\n### Setup environment\n\nWe use [Hatch](https://hatch.pypa.io/latest/install/) to manage the development environment and production build. Ensure it\'s installed on your system.\n\n### Run unit tests\n\nYou can run all the tests with:\n\n```bash\nhatch run test\n```\n\n### Format the code\n\nExecute the following command to apply `isort` and `black` formatting:\n\n```bash\nhatch run lint\n```\n\n## License\n\nThis project is licensed under the terms of the MIT license.\n',
    author_email='François Voron <fvoron@gmail.com>, Schwannden Kuo <schwannden@gmail.com>',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: AsyncIO',
        'Framework :: FastAPI',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        'Topic :: Internet :: WWW/HTTP :: Session',
    ],
    install_requires=[
        'beanie>=2.0.0',
        'fastapi-users>=15.0.1',
    ],
    packages=[
        'fastapi_users_db_beanie',
        'tests',
    ],
)
