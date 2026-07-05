from pathlib import Path
from polylith_cli.polylith.bricks.brick import create_brick
from polylith_cli.polylith.repo import bases_dir
from polylith_cli.polylith.test import create_test

def create_base(path: Path, options: dict) -> None:
    extra = {'brick': bases_dir}
    base_options = {**options, **extra}
    create_brick(path, base_options)
    create_test(path, base_options)