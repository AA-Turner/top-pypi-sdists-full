from setuptools import find_packages, setup

setup(
    name="asyncarve",
    version="0.1.1",
    description="Simple Arve library",
    package_dir={"": "app"},
    packages=find_packages(where="app"),
    long_description="Asynchronous Python client to communicate with Arve devices",
    long_description_content_type="text/markdown",
    install_requires=["orjson>=2.0.1", "mashumaro>=3.12", "aiohttp>=3.9.3", "yarl>=1.9.4"],
    extras_require={"dev": ["pytest", "aresponses", "twine"]},
    url="https://github.com/arvetech/asyncarve",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License"
    ]
)
