import redis
import random
from simple_parsing import parse
from dataclasses import dataclass
from redis_command_generator.BaseGen import BaseGen, cg_method

@dataclass
class BitmapGen(BaseGen):
    max_subelements: int = 1000
    
    @cg_method(cmd_type="bit", can_create_key=True)
    def setbit(self, pipe: redis.client.Pipeline, key: str) -> None:
        offset = random.randint(0, self.max_subelements)
        value = random.randint(0, 1)
        pipe.setbit(key, offset, value)
    
    @cg_method(cmd_type="bit", can_create_key=False)
    def getbit(self, pipe: redis.client.Pipeline, key: str) -> None:
        offset = random.randint(0, self.max_subelements)
        pipe.getbit(key, offset)

if __name__ == "__main__":
    bitmap_gen = parse(BitmapGen)
    bitmap_gen.distributions = '{"setbit": 100, "getbit": 100}'
    bitmap_gen._run()
