import asyncio
import hashlib
from contextlib import suppress
from pathlib import Path

from aioboto3 import Session
from platformdirs import user_cache_dir

from fluidattacks_core.cpg.joern import Language as JoernLanguage
from fluidattacks_core.cpg.joern import run_joern_command
from fluidattacks_core.filesystem.defaults import Language as SystemLanguage


def _generate_args_parse(
    language: JoernLanguage,
    output_file: Path,
    working_dir: Path,
    exclude: list[Path],
) -> list[str]:
    exclude = list(exclude)
    args = [
        "--language",
        language.value,
        "--output",
        str(output_file.absolute()),
        str(working_dir.absolute()),
    ]
    match language:
        case JoernLanguage.Python | JoernLanguage.PythonAlias:
            ignore_files = [str(p.relative_to(working_dir)) for p in exclude if p.is_file()]
            ignore_dirs = [str(p.relative_to(working_dir)) for p in exclude if p.is_dir()]

            if ignore_files or ignore_dirs:
                args.append("--frontend-args")
                if ignore_files:
                    args.extend(["--ignore-paths", ",".join(ignore_files)])
                if ignore_dirs:
                    args.extend(["--ignore-dir-names", ",".join(ignore_dirs)])
        case JoernLanguage.Java | JoernLanguage.JavaAlias | JoernLanguage.JavaScript:
            ignore_files = [str(p.absolute()) for p in exclude]

            if ignore_files:
                args.extend(
                    [
                        "--frontend-args",
                        "--enable-file-content",
                        "--exclude",
                        ",".join(ignore_files),
                    ],
                )
    return args


async def _get_repo_top_level(repo_path: Path) -> Path:
    process = await asyncio.create_subprocess_exec(
        "git",
        "rev-parse",
        "--show-toplevel",
        cwd=repo_path,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, _ = await process.communicate()
    return Path(stdout.decode().strip())


async def _get_last_commit(repo_path: Path | str) -> str:
    process = await asyncio.create_subprocess_exec(
        "git",
        "rev-parse",
        "HEAD",
        cwd=repo_path,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, _ = await process.communicate()
    return stdout.decode().strip()


async def generate_cpg(
    working_dir: Path,
    language: SystemLanguage,
    exclude: list[Path] | None = None,
) -> Path | None:
    cache_dir = Path(user_cache_dir("sifts"))
    cache_dir.mkdir(parents=True, exist_ok=True)
    try:
        relative_path = working_dir.relative_to(await _get_repo_top_level(working_dir))
    except ValueError:
        relative_path = working_dir
    cache_file = (
        cache_dir
        / hashlib.sha3_256(
            (await _get_last_commit(working_dir) + str(relative_path) + language.value).encode(),
        ).hexdigest()
    )
    if not await run_joern_command(
        "joern-parse",
        _generate_args_parse(
            JoernLanguage.from_sifts_language(language),
            cache_file,
            working_dir,
            exclude or [],
        ),
    ):
        return None
    return cache_file


async def generate_cpg_and_upload(
    working_dir: Path,
    language: SystemLanguage,
    exclude: list[Path] | None = None,
    *,
    group: str,
    repo_nickname: str,
) -> Path | None:
    cache_file = await generate_cpg(working_dir, language, exclude)
    if not cache_file:
        return None
    async with Session().client("s3") as s3_client:
        await s3_client.upload_file(
            str(cache_file.absolute()),
            "machine.data",
            f"cpg/{group}/{repo_nickname}/{cache_file.name}",
        )
    return cache_file


async def get_cpg(
    working_dir: Path,
    language: SystemLanguage,
    group: str,
    repo_nickname: str,
) -> Path | None:
    cache_dir = Path(user_cache_dir("sifts"))
    cache_dir.mkdir(parents=True, exist_ok=True)
    try:
        relative_path = working_dir.relative_to(await _get_repo_top_level(working_dir))
    except ValueError:
        relative_path = working_dir
    cache_file = (
        cache_dir
        / hashlib.sha3_256(
            (await _get_last_commit(working_dir) + str(relative_path) + language.value).encode(),
        ).hexdigest()
    )
    async with Session().client("s3") as s3_client:
        with suppress(s3_client.exceptions.ClientError):
            await s3_client.head_object(
                Bucket="machine.data",
                Key=f"cpg/{group}/{repo_nickname}/{cache_file.name}",
            )
            await s3_client.download_file(
                "machine.data",
                f"cpg/{group}/{repo_nickname}/{cache_file.name}",
                str(cache_file.absolute()),
            )
            return cache_file
    return None
