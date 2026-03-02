from setuptools import setup

with open("README.rst") as rst:
    description = rst.read()

setup(
    name="sqlite3_api",
    version="2.0.4",
    packages=["sqlite3_api"],
    url="https://github.com/AlexDev-py/sqlite3-api.git",
    license="MIT",
    author="AlexDev",
    author_email="aleks.filiov@yandex.ru",
    description="API for sqlite3",
    long_description=description,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ],
)

# sdist
# twine register dist/sqlite3_api-2.0.3.tar.gz
# twine upload dist/sqlite3_api-2.0.3.tar.gz
# -r testpypi
