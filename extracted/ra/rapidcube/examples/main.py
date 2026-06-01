from rapidcube import Cube2x2, Cube3x3, CubeBatch, inverse_scramble, get_next_states
import torch


def main():
    cube = Cube2x2()
    # cube.do_moves("R U R' U' R' F R2 U' R' U' R U R' F'")
    # print(cube)
    # cube.do_moves("R U R' U' R' F R2 U' R' U' R U R' F'")
    print(cube)
    cube.do_moves("D'")
    print(cube)


def test_3x3():
    cube = Cube3x3()
    moves = "F' R F R2 B' D2 R2 L F' L2 D2 L2 D L2 F2 U R2 D L2 B2 D"
    for m in moves.split(" "):
        print("Doing Move: " + m + "\n")
        cube.do_moves(m)
        print(cube)
    cube.do_moves("R")
    print(cube)


def demo_array():
    cube = Cube2x2()
    print(cube.to_sticker_array())
    print(cube)
    cube.do_moves("R")
    print(inverse_scramble("R"))
    print(cube.to_sticker_array())
    print(cube)

    cubes = [Cube2x2(), Cube2x2()]
    print(get_next_states(cubes))


def demo_scramble():
    cube = Cube2x2()
    print(cube)
    cube.scramble(10)
    print(cube)
    cube = Cube2x2()
    cube.scramble()
    print(cube)


# def encode_state():
#     cube = Cube2x2()
#     str_state = "00" + "{0:b}".format(cube.state)
#     segments = [
#         str_state[max(0, end - 5) : end] for end in range(len(str_state), 0, -5)
#     ][::-1]
#     int_segments = [[int(s[:2], 2), int(s[2:], 2)] for s in segments]

#     tensor = torch.tensor(int_segments)
#     # print(str_state)
#     # print(segments)
#     # print(tensor)
#     return tensor


def demo_cubeBatch():
    batch = CubeBatch(3, 2)
    print(torch.tensor(batch.get_next_states()))
    scramble_lengths = torch.arange(1, 4, dtype=torch.int64)
    batch.scramble(scramble_lengths.numpy())
    print(batch)


def demo_cubeBatch2():
    batch = CubeBatch(1, 2)
    print(batch)
    print(torch.from_numpy(batch.to_sticker_array()))


if __name__ == "__main__":
    # _ = encode_state()
    demo_cubeBatch2()
