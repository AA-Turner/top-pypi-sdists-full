import asyncio
import base64
import urllib.parse
from collections.abc import Callable
from typing import Optional, Dict, Any, List
from pathlib import Path
from io import BytesIO
import pandas as pd
import httpx
from tqdm import tqdm
from ..interfaces.flow import FlowComponent
from ..interfaces.http import HTTPService
from ..interfaces.cache import CacheSupport
from ..interfaces.Boto3Client import Boto3Client
from ..interfaces.qs import QSSupport
from ..exceptions import ComponentError, ConfigError
from ..conf import (
    ZOOM_ACCOUNT_ID,
    ZOOM_CLIENT_ID,
    ZOOM_CLIENT_SECRET,
)


class Zoom(HTTPService, CacheSupport, Boto3Client, QSSupport, FlowComponent):
    """
    Zoom Component

    Retrieves call logs and, for those that are recorded (recording_status=recorded),
    gets recording metadata and downloads:
      - audio/video files
      - transcripts, using the recordingId

       :widths: auto

    | from_date               | Yes      | Start date (YYYY-MM-DD) for call logs                               |
    | to_date                 | Yes      | End date (YYYY-MM-DD) for call logs                                 |
    | save_path               | No       | Folder for recordings (default: /tmp/zoom/recordings)               |
    | transcripts_path        | No       | Folder for transcripts (default: /tmp/zoom/transcripts)             |
    | download                | No       | Download recordings (bool, default: True)                           |
    | download_transcripts    | No       | Download transcripts (bool, default: True)                          |
    | max_pages               | No       | Page limit for testing/debug                                         |
    | base_path               | No       | Base path for all downloads (default: /tmp/zoom)                    |
    | extension_column        | No       | DataFrame column name containing extensions to filter                |
    | as_bytes                | No       | Store recordings/transcripts in memory as BytesIO (default: False)   |
    | content_type            | No       | Default content type for recordings (default: 'audio/mpeg')          |
    | auto_skip_processed     | No       | Auto-query DB and skip existing recordings (default: False)          |
    | datasource              | No       | Datasource name for DB connection (default: 'db')                    |
    | recordings_table        | No       | Table name with recordings (default: 'recordings')                   |
    | call_id_column          | No       | Column name for call_id (default: 'call_id')                         |
    | s3_filename_column      | No       | Column name for S3 filename (default: 'recording_mp3_s3_key')        |
    | directory               | No       | S3 directory path (default: 'zoom/recordings/')                      |
    | s3_config               | No       | S3 config name for Boto3Client (default: 'default')                  |
    | bucket                  | No       | S3 bucket name (required if auto_skip enabled)                       |

    Returns:
        pandas.DataFrame with call logs and download information.

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          Zoom:
          # attributes here
        ```
    """
    _version = "1.0.0"

    accept: str = "application/json"
    BASE_URL = "https://api.zoom.us/v2"
    AUTH_URL = "https://zoom.us/oauth/token"
    CACHE_KEY = "_zoom_authentication"

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        # Type dispatch (like Staples.py pattern)
        self._fn = kwargs.pop("type", "call_logs").lower().strip()
        if self._fn not in ("call_logs", "sms"):
            raise ConfigError(
                f"Invalid type '{self._fn}'. Supported types: 'call_logs', 'sms'"
            )
        
        # ETL inputs
        self.from_date: str = kwargs.get("from_date")
        self.to_date: str = kwargs.get("to_date")
        
        # Phone numbers for SMS (required when type=sms)
        phone_numbers_input = kwargs.get("phone_numbers")
        self.phone_numbers: List[str] = []
        if phone_numbers_input:
            if isinstance(phone_numbers_input, list):
                self.phone_numbers = [str(p).strip() for p in phone_numbers_input if str(p).strip()]
            elif isinstance(phone_numbers_input, str):
                self.phone_numbers = [p.strip() for p in phone_numbers_input.split(',') if p.strip()]
        
        # Extensions for SMS (will be mapped to phone numbers)
        extensions_input = kwargs.get("extensions")
        self.extensions: List[str] = []
        if extensions_input:
            if isinstance(extensions_input, list):
                self.extensions = [str(e).strip() for e in extensions_input if str(e).strip()]
            elif isinstance(extensions_input, str):
                self.extensions = [e.strip() for e in extensions_input.split(',') if e.strip()]


        base_path = Path(kwargs.get("base_path", "/tmp/zoom"))
        self.save_path: Path = Path(kwargs.get("save_path", base_path / "recordings"))
        self.transcripts_path: Path = Path(kwargs.get("transcripts_path", base_path / "transcripts"))

        self.download_recordings: bool = bool(kwargs.get("download", True))
        self.download_transcripts: bool = bool(kwargs.get("download_transcripts", True))
        self.max_pages: Optional[int] = kwargs.get("max_pages")

        # DataFrame filtering
        self.extension_column: Optional[str] = kwargs.get("extension_column", None)
        self._extensions_filter: List[str] = []

        # Memory storage options
        self.as_bytes: bool = kwargs.get("as_bytes", False)
        self.content_type: str = kwargs.get("content_type", "audio/mpeg")

        # Auto-skip configuration
        self.auto_skip_processed: bool = kwargs.get("auto_skip_processed", False)
        self.datasource: str = kwargs.get("datasource", "db")  # Default datasource
        self.recordings_table: str = kwargs.get("recordings_table", "recordings")
        self.call_id_column: str = kwargs.get("call_id_column", "call_id")
        self.s3_filename_column: str = kwargs.get("s3_filename_column", "recording_mp3_s3_key")
        self.s3_directory: str = kwargs.get("directory", "zoom/recordings/")

        # Database driver (required for QSSupport)
        self._driver: str = kwargs.get("driver", "pg")

        # S3 configuration (for Boto3Client)
        self._s3_config: str = kwargs.get("s3_config", "default")
        if self.auto_skip_processed:
            kwargs['config'] = self._s3_config

        # State
        self._access_token: Optional[str] = None
        self._existing_recordings: Dict[str, str] = {}  # {call_id: s3_filename}
        self._s3_client = None  # Will be initialized when needed

        # Ensure folders exist (only if not using as_bytes)
        if not self.as_bytes:
            self.save_path.mkdir(parents=True, exist_ok=True)
            self.transcripts_path.mkdir(parents=True, exist_ok=True)

        super().__init__(loop=loop, job=job, stat=stat, **kwargs)

    # =========================
    # Auth
    # =========================
    async def get_cached_token(self) -> Optional[str]:
        """
        Try to get the OAuth Access Token from cache (Redis).
        """
        try:
            async with self as cache:
                token = await cache._redis.get(self.CACHE_KEY)
                if isinstance(token, bytes):
                    token = token.decode('utf-8', errors='ignore')
                if token and isinstance(token, str) and len(token) > 10:
                    self._logger.info(f"Using cached Zoom token: {token[:10]}...")
                    return token
                else:
                    self._logger.debug(f"Invalid or no token in cache: {token!r}")
        except Exception as e:
            self._logger.warning(f"Error getting cached token: {str(e)}")
        return None

    def set_auth_headers(self, token: str) -> None:
        """
        Set Bearer token in headers and keep it in memory.
        """
        self._access_token = token
        if not isinstance(self.headers, dict):
            self.headers = {}
        self.headers["Authorization"] = f"Bearer {token}"

    def _ensure_paths(self):
        """Force save_path and transcripts_path to be pathlib.Path and ensure dirs exist."""
        if not isinstance(self.save_path, Path):
            self.save_path = Path(self.save_path)
        if not isinstance(self.transcripts_path, Path):
            self.transcripts_path = Path(self.transcripts_path)
        self.save_path.mkdir(parents=True, exist_ok=True)
        self.transcripts_path.mkdir(parents=True, exist_ok=True)


    @staticmethod
    def _basic_header_value(client_id: str, client_secret: str) -> str:
        """
        Build the HTTP Basic header for OAuth token request.
        """
        creds = f"{client_id}:{client_secret}".encode("utf-8")
        return "Basic " + base64.b64encode(creds).decode("utf-8")

    async def _fetch_token(self) -> tuple[str, int]:
        """
        Get a fresh OAuth Access Token via Server-to-Server OAuth.
        Returns: (token, expires_in)
        """
        if not (ZOOM_ACCOUNT_ID and ZOOM_CLIENT_ID and ZOOM_CLIENT_SECRET):
            raise ComponentError("Missing Zoom S2S OAuth credentials")

        params = {
            "grant_type": "account_credentials",
            "account_id": ZOOM_ACCOUNT_ID,
        }
        headers = {
            "Accept": "application/json",
            "Authorization": self._basic_header_value(ZOOM_CLIENT_ID, ZOOM_CLIENT_SECRET),
        }
        resp = await self._post(
            url=self.AUTH_URL,
            params=params,
            headers=headers,
            cookies=None,
            follow_redirects=True,
            raise_for_status=True,
            use_proxy=False,
        )
        data = resp.json()
        token = data.get("access_token")
        if not token:
            raise ComponentError("No access_token in Zoom OAuth response")
        return token, int(data.get("expires_in", 3600))

    async def start(self, **kwargs):
        """
        Ensure we have a valid token: try cache, else fetch and cache.
        Also process input DataFrame if provided.
        """
        # Apply masks to date attributes (masks are already processed by _mask_processing in __init__)
        if hasattr(self, "masks"):
            for mask, replace in self._mask.items():
                if self.from_date:
                    self.from_date = self.from_date.replace(mask, str(replace))
                if self.to_date:
                    self.to_date = self.to_date.replace(mask, str(replace))

        self._logger.info("🔐 Starting Zoom authentication...")
        token = await self.get_cached_token()
        if not token:
            self._logger.info("📡 Fetching new OAuth token from Zoom...")
            token, expires_in = await self._fetch_token()
            try:
                async with self as cache:
                    await cache.setex(self.CACHE_KEY, token, timeout=f"{expires_in}s")
                self._logger.info(f"💾 Token cached for {expires_in} seconds")
            except Exception as e:
                self._logger.warning(f"Couldn't cache token: {e}")
        self.set_auth_headers(token)
        if not self._access_token or "Authorization" not in self.headers:
            raise ComponentError("Authentication headers not properly set")
        self._logger.info("✅ Successfully authenticated with Zoom API")

        # Process input DataFrame if provided
        if self.previous and hasattr(self, 'input') and self.input is not None:
            if hasattr(self.input, 'empty'):  # It's a DataFrame
                if not self.input.empty:
                    self._logger.info(f"📊 Received input DataFrame with {len(self.input)} rows")
                    self._process_input_dataframe()

        return True

    async def _ensure_token(self):
        """
        Make sure we have an access token in memory and headers.
        If not, try cache; if still not, fetch a new one.
        """
        if self._access_token and "Authorization" in self.headers:
            return
        token = await self.get_cached_token()
        if not token:
            token, expires_in = await self._fetch_token()
            try:
                async with self as cache:
                    await cache.setex(self.CACHE_KEY, token, timeout=f"{expires_in}s")
            except Exception as e:
                self._logger.warning(f"Couldn't cache token: {e}")
        self.set_auth_headers(token)

    async def _refresh_token(self):
        """
        Force-refresh the token and update cache + headers.
        """
        token, expires_in = await self._fetch_token()
        try:
            async with self as cache:
                await cache.setex(self.CACHE_KEY, token, timeout=f"{expires_in}s")
        except Exception as e:
            self._logger.warning(f"Couldn't cache token: {e}")
        self.set_auth_headers(token)

    async def _authed_api_get(self, url: str, *, params=None, extra_headers: dict = None, use_http2=True):
        """
        Do a GET with auth guard + one retry on 401.
        """
        await self._ensure_token()
        headers = {**self.headers, "Accept": "application/json", **(extra_headers or {})}
        try:
            return await self.api_get(
                url=url,
                params=params,
                headers=headers,
                use_proxy=False,
                use_http2=use_http2
            )
        except Exception as e:
            msg = str(e).lower()
            if "401" in msg or "unauthorized" in msg:
                self._logger.warning("401 Unauthorized. Refreshing Zoom token and retrying once...")
                await self._refresh_token()
                headers = {**self.headers, "Accept": "application/json", **(extra_headers or {})}
                return await self.api_get(
                    url=url,
                    params=params,
                    headers=headers,
                    use_proxy=False,
                    use_http2=use_http2
                )
            raise

    # =========================
    # S3 helpers
    # =========================
    async def _get_s3_client(self):
        """Get or initialize S3 client (lazy initialization)."""
        if self._s3_client is None:
            import boto3
            from ..conf import AWS_CREDENTIALS

            # Load S3 credentials directly from AWS_CREDENTIALS config
            # DO NOT use self.credentials to avoid conflict with QSSupport (PostgreSQL)
            s3_credentials = AWS_CREDENTIALS.get(self._s3_config)

            if s3_credentials:
                # Use explicit credentials from AWS_CREDENTIALS
                cred = {
                    "aws_access_key_id": s3_credentials.get("aws_key"),
                    "aws_secret_access_key": s3_credentials.get("aws_secret"),
                    "region_name": s3_credentials.get("region_name", 'us-east-1'),
                }
                self._s3_client = boto3.client('s3', **cred)
                self._logger.debug(f"S3 client initialized with credentials from config: {self._s3_config}")

                # Also set bucket if not already set (from config)
                if not self.bucket and 'bucket' in s3_credentials:
                    self.bucket = s3_credentials['bucket']
                    self._logger.debug(f"S3 bucket set from config: {self.bucket}")
            else:
                # Use default credentials from environment
                self._s3_client = boto3.client('s3', region_name='us-east-1')
                self._logger.debug("S3 client initialized with default credentials from environment")

        return self._s3_client

    # =========================
    # Database helpers
    # =========================
    async def _fetch_existing_recordings(self, call_ids: List[str]) -> Dict[str, str]:
        """
        Query database to get existing recordings and their S3 filenames.

        Args:
            call_ids: List of call_ids to check

        Returns:
            Dict mapping call_id to s3_filename: {call_id: s3_filename}
        """
        if not call_ids:
            return {}

        try:
            # Create database connection
            connection = await self.create_connection()

            # Build the query with parameterized IN clause
            # PostgreSQL uses $1, $2, etc. as placeholders
            placeholders = ','.join([f'${i+1}' for i in range(len(call_ids))])
            query = f"""
                SELECT {self.call_id_column}, {self.s3_filename_column}
                FROM {self.recordings_table}
                WHERE {self.call_id_column} IN ({placeholders})
                AND {self.s3_filename_column} IS NOT NULL
            """

            self._logger.info(f"🔍 Querying database for {len(call_ids)} call_ids...")
            self._logger.debug(f"Query: {query}")

            async with await connection.connection() as conn:
                res, error = await conn.query(query, *call_ids)
                if error:
                    self._logger.error(f"Database query error: {error}")
                    return {}

                # Convert to dict: {call_id: s3_filename}
                existing_recordings = {}
                for row in res:
                    call_id = row[self.call_id_column]
                    s3_filename = row[self.s3_filename_column]
                    if s3_filename:  # Only add if s3_filename is not None/empty
                        existing_recordings[call_id] = s3_filename

                self._logger.info(f"✅ Found {len(existing_recordings)} existing recordings in database")
                return existing_recordings

        except Exception as e:
            self._logger.error(f"Error fetching existing recordings from database: {e}")
            return {}

    async def _download_recording_from_s3(self, s3_filename: str, call_id: str, recording_id: str = "rec"):
        """
        Download recording from S3.

        Args:
            s3_filename: S3 filename (not full key, just the filename)
            call_id: Call ID for naming
            recording_id: Recording ID for naming

        Returns:
            If as_bytes=True: (BytesIO, content_type, filename) or None
            If as_bytes=False: Path or None
        """
        if not self.bucket:
            self._logger.error("S3 bucket not specified, cannot download from S3")
            return None

        try:
            # Construct full S3 key: directory + filename
            s3_key = self.s3_directory + s3_filename if self.s3_directory else s3_filename

            # Get S3 client (lazy initialization to avoid conflict with QSSupport)
            s3_client = await self._get_s3_client()

            # Download from S3
            response = s3_client.get_object(
                Bucket=self.bucket,
                Key=s3_key
            )
            content = response['Body'].read()
            content_type = response.get('ContentType', self.content_type)

            if self.as_bytes:
                # Return BytesIO
                file_data = BytesIO(content)
                file_data.seek(0)
                return (file_data, content_type, s3_filename)
            else:
                # Save to disk
                final_path = self.save_path / s3_filename
                final_path.parent.mkdir(parents=True, exist_ok=True)
                with open(final_path, 'wb') as f:
                    f.write(content)
                return final_path

        except Exception as e:
            self._logger.error(f"Error downloading {s3_key} from S3: {e}")
            return None

    # =========================
    # API helpers
    # =========================
    def _clean_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean column names by replacing dots with underscores for all columns.
        This handles nested JSON fields that get flattened with dots.
        """
        if df.empty:
            return df

        # Create mapping for all columns that contain dots
        column_mapping = {}
        for col in df.columns:
            if '.' in col:
                new_col = col.replace('.', '_')
                column_mapping[col] = new_col

        # Rename columns if any were found
        if column_mapping:
            df_renamed = df.rename(columns=column_mapping)
            self._logger.info(f"🔄 Renamed {len(column_mapping)} columns with dots to underscores")
            self._logger.debug(f"Column mappings: {column_mapping}")
            return df_renamed

        return df

    def _process_input_dataframe(self):
        """
        Process input DataFrame to extract extensions for filtering.
        Similar to ScrapTool's DataFrame processing.
        """
        if not self.extension_column:
            self._logger.debug("No extension_column specified, skipping extension filtering")
            return

        if self.extension_column not in self.input.columns:
            self._logger.warning(
                f"Extension column '{self.extension_column}' not found in input DataFrame. "
                f"Available columns: {list(self.input.columns)}"
            )
            return

        # Extract unique extensions from the column
        extensions = self.input[self.extension_column].dropna().astype(str).unique().tolist()
        self._extensions_filter = [ext.strip() for ext in extensions if ext.strip()]

        if self._extensions_filter:
            self._logger.info(
                f"🔍 Extracted {len(self._extensions_filter)} extensions from column '{self.extension_column}': "
                f"{', '.join(self._extensions_filter[:5])}"
                f"{' ...' if len(self._extensions_filter) > 5 else ''}"
            )
        else:
            self._logger.warning(f"No valid extensions found in column '{self.extension_column}'")
    
    def _normalize_phone_number(self, phone: str) -> str:
        """
        Normalize phone number to international format without '+'.
        Handles formats like: (786) 879-8923, 786-879-8923, 7868798923, +17868798923
        Returns: 17868798923 (for US numbers)
        """
        import re
        # Remove all non-digit characters
        digits_only = re.sub(r'\D', '', str(phone))

        # If it's a 10-digit US number, add '1' prefix
        if len(digits_only) == 10:
            return f"1{digits_only}"

        # Otherwise return as-is (already has country code)
        return digits_only

    def _process_input_dataframe_for_sms(self):
        """
        Process input DataFrame to extract phone numbers and extensions for SMS extraction.
        Supports columns: 'phone_number', 'phone_numbers', 'extension', 'extensions', 'extension_number'

        Hybrid mode:
        - If both 'extension' and 'phone_number' columns exist: create local mapping (skip API lookup)
        - If only 'extension' column exists: will use API lookup later (backward compatible)
        """
        # Find extension and phone_number columns
        extension_column = None
        phone_column = None

        for col_name in ['extension', 'extensions', 'extension_number']:
            if col_name in self.input.columns:
                extension_column = col_name
                break

        for col_name in ['phone_number', 'phone_numbers']:
            if col_name in self.input.columns:
                phone_column = col_name
                break

        # HYBRID MODE: If we have both extension and phone_number, create local mapping
        if extension_column and phone_column:
            self._logger.info("📋 Found both extension and phone_number columns - creating local mapping")

            # Initialize mappings
            if not hasattr(self, '_extension_phone_map'):
                self._extension_phone_map = {}
            if not hasattr(self, '_phone_to_extension_map'):
                self._phone_to_extension_map = {}

            # Build bidirectional mapping
            for _, row in self.input.iterrows():
                ext = str(row[extension_column]).strip()
                phone = str(row[phone_column]).strip()

                if ext and phone and phone.lower() not in ('nan', 'none', ''):
                    # Normalize phone number to Zoom API format
                    normalized_phone = self._normalize_phone_number(phone)

                    # extension → phone mapping (for API lookup skip)
                    self._extension_phone_map[ext] = normalized_phone

                    # phone → extension mapping (for reverse lookup in results)
                    self._phone_to_extension_map[normalized_phone] = ext

            self._logger.info(f"✅ Created bidirectional mapping for {len(self._extension_phone_map)} extension(s) (will skip API lookup)")

        # Extract phone numbers from phone_number column
        if phone_column:
            phone_numbers = self.input[phone_column].dropna().astype(str).unique().tolist()
            extracted_numbers = []

            for num in phone_numbers:
                num = num.strip()
                if num and num.lower() not in ('nan', 'none', ''):
                    normalized = self._normalize_phone_number(num)
                    extracted_numbers.append(normalized)

            if extracted_numbers:
                existing_numbers = set(self.phone_numbers)
                new_numbers = [num for num in extracted_numbers if num not in existing_numbers]

                if new_numbers:
                    self.phone_numbers.extend(new_numbers)
                    self._logger.info(
                        f"📱 Extracted {len(new_numbers)} phone number(s) from column '{phone_column}': "
                        f"{', '.join(new_numbers[:3])}"
                        f"{' ...' if len(new_numbers) > 3 else ''}"
                    )
                else:
                    self._logger.info(f"📱 All phone numbers from '{phone_column}' already in list")
            else:
                self._logger.warning(f"No valid phone numbers found in column '{phone_column}'")

        # Extract extensions from extension column
        if extension_column:
            extensions_data = self.input[extension_column].dropna().astype(str).unique().tolist()
            extracted_extensions = [ext.strip() for ext in extensions_data if ext.strip()]

            if extracted_extensions:
                existing_extensions = set(self.extensions)
                new_extensions = [ext for ext in extracted_extensions if ext not in existing_extensions]

                if new_extensions:
                    self.extensions.extend(new_extensions)
                    self._logger.info(
                        f"📞 Extracted {len(new_extensions)} extension(s) from column '{extension_column}': "
                        f"{', '.join(new_extensions[:5])}"
                        f"{' ...' if len(new_extensions) > 5 else ''}"
                    )
                else:
                    self._logger.info(f"📞 All extensions from '{extension_column}' already in list")
            else:
                self._logger.warning(f"No valid extensions found in column '{extension_column}'")

        # Warn if no phone numbers or extensions found
        if not phone_column and not extension_column:
            self._logger.warning(
                f"No phone number or extension columns found in input DataFrame. "
                f"Looking for: 'phone_number', 'phone_numbers', 'extension', 'extensions', 'extension_number'. "
                f"Available columns: {list(self.input.columns)}"
            )

    def _get_extension_from_phone(self, phone_number: str) -> str:
        """
        Get extension from phone number using the phone → extension mapping.

        Args:
            phone_number: Phone number to lookup

        Returns:
            Extension string or empty string if not found
        """
        if not phone_number:
            return ""

        # Normalize the phone number for comparison
        normalized_phone = self._normalize_phone_number(phone_number)

        # Check if we have the phone → extension mapping (created during extension lookup)
        if hasattr(self, '_phone_to_extension_map') and self._phone_to_extension_map:
            extension = self._phone_to_extension_map.get(normalized_phone, "")
            if extension:
                return extension

        return ""

    def _determine_bound(self, session: dict) -> str:
        """
        Determine if session is inbound or outbound based on participants.

        Logic:
        - If the participant with is_session_owner=true has the queried phone number → outbound
        - If the participant with is_session_owner=false has the queried phone number → inbound
        - If can't determine → return 'unknown'

        Args:
            session: Session dict with 'participants' and 'queried_phone_number'

        Returns:
            'outbound', 'inbound', or 'unknown'
        """
        participants = session.get("participants", [])
        queried_number = session.get("queried_phone_number", "").lstrip('+')

        if not participants or not queried_number:
            return "unknown"

        for participant in participants:
            is_owner = participant.get("is_session_owner", False)
            phone_number = participant.get("phone_number", "").lstrip('+')

            # Normalize for comparison
            queried_normalized = self._normalize_phone_number(queried_number)
            participant_normalized = self._normalize_phone_number(phone_number)

            if queried_normalized == participant_normalized:
                # Found our number in participants
                if is_owner:
                    return "outbound"  # We initiated the session
                else:
                    return "inbound"   # They contacted us

        return "unknown"

    async def _get_phone_numbers_from_extensions(
        self,
        extensions: List[str]
    ) -> Dict[str, List[str]]:
        """
        Map extensions to phone numbers.

        Hybrid approach:
        1. First check if we have local mapping from input DataFrame (extension + phone_number columns)
        2. If not, fallback to Zoom API lookup via /phone/users

        Args:
            extensions: List of extension numbers to lookup

        Returns:
            Dict mapping extension_number -> [phone_numbers]
        """
        if not extensions:
            return {}

        extension_to_numbers = {}

        # Check if we have local mapping from DataFrame
        if hasattr(self, '_extension_phone_map') and self._extension_phone_map:
            self._logger.info(f"📋 Using local extension→phone mapping from input DataFrame")

            for ext in extensions:
                ext_str = str(ext).strip()
                if ext_str in self._extension_phone_map:
                    phone_number = self._extension_phone_map[ext_str]
                    extension_to_numbers[ext_str] = [phone_number]
                    self._logger.info(f"  ✅ Extension {ext_str} → {phone_number}")

            # Check if all extensions were found
            found = set(extension_to_numbers.keys())
            missing = set(str(e).strip() for e in extensions) - found

            if missing:
                self._logger.warning(
                    f"  ⚠️ {len(missing)} extension(s) not in local mapping: {', '.join(sorted(missing)[:5])}"
                    f"{' ...' if len(missing) > 5 else ''}"
                )

            return extension_to_numbers

        # Fallback: Use Zoom API lookup (backward compatible)
        self._logger.info(f"📞 Looking up phone numbers via Zoom API for {len(extensions)} extension(s)...")

        url = f"{self.BASE_URL}/phone/users"
        params = {"page_size": 100}

        # Fetch all users with pagination
        all_users = []
        page = 0

        while True:
            try:
                data = await self._authed_api_get(url, params=params)
                users = data.get("users", [])

                if users:
                    all_users.extend(users)
                    self._logger.debug(f"  Page {page + 1}: Retrieved {len(users)} users")

                # Check pagination
                next_page = data.get("next_page_token")
                if not next_page:
                    break
                params["next_page_token"] = next_page
                page += 1

                # Safety limit
                if page >= 100:
                    self._logger.warning("Reached safety limit of 100 pages for users")
                    break

            except Exception as e:
                self._logger.error(f"Error fetching users: {e}")
                break

        self._logger.info(f"  Retrieved {len(all_users)} total users from /phone/users")

        # Build mapping
        extensions_set = set(str(e).strip() for e in extensions)
        found_extensions = set()

        for user in all_users:
            ext_number = user.get("extension_number")
            if ext_number is None:
                continue

            # Normalize extension (handle different formats)
            ext_str = str(int(float(ext_number))) if isinstance(ext_number, (int, float)) else str(ext_number).strip()

            if ext_str in extensions_set:
                found_extensions.add(ext_str)
                phone_numbers_list = user.get("phone_numbers", [])

                # Extract phone numbers from the list
                numbers = []
                for phone_obj in phone_numbers_list:
                    if isinstance(phone_obj, dict):
                        number = phone_obj.get("number")
                        if number:
                            numbers.append(number)
                    elif isinstance(phone_obj, str):
                        numbers.append(phone_obj)

                if numbers:
                    extension_to_numbers[ext_str] = numbers
                    self._logger.info(f"  ✅ Extension {ext_str}: {len(numbers)} phone number(s)")
                else:
                    self._logger.warning(f"  ⚠️ Extension {ext_str}: No phone numbers found")

        # Report missing extensions
        missing = extensions_set - found_extensions
        if missing:
            self._logger.warning(
                f"  ⚠️ {len(missing)} extension(s) not found: {', '.join(sorted(missing)[:5])}"
                f"{' ...' if len(missing) > 5 else ''}"
            )

        return extension_to_numbers

    async def _fetch_call_logs_data(self) -> pd.DataFrame:
        """
        Fetch call logs from Zoom Phone API with pagination.
        """
        if not self.from_date or not self.to_date:
            raise ComponentError("from_date/to_date are required")

        self._logger.info(f"📞 Fetching call logs from {self.from_date} to {self.to_date}...")
        url = f"{self.BASE_URL}/phone/call_logs"
        params = {"from": self.from_date, "to": self.to_date, "page_size": 100}

        all_logs: List[Dict[str, Any]] = []
        next_page = None
        page = 0

        while True:
            if next_page:
                params["next_page_token"] = next_page
            self._logger.info(f"📄 Fetching page {page + 1} of call logs...")
            data = await self._authed_api_get(url, params=params)
            items = data.get("call_logs", [])
            all_logs.extend(items)
            self._logger.info(f"📊 Retrieved {len(items)} call logs from page {page + 1}")

            next_page = data.get("next_page_token")
            page += 1
            if self.max_pages and page >= self.max_pages:
                self._logger.warning(f"Reached max_pages={self.max_pages}, stopping pagination early.")
                break
            if not next_page:
                break

        total_logs = len(all_logs)
        self._logger.info(f"✅ Total call logs retrieved: {total_logs}")

        # Create DataFrame and clean column names
        df = pd.json_normalize(all_logs) if all_logs else pd.DataFrame()
        df = self._clean_column_names(df)

        # Filter by extensions if provided
        if self._extensions_filter and not df.empty:
            self._logger.info(f"🔍 Filtering call logs by {len(self._extensions_filter)} extensions...")
            self._logger.debug(f"Extensions to filter: {self._extensions_filter[:10]}")

            # Try different possible extension field names from Zoom API
            extension_fields = [
                'owner_extension_number'
            ]
            filter_applied = False

            for field in extension_fields:
                if field in df.columns:
                    # Normalize Zoom extensions: convert float to int to string (removes .0)
                    # Handle NaN values and convert numeric values properly
                    def normalize_extension(val):
                        if pd.isna(val):
                            return None
                        try:
                            # Try to convert to int first (removes .0 from floats)
                            return str(int(float(val)))
                        except (ValueError, TypeError):
                            # If conversion fails, use string representation
                            return str(val).strip()

                    # Apply normalization
                    df['_normalized_ext'] = df[field].apply(normalize_extension)

                    # Debug: show sample values from Zoom data
                    zoom_extensions = df['_normalized_ext'].dropna().unique()[:10].tolist()
                    self._logger.debug(f"Sample extensions from Zoom '{field}' (normalized): {zoom_extensions}")

                    before_count = len(df)
                    df = df[df['_normalized_ext'].isin(self._extensions_filter)]
                    after_count = len(df)

                    # Clean up temporary column
                    df = df.drop(columns=['_normalized_ext'])
                    self._logger.info(
                        f"✅ Filtered by '{field}': {before_count} → {after_count} calls "
                        f"({after_count} matching extensions)"
                    )

                    # Debug: if no matches, show why
                    if after_count == 0:
                        self._logger.warning(
                            f"⚠️ No matches found! Comparing:\n"
                            f"  Input extensions (first 5): {self._extensions_filter[:5]}\n"
                            f"  Zoom extensions (first 5): {zoom_extensions[:5]}"
                        )

                    filter_applied = True
                    break

            if not filter_applied:
                self._logger.warning(
                    f"⚠️ Could not filter by extensions. Extension fields not found in DataFrame. "
                    f"Available columns: {list(df.columns)}"
                )

        return df

    async def recordings_meta(self, call_id: str) -> Dict[str, Any]:
        """
        GET /phone/call_logs/{id}/recordings
        Returns list of recordings with their ids and download_url.
        """
        url = f"{self.BASE_URL}/phone/call_logs/{call_id}/recordings"
        return await self._authed_api_get(url)

    async def _download_file(self, url: str, filename: Path = None, return_bytes: bool = False) -> Optional[tuple]:
        """
        Downloads a binary resource using HTTPService._get.

        Args:
            url: URL to download from
            filename: Path for disk storage (ignored if return_bytes=True)
            return_bytes: If True, returns (BytesIO, content_type, filename_str) instead of saving to disk

        Returns:
            If return_bytes=True: (BytesIO object, content_type, filename_str) or None on error
            If return_bytes=False: Path object or None on error
        """
        try:
            # Perform the GET with redirects enabled (important for zoom.us -> file.zoom.us endpoints)
            resp = await self._get(
                url=url,
                cookies=None,
                params=None,
                headers=self.headers,
                use_proxy=False,
                free_proxy=False,
                connect_timeout=10.0,
                read_timeout=120.0,
                write_timeout=10.0,
                pool_timeout=30.0,
                num_retries=2
            )
            # Raise if a 4xx/5xx status is returned
            resp.raise_for_status()

            # 1) Determine the final filename
            content_disposition = resp.headers.get("content-disposition") or resp.headers.get("Content-Disposition")
            content_type = resp.headers.get("Content-Type", self.content_type)
            server_name: Optional[str] = None

            if content_disposition:
                # Examples: attachment; filename="foo.mp3"
                from email.message import Message
                msg = Message()
                msg["Content-Disposition"] = content_disposition
                server_name = msg.get_param("filename", header="Content-Disposition")
                utf8_filename = msg.get_param("filename*", header="Content-Disposition")
                if utf8_filename:
                    # RFC 5987: filename*=UTF-8''<url-encoded>
                    _, enc_name = utf8_filename.split("''", 1)
                    server_name = urllib.parse.unquote(enc_name)

            # If the name comes from the URL (e.g., ?filename=call_recording_...mp3) and there was no header, use it
            if not server_name:
                try:
                    from urllib.parse import urlparse, parse_qs
                    q = parse_qs(urlparse(str(resp.request.url)).query)
                    if "filename" in q and q["filename"]:
                        server_name = q["filename"][0]
                except Exception:
                    pass

            # Get content
            content = resp.content  # already bytes in httpx

            # Return bytes if requested
            if return_bytes:
                file_data = BytesIO()
                file_data.write(content)
                file_data.seek(0)
                final_filename = server_name or (str(filename.name) if filename else "recording")
                return (file_data, content_type, final_filename)

            # Otherwise save to disk
            if "{filename}" in str(filename) and server_name:
                final_path = Path(str(filename).format(filename=server_name))
            else:
                final_path = Path(filename) if filename else Path(server_name or "recording")

            # Create destination folder
            final_path.parent.mkdir(parents=True, exist_ok=True)

            # Write to disk
            with open(final_path, "wb") as fp:
                fp.write(content)

            return final_path

        except Exception as e:
            self._logger.error(f"Download failed from {url}: {e}")
            return None

    async def _download_recording(self, download_url: str, call_id: str, recording_id: str):
        """
        Downloads a recording.

        Returns:
            If as_bytes=True: (BytesIO, content_type, filename) or None
            If as_bytes=False: Path or None
        """
        if self.as_bytes:
            # Return bytes instead of saving to disk
            result = await self._download_file(download_url, return_bytes=True)
            return result
        else:
            # Attempt 1: let the server define the name
            p = await self._download_file(download_url, self.save_path / "{filename}", return_bytes=False)
            if p:
                return p
            # Fallback in case Content-Disposition doesn't come
            fallback_path = self.save_path / f"{call_id}_{recording_id}.mp4"
            p = await self._download_file(download_url, fallback_path, return_bytes=False)
            return p

    async def _download_transcript(self, recording_id: str, call_id: str):
        """
        Downloads transcript by recordingId:
          GET /phone/recording_transcript/download/{recordingId}

        Returns:
            If as_bytes=True: (BytesIO, content_type, filename) or None
            If as_bytes=False: Path or None
        """
        url = f"{self.BASE_URL}/phone/recording_transcript/download/{recording_id}"

        if self.as_bytes:
            # Return bytes instead of saving to disk
            result = await self._download_file(url, return_bytes=True)
            return result
        else:
            # Attempt 1: trust Content-Disposition
            p = await self._download_file(url, self.transcripts_path / "{filename}", return_bytes=False)
            if p:
                return p
            # Fallback (we don't know exact extension: could be .txt/.vtt/.srt)
            fallback_path = self.transcripts_path / f"{call_id}_{recording_id}.txt"
            p = await self._download_file(url, fallback_path, return_bytes=False)
            return p

    # =========================
    # Flow entrypoint
    # =========================
    async def run(self):
        """Main entry point - dispatches to appropriate method based on type."""
        import time
        t0 = time.time()

        self._logger.info(f"🚀 Starting Zoom {self._fn.upper()} processing...")
        
        # Get the function to execute based on type
        fn = getattr(self, self._fn, None)
        if fn is None or not callable(fn):
            raise ComponentError(
                f"Unknown operation type: '{self._fn}'. "
                f"Supported types: 'call_logs', 'sms'"
            )
        
        # Execute the appropriate function
        self._result = await fn()
        
        # Add timing metric
        self.add_metric("DURATION_SEC", round(time.time() - t0, 3))
        return self._result
    
    async def call_logs(self):
        """Fetch call logs and optionally download recordings/transcripts."""
        import time
        t0 = time.time()

        self._logger.info("🚀 Starting Zoom Interface processing...")
        self._logger.info(f"📅 Date range: {self.from_date} to {self.to_date}")
        self._logger.info(f"📁 Recordings path: {self.save_path}")
        self._logger.info(f"📄 Transcripts path: {self.transcripts_path}")
        self._logger.info(f"⬇️ Download recordings: {self.download_recordings}")
        self._logger.info(f"📝 Download transcripts: {self.download_transcripts}")

        # Process input DataFrame BEFORE calling Zoom API (to extract extensions for filtering)
        if self.previous and hasattr(self, 'input') and self.input is not None:
            if hasattr(self.input, 'empty') and not self.input.empty:
                self._logger.info(f"📊 Received input DataFrame with {len(self.input)} rows")
                self._process_input_dataframe()

        # Ensure paths exist
        self._ensure_paths()

        # Call logs
        self._logger.info("📞 Fetching call logs...")
        df = await self._fetch_call_logs_data()
        
        # Log available columns for debugging
        if not df.empty:
            self._logger.info(f"📋 Available columns: {list(df.columns)}")

        # If no rows, basic metrics and exit
        if df.empty:
            self._logger.warning("⚠️ No call logs found in the specified date range")
            self.add_metric("NUMROWS", 0)
            self.add_metric("NUMCOLS", 0)
            self.add_metric("RECORDED_COUNT", 0)
            self.add_metric("DOWNLOADED_COUNT", 0)
            self.add_metric("TRANSCRIPTS_DOWNLOADED", 0)
            self.add_metric("SAVE_PATH", str(self.save_path))
            self.add_metric("TRANSCRIPTS_PATH", str(self.transcripts_path))
            self.add_metric("DURATION_SEC", round(time.time() - t0, 3))
            self._result = df
            return self._result

        self._logger.info(f"📊 Total call logs retrieved: {len(df)}")

        # Output columns based on storage mode
        if self.as_bytes:
            # For memory storage: file_data, content_type, downloaded_filename
            for col in ("file_data", "content_type", "downloaded_filename", "transcript_data", "transcript_filename"):
                if col not in df.columns:
                    df[col] = None
        else:
            # For disk storage: local_path (full path), recording_filename (filename only), transcript_paths, transcript_filename
            for col in ("local_path", "recording_filename", "transcript_paths", "transcript_filename"):
                if col not in df.columns:
                    df[col] = None  # None instead of an empty string

        # Filter recorded using Zoom Phone fields
        self._logger.info("🔍 Filtering recorded calls...")
        if "recording_status" in df.columns:
            # In case that field appears for a tenant
            recorded_mask = df["recording_status"].astype(str).str.lower().eq("recorded")
            recorded_df = df[recorded_mask]
            self._logger.info(f"📹 Found {len(recorded_df)} calls with recording_status='recorded'")
        else:
            # Robust fallback using has_recording / recording_id / recording_type
            has_rec = pd.Series(False, index=df.index)
            if "has_recording" in df.columns:
                has_rec = df["has_recording"].astype(str).str.lower().isin(["true", "1", "yes"])
                self._logger.info(f"📹 Found {has_rec.sum()} calls with has_recording=True")
            by_rec_id = df["recording_id"].notna() if "recording_id" in df.columns else False
            if "recording_id" in df.columns:
                self._logger.info(f"🆔 Found {by_rec_id.sum()} calls with recording_id")
            by_rec_type = df["recording_type"].notna() if "recording_type" in df.columns else False
            if "recording_type" in df.columns:
                self._logger.info(f"📋 Found {by_rec_type.sum()} calls with recording_type")
            recorded_df = df[has_rec | by_rec_id | by_rec_type]

        recorded_count = int(recorded_df.shape[0])
        if recorded_count == 0:
            self._logger.warning(
                "⚠️ No recorded calls found using has_recording/recording_id/recording_type. "
                "If you expected recordings, verify Zoom Phone recording settings/scopes."
            )
        else:
            self._logger.info(f"🎯 Processing {recorded_count} recorded calls...")

        # Query database for existing recordings if auto-skip is enabled
        if self.auto_skip_processed and recorded_count > 0:
            recorded_call_ids = recorded_df['call_id'].dropna().unique().tolist()
            if not recorded_call_ids:
                # Try 'id' column if 'call_id' is empty
                recorded_call_ids = recorded_df['id'].dropna().unique().tolist()

            if recorded_call_ids:
                self._existing_recordings = await self._fetch_existing_recordings(recorded_call_ids)
                self._logger.info(f"📊 Auto-skip status: {len(self._existing_recordings)}/{len(recorded_call_ids)} recordings already exist in database")
            else:
                self._logger.warning("No valid call_ids found for auto-skip query")

        downloaded = 0
        transcripts_downloaded = 0

        # Prepare separate lists for recordings and transcripts
        recordings_to_download = []  # New recordings from Zoom API
        recordings_from_s3 = []  # Existing recordings from S3
        transcripts_to_download = []
        calls_with_recordings = set()  # Track unique calls with recordings
        calls_with_transcripts = set()  # Track unique calls with transcripts
        
        # Global deduplicators per run
        seen_recording_keys = set()     # (call_id, recording_id) or (call_id, url) if there is no id
        seen_transcript_keys = set()    # (call_id, recording_id)
        
        for _, row in recorded_df.iterrows():
            call_short = str(row.get("call_id", "") or "").strip()
            call_uuid = str(row.get("id", "") or "").strip()
            call_ref = call_short or call_uuid
            if not call_ref:
                continue

            # Check if this call_id already exists in database
            if call_ref in self._existing_recordings:
                # Skip metadata fetch, add to S3 download list
                s3_filename = self._existing_recordings[call_ref]
                recordings_from_s3.append({
                    's3_filename': s3_filename,
                    'call_id': call_ref,
                    'recording_id': 'rec'  # Will be extracted from filename
                })
                continue

            try:
                meta = await self.recordings_meta(call_ref)
                
                # === RECORDINGS (prefer download_url and fall back to file_url) ===
                if self.download_recordings:
                    rec_entries: List[tuple[str, str]] = []  # (url, recording_id)

                    recs = meta.get("recordings")
                    if isinstance(recs, list) and recs:
                        for rec in recs:
                            url = rec.get("download_url") or rec.get("file_url")
                            if not url:
                                continue
                            rec_id = str(rec.get("id") or rec.get("recording_id") or "").strip()
                            # If there is no id, still add it; use the URL for deduplication
                            rec_entries.append((url, rec_id))
                    else:
                        # Flat object without a list
                        url = meta.get("download_url") or meta.get("file_url")
                        if url:
                            rec_id = str(meta.get("id") or meta.get("recording_id") or "").strip()
                            rec_entries.append((url, rec_id))

                    # Deduplicate by (call_id, recording_id) or (call_id, url) if there is no id
                    for url, rec_id in rec_entries:
                        key = (call_ref, rec_id or url)
                        if key in seen_recording_keys:
                            continue
                        seen_recording_keys.add(key)

                        recordings_to_download.append({
                            'url': url,
                            'call_id': call_ref,
                            # Use the real recording_id if it exists; otherwise use a readable fallback
                            'recording_id': rec_id or "rec"
                        })

                # === TRANSCRIPTS (by real recording_id) ===
                if self.download_transcripts:
                    transcript_ids: List[str] = []

                    recs = meta.get("recordings")
                    if isinstance(recs, list) and recs:
                        for rec in recs:
                            rid = str(rec.get("id") or rec.get("recording_id") or "").strip()
                            if rid:
                                transcript_ids.append(rid)
                    else:
                        rid = str(meta.get("id") or meta.get("recording_id") or "").strip()
                        if rid:
                            transcript_ids.append(rid)

                    # Deduplicate by (call_id, recording_id)
                    for rid in transcript_ids:
                        key = (call_ref, rid)
                        if key in seen_transcript_keys:
                            continue
                        seen_transcript_keys.add(key)

                        transcripts_to_download.append({
                            'recording_id': rid,
                            'call_id': call_ref
                        })
                        
            except Exception as e:
                self._logger.warning(f"Failed to get metadata for call {call_ref}: {e}")

        # STEP 1: Download recordings
        total_new_recordings = len(recordings_to_download)
        total_existing_recordings = len(recordings_from_s3)
        total_recordings = total_new_recordings + total_existing_recordings

        if total_recordings == 0:
            self._logger.info("🎥 No recordings to download")
        else:
            self._logger.info(f"🎥 Total recordings to process: {total_recordings}")
            if total_new_recordings > 0:
                self._logger.info(f"   📥 New recordings from Zoom API: {total_new_recordings}")
            if total_existing_recordings > 0:
                self._logger.info(f"   ♻️ Existing recordings from S3: {total_existing_recordings}")

        # Download NEW recordings from Zoom API
        if recordings_to_download:
            self._logger.info(f"🎥 Starting download of {total_new_recordings} NEW recording files from Zoom API...")

            if self.as_bytes:
                # Store in memory as BytesIO
                with tqdm(total=total_recordings, desc="🎥 Downloading recordings", unit="files", colour="blue") as pbar:
                    for recording_info in recordings_to_download:
                        try:
                            result = await self._download_recording(
                                recording_info['url'],
                                recording_info['call_id'],
                                recording_info['recording_id']
                            )
                            if result:
                                file_data, content_type, filename = result
                                calls_with_recordings.add(recording_info['call_id'])

                                # Update DataFrame with BytesIO data
                                # Use .at for single cell assignment (BytesIO objects don't support len())
                                call_id = recording_info['call_id']
                                mask = (df['call_id'] == call_id) | (df['id'] == call_id)
                                indices = df.index[mask].tolist()
                                for idx in indices:
                                    df.at[idx, 'file_data'] = file_data
                                    df.at[idx, 'content_type'] = content_type
                                    df.at[idx, 'downloaded_filename'] = filename

                        except Exception as e:
                            self._logger.error(f"❌ Recording download error: {str(e)}")

                        pbar.update(1)
            else:
                # Save to disk (original behavior)
                local_path_by_call = {}
                filenames_by_call = {}

                with tqdm(total=total_recordings, desc="🎥 Downloading recordings", unit="files", colour="blue") as pbar:
                    for recording_info in recordings_to_download:
                        try:
                            saved = await self._download_recording(
                                recording_info['url'],
                                recording_info['call_id'],
                                recording_info['recording_id']
                            )
                            if saved:
                                calls_with_recordings.add(recording_info['call_id'])
                                # Store the local path for this call_id
                                call_id = recording_info['call_id']
                                if call_id not in local_path_by_call:
                                    local_path_by_call[call_id] = []
                                    filenames_by_call[call_id] = []

                                local_path_by_call[call_id].append(str(saved))
                                # Extract just the filename from the full path
                                filenames_by_call[call_id].append(Path(saved).name)

                        except Exception as e:
                            self._logger.error(f"❌ Recording download error: {str(e)}")

                        pbar.update(1)

                # Update the DataFrame with the local paths and filenames
                for call_id, paths in local_path_by_call.items():
                    # Find the corresponding row in the DataFrame
                    mask = (df['call_id'] == call_id) | (df['id'] == call_id)
                    if mask.any() and paths:  # Only update if there are actual paths
                        # Join the paths with a semicolon
                        df.loc[mask, 'local_path'] = '; '.join(paths)
                        # Also store just the filenames
                        df.loc[mask, 'recording_filename'] = '; '.join(filenames_by_call[call_id])

        # Download EXISTING recordings from S3
        s3_success_count = 0
        s3_fallback_count = 0

        if recordings_from_s3:
            self._logger.info(f"♻️ Starting download of {total_existing_recordings} EXISTING recording files from S3...")

            if self.as_bytes:
                # Store in memory as BytesIO
                with tqdm(total=total_existing_recordings, desc="♻️ Downloading from S3", unit="files", colour="cyan") as pbar:
                    for recording_info in recordings_from_s3:
                        result = None
                        call_id = recording_info['call_id']

                        s3_download_worked = False
                        try:
                            # Try S3 download first
                            result = await self._download_recording_from_s3(
                                recording_info['s3_filename'],
                                recording_info['call_id'],
                                recording_info['recording_id']
                            )
                            if result:
                                s3_download_worked = True
                                s3_success_count += 1
                        except Exception as e:
                            self._logger.warning(f"⚠️ S3 download failed for {call_id}: {str(e)}")
                            result = None

                        # Fallback: Try Zoom API if S3 failed
                        if not result:
                            self._logger.info(f"🔄 Fallback: Downloading {call_id} from Zoom API...")
                            try:
                                # Get recording metadata from Zoom API
                                meta = await self.recordings_meta(call_id)

                                # Extract download URL
                                download_url = None
                                recs = meta.get("recordings")
                                if isinstance(recs, list) and recs:
                                    download_url = recs[0].get("download_url") or recs[0].get("file_url")
                                else:
                                    download_url = meta.get("download_url") or meta.get("file_url")

                                if download_url:
                                    # Download from Zoom API
                                    result = await self._download_recording(
                                        download_url,
                                        call_id,
                                        recording_info['recording_id']
                                    )
                                    if result:
                                        s3_fallback_count += 1
                                        self._logger.info(f"✅ Fallback successful for {call_id}")
                                else:
                                    self._logger.error(f"❌ No download URL found in Zoom API for {call_id}")
                            except Exception as fallback_error:
                                self._logger.error(f"❌ Fallback failed for {call_id}: {str(fallback_error)}")

                        # Update DataFrame if we got a result (from S3 or Zoom API)
                        if result:
                            file_data, content_type, filename = result
                            calls_with_recordings.add(call_id)

                            # Update DataFrame with BytesIO data
                            mask = (df['call_id'] == call_id) | (df['id'] == call_id)
                            indices = df.index[mask].tolist()
                            for idx in indices:
                                df.at[idx, 'file_data'] = file_data
                                df.at[idx, 'content_type'] = content_type
                                df.at[idx, 'downloaded_filename'] = filename
                        else:
                            self._logger.error(f"❌ Failed to download recording for {call_id} (both S3 and Zoom API failed)")

                        pbar.update(1)
            else:
                # Save to disk
                local_path_by_call = {}
                filenames_by_call = {}

                with tqdm(total=total_existing_recordings, desc="♻️ Downloading from S3", unit="files", colour="cyan") as pbar:
                    for recording_info in recordings_from_s3:
                        saved = None
                        call_id = recording_info['call_id']

                        s3_download_worked = False
                        try:
                            # Try S3 download first
                            saved = await self._download_recording_from_s3(
                                recording_info['s3_filename'],
                                recording_info['call_id'],
                                recording_info['recording_id']
                            )
                            if saved:
                                s3_download_worked = True
                                s3_success_count += 1
                        except Exception as e:
                            self._logger.warning(f"⚠️ S3 download failed for {call_id}: {str(e)}")
                            saved = None

                        # Fallback: Try Zoom API if S3 failed
                        if not saved:
                            self._logger.info(f"🔄 Fallback: Downloading {call_id} from Zoom API...")
                            try:
                                # Get recording metadata from Zoom API
                                meta = await self.recordings_meta(call_id)

                                # Extract download URL
                                download_url = None
                                recs = meta.get("recordings")
                                if isinstance(recs, list) and recs:
                                    download_url = recs[0].get("download_url") or recs[0].get("file_url")
                                else:
                                    download_url = meta.get("download_url") or meta.get("file_url")

                                if download_url:
                                    # Download from Zoom API
                                    saved = await self._download_recording(
                                        download_url,
                                        call_id,
                                        recording_info['recording_id']
                                    )
                                    if saved:
                                        s3_fallback_count += 1
                                        self._logger.info(f"✅ Fallback successful for {call_id}")
                                else:
                                    self._logger.error(f"❌ No download URL found in Zoom API for {call_id}")
                            except Exception as fallback_error:
                                self._logger.error(f"❌ Fallback failed for {call_id}: {str(fallback_error)}")

                        # Update paths if we got a result (from S3 or Zoom API)
                        if saved:
                            calls_with_recordings.add(call_id)
                            if call_id not in local_path_by_call:
                                local_path_by_call[call_id] = []
                                filenames_by_call[call_id] = []

                            local_path_by_call[call_id].append(str(saved))
                            filenames_by_call[call_id].append(Path(saved).name)
                        else:
                            self._logger.error(f"❌ Failed to download recording for {call_id} (both S3 and Zoom API failed)")

                        pbar.update(1)

                # Update the DataFrame with the local paths and filenames
                for call_id, paths in local_path_by_call.items():
                    mask = (df['call_id'] == call_id) | (df['id'] == call_id)
                    if mask.any() and paths:
                        df.loc[mask, 'local_path'] = '; '.join(paths)
                        df.loc[mask, 'recording_filename'] = '; '.join(filenames_by_call[call_id])

        # STEP 2: Download transcripts (only if enabled)
        if transcripts_to_download:
            total_transcripts = len(transcripts_to_download)
            self._logger.info(f"📝 Starting download of {total_transcripts} transcript files...")

            if self.as_bytes:
                # Store in memory as BytesIO
                with tqdm(total=total_transcripts, desc="📝 Downloading transcripts", unit="files", colour="green") as pbar:
                    for transcript_info in transcripts_to_download:
                        try:
                            result = await self._download_transcript(
                                transcript_info['recording_id'],
                                transcript_info['call_id']
                            )
                            if result:
                                file_data, content_type, filename = result
                                calls_with_transcripts.add(transcript_info['call_id'])
                                transcripts_downloaded += 1

                                # Update DataFrame with BytesIO data
                                # Use .at for single cell assignment (BytesIO objects don't support len())
                                call_id = transcript_info['call_id']
                                mask = (df['call_id'] == call_id) | (df['id'] == call_id)
                                indices = df.index[mask].tolist()
                                for idx in indices:
                                    df.at[idx, 'transcript_data'] = file_data
                                    df.at[idx, 'transcript_filename'] = filename

                        except Exception as e:
                            self._logger.error(f"❌ Transcript download error: {str(e)}")

                        pbar.update(1)
            else:
                # Save to disk (original behavior)
                transcript_paths_by_call = {}
                transcript_filenames_by_call = {}

                with tqdm(total=total_transcripts, desc="📝 Downloading transcripts", unit="files", colour="green") as pbar:
                    for transcript_info in transcripts_to_download:
                        try:
                            saved = await self._download_transcript(
                                transcript_info['recording_id'],
                                transcript_info['call_id']
                            )
                            if saved:
                                calls_with_transcripts.add(transcript_info['call_id'])
                                transcripts_downloaded += 1
                                # Store the local path for this call_id
                                call_id = transcript_info['call_id']
                                if call_id not in transcript_paths_by_call:
                                    transcript_paths_by_call[call_id] = []
                                    transcript_filenames_by_call[call_id] = []

                                transcript_paths_by_call[call_id].append(str(saved))
                                # Extract just the filename from the full path
                                transcript_filenames_by_call[call_id].append(Path(saved).name)

                        except Exception as e:
                            self._logger.error(f"❌ Transcript download error: {str(e)}")

                        pbar.update(1)

                # Update the DataFrame with the transcript paths and filenames
                for call_id, paths in transcript_paths_by_call.items():
                    # Find the corresponding row in the DataFrame
                    mask = (df['call_id'] == call_id) | (df['id'] == call_id)
                    if mask.any() and paths:  # Only update if there are actual paths
                        # Join the paths with a semicolon
                        df.loc[mask, 'transcript_paths'] = '; '.join(paths)
                        # Also store just the filenames
                        df.loc[mask, 'transcript_filename'] = '; '.join(transcript_filenames_by_call[call_id])
        else:
            self._logger.info("📝 No transcripts to download")

        # Calculate unique calls with successful downloads
        downloaded = len(calls_with_recordings)

        # Final summary
        self._logger.info("�� Processing Summary:")
        self._logger.info(f"   �� Total call logs: {len(df)}")
        self._logger.info(f"   📹 Recorded calls: {recorded_count}")
        self._logger.info(f"   🎥 Calls with recordings downloaded: {downloaded}")
        if self.auto_skip_processed:
            self._logger.info(f"      📥 New from Zoom API: {total_new_recordings}")
            self._logger.info(f"      ♻️ Existing from S3: {total_existing_recordings}")
            if s3_success_count > 0:
                self._logger.info(f"         ✅ Downloaded from S3: {s3_success_count}")
            if s3_fallback_count > 0:
                self._logger.info(f"         🔄 Fallback to Zoom API: {s3_fallback_count}")
        self._logger.info(f"   📝 Transcripts downloaded: {transcripts_downloaded}")

        if self.as_bytes:
            self._logger.info("   💾 Storage mode: In-memory (BytesIO objects)")
            self._logger.info("   📊 DataFrame columns: file_data, content_type, downloaded_filename")
        else:
            self._logger.info("   💾 Storage mode: Disk")
            self._logger.info(f"   📁 Recordings path: {self.save_path}")
            self._logger.info(f"   📄 Transcripts path: {self.transcripts_path}")
            self._logger.info("   📊 DataFrame columns: local_path (full path), recording_filename (filename only)")

        # Metrics
        self.add_metric("NUMROWS", int(df.shape[0]))
        self.add_metric("NUMCOLS", int(df.shape[1]))
        self.add_metric("RECORDED_COUNT", recorded_count)
        self.add_metric("DOWNLOADED_COUNT", downloaded)
        if self.auto_skip_processed:
            self.add_metric("NEW_FROM_ZOOM_API", total_new_recordings)
            self.add_metric("EXISTING_FROM_S3", total_existing_recordings)
            if s3_success_count > 0:
                self.add_metric("S3_SUCCESS_COUNT", s3_success_count)
            if s3_fallback_count > 0:
                self.add_metric("S3_FALLBACK_COUNT", s3_fallback_count)
        self.add_metric("TRANSCRIPTS_DOWNLOADED", transcripts_downloaded)
        self.add_metric("SAVE_PATH", str(self.save_path))
        self.add_metric("TRANSCRIPTS_PATH", str(self.transcripts_path))
        self.add_metric("DURATION_SEC", round(time.time() - t0, 3))

        # Preview in debug mode
        if self._debug:
            print("\n=== DataFrame Preview ===")
            try:
                print(df.head(10))
            except Exception:
                print(df.head())
            print("\n=== Column dtypes ===")
            for column, dtype in df.dtypes.items():
                sample = None
                if not df.empty:
                    try:
                        sample = df[column].iloc[0]
                    except Exception:
                        sample = "N/A"
                print(f"{column} -> {dtype} -> {sample}")

        duration = round(time.time() - t0, 3)
        self._logger.info(f"🎉 Zoom Interface processing completed in {duration} seconds")
        self._result = df
        return self._result

    async def sms(self) -> pd.DataFrame:
        """
        Fetch SMS sessions and messages for specified phone numbers.
        
        This method:
        1. Fetches SMS sessions for each provided phone number
        2. Retrieves all messages for those sessions
        3. Returns a DataFrame with messages and session context
        """
        import time
        from datetime import datetime
        
        # Process input DataFrame to extract phone numbers and extensions if available
        if self.previous and hasattr(self, 'input') and self.input is not None:
            if hasattr(self.input, 'empty') and not self.input.empty:
                self._logger.info(f"📊 Received input DataFrame with {len(self.input)} rows")
                self._process_input_dataframe_for_sms()
        
        # If we have extensions, lookup their phone numbers
        if self.extensions:
            self._logger.info(f"🔍 Found {len(self.extensions)} extension(s) to lookup")
            extension_to_numbers = await self._get_phone_numbers_from_extensions(self.extensions)

            # Create phone_number → extension mapping for later use
            if not hasattr(self, '_phone_to_extension_map'):
                self._phone_to_extension_map = {}

            # Add all phone numbers from extensions and track reverse mapping
            for ext, numbers in extension_to_numbers.items():
                for number in numbers:
                    # Normalize for consistency
                    normalized_number = number.lstrip('+')

                    if normalized_number not in self.phone_numbers:
                        self.phone_numbers.append(normalized_number)

                    # Track phone → extension mapping
                    self._phone_to_extension_map[normalized_number] = ext

            total_numbers_from_extensions = sum(len(nums) for nums in extension_to_numbers.values())
            self._logger.info(f"✅ Mapped {len(extension_to_numbers)} extension(s) to {total_numbers_from_extensions} phone number(s)")
            self.add_metric("EXTENSIONS_PROVIDED", len(self.extensions))
            self.add_metric("PHONE_NUMBERS_FROM_EXTENSIONS", total_numbers_from_extensions)
        
        # Validate we have phone numbers (from kwargs, input DataFrame, or extension lookup)
        if not self.phone_numbers:
            raise ConfigError(
                "No phone numbers found. Provide one of: "
                "(1) 'phone_numbers' parameter, "
                "(2) 'extensions' parameter, "
                "(3) input DataFrame with 'phone_number'/'phone_numbers'/'extension' column."
            )
        
        self._logger.info("📱 Starting SMS extraction...")
        self._logger.info(f"📞 Phone numbers: {', '.join(self.phone_numbers)}")
        if self.from_date or self.to_date:
            self._logger.info(f"📅 Date range: {self.from_date or 'N/A'} to {self.to_date or 'N/A'}")
        
        # Step 1: Fetch SMS sessions for all phone numbers
        self._logger.info(f"📊 Step 1: Fetching SMS sessions for {len(self.phone_numbers)} phone number(s)...")
        all_sessions = []
        
        for phone_number in self.phone_numbers:
            self._logger.info(f"  Querying sessions for {phone_number}...")
            
            # Remove '+' from phone number - Zoom SMS API expects format without '+'
            # Example from API spec: '18108001001' not '+18108001001'
            phone_for_api = phone_number.lstrip('+')

            url = f"{self.BASE_URL}/phone/sms/sessions"
            params = {
                "phone_number": phone_for_api,
                "page_size": 100  # Always fetch 100 sessions per page
            }
            
            # Add date filters if provided
            # SMS API requires 'to' when 'from' is specified, max range is 1 month
            if self.from_date:
                params["from"] = self.from_date
                
                # If to_date not provided, calculate it (max 31 days from from_date or today)
                if self.to_date:
                    params["to"] = self.to_date
                else:
                    # Auto-calculate 'to' as minimum of (from_date + 31 days, today)
                    from datetime import datetime, timedelta
                    from_dt = datetime.strptime(self.from_date, "%Y-%m-%d")
                    max_to_dt = from_dt + timedelta(days=31)
                    today_dt = datetime.now()
                    to_dt = min(max_to_dt, today_dt)
                    params["to"] = to_dt.strftime("%Y-%m-%d")
                    self._logger.info(f"  Auto-calculated 'to' date: {params['to']} (required by SMS API)")
                
                # Add filter_type when using date filters
                # Options: sent_message_time, received_message_time, last_message_time, sent_received_message_time
                params["filter_type"] = "last_message_time"
                
            elif self.to_date:
                # If only to_date provided, warn user
                self._logger.warning("'to_date' specified without 'from_date' - ignoring (SMS API requires both)")
            
            # Paginate through sessions
            page = 0
            while True:
                try:
                    data = await self._authed_api_get(url, params=params)
                    sessions = data.get("sms_sessions", [])  # API returns 'sms_sessions' not 'sessions'

                    
                    if sessions:
                        # Add provenance
                        for session in sessions:
                            session["queried_phone_number"] = phone_number
                            session["fetched_at"] = datetime.utcnow().isoformat() + "Z"
                        all_sessions.extend(sessions)
                        self._logger.info(f"    Page {page + 1}: Retrieved {len(sessions)} session(s)")
                    
                    # Check pagination
                    next_page = data.get("next_page_token")
                    page += 1
                    if self.max_pages and page >= self.max_pages:
                        self._logger.warning(f"    Reached max_pages={self.max_pages}, stopping pagination")
                        break
                    if not next_page:
                        break
                    params["next_page_token"] = next_page
                    
                except Exception as e:
                    self._logger.error(f"    Error fetching sessions for {phone_number}: {e}")
                    break
        
        self._logger.info(f"✅ Step 1 complete: Found {len(all_sessions)} total session(s)")
        self.add_metric("SMS_SESSIONS_COUNT", len(all_sessions))
        
        if not all_sessions:
            self._logger.warning("⚠️ No SMS sessions found for the provided phone numbers")
            empty_df = pd.DataFrame()
            self.add_metric("NUMROWS", 0)
            self.add_metric("NUMCOLS", 0)
            self.add_metric("SMS_MESSAGES_COUNT", 0)
            return empty_df
        
        # Step 2: Fetch messages for each session and build session records
        self._logger.info(f"📨 Step 2: Fetching messages for {len(all_sessions)} session(s)...")
        session_records = []
        total_messages = 0

        for idx, session in enumerate(all_sessions, 1):
            session_id = session.get("session_id") or session.get("id")
            if not session_id:
                self._logger.warning(f"  Session {idx}: Missing session ID, skipping")
                continue

            session_messages = []

            # Check if messages are already included in the session object
            messages_in_session = session.get("sms_histories") or session.get("messages")
            if messages_in_session:
                self._logger.info(f"  Session {idx}: Found {len(messages_in_session)} message(s) in session object")
                session_messages = messages_in_session
            else:
                # Fetch messages from the session details endpoint
                try:
                    session_details_url = f"{self.BASE_URL}/phone/sms/sessions/{session_id}"
                    session_params = {}
                    session_page = 0

                    # Get first page
                    session_details = await self._authed_api_get(session_details_url, params=session_params)
                    messages = session_details.get("sms_histories", [])

                    if messages:
                        self._logger.info(f"  Session {idx}: Found {len(messages)} message(s)")
                        session_messages.extend(messages)

                    # Handle pagination
                    next_page = session_details.get("next_page_token")
                    while next_page:
                        session_page += 1

                        if self.max_pages and session_page >= self.max_pages:
                            self._logger.debug(f"    Reached max_pages={self.max_pages} for session {session_id}")
                            break

                        session_params["next_page_token"] = next_page
                        session_details = await self._authed_api_get(session_details_url, params=session_params)
                        messages = session_details.get("sms_histories", [])

                        if messages:
                            self._logger.info(f"    Page {session_page + 1}: Found {len(messages)} message(s)")
                            session_messages.extend(messages)

                        next_page = session_details.get("next_page_token")

                except Exception as session_error:
                    self._logger.error(f"  Session {idx}: Error fetching messages - {session_error}")
                    continue

            # Build session record (1 row = 1 session)
            queried_phone = session.get("queried_phone_number", "")
            bound = self._determine_bound(session)

            # Try to find extension from queried phone number
            extension = self._get_extension_from_phone(queried_phone)

            # Calculate last_message_time from messages if not in session
            last_message_time = session.get("last_message_time")
            if not last_message_time and session_messages:
                # Find the most recent message by date_time
                message_times = [msg.get("date_time") for msg in session_messages if msg.get("date_time")]
                if message_times:
                    last_message_time = max(message_times)

            # Extract participant details
            participants = session.get("participants", [])
            owner_number = None
            owner_name = None
            other_number = None

            for participant in participants:
                is_owner = participant.get("is_session_owner", False)
                phone = participant.get("phone_number", "")

                if is_owner:
                    owner_number = phone
                    owner_name = participant.get("display_name", "")
                else:
                    other_number = phone

            session_record = {
                "session_id": session_id,
                "extension": extension,
                "phone_number": queried_phone,
                "bound": bound,
                "owner_number": owner_number,
                "owner_name": owner_name,
                "other_number": other_number,
                "session_type": session.get("session_type"),
                "last_message_time": last_message_time,
                "last_access_time": session.get("last_access_time"),
                "message_count": len(session_messages),
                "messages": session_messages,  # JSON with all messages
                "participants": session.get("participants", []),
                "fetched_at": session.get("fetched_at")
            }

            session_records.append(session_record)
            total_messages += len(session_messages)

        self._logger.info(f"✅ Step 2 complete: Processed {len(session_records)} session(s) with {total_messages} total message(s)")
        self.add_metric("SMS_SESSIONS_COUNT", len(session_records))
        self.add_metric("SMS_MESSAGES_COUNT", total_messages)

        # Step 3: Build DataFrame (1 row per session)
        if not session_records:
            self._logger.warning("⚠️ No SMS sessions with data found")
            empty_df = pd.DataFrame()
            self.add_metric("NUMROWS", 0)
            self.add_metric("NUMCOLS", 0)
            return empty_df

        self._logger.info("📊 Step 3: Building DataFrame (1 row = 1 session)...")
        df = pd.DataFrame(session_records)

        self._logger.info(f"✅ SMS extraction complete: {len(df)} session(s) with {total_messages} total message(s)")
        self._logger.info(f"📋 DataFrame columns: {list(df.columns)}")
        
        # Add metrics
        self.add_metric("NUMROWS", len(df))
        self.add_metric("NUMCOLS", len(df.columns))
        
        return df

    async def close(self):
        """
        Cleanup.
        """
        self._access_token = None
        return True
