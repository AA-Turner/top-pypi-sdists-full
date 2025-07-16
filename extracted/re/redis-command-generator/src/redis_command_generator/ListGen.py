import redis
import random
from simple_parsing import parse
from dataclasses import dataclass
from redis_command_generator.BaseGen import BaseGen, cg_method

@dataclass
class ListGen(BaseGen):
    max_subelements: int = 10
    subval_size: int = 5
    
    @cg_method(cmd_type="list", can_create_key=True)
    def lpush(self, pipe: redis.client.Pipeline, key: str) -> None:
        items = [self._rand_str(self.subval_size) for _ in range(random.randint(1, self.max_subelements))]
        pipe.lpush(key, *items)
    
    @cg_method(cmd_type="list", can_create_key=True)
    def rpush(self, pipe: redis.client.Pipeline, key: str) -> None:
        items = [self._rand_str(self.subval_size) for _ in range(random.randint(1, self.max_subelements))]
        pipe.rpush(key, *items)
    
    @cg_method(cmd_type="list", can_create_key=False)
    def lpop(self, pipe: redis.client.Pipeline, key: str) -> None:
        pipe.lpop(key)
    
    @cg_method(cmd_type="list", can_create_key=False)
    def rpop(self, pipe: redis.client.Pipeline, key: str) -> None:
        pipe.rpop(key)
    
    @cg_method(cmd_type="list", can_create_key=False)
    def lrem(self, pipe: redis.client.Pipeline, key: str) -> None:
        redis_obj = self._pipe_to_redis(pipe)
        list_length = redis_obj.llen(key)
        if not list_length:
            return
        
        rand_index = random.randint(0, list_length - 1)
        item = redis_obj.lindex(key, rand_index)
        if not item:
            return
        
        pipe.lrem(key, 0, item)

    @cg_method(cmd_type="list", can_create_key=False)
    def llen(self, pipe: redis.client.Pipeline, key: str) -> None:
        pipe.llen(key)

    @cg_method(cmd_type="list", can_create_key=False)
    def lindex(self, pipe: redis.client.Pipeline, key: str) -> None:
        redis_obj = self._pipe_to_redis(pipe)
        length = redis_obj.llen(key)
        if length:
            index = random.randint(-length, length - 1)
        else:
            index = 0
        pipe.lindex(key, index)

    @cg_method(cmd_type="list", can_create_key=False)
    def lrange(self, pipe: redis.client.Pipeline, key: str) -> None:
        redis_obj = self._pipe_to_redis(pipe)
        length = redis_obj.llen(key)
        if length:
            start = random.randint(-length, length - 1)
            stop = random.randint(start, length - 1)
        else:
            start, stop = 0, -1
        pipe.lrange(key, start, stop)

    @cg_method(cmd_type="list", can_create_key=False)
    def lset(self, pipe: redis.client.Pipeline, key: str) -> None:
        redis_obj = self._pipe_to_redis(pipe)
        length = redis_obj.llen(key)
        if not length:
            return
        index = random.randint(-length, length - 1)
        value = self._rand_str(self.subval_size)
        pipe.lset(key, index, value)

    @cg_method(cmd_type="list", can_create_key=False)
    def ltrim(self, pipe: redis.client.Pipeline, key: str) -> None:
        redis_obj = self._pipe_to_redis(pipe)
        length = redis_obj.llen(key)
        if length:
            start = random.randint(0, length - 1)
            stop = random.randint(start, length - 1)
        else:
            start, stop = 0, -1
        pipe.ltrim(key, start, stop)

    @cg_method(cmd_type="list", can_create_key=False)
    def lpos(self, pipe: redis.client.Pipeline, key: str) -> None:
        redis_obj = self._pipe_to_redis(pipe)
        length = redis_obj.llen(key)
        if not length:
            return
        rand_index = random.randint(0, length - 1)
        value = redis_obj.lindex(key, rand_index)
        if value is None:
            value = self._rand_str(self.subval_size)
        pipe.lpos(key, value)

    @cg_method(cmd_type="list", can_create_key=False)
    def blpop(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Use a short timeout for non-blocking test
        pipe.blpop(key, timeout=0.1)

    @cg_method(cmd_type="list", can_create_key=False)
    def brpop(self, pipe: redis.client.Pipeline, key: str) -> None:
        pipe.brpop(key, timeout=0.1)

    @cg_method(cmd_type="list", can_create_key=False)
    def rpoplpush(self, pipe: redis.client.Pipeline, key: str) -> None:
        redis_obj = self._pipe_to_redis(pipe)
        dst_key = self._scan_rand_key(redis_obj, "list") or self._rand_key("list")
        pipe.rpoplpush(key, dst_key)

    @cg_method(cmd_type="list", can_create_key=False)
    def brpoplpush(self, pipe: redis.client.Pipeline, key: str) -> None:
        redis_obj = self._pipe_to_redis(pipe)
        dst_key = self._scan_rand_key(redis_obj, "list") or self._rand_key("list")
        pipe.brpoplpush(key, dst_key, timeout=0.1)

    @cg_method(cmd_type="list", can_create_key=False)
    def linsert(self, pipe: redis.client.Pipeline, key: str) -> None:
        redis_obj = self._pipe_to_redis(pipe)
        length = redis_obj.llen(key)
        if not length:
            return
        # Pick a pivot value from the list or random
        rand_index = random.randint(0, length - 1)
        pivot = redis_obj.lindex(key, rand_index)
        value = self._rand_str(self.subval_size)
        # Randomly choose BEFORE or AFTER
        where = random.choice(["BEFORE", "AFTER"])
        pipe.linsert(key, where, pivot, value)

if __name__ == "__main__":
    list_gen = parse(ListGen)
    list_gen.distributions = '{"lpush": 100, "rpush": 100, "lpop": 100, "rpop": 100, "lrem": 100, "llen": 100, "lindex": 100, "lrange": 100, "lset": 100, "ltrim": 100, "lpos": 100, "blpop": 100, "brpop": 100, "rpoplpush": 100, "brpoplpush": 100, "linsert": 100}'
    list_gen._run()
