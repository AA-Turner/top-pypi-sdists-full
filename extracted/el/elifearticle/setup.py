from setuptools import setup

import elifearticle

with open("README.md") as fp:
    readme = fp.read()

setup(
    name="elifearticle",
    version=elifearticle.__version__,
    description="eLife article objects.",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=["elifearticle"],
    license="MIT",
    install_requires=["elifetools>=0.43.0", "GitPython"],
    url="https://github.com/elifesciences/elife-article",
    maintainer="eLife Sciences Publications Ltd.",
    maintainer_email="tech-team@elifesciences.org",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)
