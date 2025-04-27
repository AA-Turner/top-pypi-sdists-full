# /// script
# dependencies = [
#     "urllib3>=2",
# ]
# ///

import concurrent.futures
import json
import shutil
import tarfile
import time
import traceback
import zipfile
from io import BytesIO
from pathlib import Path

import urllib3

PACKAGES_URL = 'https://hugovk.github.io/top-pypi-packages/top-pypi-packages.min.json'

ROOT = Path(__file__).resolve().parent
SDIST_ROOT = ROOT / 'pypi-sdists'
SDIST_ROOT.mkdir(exist_ok=True)
EXTRACTED_ROOT = ROOT / 'extracted'
EXTRACTED_ROOT.mkdir(exist_ok=True)

http = urllib3.PoolManager()

# Only keep interesting source files
FILE_EXTENSIONS = frozenset({
    '.c', '.h',
    '.cc', '.hh',
    '.c++', '.cpp', '.cxx', '.h++', '.hpp', '.ipp',
    '.cs',
    '.f', '.f90', '.f95',
    '.go',
    '.java',
    '.pl',
    '.php',
    '.py', '.pyi', '.pyw', '.pyx', '.pxd',
    '.rb',
    '.rs',
    '.s',
    '.zig',
})  # fmt: skip
METADATA_FILES = frozenset({
    'PKG-INFO',
    'pyproject.toml',
})
DIRECTORY_BLACKLIST = frozenset({
    # SCM directories
    '.git', '.hg', '.jj', '.svn',
    # Virtual environments
    'venv', '.venv', '.eggs',
    # Project-related directories
    '.tox', '.nox',
    '.idea', '.vs', '.vscode',
    # Non-project directories
    'deps', 'extern', 'external', 'externals', 'external_libs',
    'pybind', 'pybind11',
    'third_party',
    '_vendor', 'vendor', 'vendored', 'vendored-meson',
})  # fmt: skip


def main() -> int:
    start = time.perf_counter()

    rows = http.request('GET', PACKAGES_URL).json()['rows'][:10_000]
    project_names = [
        (row['project'], row['download_count'], rank)
        for rank, row in enumerate(rows, start=1)
    ]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(process_project, index, proj, download_count, rank)
            for index, (proj, download_count, rank) in enumerate(project_names, start=1)
        }
        sdists = {fut.result() for fut in concurrent.futures.as_completed(futures)}
    sdists.discard(None)

    dt = time.perf_counter() - start
    print(f'Processed {len(sdists)} sdists ({dt:.3f}s)')
    return 0


def process_project(index, proj, download_count, rank):
    try:
        metadata = sdist_url(http, index, proj)
        if metadata is None:
            return None
        url, upload_time = metadata
        filename = url.rpartition('/')[2]
        archive_data = http.request('GET', url).data
        print(f'{index:6,}: Downloaded {filename} for {proj!r}')

        # Group projects by first two letters, excluding 'py'
        prefix = proj.removeprefix('py').removeprefix('-')[:2] or proj
        project_root = EXTRACTED_ROOT / prefix / proj
        project_root.mkdir(parents=True, exist_ok=True)

        sdist_metadata = {
            'url': url,
            'filename': filename,
            'upload_time': upload_time,
            'download_count': download_count,
            'rank': rank,
        }
        (project_root / '__sdist_metadata__.json').write_text(
            json.dumps(sdist_metadata, ensure_ascii=False, indent=0),
            encoding='utf-8',
        )

        extract_archive(index, filename, archive_data, project_root)
        return filename
    except Exception:
        print(f'{index:6,}: Fetching {proj!r} failed')
        traceback.print_exc()


def sdist_url(
    http: urllib3.PoolManager, index: int, project_name: str
) -> tuple[str, str] | None:
    data = http.request('GET', f'https://pypi.org/pypi/{project_name}/json').json()
    for entry in data['urls']:
        if entry['packagetype'] == 'sdist':
            return entry['url'], entry['upload_time_iso_8601']
    print(f'{index:6,}: No source distribution for {project_name!r}')
    return None


