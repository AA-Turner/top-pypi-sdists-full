import redis
import random
from simple_parsing import parse
from dataclasses import dataclass, field
from typing import List, Union
from redis_command_generator.BaseGen import BaseGen, cg_method
import time

@dataclass
class StringGen(BaseGen):
    subval_size: int = 5
    incrby_min: int = -1000
    incrby_max: int = 1000
    string_cond_precentages: List[int] = field(default_factory=lambda: [50, 50, 50, 50])  # Percentages for IFEQ/IFNE/IFDEQ/IFDNE conditional operations [IFEQ, IFNE, IFDEQ, IFDNE]

    @cg_method(cmd_type="string", can_create_key=True)
    def set(self, pipe: redis.client.Pipeline, key: str) -> None:
        pipe.set(key, self._rand_str(self.subval_size))

    @cg_method(cmd_type="string", can_create_key=True)
    def append(self, pipe: redis.client.Pipeline, key: str) -> None:
        pipe.append(key, self._rand_str(self.subval_size))

    @cg_method(cmd_type="string", can_create_key=True)
    def incrby(self, pipe: redis.client.Pipeline, key: str) -> None:
        pipe.incrby(key, random.randint(self.incrby_min, self.incrby_max))

    @cg_method(cmd_type="string", can_create_key=False)
    def delete(self, pipe: redis.client.Pipeline, key: str) -> None:
        pipe.delete(key)

    @cg_method(cmd_type="string", can_create_key=True)
    def setnx(self, pipe: redis.client.Pipeline, key: str) -> None:
        value = self._rand_str(self.subval_size)
        pipe.setnx(key, value)

    @cg_method(cmd_type="string", can_create_key=True)
    def setex(self, pipe: redis.client.Pipeline, key: str) -> None:
        value = self._rand_str(self.subval_size)
        ex = random.randint(1, 1000)
        pipe.setex(key, ex, value)

    @cg_method(cmd_type="string", can_create_key=True)
    def psetex(self, pipe: redis.client.Pipeline, key: str) -> None:
        value = self._rand_str(self.subval_size)
        px = random.randint(1, 1000000)
        pipe.psetex(key, px, value)

    @cg_method(cmd_type="string", can_create_key=False)
    def get(self, pipe: redis.client.Pipeline, key: str) -> None:
        pipe.get(key)

    @cg_method(cmd_type="string", can_create_key=True)
    def getset(self, pipe: redis.client.Pipeline, key: str) -> None:
        value = self._rand_str(self.subval_size)
        pipe.getset(key, value)

    @cg_method(cmd_type="string", can_create_key=False)
    def getdel(self, pipe: redis.client.Pipeline, key: str) -> None:
        pipe.getdel(key)

    def _get_expiry_kwargs(self, expiry_type: str) -> dict:
        """
        Generate expiry kwargs based on expiry type.

        Args:
            expiry_type: One of None, 'ex', 'px', 'exat', 'pxat', 'persist', 'EX', 'PX', 'EXAT', 'PXAT', 'KEEPTTL'

        Returns:
            Dictionary with expiry option as key and value
        """
        kwargs = {}
        if expiry_type is None:
            return kwargs

        expiry_lower = expiry_type.lower()

        if expiry_lower == 'ex':
            # Expire in seconds
            kwargs['ex'] = random.randint(1, 1000)
        elif expiry_lower == 'px':
            # Expire in milliseconds
            kwargs['px'] = random.randint(1, 1000000)
        elif expiry_lower == 'exat':
            # Expire at unix timestamp in seconds
            kwargs['exat'] = int(time.time()) + random.randint(1, 1000)
        elif expiry_lower == 'pxat':
            # Expire at unix timestamp in milliseconds
            kwargs['pxat'] = int(time.time() * 1000) + random.randint(1, 1000000)
        elif expiry_lower in ('persist', 'keepttl'):
            # Keep TTL or persist
            kwargs[expiry_lower] = True

        return kwargs

    @cg_method(cmd_type="string", can_create_key=False)
    def getex(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Randomly choose an expiry option
        expiry_type = random.choice(['ex', 'px', 'exat', 'pxat', 'persist'])
        kwargs = self._get_expiry_kwargs(expiry_type)
        pipe.getex(key, **kwargs)

    @cg_method(cmd_type="string", can_create_key=True)
    def mset(self, pipe: redis.client.Pipeline, key: str) -> None:
        mapping = {}
        hash_tag = self._rand_str(self.subval_size)
        use_same_htag = random.random() < 0.8

        for i in range(random.randint(1, 5)):
            mapping[f"{{{hash_tag}}}:{key}_{i}"] = self._rand_str(self.subval_size)
            if not use_same_htag:
                hash_tag = self._rand_str(self.subval_size)

        pipe.mset(mapping)

    @cg_method(cmd_type="string", can_create_key=True)
    def msetnx(self, pipe: redis.client.Pipeline, key: str) -> None:
        mapping = {}
        hash_tag = self._rand_str(self.subval_size)
        use_same_htag = random.random() < 0.8

        for i in range(random.randint(1, 5)):
            mapping[f"{{{hash_tag}}}:{key}_{i}"] = self._rand_str(self.subval_size)
            if not use_same_htag:
                hash_tag = self._rand_str(self.subval_size)

        pipe.msetnx(mapping)

    @cg_method(cmd_type="string", can_create_key=True)
    def msetex(self, pipe: redis.client.Pipeline, key: str) -> None:
        mapping = {}
        hash_tag = self._rand_str(self.subval_size)
        use_same_htag = random.random() < 0.8

        for i in range(random.randint(1, 5)):
            mapping[f"{{{hash_tag}}}:{key}_{i}"] = self._rand_str(self.subval_size)
            if not use_same_htag:
                hash_tag = self._rand_str(self.subval_size)

        # Choose a random expiry option
        expiry_option = random.choice([None, 'ex', 'px', 'exat', 'pxat', 'keepttl'])

        # Get expiry kwargs using shared function
        kwargs = self._get_expiry_kwargs(expiry_option)

        # Decide on optional flags (NX, XX)
        condition = random.choice([None, 'NX', 'XX'])

        # Build the key-value pairs list
        items = []
        for k, v in mapping.items():
            items.append(k)
            items.append(v)

        # MSETEX numkeys key value [key value ...] [NX | XX] [EX seconds | PX milliseconds | EXAT unix-time-seconds | PXAT unix-time-milliseconds | KEEPTTL]
        cmd = ['MSETEX', len(mapping)]
        cmd.extend(items)

        if condition:
            cmd.append(condition)

        if expiry_option is not None:
            cmd.append(expiry_option.upper())
            if expiry_option != 'keepttl':
                cmd.append(kwargs[expiry_option])

        pipe.execute_command(*cmd)

    @cg_method(cmd_type="string", can_create_key=False)
    def mget(self, pipe: redis.client.Pipeline, key: str) -> None:
        keys = [key]
        for _ in range(random.randint(1, 3)):
            keys.append(self._rand_str(self.subval_size))
        pipe.mget(keys)

    @cg_method(cmd_type="string", can_create_key=True)
    def incrbyfloat(self, pipe: redis.client.Pipeline, key: str) -> None:
        value = random.uniform(1, 1000)
        pipe.incrbyfloat(key, value)

    @cg_method(cmd_type="string", can_create_key=True)
    def decrby(self, pipe: redis.client.Pipeline, key: str) -> None:
        value = random.randint(1, 1000)
        pipe.decrby(key, value)

    @cg_method(cmd_type="string", can_create_key=False)
    def strlen(self, pipe: redis.client.Pipeline, key: str) -> None:
        pipe.strlen(key)

    @cg_method(cmd_type="string", can_create_key=False)
    def getrange(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Use a random range
        start = random.randint(0, 5)
        end = start + random.randint(0, 10)
        pipe.getrange(key, start, end)

    @cg_method(cmd_type="string", can_create_key=True)
    def setrange(self, pipe: redis.client.Pipeline, key: str) -> None:
        offset = random.randint(0, 5)
        value = self._rand_str(self.subval_size)
        pipe.setrange(key, offset, value)

    def _rand_hex_digest(self) -> str:
        """Generate a random 16-character hexadecimal digest."""
        return ''.join(random.choices('0123456789abcdef', k=16))

    def _get_digest(self, redis_obj: redis.Redis, key: str) -> str:
        """Get digest from Redis, fallback to random if unavailable."""
        try:
            digest = redis_obj.execute_command("DIGEST", key)
            return digest.decode('utf-8') if isinstance(digest, bytes) else digest
        except:
            return self._rand_hex_digest()

    def _get_conditional_comparison_value(self, flag: str, current_value: bytes, redis_obj: redis.Redis, key: str) -> Union[bytes, str]:
        flag_to_index = {'IFEQ': 0, 'IFNE': 1, 'IFDEQ': 2, 'IFDNE': 3}
        percentage = self.string_cond_precentages[flag_to_index[flag]]
        should_match = random.randint(1, 100) <= percentage

        is_digest_flag = flag in ['IFDEQ', 'IFDNE']
        is_equality_flag = flag in ['IFEQ', 'IFDEQ']

        # Determine if we want to match (equality flags) or not match (inequality flags)
        want_match = should_match if is_equality_flag else not should_match

        if is_digest_flag:
            if current_value is None or not want_match:
                return self._rand_hex_digest()
            return self._get_digest(redis_obj, key)
        else:
            if current_value is None or not want_match:
                return self._rand_str(self.subval_size)
            return current_value

    @cg_method(cmd_type="string", can_create_key=True)
    def set_conditional(self, pipe: redis.client.Pipeline, key: str) -> None:
        """Conditional SET with IFEQ/IFNE/IFDEQ/IFDNE flags for CRDT Redis."""
        value = self._rand_str(self.subval_size)
        flag = random.choice(['IFEQ', 'IFNE', 'IFDEQ', 'IFDNE'])

        redis_obj = self._pipe_to_redis(pipe)
        current_value = redis_obj.get(key)
        comparison_value = self._get_conditional_comparison_value(flag, current_value, redis_obj, key)

        pipe.execute_command("SET", key, value, flag, comparison_value)

    @cg_method(cmd_type="string", can_create_key=False)
    def delex(self, pipe: redis.client.Pipeline, key: str) -> None:
        """Conditional deletion with IFEQ/IFNE/IFDEQ/IFDNE flags for CRDT Redis."""
        flag = random.choice(['IFEQ', 'IFNE', 'IFDEQ', 'IFDNE'])

        redis_obj = self._pipe_to_redis(pipe)
        current_value = redis_obj.get(key)
        comparison_value = self._get_conditional_comparison_value(flag, current_value, redis_obj, key)

        pipe.execute_command("DELEX", key, flag, comparison_value)

    @cg_method(cmd_type="string", can_create_key=False)
    def digest(self, pipe: redis.client.Pipeline, key: str) -> None:
        """Get digest for CRDT string object."""
        pipe.execute_command("DIGEST", key)

if __name__ == "__main__":
    string_gen = parse(StringGen)
    string_gen.distributions = '{"set": 100, "append": 100, "incrby": 100, "delete": 100, "setnx": 100, "setex": 100, "psetex": 100, "get": 100, "getset": 100, "getdel": 100, "getex": 100, "mset": 100, "msetnx": 100, "msetex": 100, "mget": 100, "incrbyfloat": 100, "decrby": 100, "strlen": 100, "getrange": 100, "setrange": 100, "set_conditional": 100, "delex": 100, "digest": 100}'
    string_gen._run()

