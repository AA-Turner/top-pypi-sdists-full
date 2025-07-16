import redis
import random
import json
from enum import Enum
from simple_parsing import parse
from dataclasses import dataclass
from redis_command_generator.BaseGen import BaseGen, cg_method

KEY_TYPE = "ReJSON-RL"
ROOT_PATH = "$"

class JsonOperationType(Enum):
    """Enum for different JSON operation types"""
    BASIC = "basic"
    WILDCARD_SUPPORTED = "wildcard_supported"
    ARRAY_APPEND = "array_append"
    MERGE = "merge"

@dataclass
class JsonGen(BaseGen):
    max_subelements: int = 10
    subval_size: int = 5
    subkey_size: int = 10
    max_depth: int = 3
    
    def _generate_default_json(self, depth: int = 0):
        """Generate a default JSON object with random structure and values"""
        if depth >= self.max_depth:
            # At max depth, return simple values
            return random.choice([
                self._rand_str(self.subval_size),
                random.randint(1, 1000),
                random.choice([True, False]),
                None
            ])
        
        json_obj = {}
        num_elements = random.randint(1, min(self.max_subelements, 5))
        
        for _ in range(num_elements):
            key = self._rand_str(self.subkey_size)
            
            # Generate different types of values
            value_type = random.choice(['string', 'number', 'boolean', 'null', 'array', 'object'])
            
            if value_type == 'string':
                json_obj[key] = self._rand_str(self.subval_size)
            elif value_type == 'number':
                json_obj[key] = random.choice([
                    random.randint(1, 1000),
                    random.uniform(1.0, 1000.0)
                ])
            elif value_type == 'boolean':
                json_obj[key] = random.choice([True, False])
            elif value_type == 'null':
                json_obj[key] = None
            elif value_type == 'array':
                array_length = random.randint(1, 5)
                json_obj[key] = [self._generate_default_json(depth + 1) for _ in range(array_length)]
            elif value_type == 'object':
                json_obj[key] = self._generate_default_json(depth + 1)
        
        return json_obj
    
    def _generate_json_path(self, operation_type: JsonOperationType = JsonOperationType.BASIC) -> str:
        """Generate a random JSON path for operations"""
        if operation_type == JsonOperationType.WILDCARD_SUPPORTED:
            # Operations that support wildcards like JSON.GET, JSON.DEL, etc.
            paths = [
                ROOT_PATH,
                "$.name",
                "$.age", 
                "$.items",
                "$.items[*]",
                "$.data",
                "$.data.value",
                "$.config",
                "$.users[*].name"
            ]
        else:
            # Operations that don't support wildcards (most modification operations)
            paths = [
                ROOT_PATH,
                "$.name",
                "$.age",
                "$.items",
                "$.data",
                "$.data.value",
                "$.config",
                "$.users"
            ]
        return random.choice(paths)
    
    def _generate_compatible_path_and_value(self, redis_obj, key: str, operation_type: JsonOperationType = JsonOperationType.BASIC):
        """Generate a compatible path and value based on existing JSON structure"""
        """This is in order that most json path operations will not fail on invalid paths"""
        try:
            # Try to get existing JSON structure
            existing_json = redis_obj.json().get(key, ROOT_PATH)
            if existing_json is None:
                # Key doesn't exist, use root path with new value
                return ROOT_PATH, self._generate_default_json()
            
            # Generate valid paths based on existing structure
            valid_paths = self._extract_valid_paths(existing_json, operation_type)
            if not valid_paths:
                return ROOT_PATH, self._generate_default_json()
            
            chosen_path = random.choice(valid_paths)
            
            # Generate appropriate value based on path and operation
            if operation_type == JsonOperationType.ARRAY_APPEND:
                # For array operations, generate simple values
                value = self._generate_simple_value()
            elif operation_type == JsonOperationType.MERGE:
                # For merge operations, generate object
                value = self._generate_default_json() if chosen_path == ROOT_PATH else {"new_field": self._generate_simple_value()}
            else:
                value = self._generate_default_json()
            
            return chosen_path, value
        except:
            # Fallback to safe defaults
            return ROOT_PATH, self._generate_default_json()
    
    def _extract_valid_paths(self, json_obj, operation_type: JsonOperationType = JsonOperationType.BASIC) -> list:
        """Extract valid paths from existing JSON structure"""
        if not isinstance(json_obj, dict):
            return [ROOT_PATH]
        
        paths = [ROOT_PATH]
        
        def extract_paths(obj, current_path="$"):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    new_path = f"{current_path}.{key}"
                    paths.append(new_path)
                    
                    if isinstance(value, list) and len(value) > 0:
                        # Add array paths
                        if operation_type == JsonOperationType.WILDCARD_SUPPORTED:
                            paths.append(f"{new_path}[*]")
                        # Add valid index paths
                        for i in range(min(len(value), 3)):  # Limit to first 3 items
                            paths.append(f"{new_path}[{i}]")
                    elif isinstance(value, dict):
                        extract_paths(value, new_path)
            elif isinstance(obj, list) and len(obj) > 0:
                for i, item in enumerate(obj[:3]):  # Limit to first 3 items
                    if isinstance(item, dict):
                        extract_paths(item, f"{current_path}[{i}]")
        
        extract_paths(json_obj)
        return paths
    
    def _generate_simple_value(self):
        """Generate a simple value (not nested objects/arrays)"""
        return random.choice([
            self._rand_str(self.subval_size),
            random.randint(1, 1000),
            random.uniform(1.0, 1000.0),
            random.choice([True, False]),
            None
        ])
    
    # Basic JSON commands
    @cg_method(cmd_type=KEY_TYPE, can_create_key=True)
    def json_set(self, pipe: redis.client.Pipeline, key: str) -> None:
        """JSON.SET command - Set JSON value at path"""
        redis_obj = self._pipe_to_redis(pipe)
        if random.choice([True, False]):
            scanned_key = self._scan_rand_key(redis_obj, KEY_TYPE)
            if not scanned_key:
                return
            path, json_value = self._generate_compatible_path_and_value(redis_obj, scanned_key)
            pipe.json().set(scanned_key, path, json_value)
        else:
            path = ROOT_PATH
            json_value = self._generate_default_json()
            pipe.json().set(key, path, json_value)
    
    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def json_get(self, pipe: redis.client.Pipeline, key: str) -> None:
        """JSON.GET command - Get JSON value at path"""
        path = self._generate_json_path(JsonOperationType.WILDCARD_SUPPORTED)
        pipe.json().get(key, path)
    
    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def json_del(self, pipe: redis.client.Pipeline, key: str) -> None:
        """JSON.DEL command - Delete JSON value at path"""
        path = self._generate_json_path(JsonOperationType.WILDCARD_SUPPORTED)
        pipe.json().delete(key, path)
    
    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def json_type(self, pipe: redis.client.Pipeline, key: str) -> None:
        """JSON.TYPE command - Get type of JSON value at path"""
        path = self._generate_json_path(JsonOperationType.WILDCARD_SUPPORTED)
        pipe.json().type(key, path)
    
    # Array operations
    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def json_arrappend(self, pipe: redis.client.Pipeline, key: str) -> None:
        """JSON.ARRAPPEND command - Append values to JSON array"""
        redis_obj = self._pipe_to_redis(pipe)
        path, _ = self._generate_compatible_path_and_value(redis_obj, key, JsonOperationType.ARRAY_APPEND)
        values = [self._generate_simple_value() for _ in range(random.randint(1, self.max_subelements))]
        pipe.json().arrappend(key, path, *values)
    
    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def json_arrlen(self, pipe: redis.client.Pipeline, key: str) -> None:
        """JSON.ARRLEN command - Get length of JSON array"""
        redis_obj = self._pipe_to_redis(pipe)
        path, _ = self._generate_compatible_path_and_value(redis_obj, key)
        pipe.json().arrlen(key, path)
    
    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def json_arrpop(self, pipe: redis.client.Pipeline, key: str) -> None:
        """JSON.ARRPOP command - Pop element from JSON array"""
        redis_obj = self._pipe_to_redis(pipe)
        path, _ = self._generate_compatible_path_and_value(redis_obj, key)
        index = random.randint(-5, 5)
        pipe.json().arrpop(key, path, index)
    
    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def json_arrinsert(self, pipe: redis.client.Pipeline, key: str) -> None:
        """JSON.ARRINSERT command - Insert values into JSON array"""
        redis_obj = self._pipe_to_redis(pipe)
        path, _ = self._generate_compatible_path_and_value(redis_obj, key)
        index = random.randint(0, 5)
        values = [self._generate_simple_value() for _ in range(random.randint(1, self.max_subelements))]
        pipe.json().arrinsert(key, path, index, *values)
    
    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def json_arrindex(self, pipe: redis.client.Pipeline, key: str) -> None:
        """JSON.ARRINDEX command - Find index of value in JSON array"""
        redis_obj = self._pipe_to_redis(pipe)
        path, value = self._generate_compatible_path_and_value(redis_obj, key)
        pipe.json().arrindex(key, path, value)
    
    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def json_arrtrim(self, pipe: redis.client.Pipeline, key: str) -> None:
        """JSON.ARRTRIM command - Trim JSON array to specified range"""
        redis_obj = self._pipe_to_redis(pipe)
        path, _ = self._generate_compatible_path_and_value(redis_obj, key)
        start = random.randint(0, 5)
        stop = random.randint(start, start + 10)
        pipe.json().arrtrim(key, path, start, stop)
    
    # String operations
    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def json_strappend(self, pipe: redis.client.Pipeline, key: str) -> None:
        """JSON.STRAPPEND command - Append string to JSON string value"""
        redis_obj = self._pipe_to_redis(pipe)
        path, _ = self._generate_compatible_path_and_value(redis_obj, key)
        append_str = self._rand_str(self.subval_size)
        pipe.json().strappend(key, json.dumps(append_str), path)
    
    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def json_strlen(self, pipe: redis.client.Pipeline, key: str) -> None:
        """JSON.STRLEN command - Get length of JSON string value"""
        redis_obj = self._pipe_to_redis(pipe)
        path, _ = self._generate_compatible_path_and_value(redis_obj, key)
        pipe.json().strlen(key, path)
    
    # Numeric operations
    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def json_numincrby(self, pipe: redis.client.Pipeline, key: str) -> None:
        """JSON.NUMINCRBY command - Increment numeric value"""
        redis_obj = self._pipe_to_redis(pipe)
        path, _ = self._generate_compatible_path_and_value(redis_obj, key)
        increment = random.uniform(-100, 100)
        pipe.json().numincrby(key, path, increment)
    
    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def json_nummultby(self, pipe: redis.client.Pipeline, key: str) -> None:
        """JSON.NUMMULTBY command - Multiply numeric value"""
        redis_obj = self._pipe_to_redis(pipe)
        path, _ = self._generate_compatible_path_and_value(redis_obj, key)
        multiplier = random.uniform(0.1, 10.0)
        pipe.json().nummultby(key, path, multiplier)
    
    # Object operations
    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def json_objkeys(self, pipe: redis.client.Pipeline, key: str) -> None:
        """JSON.OBJKEYS command - Get object keys"""
        redis_obj = self._pipe_to_redis(pipe)
        path, _ = self._generate_compatible_path_and_value(redis_obj, key)
        pipe.json().objkeys(key, path)
    
    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def json_objlen(self, pipe: redis.client.Pipeline, key: str) -> None:
        """JSON.OBJLEN command - Get object length"""
        redis_obj = self._pipe_to_redis(pipe)
        path, _ = self._generate_compatible_path_and_value(redis_obj, key)
        pipe.json().objlen(key, path)
    
    # Utility operations
    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def json_clear(self, pipe: redis.client.Pipeline, key: str) -> None:
        """JSON.CLEAR command - Clear JSON value"""
        redis_obj = self._pipe_to_redis(pipe)
        path, _ = self._generate_compatible_path_and_value(redis_obj, key)
        pipe.json().clear(key, path)
    
    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def json_toggle(self, pipe: redis.client.Pipeline, key: str) -> None:
        """JSON.TOGGLE command - Toggle boolean value"""
        redis_obj = self._pipe_to_redis(pipe)
        path, _ = self._generate_compatible_path_and_value(redis_obj, key)
        pipe.json().toggle(key, path)
    
    # Multi-key operations
    @cg_method(cmd_type=KEY_TYPE, can_create_key=False)
    def json_mget(self, pipe: redis.client.Pipeline, key: str) -> None:
        """JSON.MGET command - Get multiple JSON values"""
        redis_obj = self._pipe_to_redis(pipe)
        keys = [key]
        for _ in range(random.randint(2, 5)):
            key_scanned = self._scan_rand_key(redis_obj, KEY_TYPE)
            if key_scanned:
                keys.append(key_scanned)
        path = self._generate_json_path(JsonOperationType.WILDCARD_SUPPORTED)
        pipe.json().mget(keys, path)
    
    @cg_method(cmd_type=KEY_TYPE, can_create_key=True)
    def json_mset(self, pipe: redis.client.Pipeline, key: str) -> None:
        """JSON.MSET command - Set multiple JSON values"""
        redis_obj = self._pipe_to_redis(pipe)
        num_pairs = random.randint(2, 5)
        mset_args = []
        for _ in range(num_pairs):
            if random.choice([True, False]):
                # Use new key
                k = key
                p = ROOT_PATH
                v = self._generate_default_json()
            else:
                # Use existing key, random path and value
                k = self._scan_rand_key(redis_obj, KEY_TYPE)
                if not k:
                    # fallback to new key if no existing found
                    k = self._rand_str(self.subkey_size)
                    p = ROOT_PATH
                    v = self._generate_default_json()
                else:
                    p, v = self._generate_compatible_path_and_value(redis_obj, k)
            mset_args.append((k, p, v))
        pipe.json().mset(mset_args)
    
    @cg_method(cmd_type=KEY_TYPE, can_create_key=True)
    def json_merge(self, pipe: redis.client.Pipeline, key: str) -> None:
        """JSON.MERGE command - Merge JSON objects"""
        redis_obj = self._pipe_to_redis(pipe)
        if random.choice([True, False]):
            scanned_key = self._scan_rand_key(redis_obj, KEY_TYPE)
            if not scanned_key:
                return
            path, merge_obj = self._generate_compatible_path_and_value(redis_obj, scanned_key, JsonOperationType.MERGE)
            pipe.json().merge(scanned_key, path, merge_obj)
        else:
            path = ROOT_PATH
            merge_obj = self._generate_default_json()
            pipe.json().merge(key, path, merge_obj) 

if __name__ == "__main__":
    json_gen = parse(JsonGen)
    json_gen.distributions = '{"json_set":100, "json_get":100, "json_del":100, "json_type":100, "json_arrappend":100, "json_arrlen":100, "json_arrpop":100, "json_arrinsert":100, "json_arrindex":100, "json_arrtrim":100, "json_strappend":100, "json_strlen":100, "json_numincrby":100, "json_nummultby":100, "json_objkeys":100, "json_objlen":100, "json_clear":100, "json_toggle":100, "json_mget":100,  "json_merge":100, "json_mset":100}'
    json_gen._run()