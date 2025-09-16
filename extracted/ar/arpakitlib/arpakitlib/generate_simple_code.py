from random import randint


def generate_simple_code(
        *,
        amount: int = 5
) -> str:
    alphabet: list = list("JZSDQWRLGFZ" + "123456789")
    return "".join(alphabet[randint(0, len(alphabet) - 1)] for _ in range(amount))


def __example():
    print(generate_simple_code(amount=5))


if __name__ == '__main__':
    __example()
