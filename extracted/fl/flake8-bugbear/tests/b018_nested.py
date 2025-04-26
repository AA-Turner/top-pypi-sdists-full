
X = 1
False  # bad


def func(y):
    a = y + 1
    5.5  # bad
    return a


class TestClass:
    GOOD = [1, 3]
    [5, 6]  # bad

    def method(self, xx, yy=5):
        t = (xx,)
        (yy,)  # bad

        while 1:
            i = 3
            4  # bad
            for n in range(i):
                j = 5
                1.5  # bad
                if j < n:
                    u = {1, 2}
                    {4, 5}  # bad
                elif j == n:
                    u = {1, 2, 3}
                    {4, 5, 6}  # bad
                else:
                    u = {2, 3}
                    {4, 6}  # bad
                    try:
                        1j  # bad
                        r = 2j
                    except Exception:
                        r = 3j
                        5  # bad
                    finally:
                        4j  # bad
                        r += 1
                    return u + t
