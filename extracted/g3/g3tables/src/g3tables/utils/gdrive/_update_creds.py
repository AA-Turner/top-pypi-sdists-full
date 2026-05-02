import argparse
import os

from ._gdrive import CredsFileManager


def main():
    manager = CredsFileManager()
    creds_dir = os.path.dirname(manager.get_creds_file(ensure_is_valid=False))
    parser = argparse.ArgumentParser(
        description=(
            f'Update Google Drive service account credentials file.\n'
            f'If the contents of the file are a valid JSON object, '
            f'they are copied to the directory of the g3tables library: '
            f'"{creds_dir}".'
            )
        )
    parser.add_argument(
        "creds_file_path",
        nargs="?",
        type=str,
        help=(
            "Path to the new Google Drive service account credentials file. "
            "If not provided, the user will be prompted to input "
            "the file path via the console."
            )
        )
    args = parser.parse_args()
    path = args.creds_file_path
    if path:
        try:
            manager.update_creds_file(path)
        except Exception as exp:
            print(f'Failed to update the credentials file ({exp}).\n')
            manager.update_creds_file_from_input()
    else:
        manager.update_creds_file_from_input()


if __name__ == "__main__":
    main()
