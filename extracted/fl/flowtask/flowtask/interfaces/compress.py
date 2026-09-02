import os
from pathlib import Path, PosixPath
from typing import Optional, Union
from abc import ABC
from io import BytesIO
from zipfile import (
    ZipFile,
    ZIP_DEFLATED,
    ZIP_BZIP2,
    ZIP_LZMA,
    BadZipFile
)
import tarfile
import py7zr
import rarfile
import gzip

## TODO: Simplify Interface.

class CompressSupport(ABC):
    """
    CompressSupport.

    Overview:
        This component handles compressing and uncompressing files and folders
        into various formats.
        Supported formats:
            - ZIP (.zip and .jar)
            - TAR (.tar)
            - GZ (.gz)
            - BZIP2 (.bz2)
            - XZ (.xz)
            - 7z (.7z)
            - RAR (.rar)

    Methods:
        - compress: Compress files/folders into various formats.
        - uncompress: Uncompress files/folders from various formats.
        - zip_file: Compress a single file into a zip file.
        - unzip_file: Uncompress a single file from a zip archive.
        - zip_folder: Compress a folder into a zip file.
        - unzip_folder: Uncompress files from a zip archive to a folder.

    Parameters:
    - source: Path to the file or folder to be compressed or uncompressed.
    - destination: Path where the compressed/uncompressed file should be saved.
    - remove_source: Boolean to remove the source file/folder after operation.
    """

    def __init__(self, *args, **kwargs):
        self.source_dir = None
        self.destination_dir = None
        self.remove_source: bool = kwargs.get('remove_source', False)
        try:
            super().__init__(*args, **kwargs)
        except TypeError:
            super().__init__()

    async def compress(
        self,
        source: str,
        destination: str,
        format: str = 'zip',
        remove_source: bool = False,
        **kwargs
    ):
        """
        Compress the given source into the destination file in the specified format.
        """
        self.source_dir = Path(source).resolve()
        self.destination_dir = Path(destination).resolve()
        self.remove_source = remove_source

        if format == 'zip':
            await self.compress_zip(
                self.source_dir,
                self.destination_dir,
                remove_source=self.remove_source,
                **kwargs
            )
        elif format == 'tar':
            await self.compress_tar(
                self.source_dir,
                self.destination_dir,
                remove_source=self.remove_source,
                **kwargs
            )
        elif format == '7z':
            await self.compress_7z(
                self.source_dir,
                self.destination_dir,
                remove_source=self.remove_source,
                **kwargs
            )
        elif format == 'rar':
            await self.compress_rar(
                self.source_dir,
                self.destination_dir,
                remove_source=self.remove_source,
                **kwargs
            )
        else:
            raise ValueError(
                f"Unsupported compression format: {format}"
            )

    async def uncompress(
        self,
        source: str,
        destination: str,
        format: str = 'zip',
        remove_source: bool = False,
    ):
        """
        Uncompress the given source file into the destination folder.
        """
        self.source_dir = Path(source).resolve()
        self.destination_dir = Path(destination).resolve()

        if format == 'zip':
            await self.uncompress_zip(
                self.source_dir,
                self.destination_dir
            )
        elif format == 'tar':
            await self.uncompress_tar(
                self.source_dir,
                self.destination_dir,
                remove_source=remove_source
            )
        elif format == '7z':
            await self.uncompress_7z(
                self.source_dir,
                self.destination_dir,
                remove_source=remove_source
            )
        elif format == 'rar':
            await self.uncompress_rar(
                self.source_dir,
                self.destination_dir,
                remove_source=remove_source
            )
        else:
            raise ValueError(
                f"Unsupported uncompression format: {format}"
            )

    async def zip_file(
        self,
        source: str,
        destination: str,
        remove_source: bool = False
    ):
        """
        Compress a single file into a zip file.
        """
        self.source_dir = Path(source).resolve()
        self.destination_dir = Path(destination).resolve()
        self.remove_source = remove_source
        await self.compress_zip()

    async def unzip_file(
        self,
        source: str,
        destination: str
    ):
        """
        Uncompress a single file from a zip archive.
        """
        self.source_dir = Path(source).resolve()
        self.destination_dir = Path(destination).resolve()
        await self.uncompress_zip()

    async def zip_folder(
        self,
        source: str,
        destination: str,
        remove_source: bool = False,
        **kwargs
    ):
        """
        Compress a folder into a zip file.
        """
        self.source_dir = Path(source).resolve()
        self.destination_dir = Path(destination).resolve()
        await self.compress_zip(
            source=self.source_dir,
            destination=self.destination_dir,
            remove_source=remove_source,
            **kwargs
        )

    async def unzip_folder(
        self,
        source: str,
        destination: str,
        remove_source: bool = False
    ):
        """
        Uncompress files from a zip archive into a folder.
        """
        self.source_dir = Path(source).resolve()
        self.destination_dir = Path(destination).resolve()
        await self.uncompress_zip(
            source=self.source_dir,
            destination=self.destination_dir,
            remove_source=remove_source
        )

    def _remove_source(self, source: PosixPath):
        """Remove the source file or folder after compression, if required."""
        if isinstance(source, str):
            source = Path(source)
        if source.is_dir():
            source.rmdir()
        else:
            source.unlink(missing_ok=True)

    async def compress_gzip(
        self,
        source: Union[str, PosixPath],
        destination: Union[str, PosixPath],
        extension: str = '.gz',
        remove_source: bool = False
    ) -> str:
        """
        Compress a file or folder into a gzip file.
        If the extension indicates a tarball format
        (e.g., .tar.gz, .tar.bz2, .tar.xz), compress as a tarball;
        otherwise, compress as a simple .gz file.

        Args:
            source: The file or folder to compress.
            destination: The destination path for the compressed file.
            extension: The desired extension (e.g., .gz, .tar.gz, .tar.bz2, .tar.xz).
            remove_source: Whether to remove the source file/folder after compression.

        Returns:
            The path of the compressed file.
        """
        if isinstance(destination, str):
            destination = Path(destination).resolve()
        if isinstance(source, str):
            source = Path(source).resolve()

        # Determine if the extension is for a tarball
        tarball_extensions = {'.tar.gz', '.tar.bz2', '.tar.xz'}
        compressed_file = destination.with_suffix(extension)

        try:
            if extension in tarball_extensions:
                # Compress the source into a tarball with the appropriate compression
                mode = {
                    '.tar.gz': 'w:gz',
                    '.tar.bz2': 'w:bz2',
                    '.tar.xz': 'w:xz'
                }[extension]
                with tarfile.open(compressed_file, mode) as tarf:
                    tarf.add(source, arcname=os.path.basename(source))
            else:
                # Compress a single file using gzip
                if source.is_dir():
                    raise ValueError(
                        "Cannot compress a directory into a simple .gz file."
                        " Use a tarball format for directories."
                    )
                with open(source, 'rb') as f_in:
                    with gzip.open(compressed_file, 'wb') as f_out:
                        f_out.writelines(f_in)

            if remove_source:
                self._remove_source(source)

            return str(compressed_file)

        except Exception as err:
            raise RuntimeError(
                f"Gzip compression failed: {err}"
            )

    async def compress_zip(
        self,
        source: Union[str, PosixPath],
        destination: Union[str, PosixPath],
        compress_type: int = ZIP_DEFLATED,
        compress_level: int = 9,
        remove_source: bool = False
    ):
        """Compress files/folders into a zip archive."""
        if isinstance(destination, str):
            destination = Path(destination).resolve()
        if isinstance(source, str):
            source = Path(source).resolve()
        with ZipFile(destination, 'w', compress_type) as zipf:
            if source.is_dir():
                for root, dirs, files in os.walk(str(source)):
                    for file in files:
                        zipf.write(
                            os.path.join(root, file),
                            os.path.relpath(os.path.join(root, file), source),
                            compress_type=compress_type,
                            compresslevel=compress_level
                        )
            else:
                zipf.write(
                    source,
                    arcname=source.name,
                    compress_type=compress_type,
                    compresslevel=compress_level
                )
        if remove_source is True:
            self._remove_source(source)

    async def uncompress_zip(
        self,
        source: Union[str, PosixPath],
        destination: Union[str, PosixPath],
        source_files: Optional[list] = None,
        password: Optional[str] = None,
        remove_source: bool = False
    ) -> list:
        """Uncompress files from a zip archive."""
        if isinstance(destination, str):
            destination = Path(destination).resolve()
            if destination.exists() and not destination.is_dir():
                raise ValueError(
                    f"Destination path {destination} exists and is not a directory."
                )
            elif not destination.exists():
                destination.mkdir(parents=True, exist_ok=True)
        if isinstance(source, str):
            source = Path(source).resolve()
        with ZipFile(source, 'r') as zipf:
            status = zipf.testzip()
            if status:  # Si no hay status
                raise RuntimeError(
                    f"Zip File {status} is corrupted"
                )
            try:
                members = source_files if source_files else None
                # Check if a password is provided
                if password:
                    # The password should be bytes, so we encode it
                    zipf.extractall(
                        path=destination,
                        members=members,
                        pwd=password.encode('utf-8')
                    )
                else:
                    zipf.extractall(
                        path=destination,
                        members=members,
                    )
                # getting the list of files:
                return source_files if source_files else zipf.namelist()
            except BadZipFile as err:
                # The error raised for bad ZIP files.
                raise RuntimeError(
                    f"Bad Zip File: {err}"
                ) from err
            except Exception as err:
                # Undefined error
                raise RuntimeError(
                    f"ZIP Error: {err}"
                ) from err
        if remove_source is True:
            self._remove_source(source)

    async def compress_tar(
        self,
        source: Union[str, PosixPath],
        destination: Union[str, PosixPath],
        compress_type: str = 'w:gz',  # You can specify 'w:gz', 'w:bz2', 'w:xz', etc.
        remove_source: bool = False
    ):
        """Compress files/folders into a tar archive."""
        if isinstance(destination, str):
            destination = Path(destination).resolve()
        if isinstance(source, str):
            source = Path(source).resolve()

        with tarfile.open(destination, compress_type) as tarf:
            tarf.add(source, arcname=os.path.basename(source))

        if remove_source:
            self._remove_source(source)

    async def uncompress_tar(
        self,
        source: Union[str, PosixPath],
        destination: Union[str, PosixPath],
        remove_source: bool = False
    ):
        """Uncompress files from a tar archive."""
        if isinstance(destination, str):
            destination = Path(destination).resolve()

        with tarfile.open(source, 'r') as tarf:
            tarf.extractall(destination)

        if remove_source:
            self._remove_source(source)

    async def compress_7z(
        self,
        source: Union[str, PosixPath],
        destination: Union[str, PosixPath],
        remove_source: bool = False
    ):
        """Compress files/folders into a 7z archive."""
        if isinstance(destination, str):
            destination = Path(destination).resolve()
        if isinstance(source, str):
            source = Path(source).resolve()

        with py7zr.SevenZipFile(destination, 'w') as archive:
            if source.is_dir():
                archive.writeall(source, arcname=os.path.basename(source))
            else:
                archive.write(source, arcname=os.path.basename(source))

        if remove_source:
            self._remove_source(source)

    async def uncompress_7z(
        self,
        source: Union[str, PosixPath],
        destination: Union[str, PosixPath],
        remove_source: bool = False
    ):
        """Uncompress files from a 7z archive."""
        if isinstance(destination, str):
            destination = Path(destination).resolve()

        with py7zr.SevenZipFile(source, 'r') as archive:
            archive.extractall(path=destination)

        if remove_source:
            self._remove_source(source)

    async def compress_rar(
        self,
        source: Union[str, PosixPath],
        destination: Union[str, PosixPath],
        remove_source: bool = False,
        **kwargs
    ):
        """Compress files/folders into a rar archive."""
        if isinstance(destination, str):
            destination = Path(destination).resolve()
        if isinstance(source, str):
            source = Path(source).resolve()

        with rarfile.RarFile(destination, 'w', **kwargs) as rarf:
            if source.is_dir():
                for root, dirs, files in os.walk(str(source)):
                    for file in files:
                        rarf.write(os.path.join(root, file),
                                   os.path.relpath(os.path.join(root, file), source))
            else:
                rarf.write(source, arcname=source.name)

        if remove_source:
            self._remove_source(source)

    async def uncompress_rar(
        self,
        source: Union[str, PosixPath],
        destination: Union[str, PosixPath],
        remove_source: bool = False
    ):
        """Uncompress files from a rar archive."""
        if isinstance(destination, str):
            destination = Path(destination).resolve()

        with rarfile.RarFile(source, 'r') as rarf:
            rarf.extractall(path=destination)

        if remove_source:
            self._remove_source(source)

    async def uncompress_gzip(
        self,
        source: Union[str, bytes, PosixPath],
        destination: Union[str, PosixPath],
        remove_source: bool = False
    ) -> list:
        """Uncompress a Gzip file or tarball and return the list of uncompressed files."""
        if isinstance(source, (bytes, BytesIO)):
            with gzip.GzipFile(fileobj=source, mode='rb') as gz:
                uncompressed_file = gz.read()
            decompresed_file = BytesIO(uncompressed_file)
            decompresed_file.seek(0)
            return decompresed_file
        if isinstance(destination, str):
            destination = Path(destination).resolve()
        if isinstance(source, str):
            source = Path(source).resolve()

        uncompressed_files = []  # To keep track of the uncompressed files

        try:
            # Check if it's a tarball (e.g., .tar.gz, .tar.bz2, .tar.xz)
            if tarfile.is_tarfile(source):
                print('Is a tarfile')
                with tarfile.open(source, "r:*") as tar:
                    tar.extractall(path=destination)
                    # Get list of uncompressed files from the tarball
                    uncompressed_files = [
                        destination / member.name for member in tar.getmembers()
                    ]
            else:
                # Handle simple .gz files (non-tarball)
                output_file = destination / source.stem  # Remove .gz suffix
                with gzip.open(source, 'rb') as gz_f:
                    with open(output_file, 'wb') as out_f:
                        out_f.write(gz_f.read())
                uncompressed_files.append(output_file)
            if remove_source:
                self._remove_source(source)
            return uncompressed_files

        except Exception as err:
            print(err)
            raise RuntimeError(f"Gzip extraction failed: {err}")
