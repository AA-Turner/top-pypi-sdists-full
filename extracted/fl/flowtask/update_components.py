import ast
import os
import re
import argparse

# --- Configuration ---
COMPONENTS_DIR = "flowtask/components"
TARGET_BASE_CLASS = "FlowComponent"
VERSION_ATTR_LINE = '    _version = "1.0.0"'

# --- Helpers ---

def get_classes_in_file(filepath):
    """Parses a file and returns a list of (ClassNode, ClassName, BaseClasses)."""
    with open(filepath, "r", encoding="utf-8") as f:
        try:
            tree = ast.parse(f.read(), filename=filepath)
        except SyntaxError:
            return []

    classes = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            bases = []
            for base in node.bases:
                if isinstance(base, ast.Name):
                    bases.append(base.id)
                elif isinstance(base, ast.Attribute):
                    bases.append(base.attr)
            classes.append((node, node.name, bases))
    return classes

def build_inheritance_map(directory):
    """Builds a map of Class -> [ParentClasses] and a set of FlowComponent descendants."""
    class_parents = {}
    class_files = {}

    # Scan all files
    for root, dirs, files in os.walk(directory):
        for file in files:
            if not file.endswith(".py"):
                continue
            filepath = os.path.join(root, file)
            for node, name, bases in get_classes_in_file(filepath):
                class_parents[name] = bases
                class_files[name] = filepath

    # Identify descendants of TARGET_BASE_CLASS
    flow_components = set()

    def is_descendant(name, visited):
        if name == TARGET_BASE_CLASS:
            return True
        if name in visited:
            return False
        visited.add(name)

        bases = class_parents.get(name, [])
        for base in bases:
            if is_descendant(base, visited):
                return True
        return False

    for name in class_parents:
        if is_descendant(name, set()):
            flow_components.add(name)

    if TARGET_BASE_CLASS in flow_components:
        flow_components.remove(TARGET_BASE_CLASS)

    return sorted(list(flow_components)), class_files

def convert_to_markdown_table(rows):
    """Converts list of rows to Markdown table."""
    # Ensure version is present
    has_version = False
    for r in rows:
        if r[0].lower() == 'version':
            has_version = True
            break

    if not has_version:
        rows.append(("version", "No", "version of component"))

    md = "| Name | Required | Summary |\n|---|---|---|\n"
    for name, required, summary in rows:
        md += f"| {name} | {required} | {summary} |\n"
    return md

