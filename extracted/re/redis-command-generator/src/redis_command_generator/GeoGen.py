import redis
import random
from simple_parsing import parse
from dataclasses import dataclass
from redis_command_generator.BaseGen import BaseGen, cg_method

geo_long_min: float = -180
geo_long_max: float = 180
geo_lat_min : float = -85.05112878
geo_lat_max : float = 85.05112878

@dataclass
class GeoGen(BaseGen):
    max_subelements: int = 10
    subval_size: int = 5
    
    @cg_method(cmd_type="geo", can_create_key=True)
    def geoadd(self, pipe: redis.client.Pipeline, key: str) -> None:
        members = []
        for _ in range(random.randint(1, self.max_subelements)):
            members += [random.uniform(geo_long_min, geo_long_max), random.uniform(geo_lat_min, geo_lat_max), self._rand_str(self.subval_size)]
        pipe.geoadd(key, members)
    
    @cg_method(cmd_type="geo", can_create_key=False)
    def geodel(self, pipe: redis.client.Pipeline, key: str) -> None:
        members = [self._rand_str(self.subval_size) for _ in range(random.randint(1, self.max_subelements))]
        pipe.zrem(key, *members)

if __name__ == "__main__":
    geo_gen = parse(GeoGen)
    geo_gen.distributions = '{"geoadd": 100, "geodel": 100}'
    geo_gen._run()
