import redis
import random
from simple_parsing import parse
from dataclasses import dataclass
from redis_command_generator.BaseGen import BaseGen, cg_method
from typing import Optional

KEY_TYPE = "MBbloomCF"

@dataclass
class CuckooGen(BaseGen):
    max_subelements: int = 1000
    subval_size: int = 5
    max_capacity: int = 1000
    max_items_per_insert: int = 10
    max_generated_header_size: int = 20

    @cg_method(cmd_type=KEY_TYPE, can_create_key=True)
    def cf_reserve(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Classification: initialization
        args = ["CF.RESERVE", key, random.randint(100, self.max_capacity)]
        if random.choice([True, False]):
            args.extend(["BUCKETSIZE", random.randint(2, 10)])
        if random.choice([True, False]):
            args.extend(["MAXITERATIONS", random.randint(1, 20)])
        if random.choice([True, False]):
            args.extend(["EXPANSION", random.randint(1, 100)])
        pipe.execute_command(*args)

    @cg_method(cmd_type=KEY_TYPE, can_create_key=True)
    def cf_add(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Classification: additive
        value = self._rand_str(self.subval_size)
        self._put_rand_value(KEY_TYPE, value)
        pipe.execute_command("CF.ADD", key, value)

    @cg_method(cmd_type=KEY_TYPE, can_create_key=True)
    def cf_addnx(self, pipe: redis.client.Pipeline, key: str) -> None:
       # Classification: additive
        value = self._rand_str(self.subval_size)
        self._put_rand_value(KEY_TYPE, value)
        pipe.execute_command("CF.ADDNX", key, value)

    def cf_insert_common(self, pipe: redis.client.Pipeline, key: Optional[str], args: Optional[list] = None) -> None:
        if args is None:
            args = []
        
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
        
        # Always add ITEMS
        items = [self._rand_str(self.subval_size) for _ in range(random.randint(1, self.max_items_per_insert))]
        args.append("ITEMS")
        args.extend(items)
        pipe.execute_command(*args)

    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def cf_insert(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Classification: initialization/additive
        args = ["CF.INSERT"]
        self.cf_insert_common(pipe, key, args)

    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def cf_insertnx(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Classification: initialization/additive
        args = ["CF.INSERTNX"]
        self.cf_insert_common(pipe, key, args)

    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def cf_exists(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Classification: lookup
        item = self._get_rand_value(key) or self._rand_str(self.subval_size)
        pipe.execute_command("CF.EXISTS", key, item)

    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def cf_mexists(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Classification: lookup
        items = [self._get_rand_value(key) or self._rand_str(self.subval_size) for _ in range(random.randint(1, self.max_items_per_insert))]
        pipe.execute_command("CF.MEXISTS", key, *items)

    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def cf_count(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Classification: lookup
        pipe.execute_command("CF.COUNT", key, self._get_rand_value(key) or self._rand_str(self.subval_size))

    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def cf_del(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Classification: removal
        pipe.execute_command("CF.DEL", key, self._get_rand_value(key) or self._rand_str(self.subval_size))


    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def cf_info(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Classification: lookup
        pipe.execute_command("CF.INFO", key)

    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def cf_scandump(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Classification: lookup
        redis_obj = self._pipe_to_redis(pipe)
        it, _ = redis_obj.cf().scandump(key, 0)
        while it is not 0:
            it, _ = redis_obj.cf().scandump(key, it)

    @cg_method(cmd_type=KEY_TYPE, can_create_key=True)
    def cf_loadchunk(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Classification: initialization
        byte_array = bytes([random.randint(0, 255) for _ in range(self.max_generated_header_size)])
        pipe.execute_command("CF.LOADCHUNK", key, 1, byte_array)

if __name__ == "__main__":
    cuckoo_gen = parse(CuckooGen)
    cuckoo_gen.distributions = '{"cf_reserve": 100, "cf_add": 100, "cf_addnx": 100, "cf_insert": 100, "cf_insertnx": 100, "cf_exists": 100, "cf_mexists": 100, "cf_count": 100, "cf_del": 100, "cf_info": 100, "cf_scandump": 100, "cf_loadchunk": 100}'
    cuckoo_gen._run()
