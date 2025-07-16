import redis
import random
from simple_parsing import parse
from dataclasses import dataclass
from redis_command_generator.BaseGen import BaseGen, cg_method

@dataclass
class HyperLogLogGen(BaseGen):
    max_subelements: int = 10
    
    @cg_method(cmd_type="hll", can_create_key=True)
    def pfadd(self, pipe: redis.client.Pipeline, key: str) -> None:
        elements = [self._rand_str(self.def_key_size) for _ in range(random.randint(1, self.max_subelements))]
        pipe.pfadd(key, *elements)
    
    @cg_method(cmd_type="hll", can_create_key=False)
    def pfmerge(self, pipe: redis.client.Pipeline, key: str) -> None:
        redis_obj = self._pipe_to_redis(pipe)
        src_keys = [src_key for _ in range(random.randint(1, self.max_subelements)) if (src_key := self._scan_rand_key(redis_obj, "hll"))]
        pipe.pfmerge(key, *src_keys)
    
    @cg_method(cmd_type="hll", can_create_key=False)
    def pfcount(self, pipe: redis.client.Pipeline, key: str) -> None:
        redis_obj = self._pipe_to_redis(pipe)
        # Randomly decide to use single or multiple keys
        if random.random() < 0.5:
            # Single key
            pipe.pfcount(key)
        else:
            # Multi-key: gather other hll keys (including this one)
            keys = [key]
            for _ in range(random.randint(1, self.max_subelements - 1)):
                k = self._scan_rand_key(redis_obj, "hll")
                if k and k not in keys:
                    keys.append(k)
            pipe.pfcount(*keys)

if __name__ == "__main__":
    hyper_log_log_gen = parse(HyperLogLogGen)
    hyper_log_log_gen.distributions = '{"pfadd": 100, "pfmerge": 100, "pfcount": 100}'
    hyper_log_log_gen._run()
