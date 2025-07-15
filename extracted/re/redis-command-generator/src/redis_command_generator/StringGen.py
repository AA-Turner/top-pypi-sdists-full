import redis
import random
from simple_parsing import parse
from dataclasses import dataclass
from redis_command_generator.BaseGen import BaseGen, cg_method

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

if __name__ == "__main__":
    string_gen = parse(StringGen)
    string_gen.distributions = '{"set": 100, "append": 100, "incrby": 100, "delete": 100}'
    string_gen._run()

