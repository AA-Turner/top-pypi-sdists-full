import redis
import random
from simple_parsing import parse
from dataclasses import dataclass
from redis_command_generator.BaseGen import BaseGen, cg_method

@dataclass
class SetGen(BaseGen):
    max_subelements: int = 10
    subval_size: int = 5
    
    @cg_method(cmd_type="set", can_create_key=True)
    def sadd(self, pipe: redis.client.Pipeline, key: str) -> None:
        members = [self._rand_str(self.subval_size) for _ in range(random.randint(1, self.max_subelements))]
        pipe.sadd(key, *members)
    
    @cg_method(cmd_type="set", can_create_key=False)
    def srem(self, pipe: redis.client.Pipeline, key: str) -> None:
        redis_obj = self._pipe_to_redis(pipe)
        member = redis_obj.srandmember(key)
        if not member:
            return
        pipe.srem(key, member)

    @cg_method(cmd_type="set", can_create_key=False)
    def scard(self, pipe: redis.client.Pipeline, key: str) -> None:
        pipe.scard(key)

    @cg_method(cmd_type="set", can_create_key=False)
    def sismember(self, pipe: redis.client.Pipeline, key: str) -> None:
        redis_obj = self._pipe_to_redis(pipe)
        members = redis_obj.smembers(key)
        # 70% chance to use an existing member, else random
        if members and random.random() < 0.7:
            member = random.choice(list(members))
        else:
            member = self._rand_str(self.subval_size)
        pipe.sismember(key, member)

    @cg_method(cmd_type="set", can_create_key=False)
    def smembers(self, pipe: redis.client.Pipeline, key: str) -> None:
        pipe.smembers(key)

    @cg_method(cmd_type="set", can_create_key=False)
    def smove(self, pipe: redis.client.Pipeline, key: str) -> None:
        redis_obj = self._pipe_to_redis(pipe)
        # Find a random destination set (different from key)
        dest_key = self._scan_rand_key(redis_obj, "set") or self._rand_str(self.def_key_size)
        members = redis_obj.smembers(key)
        # 70% chance to use an existing member, else random
        if members and random.random() < 0.7:
            member = random.choice(list(members))
        else:
            member = self._rand_str(self.subval_size)
        pipe.smove(key, dest_key, member)

    @cg_method(cmd_type="set", can_create_key=False)
    def spop(self, pipe: redis.client.Pipeline, key: str) -> None:
        # 50% chance to pop a single or multiple members
        if random.random() < 0.5:
            pipe.spop(key)
        else:
            count = random.randint(1, self.max_subelements)
            pipe.spop(key, count)

    @cg_method(cmd_type="set", can_create_key=False)
    def srandmember(self, pipe: redis.client.Pipeline, key: str) -> None:
        # 50% chance to get a single or multiple members
        if random.random() < 0.5:
            pipe.srandmember(key)
        else:
            count = random.randint(1, self.max_subelements)
            pipe.srandmember(key, count)

    @cg_method(cmd_type="set", can_create_key=False)
    def sdiff(self, pipe: redis.client.Pipeline, key: str) -> None:
        redis_obj = self._pipe_to_redis(pipe)
        keys = [key]
        for _ in range(random.randint(1, self.max_subelements - 1)):
            k = self._scan_rand_key(redis_obj, "set")
            if k and k not in keys:
                keys.append(k)
        pipe.sdiff(*keys)

    @cg_method(cmd_type="set", can_create_key=True)
    def sdiffstore(self, pipe: redis.client.Pipeline, key: str) -> None:
        redis_obj = self._pipe_to_redis(pipe)
        dest_key = self._rand_str(self.def_key_size)
        keys = [key]
        for _ in range(random.randint(1, self.max_subelements - 1)):
            k = self._scan_rand_key(redis_obj, "set")
            if k and k not in keys:
                keys.append(k)
        pipe.sdiffstore(dest_key, *keys)

    @cg_method(cmd_type="set", can_create_key=False)
    def sinter(self, pipe: redis.client.Pipeline, key: str) -> None:
        redis_obj = self._pipe_to_redis(pipe)
        keys = [key]
        for _ in range(random.randint(1, self.max_subelements - 1)):
            k = self._scan_rand_key(redis_obj, "set")
            if k and k not in keys:
                keys.append(k)
        pipe.sinter(*keys)

    @cg_method(cmd_type="set", can_create_key=True)
    def sinterstore(self, pipe: redis.client.Pipeline, key: str) -> None:
        redis_obj = self._pipe_to_redis(pipe)
        dest_key = self._rand_str(self.def_key_size)
        keys = [key]
        for _ in range(random.randint(1, self.max_subelements - 1)):
            k = self._scan_rand_key(redis_obj, "set")
            if k and k not in keys:
                keys.append(k)
        pipe.sinterstore(dest_key, *keys)

    @cg_method(cmd_type="set", can_create_key=False)
    def sunion(self, pipe: redis.client.Pipeline, key: str) -> None:
        redis_obj = self._pipe_to_redis(pipe)
        keys = [key]
        for _ in range(random.randint(1, self.max_subelements - 1)):
            k = self._scan_rand_key(redis_obj, "set")
            if k and k not in keys:
                keys.append(k)
        pipe.sunion(*keys)

    @cg_method(cmd_type="set", can_create_key=True)
    def sunionstore(self, pipe: redis.client.Pipeline, key: str) -> None:
        redis_obj = self._pipe_to_redis(pipe)
        dest_key = self._rand_str(self.def_key_size)
        keys = [key]
        for _ in range(random.randint(1, self.max_subelements - 1)):
            k = self._scan_rand_key(redis_obj, "set")
            if k and k not in keys:
                keys.append(k)
        pipe.sunionstore(dest_key, *keys)
        
if __name__ == "__main__":
    set_gen = parse(SetGen)
    set_gen.distributions = '{"sadd": 100, "srem": 100, "scard": 100, "sismember": 100, "smembers": 100, "smove": 100, "spop": 100, "srandmember": 100, "sdiff": 100, "sdiffstore": 100, "sinter": 100, "sinterstore": 100, "sunion": 100, "sunionstore": 100}'
    set_gen._run()