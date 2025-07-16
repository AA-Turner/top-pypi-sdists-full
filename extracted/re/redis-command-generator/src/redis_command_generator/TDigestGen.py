from typing import Optional
import redis
import random
from simple_parsing import parse
from dataclasses import dataclass
from redis_command_generator.BaseGen import BaseGen, cg_method

KEY_TYPE = "TDIS-TYPE"

@dataclass
class TDigestGen(BaseGen):
    max_compression: int = 1000
    min_compression: int = 100
    max_values_per_add: int = 10
    max_value: float = 1000.0
    min_value: float = -1000.0
    max_quantiles: int = 5
    max_ranks: int = 10

    @cg_method(cmd_type=KEY_TYPE, can_create_key=True)
    def tdigest_create(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Classification: initialization
        
        # Optional compression parameter
        if random.choice([True, False]):
            compression = random.randint(self.min_compression, self.max_compression)
            pipe.execute_command("TDIGEST.CREATE", key, "COMPRESSION", compression)
        else:
            pipe.execute_command("TDIGEST.CREATE", key)

    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def tdigest_add(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Classification: additive
        
        # Add one or more values
        values = []
        num_values = random.randint(1, self.max_values_per_add)
        for _ in range(num_values):
            value = round(random.uniform(self.min_value, self.max_value), 3)
            values.append(str(value))
        
        pipe.execute_command("TDIGEST.ADD", key, *values)

    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def tdigest_info(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Classification: lookup
        pipe.execute_command("TDIGEST.INFO", key)

    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def tdigest_min(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Classification: lookup
        pipe.execute_command("TDIGEST.MIN", key)

    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def tdigest_max(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Classification: lookup
        pipe.execute_command("TDIGEST.MAX", key)

    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def tdigest_quantile(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Classification: lookup
        
        # Generate quantiles (values between 0 and 1)
        quantiles = []
        num_quantiles = random.randint(1, self.max_quantiles)
        for _ in range(num_quantiles):
            quantile = round(random.uniform(0.0, 1.0), 3)
            quantiles.append(str(quantile))
        
        pipe.execute_command("TDIGEST.QUANTILE", key, *quantiles)

    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def tdigest_cdf(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Classification: lookup
        
        # Generate values for CDF calculation
        values = []
        num_values = random.randint(1, self.max_quantiles)
        for _ in range(num_values):
            value = round(random.uniform(self.min_value, self.max_value), 3)
            values.append(str(value))
        
        pipe.execute_command("TDIGEST.CDF", key, *values)

    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def tdigest_rank(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Classification: lookup
        
        # Generate values for rank calculation
        values = []
        num_values = random.randint(1, self.max_quantiles)
        for _ in range(num_values):
            value = round(random.uniform(self.min_value, self.max_value), 3)
            values.append(str(value))
        
        pipe.execute_command("TDIGEST.RANK", key, *values)

    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def tdigest_revrank(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Classification: lookup
        # Generate values for reverse rank calculation
        values = []
        num_values = random.randint(1, self.max_quantiles)
        for _ in range(num_values):
            value = round(random.uniform(self.min_value, self.max_value), 3)
            values.append(str(value))
        
        pipe.execute_command("TDIGEST.REVRANK", key, *values)

    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def tdigest_byrank(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Classification: lookup
        
        # Generate ranks (integer values)
        ranks = []
        num_ranks = random.randint(1, self.max_ranks)
        for _ in range(num_ranks):
            rank = random.randint(0, 100)  # Assuming reasonable rank range
            ranks.append(str(rank))
        
        pipe.execute_command("TDIGEST.BYRANK", key, *ranks)

    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def tdigest_byrevrank(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Classification: lookup
        
        # Generate reverse ranks (integer values)
        ranks = []
        num_ranks = random.randint(1, self.max_ranks)
        for _ in range(num_ranks):
            rank = random.randint(0, 100)  # Assuming reasonable rank range
            ranks.append(str(rank))
        
        pipe.execute_command("TDIGEST.BYREVRANK", key, *ranks)

    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def tdigest_trimmed_mean(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Classification: lookup
        
        # Generate low and high quantiles for trimmed mean
        low_quantile = round(random.uniform(0.0, 0.2), 3)
        high_quantile = round(random.uniform(0.8, 1.0), 3)
        
        pipe.execute_command("TDIGEST.TRIMMED_MEAN", key, str(low_quantile), str(high_quantile))

    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def tdigest_reset(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Classification: destructive
        pipe.execute_command("TDIGEST.RESET", key)

    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def tdigest_merge(self, pipe: redis.client.Pipeline, key: Optional[str]) -> None:
        # Classification: initialization/additive
        redis_obj = self._pipe_to_redis(pipe)
        
        # Find existing T-Digest keys to merge
        existing_keys = []
        for _ in range(random.randint(2, 5)):  # Try to find 2-5 keys
            existing_key = self._scan_rand_key(redis_obj, KEY_TYPE)
            if existing_key and existing_key not in existing_keys:
                existing_keys.append(existing_key)
        
        if len(existing_keys) < 2:
            return  # Need at least 2 keys to merge
                
        # Build merge command
        args = ["TDIGEST.MERGE", key, str(len(existing_keys))]
        args.extend(existing_keys)
        
        # Optionally add compression parameter
        if random.choice([True, False]):
            compression = random.randint(self.min_compression, self.max_compression)
            args.extend(["COMPRESSION", str(compression)])
        
        pipe.execute_command(*args)


if __name__ == "__main__":
    tdigest_gen = parse(TDigestGen)
    tdigest_gen.distributions = '{"tdigest_create": 1000, "tdigest_add": 100, "tdigest_info": 300, "tdigest_min": 300, "tdigest_max": 300, "tdigest_quantile": 300, "tdigest_cdf": 300, "tdigest_rank": 300, "tdigest_revrank": 300, "tdigest_byrank": 300, "tdigest_byrevrank": 300, "tdigest_trimmed_mean": 300, "tdigest_reset": 300, "tdigest_merge": 300}'
    tdigest_gen._run() 