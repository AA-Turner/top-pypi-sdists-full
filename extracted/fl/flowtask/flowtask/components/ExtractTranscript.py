import asyncio
import tempfile
import logging
import sys
import glob
import gc
from io import StringIO
from typing import List, Optional
from collections.abc import Callable
from pathlib import Path, PurePath
from io import BytesIO
import pandas as pd
from tqdm import tqdm
from parrot.loaders.audio import AudioLoader
from sqlalchemy import create_engine, text, bindparam
from .flow import FlowComponent
from ..interfaces.Boto3Client import Boto3Client
from ..exceptions import ConfigError, ComponentError
from ..conf import default_dsn

# Import torch conditionally for CUDA cleanup
try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False


class ExtractTranscript(Boto3Client, FlowComponent):
    """
    ExtractTranscript Component

    **Overview**

    This component extracts audio transcripts, VTT subtitles, SRT files with speaker diarization,
    and AI-generated summaries from audio files specified in a DataFrame. It uses Parrot's
    AudioLoader which leverages WhisperX for high-quality transcription with word-level timestamps.

    The component processes audio files in batch from a pandas DataFrame and generates multiple
    output formats for each audio file, returning an enhanced DataFrame with paths to all
    generated files.

       :widths: auto

    |   audio_column             | Yes*     | Name of DataFrame column containing audio file paths. Default: `"audio_path"`.              |
    |                            |          | The DataFrame must contain this column with valid paths to audio files.                     |
    |                            |          | *Not required if `use_bytes_input` is `true`.                                               |
    |   use_bytes_input          | No       | Enable BytesIO input mode for in-memory audio data. Default: `false`.                      |
    |                            |          | When `true`, reads audio from BytesIO objects instead of file paths.                        |
    |   bytes_column             | No       | Name of DataFrame column containing BytesIO audio data. Default: `"file_data"`.             |
    |                            |          | Only used when `use_bytes_input` is `true`.                                                 |
    |   filename_column          | No       | Name of DataFrame column containing original filenames. Default: `"downloaded_filename"`.   |
    |                            |          | Only used when `use_bytes_input` is `true`. Used for naming temporary files.               |
    |   language                 | No       | Language code for transcription. Accepts language codes like `"en"`, `"es"`, `"fr"`, etc.   |
    |                            |          | Default: `"en"`. Used to improve transcription accuracy.                                    |
    |   model_size               | No       | Whisper model size for transcription. Accepts `"tiny"`, `"small"`, `"medium"`, `"large"`.   |
    |                            |          | Default: `"small"`. Larger models provide better accuracy but require more resources.       |
    |   diarization              | No       | Enable speaker diarization to identify different speakers in the audio.                     |
    |                            |          | Default: `false`. When enabled, generates SRT files with speaker labels.                    |
    |   summarization            | No       | Enable AI-generated summaries of the transcripts.                                          |
    |                            |          | Default: `true`. Generates summary files using LLM models.                                 |
    |   device                   | No       | Device to use for processing. Accepts `"cpu"`, `"cuda"`, or `"mps"`.                       |
    |                            |          | Default: `"cpu"`. Use `"cuda"` for GPU acceleration (10-20x faster).                       |
    |   skip_errors              | No       | Continue processing if a file fails. Default: `true`.                                      |
    |                            |          | When `false`, the first error stops the entire workflow.                                   |
    |   skip_processed           | No       | Skip rows that are already processed. Default: `true`.                                     |
    |                            |          | Checks `processed_column` for True/1 values and skips reprocessing those rows.             |
    |   processed_column         | No       | Column name to check for processed status. Default: `"transcript_processed"`.              |
    |                            |          | Used with `skip_processed` to determine which rows to skip.                                |
    |   download_from_s3         | No       | Download SRT files from S3 for skipped rows. Default: `true`.                              |
    |                            |          | When skipping processed rows, downloads SRT from S3 for downstream components.             |
    |   s3_srt_key_column        | No       | Column containing S3 keys for SRT files. Default: `"transcript_srt_s3_key"`.               |
    |                            |          | Used with `download_from_s3` to locate SRT files in S3.                                    |

    **Returns**

    This component returns a pandas DataFrame containing the original data plus additional
    columns with transcription results. The structure includes:

    - **Original DataFrame columns**: All columns from the input DataFrame are preserved.
    - **transcript_success**: Boolean indicating if processing succeeded for each file.
    - **transcript_error**: Error message if processing failed (None if successful).
    - **transcript_vtt_path**: Path to generated WebVTT file with timestamps.
    - **transcript_transcript_path**: Path to plain text transcript file.
    - **transcript_srt_path**: Path to SRT subtitle file (if diarization enabled).
    - **transcript_summary_path**: Path to AI-generated summary file.
    - **transcript_summary**: Summary text content.
    - **transcript_language**: Detected or specified language.

    **Example**


    **Example with Skip Processed + S3 Download (Batch Reprocessing)**

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          ExtractTranscript:
          audio_column: audio_path
          language: en
          model_size: small
          diarization: false
          summarization: true
          device: cuda
          cuda_number: 0
          skip_errors: true
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
        """Initialize ExtractTranscript component.

        Args:
            audio_column: Name of DataFrame column containing audio file paths (default: 'audio_path')
            use_bytes_input: Enable BytesIO input mode (default: False)
            bytes_column: Name of DataFrame column containing BytesIO audio data (default: 'file_data')
            filename_column: Name of DataFrame column containing original filenames (default: 'downloaded_filename')
            language: Language code for transcription (default: 'en')
            model_size: Whisper model size: tiny, small, medium, large (default: 'small')
            model_name: Explicit model name (optional, overrides model_size)
            diarization: Enable speaker diarization (default: False)
            summarization: Enable summary generation (default: True)
            device: Device to use: cpu, cuda, mps (default: 'cpu')
            cuda_number: CUDA device number if multiple GPUs (default: 0)
            source_type: Source type for metadata (default: 'AUDIO')
            batch_size: Batch size for processing (default: 1)
            skip_errors: Continue processing if a file fails (default: True)
            skip_processed: Skip rows that are already processed (default: True)
            processed_column: Column name to check for processed status (default: 'transcript_processed')
            download_from_s3: Download SRT files from S3 for skipped rows (default: True)
            s3_srt_key_column: Column containing S3 keys for SRT files (default: 'transcript_srt_s3_key')
        """
        # Input mode configuration
        self.use_bytes_input: bool = kwargs.pop('use_bytes_input', False)
        self.bytes_column: str = kwargs.pop('bytes_column', 'file_data')
        self.filename_column: str = kwargs.pop('filename_column', 'downloaded_filename')

        # Audio processing configuration
        self.audio_column: str = kwargs.pop('audio_column', 'audio_path')
        self.language: str = kwargs.pop('language', 'en')
        self.model_size: str = kwargs.pop('model_size', 'small')
        self.model_name: Optional[str] = kwargs.pop('model_name', None)
        self.diarization: bool = kwargs.pop('diarization', True)
        self.source_type: str = kwargs.pop('source_type', 'AUDIO')
        self.summarization: bool = kwargs.pop('summarization', False)

        # Device configuration
        self._device: str = kwargs.pop('device', 'cpu')
        self._cuda_number: int = kwargs.pop('cuda_number', 0)

        # Processing configuration
        self.batch_size: int = kwargs.pop('batch_size', 1)
        self.skip_errors: bool = kwargs.pop('skip_errors', True)

        # Skip processed configuration
        self.skip_processed: bool = kwargs.pop('skip_processed', True)
        self.processed_column: str = kwargs.pop('processed_column', 'transcript_processed')

        # S3 download configuration (for skipped rows)
        self.download_from_s3: bool = kwargs.pop('download_from_s3', True)
        self.s3_srt_key_column: str = kwargs.pop('s3_srt_key_column', 'transcript_srt_s3_key')

        # S3 upload configuration
        self.save_s3: bool = kwargs.pop('save_s3', False)
        self._s3_config: str = kwargs.pop('s3_config', 'default')
        self.s3_directory: str = kwargs.pop('directory', 'transcripts/')
        self.generate_presigned_url: bool = kwargs.pop('generate_presigned_url', False)
        self.url_expiration: int = kwargs.pop('url_expiration', 3600)

        # Database lookup configuration for already-processed transcripts
        self.lookup_table: str = kwargs.pop('lookup_table', 'calls')
        self.lookup_schema_column: str = kwargs.pop('schema_column', 'program_slug')
        self.lookup_id_column: str = kwargs.pop('id_column', 'call_id')
        self.lookup_dsn: str = kwargs.pop('lookup_dsn', default_dsn)
        self._lookup_engine = None

        # Pass config to Boto3Client if S3 is enabled
        if self.save_s3:
            kwargs['config'] = self._s3_config

        super().__init__(
            loop=loop, job=job, stat=stat, **kwargs
        )

        # AudioLoader instance (initialized in start)
        self._audio_loader: Optional[AudioLoader] = None

    def _release_audio_resources(self) -> None:
        """Release GPU/CPU resources allocated by AudioLoader/WhisperX."""
        try:
            if self._audio_loader and hasattr(self._audio_loader, 'clear_cuda'):
                self._audio_loader.clear_cuda()
        except Exception as exc:  # pragma: no cover - best effort cleanup
            self._logger.debug(f"AudioLoader.clear_cuda failed: {exc}")

        # Free any cached CUDA memory from torch directly as well
        if torch is not None:
            try:
                if torch.cuda.is_available():  # pragma: no cover - depends on environment
                    torch.cuda.empty_cache()
            except Exception as exc:  # pragma: no cover - best effort cleanup
                self._logger.debug(f"torch.cuda.empty_cache failed: {exc}")

        # Trigger Python GC to release CPU memory/file handles that keep GPU tensors alive
        gc.collect()

    async def start(self, **kwargs):
        """Initialize the component and validate configuration."""
        await super().start(**kwargs)

        # Validate that we have input from previous component
        if self.previous is None or self.input is None:
            raise ConfigError(
                "ExtractTranscript requires input from a previous component (e.g., DataFrame)"
            )

        # Validate input is a DataFrame
        if not isinstance(self.input, pd.DataFrame):
            raise ComponentError(
                f"ExtractTranscript expects a DataFrame as input, got {type(self.input)}"
            )

        # Validate columns based on input mode
        if self.use_bytes_input:
            # Validate BytesIO columns exist
            if self.bytes_column not in self.input.columns:
                raise ConfigError(
                    f"Column '{self.bytes_column}' not found in input DataFrame. "
                    f"Available columns: {list(self.input.columns)}"
                )
            if self.filename_column not in self.input.columns:
                raise ConfigError(
                    f"Column '{self.filename_column}' not found in input DataFrame. "
                    f"Available columns: {list(self.input.columns)}"
                )
        else:
            # Validate audio_column exists in DataFrame
            if self.audio_column not in self.input.columns:
                raise ConfigError(
                    f"Column '{self.audio_column}' not found in input DataFrame. "
                    f"Available columns: {list(self.input.columns)}"
                )

        # Initialize AudioLoader with configuration
        # Only pass model_name when explicitly set; when None the downstream
        # defaults apply correctly (e.g. 'gpt-4' for tiktoken in SemanticTextSplitter).
        loader_kwargs = dict(
            source=None,  # We'll pass source per file
            language=self.language,
            source_type=self.source_type,
            diarization=self.diarization,
            model_size=self.model_size,
            device=self._device,
            cuda_number=self._cuda_number,
            summarization=self.summarization,
            video_path=None,  # Not needed for audio-only processing
        )
        if self.model_name is not None:
            loader_kwargs['model_name'] = self.model_name
        self._audio_loader = AudioLoader(**loader_kwargs)

        # Initialize S3 connection if save_s3 is enabled
        if self.save_s3:
            # Process credentials (similar to UploadToS3)
            self.processing_credentials()

            # Ensure directory has trailing slash
            if self.s3_directory and not self.s3_directory.endswith("/"):
                self.s3_directory += "/"

            # Open S3 connection
            await self.open()

    async def close(self):
        """Clean up resources."""
        self._release_audio_resources()
        await super().close()

    async def _generate_presigned_url(self, s3_key: str) -> str:
        """Generate a presigned URL for the S3 object."""
        try:
            url = self._connection.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket, 'Key': s3_key},
                ExpiresIn=self.url_expiration
            )
            return url
        except Exception as e:
            self._logger.error(f"Error generating presigned URL for {s3_key}: {e}")
            return None

    async def _upload_to_s3(self, metadata: dict, base_filename: str) -> dict:
        """
        Upload all files (audio + transcripts) to S3 and generate presigned URLs.

        Args:
            metadata: Dict containing BytesIO objects and file info
            base_filename: Base filename for S3 keys (e.g., "recording.mp3")

        Returns:
            Dict with S3 keys and URLs for each file type
        """
        s3_info = {}

        # Determine base name without extension for transcript files
        base_name = Path(base_filename).stem

        # Determine audio content type based on file extension
        audio_ext = Path(base_filename).suffix.lower()
        audio_content_type = 'audio/wav' if audio_ext == '.wav' else 'audio/mpeg'

        # Files to upload: (metadata_key, s3_suffix, content_type)
        files_to_upload = [
            ('audio_bytesio', base_filename, audio_content_type),
            ('transcript_bytesio', f'{base_name}.txt', 'text/plain'),
            ('vtt_bytesio', f'{base_name}.vtt', 'text/vtt'),
            ('summary_bytesio', f'{base_name}.summary', 'text/plain'),
            ('srt_bytesio', f'{base_name}.srt', 'application/x-subrip'),
        ]

        for bytesio_key, s3_filename, content_type in files_to_upload:
            if bytesio_key in metadata and metadata[bytesio_key]:
                file_data = metadata[bytesio_key]
                s3_key = f"{self.s3_directory}{s3_filename}"

                try:
                    # Upload to S3
                    file_data.seek(0)
                    content = file_data.read()

                    response = self._connection.put_object(
                        Bucket=self.bucket,
                        Key=s3_key,
                        Body=content,
                        ContentType=content_type,
                    )

                    status_code = response["ResponseMetadata"]["HTTPStatusCode"]

                    if status_code == 200:
                        # Determine the type from bytesio_key (e.g., 'audio_bytesio' -> 'audio')
                        file_type = bytesio_key.replace('_bytesio', '')

                        # Store S3 key
                        s3_info[f'{file_type}_s3_key'] = s3_key

                        # Generate presigned URL if enabled
                        if self.generate_presigned_url:
                            presigned_url = await self._generate_presigned_url(s3_key)
                            if presigned_url:
                                s3_info[f'{file_type}_s3_url'] = presigned_url
                    else:
                        self._logger.error(f"Failed to upload {s3_filename} to S3: {response}")

                except Exception as e:
                    self._logger.error(f"Error uploading {s3_filename} to S3: {e}")

        return s3_info

    async def _download_from_s3(self, s3_filename: str) -> BytesIO:
        """
        Download a file from S3 and return as BytesIO.

        Args:
            s3_filename: S3 filename (not full key, just the filename)

        Returns:
            BytesIO object with the file content, or None if failed
        """
        try:
            # Construct full S3 key: directory + filename
            s3_key = self.s3_directory + s3_filename if self.s3_directory else s3_filename

            # Download from S3
            response = self._connection.get_object(
                Bucket=self.bucket,
                Key=s3_key
            )

            # Read content and create BytesIO
            content = response['Body'].read()
            file_bytesio = BytesIO(content)
            file_bytesio.seek(0)

            self._logger.debug(f"✓ Downloaded from S3: {s3_key}")
            return file_bytesio

        except Exception as e:
            self._logger.error(f"Error downloading {s3_key} from S3 (bucket: {self.bucket}, directory: {self.s3_directory}, filename: {s3_filename}): {e}")
            return None

    def _extract_existing_metadata(self, row: pd.Series, idx: int) -> dict:
        """
        Extract existing metadata from a row that was already processed.

        Args:
            row: DataFrame row with existing transcript data
            idx: Row index

        Returns:
            Dictionary with existing metadata
        """
        # Map of column names to metadata keys
        column_mapping = {
            'transcript_success': 'success',
            'transcript_processed': 'processed',
            'transcript_error': 'error',
            'transcript_source': 'source',
            'transcript_vtt_path': 'vtt_path',
            'transcript_transcript_path': 'transcript_path',
            'transcript_srt_path': 'srt_path',
            'transcript_summary_path': 'summary_path',
            'transcript_summary': 'summary',
            'transcript_language': 'language',
            # BytesIO columns (if they exist)
            'transcript_audio_bytesio': 'audio_bytesio',
            'transcript_transcript_bytesio': 'transcript_bytesio',
            'transcript_vtt_bytesio': 'vtt_bytesio',
            'transcript_summary_bytesio': 'summary_bytesio',
            'transcript_srt_bytesio': 'srt_bytesio',
            # S3 columns (if they exist)
            'transcript_audio_s3_key': 'audio_s3_key',
            'transcript_transcript_s3_key': 'transcript_s3_key',
            'transcript_vtt_s3_key': 'vtt_s3_key',
            'transcript_summary_s3_key': 'summary_s3_key',
            'transcript_srt_s3_key': 'srt_s3_key',
            'transcript_audio_s3_url': 'audio_s3_url',
            'transcript_transcript_s3_url': 'transcript_s3_url',
            'transcript_vtt_s3_url': 'vtt_s3_url',
            'transcript_summary_s3_url': 'summary_s3_url',
            'transcript_srt_s3_url': 'srt_s3_url',
        }

        metadata = {}
        for col_name, meta_key in column_mapping.items():
            if col_name in row.index:
                value = row[col_name]
                # Only include if not NaN
                if not pd.isna(value):
                    metadata[meta_key] = value

        # If no metadata was extracted, create minimal structure
        if not metadata:
            filename = row.get(self.filename_column, f"audio_{idx}") if self.use_bytes_input else row.get(self.audio_column)
            metadata = {
                'success': True,
                'processed': True,
                'source': filename,
            }
        else:
            # IMPORTANT: Ensure 'success' field is always set for processed rows
            # If the row was marked as processed but doesn't have 'success' field,
            # default it to True (since it was successfully processed before)
            if 'success' not in metadata:
                metadata['success'] = True

            # Also ensure 'error' field exists (None means no error)
            if 'error' not in metadata:
                metadata['error'] = None

        return metadata

    async def _process_audio_file(
        self,
        audio_input,
        row_idx: int,
        filename: str = None,
        is_bytes: bool = False
    ) -> dict:
        """Process a single audio file and extract transcripts.

        Args:
            audio_input: Either a file path (str) or BytesIO object
            row_idx: Row index for logging
            filename: Original filename (used when is_bytes=True)
            is_bytes: Whether audio_input is a BytesIO object

        Returns:
            Dictionary with extracted metadata and file paths
        """
        temp_file = None
        files_to_delete = []  # Track all temporary files for cleanup
        try:
            if is_bytes:
                # Handle BytesIO input - create temporary file
                if not isinstance(audio_input, BytesIO):
                    raise ComponentError(f"Expected BytesIO object, got {type(audio_input)}")

                # Determine file extension from filename
                file_ext = Path(filename).suffix if filename else '.wav'
                if not file_ext:
                    file_ext = '.wav'

                # Create temporary file with appropriate extension
                temp_file = tempfile.NamedTemporaryFile(
                    mode='wb',
                    suffix=file_ext,
                    delete=False,
                    prefix='extract_transcript_'
                )

                # Write BytesIO content to temporary file
                audio_input.seek(0)  # Ensure we're at the beginning
                temp_file.write(audio_input.read())
                temp_file.flush()
                temp_file.close()

                # Use the temporary file path
                path = Path(temp_file.name)
                display_name = filename or path.name

            else:
                # Handle file path input (original behavior)
                path = Path(audio_input).resolve()

                if not path.exists():
                    raise FileNotFoundError(f"Audio file not found: {path}")

                display_name = path.name

            # Extract audio using Parrot's AudioLoader (suppress verbose output)
            # Redirect stdout/stderr to suppress print() statements from Parrot
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            sys.stdout = StringIO()
            sys.stderr = StringIO()

            try:
                metadata = await self._audio_loader.extract_audio(path)
            finally:
                # Restore stdout/stderr
                sys.stdout = old_stdout
                sys.stderr = old_stderr

            # Add success flag
            metadata['success'] = True
            metadata['processed'] = True  # Mark as successfully processed
            metadata['error'] = None

            # If BytesIO mode, read generated files and convert to BytesIO
            if is_bytes:
                # Get the base name (without extension) of the temp file
                temp_base = path.stem  # e.g., "extract_transcript_e8sjit72"
                temp_dir = path.parent  # e.g., "/tmp"

                # Find ALL files with the same base name using glob
                # This captures all files generated by AudioLoader, including intermediates
                pattern = str(temp_dir / f"{temp_base}.*")
                all_generated_files = glob.glob(pattern)

                # Find and read the .wav file generated by AudioLoader
                wav_file = None
                for file_str in all_generated_files:
                    if file_str.endswith('.wav'):
                        wav_file = Path(file_str)
                        break

                # Use .wav file if found, otherwise use original audio
                if wav_file and wav_file.exists():
                    try:
                        # Read wav file and convert to BytesIO
                        with open(wav_file, 'rb') as f:
                            wav_content = f.read()

                        wav_bytesio = BytesIO(wav_content)
                        wav_bytesio.seek(0)
                        metadata['audio_bytesio'] = wav_bytesio

                        # Update filename to .wav extension
                        base_name = Path(filename).stem
                        metadata['original_filename'] = f"{base_name}.wav"
                    except Exception as e:
                        self._logger.warning(f"Failed to read wav file {wav_file}, using original: {e}")
                        audio_input.seek(0)
                        metadata['audio_bytesio'] = audio_input
                        metadata['original_filename'] = filename
                else:
                    # Fallback to original audio if no wav found
                    audio_input.seek(0)
                    metadata['audio_bytesio'] = audio_input
                    metadata['original_filename'] = filename

                # Read generated files and create BytesIO objects
                files_to_read = {
                    'transcript_path': 'transcript_bytesio',
                    'vtt_path': 'vtt_bytesio',
                    'summary_path': 'summary_bytesio',
                    'srt_path': 'srt_bytesio',
                }

                for path_key, bytesio_key in files_to_read.items():
                    if path_key in metadata and metadata[path_key]:
                        file_path = Path(metadata[path_key])

                        # Try to read and convert to BytesIO
                        if file_path.exists():
                            try:
                                # Read file content
                                with open(file_path, 'rb') as f:
                                    content = f.read()

                                # Create BytesIO object
                                file_bytesio = BytesIO(content)
                                file_bytesio.seek(0)
                                metadata[bytesio_key] = file_bytesio
                            except Exception as e:
                                self._logger.warning(f"Failed to read {file_path}: {e}")
                                metadata[bytesio_key] = None
                        else:
                            metadata[bytesio_key] = None
                    else:
                        metadata[bytesio_key] = None

                # Mark ALL generated files for deletion (including intermediates like .wav)
                for file_str in all_generated_files:
                    file_path = Path(file_str)
                    if file_path.exists() and file_path not in files_to_delete:
                        files_to_delete.append(file_path)

            else:
                # File path mode - log completion (only if not using tqdm to avoid conflicts)
                self._logger.debug(f"✓ Completed: {path.name}")
                if 'transcript_path' in metadata:
                    self._logger.debug(f"  - Transcript: {metadata['transcript_path']}")
                if 'vtt_path' in metadata:
                    self._logger.debug(f"  - VTT: {metadata['vtt_path']}")
                if metadata.get('summary'):
                    self._logger.debug("  - Summary generated")

            return metadata

        except Exception as e:
            source_name = filename if is_bytes else audio_input
            error_msg = f"Error processing {source_name}: {str(e)}"

            # Log the error with more context
            self._logger.error(f"Failed to process audio file: {source_name}")
            self._logger.error(f"Error details: {type(e).__name__}: {str(e)}")

            # Log traceback for better debugging
            import traceback
            self._logger.debug(f"Traceback:\n{traceback.format_exc()}")

            if self.skip_errors:
                # Return error metadata
                error_result = {
                    'success': False,
                    'processed': False,  # Mark as unprocessed
                    'error': str(e),
                    'error_type': type(e).__name__,
                    'source': source_name,
                    'vtt_path': None,
                    'transcript_path': None,
                    'srt_path': None,
                    'summary_path': None,
                    'summary': None,
                    'language': None,
                }

                # If BytesIO mode, preserve the original audio for S3 upload
                # This ensures the frontend can still access the audio even if processing failed
                if is_bytes and audio_input:
                    try:
                        audio_input.seek(0)
                        error_result['audio_bytesio'] = audio_input
                        error_result['original_filename'] = filename
                        self._logger.info(f"✓ Preserved original audio for S3 upload: {filename}")
                    except Exception as preserve_error:
                        self._logger.warning(f"Failed to preserve original audio: {preserve_error}")

                return error_result
            else:
                raise ComponentError(error_msg) from e

        finally:
            # Clean up ALL temporary files (silently to avoid breaking tqdm)
            cleanup_errors = []

            # Delete all files marked for deletion
            if is_bytes and files_to_delete:
                for file_path in files_to_delete:
                    try:
                        if file_path.exists():
                            file_path.unlink()
                    except Exception as e:
                        cleanup_errors.append(f"{file_path.name}: {e}")

            # Log cleanup errors only if any occurred (to avoid breaking tqdm)
            if cleanup_errors:
                self._logger.warning(
                    f"Failed to delete {len(cleanup_errors)} temporary file(s): {', '.join(cleanup_errors)}"
                )

            # Ensure GPU memory is returned to the pool between files
            self._release_audio_resources()

    async def run(self):
        """Process all audio files in the DataFrame."""
        df = self.input.copy()

        # Initialize all expected output columns to ensure they exist
        # This prevents issues when some rows fail or are skipped
        expected_columns = [
            'transcript_success',
            'transcript_processed',
            'transcript_error',
            'transcript_source',
            'transcript_vtt_path',
            'transcript_transcript_path',
            'transcript_srt_path',
            'transcript_summary_path',
            'transcript_summary',
            'transcript_language',
            'transcript_audio_bytesio',
            'transcript_transcript_bytesio',
            'transcript_vtt_bytesio',
            'transcript_summary_bytesio',
            'transcript_srt_bytesio',
            'transcript_audio_s3_key',
            'transcript_transcript_s3_key',
            'transcript_vtt_s3_key',
            'transcript_summary_s3_key',
            'transcript_srt_s3_key',
        ]

        # Add S3 URL columns if presigned URLs are enabled
        if self.save_s3 and self.generate_presigned_url:
            expected_columns.extend([
                'transcript_audio_s3_url',
                'transcript_transcript_s3_url',
                'transcript_vtt_s3_url',
                'transcript_summary_s3_url',
                'transcript_srt_s3_url',
            ])

        # Ensure all columns exist
        for column in expected_columns:
            self._column_exists(df, column)

        # Attempt DB lookup to mark already-processed rows and fetch keys
        df = await self._apply_db_lookup(df)

        # Log skip configuration
        if self.skip_processed and self.processed_column in df.columns:
            already_processed_count = df[self.processed_column].sum() if self.processed_column in df.columns else 0
            if already_processed_count > 0:
                self._logger.info(
                    f"Skip mode enabled: Found {already_processed_count} already processed files. "
                    f"Will skip reprocessing."
                )

        # Suppress verbose logging from external libraries to keep tqdm clean
        logging.getLogger('parrot').setLevel(logging.ERROR)
        logging.getLogger('whisperx').setLevel(logging.ERROR)
        logging.getLogger('pyannote').setLevel(logging.ERROR)
        logging.getLogger('pytorch_lightning').setLevel(logging.ERROR)
        logging.getLogger('pytorch_lightning.utilities').setLevel(logging.ERROR)
        logging.getLogger('pytorch_lightning.utilities.migration').setLevel(logging.ERROR)
        logging.getLogger('fsspec').setLevel(logging.ERROR)
        logging.getLogger('speechbrain').setLevel(logging.ERROR)
        logging.getLogger('speechbrain.utils').setLevel(logging.ERROR)
        logging.getLogger('torio').setLevel(logging.ERROR)
        logging.getLogger('torio._extension').setLevel(logging.ERROR)

        # Process each audio file with progress bar
        results = []
        skipped_count = 0

        with tqdm(total=len(df), desc="🎙️ Transcribing audio", unit="files", colour="cyan") as pbar:
            for idx, row in df.iterrows():
                # Check if already processed (skip logic)
                if self.skip_processed and self.processed_column in df.columns:
                    is_processed = row.get(self.processed_column, False)
                    # Check if processed is True or 1 (could be bool or int)
                    # Handle NA/NaN values by treating them as False (not processed)
                    if not pd.isna(is_processed) and (is_processed is True or is_processed == 1 or (isinstance(is_processed, str) and is_processed.lower() == 'true')):
                        # Skip this row - preserve existing data
                        skipped_count += 1

                        # Create metadata from existing row data to preserve it
                        existing_metadata = self._extract_existing_metadata(row, idx)

                        # Download SRT from S3 if needed and enabled
                        if self.download_from_s3 and self.s3_srt_key_column in df.columns:
                            s3_key = row.get(self.s3_srt_key_column)
                            if pd.notna(s3_key) and s3_key:
                                # Download SRT from S3
                                srt_bytesio = await self._download_from_s3(s3_key)
                                if srt_bytesio:
                                    # Add to metadata so it's available for CallAnalysis
                                    existing_metadata['srt_bytesio'] = srt_bytesio
                                    self._logger.debug(f"Downloaded SRT for skipped row {idx}: {s3_key}")

                        results.append(existing_metadata)

                        # IMPORTANT: Update DataFrame with preserved data
                        # This ensures downstream components (like CallAnalysis) can access
                        # transcript_srt_bytesio and other fields even for skipped rows
                        self._update_dataframe_row(df, idx, existing_metadata)

                        pbar.update(1)
                        continue

                if self.use_bytes_input:
                    # Process BytesIO input
                    audio_data = row[self.bytes_column]
                    filename = row.get(self.filename_column, f"audio_{idx}")

                    # Skip if data is None or empty
                    if pd.isna(audio_data) or audio_data is None:
                        empty_metadata = {
                            'success': False,
                            'error': 'No audio data provided',
                            'source': filename,
                            'vtt_path': None,
                            'transcript_path': None,
                            'srt_path': None,
                            'summary_path': None,
                            'summary': None,
                            'language': None,
                        }
                        results.append(empty_metadata)
                        self._update_dataframe_row(df, idx, empty_metadata)
                        pbar.update(1)
                        continue

                    # Process the audio from BytesIO
                    result = await self._process_audio_file(
                        audio_data,
                        idx,
                        filename=filename,
                        is_bytes=True
                    )

                    # Upload to S3 if enabled and audio_bytesio exists
                    # This uploads both successfully processed files (wav) and failed files (original mp3)
                    if self.save_s3 and result.get('audio_bytesio'):
                        # Use the updated filename (now .wav instead of .mp3)
                        upload_filename = result.get('original_filename', filename)

                        # Log upload type for debugging
                        if result.get('processed'):
                            self._logger.debug(f"Uploading processed audio (wav): {upload_filename}")
                        else:
                            self._logger.info(f"Uploading unprocessed audio (original): {upload_filename}")

                        s3_info = await self._upload_to_s3(result, upload_filename)
                        # Merge S3 info into result
                        result.update(s3_info)

                    results.append(result)
                    self._update_dataframe_row(df, idx, result)

                else:
                    # Process file path input (original behavior)
                    audio_path = row[self.audio_column]

                    # Skip if path is None or empty
                    if pd.isna(audio_path) or not audio_path:
                        empty_metadata = {
                            'success': False,
                            'error': 'No audio path provided',
                            'source': None,
                            'vtt_path': None,
                            'transcript_path': None,
                            'srt_path': None,
                            'summary_path': None,
                            'summary': None,
                            'language': None,
                        }
                        results.append(empty_metadata)
                        self._update_dataframe_row(df, idx, empty_metadata)
                        pbar.update(1)
                        continue

                    # Process the audio file
                    result = await self._process_audio_file(
                        audio_path,
                        idx,
                        is_bytes=False
                    )
                    results.append(result)
                    self._update_dataframe_row(df, idx, result)

                # Periodic VRAM cleanup every 5 files to prevent memory accumulation
                if (idx + 1) % 5 == 0:
                    gc.collect()
                    if TORCH_AVAILABLE and self._device == 'cuda':
                        torch.cuda.empty_cache()
                        self._logger.debug(f"🧹 VRAM cleanup after processing {idx + 1} files")

                pbar.update(1)

        # Calculate metrics
        success_count = sum(1 for r in results if r.get('success', False))
        error_count = len(results) - success_count
        newly_processed_count = success_count - skipped_count

        # Collect error details
        failed_files = [r for r in results if not r.get('success', False)]

        self.add_metric('TOTAL_FILES', len(results))
        self.add_metric('SUCCESS_COUNT', success_count)
        self.add_metric('ERROR_COUNT', error_count)
        if skipped_count > 0:
            self.add_metric('SKIPPED_COUNT', skipped_count)
            self.add_metric('NEWLY_PROCESSED_COUNT', newly_processed_count)

        # Calculate S3 upload metrics if enabled
        if self.save_s3:
            s3_uploaded_count = sum(1 for r in results if r.get('audio_s3_key'))
            s3_processed_count = sum(1 for r in results if r.get('audio_s3_key') and r.get('processed'))
            s3_unprocessed_count = sum(1 for r in results if r.get('audio_s3_key') and not r.get('processed'))

            self.add_metric('S3_UPLOADED_COUNT', s3_uploaded_count)
            self.add_metric('S3_PROCESSED_COUNT', s3_processed_count)
            self.add_metric('S3_UNPROCESSED_COUNT', s3_unprocessed_count)
            if self.generate_presigned_url:
                self.add_metric('S3_PRESIGNED_URLS', True)

        print(f"\n{'='*60}")
        print("Extraction complete:")
        print(f"  - Total files: {len(results)}")
        if skipped_count > 0:
            print(f"  - Skipped (already processed): {skipped_count}")
            print(f"  - Newly processed: {newly_processed_count}")
            print(f"  - Errors: {error_count}")
        else:
            print(f"  - Successful: {success_count}")
            print(f"  - Errors: {error_count}")
        if self.save_s3:
            s3_uploaded_count = sum(1 for r in results if r.get('audio_s3_key'))
            s3_processed_count = sum(1 for r in results if r.get('audio_s3_key') and r.get('processed'))
            s3_unprocessed_count = sum(1 for r in results if r.get('audio_s3_key') and not r.get('processed'))

            print(f"  - Uploaded to S3: {s3_uploaded_count}")
            if s3_processed_count > 0:
                print(f"    • Processed (wav): {s3_processed_count}")
            if s3_unprocessed_count > 0:
                print(f"    • Unprocessed (original): {s3_unprocessed_count}")
            if self.generate_presigned_url:
                print(f"  - Presigned URLs generated: Yes")
        print(f"{'='*60}")

        # Display detailed error information if any errors occurred
        if error_count > 0:
            print(f"\n{'='*60}")
            print(f"⚠️  ERROR DETAILS ({error_count} failed):")
            print(f"{'='*60}")
            for idx, result in enumerate(failed_files, 1):
                source = result.get('source', 'Unknown')
                error = result.get('error', 'Unknown error')
                error_type = result.get('error_type', 'Exception')
                print(f"\n{idx}. {source}")
                print(f"   Type: {error_type}")
                print(f"   Message: {error}")
            print(f"{'='*60}\n")
        else:
            print()  # Extra newline for clean output

        # Set result as the enhanced DataFrame
        self._result = df

        return True

    def _update_dataframe_row(self, df: pd.DataFrame, row_idx: int, metadata: dict) -> None:
        """Persist AudioLoader metadata into the original DataFrame."""
        prefix = 'transcript_'

        def _normalize(value):
            """Convert metadata values into DataFrame-friendly objects."""
            if isinstance(value, pd.Series):
                return value.to_dict()
            if isinstance(value, pd.DataFrame):
                return value.to_dict(orient='list')
            if isinstance(value, (Path, PurePath)):
                return str(value)
            return value

        for key, value in metadata.items():
            column_name = f"{prefix}{key}"

            if column_name not in df.columns:
                # Create column with object dtype to allow any Python object (including BytesIO)
                df[column_name] = pd.Series(dtype='object')
            else:
                # If column exists but has wrong dtype (e.g., from AddDataset), convert to object
                # This allows storing BytesIO objects even if the column came from DB with string dtype
                if df[column_name].dtype != 'object':
                    df[column_name] = df[column_name].astype('object')

            df.at[row_idx, column_name] = _normalize(value)

    def _column_exists(self, df: pd.DataFrame, column: str) -> bool:
        """
        Ensure a column exists in the DataFrame. Creates it with None values if missing.

        Args:
            df: DataFrame to check
            column: Column name to verify/create

        Returns:
            True if column already existed, False if it was created
        """
        if column not in df.columns:
            self._logger.debug(
                f"Column {column} does not exist in dataframe, creating it"
            )
            df[column] = pd.Series(dtype='object')
            return False
        return True

    def _safe_identifier(self, name: str) -> str | None:
        """Return a safe identifier or None if invalid."""
        if not isinstance(name, str):
            return None
        if name.replace('_', '').replace('-', '').isalnum():
            return name
        return None

    def _get_lookup_engine(self):
        """Create or return cached SQLAlchemy engine for lookups."""
        if self._lookup_engine is None:
            try:
                dsn = self.lookup_dsn
                if isinstance(dsn, Path):
                    dsn = str(dsn)
                if isinstance(dsn, str) and dsn.startswith('postgres:'):
                    dsn = dsn.replace('postgres:', 'postgresql:')
                self._lookup_engine = create_engine(dsn, echo=False)
            except Exception as err:
                self._logger.error(f"Error creating lookup engine: {err}")
                return None
        return self._lookup_engine

    async def _apply_db_lookup(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        If skip_processed is enabled, enrich DataFrame with processed info from DB
        to avoid reprocessing transcripts stored in other tables/schemas.
        """
        if not self.skip_processed:
            return df
        if df.empty:
            return df

        schema_col_present = (
            self.lookup_schema_column
            and isinstance(self.lookup_schema_column, str)
            and self.lookup_schema_column in df.columns
        )

        table_name = self._safe_identifier(self.lookup_table)
        id_column = self.lookup_id_column or 'call_id'
        id_col_safe = self._safe_identifier(id_column)
        if not table_name or not id_col_safe:
            return df

        engine = self._get_lookup_engine()
        if engine is None:
            return df

        groups = [(None, df)] if not schema_col_present else df.groupby(self.lookup_schema_column)

        for schema_value, group_df in groups:
            schema_safe = self._safe_identifier(str(schema_value)) if schema_value is not None else None
            if schema_col_present and not schema_safe:
                continue

            call_ids = [
                x for x in group_df[id_column].dropna().unique().tolist()
                if str(x).strip() != ''
            ]
            if not call_ids:
                continue

            try:
                if schema_safe:
                    stmt = text(
                        f'SELECT "{id_col_safe}" AS call_id, '
                        f'"{self.processed_column}" AS processed, '
                        f'"{self.s3_srt_key_column}" AS srt_key, '
                        f'"transcript_vtt_s3_key" AS vtt_key, '
                        f'"transcript_audio_s3_key" AS audio_key '
                        f'FROM "{schema_safe}"."{table_name}" '
                        f'WHERE "{id_col_safe}" IN :ids'
                    )
                else:
                    stmt = text(
                        f'SELECT "{id_col_safe}" AS call_id, '
                        f'"{self.processed_column}" AS processed, '
                        f'"{self.s3_srt_key_column}" AS srt_key, '
                        f'"transcript_vtt_s3_key" AS vtt_key, '
                        f'"transcript_audio_s3_key" AS audio_key '
                        f'FROM "{table_name}" '
                        f'WHERE "{id_col_safe}" IN :ids'
                    )
                stmt = stmt.bindparams(bindparam("ids", expanding=True))
                with engine.connect() as conn:
                    rows = conn.execute(stmt, {"ids": call_ids}).fetchall()
                if not rows:
                    continue
                for row in rows:
                    call_id_val = row.call_id
                    mask = df[id_column] == call_id_val
                    if schema_col_present:
                        mask &= df[self.lookup_schema_column] == schema_value
                    df.loc[mask, self.processed_column] = row.processed
                    if row.srt_key:
                        df.loc[mask, self.s3_srt_key_column] = row.srt_key
                    if row.vtt_key and 'transcript_vtt_s3_key' in df.columns:
                        df.loc[mask, 'transcript_vtt_s3_key'] = row.vtt_key
                    if row.audio_key and 'transcript_audio_s3_key' in df.columns:
                        df.loc[mask, 'transcript_audio_s3_key'] = row.audio_key
                self._logger.info(
                    f"DB lookup: marked {len(rows)} existing transcripts "
                    f"from {'schema '+schema_safe if schema_safe else 'default schema'}"
                )
            except Exception as err:
                self._logger.error(f"Error fetching existing transcripts from DB: {err}")
                continue

        return df
