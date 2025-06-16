
import os
import pytest

from hdmf_docutils.init_sphinx_extension_doc import main as init_sphinx_extension_doc


@pytest.mark.parametrize(
    "additional_args,additional_expected_files",
    [
        (
            [],
            [
                "source/credits.rst",
                "source/format.rst",
                "source/index.rst",
            ]
        ),
        (
            [
                "--custom_description", "description.rst",
                "--custom_release_notes", "release_notes.rst",
            ],
            [
                "source/credits.rst",
                "source/format.rst",
                "source/index.rst",
                "source/description.rst",
                "source/release_notes.rst",
            ]
        ),
        (
            [
                "--master", "my_index.rst",
                "--credits_master", "my_credits.rst",
                "--format_master", "my_format.rst",
                "--custom_description", "description.rst",
                "--custom_release_notes", "release_notes.rst",
            ],
            [
                "source/my_credits.rst",
                "source/my_format.rst",
                "source/my_index.rst",
                "source/description.rst",
                "source/release_notes.rst",
            ]
        ),
    ]
)
def test_cli(tmpdir, additional_args, additional_expected_files):
    tmpdir = str(tmpdir)
    docs_dir = os.path.join(str(tmpdir), "docs")
    project = "ndx-my-extension"
    init_sphinx_extension_doc([
        "--project", project,
        "--author", "John Doe",
        "--version", "0.0.1",
        "--release", "alpha",
        "--output", docs_dir,
        "--spec_dir", "spec",
        "--namespace_filename", "%s.namespace.yaml" % project,
        "--default_namespace", project,
    ] + additional_args)

    for expected_file in [
        "make.bat",
        "Makefile",
        "README.md",
        "source/conf_doc_autogen.py",
        "source/conf.py",
        "source/_static/theme_overrides.css",
    ] + additional_expected_files:
        assert os.path.exists(os.path.join(docs_dir, expected_file))
