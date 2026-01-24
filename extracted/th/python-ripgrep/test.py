from python_ripgrep import PySortMode, PySortModeKind, files, search


def test_search_with_kwargs() -> None:
    print("Testing search with keyword arguments:")
    results = search(patterns=["def"], paths=["src"], globs=["*.rs"], line_number=True)
    print(f"Found {len(results)} matches")
    for result in results:
        print(result)
    print()


def test_files_with_kwargs() -> None:
    print("Testing files with keyword arguments:")
    results = files(
        patterns=[".*"],
        paths=["src"],
        globs=["*.rs"],
        sort=PySortMode(PySortModeKind.Path),
    )
    print(f"Found {len(results)} files")
    for result in results:
        print(result)
    print()


if __name__ == "__main__":
    # Test both new and legacy interfaces
    test_search_with_kwargs()
    test_files_with_kwargs()
