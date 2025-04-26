from collections import defaultdict
from itertools import chain, combinations


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def opts(n, nope, must=set()):
    print("=====")
    must = set(must)
    nums = set(range(1, 10)) - set(nope)
    ps = powerset(nums)
    results = defaultdict(list)
    for x in ps:
        if sum(x) == n and ((set(x) & must) == must):
            results[len(x)].append(x)
    for k, entries in results.items():
        print(k)
        for entry in entries:
            print("    ", list(sorted(entry)))
        # __.give(dict(results))
    return results


def mainx():
    # n = 2
    # x = 1
    # res = opts(n * 10 + x, [n, x], [3])

    res = opts(12, [], [])

    print(2 + 3 + 8 + 9 + 2 * 1 + 2 * 7 + 2 * 5 + 4 * 2 + 6 * 4)
    print(2 + 3 + 8 + 9 + 2 * 1 + 2 * 7 + 2 * 5 + 4 * 4 + 6 * 2)
    print(6 * 19 - 90)
    print(90 - (19 * 4 - 14))

    print(-24 + 19 - (45 - 19 - 13))
    print(-24 + 19 - (45 - 19 - 14))

    # 32: 145679 8

    # 35: 146789 2

    # 27: 134568 9
    # 28: 134569 7
    # 29: 134678 5


def mainy():
    for x in combinations(range(1, 10), 5):
        sm = sum(x)
        for i in range(1, 10):
            for j in range(i, 10):
                if i != j and i * j == sm and i not in x and j not in x:
                    xp = [*x, i, j]
                    print(x, sm, i, j, [k for k in range(1, 10) if k not in xp])


def main():
    mainx()


# [1, 2, 6, 9]
# [1, 2, 7, 8]
[1, 3, 5, 9]
[1, 3, 6, 8]
# [1, 4, 5, 8]
# [1, 4, 6, 7]
[2, 3, 4, 9]
# [2, 3, 5, 8]
[2, 3, 6, 7]
# [2, 4, 5, 7]
# [3, 4, 5, 6]

main()


# 13
# 17
# 19
# 23
# 29
# 31
# 37
# 41
# 43
# 47
# 53
# 59
# 61
# 67
# 71
# 73
# 79
# 83
# 89
# 97

1111222333455678
