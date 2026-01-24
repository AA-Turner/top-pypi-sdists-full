import inspect
import io
import tarfile
from pathlib import Path

from fa_purity import (
    Cmd,
    Unsafe,
)

from fluidattacks_etl_utils import secrets
from fluidattacks_etl_utils.bug import (
    Bug,
)


def _fake_archive(
    _repo_ssh_url: str,
    _ref: str,
    path: str,
) -> Cmd[io.BytesIO]:
    def _action() -> io.BytesIO:
        tar_bytes = io.BytesIO()
        data = b"foo: bar\n"

        with tarfile.open(fileobj=tar_bytes, mode="w") as tar:
            ti = tarfile.TarInfo(name=path)
            ti.size = len(data)
            tar.addfile(ti, io.BytesIO(data))

        return tar_bytes

    return Cmd.wrap_impure(_action)


def test_fetch_secret_file_uses_git_archive() -> None:
    result = Unsafe.compute(secrets._fetch_secret_file(_fake_archive))  # noqa: SLF001

    temp_path: Path = Bug.assume_success(
        "_fetch_secret_file",
        inspect.currentframe(),
        (),
        result,
    )

    try:
        assert temp_path.exists()
        assert temp_path.suffix == ".yaml"

        content = temp_path.read_bytes()
        assert content == b"foo: bar\n"
    finally:
        temp_path.unlink(missing_ok=True)
