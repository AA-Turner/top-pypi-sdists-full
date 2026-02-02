from giving import give, given


def test(n):
    # Explicitly give one=1 and two=2
    give(one=1, two=2)

    # Equivalent to give(n=n)
    give(n)

    for i in range(n):
        # Equivalent to give(i=i)
        give(i, even=i % 2 == 0)

    # Equivalent to give(twicen=2 * n)
    twicen = give(2 * n)

    nsqr = n * n
    # Equivalent to give(nsqr=nsqr)
    give()


with given() as gv:
    gv.display()
    gv["?i"].average().as_("avg").display()

    test(4)
