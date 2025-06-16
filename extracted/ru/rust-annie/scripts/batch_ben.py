# batch_benchmark.py

import time
import numpy as np
from rust_annie import AnnIndex, Distance

def benchmark_batch(N=10000, D=64, k=10, batch_size=64, repeats=20):
    # 1. Prepare random data
    data = np.random.rand(N, D).astype(np.float32)
    ids  = np.arange(N, dtype=np.int64)
    idx  = AnnIndex(D, Distance.EUCLIDEAN)
    idx.add(data, ids)

    # 2. Prepare query batch
    queries = data[:batch_size]

    # Warm-up
    idx.search_batch(queries, k)

    # 3. Benchmark Rust batch search
    t0 = time.perf_counter()
    for _ in range(repeats):
        idx.search_batch(queries, k)
    t_batch = (time.perf_counter() - t0) / repeats

    print(f"Rust batch search time ({batch_size} queries): {t_batch*1e3:8.3f} ms")
    print(f"Per-query time:                  {t_batch/batch_size*1e3:8.3f} ms")

if __name__ == "__main__":
    benchmark_batch()
