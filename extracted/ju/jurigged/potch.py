import time

from jurigged import make_recoder, watch

watch()


def f(x):
    return x * x * x


assert f(2) == 4

# Change the behavior of the function, but not in the original file
recoder = make_recoder(f)

recoder.on_status.register(print)

recoder.patch("def f(x): return x * x * x")
assert f(2) == 8

for i in range(10):
    print(i)
    time.sleep(1)

# Write the patch to the original file itself
recoder.commit()
