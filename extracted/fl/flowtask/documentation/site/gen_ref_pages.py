"""Generate the code reference pages and navigation."""

import os
import sys
from pathlib import Path
from navconfig import BASE_DIR
import mkdocs_gen_files

# Add parent directory to path so we can import flowtask
sys.path.insert(0, str(Path(__file__).parent.parent))

nav = mkdocs_gen_files.Nav()

def should_skip_module(path):
    """Skip certain files and directories."""
    skip_patterns = [
        '__pycache__',
        '.pyc',
        '.pyo',
        '.git',
        'tests',
        'test_',
        '.pytest_cache',
        'docs',
        'build',
        'dist',
        '.egg-info',
        'venv',
        'env',
        '.venv'
    ]

    path_str = str(path).lower()
    return any(pattern in path_str for pattern in skip_patterns)

def find_flowtask_root():
    """Find the flowtask package root directory."""
    # Try different possible locations
    possible_locations = [
        Path("../flowtask"),  # From docs directory
        Path("flowtask"),     # Direct
        Path("../"),          # Check parent for any Python packages
        Path("./"),           # Current directory
        BASE_DIR.joinpath("flowtask")  # BASE_DIR flowtask
    ]

    for location in possible_locations:
        if location.exists() and location.is_dir():
            # Check if it has Python files
            py_files = list(location.rglob("*.py"))
            if py_files:
                print(f"Found Python package at: {location.absolute()}")
                return location.resolve()

    print("❌ Could not find flowtask package")
    return None

def generate_docs_for_path(src_path, module_prefix="flowtask"):
    """Generate documentation for all Python files in a directory."""
    print(f"🔍 Scanning {src_path} for Python modules...")

    python_files = []
    for path in sorted(src_path.rglob("*.py")):
        if should_skip_module(path):
            print(f"  ⏭️  Skipping: {path}")
            continue
        python_files.append(path)
        print(f"  ✅ Found: {path}")

    print(f"📊 Processing {len(python_files)} Python files...")

    for path in python_files:
        try:
            # Calculate relative path from the source root
            if src_path.name == "flowtask":
                module_path = path.relative_to(src_path.parent)
            else:
                module_path = path.relative_to(src_path)

            doc_path = module_path.with_suffix(".md")
            full_doc_path = Path("reference") / doc_path

            parts = tuple(module_path.parts)

            # Handle __init__.py files
            if parts[-1] == "__init__.py":
                if len(parts) > 1:
                    # Create a directory index
                    parts = parts[:-1]
                    full_doc_path = Path("reference") / Path(*parts) / "index.md"
                    doc_path = Path(*parts) / "index.md"
                else:
                    continue

            # Convert file path to module path
            if parts[-1].endswith(".py"):
                parts = parts[:-1] + (parts[-1][:-3],)

            # Build navigation parts
            nav_parts = []
            for part in parts:
                # Clean up part names for navigation
                clean_part = part.replace("_", " ").title()
                if clean_part.lower() == "flowtask":
                    clean_part = "FlowTask"
                elif clean_part.lower() == "components":
                    clean_part = "Components"
                elif clean_part.lower() == "interfaces":
                    clean_part = "Interfaces"
                nav_parts.append(clean_part)

            nav[nav_parts] = doc_path.as_posix()

            # Create the markdown content
            with mkdocs_gen_files.open(full_doc_path, "w") as fd:
                module_name = ".".join(parts)

                # Create a nice title
                title = nav_parts[-1] if nav_parts else module_name
                print(f"# {title}", file=fd)
                print("", file=fd)

                if parts[-1] == "index" or path.name == "__init__.py":
                    # For package index pages
                    package_name = ".".join(parts[:-1]) if parts[-1] == "index" else ".".join(parts)
                    if package_name:
                        print(f"::: {package_name}", file=fd)
                        print("    options:", file=fd)
                        print("      show_submodules: true", file=fd)
                        print("      show_source: false", file=fd)
                        print("      members_order: alphabetical", file=fd)
                else:
                    # For individual modules
                    print(f"::: {module_name}", file=fd)
                    print("    options:", file=fd)
                    print("      show_source: false", file=fd)
                    print("      members_order: alphabetical", file=fd)

            mkdocs_gen_files.set_edit_path(full_doc_path, path)
            print(f"  📝 Generated: {full_doc_path}")

        except Exception as e:
            print(f"  ❌ Error processing {path}: {e}")

