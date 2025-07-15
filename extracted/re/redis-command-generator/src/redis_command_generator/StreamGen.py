import redis
import random
from simple_parsing import parse
from dataclasses import dataclass
from redis_command_generator.BaseGen import BaseGen, cg_method

@dataclass
class StreamGen(BaseGen):
    max_subelements: int = 10
    subkey_size: int = 5
    subval_size: int = 5
    
    @cg_method(cmd_type="stream", can_create_key=True)
    def xadd(self, pipe: redis.client.Pipeline, key: str) -> None:
        fields = {self._rand_str(self.subkey_size): self._rand_str(self.subval_size) for _ in range(random.randint(1, self.max_subelements))}
        pipe.xadd(key, fields)
    
    @cg_method(cmd_type="stream", can_create_key=False)
    def xdel(self, pipe: redis.client.Pipeline, key: str) -> None:
        stream_len = random.randint(0, 10)
        if stream_len > 0:
            stream_id = f"{random.randint(1, 1000)}-0"
            pipe.xdel(key, stream_id)

if __name__ == "__main__":
    stream_gen = parse(StreamGen)
    stream_gen.distributions = '{"xadd": 100, "xdel": 100}'
    stream_gen._run()
