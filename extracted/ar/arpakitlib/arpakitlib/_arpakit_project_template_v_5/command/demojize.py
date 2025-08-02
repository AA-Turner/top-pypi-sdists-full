from emoji import demojize


def __command():
    print(demojize(input("text: ").strip()))


if __name__ == '__main__':
    __command()
