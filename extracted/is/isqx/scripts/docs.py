#!/usr/bin/env -S uv run --script
import logging
import shutil
import subprocess
from functools import partial
from pathlib import Path

PATH_ROOT = Path(__file__).parent.parent

FILENAME_INDEX = "index"
FILENAME_CONTRIBUTING = "contributing"
logger = logging.getLogger(__name__)


def copy_docs_file(path_in: Path, path_out: Path) -> None:
    """Copy a file from `path_in` to `path_out` with warnings.

    Should be used to sync the homepage in the docs with the one from
    `path_root/README.md`.

    - `base_path: !relative $config_dir` and `--8<-- "README.md"` doesn't work
      and it causes crossrefs to break.
    - symlinking `docs/README.md` to `../README.md` breaks images as well.
    - https://stackoverflow.com/questions/75716969/mkdocs-with-readme-as-index-containing-images-with-broken-links
    - https://stackoverflow.com/questions/73828765/mkdocs-how-to-link-to-the-same-images-in-readme-md-and-docs-index-md-at-the
    """
    with open(path_in, "r") as f:
        readme_content = f.read()
    output = (
        "<!-- DO NOT EDIT! CHANGES WILL BE LOST. edit `README.md` and"
        + f" run `{Path(__file__).relative_to(PATH_ROOT)}` instead. -->\n"
        + readme_content.replace("](docs/assets/", "](assets/")
    )
    with open(path_out, "w+") as f:
        content = f.read()
        if content != output:
            f.write(output)


copy_readme = partial(
    copy_docs_file,
    path_in=PATH_ROOT / "README.md",
    path_out=PATH_ROOT / "docs" / f"{FILENAME_INDEX}.md",
)

copy_contributing = partial(
    copy_docs_file,
    path_in=PATH_ROOT / "CONTRIBUTING.md",
    path_out=PATH_ROOT / "docs" / f"{FILENAME_CONTRIBUTING}.md",
)


# mkdocs events


def on_pre_build(config) -> None:  # type: ignore
    copy_readme()
    copy_contributing()


PATH_VIS_SOURCE = Path(__file__).parent.parent / "src" / "isqx_vis"


def on_post_build(config) -> None:  # type: ignore
    path_out = Path(config["site_dir"])
    path_vis_html = path_out / "vis.html"

    if not (PATH_VIS_SOURCE / "node_modules").exists():
        logger.error(
            "`module_modules` not found.\n"
            f"= help: run `pnpm install` in {PATH_VIS_SOURCE}"
        )
        return
    subprocess.run(["pnpm", "build"], cwd=PATH_VIS_SOURCE, check=True)
    # not removing dir because assets/objects.json exists
    shutil.copytree(
        PATH_VIS_SOURCE / "dist",
        path_out,
        ignore=lambda d, files: ["index.html"] if "index.html" in files else [],
        dirs_exist_ok=True,
    )
    shutil.copy(
        PATH_VIS_SOURCE / "dist" / "index.html",
        path_vis_html,
    )
    logger.info(f"built isqx-vis to {path_vis_html}")


if __name__ == "__main__":
    copy_readme()
    copy_contributing()
