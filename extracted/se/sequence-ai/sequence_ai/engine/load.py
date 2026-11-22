# SPDX-FileCopyrightText: Copyright (c) 2026 General Sequences Company
# SPDX-License-Identifier: Apache-2.0
"""
A model's weights read onto the GPU from one contiguous file in large parallel reads, in place of a checkpoint read
tensor by tensor (fast loading): the same bytes, in about half the time from a cold disk.

    from sequence_ai.engine import load

    load.pack_from("checkpoint/", "model.load")              # once: a safetensors, .pth or orbax checkpoint, packed
    weights = load.load("model.load", device="cuda")          # {name: torch tensor}, on the GPU
    params = load.load("model.load", device="cuda", to="jax") # {name: JAX array}, in JAX's own memory
    tree = load.nest(params)                                  # an orbax checkpoint's tree again: {"a": {"b": ...}}

    load.pack(state_dict, "model.load", dtype="bfloat16")     # any {name: tensor or array}, floats in the dtype given

In one sentence: pack writes the tensors grouped by dtype, each group one block of the file aligned to 4096 bytes,
after a header that names each tensor's block, offset, dtype and shape → load reads the header, allocates one buffer a
block on the device, and splits the blocks into 64 MiB chunks → several threads each read a chunk into a pinned buffer
of their own - through the page cache, or with O_DIRECT where the chunk is not in it and memory cannot hold what the
file lacks there - and copy it to
the GPU on a stream of their own, reading the next chunk while the last one copies → once every copy is done, each
tensor is a view of its block's buffer: the bytes that were packed.

WHY one contiguous file: a checkpoint read tensor by tensor opens, parses and copies each one in turn, and one thread
reading a disk leaves it half used; a few long reads of one file in parallel keep the disk busy to its limit.
WHY through the page cache unless memory cannot hold the file: read in parallel, a cold file comes through it as fast
as with O_DIRECT and stays there for the next load (gr00t-droid's 6.9 GB on an L4: 13.0 s cold either way, then 0.56 s
through the cache, and 13.0 s again after O_DIRECT, which leaves nothing there).
WHY O_DIRECT chunk by chunk where memory cannot hold it, never for the whole file: the chunks the cache holds are read
through it at memory speed, and the others from the disk past it, so a file partly in memory - a large model on a
smaller machine - keeps that part, which a decision taken for the whole file would lose. Where the kernel says nothing
is cached but a sampled read runs at memory speed (some containers' memory accounting hides the cache), every chunk is
read through the page cache.
WHY one buffer a dtype: the tensors are views of it, so the load is a handful of allocations and no copy after the
read; a block's dtype is every tensor's in it, so each view is a plain slice.
WHY pack can cast: a model kept in float32 on disk that runs in bfloat16 reads half the bytes from a
file packed in bfloat16, and loads what it would have cast to anyway.
WHY a JAX load is read into memory and then put on the GPU, never into buffers torch holds there: JAX takes most of
the GPU's memory for its own pool when it starts, which a policy does before it loads its weights, and buffers torch
allocates beside that pool run out (pi0.5's 6.25 GiB on an L4, with 5.31 GiB left); the disk is the slow part of a
load either way, and each array put on the device is one copy at the bus's speed.
WHY buffers in memory start at a multiple of 4096 bytes: a read with O_DIRECT lands only in an aligned buffer, and a
large numpy allocation starts just past a page's start.

The tensors read back are the packed ones byte for byte. On a machine with no CUDA GPU, load reads into memory with
the same threads (device="cpu"). torch is needed for a torch load onto a GPU, JAX for a JAX one; numpy alone for one
into memory.

Adapted from fal-ai/flashpack src/flashpack/parallel_read.py (MIT), with its src/flashpack/serialization.py and
src/flashpack/constants.py: see THIRD_PARTY_NOTICES.md. Changed here: the file's own header and layout; whether to read
through the page cache decided for each chunk, from the pages the kernel holds, in place of once for the whole file; JAX
arrays, put on the device from memory; checkpoints read from safetensors, .pth and orbax.
"""
from __future__ import annotations

