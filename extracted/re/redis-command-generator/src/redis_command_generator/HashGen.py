import redis
import random
import time
from simple_parsing import parse
from dataclasses import dataclass
from redis_command_generator.BaseGen import BaseGen, cg_method
from redis.commands.core import HashDataPersistOptions

@dataclass
class HashGen(BaseGen):
    max_subelements: int = 10
    subkey_size: int = 5
    subval_size: int = 5
    incrby_min: int = -1000
    incrby_max: int = 1000
    
    @cg_method(cmd_type="hash", can_create_key=True)
    def hset(self, pipe: redis.client.Pipeline, key: str) -> None:
        fields = {self._rand_str(self.subkey_size): self._rand_str(self.subval_size) for _ in range(random.randint(1, self.max_subelements))}
        pipe.hset(key, mapping=fields)
    
    @cg_method(cmd_type="hash", can_create_key=True)
    def hincrby(self, pipe: redis.client.Pipeline, key: str) -> None:
        field = self._rand_str(self.def_key_size)
        increment = random.randint(self.incrby_min, self.incrby_max)
        pipe.hincrby(key, field, increment)
    
    @cg_method(cmd_type="hash", can_create_key=False)
    def hdel(self, pipe: redis.client.Pipeline, key: str) -> None:
        fields = [self._rand_str(self.subkey_size) for _ in range(random.randint(1, self.max_subelements))]
        pipe.hdel(key, *fields)
    
    @cg_method(cmd_type="hash", can_create_key=False)
    def hgetdel(self, pipe: redis.client.Pipeline, key: str) -> None:
        redis_obj = self._pipe_to_redis(pipe)
        fields = redis_obj.hkeys(key)
        pipe.hgetdel(key, *fields)
    
    @cg_method(cmd_type="hash", can_create_key=False)
    def hgetex(self, pipe: redis.client.Pipeline, key: str) -> None:
        redis_obj = self._pipe_to_redis(pipe)
        fields = redis_obj.hkeys(key)
        
        # Choose a random expiry option
        expiry_option = random.choice(['EX', 'PX', 'EXAT', 'PXAT', 'PERSIST'])
        
        # Prepare keyword arguments for expiry options
        kwargs = {}
        if expiry_option == 'EX':
            # Expire in seconds
            kwargs['ex'] = random.randint(self.ttl_low, self.ttl_high)
        elif expiry_option == 'PX':
            # Expire in milliseconds
            kwargs['px'] = random.randint(self.ttl_low * 1000, self.ttl_high * 1000)
        elif expiry_option == 'EXAT':
            # Expire at unix timestamp in seconds
            kwargs['exat'] = int(time.time()) + random.randint(self.ttl_low, self.ttl_high)
        elif expiry_option == 'PXAT':
            # Expire at unix timestamp in milliseconds
            kwargs['pxat'] = int(time.time() * 1000) + random.randint(self.ttl_low * 1000, self.ttl_high * 1000)
        elif expiry_option == 'PERSIST':
            kwargs['persist'] = True
        
        pipe.hgetex(key, *fields, **kwargs)
    
    @cg_method(cmd_type="hash", can_create_key=True)
    def hsetex(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Choose a random expiry option
        expiry_option = random.choice(['EX', 'PX', 'EXAT', 'PXAT', 'KEEPTTL'])
        
        # Prepare kwargs for the command
        kwargs = {}
        
        # Decide on optional flags (FNX, FXX)
        data_persist_option = random.choice([None, HashDataPersistOptions.FNX, HashDataPersistOptions.FXX])
        if data_persist_option:
            kwargs['data_persist_option'] = data_persist_option
        
        # Add expiry option
        if expiry_option == 'EX':
            # Expire in seconds
            kwargs['ex'] = random.randint(self.ttl_low, self.ttl_high)
        elif expiry_option == 'PX':
            # Expire in milliseconds
            kwargs['px'] = random.randint(self.ttl_low * 1000, self.ttl_high * 1000)
        elif expiry_option == 'EXAT':
            # Expire at unix timestamp in seconds
            kwargs['exat'] = int(time.time()) + random.randint(self.ttl_low, self.ttl_high)
        elif expiry_option == 'PXAT':
            # Expire at unix timestamp in milliseconds
            kwargs['pxat'] = int(time.time() * 1000) + random.randint(self.ttl_low * 1000, self.ttl_high * 1000)
        elif expiry_option == 'KEEPTTL':
            kwargs['keepttl'] = True
        
        items = []
        for _ in range(random.randint(1, self.max_subelements)):
            items.append(self._rand_str(self.subkey_size))  # Field
            items.append(self._rand_str(self.subval_size))  # Value
        pipe.hsetex(key, items=items, **kwargs)

if __name__ == "__main__":
    hash_gen = parse(HashGen)
    hash_gen.distributions = '{"hset": 100, "hincrby": 100, "hdel": 100, "hgetdel": 100, "hgetex": 100, "hsetex": 100}'
    hash_gen._run()
