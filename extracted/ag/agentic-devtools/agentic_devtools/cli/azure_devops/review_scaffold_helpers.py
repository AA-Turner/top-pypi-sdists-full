"""Path and presentation helpers for review scaffolding."""

from .review_state import normalize_file_path


def _get_folder_for_path(file_path: str) -> str:
    """Get the top-level folder name for a file path.

    Args:
        file_path: Repository file path (with or without leading slash).

    Returns:
        Top-level folder name, or "root" for root-level files.
    """
    from .review_helpers import get_root_folder

    normalized = normalize_file_path(file_path)
    return get_root_folder(normalized.lstrip("/"))


def _get_file_name(file_path: str) -> str:
    """Get the base file name from a file path.

    Args:
        file_path: Repository file path.

    Returns:
        Base file name (last path segment).
    """
    normalized = normalize_file_path(file_path)
    return normalized.split("/")[-1]


def _print_dry_run_plan(
    pull_request_id: int,
    files: list[str],
    folders: dict[str, list[str]],
) -> None:
    """Print the scaffolding plan without making API calls.

    Folder-level threads have been eliminated; file threads, the overall
    PR summary thread, and a Review Activity Log thread are created
    (N + 3 thread-creation POST calls in total; additional non-POST calls
    may be made when initializing the activity log).

    Args:
        pull_request_id: Pull request ID.
        files: List of file paths.
        folders: Mapping of folder name to list of file paths.
    """
    print(f"[DRY RUN] Scaffolding plan for PR {pull_request_id}:")
    for file_path in files:
        normalized = normalize_file_path(file_path)
        print(f"  [DRY RUN] Would create file summary thread for {normalized}")
    for folder_name in folders:
        print(f"  [DRY RUN] Would group files under folder: {folder_name}")
    print("  [DRY RUN] Would create overall PR summary thread")
    print("  [DRY RUN] Would create Review Activity Log thread")
    api_calls = len(files) + 3
    print(f"  [DRY RUN] Total API calls: {api_calls}")
