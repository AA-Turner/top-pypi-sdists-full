base_ignore = [
    "E501",  # Line too long (ignored by pysen)
    "D",  # pydocstyle (https://pypi.org/project/pydocstyle/)
    "ICN",  # flake8-import-conventions (https://github.com/joaopalmeiro/flake8-import-conventions) # NOQA
    "COM812",  # break formatter compatibility(https://docs.astral.sh/ruff/rules/missing-trailing-comma/#formatter-compatibility) # NOQA
]
strict_ignore = [
    *base_ignore,
    "S101",  # Use of `assert` detected
    "T20",  # flake8-print (https://pypi.org/project/flake8-print/)
    "ANN",  # flkae8-annotations (https://pypi.org/project/flake8-annotations/)
    "INP001",  # File {file} is part of an implicit namespace package. Add an `__init__.py`.
]

basic_select = [
    "I",  # isort (https://pypi.org/project/isort/)
    "E",  # pycodestyle (https://pypi.org/project/pycodestyle/)
    "F",  # pyflakes (https://pypi.org/project/pyflakes/)
    "W",  # pycodestyle (https://pypi.org/project/pycodestyle/)
    "B",  # flake8-bugbear (https://pypi.org/project/flake8-bugbear/)
]

UNFIXABLE = [
    "ERA001",  # do not delete commented code
]

preset_dict = {
    "basic": (basic_select, strict_ignore),
    "strict": (["ALL"], strict_ignore),
    "very_strict": (["ALL"], base_ignore),
    "all": (["ALL"], base_ignore),  # TODO: delete
}
