#!/usr/bin/env python3
"""Sync AI models to GCS bucket for SAGE.

Downloads GGUF models from HuggingFace and uploads to GCS,
with automatic local cleanup to save disk space.

Performance optimizations:
- Uses httpx with HTTP/2 instead of curl subprocess (faster, less overhead)
- Streaming downloads with large 1MB chunks and buffered writes
- Optional streaming upload pipeline (download→upload without temp file)
- Parallel sync with configurable workers

Usage:
    python sage/scripts/sync_models_to_gcs.py --all          # Sync all models
    python sage/scripts/sync_models_to_gcs.py --model qwen   # Sync matching models
    python sage/scripts/sync_models_to_gcs.py --list         # List what would sync
    python sage/scripts/sync_models_to_gcs.py --all --workers 4  # Parallel sync
    python sage/scripts/sync_models_to_gcs.py --all --stream # Stream directly to GCS
"""

from __future__ import annotations

import argparse
import subprocess
import tempfile
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import httpx

# Thread-safe print lock
_print_lock = threading.Lock()

# Optimized chunk size for downloads (1MB)
CHUNK_SIZE = 1024 * 1024
# Buffer size for file writes (8MB)
WRITE_BUFFER_SIZE = 8 * 1024 * 1024


def safe_print(*args, **kwargs):
    """Thread-safe print with flush."""
    with _print_lock:
        print(*args, **kwargs, flush=True)


# GCS bucket for SAGE models
GCS_BUCKET = "gs://sage-ai-models"
GCS_GGUF_PATH = f"{GCS_BUCKET}/gguf"

