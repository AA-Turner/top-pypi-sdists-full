import os
import shutil
import ast
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
import re


class EnhancedStubGenerator:
    """Enhanced stub file generator with proper type hints and documentation."""

    def __init__(self, source_dir: str, target_dir: str, recursive: bool = False):
        self.source_dir = Path(source_dir)
        self.target_dir = Path(target_dir)
        self.recursive = recursive
        self.type_mapping = {
            'str': 'str',
            'int': 'int',
            'float': 'float',
            'bool': 'bool',
            'list': 'List[Any]',
            'dict': 'Dict[str, Any]',
            'tuple': 'Tuple[Any, ...]',
            'set': 'Set[Any]',
            'None': 'None',
            'Any': 'Any',
        }
        self.ast_cache = {} 
        
    def collect_typing_imports(self, stub_lines: List[str]) -> Set[str]:
        """Scan stub lines and collect typing names that must be imported."""
        typing_names = {"Any", "Dict", "List", "Optional", "Tuple", "Union", "Set", "Callable"}
        found: Set[str] = set()
        for line in stub_lines:
            for name in typing_names:
                if re.search(rf"\b{name}\b", line):
                    found.add(name)
        return found

    def _inject_typing_imports(self, lines: List[str]) -> List[str]:
        """Insert a single consolidated 'from typing import ...' based on usage."""
        needed = self.collect_typing_imports(lines)
        lines = [l for l in lines if not l.strip().startswith("from typing import")]
        if needed:
            insert_pos = 1 if (lines and lines[0].lstrip().startswith('"""')) else 0
            lines.insert(insert_pos, f"from typing import {', '.join(sorted(needed))}")
        return lines

    def generate_all_stubs(self):
        # Validate directories
        if not self.source_dir.exists():
            raise FileNotFoundError(f"Source directory {self.source_dir} does not exist")
        if not self.target_dir.exists():
            self.target_dir.mkdir(parents=True, exist_ok=True)

        # Clean up unwanted .pyi files for scripts unless recursive
        if not self.recursive:
            for pyi_file in self.target_dir.glob("*.pyi"):
                if pyi_file.name != "__init__.pyi":
                    pyi_file.unlink()
                    # print(f" Removed unwanted stub: {pyi_file}")

        # Copy __init__.py files if source and target differ
        if self.source_dir.resolve() != self.target_dir.resolve():
            for root, _, files in os.walk(self.source_dir):
                for file in files:
                    if file == "__init__.py":
                        src_path = Path(root) / file
                        rel_path = src_path.relative_to(self.source_dir)
                        dest_path = self.target_dir / rel_path
                        dest_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(src_path, dest_path)
            # print(f" Copied __init__.py files to {self.target_dir}")

        # Collect directories with Python files
        directories = {
            p.parent for p in self.source_dir.rglob("*.py")
            if p.name != "__init__.py"
        }

        # Check if the structure is flat (only root directory contains Python files) -- matrice_common case
        is_flat = len(directories) == 1 and self.source_dir in directories

        if is_flat:
            # Generate detailed stub for flat structure
            self.generate_flat_stub(self.source_dir)
        else:
            # Generate flat stub for root directory (minimal, with imports)
            self.generate_flat_stub(self.source_dir)
            # Generate stubs for subdirectories
            stub_files_generated = 0
            for directory in sorted(directories):
                if directory != self.source_dir:  # Skip root directory
                    stub_path = self.generate_directory_stub(directory)
                    if stub_path:
                        stub_files_generated += 1
            print(f"Generated {stub_files_generated} directory-level __init__.pyi files")

    def parse_file(self, py_file: Path) -> Optional[ast.AST]:
        """Parse a Python file and cache the AST."""
        file_path = str(py_file.resolve())
        if file_path not in self.ast_cache:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    self.ast_cache[file_path] = ast.parse(f.read())
            except Exception as e:
                print(f"   ⚠️ Failed to parse {py_file}: {e}")
                return None
        return self.ast_cache[file_path]

    def generate_flat_stub(self, directory: Path):
        """Generate a detailed __init__.pyi for a flat package, including all definitions."""
        py_files = [f for f in directory.glob("*.py") if f.name != "__init__.py"]
        if not py_files:
            print(f" No Python files found in {directory}, skipping stub generation")
            return

        lines: List[str] = [
            f'"""Auto-generated stubs for package: {directory.name}."""',
            "",
        ]

        all_imports = set()
        all_definitions = {'constants': [], 'functions': [], 'classes': []}

        for py_file in sorted(py_files):
            mod_name = py_file.stem
            tree = self.parse_file(py_file)
            if not tree:
                continue

            # Extract imports and definitions
            imports = self.extract_imports(tree)
            all_imports.update(imports)
            definitions = self.extract_definitions(tree)
            all_definitions['constants'].extend([{**d, 'module': mod_name} for d in definitions['constants']])
            all_definitions['functions'].extend([{**d, 'module': mod_name} for d in definitions['functions']])
            all_definitions['classes'].extend([{**d, 'module': mod_name} for d in definitions['classes']])

            # Generate individual .pyi file if recursive
            if self.recursive:
                stub_path = self.target_dir / f"{mod_name}.pyi"
                stub_lines = [
                    f'"""Auto-generated stub for module: {mod_name}."""',
                    "",
                ]
                if imports:
                    stub_lines.extend(sorted(imports))
                    stub_lines.append("")
                if definitions['constants']:
                    stub_lines.append("# Constants")
                    for const in sorted(definitions['constants'], key=lambda x: x['name']):
                        stub_lines.append(f"{const['name']}: {const['type']}")
                    stub_lines.append("")
                if definitions['functions']:
                    stub_lines.append("# Functions")
                    for func in sorted(definitions['functions'], key=lambda x: x['name']):
                        stub_lines.extend(self.format_function_stub(func))
                    stub_lines.append("")
                if definitions['classes']:
                    stub_lines.append("# Classes")
                    for cls in sorted(definitions['classes'], key=lambda x: x['name']):
                        stub_lines.extend(self.format_class_stub(cls))
                    stub_lines.append("")
                stub_lines = self._inject_typing_imports(stub_lines)
                stub_path.write_text("\n".join(stub_lines), encoding="utf-8")
                # print(f" Generated script stub: {stub_path}")

        # Avoid copying imports into the flat package stub to prevent
        # duplicate re-exports and wrong absolute imports.

        # Add definitions to the main stub
        if all_definitions['constants']:
            lines.append("# Constants")
            for const in sorted(all_definitions['constants'], key=lambda x: (x['module'], x['name'])):
                lines.append(f"{const['name']}: {const['type']} = ...  # From {const['module']}")
            lines.append("")
        if all_definitions['functions']:
            lines.append("# Functions")
            for func in sorted(all_definitions['functions'], key=lambda x: (x['module'], x['name'])):
                lines.append(f"# From {func['module']}")
                lines.extend(self.format_function_stub(func))
                lines.append("")
        if all_definitions['classes']:
            lines.append("# Classes")
            for cls in sorted(all_definitions['classes'], key=lambda x: (x['module'], x['name'])):
                lines.append(f"# From {cls['module']}")
                lines.extend(self.format_class_stub(cls))
                lines.append("")

        # Add module imports
        lines.append(f"from . import {', '.join(sorted(py_file.stem for py_file in py_files))}")
        lines.append("")
        lines.append("def __getattr__(name: str) -> Any: ...")

        # Inject typing imports
        lines = self._inject_typing_imports(lines)

        # Write the stub file
        out_path = self.target_dir / "__init__.pyi"
        out_path.write_text("\n".join(lines), encoding="utf-8")
        print(f"  Generated flat stub: {out_path}")

    def generate_directory_stub(self, directory: Path) -> Optional[Path]:
        """Generate __init__.pyi for a subdirectory."""
        try:
            rel_path = directory.relative_to(self.source_dir)
            stub_path = self.target_dir / rel_path / "__init__.pyi"
            stub_path.parent.mkdir(parents=True, exist_ok=True)
            py_files = [f for f in directory.glob("*.py") if f.name != "__init__.py"]
            if not py_files:
                print(f" Skipping {directory}: No Python files found")
                return None
            stub_content = self.generate_directory_stub_content(py_files, directory)
            with open(stub_path, 'w', encoding='utf-8') as f:
                f.write(stub_content)
            return stub_path
        except Exception as e:
            print(f"   Failed to generate __init__.pyi for directory {directory}: {e}")
            return None

    def generate_directory_stub_content(self, py_files: List[Path], directory: Path) -> str:
        lines: List[str] = []
        module_name = ".".join(directory.relative_to(self.source_dir).parts) or self.source_dir.name
        lines.append(f'"""Stub file for {module_name} directory."""')
        lines.append("")

        all_imports = set()
        all_definitions = {'constants': [], 'functions': [], 'classes': []}

        for py_file in sorted(py_files):
            tree = self.parse_file(py_file)
            if not tree:
                continue
            mod_name = py_file.stem
            imports = self.extract_imports(tree)
            all_imports.update(imports)
            definitions = self.extract_definitions(tree)
            all_definitions['constants'].extend([{**d, 'module': mod_name} for d in definitions['constants']])
            all_definitions['functions'].extend([{**d, 'module': mod_name} for d in definitions['functions']])
            all_definitions['classes'].extend([{**d, 'module': mod_name} for d in definitions['classes']])

            # Generate .pyi for individual script only if recursive
            if self.recursive:
                stub_path = self.target_dir / py_file.relative_to(self.source_dir).with_suffix(".pyi")
                stub_path.parent.mkdir(parents=True, exist_ok=True)
                stub_lines = [
                    f'"""Auto-generated stub for module: {mod_name}."""',
                    "",
                ]
                if imports:
                    stub_lines.extend(sorted(imports))
                    stub_lines.append("")
                if definitions['constants']:
                    stub_lines.append("# Constants")
                    for const in sorted(definitions['constants'], key=lambda x: x['name']):
                        stub_lines.append(f"{const['name']}: {const['type']}")
                    stub_lines.append("")
                if definitions['functions']:
                    stub_lines.append("# Functions")
                    for func in sorted(definitions['functions'], key=lambda x: x['name']):
                        stub_lines.extend(self.format_function_stub(func))
                    stub_lines.append("")
                if definitions['classes']:
                    stub_lines.append("# Classes")
                    for cls in sorted(definitions['classes'], key=lambda x: x['name']):
                        stub_lines.extend(self.format_class_stub(cls))
                    stub_lines.append("")
                stub_lines = self._inject_typing_imports(stub_lines)
                stub_path.write_text("\n".join(stub_lines), encoding="utf-8")
                print(f"  Generated script stub: {stub_path}")

        if all_imports:
            lines.extend(sorted(all_imports))
            lines.append("")

        if all_definitions['constants']:
            lines.append("# Constants")
            for const in sorted(all_definitions['constants'], key=lambda x: (x['module'], x['name'])):
                lines.append(f"{const['name']}: {const['type']} = ...  # From {const['module']}")
            lines.append("")
        if all_definitions['functions']:
            lines.append("# Functions")
            for func in sorted(all_definitions['functions'], key=lambda x: (x['module'], x['name'])):
                lines.append(f"# From {func['module']}")
                lines.extend(self.format_function_stub(func))
                lines.append("")
        if all_definitions['classes']:
            lines.append("# Classes")
            for cls in sorted(all_definitions['classes'], key=lambda x: (x['module'], x['name'])):
                lines.append(f"# From {cls['module']}")
                lines.extend(self.format_class_stub(cls))
                lines.append("")

        lines.append(f"from . import {', '.join(sorted(py_file.stem for py_file in py_files))}")
        lines = self._inject_typing_imports(lines)
        return "\n".join(lines)

    def extract_imports(self, tree: ast.AST) -> List[str]:
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                # Skip absolute imports in stubs to avoid missing third-party modules
                continue
            elif isinstance(node, ast.ImportFrom):
                # Preserve relative import level with leading dots
                dots = "." * getattr(node, "level", 0)
                module = (dots + (node.module or "")) if dots else (node.module or "")
                # Skip absolute from-imports
                if not module.startswith('.'):
                    continue
                names = [alias.name for alias in node.names]
                if len(names) == 1:
                    imports.append(f"from {module} import {names[0]}")
                else:
                    imports.append(f"from {module} import {', '.join(names)}")
        return imports

    def extract_definitions(self, tree: ast.AST) -> Dict:
        definitions = {
            'constants': [],
            'functions': [],
            'classes': []
        }
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                func_def = self.extract_function_info(node)
                if not func_def['name'].startswith('_'):
                    definitions['functions'].append(func_def)
            elif isinstance(node, ast.ClassDef) and not node.name.startswith('_'):
                class_def = self.extract_class_info(node)
                definitions['classes'].append(class_def)
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and not target.id.startswith('_'):
                        const_info = {
                            'name': target.id,
                            'type': self.infer_type_from_value(node.value) if self.recursive else "Any"
                        }
                        definitions['constants'].append(const_info)
        return definitions

    def extract_function_info(self, node: ast.AST) -> Dict:
        params = []
        for arg in node.args.args:
            param_info = {
                'name': arg.arg,
                'type': self.extract_annotation(arg.annotation),
                'default': None
            }
            params.append(param_info)
        if node.args.defaults:
            defaults_start = len(params) - len(node.args.defaults)
            for i, default in enumerate(node.args.defaults):
                try:
                    params[defaults_start + i]['default'] = ast.unparse(default)
                except Exception:
                    params[defaults_start + i]['default'] = "..."
        if node.args.vararg:
            params.append({'name': f"*{node.args.vararg.arg}", 'type': 'Any', 'default': None})
        if node.args.kwarg:
            params.append({'name': f"**{node.args.kwarg.arg}", 'type': 'Any', 'default': None})
        return_type = self.extract_annotation(node.returns)
        if node.name in ('__init__', 'stop_streaming', 'cleanup', 'start_logging', 'update_status'):
            return_type = 'None'
        return {
            'name': node.name,
            'params': params,
            'return_type': return_type,
            'docstring': self.extract_docstring(node),
            'is_async': isinstance(node, ast.AsyncFunctionDef),
            'decorators': [self._safe_unparse(d) for d in node.decorator_list]
        }

    def extract_class_info(self, node: ast.ClassDef) -> Dict:
        methods = []
        class_vars = []
        init_method = None
        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                method_info = self.extract_function_info(item)
                if item.name == '__init__':
                    init_method = method_info
                elif not item.name.startswith('_'):
                    methods.append(method_info)
            elif isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name) and not target.id.startswith('_'):
                        class_vars.append({
                            'name': target.id,
                            'type': self.infer_type_from_value(item.value) if self.recursive else "Any"
                        })
        return {
            'name': node.name,
            'bases': [self._safe_unparse(base) for base in node.bases],
            'methods': methods,
            'init_method': init_method,
            'class_vars': class_vars,
            'docstring': self.extract_docstring(node),
            'decorators': [self._safe_unparse(d) for d in node.decorator_list]
        }

    def _safe_unparse(self, node: ast.AST) -> str:
        try:
            return ast.unparse(node)
        except Exception:
            return "Any"

    def extract_annotation(self, annotation) -> str:
        if annotation is None:
            return "Any"
        try:
            ann_str = ast.unparse(annotation)
        except Exception:
            return "Any"
        allowed = {
            "str", "int", "float", "bool", "list", "dict", "tuple", "set", "None",
            "Any", "Optional", "List", "Dict", "Tuple", "Set", "Union", "Callable", "Session"
        }
        # Replace any unknown identifiers within the annotation string with Any
        def _replace(m: re.Match[str]) -> str:
            name = m.group(0)
            return name if name in allowed else "Any"
        sanitized = re.sub(r"\b[A-Za-z_][A-Za-z0-9_]*\b", _replace, ann_str)
        # If everything was replaced leaving awkward constructs, default to Any
        if sanitized.strip() == "" or sanitized.strip() == ann_str.strip() and re.search(r"\b[A-Za-z_][A-Za-z0-9_]*\b", ann_str) and any(tok not in allowed for tok in re.findall(r"\b[A-Za-z_][A-Za-z0-9_]*\b", ann_str)):
            return "Any"
        return sanitized

    def extract_docstring(self, node) -> Optional[str]:
        if (
            node.body
            and isinstance(node.body[0], ast.Expr)
            and isinstance(node.body[0].value, ast.Constant)
            and isinstance(node.body[0].value.value, str)
        ):
            docstring = node.body[0].value.value
            lines = docstring.splitlines()
            if not lines:
                return None
            non_empty_lines = [line for line in lines if line.strip()]
            if not non_empty_lines:
                return "\n".join(lines).strip()
            min_indent = min(len(line) - len(line.lstrip()) for line in non_empty_lines)
            cleaned_lines = [line[min_indent:] if line.strip() else line for line in lines]
            return "\n".join(cleaned_lines).strip()
        return None

    def infer_type_from_value(self, value) -> str:
        if isinstance(value, ast.Constant):
            if value.value is None:
                return "None"
            elif isinstance(value.value, bool):
                return "bool"
            elif isinstance(value.value, int):
                return "int"
            elif isinstance(value.value, float):
                return "float"
            elif isinstance(value.value, str):
                return "str"
        elif isinstance(value, ast.List):
            return "List[Any]"
        elif isinstance(value, ast.Dict):
            return "Dict[Any, Any]"
        elif isinstance(value, ast.Tuple):
            return "Tuple[Any, ...]"
        elif isinstance(value, ast.Set):
            return "Set[Any]"
        return "Any"
    
    def format_function_stub(self, func_info: Dict) -> List[str]:
        lines: List[str] = []
        param_strs = []
        for param in func_info["params"]:
            param_str = (
                f"{param['name']}: {param['type']}"
                if self.recursive or param["type"] != "Any"
                else param["name"]
            )
            if param.get("default") is not None:
                param_str += f" = {param['default']}"
            param_strs.append(param_str)
        params_str = ", ".join(param_strs)
        prefix = "async def" if func_info["is_async"] else "def"
        return_type = func_info["return_type"]

        doc = func_info.get("docstring") or ""
        if doc.strip():
            lines.append(f"{prefix} {func_info['name']}({params_str}) -> {return_type}:")
            doc_lines = doc.splitlines()
            lines.append('    """')
            for line in doc_lines:
                lines.append(f"    {line.rstrip()}")
            lines.append('    """')
            lines.append("    ...")
        else:
            lines.append(f"{prefix} {func_info['name']}({params_str}) -> {return_type}: ...")
        return lines
    
    def format_class_stub(self, class_info: Dict) -> List[str]:
        lines: List[str] = []
        safe_builtin_bases = {"object", "Exception", "BaseException"}
        safe_bases = [b for b in class_info.get("bases", []) if b in safe_builtin_bases]
        bases_str = f"({', '.join(safe_bases)})" if safe_bases else ""
        lines.append(f"class {class_info['name']}{bases_str}:")

        emitted_stmt = False  # tracks real statements in the class body

        # Docstring as comments (does NOT count as body)
        doc = class_info.get("docstring") or ""
        if doc:
            for line in doc.splitlines():
                lines.append(f"    # {line.rstrip()}" if line.strip() else "    #")
            lines.append("")

        if class_info.get("init_method"):
            for line in self.format_function_stub(class_info["init_method"]):
                lines.append(f"    {line}")
            lines.append("")
            emitted_stmt = True

        class_vars = class_info.get("class_vars") or []
        if class_vars:
            for var in sorted(class_vars, key=lambda x: x["name"]):
                lines.append(f"    {var['name']}: {var['type']}")
            lines.append("")
            emitted_stmt = True

        methods = class_info.get("methods") or []
        if methods:
            for method in sorted(methods, key=lambda x: x["name"]):
                for line in self.format_function_stub(method):
                    lines.append(f"    {line}")
                lines.append("")
            emitted_stmt = True
        else:
            if class_info["name"] == "ErrorType":
                existing = {v["name"] for v in class_vars}
                if "INTERNAL" not in existing:
                    lines.append("    INTERNAL: object = ...")
                    emitted_stmt = True

        if not emitted_stmt:
            lines.append("    ...")

        return lines

    def generate_main_init_stub(self):
        """Generate a minimal __init__.pyi for non-flat structures."""
        init_stub_path = self.target_dir / "__init__.pyi"
        lines = [
            f'"""Stub file for {self.target_dir.name} package."""',
            "",
            "from typing import Any",
            "",
            "# Re-export all public symbols",
        ]

        # Root-level modules
        root_py_files = [f for f in self.source_dir.glob("*.py") if f.name != "__init__.py"]
        if root_py_files:
            module_names = [f.stem for f in sorted(root_py_files)]
            lines.append(f"from . import {', '.join(module_names)}")

        # Subdirectory modules
        subdirs = {
            p.parent for p in self.source_dir.rglob("*.py")
            if p.name != "__init__.py" and p.parent != self.source_dir
        }
        for subdir in sorted(subdirs):
            rel_path = subdir.relative_to(self.source_dir)
            module_path = ".".join(rel_path.parts)
            subdir_files = [f for f in subdir.glob("*.py") if f.name != "__init__.py"]
            if subdir_files:
                module_names = [f.stem for f in sorted(subdir_files)]
                lines.append(f"from .{module_path} import {', '.join(module_names)}")

        lines.append("")
        lines.append("def __getattr__(name: str) -> Any: ...")
        lines = self._inject_typing_imports(lines)

        with open(init_stub_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(lines))
        print(f"   Generated main stub: {init_stub_path}")


def main():
    source_dir = "src/matrice_common"
    target_dir = "src/matrice_common"
    recursive = True

    generator = EnhancedStubGenerator(source_dir, target_dir, recursive=recursive)
    generator.generate_all_stubs()

    print("Stub generation complete.")


if __name__ == "__main__":
    main()
