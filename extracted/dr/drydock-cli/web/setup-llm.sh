#!/usr/bin/env bash
# Gemma 4 + llama.cpp one-command setup for drydock.
#
# What this does:
#   1. Downloads the Gemma 4 GGUF from Unsloth (HuggingFace), ~13 GB
#   2. Pulls the official llama.cpp server-cuda image (~2 GB)
#   3. Starts the server on port 8000 with the load-bearing flags
#      (--jinja, q8 KV cache, full-layer GPU offload)
#
# Requirements:
#   - docker + nvidia-container-toolkit (so containers see the GPU)
#   - a GPU with >=16 GB VRAM, OR lower CONTEXT (e.g. 16384)
#   - ~15 GB free disk for the GGUF
#
# Idempotent: re-running re-uses the cached model and replaces the
# running container in place.
#
# Usage:
#   ./setup-llm.sh                       # defaults: Q3_K_M, 32k context, port 8000
#   QUANT=Q4_K_M ./setup-llm.sh          # higher quality, slower (~17 GB)
#   VISION=1 ./setup-llm.sh              # also download mmproj for image input
#   PORT=8001 ./setup-llm.sh             # different host port
#   MODEL_DIR=/data/llms ./setup-llm.sh  # cache GGUF elsewhere
#
# One-liner from a fresh box:
#   curl -sSL https://drydock.pages.dev/setup-llm.sh | bash
#
# Then point drydock at it:
#   export DRYDOCK_LOCAL_URL=http://localhost:8000/v1
#   drydock

set -euo pipefail

QUANT="${QUANT:-Q3_K_M}"
VISION="${VISION:-0}"
PORT="${PORT:-8000}"
CONTEXT="${CONTEXT:-32768}"
CONTAINER="${CONTAINER:-llamacpp-gemma4}"
MODEL_DIR="${MODEL_DIR:-$HOME/.cache/drydock/models}"

MODEL_FILE="gemma-4-26B-A4B-it-UD-${QUANT}.gguf"
MMPROJ_FILE="mmproj-F16.gguf"
HF_BASE="https://huggingface.co/unsloth/gemma-4-26B-A4B-it-GGUF/resolve/main"

# --- preflight ---

if ! command -v docker >/dev/null 2>&1; then
    echo "ERROR: docker not found. Install Docker first: https://docs.docker.com/engine/install/" >&2
    exit 1
fi
if ! docker info 2>/dev/null | grep -q "Runtimes:.*nvidia"; then
    echo "WARNING: nvidia container runtime not detected — GPU may not be accessible."
    echo "         Install: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/"
    echo
fi
if ! command -v curl >/dev/null 2>&1; then
    echo "ERROR: curl is required to download the model." >&2
    exit 1
fi

mkdir -p "$MODEL_DIR"

# --- download model (resumable, idempotent) ---

if [ -f "$MODEL_DIR/$MODEL_FILE" ]; then
    echo "==> $MODEL_FILE already cached at $MODEL_DIR (skipping download)"
else
    echo "==> Downloading $MODEL_FILE (~13 GB, one-time, resumable)..."
    # curl -C - resumes a partial download
    curl -fL -C - -o "$MODEL_DIR/$MODEL_FILE.partial" "$HF_BASE/$MODEL_FILE"
    mv "$MODEL_DIR/$MODEL_FILE.partial" "$MODEL_DIR/$MODEL_FILE"
    echo "==> Done."
fi

if [ "$VISION" = "1" ]; then
    if [ -f "$MODEL_DIR/$MMPROJ_FILE" ]; then
        echo "==> $MMPROJ_FILE already cached (skipping)"
    else
        echo "==> Downloading $MMPROJ_FILE (~1.2 GB) for vision support..."
        curl -fL -C - -o "$MODEL_DIR/$MMPROJ_FILE.partial" "$HF_BASE/$MMPROJ_FILE"
        mv "$MODEL_DIR/$MMPROJ_FILE.partial" "$MODEL_DIR/$MMPROJ_FILE"
    fi
fi

# --- stop existing container (so re-runs are idempotent) ---

if docker ps -a --format '{{.Names}}' | grep -qx "$CONTAINER"; then
    echo "==> Replacing existing container $CONTAINER..."
    docker stop "$CONTAINER" >/dev/null 2>&1 || true
    docker rm "$CONTAINER" >/dev/null 2>&1 || true
fi

# --- start server ---

vision_args=()
if [ "$VISION" = "1" ]; then
    vision_args=(--mmproj "/models/$MMPROJ_FILE")
fi

echo "==> Pulling llama.cpp image (cached after first run)..."
docker pull -q ghcr.io/ggml-org/llama.cpp:server-cuda

echo "==> Starting server on port $PORT..."
docker run -d \
    --gpus all \
    --name "$CONTAINER" \
    --restart unless-stopped \
    -p "$PORT:8000" \
    -v "$MODEL_DIR:/models:ro" \
    ghcr.io/ggml-org/llama.cpp:server-cuda \
    -m "/models/$MODEL_FILE" \
    --host 0.0.0.0 --port 8000 \
    -ngl 99 -c "$CONTEXT" -np 1 \
    --jinja \
    -ctk q8_0 -ctv q8_0 \
    --alias gemma4 \
    "${vision_args[@]}" >/dev/null

# --- wait for ready ---

echo -n "==> Waiting for server to come up"
for _ in $(seq 1 60); do
    if curl -sf "http://localhost:$PORT/v1/models" >/dev/null 2>&1; then
        echo " ready."
        echo
        echo "Live at: http://localhost:$PORT/v1/"
        echo
        echo "Point drydock at it:"
        echo "  export DRYDOCK_LOCAL_URL=http://localhost:$PORT/v1"
        echo "  export DRYDOCK_LOCAL_MODEL=gemma4"
        echo "  drydock"
        echo
        echo "Stop the server:   docker stop $CONTAINER"
        echo "Restart it:        docker start $CONTAINER"
        echo "View logs:         docker logs -f $CONTAINER"
        exit 0
    fi
    echo -n "."
    sleep 2
done
echo
echo "ERROR: server didn't respond in 120s. Check logs:" >&2
echo "  docker logs $CONTAINER" >&2
exit 1
