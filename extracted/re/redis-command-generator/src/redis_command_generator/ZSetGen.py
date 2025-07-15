import redis
import random
from simple_parsing import parse
from dataclasses import dataclass
from redis_command_generator.BaseGen import BaseGen, cg_method

@dataclass
class ZSetGen(BaseGen):
    max_subelements: int = 10
    subval_size: int = 5
    
    @cg_method(cmd_type="zset", can_create_key=True)
    def zadd(self, pipe: redis.client.Pipeline, key: str) -> None:
        members = {self._rand_str(self.subval_size): random.random() for _ in range(random.randint(1, self.max_subelements))}
        pipe.zadd(key, mapping=members)
    
    @cg_method(cmd_type="zset", can_create_key=True)
    def zincrby(self, pipe: redis.client.Pipeline, key: str) -> None:
        member = self._rand_str(self.subval_size)
        increment = random.random()
        pipe.zincrby(key, increment, member)
    
    @cg_method(cmd_type="zset", can_create_key=False)
    def zrem(self, pipe: redis.client.Pipeline, key: str) -> None:
        members = [self._rand_str(self.subval_size) for _ in range(random.randint(1, self.max_subelements))]
        pipe.zrem(key, *members)

if __name__ == "__main__":
    zset_gen = parse(ZSetGen)
    zset_gen.distributions = '{"zadd": 100, "zincrby": 100, "zrem": 100}'
    zset_gen._run()
