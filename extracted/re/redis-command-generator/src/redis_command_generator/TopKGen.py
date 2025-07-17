from typing import Optional
import redis
import random
from simple_parsing import parse
from dataclasses import dataclass
from redis_command_generator.BaseGen import BaseGen, cg_method

KEY_TYPE = "TopK-TYPE"

@dataclass
class TopKGen(BaseGen):
    max_k: int = 100
    max_width: int = 8
    max_depth: int = 7
    max_decay: float = 0.9
    subval_size: int = 5
    max_items_per_command: int = 10
    max_increment: int = 100
    min_increment: int = 1


    @cg_method(cmd_type=KEY_TYPE, can_create_key=True)
    def topk_reserve(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Classification: initialization
        
        k = random.randint(1, self.max_k)
        args = ["TOPK.RESERVE", key, k]
        
        # Optional parameters
        if random.choice([True, False]):
            width = random.randint(1, self.max_width)
            depth = random.randint(1, self.max_depth)
            decay = round(random.uniform(0.1, self.max_decay), 2)
            args.extend([width, depth, decay])
        
        pipe.execute_command(*args)

    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def topk_add(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Classification: additive
        
        # Generate items to add
        items = [self._rand_str(self.subval_size) for _ in range(random.randint(1, self.max_items_per_command))]
        for item in items:
            self._put_rand_value(KEY_TYPE, item)
        pipe.execute_command("TOPK.ADD", key, *items)

    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def topk_incrby(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Classification: additive
        
        # Generate item-increment pairs
        args = ["TOPK.INCRBY", key]
        num_items = random.randint(1, self.max_items_per_command)
        for _ in range(num_items):
            item = self._get_rand_value(key) or self._rand_str(self.subval_size)
            increment = random.randint(self.min_increment, self.max_increment)
            args.extend([item, str(increment)])
        
        pipe.execute_command(*args)

    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def topk_query(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Classification: lookup
        
        # Query multiple items
        items = [self._get_rand_value(key) or self._rand_str(self.subval_size) for _ in range(random.randint(1, self.max_items_per_command))]
        pipe.execute_command("TOPK.QUERY", key, *items)

    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def topk_count(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Classification: lookup
        
        # Count multiple items
        items = [self._get_rand_value(key) or self._rand_str(self.subval_size) for _ in range(random.randint(1, self.max_items_per_command))]
        pipe.execute_command("TOPK.COUNT", key, *items)

    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def topk_list(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Classification: lookup
        
        # Optionally include counts
        if random.choice([True, False]):
            pipe.execute_command("TOPK.LIST", key, "WITHCOUNT")
        else:
            pipe.execute_command("TOPK.LIST", key)

    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def topk_info(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Classification: lookup
        
        pipe.execute_command("TOPK.INFO", key)


if __name__ == "__main__":
    topk_gen = parse(TopKGen)
    topk_gen.distributions = '{"topk_reserve": 100, "topk_add": 200, "topk_incrby": 150, "topk_query": 150, "topk_count": 150, "topk_list": 100, "topk_info": 50}'
    topk_gen._run() 