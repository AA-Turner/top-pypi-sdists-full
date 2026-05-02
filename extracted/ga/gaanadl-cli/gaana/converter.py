"""
Audio Converter.
Converts audio files to FLAC using FFmpeg.
"""

import json
import os
import subprocess
import shutil
from typing import Optional

from .errors import ConversionError
from .printer import info, warning, error as print_error


class AudioConverter:
    """Converts audio files to various formats using FFmpeg."""
    
    # Supported output formats with their codecs and quality settings
    FORMATS = {
        "flac": {"codec": "flac", "ext": "flac", "desc": "Lossless FLAC"},
        "alac": {"codec": "alac", "ext": "m4a", "desc": "Apple Lossless"},
        "wav": {"codec": "pcm_s24le", "ext": "wav", "desc": "Uncompressed WAV"},
        "aiff": {"codec": "pcm_s24be", "ext": "aiff", "desc": "Apple AIFF"},
        "mp3": {"codec": "libmp3lame", "ext": "mp3", "desc": "MP3 320kbps"},
        "aac": {"codec": "aac", "ext": "m4a", "desc": "AAC (best for Apple)"},
        "m4a": {"codec": "aac", "ext": "m4a", "desc": "AAC in M4A container"},
        "opus": {"codec": "libopus", "ext": "opus", "desc": "Opus (modern, efficient)"},
        "ogg": {"codec": "libvorbis", "ext": "ogg", "desc": "Ogg Vorbis"},
        "vorbis": {"codec": "libvorbis", "ext": "ogg", "desc": "Vorbis in OGG"},
        "wma": {"codec": "wmav2", "ext": "wma", "desc": "Windows Media Audio"},
    }
    
    SUPPORTED_OUTPUTS = list(FORMATS.keys())
    
    def __init__(self, output_format: str = "flac"):
        """
        Initialize converter.
        
        Args:
            output_format: Target output format (default: flac)
        """
        self.output_format = output_format.lower()
        self._verify_ffmpeg()
    
    def _verify_ffmpeg(self):
        """Check if FFmpeg is available."""
        if not shutil.which("ffmpeg"):
            raise ConversionError(
                "FFmpeg not found. Please install FFmpeg and add it to PATH.\n"
                "Download from: https://ffmpeg.org/download.html"
            )
    
    @staticmethod
    def get_audio_info(input_path: str) -> dict:
        """
        Get audio file information using ffprobe.
        
        Args:
            input_path: Path to audio file
        
        Returns:
            Dict with codec, sample_rate, bit_rate, duration, channels
        """
        try:
            cmd = [
                "ffprobe",
                "-v", "error",
                "-select_streams", "a:0",
                "-show_entries", "stream=codec_name,sample_rate,bit_rate,duration,channels",
                "-show_entries", "format=duration,bit_rate",
                "-of", "json",
                input_path,
            ]
            result = subprocess.run(cmd, capture_output=True, check=True)
            info = json.loads(result.stdout)
            
            stream = info.get("streams", [{}])[0]
            fmt = info.get("format", {})
            
            return {
                "codec": stream.get("codec_name", "unknown"),
                "sample_rate": int(stream.get("sample_rate", 0)),
                "bit_rate": int(stream.get("bit_rate", 0) or fmt.get("bit_rate", 0)),
                "duration": float(stream.get("duration", 0) or fmt.get("duration", 0)),
                "channels": int(stream.get("channels", 2)),
            }
        except (subprocess.CalledProcessError, json.JSONDecodeError, KeyError) as e:
            warning(f"Could not get audio info: {e}")
            return {}
    
    def convert_to_flac(
        self,
        input_path: str,
        output_path: str,
        compression_level: int = 8,
    ) -> str:
        """
        Convert audio to FLAC format.
        
        Args:
            input_path: Input audio file path
            output_path: Output FLAC file path (without extension)
            compression_level: FLAC compression (0-12, higher = smaller file)
        
        Returns:
            Path to converted FLAC file
        """
        if not os.path.isfile(input_path):
            raise ConversionError(f"Input file not found: {input_path}")
        
        output_file = f"{output_path}.flac"
        
        # FFmpeg command for highest quality FLAC
        # -c:a flac : Use FLAC codec
        # -compression_level 8 : Good balance of compression/speed
        # -sample_fmt s32 : 32-bit samples (preserves source precision)
        # -ar : Keep original sample rate (no resampling)
        cmd = [
            "ffmpeg",
            "-y",                           # Overwrite output
            "-threads", "0",                # Use all CPU cores
            "-i", input_path,               # Input file
            "-vn",                          # No video
            "-c:a", "flac",                 # FLAC codec
            "-compression_level", str(compression_level),
            output_file,
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                check=True,
            )
            return output_file
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.decode(errors="ignore") if e.stderr else str(e)
            raise ConversionError(f"FLAC conversion failed: {error_msg}")
    
    def convert_to_mp3(
        self,
        input_path: str,
        output_path: str,
        bitrate: str = "320k",
    ) -> str:
        """
        Convert audio to MP3 format.
        
        Args:
            input_path: Input audio file path
            output_path: Output file path (without extension)
            bitrate: MP3 bitrate (e.g., "320k", "256k", "192k")
        
        Returns:
            Path to converted MP3 file
        """
        if not os.path.isfile(input_path):
            raise ConversionError(f"Input file not found: {input_path}")
        
        output_file = f"{output_path}.mp3"
        
        cmd = [
            "ffmpeg",
            "-y",
            "-threads", "0",                # Use all CPU cores
            "-i", input_path,
            "-vn",
            "-c:a", "libmp3lame",
            "-b:a", bitrate,
            "-q:a", "0",                    # Highest quality VBR
            output_file,
        ]
        
        try:
            subprocess.run(cmd, capture_output=True, check=True)
            return output_file
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.decode(errors="ignore") if e.stderr else str(e)
            raise ConversionError(f"MP3 conversion failed: {error_msg}")
    
    def convert(
        self,
        input_path: str,
        output_path: str,
        output_format: Optional[str] = None,
    ) -> str:
        """
        Convert audio to specified format.
        
        Args:
            input_path: Input audio file path
            output_path: Output file path (without extension)
            output_format: Target format (default: self.output_format)
        
        Returns:
            Path to converted file
        """
        fmt = (output_format or self.output_format).lower()
        
        if fmt not in self.FORMATS:
            raise ConversionError(f"Unsupported format: {fmt}. Supported: {', '.join(self.SUPPORTED_OUTPUTS)}")
        
        format_info = self.FORMATS[fmt]
        codec = format_info["codec"]
        ext = format_info["ext"]
        
        # Special handling for high-quality formats
        if fmt == "flac":
            return self.convert_to_flac(input_path, output_path)
        elif fmt == "mp3":
            return self.convert_to_mp3(input_path, output_path)
        elif fmt == "opus":
            return self._convert_with_bitrate(input_path, output_path, ext, codec, "128k")
        elif fmt in ["ogg", "vorbis"]:
            return self._convert_with_quality(input_path, output_path, "ogg", codec, "10")  # Highest VBR
        elif fmt in ["aac", "m4a"]:
            return self._convert_with_bitrate(input_path, output_path, "m4a", codec, "256k")
        elif fmt == "alac":
            return self._convert_generic(input_path, output_path, "m4a", codec)
        elif fmt == "wma":
            return self._convert_with_bitrate(input_path, output_path, ext, codec, "256k")
        else:
            return self._convert_generic(input_path, output_path, ext, codec)
    
    def _convert_generic(
        self,
        input_path: str,
        output_path: str,
        extension: str,
        codec: str,
    ) -> str:
        """Generic conversion using specified codec."""
        if not os.path.isfile(input_path):
            raise ConversionError(f"Input file not found: {input_path}")
        
        output_file = f"{output_path}.{extension}"
        
        cmd = [
            "ffmpeg",
            "-y",
            "-threads", "0",                # Use all CPU cores
            "-i", input_path,
            "-vn",
            "-c:a", codec,
            output_file,
        ]
        
        try:
            subprocess.run(cmd, capture_output=True, check=True)
            return output_file
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.decode(errors="ignore") if e.stderr else str(e)
            raise ConversionError(f"Conversion failed: {error_msg}")
    
    def _convert_with_bitrate(
        self,
        input_path: str,
        output_path: str,
        extension: str,
        codec: str,
        bitrate: str,
    ) -> str:
        """Conversion with specified bitrate."""
        if not os.path.isfile(input_path):
            raise ConversionError(f"Input file not found: {input_path}")
        
        output_file = f"{output_path}.{extension}"
        
        cmd = [
            "ffmpeg",
            "-y",
            "-threads", "0",                # Use all CPU cores
            "-i", input_path,
            "-vn",
            "-c:a", codec,
            "-b:a", bitrate,
            output_file,
        ]
        
        # Add faststart for M4A container
        if extension == "m4a":
            cmd.insert(-1, "-movflags")
            cmd.insert(-1, "+faststart")
        
        try:
            subprocess.run(cmd, capture_output=True, check=True)
            return output_file
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.decode(errors="ignore") if e.stderr else str(e)
            raise ConversionError(f"Conversion failed: {error_msg}")
    
    def _convert_with_quality(
        self,
        input_path: str,
        output_path: str,
        extension: str,
        codec: str,
        quality: str,
    ) -> str:
        """Conversion with VBR quality setting."""
        if not os.path.isfile(input_path):
            raise ConversionError(f"Input file not found: {input_path}")
        
        output_file = f"{output_path}.{extension}"
        
        cmd = [
            "ffmpeg",
            "-y",
            "-threads", "0",                # Use all CPU cores
            "-i", input_path,
            "-vn",
            "-c:a", codec,
            "-q:a", quality,
            output_file,
        ]
        
        try:
            subprocess.run(cmd, capture_output=True, check=True)
            return output_file
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.decode(errors="ignore") if e.stderr else str(e)
            raise ConversionError(f"Conversion failed: {error_msg}")
    
    def remux_to_m4a(self, input_path: str, output_path: str) -> str:
        """
        Remux container to M4A without re-encoding (fast, lossless).
        
        Args:
            input_path: Input m4s/mp4 file
            output_path: Output path (without extension)
        
        Returns:
            Path to remuxed M4A file
        """
        if not os.path.isfile(input_path):
            raise ConversionError(f"Input file not found: {input_path}")
        
        output_file = f"{output_path}.m4a"
        
        cmd = [
            "ffmpeg",
            "-y",
            "-i", input_path,
            "-c", "copy",                   # Copy streams without re-encoding
            "-movflags", "+faststart",      # Optimize for streaming
            output_file,
        ]
        
        try:
            subprocess.run(cmd, capture_output=True, check=True)
            return output_file
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.decode(errors="ignore") if e.stderr else str(e)
            raise ConversionError(f"Remux failed: {error_msg}")
