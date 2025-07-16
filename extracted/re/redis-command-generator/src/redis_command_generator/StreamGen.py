import redis
import random
from simple_parsing import parse
from dataclasses import dataclass
from redis_command_generator.BaseGen import BaseGen, cg_method

@dataclass
class StreamGen(BaseGen):
    max_subelements: int = 10
    subkey_size: int = 5
    subval_size: int = 5
    
    def _get_group_name(self) -> str:
        """Get a group name from a fixed set for consistency across operations"""
        return random.choice([f"group{i}" for i in range(1, 11)])  # group1 through group10
    
    def _get_consumer_name(self) -> str:
        """Get a consumer name from a fixed set for consistency across operations"""
        return random.choice([f"consumer{i}" for i in range(1, 6)])  # consumer1 through consumer5
    
    def _get_existing_group(self, redis_obj, key: str) -> str:
        """Get an existing consumer group for the stream, or return a default group name"""
        try:
            # Try to get existing groups for this stream
            groups = redis_obj.xinfo_groups(key)
            if groups:
                # Return a random existing group name
                group_info = random.choice(groups)
                return group_info['name']
        except:
            # If stream doesn't exist or has no groups, fall back to fixed names
            pass
        # Fall back to fixed group names
        return self._get_group_name()
    
    def _has_existing_groups(self, redis_obj, key: str) -> bool:
        """Check if the stream has any existing consumer groups"""
        try:
            groups = redis_obj.xinfo_groups(key)
            return len(groups) > 0 if groups else False
        except:
            return False
    
    @cg_method(cmd_type="stream", can_create_key=True)
    def xadd(self, pipe: redis.client.Pipeline, key: str) -> None:
        fields = {self._rand_str(self.subkey_size): self._rand_str(self.subval_size) for _ in range(random.randint(1, self.max_subelements))}
        
        # Optional parameters for stream management
        kwargs = {}
        
        # Sometimes use maxlen for length-based trimming
        if random.random() < 0.3:
            kwargs['maxlen'] = random.randint(10, 100)
            if random.random() < 0.5:
                kwargs['approximate'] = True
        # Sometimes use minid for ID-based trimming (alternative to maxlen)
        elif random.random() < 0.2:
            kwargs['minid'] = f"{random.randint(1, 50)}-0"
        
        # Sometimes add limit when using trimming
        if 'maxlen' in kwargs or 'minid' in kwargs:
            if random.random() < 0.4:
                kwargs['limit'] = random.randint(1, 20)
        
        # Sometimes prevent stream creation
        if random.random() < 0.1:
            kwargs['nomkstream'] = True
            
        pipe.xadd(key, fields, **kwargs)
    
    @cg_method(cmd_type="stream", can_create_key=False)
    def xdel(self, pipe: redis.client.Pipeline, key: str) -> None:
        stream_len = random.randint(0, 10)
        if stream_len > 0:
            stream_id = f"{random.randint(1, 1000)}-0"
            pipe.xdel(key, stream_id)

    # Basic read operations
    @cg_method(cmd_type="stream", can_create_key=False)
    def xlen(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Simple read operation, no parameters needed
        pipe.xlen(key)

    @cg_method(cmd_type="stream", can_create_key=False)
    def xrange(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Generate stream ID range (like zrange pattern)
        redis_obj = self._pipe_to_redis(pipe)
        
        # Use various range patterns
        if random.random() < 0.3:
            # Full range
            start, end = "-", "+"
        elif random.random() < 0.5:
            # Start from beginning with count
            start = "-"
            end = "+"
        else:
            # Specific time-based range
            start_time = random.randint(1, 1000)
            end_time = random.randint(start_time, start_time + 1000)
            start = f"{start_time}-0"
            end = f"{end_time}-0"
        
        # Optional count parameter (like lrange pattern)
        if random.random() < 0.4:
            count = random.randint(1, 20)
            pipe.xrange(key, start, end, count=count)
        else:
            pipe.xrange(key, start, end)

    @cg_method(cmd_type="stream", can_create_key=False)
    def xrevrange(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Same pattern as xrange but reverse order
        if random.random() < 0.3:
            start, end = "+", "-"
        elif random.random() < 0.5:
            start = "+"
            end = "-"
        else:
            start_time = random.randint(1, 1000)
            end_time = random.randint(start_time, start_time + 1000)
            # For xrevrange, larger ID comes first
            start = f"{end_time}-0"
            end = f"{start_time}-0"
        
        if random.random() < 0.4:
            count = random.randint(1, 20)
            pipe.xrevrange(key, start, end, count=count)
        else:
            pipe.xrevrange(key, start, end)

    @cg_method(cmd_type="stream", can_create_key=False)
    def xtrim(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Trim stream to specified length (like ltrim pattern)
        
        # Choose between maxlen and minid (can't use both)
        if random.random() < 0.7:
            # Use maxlen (more common)
            maxlen = random.randint(1, 100)
            kwargs = {'maxlen': maxlen}
        else:
            # Use minid (alternative to maxlen)
            min_id = f"{random.randint(1, 50)}-0"
            kwargs = {'minid': min_id}
        
        # Sometimes use approximate trimming for better performance
        if random.random() < 0.5:
            kwargs['approximate'] = True
            
        # Sometimes add limit parameter
        if random.random() < 0.3:
            kwargs['limit'] = random.randint(1, 20)
        
        pipe.xtrim(key, **kwargs)

    @cg_method(cmd_type="stream", can_create_key=False)
    def xread(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Read from streams (can read from multiple streams)
        redis_obj = self._pipe_to_redis(pipe)
        
        # Build streams dict
        streams = {key: "$"}  # Start with current stream from latest
        
        # Sometimes add more streams
        for _ in range(random.randint(0, 2)):
            k = self._scan_rand_key(redis_obj, "stream")
            if k and k not in streams:
                # Use various starting positions
                start_pos = random.choice(["$", "0-0", f"{random.randint(1, 100)}-0"])
                streams[k] = start_pos
        
        # Optional parameters
        kwargs = {}
        if random.random() < 0.4:
            kwargs['count'] = random.randint(1, 10)
        if random.random() < 0.3:
            kwargs['block'] = 100  # milliseconds - cap at 100ms to avoid slowing down tests
        
        pipe.xread(streams, **kwargs)

    # Consumer Group Operations
    @cg_method(cmd_type="stream", can_create_key=False)
    def xgroup_create(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Create a consumer group (like sinterstore pattern for group management)
        group_name = self._get_group_name()
        
        # Use various starting positions for the group
        start_id = random.choice(["$", "0", f"{random.randint(1, 100)}-0"])
        
        # Sometimes create with mkstream option
        mkstream = random.random() < 0.5
        
        # Optional parameters for Redis 7.0+
        kwargs = {'id': start_id, 'mkstream': mkstream}
        if random.random() < 0.3:  # Sometimes use entries_read (Redis 7.0+)
            kwargs['entries_read'] = random.randint(0, 100)
        
        # Note: We don't check for existing groups here because pipeline commands
        # execute later, and checking outside pipeline creates race conditions
        pipe.xgroup_create(key, group_name, **kwargs)

    @cg_method(cmd_type="stream", can_create_key=False)
    def xgroup_destroy(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Destroy a consumer group
        redis_obj = self._pipe_to_redis(pipe)
        if self._has_existing_groups(redis_obj, key):
            group_name = self._get_existing_group(redis_obj, key)
            pipe.xgroup_destroy(key, group_name)

    @cg_method(cmd_type="stream", can_create_key=False)
    def xgroup_createconsumer(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Create a consumer in a group
        redis_obj = self._pipe_to_redis(pipe)
        if self._has_existing_groups(redis_obj, key):
            group_name = self._get_existing_group(redis_obj, key)
            consumer_name = self._get_consumer_name()
            pipe.xgroup_createconsumer(key, group_name, consumer_name)

    @cg_method(cmd_type="stream", can_create_key=False)
    def xgroup_delconsumer(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Delete a consumer from a group
        redis_obj = self._pipe_to_redis(pipe)
        if self._has_existing_groups(redis_obj, key):
            group_name = self._get_existing_group(redis_obj, key)
            consumer_name = self._get_consumer_name()
            pipe.xgroup_delconsumer(key, group_name, consumer_name)

    @cg_method(cmd_type="stream", can_create_key=False)
    def xgroup_setid(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Set the consumer group last delivered ID
        redis_obj = self._pipe_to_redis(pipe)
        if self._has_existing_groups(redis_obj, key):
            group_name = self._get_existing_group(redis_obj, key)
            new_id = random.choice(["$", "0", f"{random.randint(1, 100)}-0"])
            
            # Optional parameters for Redis 7.0+
            kwargs = {'id': new_id}
            if random.random() < 0.3:  # Sometimes use entries_read (Redis 7.0+)
                kwargs['entries_read'] = random.randint(0, 100)
            
            pipe.xgroup_setid(key, group_name, **kwargs)

    @cg_method(cmd_type="stream", can_create_key=False)
    def xreadgroup(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Read from streams via consumer group
        redis_obj = self._pipe_to_redis(pipe)
        if self._has_existing_groups(redis_obj, key):
            group_name = self._get_existing_group(redis_obj, key)
            consumer_name = self._get_consumer_name()
            
            # Build streams dict for group reading - only use the current stream
            # since we can't guarantee other streams have the same group
            streams = {key: ">"}  # Use ">" to read new messages
            
            # Optional parameters
            kwargs = {}
            if random.random() < 0.4:
                kwargs['count'] = random.randint(1, 10)
            if random.random() < 0.3:
                kwargs['block'] = 100  # milliseconds - cap at 100ms
            if random.random() < 0.2:
                kwargs['noack'] = True  # Don't acknowledge messages automatically
            
            pipe.xreadgroup(group_name, consumer_name, streams, **kwargs)

    # Message Acknowledgment and Claiming Operations
    @cg_method(cmd_type="stream", can_create_key=False)
    def xack(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Acknowledge processed messages
        redis_obj = self._pipe_to_redis(pipe)
        if self._has_existing_groups(redis_obj, key):
            group_name = self._get_existing_group(redis_obj, key)
            
            # Generate message IDs to acknowledge
            message_ids = []
            for _ in range(random.randint(1, 3)):
                msg_id = f"{random.randint(1, 1000)}-{random.randint(0, 5)}"
                message_ids.append(msg_id)
            
            pipe.xack(key, group_name, *message_ids)

    @cg_method(cmd_type="stream", can_create_key=False)
    def xclaim(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Change ownership of pending messages
        redis_obj = self._pipe_to_redis(pipe)
        if self._has_existing_groups(redis_obj, key):
            group_name = self._get_existing_group(redis_obj, key)
            consumer_name = self._get_consumer_name()
            
            # Generate message IDs to claim
            message_ids = []
            for _ in range(random.randint(1, 3)):
                msg_id = f"{random.randint(1, 1000)}-{random.randint(0, 5)}"
                message_ids.append(msg_id)
            
            # Min idle time in milliseconds
            min_idle_time = random.randint(1000, 60000)
            
            # Optional parameters
            kwargs = {}
            if random.random() < 0.3:
                kwargs['idle'] = random.randint(500, 5000)
            if random.random() < 0.2:
                kwargs['retrycount'] = random.randint(1, 10)
            if random.random() < 0.2:
                kwargs['force'] = True
            if random.random() < 0.2:
                kwargs['justid'] = True  # Return just IDs, not full messages
            
            pipe.xclaim(key, group_name, consumer_name, min_idle_time, message_ids, **kwargs)

    @cg_method(cmd_type="stream", can_create_key=False)
    def xautoclaim(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Automatically claim pending messages
        redis_obj = self._pipe_to_redis(pipe)
        if self._has_existing_groups(redis_obj, key):
            group_name = self._get_existing_group(redis_obj, key)
            consumer_name = self._get_consumer_name()
            
            # Min idle time and start ID
            min_idle_time = random.randint(1000, 60000)
            start_id = random.choice(["0-0", f"{random.randint(1, 100)}-0"])
            
            # Optional parameters
            kwargs = {}
            if random.random() < 0.4:
                kwargs['count'] = random.randint(1, 10)
            if random.random() < 0.3:
                kwargs['justid'] = True  # Return just IDs, not full messages
            
            pipe.xautoclaim(key, group_name, consumer_name, min_idle_time, start_id, **kwargs)

    @cg_method(cmd_type="stream", can_create_key=False)
    def xpending(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Get information about pending messages  
        redis_obj = self._pipe_to_redis(pipe)
        if self._has_existing_groups(redis_obj, key):
            group_name = self._get_existing_group(redis_obj, key)
            
            # Basic pending info - just key and group name (per core.py signature)
            pipe.xpending(key, group_name)

    @cg_method(cmd_type="stream", can_create_key=False)
    def xpending_range(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Get detailed information about pending messages in a range
        redis_obj = self._pipe_to_redis(pipe)
        if self._has_existing_groups(redis_obj, key):
            group_name = self._get_existing_group(redis_obj, key)
            
            # Generate range
            start_id = random.choice(["-", "0-0", f"{random.randint(1, 100)}-0"])
            end_id = random.choice(["+", f"{random.randint(100, 1000)}-0"])
            count = random.randint(1, 20)
            
            # Sometimes filter by consumer
            if random.random() < 0.5:
                consumer_name = self._get_consumer_name()
                pipe.xpending_range(key, group_name, start_id, end_id, count, consumer_name)
            else:
                pipe.xpending_range(key, group_name, start_id, end_id, count)

    # Stream Information Operations
    @cg_method(cmd_type="stream", can_create_key=False)
    def xinfo_consumers(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Get information about consumers in a group
        redis_obj = self._pipe_to_redis(pipe)
        # Only execute if groups exist
        if self._has_existing_groups(redis_obj, key):
            group_name = self._get_existing_group(redis_obj, key)
            pipe.xinfo_consumers(key, group_name)
        else:
            # Skip this operation if no groups exist
            pass

    @cg_method(cmd_type="stream", can_create_key=False)
    def xinfo_groups(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Get information about consumer groups
        pipe.xinfo_groups(key)

    @cg_method(cmd_type="stream", can_create_key=False)
    def xinfo_stream(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Get information about a stream
        # Sometimes include full details
        if random.random() < 0.3:
            pipe.xinfo_stream(key, full=True)
        else:
            pipe.xinfo_stream(key)

if __name__ == "__main__":
    stream_gen = parse(StreamGen)
    stream_gen.distributions = '{"xadd": 100, "xdel": 100, "xlen": 50, "xrange": 60, "xrevrange": 60, "xtrim": 40, "xread": 50, "xgroup_create": 30, "xgroup_destroy": 10, "xgroup_createconsumer": 25, "xgroup_delconsumer": 15, "xgroup_setid": 15, "xreadgroup": 40, "xack": 25, "xclaim": 20, "xautoclaim": 15, "xpending": 20, "xpending_range": 15, "xinfo_consumers": 15, "xinfo_groups": 20, "xinfo_stream": 25}'
    stream_gen._run()
