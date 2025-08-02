from functools import lru_cache

from fastapi.templating import Jinja2Templates

from project.core.const import ProjectPaths


def create_jinja2_templates() -> Jinja2Templates:
    return Jinja2Templates(directory=ProjectPaths.templates_dirpath)


@lru_cache()
def get_cached_jinja2_templates() -> Jinja2Templates:
    return create_jinja2_templates()
