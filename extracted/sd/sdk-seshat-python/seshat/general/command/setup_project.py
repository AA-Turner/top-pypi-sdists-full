import os
import pathlib
import re

import typer

from seshat.general.exceptions import InvalidArgumentsError

TEMPLATE_PATH = os.path.join(pathlib.Path(__file__).parent.parent, "template")

RECOMMENDATION = "recommendation"
PYPROJECT = "pyproject"
RECOMMENDATION_JUPYTER = "recommendation_nb"
CONFIG = "config"
ENV = "env"
README = "readme"
JOBIGNORE = "jobignore"

USE_CASES = [RECOMMENDATION]
TEMPLATE_TO_FILE_MAP = {
    RECOMMENDATION: "recommender.py-tmpl",
    RECOMMENDATION_JUPYTER: "recommender-jupyter.ipynb-tmpl",
    CONFIG: "config.py-tmpl",
    ENV: "env-templ",
    PYPROJECT: "pyproject._toml-tmpl",
    README: "README.md-tmpl",
    JOBIGNORE: "jobignore-tmpl",
}

PKG_TREE = {
    RECOMMENDATION: {
        "recommender": {
            "__init__.py": RECOMMENDATION,
            "main.ipynb": RECOMMENDATION_JUPYTER,
        }
    }
}


class SetUpProjectCommand:
    ctx: dict

    def __init__(self, project_name, usecase, root_path, overwrite=True, report=True):
        if usecase not in USE_CASES:
            raise InvalidArgumentsError(
                f"usecase bust must be one of these: {' - '.join(USE_CASES)}"
            )
        self.usecase = usecase
        self.project_name = project_name
        self.root_path = root_path
        self.overwrite = overwrite
        self.report = report

        self.ctx = {r"{_PROJECT_NAME}": self.project_name}

    def handle(self):
        tree = self.generate_dir_tree()
        self.make_dir(tree, self.root_path)

    def generate_dir_tree(self):
        return {
            "packages": PKG_TREE[self.usecase],
            "pyproject.toml": PYPROJECT,
            self.project_name: {"config.py": CONFIG, ".env": ENV},
            "README.md": README,
            ".jobignore": JOBIGNORE,
            "data": {},
        }

    def make_dir(self, tree: dict, root_path):
        for node, val in tree.items():
            if isinstance(val, dict):
                self.echo(f"Creating {node} directory in {root_path}")
                dir_path = os.path.join(root_path, node)
                os.makedirs(dir_path, exist_ok=True)
                self.make_dir(tree[node], dir_path)
            else:
                if not self.overwrite and os.path.exists(os.path.join(root_path, node)):
                    continue
                self.echo(f"Adding {node} to {root_path}")
                self.copy_template(
                    self.get_template_path(val), os.path.join(root_path, node), self.ctx
                )

    def copy_template(self, template_path, dst_path, ctx):
        if ctx is None:
            ctx = {}
        with open(template_path, "r") as template:
            content = template.read()
            for pattern, repl in ctx.items():
                content = re.sub(pattern, repl, content)
        with open(dst_path, "w") as dst:
            dst.write(content)

    def get_template_path(self, template):
        return os.path.join(TEMPLATE_PATH, TEMPLATE_TO_FILE_MAP[template])

    def echo(self, msg, *args, **kwargs):
        if not self.report:
            return
        typer.echo(msg, *args, **kwargs)