# HuggingFace GGUF sources (repo, filename pattern)
# These are verified working GGUF downloads
HUGGINGFACE_SOURCES: dict[str, tuple[str, str]] = {
    # Llama models
    "Llama-3.2-1B-Instruct-Q4_K_M.gguf": (
        "bartowski/Llama-3.2-1B-Instruct-GGUF",
        "Llama-3.2-1B-Instruct-Q4_K_M.gguf",
    ),
    "Llama-3.2-3B-Instruct-Q4_K_M.gguf": (
        "bartowski/Llama-3.2-3B-Instruct-GGUF",
        "Llama-3.2-3B-Instruct-Q4_K_M.gguf",
    ),
    "Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf": (
        "bartowski/Meta-Llama-3.1-8B-Instruct-GGUF",
        "Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf",
    ),
    # Qwen models
    "Qwen2.5-Coder-1.5B-Instruct-Q4_K_M.gguf": (
        "bartowski/Qwen2.5-Coder-1.5B-Instruct-GGUF",
        "Qwen2.5-Coder-1.5B-Instruct-Q4_K_M.gguf",
    ),
    "Qwen2.5-Coder-3B-Instruct-Q4_K_M.gguf": (
        "bartowski/Qwen2.5-Coder-3B-Instruct-GGUF",
        "Qwen2.5-Coder-3B-Instruct-Q4_K_M.gguf",
    ),
    "Qwen2.5-Coder-7B-Instruct-Q4_K_M.gguf": (
        "bartowski/Qwen2.5-Coder-7B-Instruct-GGUF",
        "Qwen2.5-Coder-7B-Instruct-Q4_K_M.gguf",
    ),
    "Qwen2.5-Coder-14B-Instruct-Q4_K_M.gguf": (
        "bartowski/Qwen2.5-Coder-14B-Instruct-GGUF",
        "Qwen2.5-Coder-14B-Instruct-Q4_K_M.gguf",
    ),
    "Qwen2.5-7B-Instruct-Q4_K_M.gguf": (
        "bartowski/Qwen2.5-7B-Instruct-GGUF",
        "Qwen2.5-7B-Instruct-Q4_K_M.gguf",
    ),
    "Qwen2.5-14B-Instruct-Q4_K_M.gguf": (
        "bartowski/Qwen2.5-14B-Instruct-GGUF",
        "Qwen2.5-14B-Instruct-Q4_K_M.gguf",
    ),
    "Qwen2.5-32B-Instruct-Q4_K_M.gguf": (
        "bartowski/Qwen2.5-32B-Instruct-GGUF",
        "Qwen2.5-32B-Instruct-Q4_K_M.gguf",
    ),
    # Qwen3 models
    "Qwen3-1.7B-Q4_K_M.gguf": ("bartowski/Qwen3-1.7B-GGUF", "Qwen3-1.7B-Q4_K_M.gguf"),
    "Qwen3-4B-Q4_K_M.gguf": ("bartowski/Qwen3-4B-GGUF", "Qwen3-4B-Q4_K_M.gguf"),
    "Qwen3-8B-Q4_K_M.gguf": ("bartowski/Qwen3-8B-GGUF", "Qwen3-8B-Q4_K_M.gguf"),
    "Qwen3-14B-Q4_K_M.gguf": ("bartowski/Qwen3-14B-GGUF", "Qwen3-14B-Q4_K_M.gguf"),
    "Qwen3-30B-A3B-Q4_K_M.gguf": ("bartowski/Qwen3-30B-A3B-GGUF", "Qwen3-30B-A3B-Q4_K_M.gguf"),
    # DeepSeek models
    "DeepSeek-R1-Distill-Qwen-1.5B-Q4_K_M.gguf": (
        "bartowski/DeepSeek-R1-Distill-Qwen-1.5B-GGUF",
        "DeepSeek-R1-Distill-Qwen-1.5B-Q4_K_M.gguf",
    ),
    "DeepSeek-R1-Distill-Qwen-7B-Q4_K_M.gguf": (
        "bartowski/DeepSeek-R1-Distill-Qwen-7B-GGUF",
        "DeepSeek-R1-Distill-Qwen-7B-Q4_K_M.gguf",
    ),
    "DeepSeek-R1-Distill-Qwen-14B-Q4_K_M.gguf": (
        "bartowski/DeepSeek-R1-Distill-Qwen-14B-GGUF",
        "DeepSeek-R1-Distill-Qwen-14B-Q4_K_M.gguf",
    ),
    "DeepSeek-R1-Distill-Qwen-32B-Q4_K_M.gguf": (
        "bartowski/DeepSeek-R1-Distill-Qwen-32B-GGUF",
        "DeepSeek-R1-Distill-Qwen-32B-Q4_K_M.gguf",
    ),
    "DeepSeek-Coder-V2-Lite-Instruct-Q4_K_M.gguf": (
        "bartowski/DeepSeek-Coder-V2-Lite-Instruct-GGUF",
        "DeepSeek-Coder-V2-Lite-Instruct-Q4_K_M.gguf",
    ),
    # Mistral models
    "Mistral-7B-Instruct-v0.3-Q4_K_M.gguf": (
        "bartowski/Mistral-7B-Instruct-v0.3-GGUF",
        "Mistral-7B-Instruct-v0.3-Q4_K_M.gguf",
    ),
    "Mistral-Nemo-Instruct-2407-Q4_K_M.gguf": (
        "bartowski/Mistral-Nemo-Instruct-2407-GGUF",
        "Mistral-Nemo-Instruct-2407-Q4_K_M.gguf",
    ),
    "Mistral-Small-24B-Instruct-2501-Q4_K_M.gguf": (
        "bartowski/Mistral-Small-24B-Instruct-2501-GGUF",
        "Mistral-Small-24B-Instruct-2501-Q4_K_M.gguf",
    ),
    "Codestral-22B-v0.1-Q4_K_M.gguf": (
        "bartowski/Codestral-22B-v0.1-GGUF",
        "Codestral-22B-v0.1-Q4_K_M.gguf",
    ),
    # Google Gemma models
    "gemma-2-2b-it-Q4_K_M.gguf": ("bartowski/gemma-2-2b-it-GGUF", "gemma-2-2b-it-Q4_K_M.gguf"),
    "gemma-2-9b-it-Q4_K_M.gguf": ("bartowski/gemma-2-9b-it-GGUF", "gemma-2-9b-it-Q4_K_M.gguf"),
    "gemma-2-27b-it-Q4_K_M.gguf": ("bartowski/gemma-2-27b-it-GGUF", "gemma-2-27b-it-Q4_K_M.gguf"),
    "codegemma-7b-it-Q4_K_M.gguf": (
        "bartowski/codegemma-7b-it-GGUF",
        "codegemma-7b-it-Q4_K_M.gguf",
    ),
    # Microsoft Phi models
    "Phi-3-mini-4k-instruct-Q4_K_M.gguf": (
        "bartowski/Phi-3-mini-4k-instruct-GGUF",
        "Phi-3-mini-4k-instruct-Q4_K_M.gguf",
    ),
    "Phi-3.5-mini-instruct-Q4_K_M.gguf": (
        "bartowski/Phi-3.5-mini-instruct-GGUF",
        "Phi-3.5-mini-instruct-Q4_K_M.gguf",
    ),
    "Phi-4-Q4_K_M.gguf": ("bartowski/Phi-4-GGUF", "Phi-4-Q4_K_M.gguf"),
    # IBM Granite models
    "granite-3.1-8b-instruct-Q4_K_M.gguf": (
        "bartowski/granite-3.1-8b-instruct-GGUF",
        "granite-3.1-8b-instruct-Q4_K_M.gguf",
    ),
    "granite-3.1-2b-instruct-Q4_K_M.gguf": (
        "bartowski/granite-3.1-2b-instruct-GGUF",
        "granite-3.1-2b-instruct-Q4_K_M.gguf",
    ),
    # Yi Coder models
    "Yi-Coder-1.5B-Chat-Q4_K_M.gguf": (
        "bartowski/Yi-Coder-1.5B-Chat-GGUF",
        "Yi-Coder-1.5B-Chat-Q4_K_M.gguf",
    ),
    "Yi-Coder-9B-Chat-Q4_K_M.gguf": (
        "bartowski/Yi-Coder-9B-Chat-GGUF",
        "Yi-Coder-9B-Chat-Q4_K_M.gguf",
    ),
    # StarCoder models
    "starcoder2-3b-Q4_K_M.gguf": ("bartowski/starcoder2-3b-GGUF", "starcoder2-3b-Q4_K_M.gguf"),
    "starcoder2-7b-Q4_K_M.gguf": ("bartowski/starcoder2-7b-GGUF", "starcoder2-7b-Q4_K_M.gguf"),
    "starcoder2-15b-Q4_K_M.gguf": ("bartowski/starcoder2-15b-GGUF", "starcoder2-15b-Q4_K_M.gguf"),
    # Small/Edge models
    "SmolLM2-1.7B-Instruct-Q4_K_M.gguf": (
        "bartowski/SmolLM2-1.7B-Instruct-GGUF",
        "SmolLM2-1.7B-Instruct-Q4_K_M.gguf",
    ),
    "SmolLM2-360M-Instruct-Q4_K_M.gguf": (
        "bartowski/SmolLM2-360M-Instruct-GGUF",
        "SmolLM2-360M-Instruct-Q4_K_M.gguf",
    ),
    "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf": (
        "TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF",
        "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf",
    ),
    # Code Llama models
    "CodeLlama-7b-Instruct-Q4_K_M.gguf": (
        "bartowski/CodeLlama-7b-Instruct-GGUF",
        "CodeLlama-7b-Instruct-Q4_K_M.gguf",
    ),
    "CodeLlama-13b-Instruct-Q4_K_M.gguf": (
        "bartowski/CodeLlama-13b-Instruct-GGUF",
        "CodeLlama-13b-Instruct-Q4_K_M.gguf",
    ),
    "CodeLlama-34b-Instruct-Q4_K_M.gguf": (
        "bartowski/CodeLlama-34b-Instruct-GGUF",
        "CodeLlama-34b-Instruct-Q4_K_M.gguf",
    ),
    # Dolphin models
    "dolphin-2.9.1-llama-3-8b-Q4_K_M.gguf": (
        "bartowski/dolphin-2.9.1-llama-3-8b-GGUF",
        "dolphin-2.9.1-llama-3-8b-Q4_K_M.gguf",
    ),
    # WizardCoder
    "WizardCoder-33B-V1.1-Q4_K_M.gguf": (
        "TheBloke/WizardCoder-33B-V1.1-GGUF",
        "wizardcoder-33b-v1.1.Q4_K_M.gguf",
    ),
    # Magicoder
    "magicoder-s-ds-6.7b-Q4_K_M.gguf": (
        "bartowski/magicoder-s-ds-6.7b-GGUF",
        "magicoder-s-ds-6.7b-Q4_K_M.gguf",
    ),
    # OpenCoder
    "OpenCoder-8B-Instruct-Q4_K_M.gguf": (
        "bartowski/OpenCoder-8B-Instruct-GGUF",
        "OpenCoder-8B-Instruct-Q4_K_M.gguf",
    ),
    # DeepCoder
    "DeepCoder-14B-Preview-Q4_K_M.gguf": (
        "bartowski/DeepCoder-14B-Preview-GGUF",
        "DeepCoder-14B-Preview-Q4_K_M.gguf",
    ),
    # Hermes models
    "Hermes-3-Llama-3.1-8B-Q4_K_M.gguf": (
        "bartowski/Hermes-3-Llama-3.1-8B-GGUF",
        "Hermes-3-Llama-3.1-8B-Q4_K_M.gguf",
    ),
    # Cogito models
    "Cogito-v1-Preview-Llama-3B-Q4_K_M.gguf": (
        "bartowski/Cogito-v1-Preview-Llama-3B-GGUF",
        "Cogito-v1-Preview-Llama-3B-Q4_K_M.gguf",
    ),
    # Falcon models
    "falcon3-1b-instruct-Q4_K_M.gguf": (
        "bartowski/falcon3-1b-instruct-GGUF",
        "falcon3-1b-instruct-Q4_K_M.gguf",
    ),
    "falcon3-3b-instruct-Q4_K_M.gguf": (
        "bartowski/falcon3-3b-instruct-GGUF",
        "falcon3-3b-instruct-Q4_K_M.gguf",
    ),
    "falcon3-7b-instruct-Q4_K_M.gguf": (
        "bartowski/falcon3-7b-instruct-GGUF",
        "falcon3-7b-instruct-Q4_K_M.gguf",
    ),
    "falcon3-10b-instruct-Q4_K_M.gguf": (
        "bartowski/falcon3-10b-instruct-GGUF",
        "falcon3-10b-instruct-Q4_K_M.gguf",
    ),
    # OLMo models
    "OLMo-2-1124-7B-Instruct-Q4_K_M.gguf": (
        "bartowski/OLMo-2-1124-7B-Instruct-GGUF",
        "OLMo-2-1124-7B-Instruct-Q4_K_M.gguf",
    ),
    "OLMo-2-1124-13B-Instruct-Q4_K_M.gguf": (
        "bartowski/OLMo-2-1124-13B-Instruct-GGUF",
        "OLMo-2-1124-13B-Instruct-Q4_K_M.gguf",
    ),
    # Aya models
    "aya-expanse-8b-Q4_K_M.gguf": ("bartowski/aya-expanse-8b-GGUF", "aya-expanse-8b-Q4_K_M.gguf"),
    "aya-expanse-32b-Q4_K_M.gguf": (
        "bartowski/aya-expanse-32b-GGUF",
        "aya-expanse-32b-Q4_K_M.gguf",
    ),
    # Command R models
    "command-r-08-2024-Q4_K_M.gguf": (
        "bartowski/command-r-08-2024-GGUF",
        "command-r-08-2024-Q4_K_M.gguf",
    ),
    # Exaone models
    "EXAONE-3.5-7.8B-Instruct-Q4_K_M.gguf": (
        "bartowski/EXAONE-3.5-7.8B-Instruct-GGUF",
        "EXAONE-3.5-7.8B-Instruct-Q4_K_M.gguf",
    ),
    "EXAONE-3.5-32B-Instruct-Q4_K_M.gguf": (
        "bartowski/EXAONE-3.5-32B-Instruct-GGUF",
        "EXAONE-3.5-32B-Instruct-Q4_K_M.gguf",
    ),
    # Tulu models
    "Llama-3.1-Tulu-3-8B-Q4_K_M.gguf": (
        "bartowski/Llama-3.1-Tulu-3-8B-GGUF",
        "Llama-3.1-Tulu-3-8B-Q4_K_M.gguf",
    ),
    # OpenThinker
    "OpenThinker-7B-Q4_K_M.gguf": ("bartowski/OpenThinker-7B-GGUF", "OpenThinker-7B-Q4_K_M.gguf"),
    # DeepScaler
    "DeepScaler-1.5B-Preview-Q4_K_M.gguf": (
        "bartowski/DeepScaler-1.5B-Preview-GGUF",
        "DeepScaler-1.5B-Preview-Q4_K_M.gguf",
    ),
    # SmallThinker
    "smallthinker-3b-preview-Q4_K_M.gguf": (
        "bartowski/smallthinker-3b-preview-GGUF",
        "smallthinker-3b-preview-Q4_K_M.gguf",
    ),
    # Marco-o1
    "Marco-o1-Q4_K_M.gguf": ("bartowski/Marco-o1-GGUF", "Marco-o1-Q4_K_M.gguf"),
    # DBRX
    "dbrx-instruct-Q4_K_M.gguf": ("bartowski/dbrx-instruct-GGUF", "dbrx-instruct-Q4_K_M.gguf"),
    # Solar
    "solar-10.7b-instruct-v1.0-Q4_K_M.gguf": (
        "bartowski/solar-10.7b-instruct-v1.0-GGUF",
        "solar-10.7b-instruct-v1.0-Q4_K_M.gguf",
    ),
    "solar-pro-preview-instruct-Q4_K_M.gguf": (
        "bartowski/solar-pro-preview-instruct-GGUF",
        "solar-pro-preview-instruct-Q4_K_M.gguf",
    ),
    # Internlm
    "internlm2_5-7b-chat-Q4_K_M.gguf": (
        "bartowski/internlm2_5-7b-chat-GGUF",
        "internlm2_5-7b-chat-Q4_K_M.gguf",
    ),
    "internlm2_5-20b-chat-Q4_K_M.gguf": (
        "bartowski/internlm2_5-20b-chat-GGUF",
        "internlm2_5-20b-chat-Q4_K_M.gguf",
    ),
    # GLM models
    "glm-4-9b-chat-Q4_K_M.gguf": ("bartowski/glm-4-9b-chat-GGUF", "glm-4-9b-chat-Q4_K_M.gguf"),
    # Athene
    "Athene-V2-Chat-Q4_K_M.gguf": ("bartowski/Athene-V2-Chat-GGUF", "Athene-V2-Chat-Q4_K_M.gguf"),
    # Nemotron
    "nemotron-mini-4b-instruct-Q4_K_M.gguf": (
        "bartowski/nemotron-mini-4b-instruct-GGUF",
        "nemotron-mini-4b-instruct-Q4_K_M.gguf",
    ),
    "Llama-3.1-Nemotron-70B-Instruct-Q4_K_M.gguf": (
        "bartowski/Llama-3.1-Nemotron-70B-Instruct-GGUF",
        "Llama-3.1-Nemotron-70B-Instruct-Q4_K_M.gguf",
    ),
    # ══════════════════════════════════════════════════════════════════════════
    # EXPANDED MODELS - Converting Ollama catalog to GGUF downloads
    # ══════════════════════════════════════════════════════════════════════════
    # Llama 3.3 70B
    "Llama-3.3-70B-Instruct-Q4_K_M.gguf": (
        "bartowski/Llama-3.3-70B-Instruct-GGUF",
        "Llama-3.3-70B-Instruct-Q4_K_M.gguf",
    ),
    # Llama 2 models
    "llama-2-7b-chat.Q4_K_M.gguf": ("TheBloke/Llama-2-7B-Chat-GGUF", "llama-2-7b-chat.Q4_K_M.gguf"),
    "llama-2-13b-chat.Q4_K_M.gguf": (
        "TheBloke/Llama-2-13B-chat-GGUF",
        "llama-2-13b-chat.Q4_K_M.gguf",
    ),
    "llama-2-70b-chat.Q4_K_M.gguf": (
        "TheBloke/Llama-2-70B-chat-GGUF",
        "llama-2-70b-chat.Q4_K_M.gguf",
    ),
    # Mixtral MoE
    "Mixtral-8x7B-Instruct-v0.1-Q4_K_M.gguf": (
        "bartowski/Mixtral-8x7B-Instruct-v0.1-GGUF",
        "Mixtral-8x7B-Instruct-v0.1-Q4_K_M.gguf",
    ),
    "Mixtral-8x22B-Instruct-v0.1-Q4_K_M.gguf": (
        "bartowski/Mixtral-8x22B-Instruct-v0.1-GGUF",
        "Mixtral-8x22B-Instruct-v0.1-Q4_K_M.gguf",
    ),
    # Qwen 2 base models
    "Qwen2-0.5B-Instruct-Q4_K_M.gguf": (
        "bartowski/Qwen2-0.5B-Instruct-GGUF",
        "Qwen2-0.5B-Instruct-Q4_K_M.gguf",
    ),
    "Qwen2-1.5B-Instruct-Q4_K_M.gguf": (
        "bartowski/Qwen2-1.5B-Instruct-GGUF",
        "Qwen2-1.5B-Instruct-Q4_K_M.gguf",
    ),
    "Qwen2-7B-Instruct-Q4_K_M.gguf": (
        "bartowski/Qwen2-7B-Instruct-GGUF",
        "Qwen2-7B-Instruct-Q4_K_M.gguf",
    ),
    "Qwen2-72B-Instruct-Q4_K_M.gguf": (
        "bartowski/Qwen2-72B-Instruct-GGUF",
        "Qwen2-72B-Instruct-Q4_K_M.gguf",
    ),
    # Qwen 2.5 extended
    "Qwen2.5-0.5B-Instruct-Q4_K_M.gguf": (
        "bartowski/Qwen2.5-0.5B-Instruct-GGUF",
        "Qwen2.5-0.5B-Instruct-Q4_K_M.gguf",
    ),
    "Qwen2.5-1.5B-Instruct-Q4_K_M.gguf": (
        "bartowski/Qwen2.5-1.5B-Instruct-GGUF",
        "Qwen2.5-1.5B-Instruct-Q4_K_M.gguf",
    ),
    "Qwen2.5-3B-Instruct-Q4_K_M.gguf": (
        "bartowski/Qwen2.5-3B-Instruct-GGUF",
        "Qwen2.5-3B-Instruct-Q4_K_M.gguf",
    ),
    "Qwen2.5-72B-Instruct-Q4_K_M.gguf": (
        "bartowski/Qwen2.5-72B-Instruct-GGUF",
        "Qwen2.5-72B-Instruct-Q4_K_M.gguf",
    ),
    # Qwen 2.5 Coder extended
    "Qwen2.5-Coder-0.5B-Instruct-Q4_K_M.gguf": (
        "bartowski/Qwen2.5-Coder-0.5B-Instruct-GGUF",
        "Qwen2.5-Coder-0.5B-Instruct-Q4_K_M.gguf",
    ),
    "Qwen2.5-Coder-32B-Instruct-Q4_K_M.gguf": (
        "bartowski/Qwen2.5-Coder-32B-Instruct-GGUF",
        "Qwen2.5-Coder-32B-Instruct-Q4_K_M.gguf",
    ),
    # QwQ reasoning
    "QwQ-32B-Preview-Q4_K_M.gguf": (
        "bartowski/QwQ-32B-Preview-GGUF",
        "QwQ-32B-Preview-Q4_K_M.gguf",
    ),
    # Qwen2 Math
    "Qwen2-Math-1.5B-Instruct-Q4_K_M.gguf": (
        "bartowski/Qwen2-Math-1.5B-Instruct-GGUF",
        "Qwen2-Math-1.5B-Instruct-Q4_K_M.gguf",
    ),
    "Qwen2-Math-7B-Instruct-Q4_K_M.gguf": (
        "bartowski/Qwen2-Math-7B-Instruct-GGUF",
        "Qwen2-Math-7B-Instruct-Q4_K_M.gguf",
    ),
    "Qwen2-Math-72B-Instruct-Q4_K_M.gguf": (
        "bartowski/Qwen2-Math-72B-Instruct-GGUF",
        "Qwen2-Math-72B-Instruct-Q4_K_M.gguf",
    ),
    # DeepSeek extended
    "deepseek-llm-7b-chat-Q4_K_M.gguf": (
        "TheBloke/deepseek-llm-7B-chat-GGUF",
        "deepseek-llm-7b-chat.Q4_K_M.gguf",
    ),
    "deepseek-llm-67b-chat-Q4_K_M.gguf": (
        "TheBloke/deepseek-llm-67b-chat-GGUF",
        "deepseek-llm-67b-chat.Q4_K_M.gguf",
    ),
    "deepseek-coder-1.3b-instruct-Q4_K_M.gguf": (
        "TheBloke/deepseek-coder-1.3b-instruct-GGUF",
        "deepseek-coder-1.3b-instruct.Q4_K_M.gguf",
    ),
    "deepseek-coder-6.7b-instruct-Q4_K_M.gguf": (
        "TheBloke/deepseek-coder-6.7b-instruct-GGUF",
        "deepseek-coder-6.7b-instruct.Q4_K_M.gguf",
    ),
    "deepseek-coder-33b-instruct-Q4_K_M.gguf": (
        "TheBloke/deepseek-coder-33b-instruct-GGUF",
        "deepseek-coder-33b-instruct.Q4_K_M.gguf",
    ),
    # Mistral Large
    "Mistral-Large-Instruct-2407-Q4_K_M.gguf": (
        "bartowski/Mistral-Large-Instruct-2407-GGUF",
        "Mistral-Large-Instruct-2407-Q4_K_M.gguf",
    ),
    # Command R+
    "command-r-plus-08-2024-Q4_K_M.gguf": (
        "bartowski/command-r-plus-08-2024-GGUF",
        "command-r-plus-08-2024-Q4_K_M.gguf",
    ),
    "c4ai-command-r7b-12-2024-Q4_K_M.gguf": (
        "bartowski/c4ai-command-r7b-12-2024-GGUF",
        "c4ai-command-r7b-12-2024-Q4_K_M.gguf",
    ),
    # Dolphin extended
    "dolphin-2.9.4-llama3.1-8b-Q4_K_M.gguf": (
        "bartowski/dolphin-2.9.4-llama3.1-8b-GGUF",
        "dolphin-2.9.4-llama3.1-8b-Q4_K_M.gguf",
    ),
    "dolphin-2.9-mixtral-8x22b-Q4_K_M.gguf": (
        "bartowski/dolphin-2.9-mixtral-8x22b-GGUF",
        "dolphin-2.9-mixtral-8x22b-Q4_K_M.gguf",
    ),
    "dolphin-2.8-mistral-7b-v02-Q4_K_M.gguf": (
        "TheBloke/dolphin-2.8-mistral-7b-v02-GGUF",
        "dolphin-2.8-mistral-7b-v02.Q4_K_M.gguf",
    ),
    "dolphin-2.6-phi-2-Q4_K_M.gguf": (
        "TheBloke/dolphin-2_6-phi-2-GGUF",
        "dolphin-2_6-phi-2.Q4_K_M.gguf",
    ),
    # Vicuna
    "vicuna-7b-v1.5-Q4_K_M.gguf": ("TheBloke/vicuna-7B-v1.5-GGUF", "vicuna-7b-v1.5.Q4_K_M.gguf"),
    "vicuna-13b-v1.5-Q4_K_M.gguf": ("TheBloke/vicuna-13B-v1.5-GGUF", "vicuna-13b-v1.5.Q4_K_M.gguf"),
    "vicuna-33b-v1.3-Q4_K_M.gguf": ("TheBloke/vicuna-33B-v1.3-GGUF", "vicuna-33b-v1.3.Q4_K_M.gguf"),
    # Zephyr
    "zephyr-7b-beta-Q4_K_M.gguf": ("TheBloke/zephyr-7B-beta-GGUF", "zephyr-7b-beta.Q4_K_M.gguf"),
    # OpenChat
    "openchat-3.5-0106-Q4_K_M.gguf": (
        "bartowski/openchat-3.5-0106-GGUF",
        "openchat-3.5-0106-Q4_K_M.gguf",
    ),
    # OpenHermes
    "OpenHermes-2.5-Mistral-7B-Q4_K_M.gguf": (
        "TheBloke/OpenHermes-2.5-Mistral-7B-GGUF",
        "openhermes-2.5-mistral-7b.Q4_K_M.gguf",
    ),
    # Starling
    "Starling-LM-7B-alpha-Q4_K_M.gguf": (
        "TheBloke/Starling-LM-7B-alpha-GGUF",
        "starling-lm-7b-alpha.Q4_K_M.gguf",
    ),
    # Neural Chat
    "neural-chat-7b-v3-3-Q4_K_M.gguf": (
        "TheBloke/neural-chat-7B-v3-3-GGUF",
        "neural-chat-7b-v3-3.Q4_K_M.gguf",
    ),
    # WizardLM
    "WizardLM-2-7B-Q4_K_M.gguf": ("bartowski/WizardLM-2-7B-GGUF", "WizardLM-2-7B-Q4_K_M.gguf"),
    "WizardLM-2-8x22B-Q4_K_M.gguf": (
        "bartowski/WizardLM-2-8x22B-GGUF",
        "WizardLM-2-8x22B-Q4_K_M.gguf",
    ),
    "WizardLM-13B-V1.2-Q4_K_M.gguf": (
        "TheBloke/WizardLM-13B-V1.2-GGUF",
        "wizardlm-13b-v1.2.Q4_K_M.gguf",
    ),
    # Wizard Math
    "WizardMath-7B-V1.1-Q4_K_M.gguf": (
        "TheBloke/WizardMath-7B-V1.1-GGUF",
        "wizardmath-7b-v1.1.Q4_K_M.gguf",
    ),
    "WizardMath-70B-V1.0-Q4_K_M.gguf": (
        "TheBloke/WizardMath-70B-V1.0-GGUF",
        "wizardmath-70b-v1.0.Q4_K_M.gguf",
    ),
    # Nous Hermes 2
    "Nous-Hermes-2-Mixtral-8x7B-DPO-Q4_K_M.gguf": (
        "TheBloke/Nous-Hermes-2-Mixtral-8x7B-DPO-GGUF",
        "Nous-Hermes-2-Mixtral-8x7B-DPO.Q4_K_M.gguf",
    ),
    "Nous-Hermes-2-SOLAR-10.7B-Q4_K_M.gguf": (
        "TheBloke/Nous-Hermes-2-SOLAR-10.7B-GGUF",
        "nous-hermes-2-solar-10.7b.Q4_K_M.gguf",
    ),
    # Phi extended
    "Phi-3-medium-4k-instruct-Q4_K_M.gguf": (
        "bartowski/Phi-3-medium-4k-instruct-GGUF",
        "Phi-3-medium-4k-instruct-Q4_K_M.gguf",
    ),
    "Phi-3-medium-128k-instruct-Q4_K_M.gguf": (
        "bartowski/Phi-3-medium-128k-instruct-GGUF",
        "Phi-3-medium-128k-instruct-Q4_K_M.gguf",
    ),
    # CodeQwen
    "CodeQwen1.5-7B-Chat-Q4_K_M.gguf": (
        "bartowski/CodeQwen1.5-7B-Chat-GGUF",
        "CodeQwen1.5-7B-Chat-Q4_K_M.gguf",
    ),
    # CodeGeeX
    "codegeex4-all-9b-Q4_K_M.gguf": (
        "bartowski/codegeex4-all-9b-GGUF",
        "codegeex4-all-9b-Q4_K_M.gguf",
    ),
    # Stable Code
    "stable-code-instruct-3b-Q4_K_M.gguf": (
        "bartowski/stable-code-instruct-3b-GGUF",
        "stable-code-instruct-3b-Q4_K_M.gguf",
    ),
    # DolphinCoder
    "dolphincoder-starcoder2-7b-Q4_K_M.gguf": (
        "bartowski/dolphincoder-starcoder2-7b-GGUF",
        "dolphincoder-starcoder2-7b-Q4_K_M.gguf",
    ),
    "dolphincoder-starcoder2-15b-Q4_K_M.gguf": (
        "bartowski/dolphincoder-starcoder2-15b-GGUF",
        "dolphincoder-starcoder2-15b-Q4_K_M.gguf",
    ),
    # StarCoder 1
    "starcoder-Q4_K_M.gguf": ("TheBloke/starcoder-GGUF", "starcoder.Q4_K_M.gguf"),
    # SQLCoder
    "sqlcoder-7b-2-Q4_K_M.gguf": ("bartowski/sqlcoder-7b-2-GGUF", "sqlcoder-7b-2-Q4_K_M.gguf"),
    # Phind CodeLlama
    "Phind-CodeLlama-34B-v2-Q4_K_M.gguf": (
        "TheBloke/Phind-CodeLlama-34B-v2-GGUF",
        "phind-codellama-34b-v2.Q4_K_M.gguf",
    ),
    # Yi extended
    "Yi-1.5-6B-Chat-Q4_K_M.gguf": ("bartowski/Yi-1.5-6B-Chat-GGUF", "Yi-1.5-6B-Chat-Q4_K_M.gguf"),
    "Yi-1.5-9B-Chat-Q4_K_M.gguf": ("bartowski/Yi-1.5-9B-Chat-GGUF", "Yi-1.5-9B-Chat-Q4_K_M.gguf"),
    "Yi-1.5-34B-Chat-Q4_K_M.gguf": (
        "bartowski/Yi-1.5-34B-Chat-GGUF",
        "Yi-1.5-34B-Chat-Q4_K_M.gguf",
    ),
    # Mathstral
    "Mathstral-7B-v0.1-Q4_K_M.gguf": (
        "bartowski/Mathstral-7B-v0.1-GGUF",
        "Mathstral-7B-v0.1-Q4_K_M.gguf",
    ),
    # InternLM extended
    "internlm2-chat-1_8b-Q4_K_M.gguf": (
        "bartowski/internlm2-chat-1_8b-GGUF",
        "internlm2-chat-1_8b-Q4_K_M.gguf",
    ),
    # Falcon 2
    "falcon-11B-Q4_K_M.gguf": ("bartowski/falcon-11B-GGUF", "falcon-11B-Q4_K_M.gguf"),
    # Falcon 1
    "falcon-7b-instruct-Q4_K_M.gguf": (
        "TheBloke/falcon-7b-instruct-GGUF",
        "falcon-7b-instruct.Q4_K_M.gguf",
    ),
    "falcon-40b-instruct-Q4_K_M.gguf": (
        "TheBloke/falcon-40b-instruct-GGUF",
        "falcon-40b-instruct.Q4_K_M.gguf",
    ),
    # Reflection
    "Reflection-Llama-3.1-70B-Q4_K_M.gguf": (
        "bartowski/Reflection-Llama-3.1-70B-GGUF",
        "Reflection-Llama-3.1-70B-Q4_K_M.gguf",
    ),
    # NuExtract
    "NuExtract-v1.5-Q4_K_M.gguf": ("bartowski/NuExtract-v1.5-GGUF", "NuExtract-v1.5-Q4_K_M.gguf"),
    # Llama Guard
    "Llama-Guard-3-8B-Q4_K_M.gguf": (
        "bartowski/Llama-Guard-3-8B-GGUF",
        "Llama-Guard-3-8B-Q4_K_M.gguf",
    ),
    "Llama-Guard-3-1B-Q4_K_M.gguf": (
        "bartowski/Llama-Guard-3-1B-GGUF",
        "Llama-Guard-3-1B-Q4_K_M.gguf",
    ),
    # Granite Guardian
    "granite-3.0-8b-instruct-Q4_K_M.gguf": (
        "bartowski/granite-3.0-8b-instruct-GGUF",
        "granite-3.0-8b-instruct-Q4_K_M.gguf",
    ),
    "granite-3.0-2b-instruct-Q4_K_M.gguf": (
        "bartowski/granite-3.0-2b-instruct-GGUF",
        "granite-3.0-2b-instruct-Q4_K_M.gguf",
    ),
    # Granite MoE
    "granite-3.1-1b-a400m-instruct-Q4_K_M.gguf": (
        "bartowski/granite-3.1-1b-a400m-instruct-GGUF",
        "granite-3.1-1b-a400m-instruct-Q4_K_M.gguf",
    ),
    "granite-3.1-3b-a800m-instruct-Q4_K_M.gguf": (
        "bartowski/granite-3.1-3b-a800m-instruct-GGUF",
        "granite-3.1-3b-a800m-instruct-Q4_K_M.gguf",
    ),
    # Granite Code
    "granite-3b-code-instruct-Q4_K_M.gguf": (
        "bartowski/granite-3b-code-instruct-GGUF",
        "granite-3b-code-instruct-Q4_K_M.gguf",
    ),
    "granite-8b-code-instruct-Q4_K_M.gguf": (
        "bartowski/granite-8b-code-instruct-GGUF",
        "granite-8b-code-instruct-Q4_K_M.gguf",
    ),
    "granite-20b-code-instruct-Q4_K_M.gguf": (
        "bartowski/granite-20b-code-instruct-GGUF",
        "granite-20b-code-instruct-Q4_K_M.gguf",
    ),
    "granite-34b-code-instruct-Q4_K_M.gguf": (
        "bartowski/granite-34b-code-instruct-GGUF",
        "granite-34b-code-instruct-Q4_K_M.gguf",
    ),
    # OLMo extended
    "OLMo-7B-Instruct-Q4_K_M.gguf": (
        "bartowski/OLMo-7B-Instruct-GGUF",
        "OLMo-7B-Instruct-Q4_K_M.gguf",
    ),
    # Tulu extended
    "Llama-3.1-Tulu-3-70B-Q4_K_M.gguf": (
        "bartowski/Llama-3.1-Tulu-3-70B-GGUF",
        "Llama-3.1-Tulu-3-70B-Q4_K_M.gguf",
    ),
    # Sailor
    "Sailor2-1B-Chat-Q4_K_M.gguf": (
        "bartowski/Sailor2-1B-Chat-GGUF",
        "Sailor2-1B-Chat-Q4_K_M.gguf",
    ),
    "Sailor2-8B-Chat-Q4_K_M.gguf": (
        "bartowski/Sailor2-8B-Chat-GGUF",
        "Sailor2-8B-Chat-Q4_K_M.gguf",
    ),
    "Sailor2-20B-Chat-Q4_K_M.gguf": (
        "bartowski/Sailor2-20B-Chat-GGUF",
        "Sailor2-20B-Chat-Q4_K_M.gguf",
    ),
    # Aya 23
    "aya-23-8B-Q4_K_M.gguf": ("bartowski/aya-23-8B-GGUF", "aya-23-8B-Q4_K_M.gguf"),
    "aya-23-35B-Q4_K_M.gguf": ("bartowski/aya-23-35B-GGUF", "aya-23-35B-Q4_K_M.gguf"),
    # Cogito extended
    "Cogito-v1-Preview-Llama-8B-Q4_K_M.gguf": (
        "bartowski/Cogito-v1-Preview-Llama-8B-GGUF",
        "Cogito-v1-Preview-Llama-8B-Q4_K_M.gguf",
    ),
    "Cogito-v1-Preview-Llama-70B-Q4_K_M.gguf": (
        "bartowski/Cogito-v1-Preview-Llama-70B-GGUF",
        "Cogito-v1-Preview-Llama-70B-Q4_K_M.gguf",
    ),
    # EXAONE Deep
    "EXAONE-Deep-2.4B-Q4_K_M.gguf": (
        "bartowski/EXAONE-Deep-2.4B-GGUF",
        "EXAONE-Deep-2.4B-Q4_K_M.gguf",
    ),
    # SmolLM extended
    "SmolLM-135M-Instruct-Q4_K_M.gguf": (
        "bartowski/SmolLM-135M-Instruct-GGUF",
        "SmolLM-135M-Instruct-Q4_K_M.gguf",
    ),
    "SmolLM-1.7B-Instruct-Q4_K_M.gguf": (
        "bartowski/SmolLM-1.7B-Instruct-GGUF",
        "SmolLM-1.7B-Instruct-Q4_K_M.gguf",
    ),
    # TinyDolphin
    "TinyDolphin-2.8.2-1.1b-Q4_K_M.gguf": (
        "bartowski/TinyDolphin-2.8.2-1.1b-GGUF",
        "TinyDolphin-2.8.2-1.1b-Q4_K_M.gguf",
    ),
    # Gemma 1
    "gemma-2b-it-Q4_K_M.gguf": ("bartowski/gemma-2b-it-GGUF", "gemma-2b-it-Q4_K_M.gguf"),
    "gemma-7b-it-Q4_K_M.gguf": ("bartowski/gemma-7b-it-GGUF", "gemma-7b-it-Q4_K_M.gguf"),
    # FireFunction
    "firefunction-v2-Q4_K_M.gguf": (
        "bartowski/firefunction-v2-GGUF",
        "firefunction-v2-Q4_K_M.gguf",
    ),
    # Groq Tool Use
    "Llama-3-Groq-8B-Tool-Use-Q4_K_M.gguf": (
        "bartowski/Llama-3-Groq-8B-Tool-Use-GGUF",
        "Llama-3-Groq-8B-Tool-Use-Q4_K_M.gguf",
    ),
    "Llama-3-Groq-70B-Tool-Use-Q4_K_M.gguf": (
        "bartowski/Llama-3-Groq-70B-Tool-Use-GGUF",
        "Llama-3-Groq-70B-Tool-Use-Q4_K_M.gguf",
    ),
    # Llama Pro
    "Llama-Pro-8B-Instruct-Q4_K_M.gguf": (
        "bartowski/Llama-Pro-8B-Instruct-GGUF",
        "Llama-Pro-8B-Instruct-Q4_K_M.gguf",
    ),
    # ChatQA
    "Llama-3-ChatQA-1.5-8B-Q4_K_M.gguf": (
        "bartowski/Llama-3-ChatQA-1.5-8B-GGUF",
        "Llama-3-ChatQA-1.5-8B-Q4_K_M.gguf",
    ),
    "Llama-3-ChatQA-1.5-70B-Q4_K_M.gguf": (
        "bartowski/Llama-3-ChatQA-1.5-70B-GGUF",
        "Llama-3-ChatQA-1.5-70B-Q4_K_M.gguf",
    ),
    # Bespoke Minicheck
    "Bespoke-Minicheck-7B-Q4_K_M.gguf": (
        "bartowski/Bespoke-Minicheck-7B-GGUF",
        "Bespoke-Minicheck-7B-Q4_K_M.gguf",
    ),
    # R1-1776 (Perplexity)
    "r1-1776-Q4_K_M.gguf": ("bartowski/r1-1776-GGUF", "r1-1776-Q4_K_M.gguf"),
    # OpenThinker extended
    "OpenThinker-32B-Q4_K_M.gguf": (
        "bartowski/OpenThinker-32B-GGUF",
        "OpenThinker-32B-Q4_K_M.gguf",
    ),
    # Devstral
    "Devstral-Small-2411-Q4_K_M.gguf": (
        "bartowski/Devstral-Small-2411-GGUF",
        "Devstral-Small-2411-Q4_K_M.gguf",
    ),
    # Magistral
    "Magistral-8B-2506-Q4_K_M.gguf": (
        "bartowski/Magistral-8B-2506-GGUF",
        "Magistral-8B-2506-Q4_K_M.gguf",
    ),
    # Vision models (where available as GGUF)
    "llava-v1.6-mistral-7b-Q4_K_M.gguf": (
        "cjpais/llava-v1.6-mistral-7b-gguf",
        "llava-v1.6-mistral-7b.Q4_K_M.gguf",
    ),
    "llava-phi-3-mini-Q4_K_M.gguf": (
        "bartowski/llava-phi-3-mini-GGUF",
        "llava-phi-3-mini-Q4_K_M.gguf",
    ),
    # MiniCPM-V
    "MiniCPM-V-2_6-Q4_K_M.gguf": ("bartowski/MiniCPM-V-2_6-GGUF", "MiniCPM-V-2_6-Q4_K_M.gguf"),
    # Moondream
    "moondream2-Q4_K_M.gguf": ("bartowski/moondream2-GGUF", "moondream2-Q4_K_M.gguf"),
    # BakLLaVA
    "BakLLaVA-1-Q4_K_M.gguf": ("TheBloke/BakLLaVA-1-GGUF", "bakllava-1.Q4_K_M.gguf"),
    # ══════════════════════════════════════════════════════════════════════════
    # ADDITIONAL MODELS - Expanding to reach 295 total
    # ══════════════════════════════════════════════════════════════════════════
    # Llama 3 base models
    "Meta-Llama-3-8B-Instruct-Q4_K_M.gguf": (
        "bartowski/Meta-Llama-3-8B-Instruct-GGUF",
        "Meta-Llama-3-8B-Instruct-Q4_K_M.gguf",
    ),
    "Meta-Llama-3-70B-Instruct-Q4_K_M.gguf": (
        "bartowski/Meta-Llama-3-70B-Instruct-GGUF",
        "Meta-Llama-3-70B-Instruct-Q4_K_M.gguf",
    ),
    # Llama 3.1 extended
    "Meta-Llama-3.1-70B-Instruct-Q4_K_M.gguf": (
        "bartowski/Meta-Llama-3.1-70B-Instruct-GGUF",
        "Meta-Llama-3.1-70B-Instruct-Q4_K_M.gguf",
    ),
    "Meta-Llama-3.1-405B-Instruct-Q4_K_M.gguf": (
        "bartowski/Meta-Llama-3.1-405B-Instruct-GGUF",
        "Meta-Llama-3.1-405B-Instruct-Q4_K_M.gguf",
    ),
    # Llama 3.2 Vision
    "Llama-3.2-11B-Vision-Instruct-Q4_K_M.gguf": (
        "bartowski/Llama-3.2-11B-Vision-Instruct-GGUF",
        "Llama-3.2-11B-Vision-Instruct-Q4_K_M.gguf",
    ),
    "Llama-3.2-90B-Vision-Instruct-Q4_K_M.gguf": (
        "bartowski/Llama-3.2-90B-Vision-Instruct-GGUF",
        "Llama-3.2-90B-Vision-Instruct-Q4_K_M.gguf",
    ),
    # Qwen 2.5 VL Vision models
    "Qwen2.5-VL-3B-Instruct-Q4_K_M.gguf": (
        "bartowski/Qwen2.5-VL-3B-Instruct-GGUF",
        "Qwen2.5-VL-3B-Instruct-Q4_K_M.gguf",
    ),
    "Qwen2.5-VL-7B-Instruct-Q4_K_M.gguf": (
        "bartowski/Qwen2.5-VL-7B-Instruct-GGUF",
        "Qwen2.5-VL-7B-Instruct-Q4_K_M.gguf",
    ),
    "Qwen2.5-VL-72B-Instruct-Q4_K_M.gguf": (
        "bartowski/Qwen2.5-VL-72B-Instruct-GGUF",
        "Qwen2.5-VL-72B-Instruct-Q4_K_M.gguf",
    ),
    # Qwen3 extended
    "Qwen3-0.6B-Q4_K_M.gguf": ("bartowski/Qwen3-0.6B-GGUF", "Qwen3-0.6B-Q4_K_M.gguf"),
    "Qwen3-32B-Q4_K_M.gguf": ("bartowski/Qwen3-32B-GGUF", "Qwen3-32B-Q4_K_M.gguf"),
    # DeepSeek R1 extended
    "DeepSeek-R1-Distill-Llama-8B-Q4_K_M.gguf": (
        "bartowski/DeepSeek-R1-Distill-Llama-8B-GGUF",
        "DeepSeek-R1-Distill-Llama-8B-Q4_K_M.gguf",
    ),
    "DeepSeek-R1-Distill-Llama-70B-Q4_K_M.gguf": (
        "bartowski/DeepSeek-R1-Distill-Llama-70B-GGUF",
        "DeepSeek-R1-Distill-Llama-70B-Q4_K_M.gguf",
    ),
    # DeepSeek V3
    "DeepSeek-V3-Q4_K_M.gguf": ("bartowski/DeepSeek-V3-GGUF", "DeepSeek-V3-Q4_K_M.gguf"),
    # Gemma 3
    "gemma-3-1b-it-Q4_K_M.gguf": ("bartowski/gemma-3-1b-it-GGUF", "gemma-3-1b-it-Q4_K_M.gguf"),
    "gemma-3-4b-it-Q4_K_M.gguf": ("bartowski/gemma-3-4b-it-GGUF", "gemma-3-4b-it-Q4_K_M.gguf"),
    "gemma-3-12b-it-Q4_K_M.gguf": ("bartowski/gemma-3-12b-it-GGUF", "gemma-3-12b-it-Q4_K_M.gguf"),
    "gemma-3-27b-it-Q4_K_M.gguf": ("bartowski/gemma-3-27b-it-GGUF", "gemma-3-27b-it-Q4_K_M.gguf"),
    # Phi 4 Mini
    "Phi-4-mini-instruct-Q4_K_M.gguf": (
        "bartowski/Phi-4-mini-instruct-GGUF",
        "Phi-4-mini-instruct-Q4_K_M.gguf",
    ),
    # Phi 4 Reasoning
    "Phi-4-reasoning-Q4_K_M.gguf": (
        "bartowski/Phi-4-reasoning-GGUF",
        "Phi-4-reasoning-Q4_K_M.gguf",
    ),
    "Phi-4-mini-reasoning-Q4_K_M.gguf": (
        "bartowski/Phi-4-mini-reasoning-GGUF",
        "Phi-4-mini-reasoning-Q4_K_M.gguf",
    ),
    # Granite extended
    "granite-3.2-2b-instruct-Q4_K_M.gguf": (
        "bartowski/granite-3.2-2b-instruct-GGUF",
        "granite-3.2-2b-instruct-Q4_K_M.gguf",
    ),
    "granite-3.2-8b-instruct-Q4_K_M.gguf": (
        "bartowski/granite-3.2-8b-instruct-GGUF",
        "granite-3.2-8b-instruct-Q4_K_M.gguf",
    ),
    "granite-3.3-2b-instruct-Q4_K_M.gguf": (
        "bartowski/granite-3.3-2b-instruct-GGUF",
        "granite-3.3-2b-instruct-Q4_K_M.gguf",
    ),
    "granite-3.3-8b-instruct-Q4_K_M.gguf": (
        "bartowski/granite-3.3-8b-instruct-GGUF",
        "granite-3.3-8b-instruct-Q4_K_M.gguf",
    ),
    "granite4-350m-instruct-Q4_K_M.gguf": (
        "bartowski/granite4-350m-instruct-GGUF",
        "granite4-350m-instruct-Q4_K_M.gguf",
    ),
    "granite4-3b-instruct-Q4_K_M.gguf": (
        "bartowski/granite4-3b-instruct-GGUF",
        "granite4-3b-instruct-Q4_K_M.gguf",
    ),
    # Hermes 3 extended
    "Hermes-3-Llama-3.1-70B-Q4_K_M.gguf": (
        "bartowski/Hermes-3-Llama-3.1-70B-GGUF",
        "Hermes-3-Llama-3.1-70B-Q4_K_M.gguf",
    ),
    "Hermes-3-Llama-3.1-405B-Q4_K_M.gguf": (
        "bartowski/Hermes-3-Llama-3.1-405B-GGUF",
        "Hermes-3-Llama-3.1-405B-Q4_K_M.gguf",
    ),
    # Dolphin 3
    "dolphin-3.0-llama3.1-8b-Q4_K_M.gguf": (
        "bartowski/dolphin-3.0-llama3.1-8b-GGUF",
        "dolphin-3.0-llama3.1-8b-Q4_K_M.gguf",
    ),
    # Command R+
    "command-a-Q4_K_M.gguf": ("bartowski/command-a-GGUF", "command-a-Q4_K_M.gguf"),
    # OLMo 3
    "OLMo-3-7B-Instruct-Q4_K_M.gguf": (
        "bartowski/OLMo-3-7B-Instruct-GGUF",
        "OLMo-3-7B-Instruct-Q4_K_M.gguf",
    ),
    "OLMo-3-32B-Instruct-Q4_K_M.gguf": (
        "bartowski/OLMo-3-32B-Instruct-GGUF",
        "OLMo-3-32B-Instruct-Q4_K_M.gguf",
    ),
    "OLMo-3.1-32B-Instruct-Q4_K_M.gguf": (
        "bartowski/OLMo-3.1-32B-Instruct-GGUF",
        "OLMo-3.1-32B-Instruct-Q4_K_M.gguf",
    ),
    # EXAONE Deep
    "EXAONE-Deep-7.8B-Q4_K_M.gguf": (
        "bartowski/EXAONE-Deep-7.8B-GGUF",
        "EXAONE-Deep-7.8B-Q4_K_M.gguf",
    ),
    "EXAONE-Deep-32B-Q4_K_M.gguf": (
        "bartowski/EXAONE-Deep-32B-GGUF",
        "EXAONE-Deep-32B-Q4_K_M.gguf",
    ),
    # Nemotron extended
    "nemotron-cascade-2-Q4_K_M.gguf": (
        "bartowski/nemotron-cascade-2-GGUF",
        "nemotron-cascade-2-Q4_K_M.gguf",
    ),
    "nemotron-3-nano-4b-Q4_K_M.gguf": (
        "bartowski/nemotron-3-nano-4b-GGUF",
        "nemotron-3-nano-4b-Q4_K_M.gguf",
    ),
    # Ministral
    "Ministral-3B-Instruct-Q4_K_M.gguf": (
        "bartowski/Ministral-3B-Instruct-GGUF",
        "Ministral-3B-Instruct-Q4_K_M.gguf",
    ),
    "Ministral-8B-Instruct-Q4_K_M.gguf": (
        "bartowski/Ministral-8B-Instruct-GGUF",
        "Ministral-8B-Instruct-Q4_K_M.gguf",
    ),
    # Mistral Small 3.1 and 3.2
    "Mistral-Small-3.1-24B-Instruct-Q4_K_M.gguf": (
        "bartowski/Mistral-Small-3.1-24B-Instruct-GGUF",
        "Mistral-Small-3.1-24B-Instruct-Q4_K_M.gguf",
    ),
    "Mistral-Small-3.2-24B-Instruct-Q4_K_M.gguf": (
        "bartowski/Mistral-Small-3.2-24B-Instruct-GGUF",
        "Mistral-Small-3.2-24B-Instruct-Q4_K_M.gguf",
    ),
    # Devstral
    "Devstral-2-Q4_K_M.gguf": ("bartowski/Devstral-2-GGUF", "Devstral-2-Q4_K_M.gguf"),
    # StableLM
    "stablelm-2-1_6b-chat-Q4_K_M.gguf": (
        "bartowski/stablelm-2-1_6b-chat-GGUF",
        "stablelm-2-1_6b-chat-Q4_K_M.gguf",
    ),
    "stablelm-2-12b-chat-Q4_K_M.gguf": (
        "bartowski/stablelm-2-12b-chat-GGUF",
        "stablelm-2-12b-chat-Q4_K_M.gguf",
    ),
    "stablelm-zephyr-3b-Q4_K_M.gguf": (
        "bartowski/stablelm-zephyr-3b-GGUF",
        "stablelm-zephyr-3b-Q4_K_M.gguf",
    ),
    # Reader LM
    "reader-lm-0.5b-Q4_K_M.gguf": ("bartowski/reader-lm-0.5b-GGUF", "reader-lm-0.5b-Q4_K_M.gguf"),
    "reader-lm-1.5b-Q4_K_M.gguf": ("bartowski/reader-lm-1.5b-GGUF", "reader-lm-1.5b-Q4_K_M.gguf"),
    # Phi 2
    "phi-2-Q4_K_M.gguf": ("TheBloke/phi-2-GGUF", "phi-2.Q4_K_M.gguf"),
    # FunctionGemma
    "functiongemma-2b-Q4_K_M.gguf": (
        "bartowski/functiongemma-2b-GGUF",
        "functiongemma-2b-Q4_K_M.gguf",
    ),
    # ShieldGemma
    "shieldgemma-2b-Q4_K_M.gguf": ("bartowski/shieldgemma-2b-GGUF", "shieldgemma-2b-Q4_K_M.gguf"),
    "shieldgemma-9b-Q4_K_M.gguf": ("bartowski/shieldgemma-9b-GGUF", "shieldgemma-9b-Q4_K_M.gguf"),
    "shieldgemma-27b-Q4_K_M.gguf": (
        "bartowski/shieldgemma-27b-GGUF",
        "shieldgemma-27b-Q4_K_M.gguf",
    ),
    # Orca
    "orca-mini-3b-Q4_K_M.gguf": ("TheBloke/orca_mini_3B-GGUF", "orca_mini_3b.Q4_K_M.gguf"),
    "orca-mini-7b-Q4_K_M.gguf": ("TheBloke/orca_mini_7B-GGUF", "orca_mini_7b.Q4_K_M.gguf"),
    "orca-mini-13b-Q4_K_M.gguf": ("TheBloke/orca_mini_13B-GGUF", "orca_mini_13b.Q4_K_M.gguf"),
    "Orca-2-7b-Q4_K_M.gguf": ("TheBloke/Orca-2-7B-GGUF", "orca-2-7b.Q4_K_M.gguf"),
    "Orca-2-13b-Q4_K_M.gguf": ("TheBloke/Orca-2-13B-GGUF", "orca-2-13b.Q4_K_M.gguf"),
    # Llama 2 Chinese
    "Chinese-Llama-2-7B-Q4_K_M.gguf": (
        "TheBloke/Chinese-Llama-2-7B-GGUF",
        "chinese-llama-2-7b.Q4_K_M.gguf",
    ),
    "Chinese-Llama-2-13B-Q4_K_M.gguf": (
        "TheBloke/Chinese-Llama-2-13B-GGUF",
        "chinese-llama-2-13b.Q4_K_M.gguf",
    ),
    # YaRN extended context
    "Yarn-Llama-2-7B-128K-Q4_K_M.gguf": (
        "TheBloke/Yarn-Llama-2-7B-128K-GGUF",
        "yarn-llama-2-7b-128k.Q4_K_M.gguf",
    ),
    "Yarn-Llama-2-13B-128K-Q4_K_M.gguf": (
        "TheBloke/Yarn-Llama-2-13B-128K-GGUF",
        "yarn-llama-2-13b-128k.Q4_K_M.gguf",
    ),
    "Yarn-Mistral-7B-128K-Q4_K_M.gguf": (
        "TheBloke/Yarn-Mistral-7B-128k-GGUF",
        "yarn-mistral-7b-128k.Q4_K_M.gguf",
    ),
    # Samantha
    "samantha-mistral-7b-Q4_K_M.gguf": (
        "TheBloke/samantha-mistral-7B-GGUF",
        "samantha-mistral-7b.Q4_K_M.gguf",
    ),
    # Mistral OpenOrca
    "Mistral-7B-OpenOrca-Q4_K_M.gguf": (
        "TheBloke/Mistral-7B-OpenOrca-GGUF",
        "mistral-7b-openorca.Q4_K_M.gguf",
    ),
    # MistralLite
    "MistralLite-7B-Q4_K_M.gguf": ("TheBloke/MistralLite-7B-GGUF", "mistrallite-7b.Q4_K_M.gguf"),
    # NexusRaven
    "NexusRaven-V2-13B-Q4_K_M.gguf": (
        "TheBloke/NexusRaven-V2-13B-GGUF",
        "nexusraven-v2-13b.Q4_K_M.gguf",
    ),
    # Stable Beluga
    "StableBeluga-7B-Q4_K_M.gguf": ("TheBloke/StableBeluga-7B-GGUF", "stablebeluga-7b.Q4_K_M.gguf"),
    "StableBeluga2-70B-Q4_K_M.gguf": (
        "TheBloke/StableBeluga2-70B-GGUF",
        "stablebeluga2-70b.Q4_K_M.gguf",
    ),
    # Notus/Notux
    "notus-7b-v1-Q4_K_M.gguf": ("TheBloke/notus-7B-v1-GGUF", "notus-7b-v1.Q4_K_M.gguf"),
    "Notux-8x7B-v1-Q4_K_M.gguf": ("TheBloke/Notux-8x7B-v1-GGUF", "notux-8x7b-v1.Q4_K_M.gguf"),
    # Goliath
    "goliath-120b-Q4_K_M.gguf": ("TheBloke/goliath-120b-GGUF", "goliath-120b.Q4_K_M.gguf"),
    # XWinLM
    "Xwin-LM-7B-V0.2-Q4_K_M.gguf": ("TheBloke/Xwin-LM-7B-V0.2-GGUF", "xwin-lm-7b-v0.2.Q4_K_M.gguf"),
    "Xwin-LM-13B-V0.2-Q4_K_M.gguf": (
        "TheBloke/Xwin-LM-13B-V0.2-GGUF",
        "xwin-lm-13b-v0.2.Q4_K_M.gguf",
    ),
    # EverythingLM
    "EverythingLM-13B-16K-Q4_K_M.gguf": (
        "TheBloke/EverythingLM-13B-16K-GGUF",
        "everythinglm-13b-16k.Q4_K_M.gguf",
    ),
    # DuckDB NSQL
    "nsql-llama-2-7B-Q4_K_M.gguf": ("TheBloke/nsql-llama-2-7B-GGUF", "nsql-llama-2-7b.Q4_K_M.gguf"),
    # Medical LLMs
    "meditron-7B-Q4_K_M.gguf": ("TheBloke/meditron-7B-GGUF", "meditron-7b.Q4_K_M.gguf"),
    "meditron-70B-Q4_K_M.gguf": ("TheBloke/meditron-70B-GGUF", "meditron-70b.Q4_K_M.gguf"),
    "medllama2-7b-Q4_K_M.gguf": ("TheBloke/medllama-2-7B-GGUF", "medllama2-7b.Q4_K_M.gguf"),
    # Code Llama extended
    "CodeLlama-70b-Instruct-Q4_K_M.gguf": (
        "TheBloke/CodeLlama-70B-Instruct-GGUF",
        "codellama-70b-instruct.Q4_K_M.gguf",
    ),
    # Embedding models (for completeness - some may need special handling)
    "nomic-embed-text-v1.5-Q4_K_M.gguf": (
        "nomic-ai/nomic-embed-text-v1.5-GGUF",
        "nomic-embed-text-v1.5-Q4_K_M.gguf",
    ),
    "mxbai-embed-large-v1-Q4_K_M.gguf": (
        "mixedbread-ai/mxbai-embed-large-v1-GGUF",
        "mxbai-embed-large-v1-Q4_K_M.gguf",
    ),
    "bge-large-en-v1.5-Q4_K_M.gguf": (
        "bartowski/bge-large-en-v1.5-GGUF",
        "bge-large-en-v1.5-Q4_K_M.gguf",
    ),
    "bge-m3-Q4_K_M.gguf": ("bartowski/bge-m3-GGUF", "bge-m3-Q4_K_M.gguf"),
    # Granite Embedding
    "granite-embedding-30m-Q4_K_M.gguf": (
        "bartowski/granite-embedding-30m-english-GGUF",
        "granite-embedding-30m-english-Q4_K_M.gguf",
    ),
    "granite-embedding-125m-Q4_K_M.gguf": (
        "bartowski/granite-embedding-125m-english-GGUF",
        "granite-embedding-125m-english-Q4_K_M.gguf",
    ),
    # Qwen 3 Embedding
    "Qwen3-Embedding-0.6B-Q4_K_M.gguf": (
        "bartowski/Qwen3-Embedding-0.6B-GGUF",
        "Qwen3-Embedding-0.6B-Q4_K_M.gguf",
    ),
    "Qwen3-Embedding-8B-Q4_K_M.gguf": (
        "bartowski/Qwen3-Embedding-8B-GGUF",
        "Qwen3-Embedding-8B-Q4_K_M.gguf",
    ),
    # LFM2
    "lfm-2-24b-Q4_K_M.gguf": ("bartowski/lfm-2-24b-GGUF", "lfm-2-24b-Q4_K_M.gguf"),
    # TranslateGemma
    "translategemma-4b-Q4_K_M.gguf": (
        "bartowski/translategemma-4b-GGUF",
        "translategemma-4b-Q4_K_M.gguf",
    ),
    "translategemma-27b-Q4_K_M.gguf": (
        "bartowski/translategemma-27b-GGUF",
        "translategemma-27b-Q4_K_M.gguf",
    ),
    # GLM 4 extended
    "glm-4-9b-chat-1m-Q4_K_M.gguf": (
        "bartowski/glm-4-9b-chat-1m-GGUF",
        "glm-4-9b-chat-1m-Q4_K_M.gguf",
    ),
    # DeepSeek OCR
    "deepseek-ocr-3b-Q4_K_M.gguf": (
        "bartowski/deepseek-ocr-3b-GGUF",
        "deepseek-ocr-3b-Q4_K_M.gguf",
    ),
    # Aya 23 extended
    "aya-23-8B-Q4_K_M.gguf": ("bartowski/aya-23-8B-GGUF", "aya-23-8B-Q4_K_M.gguf"),
    "aya-23-35B-Q4_K_M.gguf": ("bartowski/aya-23-35B-GGUF", "aya-23-35B-Q4_K_M.gguf"),
    # Qwen 1.5
    "Qwen1.5-0.5B-Chat-Q4_K_M.gguf": (
        "bartowski/Qwen1.5-0.5B-Chat-GGUF",
        "Qwen1.5-0.5B-Chat-Q4_K_M.gguf",
    ),
    "Qwen1.5-1.8B-Chat-Q4_K_M.gguf": (
        "bartowski/Qwen1.5-1.8B-Chat-GGUF",
        "Qwen1.5-1.8B-Chat-Q4_K_M.gguf",
    ),
    "Qwen1.5-4B-Chat-Q4_K_M.gguf": (
        "bartowski/Qwen1.5-4B-Chat-GGUF",
        "Qwen1.5-4B-Chat-Q4_K_M.gguf",
    ),
    "Qwen1.5-7B-Chat-Q4_K_M.gguf": (
        "bartowski/Qwen1.5-7B-Chat-GGUF",
        "Qwen1.5-7B-Chat-Q4_K_M.gguf",
    ),
    "Qwen1.5-14B-Chat-Q4_K_M.gguf": (
        "bartowski/Qwen1.5-14B-Chat-GGUF",
        "Qwen1.5-14B-Chat-Q4_K_M.gguf",
    ),
    "Qwen1.5-32B-Chat-Q4_K_M.gguf": (
        "bartowski/Qwen1.5-32B-Chat-GGUF",
        "Qwen1.5-32B-Chat-Q4_K_M.gguf",
    ),
    "Qwen1.5-72B-Chat-Q4_K_M.gguf": (
        "bartowski/Qwen1.5-72B-Chat-GGUF",
        "Qwen1.5-72B-Chat-Q4_K_M.gguf",
    ),
    "Qwen1.5-110B-Chat-Q4_K_M.gguf": (
        "bartowski/Qwen1.5-110B-Chat-GGUF",
        "Qwen1.5-110B-Chat-Q4_K_M.gguf",
    ),
}


