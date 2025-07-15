import redis
import random
import string
import threading
import json
import time
from typing import Callable
from simple_parsing import parse
from dataclasses import dataclass
from contextlib import contextmanager
from pathlib import Path
from functools import wraps

JSON_PATH = str(Path(__file__).parent / "distributions.json")

def cg_method(cmd_type, can_create_key):
    """Decorator for command-generator methods that sets required attributes."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        
        setattr(wrapper, 'type', cmd_type)
        setattr(wrapper, 'can_create_key', can_create_key)
        return wrapper
    return decorator

@contextmanager
def exception_wrapper():
    """
    Suppresses ResponseError exceptions that are expected to occur during the execution of 
    randomally generated Redis commands. All other exceptions are raised.
    """
    try:
        yield
    except redis.exceptions.ResponseError as e:
        if (("WRONGTYPE" not in str(e)) and (
        not ("INCRBY" in str(e) and "value is not an integer or out of range" in str(e))) and
                ("MOVED" not in str(e)) and "the key does not exist" not in str(e)):
            raise e

class RedisObj():
    """
    A wrapper class for the redis.Redis client that intercepts method calls
    and wraps them in an exception handling context manager.
    """

    def __init__(self, *args, **kwargs):
        self._client = redis.Redis(*args, **kwargs)

    def __getattr__(self, name):
        """
        Retrieves the attribute from the underlying Redis client. If the attribute
        is callable, it wraps the method call in the exception_wrapper context manager.
        """
        original_attr = getattr(self._client, name)

        if callable(original_attr):
            def wrapper(*args, **kwargs):
                with exception_wrapper():
                    return original_attr(*args, **kwargs)
            return wrapper
        else:
            return original_attr

@dataclass
class BaseGen():
    verbose: bool = False  # Print debug information (sent commands)
    hosts: tuple = ("localhost:6379",)  # Redis hosts to connect to
    flush: bool = False  # Flush all hosts on connection
    max_cmd_cnt: int = 10000  # Maximum number of commands to execute, may be interrupted by exceeding memory cap. Set to 0 for infinite
    mem_cap: float = 70  # Memory cap percentage
    pipe_every_x: int = 1000  # Execute pipeline every X commands
    def_key_size: int = 10  # Default key size
    def_key_pref: str = '' # Default key prefix
    distributions: str = None # distributions.json file path or a serialized dict (e.g. {"expire": 50, "incrby": 70, ...})
    expire_precentage: int = 0  # Percentage of commands with expiry/ttl
    logfile: str = None  # Optional log file path to write debug information to
    maxmemory_bytes: int = None  # Override INFO's maxmemory (useful when unavailable, for e.g. in cluster mode)
    print_prefix: str = "COMMAND GENERATOR: "
    identical_values_across_hosts: bool = False  # Generate identical commands across connections, or allow value conflicts
    
    ttl_low: int = 15
    ttl_high: int = 300

    ########################################
    ######## Internal use methods ##########
    ########################################
    
    UNSCANNABLE_TYPES = ["hll", "bit", "geo"]

    def _rand_str(self, str_size: int) -> str:
        return "".join(random.choices(string.ascii_letters + string.digits, k = str_size))
    
    def _rand_key(self, type: str) -> str:
        prefix = self.def_key_pref
        # The following types can't be directly scanned, so we must add a prefix to distinguish them
        prefix += f"{type}:" if type in self.UNSCANNABLE_TYPES else ""
        
        return prefix + self._rand_str(self.def_key_size)
    
    def _scan_rand_key(self, redis_obj: redis.Redis, type: str) -> str | None:
        if not hasattr(self, 'scan_cursors'):
            self.scan_cursors = {}
        
        conn = self._get_conn_info(redis_obj)
        if conn not in self.scan_cursors:
            self.scan_cursors[conn] = {}
        
        if type not in self.scan_cursors[conn]:
            self.scan_cursors[conn][type] = 0

        if type not in self.UNSCANNABLE_TYPES:
            cursor, keys = redis_obj.scan(self.scan_cursors[conn][type], _type=type)
        else:
            scan_match = f"{self.def_key_pref}{type}:*"
            cursor, keys = redis_obj.scan(self.scan_cursors[conn][type], match=scan_match)
        self.scan_cursors[conn][type] = cursor
        return random.choice(keys) if keys else None
    
    def _check_mem_cap(self, redis_obj: redis.Redis):
        info = redis_obj.info()
        
        if self.maxmemory_bytes:
            max_mem = self.maxmemory_bytes
        else:
            max_mem = info['maxmemory'] if ('maxmemory' in info) else None
        
        curr_mem = info['used_memory']
        
        if max_mem and curr_mem >= (self.mem_cap / 100) * max_mem:
            self._print(f"Memory cap for {self._get_conn_info(redis_obj)} reached, with {curr_mem} bytes used out of {max_mem * (self.mem_cap / 100)} available")
            return True
        else:
            return False
    
    def _get_conn_info(self, redis_obj: redis.Redis) -> str:
        return f"{redis_obj.connection_pool.connection_kwargs['host']}:{redis_obj.connection_pool.connection_kwargs['port']}"
    
    def _pipe_to_redis(self, pipe: redis.client.Pipeline) -> RedisObj:
        return RedisObj(connection_pool=pipe.connection_pool)
    
    def _print(self, msg: str) -> None:
        if self.file:
            self.file.write(f"{msg}\n")
        
        if self.verbose:
            print(self.print_prefix + msg)
    
    def _extract_distributions(self) -> None:
        if self.distributions is None:
            self.distributions = JSON_PATH
        
        if self.distributions.endswith('.json'):
            with open(self.distributions, 'r') as f:
                self.distributions = json.load(f)
        else:
            self.distributions = json.loads(self.distributions)
        
        method_names = [name for name in dir(self) if callable(getattr(self, name)) and not name.startswith('_')]
        for cmd in self.distributions:
            if cmd not in method_names:
                raise ValueError(f"Command '{cmd}' not found in generator")
    
    def _run(self, stop_event: threading.Event = None) -> None:
        self.file = open(self.logfile, 'w') if self.logfile else None
        rl = []  # Redis connections list
        redis_pipes = []
        
        try:
            self._extract_distributions()
            
            for host in self.hosts:
                (hostname, port) = host.split(':')
                r = redis.Redis(host=hostname, port=port)
                r.ping()
                
                if self.flush:
                    r.flushall()
                self._print("INFO: " + str(r.info()))
                
                rl.append(r)
                redis_pipes.append(r.pipeline(transaction=False))
            
            i = 1
            while self.max_cmd_cnt == 0 or i <= self.max_cmd_cnt:
                if stop_event and stop_event.is_set():
                    break
                for r in rl:
                    if self._check_mem_cap(r):
                        return
                
                key = None
                should_expire = False  # Whether generated key should have a TTL
                cmd_name = random.choices(list(self.distributions.keys()), weights=list(self.distributions.values()))[0]
                cmd = getattr(self, cmd_name)
                
                # Generate a single key for all hosts. In case the command can add keys, we'd prefer to generate
                # a new keyname to increase DBSIZE. Otherwise, we'd prefer to act upon an existing key
                if cmd.can_create_key:
                    key = self._rand_key(cmd.type)
                    
                    if random.randint(0, 99) < self.expire_precentage:
                        should_expire = True
                else:
                    r = random.choice(rl)  # Randomly select a connection for scanning
                    if cmd.type != "base":
                        key = self._scan_rand_key(r, cmd.type)
                    else:
                        key = r.randomkey()
                        
                    if not key:
                        continue  # Skip if no key found, e.g. in case of empty DB or no keys of the requested type

                # Generate command with common seed accross hosts if `identical_values_across_hosts`
                if self.identical_values_across_hosts:
                    seed = time.time()
                
                for pipe in redis_pipes:
                    if self.identical_values_across_hosts:
                        random.seed(seed)
                    cmd(pipe, key)
                    
                    if should_expire:
                        self.expire(pipe, key)

                if i % self.pipe_every_x == 0:
                    for (pipe, r) in zip(redis_pipes, rl):
                        self._print(f"Executing pipeline for {self._get_conn_info(r)}")
                        for command in pipe.command_stack:
                            self._print(f"Command: {command[0]}")
                        
                        with exception_wrapper():
                            pipe.execute()
                
                i += 1
            
            # Execute remaining commands
            for pipe in redis_pipes:
                with exception_wrapper():
                    pipe.execute()
        
        except Exception as e:
            self._print(f"Exception: {e}")
            raise e
        
        finally:
            for r in rl:
                self._print("Connection: " + self._get_conn_info(r))
                self._print("Memory usage: " + str(r.info()['used_memory']))
                self._print("DB size: " + str(r.dbsize()))
                r.close()
            self.file.close() if self.file else None
    
    ########################################
    ######## Redis command methods #########
    ########################################
    
    @cg_method("base", False)
    def expire(self, pipe: redis.client.Pipeline, key: str) -> None:
        pipe.expire(key, random.randrange(self.ttl_low, self.ttl_high))
    
    @cg_method("base", False)
    def persist(self, pipe: redis.client.Pipeline, key: str) -> None:
        pipe.persist(key)

if __name__ == "__main__":
    base_gen = parse(BaseGen)
    base_gen.distributions = '{"expire": 100, "persist": 100}'
    base_gen._run()