import ctypes
import json
import mmap as _mmap
import os
import queue
import struct
import sys
import threading
import time
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping, Optional

__all__ = ["pack", "pack_from", "load", "nest", "read_checkpoint", "header", "MAGIC", "SUFFIX"]

MAGIC = b"SEQLOAD1"           # the first 8 bytes of a packed file
SUFFIX = ".load"
FORMAT = "sequence-ai-load-1"
ALIGN = 4096                  # each block's place in the file: O_DIRECT's alignment
TENSOR_ALIGN = 128            # each tensor's place in its block
CHUNK = 64 << 20              # the bytes one read moves
THREADS = 16                  # readers: a disk's queue depth, not a CPU budget
RESIDENT = 0.9                # a chunk this much in the page cache is in it
SPARE = 1 << 30               # memory left over once the cache holds what a file lacks there
SAMPLE_BYTES = 16 << 20       # each sampled read, when the kernel says nothing is cached
HOT_GBPS = 5.0                # a sampled read faster than this is from memory

# a dtype's name in the header: its element's bytes and numpy's name for it, where it has one
_DTYPES = {
    "float64": (8, "float64"), "float32": (4, "float32"), "float16": (2, "float16"), "bfloat16": (2, None),
    "int64": (8, "int64"), "int32": (4, "int32"), "int16": (2, "int16"), "int8": (1, "int8"), "uint8": (1, "uint8"),
    "bool": (1, "bool"), "float8_e4m3fn": (1, None), "float8_e5m2": (1, None), "uint16": (2, "uint16"),
    "uint32": (4, "uint32"), "uint64": (8, "uint64"), "complex64": (8, "complex64"),
}


# ── packing ─────────────────────────────────────────────────────────────────────────────────────────────────────────
def pack(tensors: Mapping[str, Any], path: str | os.PathLike, *, dtype: Optional[str] = None) -> dict:
    """`tensors` ({name: torch tensor, numpy or JAX array}) written to one file at `path`: each dtype's tensors in one
    block, the largest first, `dtype` (a name: "bfloat16", "float16", "float32") the dtype every floating-point one is
    written in when it is given. The header it wrote."""
    items = {str(name): _host(value, dtype) for name, value in tensors.items()}
    if not items:
        raise ValueError("pack: no tensors to write")
    by_dtype: dict[str, list] = {}
    for name in sorted(items, key=lambda n: -len(items[n][2])):
        by_dtype.setdefault(items[name][0], []).append(name)
    blocks, records = [], []
    for index, (kind, names) in enumerate(by_dtype.items()):
        offset = 0
        for name in names:
            offset = _up(offset, TENSOR_ALIGN)
            records.append({"name": name, "dtype": kind, "shape": list(items[name][1]), "block": index,
                            "offset": offset, "bytes": len(items[name][2])})
            offset += len(items[name][2])
        blocks.append({"dtype": kind, "bytes": offset, "offset": 10 ** 15})  # a placeholder as wide as any offset
    head = {"format": FORMAT, "blocks": blocks, "tensors": records}
    cursor = _up(16 + len(json.dumps(head, separators=(",", ":"))), ALIGN)  # where the data starts, past the header
    for block in blocks:
        block["offset"] = cursor = _up(cursor, ALIGN)
        cursor += block["bytes"]
    text = json.dumps(head, separators=(",", ":")).encode()
    text += b" " * (blocks[0]["offset"] - 16 - len(text))              # the header padded to the first block
    path = Path(path)
    part = path.with_name(f".{path.name}.{os.getpid()}.part")
    with open(part, "wb") as f:
        f.write(MAGIC + struct.pack("<Q", len(text)) + text)
        for record in records:
            f.seek(blocks[record["block"]]["offset"] + record["offset"])
            f.write(items[record["name"]][2])
        f.truncate(cursor)
        f.flush()
        os.fsync(f.fileno())
    os.replace(part, path)
    return head


