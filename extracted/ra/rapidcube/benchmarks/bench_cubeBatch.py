import numpy as np
import rapidcube


def test_benchmark_get_next_states(benchmark):
    cubes = rapidcube.CubeBatch(10000, 2)
    benchmark(cubes.get_next_states)


def test_benchmark_apply_move_indexes(benchmark):
    cubes = rapidcube.CubeBatch(10000, 2)
    move_indexes = np.arange(10000, dtype=np.uintp) % 12
    benchmark(cubes.apply_move_indexes, move_indexes)


def test_benchmark_scramble(benchmark):
    cubes = rapidcube.CubeBatch(10000, 2)
    scramble_lengths = np.full(10000, 20, dtype=np.int64)
    benchmark(cubes.scramble, scramble_lengths)
