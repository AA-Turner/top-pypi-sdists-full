# adapted from https://github.com/ImperialCollegeLondon/Mathematical-Computing-Demo/blob/219bc0e26ea6f5ee7548009c849959b268f54821/M1C%20(Python)/M1C-Number-Theory/.ipynb_checkpoints/Python%20Number%20Theory%2003%20-%20Extended%20Euclidean%20Algorithm-checkpoint.ipynb
def _ehcf(a: int, b: int) -> int:
    """Extended euclidean algorithm."""
    p1, q1, h1 = 1, 0, a
    p2, q2, h2 = 0, 1, b

    while h2:
        r = h1 // h2
        p3 = p1 - r * p2
        q3 = q1 - r * q2
        h3 = h1 - r * h2
        p1, q1, h1 = p2, q2, h2
        p2, q2, h2 = p3, q3, h3

    return (p1, q1, h1)


# adapted from https://github.com/ImperialCollegeLondon/Mathematical-Computing-Demo/blob/219bc0e26ea6f5ee7548009c849959b268f54821/M1C%20(Python)/M1C-Number-Theory/.ipynb_checkpoints/Python%20Number%20Theory%2003%20-%20Extended%20Euclidean%20Algorithm-checkpoint.ipynb
def inverse_mod_n(e: int, n: int) -> int:
    # if int(e).bit_count() != 1:  # py3.10+
    if e == 0 or e & (e - 1):  # py3.8 compat
        raise ValueError("e must be a power of 2")
    if n % 2 == 0:
        raise ValueError("n must be odd")
    p, _q, _h = _ehcf(e, n)

    return p % n
