from typing import Optional
import redis
import random
from simple_parsing import parse
from dataclasses import dataclass
from redis_command_generator.BaseGen import BaseGen, cg_method

KEY_TYPE = "MBbloom--"

@dataclass
class BloomGen(BaseGen):
    max_error_rate: float = 0.01
    max_capacity: int = 1000
    subval_size: int = 5
    max_items_per_insert: int = 10
    max_generated_header_size: int = 20

    @cg_method(cmd_type=KEY_TYPE, can_create_key=True)
    def bf_add(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Classification: additive
        value = self._rand_str(self.subval_size)
        self._put_rand_value(KEY_TYPE, value)
        pipe.execute_command("BF.ADD", key, value)

    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def bf_card(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Classification: lookup
        pipe.execute_command("BF.CARD", key)

    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def bf_exists(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Classification: lookup
        value = self._get_rand_value(key) or self._rand_str(self.subval_size)
        pipe.execute_command("BF.EXISTS", key, value)

    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def bf_info(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Classification: lookup
        pipe.execute_command("BF.INFO", key)

    @cg_method(cmd_type=KEY_TYPE, can_create_key=True)
    def bf_insert(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Classification: initialization/additive
        # Randomly decide whether to use optional arguments
        args = ["BF.INSERT"]
        new_key = True
        if random.choice([True, False]):
            redis_obj = self._pipe_to_redis(pipe)
            key = self._scan_rand_key(redis_obj, KEY_TYPE)
            new_key = key is None
        
        if new_key:
            key = self._rand_key(KEY_TYPE)
            args.append(key)
        else:
             # If key exists, insert to existing key
            args.extend([key, "NOCREATE"])

        if random.choice([True, False]):
            args.extend(["CAPACITY", random.randint(100, self.max_capacity)])
        if random.choice([True, False]):
            args.extend(["ERROR", round(random.uniform(self.max_error_rate / 10 , self.max_error_rate), 4)])
        if random.choice([True, False]):
            args.extend(["EXPANSION", random.randint(1, 10)])
        # Always add ITEMS
        items = [self._get_rand_value(key) or self._rand_str(self.subval_size) for _ in range(random.randint(1, self.max_items_per_insert))]
        for item in items:
            self._put_rand_value(KEY_TYPE, item)
        args.append("ITEMS")
        args.extend(items)
        pipe.execute_command(*args)

    @cg_method(cmd_type=KEY_TYPE, can_create_key=True)
    def bf_loadchunk(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Classification: initialization
        byte_array = bytes([random.randint(0, 255) for _ in range(self.max_generated_header_size)])
        pipe.execute_command("BF.LOADCHUNK", key, 1, byte_array)

    @cg_method(cmd_type=KEY_TYPE, can_create_key=True)
    def bf_madd(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Classification: additive
        items = [self._rand_str(self.subval_size) for _ in range(random.randint(1, self.max_items_per_insert))]
        for item in items:
            self._put_rand_value(KEY_TYPE, item)
        pipe.execute_command("BF.MADD", key, *items)

    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def bf_mexists(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Classification: lookup
        items = [self._get_rand_value(key) or self._rand_str(self.subval_size) for _ in range(random.randint(1, self.max_items_per_insert))]
        pipe.execute_command("BF.MEXISTS", key, *items)
        

    @cg_method(cmd_type=KEY_TYPE, can_create_key=True)
    def bf_reserve(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Classification: initialization
        pipe.execute_command("BF.RESERVE", key, self.max_error_rate, self.max_capacity)
    
    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def bf_scandump(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Classification: lookup
        redis_obj = self._pipe_to_redis(pipe)
        it, _ = redis_obj.bf().scandump(key, 0)
        while it is not 0:
            it, _ = redis_obj.bf().scandump(key, it)



if __name__ == "__main__":
    bloom_gen = parse(BloomGen)
    bloom_gen.distributions = '{"bf_reserve": 100, "bf_add": 100, "bf_exists": 100, "bf_card": 100, "bf_insert": 100, "bf_madd": 100, "bf_mexists": 100, "bf_scandump": 100, "bf_info": 100, "bf_loadchunk": 100}'
    bloom_gen._run()

