import redis
import random
from simple_parsing import parse
from dataclasses import dataclass
from redis_command_generator.BaseGen import BaseGen, cg_method

@dataclass
class SetGen(BaseGen):
    max_subelements: int = 10
    subval_size: int = 5
    
    @cg_method(cmd_type="set", can_create_key=True)
    def sadd(self, pipe: redis.client.Pipeline, key: str) -> None:
        members = [self._rand_str(self.subval_size) for _ in range(random.randint(1, self.max_subelements))]
        pipe.sadd(key, *members)
    
    @cg_method(cmd_type="set", can_create_key=False)
    def srem(self, pipe: redis.client.Pipeline, key: str) -> None:
        redis_obj = self._pipe_to_redis(pipe)
        member = redis_obj.srandmember(key)
        if not member:
            return
        pipe.srem(key, member)

if __name__ == "__main__":
    set_gen = parse(SetGen)
    set_gen.distributions = '{"sadd": 100, "srem": 100}'
    set_gen._run()