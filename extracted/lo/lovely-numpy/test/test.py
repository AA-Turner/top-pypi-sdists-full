import numpy as np
import lovely_numpy
from time import perf_counter
import memory_profiler

very_large = np.random.default_rng(1337).standard_normal(1024*1024*1024, dtype=np.float32)

def f():
    t0 = perf_counter()
    print(f"Lovely numpy: {lovely_numpy.__version__}")
    print(f"One Billion float32 array:\n{lovely_numpy.Lo(very_large)}")
    print(f"Time: {perf_counter() - t0:.3f}s")

mem = memory_profiler.memory_usage((f, ), interval=0.01)
print("Memory:")
print(f"\tInitial (input array): {mem[0] / 1024:.3f} GiB")
print(f"\tPeak:                  {max(mem) / 1024:.3f} GiB")
print(f"\tOverhead:              {(max(mem) - mem[0]) / 1024:.3f} GiB")