def pack_from(source: str | os.PathLike, path: str | os.PathLike, *, dtype: Optional[str] = None) -> dict:
    """A checkpoint - a safetensors file or a folder of them, a .pth/.pt/.bin file, an orbax checkpoint folder - packed
    to `path` (pack): the header it wrote."""
    return pack(read_checkpoint(source), path, dtype=dtype)


def read_checkpoint(source: str | os.PathLike) -> dict:
    """A checkpoint's tensors by name, as its own format reads them: safetensors (a file, or each in a folder), a
    torch file (.pth, .pt, .bin; its state_dict, its nested dicts' names joined by "."), or orbax (a folder holding
    _METADATA or a checkpoint; its names joined by "/"). ValueError for anything else."""
    source = Path(source)
    if source.is_dir():
        shards = sorted(source.glob("*.safetensors"))
        if shards:
            out: dict = {}
            for shard in shards:
                out.update(_safetensors(shard))
            return out
        if (source / "_METADATA").exists() or (source / "checkpoint").exists() or \
                (source / "manifest.ocdbt").exists() or (source / "_CHECKPOINT_METADATA").exists():
            return _orbax(source)
        raise ValueError(f"{source}: no safetensors file and no orbax checkpoint in it")
    if source.suffix == ".safetensors":
        return _safetensors(source)
    if source.suffix in (".pth", ".pt", ".bin", ".ckpt"):
        return _torch_file(source)
    raise ValueError(f"{source}: a .safetensors, .pth, .pt or .bin file, or a folder of safetensors or orbax")


def _safetensors(path: Path) -> dict:
    from safetensors import safe_open

    with safe_open(str(path), framework="pt") as f:
        return {name: f.get_tensor(name) for name in f.keys()}


def _torch_file(path: Path) -> dict:
    import torch

    state = torch.load(str(path), map_location="cpu", weights_only=True)
    for key in ("state_dict", "model", "module"):
        if isinstance(state, dict) and isinstance(state.get(key), dict) and len(state) <= 4:
            state = state[key]
            break
    return dict(_flat(state, "."))


def _orbax(path: Path) -> dict:
    """An orbax PyTree checkpoint restored into memory as numpy arrays."""
    import jax
    import numpy as np
    import orbax.checkpoint as ocp

    with ocp.PyTreeCheckpointer() as checkpointer:
        metadata = checkpointer.metadata(str(path))
        tree = getattr(metadata, "item_metadata", None) or getattr(metadata, "tree", None) or metadata
        restore_args = jax.tree.map(lambda _: ocp.ArrayRestoreArgs(restore_type=np.ndarray), tree)
        restored = checkpointer.restore(str(path), ocp.args.PyTreeRestore(item=tree, restore_args=restore_args))
    return dict(_flat(restored, "/"))


def _flat(tree: Any, sep: str, prefix: str = "") -> Iterable[tuple[str, Any]]:
    if isinstance(tree, Mapping):
        for key, value in tree.items():
            yield from _flat(value, sep, f"{prefix}{sep}{key}" if prefix else str(key))
    elif tree is not None:
        yield prefix, tree


def _host(value: Any, dtype: Optional[str]) -> tuple[str, tuple, bytes]:
    """One tensor as (its dtype's name, its shape, its bytes in C order), floats cast to `dtype` when given."""
    torch = sys.modules.get("torch")
    if torch is not None and isinstance(value, torch.Tensor):
        tensor = value.detach()
        if dtype and tensor.is_floating_point():
            tensor = tensor.to(getattr(torch, dtype))
        tensor = tensor.contiguous().cpu()
        kind = str(tensor.dtype).replace("torch.", "")
        return kind, tuple(tensor.shape), tensor.reshape(-1).view(torch.uint8).numpy().tobytes()
    import numpy as np

    array = np.asarray(value)
    kind = _numpy_name(array.dtype)
    if dtype and (array.dtype.kind == "f" or kind in ("bfloat16", "float8_e4m3fn", "float8_e5m2")):
        array, kind = _cast(array, dtype), dtype
    return kind, tuple(array.shape), np.ascontiguousarray(array).tobytes()


