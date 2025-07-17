from typing import Optional
import redis
import random
from simple_parsing import parse
from dataclasses import dataclass
from redis_command_generator.BaseGen import BaseGen, cg_method

KEY_TYPE = "CMSk-TYPE"

@dataclass
class CmsGen(BaseGen):
    max_error_rate: float = 0.01
    max_probability: float = 0.02
    max_width: int = 3
    max_depth: int = 3
    subval_size: int = 5
    max_items_per_command: int = 10
    max_increment: int = 100


    @cg_method(cmd_type=KEY_TYPE, can_create_key=True)
    def cms_initbydim(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Classification: initialization
        width = random.randint(1, self.max_width)
        depth = random.randint(1, self.max_depth)
        pipe.execute_command("CMS.INITBYDIM", key, width, depth)

    @cg_method(cmd_type=KEY_TYPE, can_create_key=True)
    def cms_initbyprob(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Classification: initialization
        error = round(random.uniform(self.max_error_rate / 10, self.max_error_rate), 6)
        probability = round(random.uniform(self.max_probability / 10, self.max_probability), 6)
        pipe.execute_command("CMS.INITBYPROB", key, error, probability)

    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def cms_incrby(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Classification: additive
        
        args = ["CMS.INCRBY", key]
        num_items = random.randint(1, self.max_items_per_command)
        for _ in range(num_items):
            item = self._rand_str(self.subval_size)
            self._put_rand_value(key, item)
            increment = random.randint(1, self.max_increment)
            args.extend([item, str(increment)])
        
        pipe.execute_command(*args)

    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def cms_query(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Classification: lookup
        
        # Query multiple items
        items = [self._get_rand_value(key) or self._rand_str(self.subval_size) for _ in range(random.randint(1, self.max_items_per_command))]
        pipe.execute_command("CMS.QUERY", key, *items)

    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def cms_info(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Classification: lookup
        pipe.execute_command("CMS.INFO", key)

    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def cms_merge(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Classification: initialization/additive
        redis_obj = self._pipe_to_redis(pipe)
        
        # Find existing CMS keys to merge
        existing_keys = []
        for _ in range(random.randint(2, 5)):  # Try to find 2-5 keys
            existing_key = self._scan_rand_key(redis_obj, KEY_TYPE)
            if existing_key and existing_key not in existing_keys:
                existing_keys.append(existing_key)
        
        if len(existing_keys) < 2:
            return  # Need at least 2 keys to merge
                
        # Build merge command
        args = ["CMS.MERGE", key, str(len(existing_keys))]
        args.extend(existing_keys)
        
        # Randomly add weights
        if random.choice([True, False]):
            args.append("WEIGHTS")
            weights = [str(random.randint(1, 10)) for _ in range(len(existing_keys))]
            args.extend(weights)
        
        pipe.execute_command(*args)


if __name__ == "__main__":
    cms_gen = parse(CmsGen)
    cms_gen.distributions = '{"cms_initbyprob": 1000, "cms_initbydim": 1000, "cms_incrby": 100, "cms_query": 300, "cms_info": 300, "cms_merge": 300}'
    cms_gen._run()
