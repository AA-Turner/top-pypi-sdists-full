import redis
import random
from simple_parsing import parse
from dataclasses import dataclass
from redis_command_generator.BaseGen import BaseGen, cg_method
import time

@dataclass
class StringGen(BaseGen):
    subval_size: int = 5
    incrby_min: int = -1000
    incrby_max: int = 1000
    
    @cg_method(cmd_type="string", can_create_key=True)
    def set(self, pipe: redis.client.Pipeline, key: str) -> None:
        pipe.set(key, self._rand_str(self.subval_size))
    
    @cg_method(cmd_type="string", can_create_key=True)
    def append(self, pipe: redis.client.Pipeline, key: str) -> None:
        pipe.append(key, self._rand_str(self.subval_size))
    
    @cg_method(cmd_type="string", can_create_key=True)
    def incrby(self, pipe: redis.client.Pipeline, key: str) -> None:
        pipe.incrby(key, random.randint(self.incrby_min, self.incrby_max))
    
    @cg_method(cmd_type="string", can_create_key=False)
    def delete(self, pipe: redis.client.Pipeline, key: str) -> None:
        pipe.delete(key)
    
    @cg_method(cmd_type="string", can_create_key=True)
    def setnx(self, pipe: redis.client.Pipeline, key: str) -> None:
        value = self._rand_str(self.subval_size)
        pipe.setnx(key, value)

    @cg_method(cmd_type="string", can_create_key=True)
    def setex(self, pipe: redis.client.Pipeline, key: str) -> None:
        value = self._rand_str(self.subval_size)
        ex = random.randint(1, 1000)
        pipe.setex(key, ex, value)

    @cg_method(cmd_type="string", can_create_key=True)
    def psetex(self, pipe: redis.client.Pipeline, key: str) -> None:
        value = self._rand_str(self.subval_size)
        px = random.randint(1, 1000000)
        pipe.psetex(key, px, value)

    @cg_method(cmd_type="string", can_create_key=False)
    def get(self, pipe: redis.client.Pipeline, key: str) -> None:
        pipe.get(key)

    @cg_method(cmd_type="string", can_create_key=True)
    def getset(self, pipe: redis.client.Pipeline, key: str) -> None:
        value = self._rand_str(self.subval_size)
        pipe.getset(key, value)

    @cg_method(cmd_type="string", can_create_key=False)
    def getdel(self, pipe: redis.client.Pipeline, key: str) -> None:
        pipe.getdel(key)

    @cg_method(cmd_type="string", can_create_key=False)
    def getex(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Randomly choose an expiry option
        expiry_type = random.choice(['ex', 'px', 'exat', 'pxat', 'persist'])
        kwargs = {}
        if expiry_type == 'ex':
            kwargs['ex'] = random.randint(1, 1000)
        elif expiry_type == 'px':
            kwargs['px'] = random.randint(1, 1000000)
        elif expiry_type == 'exat':
            kwargs['exat'] = int(time.time()) + random.randint(1, 1000)
        elif expiry_type == 'pxat':
            kwargs['pxat'] = int(time.time() * 1000) + random.randint(1, 1000000)
        elif expiry_type == 'persist':
            kwargs['persist'] = True
        pipe.getex(key, **kwargs)

    @cg_method(cmd_type="string", can_create_key=True)
    def mset(self, pipe: redis.client.Pipeline, key: str) -> None:
        mapping = {key: self._rand_str(self.subval_size)}
        for _ in range(random.randint(1, 3)):
            mapping[self._rand_str(self.subval_size)] = self._rand_str(self.subval_size)
        pipe.mset(mapping)

    @cg_method(cmd_type="string", can_create_key=True)
    def msetnx(self, pipe: redis.client.Pipeline, key: str) -> None:
        mapping = {key: self._rand_str(self.subval_size)}
        for _ in range(random.randint(1, 3)):
            mapping[self._rand_str(self.subval_size)] = self._rand_str(self.subval_size)
        pipe.msetnx(mapping)

    @cg_method(cmd_type="string", can_create_key=False)
    def mget(self, pipe: redis.client.Pipeline, key: str) -> None:
        keys = [key]
        for _ in range(random.randint(1, 3)):
            keys.append(self._rand_str(self.subval_size))
        pipe.mget(keys)

    @cg_method(cmd_type="string", can_create_key=True)
    def incrbyfloat(self, pipe: redis.client.Pipeline, key: str) -> None:
        value = random.uniform(1, 1000)
        pipe.incrbyfloat(key, value)

    @cg_method(cmd_type="string", can_create_key=True)
    def decrby(self, pipe: redis.client.Pipeline, key: str) -> None:
        value = random.randint(1, 1000)
        pipe.decrby(key, value)

    @cg_method(cmd_type="string", can_create_key=False)
    def strlen(self, pipe: redis.client.Pipeline, key: str) -> None:
        pipe.strlen(key)

    @cg_method(cmd_type="string", can_create_key=False)
    def getrange(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Use a random range
        start = random.randint(0, 5)
        end = start + random.randint(0, 10)
        pipe.getrange(key, start, end)

    @cg_method(cmd_type="string", can_create_key=True)
    def setrange(self, pipe: redis.client.Pipeline, key: str) -> None:
        offset = random.randint(0, 5)
        value = self._rand_str(self.subval_size)
        pipe.setrange(key, offset, value)

if __name__ == "__main__":
    string_gen = parse(StringGen)
    string_gen.distributions = '{"set": 100, "append": 100, "incrby": 100, "delete": 100, "setnx": 100, "setex": 100, "psetex": 100, "get": 100, "getset": 100, "getdel": 100, "getex": 100, "mset": 100, "msetnx": 100, "mget": 100, "incrbyfloat": 100, "decrby": 100, "strlen": 100, "getrange": 100, "setrange": 100}'
    string_gen._run()