def get_existing_gcs_files() -> set[str]:
    """Get list of files already in GCS bucket."""
    result = subprocess.run(
        ["gcloud", "storage", "ls", GCS_GGUF_PATH + "/"], capture_output=True, text=True
    )
    files = set()
    for line in result.stdout.strip().split("\n"):
        if line:
            filename = line.split("/")[-1]
            if filename:
                files.add(filename)
    return files


def download_from_huggingface(
    repo: str, filename: str, output_path: Path, quiet: bool = False
) -> bool:
    """Download a file from HuggingFace using httpx (faster than curl subprocess)."""
    url = f"https://huggingface.co/{repo}/resolve/main/{filename}"
    if not quiet:
        safe_print(f"  Downloading from: {url}")

    try:
        # Use HTTP/2 for better performance and connection multiplexing
        with httpx.Client(
            follow_redirects=True,
            timeout=httpx.Timeout(30.0, read=600.0),  # 10min read timeout for large files
            http2=True,
        ) as client:
            with client.stream("GET", url) as response:
                if response.status_code != 200:
                    if not quiet:
                        safe_print(f"  [ERROR] HTTP {response.status_code}")
                    return False

                total = int(response.headers.get("content-length", 0))
                downloaded = 0

                # Use buffered writes for better I/O performance
                with open(output_path, "wb", buffering=WRITE_BUFFER_SIZE) as f:
                    for chunk in response.iter_bytes(chunk_size=CHUNK_SIZE):
                        f.write(chunk)
                        downloaded += len(chunk)

                        # Progress reporting every 100MB if not quiet
                        if (
                            not quiet
                            and total > 0
                            and downloaded % (100 * 1024 * 1024) < CHUNK_SIZE
                        ):
                            pct = (downloaded / total) * 100
                            safe_print(f"  Progress: {pct:.1f}% ({downloaded // (1024 * 1024)} MB)")

        return output_path.exists() and output_path.stat().st_size > 0

    except Exception as e:
        if not quiet:
            safe_print(f"  [ERROR] Download failed: {e}")
        return False


