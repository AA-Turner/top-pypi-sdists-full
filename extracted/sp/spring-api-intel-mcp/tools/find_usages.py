from core.indexer import CodeIndex

def find_usages(index: CodeIndex, class_name: str) -> str:
    """Find all classes that reference a given class name."""
    results = []
    target = class_name.lower()

    for file_path, source in index.file_contents.items():
        if target in source.lower():
            owning_class = next(
                (name for name, info in index.classes.items() if info.file_path == file_path),
                file_path.split("/")[-1].replace(".java", "")
            )
            lines = [
                f"    line {i+1}: {line.strip()}"
                for i, line in enumerate(source.splitlines())
                if target in line.lower() and line.strip() and not line.strip().startswith("//")
            ]
            if lines:
                results.append(f"\n  {owning_class}  ({file_path})")
                results.extend(lines[:8])
                if len(lines) > 5:
                    results.append(f"    ... and {len(lines) - 5} more")

    if not results:
        return f"No usages of '{class_name}' found in the indexed codebase."

    return f"Usages of '{class_name}':\n" + "\n".join(results)