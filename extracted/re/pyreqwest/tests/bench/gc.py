import gc
from collections.abc import Generator
from contextlib import contextmanager


@contextmanager
def capture_gc_stats(lib: str) -> Generator[None, None, None]:
    gc.collect()
    gc.collect()
    gc.collect()
    stats_before = gc.get_stats()

    yield

    gc.collect()
    gc.collect()
    gc.collect()
    stats_after = gc.get_stats()

    tot_collections = 0
    tot_collected = 0
    for gen in range(len(stats_after)):
        gen_collections = stats_after[gen]["collections"] - stats_before[gen]["collections"]
        gen_collected = stats_after[gen]["collected"] - stats_before[gen]["collected"]
        tot_collections += gen_collections
        tot_collected += gen_collected
        print(f"{lib} generation {gen}, collections: {gen_collections}, collected: {gen_collected}")
    print(f"{lib} total collections: {tot_collections}, total collected: {tot_collected}")
