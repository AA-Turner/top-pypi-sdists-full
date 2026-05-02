import asyncio
import aiohttp
import mimetypes
from pathlib import Path
from io import BytesIO
from collections.abc import Callable
from tqdm import tqdm
from ..utils import is_empty
from ..exceptions import ComponentError, DataNotFound
from ..interfaces.sassie import SassieClient
from ..interfaces.http import HTTPService
from .flow import FlowComponent

class Sassie(SassieClient, FlowComponent):
    """
    Sassie

    Overview

        Get Data from Sassie API.

    Properties (inherited from Sassie)

        :widths: auto

        | domain             |   Yes    | Domain of Sassie API                                                             |
        | credentials        |   Yes    | Credentials to establish connection with Polestar site (user and password)       |
        |                    |          | get credentials from environment if null.                                        |
        | data               |   No     | Type of data to retrieve (surveys, questions, jobs, waves, locations, clients,   |
        |                    |          | download_photos)                                                                 |
        | filter             |   No     | List of filters to apply to the results. Each filter must have:                  |
        |                    |          | - column: The column name to filter on                                           |
        |                    |          | - operator: One of: eq (equals), lt (less than), gt (greater than),              |
        |                    |          |   lte (less than or equal), gte (greater than or equal), btw (between)           |
        |                    |          | - value: The value to compare against                                            |
        | masks              |   No     | A dictionary mapping mask strings to replacement strings used for                |
        |                    |          | replacing values in filters.                                                     |
        | column             |   No     | Column name containing photo URLs (default: 'photo_path')                        |
        | filename           |   No     | Column name for filename template (default: 'photo')                             |
        | path               |   No     | Local directory to save downloaded photos (optional)                             |
        | bk_path            |   No     | Backup directory for downloaded photos (optional)                                |
        | as_bytes           |   No     | Store photos in memory as BytesIO objects (default: True)                        |
        | content_type       |   No     | Default content type for photos (default: 'image/jpeg')                          |

        Save the downloaded files on the new destination.

        Example:


        Example for downloading photos to memory:


        Example for downloading photos to disk:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          Sassie:
          domain: SASSIE_PROD_URL
          data: locations
          credentials:
          client_id: SASSIE_CLIENT_ID
          client_secret: SASSIE_CLIENT_SECRET
          filter:
          - column: updated
          operator: eq
          value: '{today}'
          masks:
          '{today}':
          - today
          - mask: '%Y-%m-%d'
        ```
    """
    _version = "1.0.0"
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        # Download photos specific parameters
        self.column: str = kwargs.get('column', 'photo_path')
        self.filename: str = kwargs.get('filename', 'photo')
        self.path: str = kwargs.get('path', '')
        self.bk_path: str = kwargs.get('bk_path', '')
        self.as_bytes: bool = kwargs.get('as_bytes', True)  # Default to memory storage
        self.content_type: str = kwargs.get('content_type', 'image/jpeg')

        self._semaphore_limit = kwargs.get('semaphore_limit', 10)
        
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)
        self._semaphore = asyncio.Semaphore(self._semaphore_limit)

    async def start(self, **kwargs):
        self.data = kwargs.get('data')
        
        # Only process credentials and filters for non-download_photos operations
        if self.data != 'download_photos':
            # Apply masks to filter values if present
            if hasattr(self, 'filters') and hasattr(self, 'masks'):
                for filter_item in self.filters:
                    filter_item['value'] = self.mask_replacement(filter_item['value'])

            self.processing_credentials()
            self.client_id: str = self.credentials.get('username', None)
            self.client_secret: str = self.credentials.get('password', None)
            await self.get_bearer_token()
            await super(Sassie, self).start(**kwargs)
        
        return True

    async def close(self):
        pass

    async def run(self):
        # Map data types to their corresponding methods
        data_methods = {
            'surveys': self.get_surveys,
            'questions': self.get_questions,
            'jobs': self.get_jobs,
            'waves': self.get_waves,
            'locations': self.get_locations,
            'clients': self.get_clients,
            'responses': self.get_responses,
            'question_sections': self.get_question_sections,
            'question_properties': self.get_question_properties,
            'custom': self.get_custom,
            'download_photos': self.download_photos,
        }

        if self.data not in data_methods:
            raise ComponentError(f"{self.__name__}: Unsupported data type '{self.data}'. Supported types are: {', '.join(data_methods.keys())}")

        try:
            if self.data == 'download_photos':
                self._result = await data_methods[self.data]()
            else:
                self._result = await self.create_dataframe(await data_methods[self.data]())
                
            if is_empty(self._result):
                raise DataNotFound(f"{self.__name__}: Data Not Found")
        except Exception as e:
            raise ComponentError(f"{self.__name__}: Error retrieving {self.data} data: {str(e)}")

        if self._debug:
            print(self._result)
            columns = list(self._result.columns)
            print(f"Debugging: {self.__name__} ===")
            for column in columns:
                t = self._result[column].dtype
                print(column, "->", t, "->", self._result[column].iloc[0] if not self._result.empty else "Empty DataFrame")
        return self._result

    async def fetch_and_save(self, session, url, save_path_base: Path, backup_path_base: Path, row_index: int, data, pbar=None):
        """Download and save a single photo - supports both memory and disk storage"""
        filename = save_path_base.name
        
        # Check if file already exists in backup (only for disk storage)
        if not self.as_bytes:
            for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp']:
                if (backup_path_base.with_suffix(ext)).exists():
                    if pbar:
                        pbar.update(1)
                    return (backup_path_base.with_suffix(ext)).name, None

        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    content_type = resp.headers.get('Content-Type', '')
                    guessed_extension = mimetypes.guess_extension(content_type.split(";")[0].strip()) or ''
                    
                    # Read content
                    content = await resp.read()
                    
                    if self.as_bytes:
                        # Store in memory as BytesIO
                        file_data = BytesIO()
                        file_data.write(content)
                        file_data.seek(0)
                        
                        # Update the DataFrame with file data
                        data.at[row_index, 'file_data'] = file_data
                        data.at[row_index, 'content_type'] = content_type or self.content_type
                        
                        # Generate filename with extension
                        final_filename = f"{filename}{guessed_extension}"
                        data.at[row_index, 'downloaded_filename'] = final_filename
                        
                        if pbar:
                            pbar.update(1)
                        return final_filename, file_data
                    else:
                        # Save to disk
                        final_path = save_path_base.with_suffix(guessed_extension)
                        
                        if not final_path.exists():
                            final_path.write_bytes(content)
                        
                        # Update DataFrame with file path
                        data.at[row_index, 'file_path'] = str(final_path)
                        data.at[row_index, 'content_type'] = content_type or self.content_type
                        
                        if pbar:
                            pbar.update(1)
                        return final_path.name, None
                else:
                    self._logger.error(f"❌ Error {resp.status} to download {url}")
        except Exception as e:
            self._logger.error(f"⚠️  Error to download {url}: {e}")

        if pbar:
            pbar.update(1)
        return save_path_base.name, None

    async def download_photos(self):
        """Download photos from URLs in DataFrame"""
        if not self.previous:
            raise ComponentError(f"{self.__name__}: download_photos requires input data from previous step")
        
        data = self.input
        if data is None or data.empty:
            raise DataNotFound(f"{self.__name__}: No input data available for download_photos")
        
        if self.column not in data.columns:
            raise ComponentError(f"{self.__name__}: Column '{self.column}' not found in input data")
        
        # For disk storage, path is required
        if not self.as_bytes and not self.path:
            raise ComponentError(f"{self.__name__}: 'path' parameter is required when as_bytes=false")
        
        # Create directories if saving to disk
        if not self.as_bytes:
            path = Path(self.path)
            path.mkdir(parents=True, exist_ok=True)
            bk_path = Path(self.bk_path) if self.bk_path else path
            bk_path.mkdir(parents=True, exist_ok=True)
        
        # Add new columns to DataFrame
        if self.as_bytes:
            data['file_data'] = None
            data['content_type'] = None
            data['downloaded_filename'] = None
        else:
            data['file_path'] = None
            data['content_type'] = None
        
        # Initialize progress bar
        total_photos = len(data)
        # Always show progress bar
        pbar = tqdm(
            total=total_photos,
            desc="📥 Downloading photos",
            unit="photos",
            ncols=100,
            colour="green"
        )
        
        try:
            async with aiohttp.ClientSession() as session:
                tasks = []
                for index, row in data.iterrows():
                    url = row[self.column]
                    base_name = row.get(self.filename, f'file_{index}')
                    
                    if self.as_bytes:
                        # For memory storage, we don't need actual paths
                        save_path = Path(base_name)
                        backup_path = Path(base_name)
                    else:
                        # For disk storage
                        save_path = path / base_name
                        backup_path = bk_path / base_name
                    
                    tasks.append(self.fetch_and_save(session, url, save_path, backup_path, index, data, pbar))

                results = await asyncio.gather(*tasks)
                
                # Update filename column with results
                filenames = [result[0] for result in results]
                data[self.filename] = filenames

            downloaded_count = len([r for r in results if r[0] is not None])
            self._logger.info(f"Downloaded {downloaded_count}/{len(results)} photos")
            
            if self.as_bytes:
                self._logger.info("Photos stored in memory as BytesIO objects")
            else:
                self._logger.info(f"Photos saved to disk at {self.path}")
            
            if self._debug:
                columns = list(data.columns)
                for column in columns:
                    if column in ['file_data']:
                        self._logger.debug(f"{column} -> BytesIO objects")
                    else:
                        t = data[column].dtype
                        self._logger.debug(f"{column} -> {t} -> {data[column].iloc[0] if not data.empty else 'Empty DataFrame'}")

        finally:
            # Close progress bar
            if pbar:
                pbar.close()

        return data