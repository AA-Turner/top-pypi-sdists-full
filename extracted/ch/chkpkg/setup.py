from pathlib import Path

from setuptools import setup


def load_module_dict(filename: str) -> dict:
    import importlib.util as ilu
    filename = Path(__file__).parent / filename
    spec = ilu.spec_from_file_location('', filename)
    module = ilu.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.__dict__


name = "chkpkg"
constants = load_module_dict(f'{name}/_constants.py')


def read_readme() -> str:
    # need encoding for Windows
    txt = (Path(__file__).parent / 'README.md').read_text(encoding='utf-8')
    # skipping badges (everything before the first header)
    txt = txt.partition("# ")[-1]
    return txt


setup(
    name=name,
    version=constants['__version__'],
    author=constants['__author__'],
    author_email=constants['__author_email__'],
    url='https://github.com/rtmigo/chkpkg_py#readme',

    python_requires='>=3.6',
    install_requires=[],
    packages=[name],
    package_data={name: ['py.typed']},

    description=constants['__summary__'],

    keywords=constants['__keywords__'],

    long_description=read_readme(),  # need encoding for Windows
    long_description_content_type='text/markdown',

    license=constants['__license__'],

    classifiers=[
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
    ],
)
