"""Top level conftest.py for BACore test cases."""

import pytest


@pytest.fixture
def fixt_markdown_content():
    """Markdown file content."""
    return """# BACore ReadMe File

    This is some markdown content.

    ## With sub-heading

    - and some
    - bullets

    End of file.
    """


@pytest.fixture
def fixt_pyproject_content():
    """Create a temporary pyproject.toml file."""
    return """
    [project]
    name = 'bacore'
    version = "1.0.0"
    description = "BACore is a framework for business analysis and test automation."
    """


@pytest.fixture
def fixt_python_src():
    return '''
    """This module is for testing."""

    class StandardClass:
        """Standard class docstring."""
        pass

    def standard_function():
        """Standard function docstring."""
        pass
    '''


@pytest.fixture(scope="function")
def fixt_dir_with_files(tmp_path, fixt_markdown_content, fixt_pyproject_content, fixt_python_src):
    directory = tmp_path
    (directory / "pyproject.toml").write_text(fixt_pyproject_content, encoding="utf-8")
    (directory / "readme.md").write_text(fixt_markdown_content, encoding="utf-8")
    (directory / "src").mkdir()
    (directory / "src" / "bacore").mkdir()
    (directory / "src" / "bacore" / "__init__.py").write_text('"""BACore main module"""', encoding="utf-8")
    (directory / "src" / "bacore" / "python_src_file.py").write_text(fixt_python_src, encoding="utf-8")

    return directory
