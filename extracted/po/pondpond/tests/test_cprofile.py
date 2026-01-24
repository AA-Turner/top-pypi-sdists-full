import time

import pytest

from pond import Pond, PooledObject, PooledObjectFactory


class Dog:
    name: str
    validate_result: bool = True


class PooledDogFactory(PooledObjectFactory):
    def createInstance(self) -> PooledObject:
        dog = Dog()
        dog.name = "puppy"
        return PooledObject(dog)

    def destroy(self, pooled_object: PooledObject) -> None:
        del pooled_object

    def reset(self, pooled_object: PooledObject) -> PooledObject:
        pooled_object.keeped_object.name = "puppy"
        return pooled_object

    def validate(self, pooled_object: PooledObject) -> bool:
        return pooled_object.keeped_object.validate_result


pooled_maxsize = 10
pond = Pond(
    borrowed_timeout=2,
    time_between_eviction_runs=-1,
    thread_daemon=True,
    eviction_weight=0.8,
)
factory = PooledDogFactory(pooled_maxsize=10, least_one=False)

pond.register(factory)
T1 = time.perf_counter()
for i in range(100000):
    pooled_object: PooledObject = pond.borrow(factory)
    dog: Dog = pooled_object.use()
    pond.recycle(pooled_object, factory)
T2 = time.perf_counter()
print("Run time: %s ms" % ((T2 - T1) * 1000))
