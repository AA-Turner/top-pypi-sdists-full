"""
SmartSheet.

Making operations over an Smartsheet Service.

"""
import re
import random
from functools import partial
from pathlib import Path
import ssl
import aiofiles
import aiohttp
from tqdm.asyncio import tqdm
from ..exceptions import (
    ComponentError,
    ConfigError,
    FileNotFound
)
from .credentials import CredentialsInterface
from ..interfaces.http import ua


class SmartSheetClient(CredentialsInterface):
    _credentials: dict = {"token": str, "scheme": str}

    def __init__(self, *args, **kwargs):
        self.file_format: str = "application/vnd.ms-excel"
        self.url: str = "https://api.smartsheet.com/2.0/sheets/"
        self.create_destination: bool = True  # by default
        self.file_id: str = kwargs.pop('file_id', None)
        api_key = self.get_env_value("SMARTSHEET_API_KEY")
        self.api_key: str = kwargs.pop('api_key', api_key)
        self.timeout: int = kwargs.get('timeout', 60)
        kwargs['no_host'] = True
        super().__init__(*args, **kwargs)
        if not self.api_key:
            raise ComponentError(
                f"SmartSheet: Invalid API Key name {self.api_key}"
            )
        self.ssl_certs = kwargs.get('ssl_certs', [])
        self.ssl_ctx = ssl.SSLContext(ssl.PROTOCOL_TLS)
        self.ssl_ctx.options &= ~ssl.OP_NO_SSLv3
        self.ssl_ctx.minimum_version = ssl.TLSVersion.TLSv1_2
        self.ssl_ctx.check_hostname = False
        self.ssl_ctx.verify_mode = ssl.CERT_NONE
        if self.ssl_certs:
            self.ssl_ctx.load_cert_chain(*self.ssl_certs)

    async def http_get(
        self,
        url: str = None,
        credentials: dict = None,
        headers: dict = {},
        accept: str = 'application/vnd.ms-excel',
        destination: Path = None
    ):
        """
        session.
            connect to an http source using aiohttp
        """
        timeout = aiohttp.ClientTimeout(total=self.timeout)
        if url is None:
            url = self.url
        # TODO: Auth, Data, etc
        auth = {}
        params = {}
        headers = {
            "Accept": accept,
            "Accept-Encoding": "gzip, deflate",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": random.choice(ua),
            **headers,
        }
        if credentials:
            if "username" in credentials:  # basic Authentication
                auth = aiohttp.BasicAuth(
                    credentials["username"], credentials["password"]
                )
                params = {"auth": auth}
            elif "token" in credentials:
                headers["Authorization"] = "{scheme} {token}".format(
                    scheme=credentials["scheme"], token=credentials["token"]
                )
        async with aiohttp.ClientSession(**params) as session:
            meth = getattr(session, 'get')
            ssl = {"ssl": self.ssl_ctx, "verify_ssl": True}
            fn = partial(
                meth,
                url,
                headers=headers,
                timeout=timeout,
                allow_redirects=True,
                **ssl,
            )
            try:
                async with fn() as response:
                    if response.status in (200, 201, 202):
                        return await self.http_response(response, destination)
                    else:
                        print("ERROR RESPONSE >> ", response)
                        raise ComponentError(
                            f"Smartsheet: Error getting data from URL {response}"
                        )
            except Exception as err:
                raise ComponentError(
                    f"Smartsheet: Error Making an SSL Connection to ({self.url}): {err}"
                ) from err
            except aiohttp.exceptions.HTTPError as err:
                raise ComponentError(
                    f"Smartsheet: SSL Certificate Error: {err}"
                ) from err

    async def http_response(self, response, destination: str):
        # getting aiohttp response:
        if response.status == 200:
            try:
                async with aiofiles.open(str(destination), mode="wb") as fp:
                    await fp.write(await response.read())
                if destination.exists():
                    return response
                else:
                    raise FileNotFound(
                        f"Error saving File {destination!s}"
                    )
            except FileNotFound:
                raise
            except Exception as err:
                raise FileNotFound(
                    f"Error saving File {err!s}"
                )
        else:
            raise ComponentError(
                f"DownloadFromSmartSheet: Wrong response from Smartsheet: {response!s}"
            )

    async def download_file(self, file_id: str = None, destination: Path = None):
        if isinstance(destination, str):
            destination = Path(destination)
        if not file_id:
            file_id = self.file_id
        if not file_id:
            raise ConfigError(
                "SmartSheet: Unable to Download without FileId."
            )
        credentials = {"token": self.api_key, "scheme": "Bearer"}
        url = f"{self.url}{file_id}"
        if not destination:
            destination = self.filename
        if await self.http_get(
            url=url,
            credentials=credentials,
            destination=destination
        ):
            return True

    async def _get_sheet_rows_data(
        self,
        sheet_id: str,
        session: aiohttp.ClientSession,
        headers: dict,
        filename_columns: list,
        column_filter: dict = None
    ) -> dict:
        """
        Fetch sheet data to get row information for filename generation and filtering.

        IMPORTANT: Returns ALL rows with their data. Filtering is applied later when
        matching attachments to rows. This ensures we can match attachment parentId
        to row ID even if the row doesn't match the filter.

        Returns a dict mapping row_id -> {column_name: value, _filter_match: bool}
        """
        sheet_url = f"https://api.smartsheet.com/2.0/sheets/{sheet_id}"

        row_progress = None
        try:
            page_token = None
            row_data = {}
            columns = []
            target_column_ids = {}
            filter_column_ids = {}
            filter_column_lookup = {}
            total_rows_processed = 0
            total_rows = None
            page = 1
            page_size = 100  # Max page size for Smartsheet API
            total_processed = ""

            def _normalize_cell_value(value):
                """Return a string representation suitable for filtering comparisons."""
                if isinstance(value, (list, tuple, set)):
                    return " ".join(
                        str(item).strip()
                        for item in value
                        if item not in (None, "")
                    )
                if value in (None, ""):
                    return ""
                return str(value)
            while True:
                params = {
                    "pageSize": page_size,
                    "page": page
                }
                if page_token:
                    params["pageToken"] = page_token

                async with session.get(
                    sheet_url,
                    headers=headers,
                    ssl=self.ssl_ctx,
                    params=params
                ) as response:
                    if response.status != 200:
                        # If we can't get sheet data, return empty dict
                        return {}
                    sheet_data = await response.json()
                if total_rows is None:
                    total_rows = sheet_data.get("totalRowCount", 0)
                    if row_progress is None:
                        row_progress = tqdm(
                            total=total_rows or 0,
                            desc="Fetching Smartsheet rows",
                            unit="row",
                            leave=False,
                        )
                # Capture columns only once (they're identical across pages)
                if not columns:
                    columns = sheet_data.get("columns", [])

                    # Build lookup to support case-insensitive filter matches
                    normalized_columns = {}
                    for col in columns:
                        title = col.get("title")
                        column_id = col.get("id")
                        if title is None or column_id is None:
                            continue
                        normalized_columns[title.strip().casefold()] = col

                    # Find column IDs for the requested filename columns
                    target_column_ids = {}
                    for col in columns:
                        title = col.get("title")
                        column_id = col.get("id")
                        if title in filename_columns and column_id is not None:
                            target_column_ids[column_id] = title

                    # Find column IDs for filter columns (if provided)
                    filter_column_ids = {}
                    filter_column_lookup = {}
                    if column_filter:
                        for requested_column in column_filter:
                            normalized_name = str(requested_column).strip().casefold()
                            matched_column = normalized_columns.get(normalized_name)
                            if matched_column:
                                filter_column_ids[matched_column["id"]] = matched_column.get("title", "")
                                filter_column_lookup[requested_column] = matched_column.get("title", requested_column)
                                continue

                            # Fall back to exact match if case-insensitive lookup fails
                            for col in columns:
                                if col.get("title") == requested_column:
                                    column_id = col.get("id")
                                    if column_id is not None:
                                        filter_column_ids[column_id] = col.get("title", requested_column)
                                        filter_column_lookup[requested_column] = col.get("title", requested_column)
                                    break

                        # Debug logging
                        if not filter_column_ids:
                            # Column names in filter not found in sheet
                            available_columns = [col.get("title") for col in columns]
                            print("WARNING: No filter columns found in sheet!")
                            print(f"Looking for: {list(column_filter.keys())}")
                            print(f"Available columns: {available_columns[:10]}...")  # Show first 10

                rows = sheet_data.get("rows", [])

                for row_index, row in enumerate(rows, start=total_rows_processed + 1):
                    row_id = row.get("id")
                    row_number = row.get("rowNumber")  # Visual row number from SmartSheet

                    if not row_id:
                        continue

                    row_info = {
                        "_row_number": row_number if row_number else row_index,
                        "_row_index": row_index,
                        "_filter_match": True
                    }

                    # Extract all relevant column values
                    for cell in row.get("cells", []):
                        column_id = cell.get("columnId")

                        # Add filename columns
                        if column_id in target_column_ids:
                            column_name = target_column_ids[column_id]
                            value = cell.get("displayValue") or cell.get("value", "")
                            row_info[column_name] = _normalize_cell_value(value)

                        # Add filter columns
                        if column_id in filter_column_ids:
                            column_name = filter_column_ids[column_id]
                            value = cell.get("displayValue") or cell.get("value", "")
                            row_info[column_name] = _normalize_cell_value(value)

                    # Check if row matches column filter (but don't skip it yet!)
                    if column_filter:
                        for filter_col, filter_value in column_filter.items():
                            column_name = filter_column_lookup.get(filter_col, filter_col)
                            row_value = row_info.get(column_name, "")
                            normalized_row_value = _normalize_cell_value(row_value).casefold()

                            if isinstance(filter_value, (list, tuple, set)):
                                filter_values = [
                                    str(value).strip().casefold()
                                    for value in filter_value
                                    if value not in (None, "")
                                ]
                            else:
                                value = "" if filter_value in (None, "") else str(filter_value).strip()
                                filter_values = [value.casefold()] if value else []

                            msg = (
                                "SmartSheet: Filtering Row {row_id} Column '{col_name}': "
                                "Row Value='{row_val}' vs FilterValue='{filter_val}'"
                            ).format(
                                row_id=row_id,
                                col_name=column_name,
                                row_val=normalized_row_value,
                                filter_val=filter_values,
                            )
                            total_processed += msg + "\n"

                            if not normalized_row_value or not filter_values:
                                row_info["_filter_match"] = False
                                break

                            if not any(value in normalized_row_value for value in filter_values):
                                row_info["_filter_match"] = False
                                break

                    # Store ALL rows, even if they don't match filter
                    row_data[row_id] = row_info

                total_rows_processed += len(rows)
                if row_progress:
                    row_progress.update(len(rows))

                if 'nextPageToken' in sheet_data:
                    page_token = sheet_data.get("nextPageToken")
                    if not page_token:
                        break
                else:
                    # check if we've processed all rows
                    if total_rows_processed >= total_rows:
                        break
                    page += 1

            if row_progress:
                row_progress.close()
            return row_data

        except Exception as err:
            # If anything fails, return empty dict
            if row_progress:
                row_progress.close()
            return {}

    def _generate_unique_filename(
        self,
        original_filename: str,
        row_id: str,
        row_data: dict,
        filename_columns: list,
        use_row_number: bool = False
    ) -> str:
        """
        Generate unique filename using row data.

        Format: {row_identifier}_{column1_value}_{column2_value}_{original_filename}

        Parameters
        ----------
        use_row_number : bool
            If True, uses visual row number (1, 2, 3, 16, etc.)
            If False, uses internal SmartSheet row ID (default)

        Example with use_row_number=False: 7075005843705732_3547_Comfortable-Heating_W-9.pdf
        Example with use_row_number=True: 16_3547_Comfortable-Heating_W-9.pdf
        """
        # Split filename into name and extension
        path = Path(original_filename)
        name = path.stem
        ext = path.suffix

        # Determine which identifier to use
        if use_row_number:
            # Use visual row number from sheet
            row_identifier = str(row_data.get("_row_number", row_id))
        else:
            # Use internal SmartSheet row ID (default, backward compatible)
            row_identifier = str(row_id)

        # Build prefix from row data
        prefix_parts = [row_identifier]

        for col_name in filename_columns:
            # Skip internal metadata fields
            if col_name.startswith("_"):
                continue

            value = row_data.get(col_name, "")
            if value:
                # Clean the value for use in filename
                clean_value = str(value).strip()
                # Replace spaces and special chars with hyphens
                clean_value = clean_value.replace(" ", "-")
                clean_value = clean_value.replace("/", "-")
                clean_value = clean_value.replace("\\", "-")
                clean_value = clean_value.replace(":", "-")
                # Remove any remaining problematic characters
                clean_value = "".join(c for c in clean_value if c.isalnum() or c in "-_.")

                if clean_value:
                    prefix_parts.append(clean_value)

        # Join all parts with underscore
        prefix = "_".join(prefix_parts)

        # Build final filename
        unique_filename = f"{prefix}_{name}{ext}"

        return unique_filename

    async def download_attachments(
        self,
        sheet_id: str,
        row_id: str = None,
        directory: Path = None,
        overwrite: bool = False,
        attachment_filter: list = None,
        filename_columns: list = None,
        filename_filter: str = None,
        column_filter: dict = None,
        use_row_number: bool = False
    ) -> dict:
        """
        Download attachments from a SmartSheet sheet or specific row.

        NOTE: SmartSheet API requires TWO API calls per attachment:
        1. List attachments (returns metadata with attachment IDs)
        2. Get attachment details (returns the actual download URL)

        Parameters
        ----------
        sheet_id : str
            The SmartSheet sheet ID
        row_id : str, optional
            The row ID if downloading row-specific attachments
        directory : Path, optional
            Directory path where attachments will be saved
        overwrite : bool, default=False
            Whether to overwrite existing files
        attachment_filter : list, optional
            List of file extensions to filter (e.g., ['.pdf', '.xlsx', '.csv'])
        filename_columns : list, optional
            List of column names to include in filename for uniqueness.
            Default: ['lead_id', 'Company Name']
            Format: {row_id}_{column1}_{column2}_{original_filename}
        filename_filter : str, optional
            Regular expression pattern to match filenames.
            Example: r'Full Packet\.pdf$' to match files ending with "Full Packet.pdf"
            Only files matching this pattern will be downloaded.
        column_filter : dict, optional
            Dictionary of column_name: value pairs to filter rows.
            Example: {'Document Status': 'Send to TROC Processing'}
            Only attachments from rows matching ALL filter criteria will be downloaded.
        use_row_number : bool, default=False
            If True, uses visual row number (1, 2, 3, 16, etc.) in filename.
            If False, uses internal SmartSheet row ID (default, large number).
            Example with False: 7075005843705732_Pool-Spa_file.pdf
            Example with True: 16_Pool-Spa_file.pdf

        Returns
        -------
        dict
            Dictionary containing:
            - downloaded: list of successfully downloaded file paths
            - skipped: list of skipped files (filtered or already exist)
            - failed: list of failed downloads with error messages
            - total: total number of attachments found
            - filtered_by_column: number of attachments skipped by column filter
            - filtered_by_filename: number of attachments skipped by filename filter

        Raises
        ------
        ComponentError
            If there's an error fetching attachments or during download
        ConfigError
            If required parameters are missing
        """
        if not directory:
            directory = Path.cwd()
        elif isinstance(directory, str):
            directory = Path(directory)

        # Create directory if it doesn't exist
        directory.mkdir(parents=True, exist_ok=True)

        # Default filename columns
        if filename_columns is None:
            filename_columns = ['lead_id', 'Company Name']

        # Compile regex pattern if filename_filter is provided
        filename_pattern = None
        if filename_filter:
            try:
                filename_pattern = re.compile(filename_filter)
            except re.error as err:
                raise ConfigError(
                    f"SmartSheet: Invalid filename_filter regex pattern: {err}"
                )

        # Prepare credentials
        credentials = {"token": self.api_key, "scheme": "Bearer"}
        headers = {
            "Authorization": f"{credentials['scheme']} {credentials['token']}",
            "Content-Type": "application/json"
        }

        # Build attachments list URL
        if row_id:
            attachments_url = (
                f"https://api.smartsheet.com/2.0/sheets/{sheet_id}/rows/{row_id}/attachments?includeAll=true"
            )
        else:
            attachments_url = (
                f"https://api.smartsheet.com/2.0/sheets/{sheet_id}/attachments?includeAll=true"
            )

        downloaded = []
        skipped = []
        failed = []
        filtered_by_column = 0
        filtered_by_filename = 0

        timeout = aiohttp.ClientTimeout(total=self.timeout)

        try:
            async with aiohttp.ClientSession(timeout=timeout) as session:
                # Get sheet row data for filename generation and column filtering
                rows_data = await self._get_sheet_rows_data(
                    sheet_id, session, headers, filename_columns, column_filter
                )

                # Get attachments list
                async with session.get(attachments_url, headers=headers, ssl=self.ssl_ctx, ) as response:
                    if response.status not in (200, 201, 202):
                        raise ComponentError(
                            f"SmartSheet: Error fetching attachments list. Status: {response.status}"
                        )

                    data = await response.json()
                    all_attachments = data.get("data", [])

                    print(f"\n{'='*60}")
                    print(f"DEBUG: Total rows in sheet: {len(rows_data)}")
                    print(f"DEBUG: Total attachments found: {len(all_attachments)}")
                    print(f"{'='*60}\n")

                    # CRITICAL FIX: The parentId in attachments doesn't reliably match row IDs
                    # We need to fetch attachments differently - by iterating through rows

                    # Instead of matching parentId to row ID, we'll:
                    # 1. Get attachments for each filtered row individually
                    # 2. This ensures we know exactly which row each attachment belongs to

                    attachments = []  # Will rebuild with correct row associations

                    row_attachment_progress = tqdm(
                        total=len(rows_data),
                        desc="Fetching row attachments",
                        unit="row",
                        leave=False,
                    )

                    for row_id, row_info in rows_data.items():
                        # Skip rows that don't match filter
                        if column_filter and not row_info.get("_filter_match", True):
                            row_attachment_progress.update(1)
                            continue

                        # Fetch attachments for this specific row
                        row_attachments_url = f"https://api.smartsheet.com/2.0/sheets/{sheet_id}/rows/{row_id}/attachments"  # noqa

                        try:
                            async with session.get(
                                row_attachments_url, headers=headers, ssl=self.ssl_ctx
                            ) as row_response:
                                if row_response.status == 200:
                                    row_data_response = await row_response.json()
                                    row_attachments = row_data_response.get("data", [])

                                    # Tag each attachment with its row info
                                    for att in row_attachments:
                                        att["_row_id"] = row_id
                                        att["_row_info"] = row_info
                                        attachments.append(att)
                        except Exception as err:
                            print(f"Warning: Could not fetch attachments for row {row_id}: {err}")
                            continue
                        finally:
                            row_attachment_progress.update(1)

                    row_attachment_progress.close()

                    if not attachments:
                        return {
                            "filenames": [],
                            "skipped": [],
                            "failed": [],
                            "total": 0,
                            "filtered_by_column": 0,
                            "filtered_by_filename": 0
                        }

                    print(f"DEBUG: Found {len(attachments)} attachments in filtered rows\n")

                    # Download each attachment (requires two API calls per attachment)
                    download_progress = tqdm(
                        total=len(attachments),
                        desc="Downloading attachments",
                        unit="file",
                    )

                    for attachment in attachments:
                        attachment_name = attachment.get("name")
                        try:
                            attachment_id = attachment.get("id")
                            row_id = attachment.get("_row_id")
                            row_info = attachment.get("_row_info", {})

                            if not attachment_name or not attachment_id:
                                failed.append({
                                    "file": attachment_name or "unknown",
                                    "error": "Missing attachment name or ID"
                                })
                                continue

                            # Column filter already applied when fetching attachments per row
                            # No need to check again

                            # FILTER: Filename regex filter
                            if filename_pattern and not filename_pattern.search(attachment_name):
                                filtered_by_filename += 1
                                skipped.append({
                                    "file": attachment_name,
                                    "reason": f"filename does not match pattern '{filename_filter}'"
                                })
                                continue

                            # FILTER 3: Extension filter
                            if attachment_filter:
                                file_ext = Path(attachment_name).suffix.lower()
                                if file_ext not in attachment_filter:
                                    skipped.append({
                                        "file": attachment_name,
                                        "reason": "filtered by extension"
                                    })
                                    continue

                            # Generate unique filename using row data we attached
                            unique_filename = self._generate_unique_filename(
                                attachment_name,
                                row_id,
                                row_info,
                                filename_columns,
                                use_row_number
                            )

                            file_path = directory / unique_filename

                            # Check if file exists and overwrite is False
                            if file_path.exists() and not overwrite:
                                skipped.append({
                                    "file": unique_filename,
                                    "reason": "already exists"
                                })
                                continue

                            # STEP 1: Get attachment details to retrieve download URL
                            try:
                                # Build URL to get specific attachment details
                                attachment_details_url = (
                                    f"https://api.smartsheet.com/2.0/sheets/{sheet_id}/attachments/{attachment_id}"
                                )

                                async with session.get(
                                    attachment_details_url,
                                    headers=headers,
                                    ssl=self.ssl_ctx
                                ) as details_response:
                                    if details_response.status == 200:
                                        attachment_details = await details_response.json()
                                        download_url = attachment_details.get("url")

                                        if not download_url:
                                            failed.append({
                                                "file": unique_filename,
                                                "error": "No download URL in attachment details"
                                            })
                                            continue

                                        # STEP 2: Now download the actual file from the URL
                                        async with session.get(download_url, ssl=self.ssl_ctx) as file_response:
                                            if file_response.status == 200:
                                                content = await file_response.read()

                                                # Write file to disk
                                                async with aiofiles.open(file_path, mode="wb") as fp:
                                                    await fp.write(content)

                                                if file_path.exists():
                                                    downloaded.append(str(file_path))
                                                else:
                                                    failed.append({
                                                        "file": unique_filename,
                                                        "error": "File was not saved successfully"
                                                    })
                                            else:
                                                failed.append({
                                                    "file": unique_filename,
                                                    "error": f"Download failed with status {file_response.status}"
                                                })
                                    else:
                                        failed.append({
                                            "file": unique_filename,
                                            "error": f"Failed to get details with status {details_response.status}"
                                        })

                            except Exception as err:
                                failed.append({
                                    "file": unique_filename,
                                    "error": str(err)
                                })
                        except Exception as err:
                            failed.append({
                                "file": attachment_name or "unknown",
                                "error": str(err)
                            })
                        finally:
                            download_progress.update(1)

                    download_progress.close()

                    return {
                        "filenames": downloaded,
                        "skipped": skipped,
                        "failed": failed,
                        "total": len(attachments),
                        "filtered_by_column": filtered_by_column,
                        "filtered_by_filename": filtered_by_filename
                    }

        except aiohttp.ClientError as err:
            raise ComponentError(
                f"SmartSheet: Error during attachment download: {err}"
            ) from err
        except Exception as err:
            raise ComponentError(
                f"SmartSheet: Unexpected error: {err}"
            ) from err
