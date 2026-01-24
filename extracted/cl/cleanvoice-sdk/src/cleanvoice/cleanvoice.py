"""Main Cleanvoice SDK class."""

import time
from typing import Any, Callable, Dict, Optional, Union

from .client import ApiClient
from .file_handler import (
    is_valid_video_file,
    normalize_file_input,
    validate_config,
)
from .types import (
    ApiError,
    CleanvoiceConfig,
    CreateEditRequest,
    EditInput,
    EditResult,
    ProcessingConfig,
    ProcessResult,
    RetrieveEditResponse,
)


class Cleanvoice:
    """Main Cleanvoice SDK class."""

    def __init__(self, config: CleanvoiceConfig):
        """Initialize Cleanvoice SDK.

        Args:
            config: Configuration including API key

        Raises:
            ValueError: If API key is not provided
        """
        if isinstance(config, dict):
            config = CleanvoiceConfig(**config)

        if not config.api_key:
            raise ValueError("API key is required")

        self.api_client = ApiClient(config)

    def process(
        self,
        file_input: str,
        config: Optional[Union[ProcessingConfig, Dict[str, Any]]] = None,
        progress_callback: Optional[Callable[[Dict[str, Any]], None]] = None,
    ) -> ProcessResult:
        """Process audio/video file with Cleanvoice AI.

        Args:
            file_input: URL to audio/video file
            config: Processing configuration options
            progress_callback: Optional callback function for progress updates

        Returns:
            ProcessResult with processed audio and transcript data

        Raises:
            ApiError: If API request fails
            FileValidationError: If file validation fails
        """
        if config is None:
            config = ProcessingConfig()
        elif isinstance(config, dict):
            config = ProcessingConfig(**config)

        try:
            # Validate configuration
            validate_config(config.model_dump(exclude_none=True))

            # Normalize file input to URL
            file_url = normalize_file_input(file_input, self.api_client)

            # Auto-detect video if not specified
            if config.video is None:
                config.video = is_valid_video_file(file_input)

            # Create edit request
            edit_request = CreateEditRequest(
                input=EditInput(
                    files=[file_url],
                    config=config,
                )
            )

            edit_response = self.api_client.create_edit(edit_request)

            # Poll for completion
            result = self._poll_for_completion(
                edit_response.id, progress_callback=progress_callback
            )

            # Transform to simplified format
            return self._transform_result(result)

        except Exception as error:
            if isinstance(error, (ApiError, ValueError)):
                raise error
            raise ApiError(f"An unknown error occurred during processing: {str(error)}")

    def create_edit(
        self,
        file_input: str,
        config: Optional[Union[ProcessingConfig, Dict[str, Any]]] = None,
    ) -> str:
        """Create an edit job and return the ID for manual polling.

        Args:
            file_input: URL to audio/video file
            config: Processing configuration options

        Returns:
            Edit ID for polling

        Raises:
            ApiError: If API request fails
            FileValidationError: If file validation fails
        """
        if config is None:
            config = ProcessingConfig()
        elif isinstance(config, dict):
            config = ProcessingConfig(**config)

        try:
            validate_config(config.model_dump(exclude_none=True))
            file_url = normalize_file_input(file_input, self.api_client)

            if config.video is None:
                config.video = is_valid_video_file(file_input)

            edit_request = CreateEditRequest(
                input=EditInput(
                    files=[file_url],
                    config=config,
                )
            )

            response = self.api_client.create_edit(edit_request)
            return response.id

        except Exception as error:
            if isinstance(error, (ApiError, ValueError)):
                raise error
            raise ApiError(
                f"An unknown error occurred while creating edit: {str(error)}"
            )

    def get_edit(self, edit_id: str) -> RetrieveEditResponse:
        """Get the status and results of an edit job.

        Args:
            edit_id: The edit ID returned from create_edit

        Returns:
            Edit status and results

        Raises:
            ApiError: If API request fails
        """
        try:
            return self.api_client.retrieve_edit(edit_id)
        except Exception as error:
            if isinstance(error, ApiError):
                raise error
            raise ApiError(
                f"An unknown error occurred while retrieving edit: {str(error)}"
            )

    def upload_file(self, file_path: str, filename: Optional[str] = None) -> str:
        """Upload a local file and return the URL for processing.

        Args:
            file_path: Path to the local file to upload
            filename: Optional custom filename for the upload

        Returns:
            URL of the uploaded file

        Raises:
            ApiError: If upload fails
            FileValidationError: If file validation fails
        """
        try:
            from .file_handler import upload_local_file
            from pathlib import Path
            
            if filename is None:
                filename = Path(file_path).name
            
            # Override the filename in the upload function by getting signed URL directly
            signed_url = self.api_client.get_signed_upload_url(filename)
            self.api_client.upload_file(file_path, signed_url)
            
            # Return the public URL for the uploaded file
            from urllib.parse import urlparse, urlunparse
            parsed = urlparse(signed_url)
            public_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', '', ''))
            
            return public_url
            
        except Exception as error:
            if isinstance(error, (ApiError, ValueError)):
                raise error
            raise ApiError(f"File upload failed: {str(error)}")

    def download_file(self, url: str, output_path: Optional[str] = None) -> str:
        """Download a processed file from the given URL.

        Args:
            url: URL of the processed file to download
            output_path: Optional local path to save the file. If not provided, 
                        will use the filename from the URL in current directory

        Returns:
            Path to the downloaded file

        Raises:
            ApiError: If download fails
        """
        try:
            import requests
            from urllib.parse import urlparse
            from pathlib import Path
            
            # If no output path provided, derive from URL
            if output_path is None:
                parsed_url = urlparse(url)
                filename = Path(parsed_url.path).name
                if not filename:
                    filename = "downloaded_audio.mp3"  # Default filename
                output_path = filename
            
            # Download the file
            response = requests.get(url, stream=True, timeout=300)
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return output_path
            
        except Exception as error:
            if isinstance(error, (ApiError, ValueError)):
                raise error
            raise ApiError(f"File download failed: {str(error)}")

    def process_and_download(
        self,
        file_input: str,
        output_path: Optional[str] = None,
        config: Optional[Union[ProcessingConfig, Dict[str, Any]]] = None,
        progress_callback: Optional[Callable[[Dict[str, Any]], None]] = None,
    ) -> tuple[ProcessResult, str]:
        """Process audio/video file and download the result.

        Args:
            file_input: URL to audio/video file or local file path
            output_path: Optional local path to save the processed file
            config: Processing configuration options
            progress_callback: Optional callback function for progress updates

        Returns:
            Tuple of (ProcessResult, downloaded_file_path)

        Raises:
            ApiError: If processing or download fails
            FileValidationError: If file validation fails
        """
        # Process the file
        result = self.process(file_input, config, progress_callback)
        
        # Download the processed file
        downloaded_path = self.download_file(result.audio.url, output_path)
        
        return result, downloaded_path

    def check_auth(self) -> Dict[str, Any]:
        """Check if authentication is working.

        Returns:
            Account information

        Raises:
            ApiError: If authentication fails
        """
        try:
            return self.api_client.check_auth()
        except Exception as error:
            if isinstance(error, ApiError):
                raise error
            raise ApiError(f"Authentication check failed: {str(error)}")

    def _poll_for_completion(
        self,
        edit_id: str,
        max_attempts: int = 60,
        initial_delay: float = 2.0,
        progress_callback: Optional[Callable[[Dict[str, Any]], None]] = None,
    ) -> RetrieveEditResponse:
        """Poll for edit completion with exponential backoff.

        Args:
            edit_id: Edit ID to poll
            max_attempts: Maximum number of polling attempts
            initial_delay: Initial delay in seconds
            progress_callback: Optional callback for progress updates

        Returns:
            Final edit result

        Raises:
            ApiError: If polling fails or times out
        """
        attempts = 0
        delay = initial_delay

        while attempts < max_attempts:
            response = self.api_client.retrieve_edit(edit_id)

            # Call progress callback if provided
            if progress_callback:
                try:
                    progress_callback(
                        {
                            "status": response.status,
                            "result": response.result,
                            "edit_id": edit_id,
                            "attempt": attempts + 1,
                        }
                    )
                except Exception:
                    pass  # Don't let callback errors break polling

            if response.status == "SUCCESS":
                return response

            if response.status == "FAILURE":
                raise ApiError("Edit processing failed")

            # Wait before next attempt
            time.sleep(delay)

            attempts += 1
            # Exponential backoff with max delay of 30 seconds
            delay = min(delay * 1.5, 30.0)

        raise ApiError("Edit processing timeout - maximum polling attempts reached")

    def _transform_result(self, response: RetrieveEditResponse) -> ProcessResult:
        """Transform API response to simplified format.

        Args:
            response: API response

        Returns:
            Simplified result format

        Raises:
            ApiError: If result transformation fails
        """
        if not response.result:
            raise ApiError("Edit result not available")

        # Check if this is a completed result (EditResult) vs in-progress
        if isinstance(response.result, EditResult):
            # This is an EditResult (completed processing)
            edit_result = response.result

            audio_result = ProcessResult.AudioResult(
                url=edit_result.download_url,
                filename=edit_result.filename,
                statistics=edit_result.statistics,
            )

            result = ProcessResult(audio=audio_result)

            # Add transcript data if available
            if edit_result.transcription:
                transcript = edit_result.transcription

                # Combine all paragraph text for simplified access
                full_text = " ".join(p.text for p in transcript.paragraphs)

                transcript_result = ProcessResult.TranscriptResult(
                    text=full_text,
                    paragraphs=transcript.paragraphs,
                    detailed=transcript.transcription,
                )

                # Add summarization data if available
                if edit_result.summarization:
                    summary_data = edit_result.summarization
                    transcript_result.summary = summary_data.summary
                    transcript_result.title = summary_data.title
                    transcript_result.chapters = summary_data.chapters

                result.transcript = transcript_result

            return result
        else:
            # This is ProcessingProgress (still in progress)
            raise ApiError(
                "Edit is still in progress, cannot transform to final result"
            )