def extract_yaml_block(docstring):
    match = re.search(r'```yaml(.*?)```', docstring, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

def process_docstring(class_name, docstring, module_docstring=None):
    """
    Refactors the docstring.
    """
    if docstring is None:
        docstring = ""

    # Clean up common indentation
    lines = docstring.split('\n')
    # If first line is empty, remove it? No, keeping structure.

    cleaned_lines = []

    existing_yaml = extract_yaml_block(docstring)
    if not existing_yaml and module_docstring:
        existing_yaml = extract_yaml_block(module_docstring)

    # Remove existing YAML and Tables from description to avoid duplication
    in_yaml = False
    for line in lines:
        stripped = line.strip()
        if '```yaml' in stripped:
            in_yaml = True
            continue
        if '```' in stripped and in_yaml:
            in_yaml = False
            continue
        if in_yaml:
            continue

        if stripped.startswith('+--') or stripped.startswith('===') or '.. table::' in line:
            continue
        # Check for table rows (heuristics)
        # Often RST tables have lines like "| name | req |"
        # We'll skip cleaning table rows too aggressively to avoid deleting text,
        # but if we see table headers, skip.
        if "| Name |" in line or "| Required |" in line:
            continue

        cleaned_lines.append(line)

    description = "\n".join(cleaned_lines).strip()
    if not description:
        description = f"{class_name}."

    # Build Table
    # We are generating a new one.
    # Attempt to preserve attributes if we can find them would be ideal,
    # but per instruction "If there is any component without a parameters table, add a parameters table...".
    # We will just add the default table with version.

    rows = []
    # If we want to be smart, we could parse existing RST table here.
    # For now, just "version".
    rows.append(("version", "No", "version of component"))

    table_md = convert_to_markdown_table(rows)

    # YAML Block
    if not existing_yaml:
        yaml_block = f"```yaml\n    {class_name}:\n      # attributes here\n    ```"
    else:
        # Re-indent existing yaml
        # It's already stripped in extraction
        yaml_lines = existing_yaml.split('\n')
        # We indent it by 4 spaces relative to the block
        # But wait, inside the docstring which is indented by 4,
        # the block content should be indented.

        # docstring indentation:
        # """
        # Description
        #
        # Table
        #
        # Example:
        #
        # ```yaml
        # ...
        # ```
        # """

        formatted_yaml_lines = []
        for l in yaml_lines:
            formatted_yaml_lines.append(l.strip()) # Flatten

        yaml_content = "\n".join(formatted_yaml_lines)
        # Indent content
        yaml_content_indented = "\n".join(["      " + l for l in formatted_yaml_lines])

        yaml_block = f"```yaml\n{yaml_content_indented}\n    ```"

    # Final Assembly
    # We use 4 spaces indentation for the body of the docstring.
    new_doc = f"""{description}

    {table_md}

    Example:

    {yaml_block}"""

    return new_doc

def update_file(filepath, class_name):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    try:
        tree = ast.parse(content)
    except:
        return # Skip broken files

    class_node = None
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            class_node = node
            break

    if not class_node:
        return

    original_doc = ast.get_docstring(class_node, clean=True) # clean=True to get text
    module_doc = ast.get_docstring(tree, clean=True)

    new_doc_content = process_docstring(class_name, original_doc, module_doc)

    # Formatting as a Docstring Literal
    # It needs to be indented.
    # The docstring itself is usually indented by 4 spaces.
    # The content *inside* `"""` ... `"""` is what we built.

    # But new_doc_content lines might not be indented.
    # We need to indent them.
    lines = new_doc_content.split('\n')
    indented_lines = []
    for i, line in enumerate(lines):
        if i == 0 and line.strip():
            indented_lines.append(line)  # First line often on same line as quotes or next
        else:
            indented_lines.append("    " + line if line.strip() else "")

    # Actually, simpler:
    # """
    # Line 1
    # Line 2
    # """
    # All lines inside should be indented relative to the class, EXCEPT if we put the first line right after quotes.
    # Let's use the multi-line style starting on next line.

    indented_content = "\n".join(["    " + l if l.strip() else "" for l in lines])
    new_doc_formatted = f'    """\n{indented_content}\n    """'

    file_lines = content.splitlines(keepends=True)

    # Check for _version
    has_version = False
    for node in class_node.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == '_version':
                    has_version = True

    # Prepare Edits
    edits = []

    # Docstring Replacement/Insertion
    doc_node = None
    if (len(class_node.body) > 0 and
        isinstance(class_node.body[0], ast.Expr) and
        isinstance(class_node.body[0].value, (ast.Str, ast.Constant))):
        doc_node = class_node.body[0]

    if doc_node:
        s = doc_node.lineno - 1
        e = doc_node.end_lineno
        replacement = [new_doc_formatted + "\n"]
        if not has_version:
            replacement.append(VERSION_ATTR_LINE + "\n")
        edits.append((s, e, replacement))
    else:
        # Insert after class def
        # Find the line ending with ':'
        idx = class_node.lineno - 1
        found = False
        while idx < len(file_lines):
            line = file_lines[idx].strip()
            # Handle comments, but simplified
            if line.endswith(':') or line.split('#')[0].strip().endswith(':'):
                found = True
                break
            idx += 1

        insert_idx = idx + 1
        replacement = [new_doc_formatted + "\n"]
        if not has_version:
            replacement.append(VERSION_ATTR_LINE + "\n")
        edits.append((insert_idx, insert_idx, replacement))

    # Apply Edits
    edits.sort(key=lambda x: x[0], reverse=True)

    for s, e, text in edits:
        file_lines[s:e] = text

    with open(filepath, "w", encoding="utf-8") as f:
        f.writelines(file_lines)
    print(f"Updated {class_name} in {filepath}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--files", nargs="*", help="Specific files to process")
    args = parser.parse_args()

    flow_components, class_files = build_inheritance_map(COMPONENTS_DIR)

    targets = flow_components
    if args.files:
         targets = [c for c in flow_components if class_files.get(c) in args.files or c in args.files]

    if args.limit > 0:
        targets = targets[args.offset : args.offset + args.limit]

    print(f"Processing {len(targets)} components...")

    for class_name in targets:
        filepath = class_files.get(class_name)
        if filepath:
            update_file(filepath, class_name)

if __name__ == "__main__":
    main()
