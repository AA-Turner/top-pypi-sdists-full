import redis
import random
from simple_parsing import parse
from dataclasses import dataclass
from redis_command_generator.BaseGen import BaseGen, cg_method

@dataclass
class ZSetGen(BaseGen):
    max_subelements: int = 10
    subval_size: int = 5
    
    @cg_method(cmd_type="zset", can_create_key=True)
    def zadd(self, pipe: redis.client.Pipeline, key: str) -> None:
        members = {self._rand_str(self.subval_size): random.random() for _ in range(random.randint(1, self.max_subelements))}
        pipe.zadd(key, mapping=members)
    
    @cg_method(cmd_type="zset", can_create_key=True)
    def zincrby(self, pipe: redis.client.Pipeline, key: str) -> None:
        member = self._rand_str(self.subval_size)
        increment = random.random()
        pipe.zincrby(key, increment, member)
    
    @cg_method(cmd_type="zset", can_create_key=False)
    def zrem(self, pipe: redis.client.Pipeline, key: str) -> None:
        members = [self._rand_str(self.subval_size) for _ in range(random.randint(1, self.max_subelements))]
        pipe.zrem(key, *members)

    # Basic read operations
    @cg_method(cmd_type="zset", can_create_key=False)
    def zcard(self, pipe: redis.client.Pipeline, key: str) -> None:
        pipe.zcard(key)

    @cg_method(cmd_type="zset", can_create_key=False)
    def zcount(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Generate random score range (min <= max)
        min_score = random.uniform(-100, 100)
        max_score = random.uniform(min_score, min_score + 200)
        # Sometimes use inclusive/exclusive bounds
        min_bound = random.choice([f"({min_score}", str(min_score), "-inf"])
        max_bound = random.choice([f"({max_score}", str(max_score), "+inf"])
        pipe.zcount(key, min_bound, max_bound)

    @cg_method(cmd_type="zset", can_create_key=False)
    def zscore(self, pipe: redis.client.Pipeline, key: str) -> None:
        redis_obj = self._pipe_to_redis(pipe)
        # 70% chance existing member (like sismember pattern), 30% random
        members = redis_obj.zrange(key, 0, -1)
        if members and random.random() < 0.7:
            member = random.choice(members)
        else:
            member = self._rand_str(self.subval_size)
        pipe.zscore(key, member)

    @cg_method(cmd_type="zset", can_create_key=False)
    def zmscore(self, pipe: redis.client.Pipeline, key: str) -> None:
        redis_obj = self._pipe_to_redis(pipe)
        members = redis_obj.zrange(key, 0, -1)
        if members:
            # Select 1-3 existing members
            num_members = min(random.randint(1, 3), len(members))
            selected_members = random.sample(members, num_members)
        else:
            # Use random members
            selected_members = [self._rand_str(self.subval_size) for _ in range(random.randint(1, 3))]
        pipe.zmscore(key, selected_members)

    @cg_method(cmd_type="zset", can_create_key=False)
    def zrank(self, pipe: redis.client.Pipeline, key: str) -> None:
        redis_obj = self._pipe_to_redis(pipe)
        # Similar pattern to zscore - prefer existing members
        members = redis_obj.zrange(key, 0, -1)
        if members and random.random() < 0.7:
            member = random.choice(members)
        else:
            member = self._rand_str(self.subval_size)
        # Randomly include withscore parameter
        withscore = random.random() < 0.5
        pipe.zrank(key, member, withscore=withscore)

    @cg_method(cmd_type="zset", can_create_key=False)
    def zrevrank(self, pipe: redis.client.Pipeline, key: str) -> None:
        redis_obj = self._pipe_to_redis(pipe)
        members = redis_obj.zrange(key, 0, -1)
        if members and random.random() < 0.7:
            member = random.choice(members)
        else:
            member = self._rand_str(self.subval_size)
        # Randomly include withscore parameter
        withscore = random.random() < 0.5
        pipe.zrevrank(key, member, withscore=withscore)

    # Range operations
    @cg_method(cmd_type="zset", can_create_key=False)
    def zrange(self, pipe: redis.client.Pipeline, key: str) -> None:
        redis_obj = self._pipe_to_redis(pipe)
        zcard = redis_obj.zcard(key) or 10  # fallback if empty
        
        # Generate valid range (start <= stop)
        start = random.randint(-zcard, zcard-1) if zcard > 0 else 0
        end = random.randint(start, zcard-1) if zcard > 0 else -1
        
        # 50% chance to include scores (like hrandfield pattern)
        withscores = random.random() < 0.5
        pipe.zrange(key, start, end, withscores=withscores)

    @cg_method(cmd_type="zset", can_create_key=False)
    def zrevrange(self, pipe: redis.client.Pipeline, key: str) -> None:
        redis_obj = self._pipe_to_redis(pipe)
        zcard = redis_obj.zcard(key) or 10
        start = random.randint(-zcard, zcard-1) if zcard > 0 else 0
        end = random.randint(start, zcard-1) if zcard > 0 else -1
        withscores = random.random() < 0.5
        pipe.zrevrange(key, start, end, withscores=withscores)

    @cg_method(cmd_type="zset", can_create_key=False)
    def zrangebyscore(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Generate score range with various bound types
        min_score = random.uniform(-100, 100)
        max_score = random.uniform(min_score, min_score + 200)
        
        # Random bound inclusivity (like zcount)
        min_bound = random.choice([f"({min_score}", str(min_score), "-inf"])
        max_bound = random.choice([f"({max_score}", str(max_score), "+inf"])
        
        # Optional parameters (like mget pattern)
        kwargs = {}
        if random.random() < 0.5:
            kwargs['withscores'] = True
        if random.random() < 0.3:
            kwargs['start'] = random.randint(0, 10)
            kwargs['num'] = random.randint(1, 20)
        
        pipe.zrangebyscore(key, min_bound, max_bound, **kwargs)

    @cg_method(cmd_type="zset", can_create_key=False)
    def zrevrangebyscore(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Same pattern as zrangebyscore but with reversed min/max
        min_score = random.uniform(-100, 100)
        max_score = random.uniform(min_score, min_score + 200)
        
        # Note: for zrevrangebyscore, max comes first, then min
        max_bound = random.choice([f"({max_score}", str(max_score), "+inf"])
        min_bound = random.choice([f"({min_score}", str(min_score), "-inf"])
        
        kwargs = {}
        if random.random() < 0.5:
            kwargs['withscores'] = True
        if random.random() < 0.3:
            kwargs['start'] = random.randint(0, 10)
            kwargs['num'] = random.randint(1, 20)
        
        pipe.zrevrangebyscore(key, max_bound, min_bound, **kwargs)

    @cg_method(cmd_type="zset", can_create_key=False)
    def zrangebylex(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Generate lexicographical range
        start_char = random.choice(['a', 'b', 'c', 'd'])
        end_char = chr(ord(start_char) + random.randint(1, 5))
        
        min_bound = random.choice([f"[{start_char}", f"({start_char}", "-"])
        max_bound = random.choice([f"[{end_char}", f"({end_char}", "+"])
        
        kwargs = {}
        if random.random() < 0.3:
            kwargs['start'] = random.randint(0, 10)
            kwargs['num'] = random.randint(1, 20)
        
        pipe.zrangebylex(key, min_bound, max_bound, **kwargs)

    @cg_method(cmd_type="zset", can_create_key=False)
    def zrevrangebylex(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Generate lexicographical range (note reversed order for zrevrangebylex)
        start_char = random.choice(['a', 'b', 'c', 'd'])
        end_char = chr(ord(start_char) + random.randint(1, 5))
        
        # For zrevrangebylex, max comes first, then min
        max_bound = random.choice([f"[{end_char}", f"({end_char}", "+"])
        min_bound = random.choice([f"[{start_char}", f"({start_char}", "-"])
        
        kwargs = {}
        if random.random() < 0.3:
            kwargs['start'] = random.randint(0, 10)
            kwargs['num'] = random.randint(1, 20)
        
        pipe.zrevrangebylex(key, max_bound, min_bound, **kwargs)

    # Pop operations
    @cg_method(cmd_type="zset", can_create_key=False)
    def zpopmax(self, pipe: redis.client.Pipeline, key: str) -> None:
        # 50% chance single pop, 50% multiple (like spop pattern)
        if random.random() < 0.5:
            pipe.zpopmax(key)
        else:
            count = random.randint(1, self.max_subelements)
            pipe.zpopmax(key, count)

    @cg_method(cmd_type="zset", can_create_key=False)
    def zpopmin(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Same pattern as zpopmax
        if random.random() < 0.5:
            pipe.zpopmin(key)
        else:
            count = random.randint(1, self.max_subelements)
            pipe.zpopmin(key, count)

    # Random member operation
    @cg_method(cmd_type="zset", can_create_key=False)
    def zrandmember(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Similar to hrandfield and srandmember patterns
        if random.random() < 0.5:
            pipe.zrandmember(key)
        else:
            count = random.randint(1, self.max_subelements)
            withscores = random.random() < 0.5
            pipe.zrandmember(key, count, withscores=withscores)

    # Set operations
    @cg_method(cmd_type="zset", can_create_key=True)
    def zunionstore(self, pipe: redis.client.Pipeline, key: str) -> None:
        redis_obj = self._pipe_to_redis(pipe)
        dest_key = self._rand_str(self.def_key_size)
        
        # Build source keys list (like sinterstore pattern)
        keys = [key]
        for _ in range(random.randint(1, self.max_subelements - 1)):
            k = self._scan_rand_key(redis_obj, "zset")
            if k and k not in keys:
                keys.append(k)
        
        # 50% chance to use weights by converting to dict format
        if random.random() < 0.5:
            weights = [random.uniform(0.1, 2.0) for _ in keys]
            keys_dict = {k: w for k, w in zip(keys, weights)}
            keys_param = keys_dict
        else:
            keys_param = keys
            
        # Optional aggregate function
        aggregate = None
        if random.random() < 0.3:
            aggregate = random.choice(['SUM', 'MIN', 'MAX'])
            
        pipe.zunionstore(dest_key, keys_param, aggregate=aggregate)

    @cg_method(cmd_type="zset", can_create_key=True)
    def zinterstore(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Same pattern as zunionstore but intersection
        redis_obj = self._pipe_to_redis(pipe)
        dest_key = self._rand_str(self.def_key_size)
        keys = [key]
        for _ in range(random.randint(1, self.max_subelements - 1)):
            k = self._scan_rand_key(redis_obj, "zset")
            if k and k not in keys:
                keys.append(k)
        
        # 50% chance to use weights by converting to dict format
        if random.random() < 0.5:
            weights = [random.uniform(0.1, 2.0) for _ in keys]
            keys_dict = {k: w for k, w in zip(keys, weights)}
            keys_param = keys_dict
        else:
            keys_param = keys
            
        # Optional aggregate function
        aggregate = None
        if random.random() < 0.3:
            aggregate = random.choice(['SUM', 'MIN', 'MAX'])
            
        pipe.zinterstore(dest_key, keys_param, aggregate=aggregate)

    @cg_method(cmd_type="zset", can_create_key=False)
    def zunion(self, pipe: redis.client.Pipeline, key: str) -> None:
        redis_obj = self._pipe_to_redis(pipe)
        keys = [key]
        for _ in range(random.randint(1, self.max_subelements - 1)):
            k = self._scan_rand_key(redis_obj, "zset")
            if k and k not in keys:
                keys.append(k)
        
        kwargs = {}
        if random.random() < 0.5:
            kwargs['withscores'] = True
        if random.random() < 0.3:
            kwargs['aggregate'] = random.choice(['SUM', 'MIN', 'MAX'])
        
        pipe.zunion(keys, **kwargs)

    @cg_method(cmd_type="zset", can_create_key=False)
    def zinter(self, pipe: redis.client.Pipeline, key: str) -> None:
        redis_obj = self._pipe_to_redis(pipe)
        keys = [key]
        for _ in range(random.randint(1, self.max_subelements - 1)):
            k = self._scan_rand_key(redis_obj, "zset")
            if k and k not in keys:
                keys.append(k)
        
        kwargs = {}
        if random.random() < 0.5:
            kwargs['withscores'] = True
        if random.random() < 0.3:
            kwargs['aggregate'] = random.choice(['SUM', 'MIN', 'MAX'])
        
        pipe.zinter(keys, **kwargs)

    @cg_method(cmd_type="zset", can_create_key=False)
    def zdiff(self, pipe: redis.client.Pipeline, key: str) -> None:
        redis_obj = self._pipe_to_redis(pipe)
        keys = [key]
        for _ in range(random.randint(1, self.max_subelements - 1)):
            k = self._scan_rand_key(redis_obj, "zset")
            if k and k not in keys:
                keys.append(k)
        
        withscores = random.random() < 0.5
        pipe.zdiff(keys, withscores=withscores)

    @cg_method(cmd_type="zset", can_create_key=True)
    def zdiffstore(self, pipe: redis.client.Pipeline, key: str) -> None:
        redis_obj = self._pipe_to_redis(pipe)
        dest_key = self._rand_str(self.def_key_size)
        keys = [key]
        for _ in range(random.randint(1, self.max_subelements - 1)):
            k = self._scan_rand_key(redis_obj, "zset")
            if k and k not in keys:
                keys.append(k)
        
        pipe.zdiffstore(dest_key, keys)

    # Remove range operations
    @cg_method(cmd_type="zset", can_create_key=False)
    def zremrangebyrank(self, pipe: redis.client.Pipeline, key: str) -> None:
        redis_obj = self._pipe_to_redis(pipe)
        zcard = redis_obj.zcard(key) or 10
        
        start = random.randint(0, max(0, zcard - 1))
        stop = random.randint(start, max(start, zcard - 1))
        pipe.zremrangebyrank(key, start, stop)

    @cg_method(cmd_type="zset", can_create_key=False)
    def zremrangebyscore(self, pipe: redis.client.Pipeline, key: str) -> None:
        min_score = random.uniform(-100, 100)
        max_score = random.uniform(min_score, min_score + 200)
        
        min_bound = random.choice([f"({min_score}", str(min_score), "-inf"])
        max_bound = random.choice([f"({max_score}", str(max_score), "+inf"])
        
        pipe.zremrangebyscore(key, min_bound, max_bound)

    @cg_method(cmd_type="zset", can_create_key=False)
    def zremrangebylex(self, pipe: redis.client.Pipeline, key: str) -> None:
        start_char = random.choice(['a', 'b', 'c', 'd'])
        end_char = chr(ord(start_char) + random.randint(1, 5))
        
        min_bound = random.choice([f"[{start_char}", f"({start_char}", "-"])
        max_bound = random.choice([f"[{end_char}", f"({end_char}", "+"])
        
        pipe.zremrangebylex(key, min_bound, max_bound)

    # Scan operation
    @cg_method(cmd_type="zset", can_create_key=False)
    def zscan(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Similar to hscan pattern
        cursor = random.randint(0, 1000)
        kwargs = {}
        
        # Optional match pattern
        if random.random() < 0.5:
            kwargs['match'] = f"{self._rand_str(2)}*"
        
        # Optional count
        kwargs['count'] = random.randint(1, self.max_subelements)
        
        pipe.zscan(key, cursor=cursor, **kwargs)

    # Blocking pop operations
    @cg_method(cmd_type="zset", can_create_key=False)
    def bzpopmin(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Blocking pop with timeout (like blpop pattern)
        redis_obj = self._pipe_to_redis(pipe)
        keys = [key]
        # Sometimes add more keys
        for _ in range(random.randint(0, 2)):
            k = self._scan_rand_key(redis_obj, "zset")
            if k and k not in keys:
                keys.append(k)
        pipe.bzpopmin(keys, timeout=0.1)

    @cg_method(cmd_type="zset", can_create_key=False) 
    def bzpopmax(self, pipe: redis.client.Pipeline, key: str) -> None:
        redis_obj = self._pipe_to_redis(pipe)
        keys = [key]
        for _ in range(random.randint(0, 2)):
            k = self._scan_rand_key(redis_obj, "zset")
            if k and k not in keys:
                keys.append(k)
        pipe.bzpopmax(keys, timeout=0.1)

    # Multi-key pop operations
    @cg_method(cmd_type="zset", can_create_key=False)
    def zmpop(self, pipe: redis.client.Pipeline, key: str) -> None:
        redis_obj = self._pipe_to_redis(pipe)
        keys = [key]
        for _ in range(random.randint(0, 2)):
            k = self._scan_rand_key(redis_obj, "zset")
            if k and k not in keys:
                keys.append(k)
        
        # Random direction and count
        min_pop = random.random() < 0.5
        max_pop = not min_pop
        count = random.randint(1, self.max_subelements)
        
        pipe.zmpop(len(keys), keys, min=min_pop, max=max_pop, count=count)

    @cg_method(cmd_type="zset", can_create_key=False)
    def bzmpop(self, pipe: redis.client.Pipeline, key: str) -> None:
        redis_obj = self._pipe_to_redis(pipe)
        keys = [key]
        for _ in range(random.randint(0, 2)):
            k = self._scan_rand_key(redis_obj, "zset")
            if k and k not in keys:
                keys.append(k)
        
        min_pop = random.random() < 0.5
        max_pop = not min_pop
        count = random.randint(1, self.max_subelements)
        
        pipe.bzmpop(0.1, len(keys), keys, min=min_pop, max=max_pop, count=count)

    # Set operation cardinality
    @cg_method(cmd_type="zset", can_create_key=False)
    def zintercard(self, pipe: redis.client.Pipeline, key: str) -> None:
        redis_obj = self._pipe_to_redis(pipe)
        keys = [key]
        for _ in range(random.randint(1, self.max_subelements - 1)):
            k = self._scan_rand_key(redis_obj, "zset")
            if k and k not in keys:
                keys.append(k)
        
        # Optional limit parameter
        limit = random.randint(1, 100) if random.random() < 0.5 else 0
        pipe.zintercard(len(keys), keys, limit=limit)

    # Range store operation  
    @cg_method(cmd_type="zset", can_create_key=True)
    def zrangestore(self, pipe: redis.client.Pipeline, key: str) -> None:
        redis_obj = self._pipe_to_redis(pipe)
        dest_key = self._rand_str(self.def_key_size)
        zcard = redis_obj.zcard(key) or 10
        
        # Generate range parameters
        start = random.randint(0, max(0, zcard - 1))
        end = random.randint(start, max(start, zcard - 1))
        
        # Optional parameters
        kwargs = {}
        byscore_or_bylex = False
        
        if random.random() < 0.3:
            kwargs['byscore'] = True
            byscore_or_bylex = True
            # Use score bounds instead of indices
            start = random.uniform(-100, 100)
            end = random.uniform(start, start + 200)
        elif random.random() < 0.3:
            kwargs['bylex'] = True
            byscore_or_bylex = True
            # Use lexicographical bounds
            start_char = random.choice(['a', 'b', 'c'])
            end_char = chr(ord(start_char) + random.randint(1, 3))
            start = f"[{start_char}"
            end = f"[{end_char}"
            
        if random.random() < 0.3:
            kwargs['desc'] = True
            
        # Only add offset/num if using byscore or bylex
        if byscore_or_bylex and random.random() < 0.4:
            kwargs['offset'] = random.randint(0, 5)
            kwargs['num'] = random.randint(1, 10)
            
        pipe.zrangestore(dest_key, key, start, end, **kwargs)

    # Lexicographical count
    @cg_method(cmd_type="zset", can_create_key=False)
    def zlexcount(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Generate lexicographical range
        start_char = random.choice(['a', 'b', 'c', 'd'])
        end_char = chr(ord(start_char) + random.randint(1, 5))
        
        min_bound = random.choice([f"[{start_char}", f"({start_char}", "-"])
        max_bound = random.choice([f"[{end_char}", f"({end_char}", "+"])
        
        pipe.zlexcount(key, min_bound, max_bound)

if __name__ == "__main__":
    zset_gen = parse(ZSetGen)
    zset_gen.distributions = '{"zadd": 100, "zincrby": 100, "zrem": 100, "zcard": 50, "zcount": 50, "zscore": 50, "zmscore": 50, "zrank": 50, "zrevrank": 50, "zrange": 50, "zrevrange": 50, "zrangebyscore": 50, "zrevrangebyscore": 50, "zrangebylex": 30, "zrevrangebylex": 30, "zpopmax": 40, "zpopmin": 40, "zrandmember": 50, "zunionstore": 30, "zinterstore": 30, "zunion": 30, "zinter": 30, "zdiff": 30, "zdiffstore": 30, "zremrangebyrank": 40, "zremrangebyscore": 40, "zremrangebylex": 30, "zscan": 40, "bzpopmin": 20, "bzpopmax": 20, "zmpop": 30, "bzmpop": 20, "zintercard": 30, "zrangestore": 25, "zlexcount": 30}'
    zset_gen._run()
