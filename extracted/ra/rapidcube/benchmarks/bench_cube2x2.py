import rapidcube
import magiccube
import pycuber

Cube2x2 = rapidcube.Cube2x2


def test_benchmark_construct_cube(benchmark):
    benchmark(Cube2x2)


def test_benchmark_single_move_dispatch(benchmark):
    cube = Cube2x2()
    benchmark(cube.do_r_move)


def test_benchmark_state_property_read(benchmark):
    cube = Cube2x2()
    benchmark(lambda: cube.state)


def test_benchmark_to_binary(benchmark):
    cube = Cube2x2()
    benchmark(cube.to_binary)


def test_benchmark_str_render(benchmark):
    cube = Cube2x2()
    benchmark(str, cube)


def test_benchmark_short_algorithm_on_same_cube(benchmark):
    cube = Cube2x2()

    def run_alg():
        cube.do_r_move()
        cube.do_u_move()
        cube.do_f_prime_move()
        cube.do_u_prime_move()
        cube.do_r_prime_move()

    benchmark(run_alg)


def test_benchmark_do_moves_20_turn_algorithm(benchmark):
    cube = Cube2x2()
    moves_20 = "R U R' U' F2 L D B' R2 U F' L2 D' B U2 R' F L' D2 B2"

    def run_alg():
        cube.do_moves(moves_20)

    benchmark(run_alg)


def test_benchmark_do_moves_20_turn_algorithm_magiccube(benchmark):
    cube = magiccube.Cube(3)
    moves_20 = "R U R' U' F2 L D B' R2 U F' L2 D' B U2 R' F L' D2 B2"

    def run_alg():
        cube.rotate(moves_20)

    benchmark(run_alg)


def test_benchmark_do_moves_20_turn_algorithm_pycuber(benchmark):
    cube = pycuber.Cube()
    moves_20 = "R U R' U' F2 L D B' R2 U F' L2 D' B U2 R' F L' D2 B2"

    def run_alg():
        cube(moves_20)

    benchmark(run_alg)
