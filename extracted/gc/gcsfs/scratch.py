import asyncio
import ctypes
import os
import time

PyBytes_FromStringAndSize = ctypes.pythonapi.PyBytes_FromStringAndSize
PyBytes_FromStringAndSize.restype = ctypes.py_object
PyBytes_FromStringAndSize.argtypes = [ctypes.c_void_p, ctypes.c_ssize_t]

PyBytes_AsString = ctypes.pythonapi.PyBytes_AsString
PyBytes_AsString.restype = ctypes.c_void_p
PyBytes_AsString.argtypes = [ctypes.py_object]


def _fast_slice(src_bytes, offset, read_size):
    if read_size == 0:
        return b""
    dest_bytes = PyBytes_FromStringAndSize(None, read_size)
    src_ptr = PyBytes_AsString(src_bytes)
    dest_ptr = PyBytes_AsString(dest_bytes)
    ctypes.memmove(dest_ptr, src_ptr + offset, read_size)
    return dest_bytes


def bytes_slice(data: bytes, offset: int, size: int):
    """Worker using native python slicing inside a thread."""
    return data[offset: offset + size]


def memoryview_slice(data: bytes, offset: int, size: int):
    return memoryview(data)[offset: offset + size]


async def worker(func, data, offset, size, iterations):
    for _ in range(iterations):
        b"".join([
            await asyncio.to_thread(func, data, offset, size)
            for _ in range(5)
            ]
        )


async def run_scenario(scenario_name: str, payload_mb: int, slice_kb: int, tasks: int, iterations_per_task: int):
    print(f"\n--- {scenario_name} ---")
    print(f"Slice Size: {slice_kb} KB | Concurrency: {tasks} task(s) | {iterations_per_task} slices per task")

    data = os.urandom(payload_mb * 1024 * 1024)
    offset = 1024 * 1024
    size = int(slice_kb * 1024)

    methods = {
        "Native Slicing": bytes_slice,
        "Memoryview Slicing": memoryview_slice,
        "Fast Slice (ctypes)": _fast_slice
    }

    results = {}

    for name, worker_func in methods.items():
        start_time = time.perf_counter()
        async_tasks = [
            asyncio.create_task(worker(worker_func, data, offset, size, iterations_per_task))
            for _ in range(tasks)
        ]
        await asyncio.gather(*async_tasks)
        elapsed_time = time.perf_counter() - start_time

        results[name] = elapsed_time
        print(f"{name: <25}: {elapsed_time:.4f} seconds")

    print("\nResults vs Native Slicing Baseline:")
    baseline = results["Native Slicing"]
    for name, elapsed in results.items():
        if name == "Native Slicing":
            continue
        speedup = baseline / elapsed
        direction = "FASTER" if speedup >= 1 else "SLOWER"
        display_ratio = speedup if speedup >= 1 else (1 / speedup)
        print(f"-> {name: <19} is {display_ratio:.2f}x {direction}")
    print("-" * 55)


async def main():
    print("Starting Asyncio Slicing Benchmark...")
    print("=" * 55)

    scenarios = [
        {
            "name": "Micro-slicing",
            "payload_mb": 10,
            "slice_kb": 512,
            "iterations_per_task": 10000
        },
        {
            "name": "Macro-slicing",
            "payload_mb": 100,
            "slice_kb": 10 * 1024,
            "iterations_per_task": 1000
        }
    ]

    for scenario in scenarios:
        for task_count in [1, 4, 10]:
                await run_scenario(
                    scenario_name=f"{scenario['name']} - {task_count} Task(s)",
                    payload_mb=scenario["payload_mb"],
                    slice_kb=scenario["slice_kb"],
                    tasks=task_count,
                    iterations_per_task=scenario["iterations_per_task"]
                )


if __name__ == "__main__":
    asyncio.run(main())