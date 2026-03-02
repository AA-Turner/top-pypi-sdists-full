from pathlib import Path
from polylith_cli.polylith.files import create_file
template_docstring = '"""\n{description}\n"""\n\n'
template_content = 'from {namespace}.{package} import {modulename}\n\n__all__ = ["{modulename}"]\n'

def to_namespaced_path(package: str) -> str:
    parts = package.split('/')
    return '.'.join(parts)

def create_interface(path: Path, options: dict) -> None:
    interface = create_file(path, '__init__.py')
    namespace = options['namespace']
    package = options['package']
    description = options['description']
    modulename = options['modulename']
    package_path = to_namespaced_path(package)
    docstring = template_docstring.format(description=description) if description else ''
    content = template_content.format(namespace=namespace, package=package_path, modulename=modulename)
    interface.write_text(docstring + content)