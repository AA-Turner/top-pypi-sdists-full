from giving.utils import lax_function

# def wolf(n):
#     for i in range(n):
#         give(i=i, j=i * i)


# with given() as gv:
#     gv.kmap(lambda i: f"i = {i}").print()
#     # gv.kmap(lambda i: i * i).print()

#     wolf(100)


@lax_function
def f(i):
    return f"i = {i}"


for i in range(100):
    print(f(i=i))