def _numpy_name(dtype: Any) -> str:
    name = str(dtype)
    if name in _DTYPES:
        return name
    raise ValueError(f"pack: a dtype it cannot write: {name}")


def _cast(array: Any, dtype: str) -> Any:
    """A numpy array cast to `dtype`, bfloat16 by ml_dtypes (which JAX installs)."""
    import numpy as np

    if dtype == "bfloat16":
        import ml_dtypes

        return array.astype(ml_dtypes.bfloat16)
    return array.astype(np.dtype(dtype))


def _up(value: int, align: int) -> int:
    return (value + align - 1) // align * align


# ── reading ─────────────────────────────────────────────────────────────────────────────────────────────────────────
def header(path: str | os.PathLike) -> dict:
    """A packed file's header: its blocks and each tensor's name, dtype, shape, block and offset. ValueError for a file
    that is not one."""
    with open(path, "rb") as f:
        head = f.read(16)
        if len(head) < 16 or head[:8] != MAGIC:
            raise ValueError(f"{path}: not a packed weights file")
        (length,) = struct.unpack("<Q", head[8:16])
        found = json.loads(f.read(length))
    if found.get("format") != FORMAT:
        raise ValueError(f"{path}: a packed file of another format ({found.get('format')})")
    return found


def load(path: str | os.PathLike, *, device: str = "cuda", to: str = "torch", threads: int = THREADS,
         chunk: int = CHUNK, say: Optional[Callable[[str], Any]] = None) -> dict:
    """The tensors of the packed file at `path`, by name: on `device` ("cuda", "cuda:1", "cpu") as torch tensors
    (`to` "torch"), each a view of one buffer its dtype's tensors share; as JAX arrays there (`to` "jax"), read into
    memory and put on the device; or as numpy arrays in memory (`to` "numpy"). `say`, when given, is told how long the
    read took and how much went through the page cache."""
    if to not in ("torch", "jax", "numpy"):
        raise ValueError(f"load: to={to!r}: \"torch\", \"jax\" or \"numpy\"")
    path = os.fspath(path)
    head = header(path)
    started = time.perf_counter()
    if to == "torch":
        out, cached = _read_torch(path, head, device, threads, chunk)
    else:
        out, cached = _read_numpy(path, head, threads, chunk)
        if to == "jax":
            out = _put_jax(out, device)
    if say is not None:
        size = sum(block["bytes"] for block in head["blocks"])
        said = f"{size / 1e9:.2f} GB in {time.perf_counter() - started:.1f} s"
        say(f"load: {path}: {said}, {cached:.0%} of it through the page cache")
    return out


def nest(flat: Mapping[str, Any], sep: str = "/") -> dict:
    """{"a/b/c": x} as {"a": {"b": {"c": x}}}: a checkpoint's tree again from the names read_checkpoint gave its
    tensors (orbax's joined by "/", a torch file's by ".")."""
    out: dict = {}
    for name, value in flat.items():
        node = out
        *parents, leaf = name.split(sep)
        for part in parents:
            node = node.setdefault(part, {})
        node[leaf] = value
    return out


def _plan(head: dict, chunk: int) -> list[tuple[int, int, int, int]]:
    """(block, file offset, offset in the block, bytes) for every chunk: each a block's head up to the next 4096-byte
    boundary, then whole chunks, so every chunk after a head starts aligned for O_DIRECT."""
    chunks = []
    for index, block in enumerate(head["blocks"]):
        done, left = 0, block["bytes"]
        lead = min((-block["offset"]) % ALIGN, left)
        if lead:
            chunks.append((index, block["offset"], 0, lead))
            done, left = lead, left - lead
        while left > 0:
            size = min(chunk, left)
            chunks.append((index, block["offset"] + done, done, size))
            done, left = done + size, left - size
    return chunks


