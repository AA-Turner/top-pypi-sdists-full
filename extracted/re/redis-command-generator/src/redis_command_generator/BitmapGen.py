import redis
import random
from simple_parsing import parse
from dataclasses import dataclass
from redis_command_generator.BaseGen import BaseGen, cg_method

@dataclass
class BitmapGen(BaseGen):
    max_subelements: int = 1000
    
    @cg_method(cmd_type="bit", can_create_key=True)
    def setbit(self, pipe: redis.client.Pipeline, key: str) -> None:
        offset = random.randint(0, self.max_subelements)
        value = random.randint(0, 1)
        pipe.setbit(key, offset, value)
    
    @cg_method(cmd_type="bit", can_create_key=False)
    def getbit(self, pipe: redis.client.Pipeline, key: str) -> None:
        offset = random.randint(0, self.max_subelements)
        pipe.getbit(key, offset)

    @cg_method(cmd_type="bit", can_create_key=False)
    def bitcount(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Count set bits in the bitmap, optionally with byte range
        if random.random() < 0.5:
            # Sometimes include start/end byte range
            start = random.randint(0, self.max_subelements // 8)
            end = random.randint(start, self.max_subelements // 8)
            
            # Sometimes include mode parameter (BIT vs BYTE indexing)
            if random.random() < 0.3:
                mode = random.choice(['BYTE', 'BIT'])
                pipe.bitcount(key, start, end, mode=mode)
            else:
                pipe.bitcount(key, start, end)
        else:
            # Count all bits in the bitmap
            pipe.bitcount(key)

    @cg_method(cmd_type="bit", can_create_key=False) 
    def bitfield(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Complex bitfield operations with builder pattern
        redis_obj = self._pipe_to_redis(pipe)
        
        # Create bitfield operation with random overflow handling
        overflow = random.choice(['WRAP', 'SAT', 'FAIL'])
        bf = redis_obj.bitfield(key, default_overflow=overflow)
        
        # Add multiple random operations
        num_ops = random.randint(1, 3)
        for _ in range(num_ops):
            op_type = random.choice(['get', 'set', 'incrby'])
            fmt = random.choice(['u8', 'u16', 'u32', 'i8', 'i16', 'i32'])  # unsigned/signed formats
            offset = random.randint(0, self.max_subelements)
            
            if op_type == 'get':
                bf.get(fmt, offset)
            elif op_type == 'set':
                value = random.randint(0, 255)  # 8-bit value range
                bf.set(fmt, offset, value)
            else:  # incrby
                increment = random.randint(-10, 10)
                # Sometimes change overflow for this specific operation
                if random.random() < 0.3:
                    local_overflow = random.choice(['WRAP', 'SAT', 'FAIL'])
                    bf.incrby(fmt, offset, increment, overflow=local_overflow)
                else:
                    bf.incrby(fmt, offset, increment)
        
        # Execute the bitfield operations
        bf.execute()

    @cg_method(cmd_type="bit", can_create_key=False)
    def bitfield_ro(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Read-only bitfield operations for GET only
        fmt = random.choice(['u8', 'u16', 'u32', 'i8', 'i16', 'i32'])
        offset = random.randint(0, self.max_subelements)
        
        # Sometimes include additional GET operations
        items = []
        if random.random() < 0.4:
            # Add more GET operations
            for _ in range(random.randint(1, 2)):
                extra_fmt = random.choice(['u8', 'u16', 'i8', 'i16'])
                extra_offset = random.randint(0, self.max_subelements)
                items.append((extra_fmt, extra_offset))
        
        pipe.bitfield_ro(key, fmt, offset, items=items)

    @cg_method(cmd_type="bit", can_create_key=True)
    def bitop(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Bitwise operations between bitmap keys
        redis_obj = self._pipe_to_redis(pipe)
        
        operation = random.choice(['AND', 'OR', 'XOR', 'NOT'])
        dest_key = f"bitop_result_{self._rand_str(5)}"
        
        if operation == 'NOT':
            # NOT operation works on a single source key
            pipe.bitop(operation, dest_key, key)
        else:
            # AND, OR, XOR work on multiple source keys
            source_keys = [key]
            
            # Try to find other bitmap keys to operate on
            other_keys = [k for k in [self._scan_rand_key(redis_obj, "bit") for _ in range(3)] if k and k != key]
            if other_keys:
                source_keys.extend(other_keys[:2])  # Add up to 2 more keys
            else:
                # If no other bitmap keys, create some dummy key names
                source_keys.append(f"bit_{self._rand_str(5)}")
            
            pipe.bitop(operation, dest_key, *source_keys)

    @cg_method(cmd_type="bit", can_create_key=False)
    def bitpos(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Find position of first bit set to 0 or 1
        bit = random.choice([0, 1])
        
        if random.random() < 0.6:
            # Sometimes include start/end byte range
            start = random.randint(0, self.max_subelements // 8)
            
            if random.random() < 0.5:
                # Include end parameter
                end = random.randint(start, self.max_subelements // 8)
                
                # Sometimes include mode parameter
                if random.random() < 0.3:
                    mode = random.choice(['BYTE', 'BIT'])
                    pipe.bitpos(key, bit, start, end, mode=mode)
                else:
                    pipe.bitpos(key, bit, start, end)
            else:
                # Just start parameter - don't use mode when only start is provided
                # because it can cause parameter interpretation issues
                pipe.bitpos(key, bit, start)
        else:
            # Search entire bitmap
            pipe.bitpos(key, bit)

if __name__ == "__main__":
    bitmap_gen = parse(BitmapGen)
    bitmap_gen.distributions = '{"setbit": 100, "getbit": 80, "bitcount": 60, "bitfield": 40, "bitfield_ro": 30, "bitop": 50, "bitpos": 40}'
    bitmap_gen._run()
