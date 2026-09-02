# To run this code you need to install the following dependencies:
# pip install google-genai

import mimetypes
import struct
import sys
from pathlib import Path

# Allow running directly from this directory or from the project root
_HERE = Path(__file__).resolve().parent
_PROJECT_ROOT = _HERE.parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from google.genai import types
from google_client import google_client
from matrx_ai._ext import get_ext

from matrx_utils import vcprint, clear_terminal


def _temp_path() -> Path:
    """The host's AI output temp dir, resolved LAZILY at first use.

    Reading ``get_ext("TEMP_DIR")`` at import time made this module
    un-importable on a standalone install. The package must import cleanly
    with no host configured.
    """
    path = get_ext("TEMP_DIR") / 'app_outputs' / 'ai'
    path.mkdir(parents=True, exist_ok=True)
    return path


def save_binary_file(file_path: Path, data: bytes) -> None:
    with open(file_path, "wb") as f:
        f.write(data)
    print(f"File saved to: {file_path}")



def generate(file_prefix):
    client = google_client()

    # model = "gemini-2.5-pro-preview-tts"
    model = "gemini-2.5-flash-preview-tts"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""Please read aloud the following in a podcast interview style:

Alex: Okay, real talk — every single person listening to this right now started life as one cell. One. And somehow that one cell divided and divided and divided until you became a full human being with trillions of cells. How does that even work?

Sarah: And here's what makes it even wilder — that process never really stops. Right now, as you're listening to this, your body is dividing cells to replace the ones you're losing, healing damage, keeping you alive. Cell division is happening inside you this very second.

Alex: So today we're diving deep into Chapter Nine of cell biology — the cell cycle. By the end of this episode, you're going to understand exactly how cells divide, what controls that process, and why when that control breaks down, you get cancer.

Sarah: Let's start with the basics. Why does cell division even matter? There are three big jobs it does. First, in single-celled organisms like bacteria, cell division is literally reproduction — it's how they make more of themselves. Second, in multicellular creatures like us, it's how we develop from that single fertilized egg into a whole organism. And third — and this is the one people forget — it's how we repair and replace damaged or worn-out cells.


Alex: Pretty Purple Monkeys Are Tired, everyone. You've got this. Thanks for listening.

Sarah: See you in the next one.
"""),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        response_modalities=[
            "audio",
        ],
        speech_config=types.SpeechConfig(
            multi_speaker_voice_config=types.MultiSpeakerVoiceConfig(
                speaker_voice_configs=[
                    types.SpeakerVoiceConfig(
                        speaker="Alex",
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                voice_name="Orus"
                            )
                        ),
                    ),
                    types.SpeakerVoiceConfig(
                        speaker="Sarah",
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                voice_name="Kore"
                            )
                        ),
                    ),
                ]
            ),
        ),
    )

    file_index = 0
    last_chunk = None
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        if (
            chunk.parts is None
        ):
            continue
        if chunk.parts[0].inline_data and chunk.parts[0].inline_data.data:
            inline_data = chunk.parts[0].inline_data
            data_buffer = inline_data.data
            file_extension = mimetypes.guess_extension(inline_data.mime_type)
            if file_extension is None:
                file_extension = ".wav"
                data_buffer = convert_to_wav(inline_data.data, inline_data.mime_type)
            file_path = _temp_path() / f"{file_prefix}_{file_index}{file_extension}"
            file_index += 1
            save_binary_file(file_path, data_buffer)
        else:
            print(chunk.text)

        if chunk.candidates:
            for cand in chunk.candidates:
                if cand.finish_reason:
                    finish_reason = cand.finish_reason
                    usage_metadata = chunk.usage_metadata
                    model_version = chunk.model_version
                    response_id = chunk.response_id
                    last_chunk = chunk
                    
    return last_chunk


def convert_to_wav(audio_data: bytes, mime_type: str) -> bytes:
    """Generates a WAV file header for the given audio data and parameters.

    Args:
        audio_data: The raw audio data as a bytes object.
        mime_type: Mime type of the audio data.

    Returns:
        A bytes object representing the WAV file header.
    """
    parameters = parse_audio_mime_type(mime_type)
    bits_per_sample = parameters["bits_per_sample"]
    sample_rate = parameters["rate"]
    num_channels = 1
    data_size = len(audio_data)
    bytes_per_sample = bits_per_sample // 8
    block_align = num_channels * bytes_per_sample
    byte_rate = sample_rate * block_align
    chunk_size = 36 + data_size  # 36 bytes for header fields before data chunk size

    # http://soundfile.sapp.org/doc/WaveFormat/

    header = struct.pack(
        "<4sI4s4sIHHIIHH4sI",
        b"RIFF",          # ChunkID
        chunk_size,       # ChunkSize (total file size - 8 bytes)
        b"WAVE",          # Format
        b"fmt ",          # Subchunk1ID
        16,               # Subchunk1Size (16 for PCM)
        1,                # AudioFormat (1 for PCM)
        num_channels,     # NumChannels
        sample_rate,      # SampleRate
        byte_rate,        # ByteRate
        block_align,      # BlockAlign
        bits_per_sample,  # BitsPerSample
        b"data",          # Subchunk2ID
        data_size         # Subchunk2Size (size of audio data)
    )
    return header + audio_data

def parse_audio_mime_type(mime_type: str) -> dict[str, int | None]:
    """Parses bits per sample and rate from an audio MIME type string.

    Assumes bits per sample is encoded like "L16" and rate as "rate=xxxxx".

    Args:
        mime_type: The audio MIME type string (e.g., "audio/L16;rate=24000").

    Returns:
        A dictionary with "bits_per_sample" and "rate" keys. Values will be
        integers if found, otherwise None.
    """
    bits_per_sample = 16
    rate = 24000

    # Extract rate from parameters
    parts = mime_type.split(";")
    for param in parts: # Skip the main type part
        param = param.strip()
        if param.lower().startswith("rate="):
            try:
                rate_str = param.split("=", 1)[1]
                rate = int(rate_str)
            except (ValueError, IndexError):
                # Handle cases like "rate=" with no value or non-integer value
                pass # Keep rate as default
        elif param.startswith("audio/L"):
            try:
                bits_per_sample = int(param.split("L", 1)[1])
            except (ValueError, IndexError):
                pass # Keep bits_per_sample as default if conversion fails

    return {"bits_per_sample": bits_per_sample, "rate": rate}


if __name__ == "__main__":
    clear_terminal()

    file_prefix = "podcast_direct"
    last_chunk = generate(file_prefix)
    if last_chunk:
        vcprint(last_chunk, "LAST CHUNK", color="green")
    else:
        vcprint("No last chunk found", color="red")


