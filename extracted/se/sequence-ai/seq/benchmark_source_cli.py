"""
`seq benchmark source <name>[@vN] [-o PATH]`: the code a benchmark version runs, as it was registered - the version new
evals run unless NAME@vN names another - downloaded from the platform (GET /v1/benchmarks/{name}/versions/{n}/source,
checked there against what the version was registered with) and unpacked into a new folder, `./<name>-v<n>` unless -o
names one. A folder that holds anything is refused, so nothing of yours is written over. As `seq policy source` is for
a policy's version (deployments_cli.source).




"""
from __future__ import annotations

import pathlib

from seq import deployments_cli
from sequence_ai._core.names import segment
from sequence_ai.errors import InvalidRequest


def source(name: str, version: int | None = None, out: str | None = None, base_url: str | None = None,
           echo=print) -> dict:
    """Download version `version` of benchmark `name` - the one its builds say new evals run when None - into DIR.
    Returns {name, version, dir, files}."""
    if version is None:
        builds = deployments_cli._call("GET", f"/v1/benchmarks/{segment(name)}/builds", base_url).get("builds") or []
        version = next((b["version"] for b in builds if b.get("serving")), None)
        if version is None:
            raise InvalidRequest(f"no version of {name} has passed its check yet; name one: {name}@vN",
                                 hint=f"seq benchmark versions {name}")
    dest = pathlib.Path(out or f"{name}-v{version}")
    if dest.exists() and (not dest.is_dir() or any(dest.iterdir())):
        raise InvalidRequest(f"{dest} already holds files; name a new or empty folder with -o")
    data = deployments_cli._call("GET", f"/v1/benchmarks/{segment(name)}/versions/{int(version)}/source", base_url,
                                 content=True)
    dest.mkdir(parents=True, exist_ok=True)
    files = deployments_cli._unpack(data, dest)
    size = sum((dest / f).stat().st_size for f in files)
    echo(f"{name} v{version}: {len(files)} file{'' if len(files) == 1 else 's'} ({size:,} bytes) in {dest}/ - the code "
         "it runs, as it was registered")
    return {"name": name, "version": int(version), "dir": str(dest), "files": files}