def _resident(path: str, size: int) -> Optional[Any]:
    """Which of the file's pages the page cache holds (a numpy array of 0 and 1, a page each); None where the kernel
    cannot say."""
    if size == 0 or not hasattr(_mmap, "MAP_PRIVATE"):
        return None
    try:
        import numpy as np

        fd = os.open(path, os.O_RDONLY)
        try:
            mapped = _mmap.mmap(fd, size, flags=_mmap.MAP_PRIVATE, prot=_mmap.PROT_READ | _mmap.PROT_WRITE)
        finally:
            os.close(fd)
        try:
            pages = (size + _mmap.PAGESIZE - 1) // _mmap.PAGESIZE
            vector = (ctypes.c_ubyte * pages)()
            view = (ctypes.c_char * size).from_buffer(mapped)
            libc = ctypes.CDLL(None, use_errno=True)
            # 64-bit addresses: without these types ctypes passes the address as a C int, and mincore fails
            libc.mincore.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_ubyte)]
            libc.mincore.restype = ctypes.c_int
            if libc.mincore(ctypes.c_void_p(ctypes.addressof(view)), ctypes.c_size_t(size), vector) != 0:
                return None
            found = np.frombuffer(vector, dtype=np.uint8) & 1
            del view
            return found.copy()
        finally:
            mapped.close()
    except Exception:  # noqa: BLE001 (no mincore here: every chunk is decided as not cached)
        return None


def _sampled_gbps(path: str, size: int) -> float:
    """The rate of a few reads spread through the file, through the page cache: memory speed where it holds the file,
    disk speed where it does not. They land in the page cache, so nothing is wasted."""
    if size <= 4 * SAMPLE_BYTES:
        return float("inf")
    got, step = [0] * 4, (size - SAMPLE_BYTES) // 3

    def sample(i: int) -> None:
        fd = os.open(path, os.O_RDONLY)
        try:
            got[i] = max(os.preadv(fd, [bytearray(SAMPLE_BYTES)], (i * step) & ~(ALIGN - 1)), 0)
        finally:
            os.close(fd)

    started = time.perf_counter()
    workers = [threading.Thread(target=sample, args=(i,), daemon=True) for i in range(4)]
    for worker in workers:
        worker.start()
    for worker in workers:
        worker.join()
    took = time.perf_counter() - started
    return sum(got) / 1e9 / took if took > 0 else 0.0


def _decide(path: str, chunks: list, host: int = 0) -> list[bool]:
    """For each chunk, whether it is read through the page cache (True) or with O_DIRECT (False): every chunk through
    it where the memory the kernel can give holds the chunks it lacks, beside `host` bytes of buffers in memory and
    SPARE; otherwise the chunks RESIDENT in it through it and the others with O_DIRECT. Every chunk through it, too,
    where the kernel says nothing is cached but a sampled read runs at memory speed."""
    if not hasattr(os, "O_DIRECT"):
        return [True] * len(chunks)
    size = os.path.getsize(path)
    pages = _resident(path, size)
    if pages is not None and not pages.any() and _sampled_gbps(path, size) >= HOT_GBPS:
        return [True] * len(chunks)
    there = []
    for _, offset, _, length in chunks:
        first, last = offset // _mmap.PAGESIZE, (offset + length - 1) // _mmap.PAGESIZE + 1
        there.append(pages is not None and (bool(pages[first:last].mean() >= RESIDENT) if last > first else True))
    lacking = sum(length for (_, _, _, length), held in zip(chunks, there) if not held)
    if _available() >= lacking + host + SPARE:
        return [True] * len(chunks)
    return there


def _available() -> int:
    """The memory the kernel can give - free, and cached pages it can drop - in bytes (Linux's MemAvailable); 0 where
    it does not say."""
    try:
        with open("/proc/meminfo") as f:
            for line in f:
                if line.startswith("MemAvailable:"):
                    return int(line.split()[1]) * 1024
    except (OSError, ValueError, IndexError):
        pass
    return 0


