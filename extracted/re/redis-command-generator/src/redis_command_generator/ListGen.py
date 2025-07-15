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

if __name__ == "__main__":
    list_gen = parse(ListGen)
    list_gen.distributions = '{"lpush": 100, "rpush": 100, "lpop": 100, "rpop": 100, "lrem": 100}'
    list_gen._run()
