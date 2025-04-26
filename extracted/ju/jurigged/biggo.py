import gc
import time

deep = None


class Oi:
    def __init__(self, left, right):
        self.left = left
        self.right = right


def build(depth):
    global deep
    if depth == 0:
        return Oi(depth, depth)
    else:
        d1 = build(depth - 1)
        d2 = build(depth - 1)
        deep = d2
        return Oi(d1, d2)


# massive = build(21)
massive = build(10)

t1 = time.time()
print(len(gc.get_objects()))
t2 = time.time()
print(t2 - t1)

t1 = time.time()
print(len(gc.get_referrers(deep)))
t2 = time.time()
print(t2 - t1)

t1 = time.time()
print(len(gc.get_referrers(massive)))
t2 = time.time()
print(t2 - t1)