def _read_into(fd_direct: Optional[int], fd_plain: int, view: memoryview, offset: int, length: int,
               direct: bool) -> None:
    """`view[:length]` filled from the file at `offset`: its aligned body with O_DIRECT when `direct`, the rest - and
    all of it otherwise, or where O_DIRECT fails - through the page cache."""
    got = 0
    if direct and fd_direct is not None and offset % ALIGN == 0:
        body = length & ~(ALIGN - 1)
        while got < body:
            try:
                n = os.preadv(fd_direct, [view[got:body]], offset + got)
            except OSError:
                break
            if n <= 0:
                break
            got += n
    while got < length:
        n = os.preadv(fd_plain, [view[got:length]], offset + got)
        if n <= 0:
            raise OSError(f"short read: {length} bytes at {offset}, got {got}")
        got += n


def _open_direct(path: str) -> Optional[int]:
    try:
        return os.open(path, os.O_RDONLY | os.O_DIRECT) if hasattr(os, "O_DIRECT") else None
    except OSError:
        return None


def _read_torch(path: str, head: dict, device: str, threads: int, chunk: int) -> tuple[dict, float]:
    """The tensors on `device` as torch tensors, the file read in parallel through pinned buffers onto the GPU (or
    straight into memory for "cpu"); and the share of the bytes read through the page cache."""
    import torch

    device = torch.device(device)
    if device.type == "cuda" and device.index is None:
        device = torch.device("cuda", torch.cuda.current_device())   # each reading thread sets it: by its number
    blocks = [torch.empty(block["bytes"], dtype=torch.uint8, device=device) for block in head["blocks"]]
    chunks = _plan(head, chunk)
    cached = _decide(path, chunks)
    if device.type == "cpu":
        views = [memoryview(b.numpy()) for b in blocks]
        _parallel(path, chunks, cached, threads, lambda: None,
                  lambda state, k, item, direct: _read_into(state["direct"], state["plain"],
                                                            views[item[0]][item[2]:item[2] + item[3]], item[1],
                                                            item[3],
                                                            direct and blocks[item[0]].data_ptr() % ALIGN == 0))
        return _views(head, blocks, torch), _share(chunks, cached)
    ready = torch.cuda.Event()
    ready.record(torch.cuda.current_stream(device))
    size = max((item[3] for item in chunks), default=ALIGN)
    size = _up(size, ALIGN)

    def start() -> dict:
        torch.cuda.set_device(device)
        stream = torch.cuda.Stream(device=device)
        stream.wait_event(ready)
        pins = [torch.empty(size, dtype=torch.uint8, pin_memory=True) for _ in range(2)]
        events = [torch.cuda.Event() for _ in range(2)]
        for event in events:
            event.record(stream)
        aligned = all(pin.data_ptr() % ALIGN == 0 for pin in pins)
        return {"stream": stream, "pins": pins, "views": [memoryview(p.numpy()) for p in pins], "events": events,
                "aligned": aligned}

    def one(state: dict, k: int, item: tuple, direct: bool) -> None:
        block, offset, inside, length = item
        slot = k % 2
        state["events"][slot].synchronize()                 # this pinned buffer's last copy has left it
        _read_into(state["direct"], state["plain"], state["views"][slot], offset, length,
                   direct and state["aligned"])
        with torch.cuda.stream(state["stream"]):
            blocks[block].narrow(0, inside, length).copy_(state["pins"][slot].narrow(0, 0, length), non_blocking=True)
            state["events"][slot].record(state["stream"])

    def finish(state: dict) -> None:
        state["stream"].synchronize()

    _parallel(path, chunks, cached, threads, start, one, finish)
    torch.cuda.synchronize(device)
    return _views(head, blocks, torch), _share(chunks, cached)


