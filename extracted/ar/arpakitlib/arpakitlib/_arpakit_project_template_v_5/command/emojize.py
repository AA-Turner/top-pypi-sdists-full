from emoji import emojize


def __command():
    print(emojize(input("text: ").strip()))


if __name__ == '__main__':
    __command()
