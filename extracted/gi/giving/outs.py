import time

from giving import give, given

print("==========")

with given() as gv:
    gv.display()

    a, b = 10, 20
    give()
    give(a * b, c=30)

print("==========")

with given()["s"].values() as results:
    s = 0
    for i in range(5):
        s += i
        give(s)

print(results)

print("==========")


def collatz(n):
    while n != 1:
        give(n)
        n = (3 * n + 1) if n % 2 else (n // 2)


with given() as gv:
    gv["n"].max().print("max: {}")
    gv["n"].count().print("steps: {}")

    collatz(2021)

print("==========")

(steps,) = given()["n"].count().eval(collatz, 2021)
print(steps)

print("==========")

with given() as gv:
    gv.kscan().display()

    give(elk=1)
    give(rabbit=2)
    give(elk=3, wolf=4)

print("==========")

with given() as gv:
    gv.throttle(1).display()

    for i in range(50):
        give(i)
        time.sleep(0.1)
