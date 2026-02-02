import time

from rx import create


def test_observable(observer, scheduler):
    observer.on_next("Hello")
    for i in range(10):
        time.sleep(1)
        observer.on_next(i)


#    observer.on_error("Error occured")
#    observer.on_completed()

source = create(test_observable)

print("A?")
source.subscribe(print)
print("done?")
