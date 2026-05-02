#!/usr/bin/env python3
from pathlib import Path
import ast
import re
import yaml
import json

# ── CONFIGURATION ──────────────────────────────────────────────────────────────

COMPONENTS_DIR = Path("/home/jesuslara/proyectos/parallel/flowtask/flowtask/components")
TASKS_DIR = Path("/home/ubuntu/symbits/tasks/master/programs/")
NO_EXAMPLES_TXT = Path("no_examples.txt")

DOCSTRING_RE = re.compile(r'(""".*?""")', re.DOTALL)

# ── HELPER FUNCTIONS ────────────────────────────────────────────────────────────

def get_all_components(root_dir: Path):
    """
    Return list of (class_name, file_path) for every class in .py under root_dir.
    """
    components = []
    for py_file in root_dir.rglob("*.py"):
        try:
            src = py_file.read_text(encoding="utf-8")
            tree = ast.parse(src)
        except Exception:
            continue
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                components.append((node.name, py_file))
    return components

def find_example_for(name: str, tasks_root: Path):
    """
    Recursively scan all .yaml/.yml/.json under tasks_root.
    Inside each file, look in the top-level 'steps' list for
    a dict with key == name, and return that snippet.
    """
    for task_file in tasks_root.rglob("*"):
        if task_file.suffix.lower() in {".yml", ".yaml", ".json"}:
            try:
                raw = task_file.read_text(encoding="utf-8")
                data = (
                    yaml.safe_load(raw)
                    if task_file.suffix.lower() in {".yml", ".yaml"}
                    else json.loads(raw)
                )
            except Exception:
                continue

            # If the file is a single dict with a 'steps' key,
            # iterate its steps; otherwise skip.
            if isinstance(data, dict) and "steps" in data:
                for step in data["steps"]:
                    if isinstance(step, dict) and name in step:
                        # Return just { name: { … } } to pretty‑dump later
                        return { name: step[name] }
    return None


def inject_example_into_docstring(source_path: Path, example_dict: dict):
    """
    Load the Python file, find the first triple-quoted docstring,
    skip if already has "Example:", otherwise append the YAML example block.
    Returns True if modified, False otherwise.
    """
    text = source_path.read_text(encoding="utf-8")
    m = DOCSTRING_RE.search(text)
    if not m:
        return False
    doc = m.group(1)
    if "Example:" in doc:
        return False   # already has one

    # Build indented YAML block
    indent = " " * 8
    yaml_snip = yaml.safe_dump(example_dict, sort_keys=False).rstrip()
    indented = "\n".join(indent + line for line in yaml_snip.splitlines())
    example_section = (
        f"\n\n{indent}Example:\n\n"
        f"{indent}```yaml\n"
        f"{indented}\n"
        f"{indent}```\n\n    \"\"\""
    )

    # Splice before the closing triple-quotes
    new_doc = doc[:-3] + example_section
    new_text = text[:m.start(1)] + new_doc + text[m.end(1):]
    source_path.write_text(new_text, encoding="utf-8")
    return True

# ── MAIN ────────────────────────────────────────────────────────────────────────

def main():
    components = get_all_components(COMPONENTS_DIR)
    missing = []

    for comp_name, comp_file in components:
        example = find_example_for(comp_name, TASKS_DIR)
        if example:
            if inject_example_into_docstring(comp_file, example):
                print(f"[+] Injected example into {comp_name} ({comp_file})")
            else:
                print(f"[~] Skipped {comp_name}: already has Example section")
        else:
            print(f"[-] No example found for {comp_name}")
            missing.append(comp_name)

    if missing:
        NO_EXAMPLES_TXT.write_text("\n".join(missing), encoding="utf-8")
        print(f"⚠️  Wrote {len(missing)} missing components to {NO_EXAMPLES_TXT}")
    else:
        NO_EXAMPLES_TXT.unlink(missing_ok=True)
        print("✅ All components have examples.")

if __name__ == "__main__":
    main()
