"""
Usage:
1.
    Install uv from https://docs.astral.sh/uv/getting-started/installation
2.
    Copy this file to new folder
3.
    Download these files
    wget https://huggingface.co/thewh1teagle/kokoro-hebrew-nc/resolve/main/kokoro.onnx
    wget https://huggingface.co/thewh1teagle/kokoro-hebrew-nc/resolve/main/voices-hebrew.bin
    wget https://huggingface.co/thewh1teagle/kokoro-hebrew-nc/resolve/main/config.json
    wget https://huggingface.co/thewh1teagle/renikud/resolve/main/model.onnx -O renikud.onnx
4. Run
    uv venv --seed -p 3.12
    source .venv/bin/activate
    uv pip install -U kokoro-onnx soundfile renikud-onnx
    uv run main.py

For other languages read https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md

Note: this Hebrew model is licensed for non-commercial use under the terms of
https://huggingface.co/avris/kokoro-hebrew-saspeech
"""

import soundfile as sf
from renikud_onnx import G2P

from kokoro_onnx import Kokoro

# Hebrew G2P
g2p = G2P("renikud.onnx")

# Kokoro
kokoro = Kokoro("kokoro.onnx", "voices-hebrew.bin", vocab_config="config.json")

# Phonemize
text = "שימו לב נוסעים יקרים, הרכבת תכנס לתחנת תל אביב מרכז בעוד מספר דקות. אנא התרחקו מקצה הרציף."
phonemes = g2p.phonemize(text)

# Create
samples, sample_rate = kokoro.create(phonemes, "he_shaul", is_phonemes=True)

# Save
sf.write("audio.wav", samples, sample_rate)
print("Created audio.wav")
