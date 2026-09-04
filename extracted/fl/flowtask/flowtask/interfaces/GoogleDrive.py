import asyncio
import fnmatch
import re
from abc import ABC
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from .GoogleClient import GoogleClient
from ..exceptions import ComponentError, FileError, FileNotFound


class GoogleDriveClient(GoogleClient, ABC):
    """
    Google Drive Client for searching files on Google Drive.

    Search modes (combinable per spec dict in ``search_files``):

    - ``file_id``: direct metadata lookup, skips search entirely.
    - ``filename``: exact-name match within ``directory`` (default: Drive root).
    - ``pattern``/``extension``: glob-style name match and/or suffix filter
      within ``directory``.
    - Neither ``filename`` nor ``pattern`` given: matches every file directly
      under ``directory`` (i.e. "download this whole folder").
    - ``recursive: True``: descends into subfolders of ``directory`` when no
      ``filename`` is given, applying the same ``pattern``/``extension``
      filter at every level.

    ``directory`` has no literal-path equivalent in the Drive API — it is
    resolved by walking each ``/``-separated segment through
    ``_resolve_folder_path``.
    """

    FOLDER_MIME_TYPE = "application/vnd.google-apps.folder"
    NATIVE_MIME_PREFIX = "application/vnd.google-apps."

    #: Per spec §3 Module 2 — default export extension and full set of
    #: supported explicit `export_format` values (with their Drive export
    #: mimeType) for each native Google Workspace type.
    NATIVE_EXPORT_TABLE: Dict[str, Dict[str, Any]] = {
        "application/vnd.google-apps.spreadsheet": {
            "default_extension": "xlsx",
            "formats": {
                "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                "csv": "text/csv",
                "tsv": "text/tab-separated-values",
                "ods": "application/x-vnd.oasis.opendocument.spreadsheet",
                "pdf": "application/pdf",
            },
        },
        "application/vnd.google-apps.document": {
            "default_extension": "docx",
            "formats": {
                "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                "pdf": "application/pdf",
                "odt": "application/vnd.oasis.opendocument.text",
                "rtf": "application/rtf",
                "txt": "text/plain",
                "epub": "application/epub+zip",
            },
        },
        "application/vnd.google-apps.presentation": {
            "default_extension": "pptx",
            "formats": {
                "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
                "pdf": "application/pdf",
                "odp": "application/vnd.oasis.opendocument.presentation",
                "txt": "text/plain",
            },
        },
        "application/vnd.google-apps.drawing": {
            "default_extension": "png",
            "formats": {
                "png": "image/png",
                "jpeg": "image/jpeg",
                "svg": "image/svg+xml",
                "pdf": "application/pdf",
            },
        },
    }

    @staticmethod
    def _sanitize_filename(name: str) -> str:
        """Strip any path components and unsafe characters from a filename."""
        return re.sub(r'[\\/:*?"<>|]+', "_", Path(name).name).strip()

    def _resolve_export_format(
        self, mime_type: str, export_format: Optional[str]
    ) -> Tuple[str, str]:
        """Resolve the export mimeType and extension for a native Google file.

        Args:
            mime_type: The native ``application/vnd.google-apps.*`` mimeType.
            export_format: Explicit extension requested (e.g. ``"pdf"``), or
                ``None`` to use the type's documented default.

        Returns:
            A ``(export_mime_type, extension)`` tuple.

        Raises:
            FileError: If ``mime_type`` has no known export table entry, or
                ``export_format`` is not supported for that type.
        """
        table = self.NATIVE_EXPORT_TABLE.get(mime_type)
        if table is None:
            raise FileError(
                f"No export mapping known for native Google mimeType '{mime_type}'"
            )
        extension = (export_format or table["default_extension"]).lstrip(".").lower()
        export_mime = table["formats"].get(extension)
        if export_mime is None:
            supported = ", ".join(sorted(table["formats"]))
            raise FileError(
                f"Unsupported export_format '{extension}' for mimeType '{mime_type}'. "
                f"Supported formats: {supported}"
            )
        return export_mime, extension

    @staticmethod
    def _matches_pattern(name: str, pattern: str) -> bool:
        """Glob-style match (``*``/``?`` wildcards) between name and pattern."""
        return fnmatch.fnmatch(name, pattern)

    async def _resolve_folder_path(self, directory: str, root_id: str = "root") -> str:
        """Resolve a ``/``-separated folder path to its Drive folder id.

        Args:
            directory: Folder path, e.g. ``"Pharmabox/Reports"``.
            root_id: Drive id to start resolution from (default: Drive root).

        Returns:
            The Drive folder id of the final path segment.

        Raises:
            FileNotFound: If any path segment cannot be resolved.
        """
        drive_service = self.get_drive_client()
        parent_id = root_id
        for segment in (s for s in directory.split("/") if s):
            query = (
                f"name='{segment}' and mimeType='{self.FOLDER_MIME_TYPE}' "
                f"and '{parent_id}' in parents and trashed=false"
            )
            response = await self.execute_request(
                lambda q=query: drive_service.files().list(
                    q=q, fields="files(id, name)", pageSize=1
                ).execute()
            )
            matches = response.get("files", [])
            if not matches:
                raise FileNotFound(
                    f"Folder segment '{segment}' not found under Drive parent '{parent_id}' "
                    f"(resolving directory '{directory}')"
                )
            parent_id = matches[0]["id"]
        return parent_id

    async def _list_folder(
        self,
        parent_id: str,
        filename: Optional[str] = None,
        pattern: Optional[str] = None,
        extension: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """List non-folder files directly under ``parent_id`` matching the given filter."""
        drive_service = self.get_drive_client()
        q_parts = [
            f"'{parent_id}' in parents",
            "trashed=false",
            f"mimeType != '{self.FOLDER_MIME_TYPE}'",
        ]
        if filename:
            q_parts.append(f"name='{filename}'")
        elif pattern:
            # Drive's `contains` operator is a plain substring match, not a
            # real glob — strip wildcard characters for the API-side prefilter
            # and apply the real glob match client-side below.
            term = pattern.strip("*?")
            if term:
                q_parts.append(f"name contains '{term}'")
        query = " and ".join(q_parts)
        response = await self.execute_request(
            lambda q=query: drive_service.files().list(
                q=q, fields="files(id, name, mimeType, parents)"
            ).execute()
        )
        candidates = response.get("files", [])
        return [
            item for item in candidates
            if (not extension or item["name"].lower().endswith(f".{extension.lstrip('.').lower()}"))
            and (not pattern or self._matches_pattern(item["name"], pattern))
        ]

    async def _list_folder_recursive(
        self,
        parent_id: str,
        pattern: Optional[str] = None,
        extension: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Like ``_list_folder`` but also descends into every subfolder."""
        drive_service = self.get_drive_client()
        matches = await self._list_folder(parent_id, pattern=pattern, extension=extension)
        query = (
            f"'{parent_id}' in parents and mimeType='{self.FOLDER_MIME_TYPE}' "
            "and trashed=false"
        )
        response = await self.execute_request(
            lambda q=query: drive_service.files().list(
                q=q, fields="files(id, name)"
            ).execute()
        )
        for folder in response.get("files", []):
            matches.extend(
                await self._list_folder_recursive(
                    folder["id"], pattern=pattern, extension=extension
                )
            )
        return matches

    async def search_files(self, specs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Resolve each spec to one or more Drive file metadata dicts.

        Args:
            specs: List of search spec dicts. Each may contain ``file_id``,
                ``filename``, ``pattern``, ``extension``, ``directory``,
                and ``recursive`` keys (see class docstring for semantics).

        Returns:
            A flat list of Drive file metadata dicts (``id``, ``name``,
            ``mimeType``, ``parents``) — all matches across all specs, not
            just the first per spec (Drive allows duplicate filenames in
            the same folder).

        Raises:
            FileNotFound: If a spec's ``directory`` cannot be resolved.
            ComponentError: If the Drive API rejects a request (e.g. the
                service account lacks access to the file/folder).
        """
        drive_service = self.get_drive_client()
        results: List[Dict[str, Any]] = []
        try:
            for spec in specs:
                file_id = spec.get("file_id")
                if file_id:
                    metadata = await self.execute_request(
                        lambda fid=file_id: drive_service.files().get(
                            fileId=fid, fields="id, name, mimeType, parents"
                        ).execute()
                    )
                    results.append(metadata)
                    continue

                directory = spec.get("directory")
                parent_id = (
                    await self._resolve_folder_path(directory) if directory else "root"
                )

                filename = spec.get("filename")
                pattern = spec.get("pattern")
                extension = spec.get("extension")
                recursive = spec.get("recursive", False)

                if recursive and not filename:
                    matches = await self._list_folder_recursive(
                        parent_id, pattern=pattern, extension=extension
                    )
                else:
                    matches = await self._list_folder(
                        parent_id, filename=filename, pattern=pattern, extension=extension
                    )
                results.extend(matches)
        except FileNotFound:
            raise
        except HttpError as err:
            raise ComponentError(
                f"Error searching files on Google Drive: {err}"
            ) from err

        return results

    async def download_found_files(
        self,
        found: List[Dict[str, Any]],
        destination_dir: Union[str, Path],
        filenames: Optional[List[str]] = None,
        export_format: Optional[str] = None,
    ) -> List[Dict[str, str]]:
        """Download (or export, for native Google types) every matched file.

        Non-native files are fetched with ``files().get_media``; native
        Google Docs/Sheets/Slides/Drawings (``mimeType`` starting with
        ``application/vnd.google-apps.``) are exported with
        ``files().export_media`` to ``export_format`` if given, else to the
        type's documented default (see ``NATIVE_EXPORT_TABLE``).

        A failure downloading one file in the batch is logged and skipped —
        the rest of the batch still downloads (same rule
        ``SharepointClient.download_found_files`` follows).

        Args:
            found: List of Drive file metadata dicts, as returned by
                ``search_files`` (must include ``id``, ``name``, ``mimeType``).
            destination_dir: Local directory to write downloaded files into.
            filenames: Optional list of desired local filenames. Applied
                positionally against ``found`` only when its length matches;
                otherwise original names are kept (with a warning).
            export_format: Optional explicit export extension (e.g.
                ``"pdf"``) applied to every native Google file in the batch
                that doesn't specify its own.

        Returns:
            A list of ``{"filename": <local_path>}`` dicts, one per
            successfully downloaded file (failed files are omitted, not
            raised).

        Raises:
            FileError: If a native file's resolved/explicit export format
                is not supported for its type.
        """
        drive_service = self.get_drive_client()
        dest_dir = Path(destination_dir).expanduser().resolve()
        dest_dir.mkdir(parents=True, exist_ok=True)

        desired_names = filenames
        if desired_names and len(desired_names) != len(found):
            self._logger.warning(
                f"⚠️ Matched files ({len(found)}) != filenames ({len(desired_names)}). "
                "Will keep original names."
            )
            desired_names = None

        results: List[Dict[str, str]] = []
        for idx, item in enumerate(found):
            file_id = item["id"]
            mime_type = item.get("mimeType", "")
            source_name = item.get("name", file_id)
            target_name = self._sanitize_filename(
                desired_names[idx] if desired_names else source_name
            )

            try:
                if mime_type.startswith(self.NATIVE_MIME_PREFIX):
                    export_mime, ext = self._resolve_export_format(mime_type, export_format)
                    if not target_name.lower().endswith(f".{ext}"):
                        target_name = f"{Path(target_name).stem}.{ext}"
                    request = drive_service.files().export_media(
                        fileId=file_id, mimeType=export_mime
                    )
                else:
                    request = drive_service.files().get_media(fileId=file_id)

                dest_path = dest_dir / target_name
                # NOTE: MediaIoBaseDownload.next_chunk() calls `self._fd.write(content)`
                # synchronously (googleapiclient/http.py) — it is NOT awaited internally.
                # An aiofiles (async) file handle would silently produce a 0-byte file:
                # write() returns an unawaited coroutine that never actually runs. A
                # plain sync file handle is correct here because next_chunk() itself
                # already runs inside asyncio.to_thread below, off the event loop.
                with open(dest_path, "wb") as f:
                    downloader = MediaIoBaseDownload(f, request)
                    done = False
                    while not done:
                        _status, done = await asyncio.to_thread(downloader.next_chunk)

                results.append({"filename": str(dest_path)})
            except FileError:
                raise
            except (HttpError, OSError) as err:
                self._logger.error(f"❌ Download failed for {source_name}: {err}")
                continue

        return results
