import timeit
import pefile
import tracemalloc
import sys

def run_pefile(show_info=False):
    with open(sys.argv[1], 'rb') as f:
        data = f.read()
    pe = pefile.PE(data=data)
    l = len(pe.dump_info())
    if show_info:
        print(type(pe.__data__))
        print(l)

tracemalloc.start()  # Start tracing memory allocations
run_pefile(show_info=True)
snapshot = tracemalloc.take_snapshot()  # Take a snapshot of current memory allocations
top_stats = snapshot.statistics('lineno')  # Get statistics grouped by line number

for stat in top_stats[:10]:  # Print top 10 memory consuming lines
    print(stat)

print(timeit.timeit(run_pefile, number=4))
