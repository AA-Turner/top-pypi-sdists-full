from rapidpe_rift_pipe import config



import contextlib
import os
import pathlib
import pytest
import shutil
import stat
import tempfile


_example_config_fnames = pathlib.Path("examples/configs").rglob("*.ini")


@pytest.mark.parametrize("config_fname", _example_config_fnames)
def test_examples(config_fname):
    """
    Tests that all example config files in /examples/configs do not crash.
    """
    with fake_executables():
        try:
            config.Config.load(config_fname)
        except Exception as e:
            msg = f"Parsing {config_fname} produced an exception\n{e}"
            assert False, msg


# Names of executables required by config.Config
__required_exe_names = [
    "rapidpe_create_event_dag",
    "rapidpe_compute_intrinsic_grid",
    "rapidpe_integrate_extrinsic_likelihood",
]


@contextlib.contextmanager
def fake_executables():
    """
    Temporarily modify `PATH` environment variable to include placeholders
    for all of the executables expected by `config.Config`.

    NOTE: any changes to `PATH` made inside the context will be reverted.

    Adapted from https://stackoverflow.com/a/34333710/4761692
    """
    orig_environ = dict(os.environ)

    # Make a temporary directory
    fake_exe_dir = tempfile.mkdtemp(prefix="rapidpe-rift-pipe_fake-exe")

    # Write empty files in tempdir
    for exe_name in __required_exe_names:
        fake_exe_fname = os.path.join(fake_exe_dir, exe_name)
        # Create empty file
        with open(fake_exe_fname, "w"):
            pass
        # Make file executable
        permissions = os.stat(fake_exe_fname).st_mode | stat.S_IEXEC
        os.chmod(fake_exe_fname, permissions)

    # Add temporary directory to PATH environment variable
    os.environ["PATH"] += f"{os.pathsep}{fake_exe_dir}"

    # Give control back to the caller
    try:
        yield
    # Clean up the environment
    finally:
        # Delete tempdir
        shutil.rmtree(fake_exe_dir)

        # Revert environment variables
        os.environ.clear()
        os.environ.update(orig_environ)