def extract_archive(index: int, filename: str, content: bytes, project_root: Path):
    print(f'{index:6,}: Extracting {filename!r}')
    stream = BytesIO(content)
    if filename.endswith(('.tar.gz', '.tgz')):
        return extract_archive_tar_gzip(index, filename, stream, project_root)
    if filename.endswith('.tar.bz2'):
        return extract_archive_tar_bzip2(index, filename, stream, project_root)
    if filename.endswith('.zip'):
        return extract_archive_zip(index, filename, stream, project_root)
    return None


def extract_archive_tar_gzip(
    index: int, filename: str, stream: BytesIO, project_root: Path
):
    with tarfile.TarFile.gzopen(filename, mode='r', fileobj=stream) as tar:
        return extract_archive_tar(index, tar, project_root)


def extract_archive_tar_bzip2(
    index: int, filename: str, stream: BytesIO, project_root: Path
):
    with tarfile.TarFile.bz2open(filename, mode='r', fileobj=stream) as tar:
        return extract_archive_tar(index, tar, project_root)


def extract_archive_tar(index: int, tar: tarfile.TarFile, /, project_root: Path):
    extracted = set()
    while (member := tar.next()) is not None:
        if not member.isfile():
            continue

        path = Path(member.name)
        path_normcase = path.as_posix().casefold()
        if path_normcase in extracted or not keep_file(index, path, member.size):
            continue

        dest_path = cross_platform_dest_path(
            path, archive_filename=tar.name, project_root=project_root
        )
        try:
            tar.makefile(member, dest_path)
        except OSError:
            print(f'{index:6,}: Failed to extract {path!r} to {dest_path!r}!')
        extracted.add(path_normcase)


def extract_archive_zip(index: int, filename: str, stream: BytesIO, project_root: Path):
    zip = zipfile.ZipFile(stream)
    zip.filename = filename
    extracted = set()
    with zip:
        for member in zip.filelist:
            if member.is_dir():
                continue

            path = Path(member.filename)
            path_normcase = path.as_posix().casefold()
            if path_normcase in extracted or not keep_file(
                index, path, member.file_size
            ):
                continue

            dest_path = cross_platform_dest_path(
                path, archive_filename=zip.filename, project_root=project_root
            )
            try:
                with zip.open(member) as source, open(dest_path, 'wb') as target:
                    shutil.copyfileobj(source, target)
            except OSError:
                print(f'{index:6,}: Failed to extract {path!r} to {dest_path!r}!')
            extracted.add(path_normcase)


def keep_file(index: int, path: Path, size: int) -> bool:
    if any(part.lower() in DIRECTORY_BLACKLIST for part in path.parts):
        return False

    if '..' in path.parts:
        print(f'{index:6,}: Skipping {path} (would extract to parent directory)')
        return False

    # Remove large files
    if (size_mb := size / 1000 / 1000) > 5:
        print(f'{index:6,}: Skipping {path} (too large: {size_mb:.2f}MB)')
        return False

    if path.name in METADATA_FILES:
        return True

    if path.suffix.lower() in FILE_EXTENSIONS:
        return True

    return False


_ILLEGAL = dict.fromkeys((*range(0x20), *rb'?<>\:*|"'), '_')


def cross_platform_dest_path(
    path: Path, *, archive_filename: str, project_root: Path
) -> Path:
    # Remove version from archive filename
    if Path(archive_filename).name.startswith(f'{path.parts[0]}.'):
        part_parts = path.parts[1:]
    else:
        part_parts = path.parts

    # Make filenames valid for Windows
    parts = filter(None, (p.translate(_ILLEGAL).rstrip(' .') for p in part_parts))
    dest_path = Path(project_root, *parts)
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    return dest_path


if __name__ == '__main__':
    raise SystemExit(main())