def upload_to_gcs(local_path: Path, filename: str, quiet: bool = False) -> bool:
    """Upload a file to GCS."""
    gcs_path = f"{GCS_GGUF_PATH}/{filename}"
    if not quiet:
        safe_print(f"  Uploading to: {gcs_path}")

    result = subprocess.run(
        ["gcloud", "storage", "cp", str(local_path), gcs_path], capture_output=True, text=True
    )

    return result.returncode == 0


def stream_to_gcs(repo: str, hf_filename: str, gcs_filename: str, quiet: bool = False) -> bool:
    """Stream directly from HuggingFace to GCS without intermediate temp file.

    This avoids disk I/O entirely by piping the download directly to gsutil.
    Best for environments with limited disk space or when disk I/O is a bottleneck.
    """
    url = f"https://huggingface.co/{repo}/resolve/main/{hf_filename}"
    gcs_path = f"{GCS_GGUF_PATH}/{gcs_filename}"

    if not quiet:
        safe_print(f"  Streaming: {url} -> {gcs_path}")

    try:
        # Use curl to stream to gsutil (gsutil supports stdin via -)
        # This avoids writing to disk entirely
        curl_proc = subprocess.Popen(
            ["curl", "-sL", url], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        gsutil_proc = subprocess.Popen(
            ["gcloud", "storage", "cp", "-", gcs_path],
            stdin=curl_proc.stdout,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # Allow curl to receive SIGPIPE if gsutil exits
        curl_proc.stdout.close()

        _, gsutil_err = gsutil_proc.communicate()
        curl_proc.wait()

        if gsutil_proc.returncode != 0:
            if not quiet:
                safe_print(f"  [ERROR] Stream upload failed: {gsutil_err.decode()}")
            return False

        return True

    except Exception as e:
        if not quiet:
            safe_print(f"  [ERROR] Stream failed: {e}")
        return False


def sync_model(
    filename: str,
    repo: str,
    hf_filename: str,
    existing: set[str],
    dry_run: bool = False,
    worker_id: int = 0,
    quiet: bool = False,
    stream_mode: bool = False,
) -> tuple[str, bool, str]:
    """Sync a single model to GCS. Returns (filename, success, message).

    Args:
        stream_mode: If True, stream directly to GCS without temp file (faster, less disk I/O).
    """
    prefix = f"[W{worker_id}]" if worker_id > 0 else ""

    if filename in existing:
        msg = f"{prefix} [SKIP] Already in GCS: {filename}"
        if not quiet:
            safe_print(msg)
        return (filename, True, "skipped")

    if dry_run:
        msg = f"{prefix} [DRY-RUN] Would download and upload: {filename}"
        safe_print(msg)
        return (filename, True, "dry-run")

    # Use streaming mode if enabled (bypasses disk I/O)
    if stream_mode:
        safe_print(f"{prefix} Streaming {filename}...")
        if stream_to_gcs(repo, hf_filename, filename, quiet=True):
            safe_print(f"{prefix} [OK] Streamed: {filename}")
            return (filename, True, "streamed")
        else:
            safe_print(f"{prefix} [ERROR] Stream failed: {filename}")
            return (filename, False, "stream_failed")

    # Standard mode: download to temp, then upload
    with tempfile.TemporaryDirectory() as tmpdir:
        local_path = Path(tmpdir) / filename

        safe_print(f"{prefix} Downloading {filename}...")
        if not download_from_huggingface(repo, hf_filename, local_path, quiet=True):
            safe_print(f"{prefix} [ERROR] Download failed: {filename}")
            return (filename, False, "download_failed")

        size_gb = local_path.stat().st_size / (1024**3)
        safe_print(f"{prefix} Downloaded {filename} ({size_gb:.2f} GB), uploading...")

        if not upload_to_gcs(local_path, filename, quiet=True):
            safe_print(f"{prefix} [ERROR] Upload failed: {filename}")
            return (filename, False, "upload_failed")

        safe_print(f"{prefix} [OK] Synced: {filename} ({size_gb:.2f} GB)")
        return (filename, True, "synced")


def sync_models_parallel(
    models: list[tuple[str, str, str]],
    existing: set[str],
    workers: int,
    dry_run: bool = False,
    stream_mode: bool = False,
) -> tuple[int, int]:
    """Sync multiple models in parallel. Returns (success_count, failed_count)."""
    # Filter out already existing models
    missing = [(f, r, hf) for f, r, hf in models if f not in existing]
    skipped = len(models) - len(missing)

    if skipped > 0:
        safe_print(f"Skipping {skipped} models already in GCS")

    if not missing:
        return (skipped, 0)

    total = len(missing)
    mode_str = "streaming" if stream_mode else "download+upload"
    safe_print(f"\nSyncing {total} models with {workers} parallel workers ({mode_str})...")
    safe_print("=" * 60)

    success = skipped
    failed = 0
    completed = 0

    with ThreadPoolExecutor(max_workers=workers) as executor:
        # Submit all jobs with worker IDs
        futures = {}
        for i, (filename, repo, hf_filename) in enumerate(missing):
            worker_id = (i % workers) + 1
            future = executor.submit(
                sync_model,
                filename,
                repo,
                hf_filename,
                set(),
                dry_run,
                worker_id,
                False,
                stream_mode,  # Pass empty set since we already filtered
            )
            futures[future] = filename

        # Process results as they complete
        for future in as_completed(futures):
            filename = futures[future]
            completed += 1
            try:
                _, ok, status = future.result()
                if ok:
                    success += 1
                else:
                    failed += 1
                # Progress update every 5 completions
                if completed % 5 == 0 or completed == total:
                    safe_print(
                        f"--- Progress: {completed}/{total} ({success - skipped} synced, {failed} failed) ---"
                    )
            except Exception as e:
                safe_print(f"[ERROR] Exception syncing {filename}: {e}")
                failed += 1

    return (success, failed)


def main():
    parser = argparse.ArgumentParser(description="Sync AI models to GCS for SAGE")
    parser.add_argument("--all", action="store_true", help="Sync all models")
    parser.add_argument("--model", type=str, help="Sync models matching pattern")
    parser.add_argument("--list", action="store_true", help="List what would be synced")
    parser.add_argument("--dry-run", action="store_true", help="Don't actually download/upload")
    parser.add_argument(
        "--workers",
        "-w",
        type=int,
        default=1,
        help="Number of parallel workers (default: 1, recommended: 3-6)",
    )
    parser.add_argument(
        "--small-first",
        action="store_true",
        help="Process smaller models first (faster initial progress)",
    )
    parser.add_argument(
        "--stream",
        action="store_true",
        help="Stream directly to GCS without temp files (faster, less disk I/O)",
    )
    args = parser.parse_args()

    if not (args.all or args.model or args.list):
        parser.print_help()
        return

    print("Checking existing GCS files...", flush=True)
    existing = get_existing_gcs_files()
    print(f"Found {len(existing)} files already in GCS", flush=True)

    # Filter models to sync
    models_to_sync = []
    for filename, (repo, hf_filename) in HUGGINGFACE_SOURCES.items():
        if args.all or (args.model and args.model.lower() in filename.lower()):
            models_to_sync.append((filename, repo, hf_filename))

    missing = [m for m in models_to_sync if m[0] not in existing]

    print(f"\nModels to sync: {len(models_to_sync)}")
    print(f"Already in GCS: {len(models_to_sync) - len(missing)}")
    print(f"Missing: {len(missing)}")

    if args.list:
        print("\nMissing models:")
        for filename, _, _ in missing:
            print(f"  - {filename}")
        return

    if not missing:
        print("\nAll models already synced!")
        return

    # Sort by estimated size if --small-first
    if args.small_first:

        def estimate_size(filename):
            # Rough size estimates based on model name patterns
            name = filename.lower()
            if "405b" in name:
                return 200
            if "120b" in name or "110b" in name:
                return 70
            if "70b" in name or "72b" in name:
                return 40
            if "34b" in name or "33b" in name or "35b" in name or "32b" in name:
                return 20
            if "22b" in name or "20b" in name or "27b" in name:
                return 15
            if "13b" in name or "14b" in name:
                return 8
            if "8b" in name or "7b" in name or "9b" in name:
                return 4
            if "3b" in name or "4b" in name:
                return 2
            if "1b" in name or "1.5b" in name or "2b" in name:
                return 1
            return 5  # default

        models_to_sync = sorted(models_to_sync, key=lambda x: estimate_size(x[0]))
        print("Sorted models by estimated size (smallest first)")

    # Use parallel sync if workers > 1
    if args.workers > 1:
        success, failed = sync_models_parallel(
            models_to_sync, existing, args.workers, args.dry_run, args.stream
        )
    else:
        # Sequential sync (original behavior)
        mode_str = "streaming" if args.stream else "download+upload"
        print(f"\nSyncing {len(missing)} models (sequential, {mode_str})...")
        success = 0
        failed = 0

        for i, (filename, repo, hf_filename) in enumerate(missing, 1):
            print(f"\n[{i}/{len(missing)}] {filename}")
            _, ok, _ = sync_model(
                filename, repo, hf_filename, existing, args.dry_run, stream_mode=args.stream
            )
            if ok:
                success += 1
            else:
                failed += 1

    print(f"\n{'=' * 60}")
    print(f"Sync complete: {success} succeeded, {failed} failed")
    if args.workers > 1:
        print(f"Used {args.workers} parallel workers")
    if args.stream:
        print("Used streaming mode (direct HuggingFace → GCS)")


if __name__ == "__main__":
    main()
