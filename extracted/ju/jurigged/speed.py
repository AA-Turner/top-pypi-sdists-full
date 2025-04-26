import sys
import time


class Bouette:
    def __init__(self):
        self.rix = 3

    def ah(self, event, obj):
        pass
        # if event == "exec":
        #     (code,) = obj
        #     self.assimilate(code)


def ah(event, obj):
    print(event)
    if event == "exec":
        (code,) = obj
        self.assimilate(code)


def ahem(self):
    def ah(event, obj):
        if event == "exec":
            (code,) = obj
            self.assimilate(code)

    return ah


# sys.addaudithook(Bouette().ah)
# sys.addaudithook(ahem(4))
sys.addaudithook(ah)


x = Bouette()


def main(n):
    for i in range(n):
        id(x)
        [1, 2, 3]
        object.__getattr__(x, "rix", 8)
        object.__setattr__(x, "rix", 21)


# def main():
#     j = 0
#     for i in range(1000000):
#         setattr(x, "rix", 8)


# t = time.time()
# main()
# print(time.time() - t)


t = time.time()
main(1)
print(time.time() - t)
