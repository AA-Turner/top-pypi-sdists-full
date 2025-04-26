def f(x):
    return 10 / x


def g(x):
    return 10 / x


def main():
    for i in range(10, -1, -1):
        print(g(i))
        print(f(i))


if __name__ == "__main__":
    main()