# Main execution
print("🚀 Starting documentation generation...")

# Find the FloTask package
flowtask_root = find_flowtask_root()

if flowtask_root and flowtask_root.name == "flowtask":
    print(f"📦 Processing FloTask package: {flowtask_root}")
    generate_docs_for_path(flowtask_root, "flowtask")
elif flowtask_root:
    # Look for flowtask subdirectory
    flowtask_subdir = flowtask_root / "flowtask"
    if flowtask_subdir.exists():
        print(f"📦 Processing FloTask package: {flowtask_subdir}")
        generate_docs_for_path(flowtask_subdir, "flowtask")
    else:
        print(f"📦 Processing all Python files in: {flowtask_root}")
        generate_docs_for_path(flowtask_root, "")
else:
    print("❌ No Python package found to document")

# Create a comprehensive reference index page
with mkdocs_gen_files.open("reference/index.md", "w") as fd:
    print("# API Reference", file=fd)
    print("", file=fd)
    print("Welcome to the FlowTask API Reference. This section contains detailed documentation for all FlowTask modules, components, and interfaces.", file=fd)
    print("", file=fd)

    if nav:
        print("## Available Modules", file=fd)
        print("", file=fd)
        print("Navigate through the sections using the menu on the left, or explore these main areas:", file=fd)
        print("", file=fd)
        print("- **Components**: Individual processing units that can be chained together in workflows", file=fd)
        print("- **Interfaces**: Common functionality and contracts that components can implement", file=fd)
        print("- **Services**: Core FlowTask services for task management and execution", file=fd)
        print("- **Utilities**: Helper functions and utility classes", file=fd)
        print("", file=fd)
        print("Each module page includes:", file=fd)
        print("", file=fd)
        print("- Detailed class and function documentation", file=fd)
        print("- Parameter descriptions and types", file=fd)
        print("- Usage examples with YAML configurations", file=fd)
        print("- Return value specifications", file=fd)

        # Add some discovered modules to the index
        print("", file=fd)
        print("## Quick Access", file=fd)
        print("", file=fd)

        # Show some navigation items
        nav_items = list(nav.items())[:10]  # First 10 items
        try:
            for nav_path, doc_path in nav_items:
                if isinstance(nav_path, (list, tuple)):
                    title = " > ".join(nav_path)
                    link = f"[{title}]({doc_path})"
                    print(f"- {link}", file=fd)
        except TypeError:
            pass
    else:
        print("⚠️ No modules were found to document.", file=fd)
        print("", file=fd)
        print("Please ensure that:", file=fd)
        print("", file=fd)
        print("1. The `flowtask` package is in the correct location", file=fd)
        print("2. Python files contain proper docstrings", file=fd)
        print("3. The package is importable", file=fd)

# Write the navigation
print("📋 Creating navigation structure...")
with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
    if nav:
        nav_content = nav.build_literate_nav()
        nav_file.writelines(nav_content)
        print(f"✅ Navigation created with {len(list(nav.items()))} items")

        # Debug: show first few navigation items
        print("📌 First few navigation items:")
        try:
            for i, (nav_path, doc_path) in enumerate(list(nav.items())[:5]):
                print(f"  {i+1}. {nav_path} -> {doc_path}")
        except TypeError:
            pass
    else:
        # Create a minimal navigation structure
        nav_file.write("# API Reference\n\n")
        nav_file.write("* [Overview](index.md)\n")
        print("⚠️ Created minimal navigation (no modules found)")

print("🎉 Documentation generation complete!")
print(f"📊 Generated {len(list(nav.items()))} documentation pages")
