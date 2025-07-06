import ast
from pathlib import Path
from typing import List
# TODO: rewrite using AST pattern matching (experimental)


def generate_template(file_path: str) -> str:
    """Return a stripped template of ``file_path`` preserving public interface."""
    path = Path(file_path)
    tree = ast.parse(path.read_text())

    new_body: List[ast.stmt] = []
    body = list(tree.body)

    if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) and isinstance(body[0].value.value, str):
        new_body.append(body.pop(0))

    for node in body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            new_body.append(node)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            node.body = [ast.Pass()]
            new_body.append(node)

    tree.body = new_body
    return ast.unparse(tree)


def draft_directory(base: Path, dest: Path) -> List[Path]:
    """Generate templates for ``base`` under ``dest`` directory."""
    generated = []
    for file in base.rglob("*.py"):
        template = generate_template(str(file))
        target = dest / file.relative_to(base)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(template)
        generated.append(target)
    return generated


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Generate interface templates")
    parser.add_argument("base", nargs="?", default="src/tsal")
    parser.add_argument("--dest", default="drafts")
    args = parser.parse_args()

    paths = draft_directory(Path(args.base), Path(args.dest))
    print(f"Generated {len(paths)} templates under {args.dest}")


if __name__ == "__main__":
    main()
