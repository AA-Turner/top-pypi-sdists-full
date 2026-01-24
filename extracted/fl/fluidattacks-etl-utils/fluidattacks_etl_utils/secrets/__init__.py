from __future__ import (
    annotations,
)

import inspect
import io
import tarfile
import tempfile
from collections.abc import (
    Callable,
)
from dataclasses import (
    dataclass,
)
from pathlib import (
    Path,
)

import git
from fa_purity import (
    Cmd,
    CmdUnwrapper,
    FrozenList,
    PureIterFactory,
    Result,
    ResultE,
    ResultTransform,
)
from fa_purity.json import (
    JsonObj,
    JsonPrimitiveUnfolder,
    JsonUnfolder,
    Unfolder,
)

from fluidattacks_etl_utils.bug import (
    Bug,
)

from . import (
    _integrates,
    _snowflake,
    _zoho_leads,
)
from ._core import (
    GenericSecret,
    get_secrets,
)
from ._snowflake import (
    SnowflakeCredentials,
)
from ._zoho_leads import (
    ZohoCreds,
)


@dataclass(frozen=True)
class ObservesSecrets:
    zoho_creds: Cmd[ZohoCreds]
    zoho_creds_other_products: Cmd[ZohoCreds]
    snowflake_etl_access: Cmd[SnowflakeCredentials]
    integrates_fluid_org_id: Cmd[GenericSecret]
    zoho_fluid_org_id: Cmd[GenericSecret]
    get_secret: Callable[[str], Cmd[ResultE[GenericSecret]]]
    get_secrets: Callable[[FrozenList[str]], Cmd[ResultE[FrozenList[GenericSecret]]]]


Archive = Callable[[str, str, str], Cmd[io.BytesIO]]


def _fetch_with_git_archive(
    repo_ssh_url: str,
    ref: str,
    path: str,
) -> Cmd[io.BytesIO]:
    def _action() -> io.BytesIO:
        tar_bytes = io.BytesIO()
        git_cmd = git.cmd.Git()
        git_cmd.archive(
            f"--remote={repo_ssh_url}",
            "--format=tar",
            ref,
            path,
            output_stream=tar_bytes,
        )
        return tar_bytes

    return Cmd.wrap_impure(_action)


def _process_tar(tar_bytes: io.BytesIO) -> ResultE[Path]:
    repo_path = "observes/secrets/prod.yaml"
    tar_bytes.seek(0)

    with tarfile.open(fileobj=tar_bytes) as tar:
        member = tar.extractfile(repo_path)

        if member is None:
            return Result.failure(FileNotFoundError(repo_path))

        secret_data = member.read()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".yaml") as file:
        file.write(secret_data)
        return Result.success(Path(file.name))


def _fetch_secret_file(
    archive_fn: Archive,
) -> Cmd[ResultE[Path]]:
    repo_ssh_url = "git@gitlab.com:fluidattacks/universe.git"
    ref = "trunk"
    path = "observes/secrets/prod.yaml"

    def _action(unwrapper: CmdUnwrapper) -> ResultE[Path]:
        try:
            tar_bytes = unwrapper.act(archive_fn(repo_ssh_url, ref, path))
            return _process_tar(tar_bytes)
        except Exception as error:  # noqa: BLE001
            # catching all exceptions is intentional (network/auth/archive failures)
            return Result.failure(error)

    return Cmd.new_cmd(_action)


def _extract_secret(secrets: JsonObj, key: str) -> ResultE[GenericSecret]:
    return JsonUnfolder.require(
        secrets,
        key,
        lambda v: Unfolder.to_primitive(v).bind(JsonPrimitiveUnfolder.to_str).map(GenericSecret),
    )


def _standard_implementation(secrets: Path) -> ObservesSecrets:
    zoho_creds = (
        get_secrets(secrets)
        .map(lambda r: r.bind(lambda s: _zoho_leads.decode_zoho_creds(secrets, s)))
        .map(lambda r: Bug.assume_success("zoho_creds", inspect.currentframe(), (), r))
    )
    zoho_creds_other_products = (
        get_secrets(secrets)
        .map(lambda r: r.bind(lambda s: _zoho_leads.decode_zoho_creds_other_products(secrets, s)))
        .map(
            lambda r: Bug.assume_success(
                "zoho_creds_other_products_etl",
                inspect.currentframe(),
                (),
                r,
            ),
        )
    )
    snowflake_etl_access = (
        get_secrets(secrets)
        .map(lambda r: r.bind(lambda s: _snowflake.decode_snowflake_creds(secrets, s)))
        .map(lambda r: Bug.assume_success("snowflake_etl_access", inspect.currentframe(), (), r))
    )
    integrates_fluid_org_id = (
        get_secrets(secrets)
        .map(lambda r: r.bind(lambda s: _integrates.decode_fluid_org_id(secrets, s)))
        .map(lambda r: Bug.assume_success("integrates_fluid_org_id", inspect.currentframe(), (), r))
    )
    zoho_fluid_org_id = (
        get_secrets(secrets)
        .map(lambda r: r.bind(lambda s: _zoho_leads.decode_fluid_org_id(secrets, s)))
        .map(lambda r: Bug.assume_success("zoho_fluid_org_id", inspect.currentframe(), (), r))
    )
    return ObservesSecrets(
        zoho_creds=zoho_creds,
        zoho_creds_other_products=zoho_creds_other_products,
        snowflake_etl_access=snowflake_etl_access,
        integrates_fluid_org_id=integrates_fluid_org_id,
        zoho_fluid_org_id=zoho_fluid_org_id,
        get_secret=lambda k: get_secrets(secrets).map(
            lambda r: r.bind(
                lambda j: _extract_secret(j, k),
            ),
        ),
        get_secrets=lambda i: get_secrets(secrets).map(
            lambda r: r.bind(
                lambda j: ResultTransform.all_ok(
                    PureIterFactory.from_list(i).map(lambda k: _extract_secret(j, k)).to_list(),
                ),
            ),
        ),
    )


@dataclass(frozen=True)
class ObservesSecretsFactory:
    @staticmethod
    def new() -> Cmd[ResultE[ObservesSecrets]]:
        archive_fn = _fetch_with_git_archive
        return _fetch_secret_file(archive_fn).map(lambda r: r.map(_standard_implementation))


__all__ = [
    "GenericSecret",
    "SnowflakeCredentials",
    "ZohoCreds",
]
