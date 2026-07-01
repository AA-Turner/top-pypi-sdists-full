import graycode


def main():
    assert graycode.tc_to_gray_code(2) == 3
    assert graycode.gray_code_to_tc(3) == 2


if __name__ == '__main__':
    main()