def _parallel(path: str, chunks: list, cached: list, threads: int, start: Callable, one: Callable,
              finish: Callable = lambda state: None) -> None:
    """`one(state, k, chunk, direct)` for every chunk, on `threads` threads, each with its own file descriptors and the
    state `start()` makes for it; the first error raised again once all have stopped."""
    work: queue.SimpleQueue = queue.SimpleQueue()
    for item, through in zip(chunks, cached):
        work.put((item, not through))
    count = max(1, min(threads, len(chunks)))
    for _ in range(count):
        work.put(None)
    errors: list = []
    direct_wanted = not all(cached)

    def reader() -> None:
        state: dict = {}
        try:
            state = start() or {}
            state["plain"] = os.open(path, os.O_RDONLY)
            state["direct"] = _open_direct(path) if direct_wanted else None
            k = 0
            while True:
                got = work.get()
                if got is None:
                    break
                item, direct = got
                one(state, k, item, direct)
                k += 1
            finish(state)
        except BaseException as exc:  # noqa: BLE001 (raised again by the caller once every reader has stopped)
            errors.append(exc)
        finally:
            for name in ("plain", "direct"):
                if state.get(name) is not None:
                    os.close(state[name])

    workers = [threading.Thread(target=reader, daemon=True) for _ in range(count)]
    for worker in workers:
        worker.start()
    for worker in workers:
        worker.join()
    if errors:
        raise errors[0]


def _share(chunks: list, cached: list) -> float:
    total = sum(item[3] for item in chunks)
    return sum(item[3] for item, through in zip(chunks, cached) if through) / total if total else 1.0


def _views(head: dict, blocks: list, torch: Any) -> dict:
    """Each tensor as a view of its block: its bytes, its dtype, its shape."""
    out = {}
    for record in head["tensors"]:
        raw = blocks[record["block"]].narrow(0, record["offset"], record["bytes"])
        dtype = getattr(torch, record["dtype"])
        out[record["name"]] = raw.view(dtype).view(record["shape"]) if record["bytes"] else \
            torch.empty(record["shape"], dtype=dtype, device=raw.device)
    return out


def _put_jax(arrays: dict, device: str) -> dict:
    """Arrays in memory as JAX arrays on `device` ("cuda", "cuda:1", "cpu"), in JAX's own memory pool; ready once the
    caller blocks on them, each copied as JAX copies what it is given."""
    import jax

    platform, _, index = device.partition(":")
    target = jax.devices("gpu" if platform == "cuda" else platform)[int(index or 0)]
    return {name: jax.device_put(array, target) for name, array in arrays.items()}


def _read_numpy(path: str, head: dict, threads: int, chunk: int) -> tuple[dict, float]:
    """The tensors in memory as numpy arrays (bfloat16 and float8 by ml_dtypes), read in parallel."""
    blocks = [_aligned(block["bytes"]) for block in head["blocks"]]
    views = [memoryview(b) for b in blocks]
    chunks = _plan(head, chunk)
    cached = _decide(path, chunks, host=sum(block["bytes"] for block in head["blocks"]))
    _parallel(path, chunks, cached, threads, lambda: None,
              lambda state, k, item, direct: _read_into(state["direct"], state["plain"],
                                                        views[item[0]][item[2]:item[2] + item[3]], item[1], item[3],
                                                        direct and blocks[item[0]].ctypes.data % ALIGN == 0))
    out = {}
    for record in head["tensors"]:
        raw = blocks[record["block"]][record["offset"]:record["offset"] + record["bytes"]]
        out[record["name"]] = raw.view(_numpy_dtype(record["dtype"])).reshape(record["shape"])
    return out, _share(chunks, cached)


def _aligned(size: int) -> Any:
    """A numpy buffer of `size` bytes whose first byte's address is a multiple of ALIGN."""
    import numpy as np

    raw = np.empty(size + ALIGN, dtype=np.uint8)
    start = -raw.ctypes.data % ALIGN
    return raw[start:start + size]


def _numpy_dtype(name: str) -> Any:
    import numpy as np

    numpy_name = _DTYPES[name][1]
    if numpy_name is not None:
        return np.dtype(numpy_name)
    import ml_dtypes

    return np.dtype(getattr(ml_dtypes, name))
