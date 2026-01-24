import os
import sys
from setuptools import find_packages, setup  # type: ignore[import-untyped]

def _read_readme() -> str:
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    try:
        with open(readme_path, encoding="utf-8") as handle:
            return handle.read()
    except OSError:
        return ""


ext_modules: list[object]
if sys.implementation.name == "cpython":
    from mypyc.build import mypycify

    MYPYC_DEBUG_LEVEL = os.environ.get("MYPYC_DEBUG_LEVEL", "0")

    paths_to_compile = [
        "typed_envs/__init__.py",
        # TODO: implement a proxy wrapper instead of hacky subclasses "typed_envs/_env_var.py",
        "typed_envs/_typed.py",
        "typed_envs/ENVIRONMENT_VARIABLES.py",
        # TODO: fix mypyc IR error "typed_envs/factory.py",
        "typed_envs/registry.py",
        "typed_envs/typing.py",
    ]

    ext_modules = mypycify(
        paths=paths_to_compile, group_name="typed_envs", debug_level=MYPYC_DEBUG_LEVEL
    )
else:
    ext_modules = []

setup(
    name="typed_envs",
    version="0.2.4",
    url="https://github.com/BobTheBuidler/typed-envs",
    author="BobTheBuidler",
    author_email="bobthebuidlerdefi@gmail.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
    ],
    description="Typed environment variables for python applications.",
    long_description=_read_readme(),
    long_description_content_type="text/markdown",
    python_requires=">=3.9,<4",
    packages=find_packages(),
    install_requires=["typing_extensions>=4.7"],
    package_data={"typed_envs": ["py.typed"]},
    include_package_data=True,
    ext_modules=ext_modules,
)
