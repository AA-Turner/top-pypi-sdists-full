from ..imports import *
def resolve_python_module_path(module: str, base_dir: str) -> Optional[str]:
    """Resolve a module (dotted or relative) to a file or directory path."""
    # Split module into parts, handling leading dots
    parts = module.split('.')
    current_dir = base_dir
    module_parts = []
    
    # Process leading dots for relative imports
    for part in parts:
        if part == '':
            current_dir = os.path.dirname(current_dir)
        else:
            module_parts.append(part)
    
    # Build path for remaining parts
    module_path = os.path.join(current_dir, *module_parts)
    
    # Check if it’s a file
    file_path = f"{module_path}.py"
    if os.path.isfile(file_path):
        return file_path
    
    # Check if it’s a package (directory with __init__.py)
    if os.path.isdir(module_path):
        init_path = os.path.join(module_path, '__init__.py')
        if os.path.isfile(init_path):
            return init_path
    
    return None

def extract_python_imports(file_path: str) -> List[str]:
    """Extract import statements from a Python file."""
    imports = []
    content = read_from_file(file_path)
    for line in content.split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if line.startswith(('import ', 'from ')):
            parts = line.split()
            if len(parts) > 1:
                # Handle 'import module' or 'from module import ...'
                module = parts[1] if parts[0] == 'import' else parts[1].split('.')[0]
                module = module.split(',')[0].split(' as ')[0]
                imports.append(module)
    return imports

def get_py_script_paths(paths: List[str], module_paths: List[str] = None, imports: List[str] = None) -> Tuple[List[str], List[str]]:
    """Recursively collect module paths and imports from Python files."""
    module_paths = module_paths or []
    imports = imports or []
    paths = make_list(paths)
    for path in paths:
        if not os.path.exists(path):
            print(f"Path not found: {path}")
            continue
        
        if os.path.isdir(path):
            # Search for Python files in directory
            py_files = glob_search(path, '*', ext='.py')
            module_paths, imports = get_py_script_paths(py_files, module_paths, imports)
        else:
            # Add the current script to module_paths
            if path.endswith('.py') and path not in module_paths:
                module_paths.append(path)
            
            # Extract imports
            file_imports = extract_python_imports(path)
            imports.extend(file_imports)
            
            # Handle relative imports (from .module import ...)
            init_dir = os.path.dirname(path)
            content = read_from_file(path)
            for line in content.split('\n'):
                line = line.strip()
                if line.startswith('from .'):
                    module = line.split('from .')[-1].split(' ')[0]
                    resolved_path = resolve_python_module_path(module, init_dir)
                    if resolved_path and resolved_path not in module_paths:
                        module_paths, new_imports = get_py_script_paths([resolved_path], module_paths, imports)
                        imports.extend(new_imports)
    
    return list(set(module_paths)), list(set(imports))
