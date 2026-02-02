import random
import string


def random_string(length):
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_request_id(length: int = 12):
    return random_string(length)


async def reservoir_sampling_async(async_iterator, n):
    pool = []
    index = 0
    async for el in async_iterator:
        if index < n:
            pool.append(el)
        else:
            r = random.randint(0, index)
            if r < n:
                pool[r] = el
        index += 1
    return pool
