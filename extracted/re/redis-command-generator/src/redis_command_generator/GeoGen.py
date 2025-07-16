import redis
import random
from simple_parsing import parse
from dataclasses import dataclass
from redis_command_generator.BaseGen import BaseGen, cg_method

geo_long_min: float = -180
geo_long_max: float = 180
geo_lat_min : float = -85.05112878
geo_lat_max : float = 85.05112878

@dataclass
class GeoGen(BaseGen):
    max_subelements: int = 10
    subval_size: int = 5
    
    def _get_geo_member_name(self) -> str:
        """Get a member name from a fixed set for consistency across operations"""
        return random.choice([f"place{i}" for i in range(1, 21)])  # place1 through place20
    
    def _get_existing_member(self, redis_obj, key: str) -> str:
        """Get an existing member from the geo key, or return a default member name"""
        try:
            # Use ZRANGE to get random members from the geospatial index (since geo data is stored as zset)
            members = redis_obj.zrange(key, 0, -1)
            if members:
                return random.choice(members).decode('utf-8') if isinstance(members[0], bytes) else random.choice(members)
        except:
            # If key doesn't exist or has no members, fall back to fixed names
            pass
        # Fall back to fixed member names
        return self._get_geo_member_name()
    
    def _has_existing_members(self, redis_obj, key: str) -> bool:
        """Check if the geo key has any existing members"""
        try:
            # Check if the zset (geo index) has any members
            return redis_obj.zcard(key) > 0
        except:
            return False
    
    @cg_method(cmd_type="geo", can_create_key=True)
    def geoadd(self, pipe: redis.client.Pipeline, key: str) -> None:
        members = []
        for _ in range(random.randint(1, self.max_subelements)):
            # Use fixed member names for consistency across operations
            member_name = self._get_geo_member_name()
            longitude = random.uniform(geo_long_min, geo_long_max)
            latitude = random.uniform(geo_lat_min, geo_lat_max)
            members.extend([longitude, latitude, member_name])
        
        # Optional parameters for Redis geoadd enhancements
        kwargs = {}
        if random.random() < 0.2:
            kwargs['nx'] = True  # Only add new elements (don't update existing)
        elif random.random() < 0.2:
            kwargs['xx'] = True  # Only update existing elements (don't add new)
        
        if random.random() < 0.3:
            kwargs['ch'] = True  # Return number of changed elements instead of added
        
        pipe.geoadd(key, members, **kwargs)
    
    @cg_method(cmd_type="geo", can_create_key=False)
    def geodel(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Use fixed member names for consistency
        members = [self._get_geo_member_name() for _ in range(random.randint(1, self.max_subelements))]
        pipe.zrem(key, *members)

    @cg_method(cmd_type="geo", can_create_key=False)
    def geodist(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Calculate distance between two geospatial members
        redis_obj = self._pipe_to_redis(pipe)
        
        # Try to use existing geo key with members
        geo_key = self._scan_rand_key(redis_obj, "geo")
        if geo_key:
            existing_members = redis_obj.zrange(geo_key, 0, 1)  # Get first 2 members
            if len(existing_members) >= 2:
                member1 = existing_members[0].decode('utf-8') if isinstance(existing_members[0], bytes) else existing_members[0]
                member2 = existing_members[1].decode('utf-8') if isinstance(existing_members[1], bytes) else existing_members[1]
                key = geo_key
            else:
                member1 = member2 = self._get_geo_member_name()
        else:
            member1 = member2 = self._get_geo_member_name()
        
        unit = random.choice(['m', 'km', 'mi', 'ft']) if random.random() < 0.5 else None
        pipe.geodist(key, member1, member2, unit=unit)

    @cg_method(cmd_type="geo", can_create_key=False)
    def geohash(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Get geohash representation of members
        redis_obj = self._pipe_to_redis(pipe)
        
        # Try to use existing geo key with members
        geo_key = self._scan_rand_key(redis_obj, "geo")
        if geo_key:
            existing_members = redis_obj.zrange(geo_key, 0, self.max_subelements-1)
            if existing_members:
                members = [m.decode('utf-8') if isinstance(m, bytes) else m for m in existing_members]
                key = geo_key
            else:
                members = [self._get_geo_member_name() for _ in range(random.randint(1, self.max_subelements))]
        else:
            members = [self._get_geo_member_name() for _ in range(random.randint(1, self.max_subelements))]
        
        pipe.geohash(key, *members)

    @cg_method(cmd_type="geo", can_create_key=False)
    def geopos(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Get longitude/latitude coordinates of members
        redis_obj = self._pipe_to_redis(pipe)
        
        # Try to use existing geo key with members
        geo_key = self._scan_rand_key(redis_obj, "geo")
        if geo_key:
            existing_members = redis_obj.zrange(geo_key, 0, self.max_subelements-1)
            if existing_members:
                members = [m.decode('utf-8') if isinstance(m, bytes) else m for m in existing_members]
                key = geo_key
            else:
                members = [self._get_geo_member_name() for _ in range(random.randint(1, self.max_subelements))]
        else:
            members = [self._get_geo_member_name() for _ in range(random.randint(1, self.max_subelements))]
        
        pipe.geopos(key, *members)

    @cg_method(cmd_type="geo", can_create_key=False)
    def georadius(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Query by radius from longitude/latitude coordinates
        longitude = random.uniform(geo_long_min, geo_long_max)
        latitude = random.uniform(geo_lat_min, geo_lat_max)
        radius = random.uniform(1, 1000)  # 1 to 1000 unit radius
        
        # Random unit
        unit = random.choice(['m', 'km', 'mi', 'ft'])
        
        # Optional parameters
        kwargs = {}
        if random.random() < 0.3:
            kwargs['withdist'] = True  # Include distances in results
        if random.random() < 0.3:
            kwargs['withcoord'] = True  # Include coordinates in results
        if random.random() < 0.2:
            kwargs['withhash'] = True  # Include geohash in results
        if random.random() < 0.3:
            kwargs['sort'] = random.choice(['ASC', 'DESC'])  # Sort by distance
        
        # Count and any must be handled together (any requires count)
        if random.random() < 0.4:
            kwargs['count'] = random.randint(1, 20)  # Limit number of results
            # Only add 'any' if count is present
            if random.random() < 0.3:
                kwargs['any'] = True  # Return any COUNT results (Redis 6.2+)
        
        # Sometimes store results (can't combine with other WITH* options)
        if random.random() < 0.2 and not any(k.startswith('with') for k in kwargs):
            if random.random() < 0.5:
                kwargs['store'] = f"geo_store_{self._rand_str(5)}"  # Store member names
            else:
                kwargs['store_dist'] = f"geo_dist_{self._rand_str(5)}"  # Store distances
        
        pipe.georadius(key, longitude, latitude, radius, unit=unit, **kwargs)

    @cg_method(cmd_type="geo", can_create_key=False)
    def georadiusbymember(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Query by radius from an existing member
        redis_obj = self._pipe_to_redis(pipe)
        
        # Try to find a geo key with existing members
        member = None
        geo_key = self._scan_rand_key(redis_obj, "geo")
        if geo_key:
            existing_members = redis_obj.zrange(geo_key, 0, -1)
            if existing_members:
                member = random.choice(existing_members).decode('utf-8') if isinstance(existing_members[0], bytes) else random.choice(existing_members)
                key = geo_key  # Use the key that has the member
        
        # Fallback to fixed member name
        if not member:
            member = self._get_geo_member_name()
        
        radius = random.uniform(1, 1000)
        unit = random.choice(['m', 'km', 'mi', 'ft'])
        
        # Optional parameters
        kwargs = {}
        if random.random() < 0.3:
            kwargs['withdist'] = True
        if random.random() < 0.3:
            kwargs['withcoord'] = True
        if random.random() < 0.2:
            kwargs['withhash'] = True
        if random.random() < 0.3:
            kwargs['sort'] = random.choice(['ASC', 'DESC'])
        
        # Count and any must be handled together (any requires count)
        if random.random() < 0.4:
            kwargs['count'] = random.randint(1, 20)
            # Only add 'any' if count is present
            if random.random() < 0.3:
                kwargs['any'] = True
        
        # Sometimes store results
        if random.random() < 0.2 and not any(k.startswith('with') for k in kwargs):
            if random.random() < 0.5:
                kwargs['store'] = f"geo_store_{self._rand_str(5)}"
            else:
                kwargs['store_dist'] = f"geo_dist_{self._rand_str(5)}"
        
        pipe.georadiusbymember(key, member, radius, unit=unit, **kwargs)

    @cg_method(cmd_type="geo", can_create_key=False)
    def geosearch(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Modern geospatial search (Redis 6.2+)
        redis_obj = self._pipe_to_redis(pipe)
        kwargs = {}
        
        # Search origin: either by member or by coordinates
        if random.random() < 0.5:
            # Search by member
            geo_key = self._scan_rand_key(redis_obj, "geo")
            if geo_key:
                existing_members = redis_obj.zrange(geo_key, 0, -1)
                if existing_members:
                    member = random.choice(existing_members).decode('utf-8') if isinstance(existing_members[0], bytes) else random.choice(existing_members)
                    key = geo_key
                    kwargs['member'] = member
                else:
                    kwargs['member'] = self._get_geo_member_name()
            else:
                kwargs['member'] = self._get_geo_member_name()
        else:
            # Search by coordinates
            kwargs['longitude'] = random.uniform(geo_long_min, geo_long_max)
            kwargs['latitude'] = random.uniform(geo_lat_min, geo_lat_max)
        
        # Search area: either circular (radius) or rectangular (width/height)
        kwargs['unit'] = random.choice(['m', 'km', 'mi', 'ft'])
        
        if random.random() < 0.7:
            kwargs['radius'] = random.uniform(1, 1000)
        else:
            kwargs['width'] = random.uniform(1, 1000)
            kwargs['height'] = random.uniform(1, 1000)
        
        # Optional parameters - with proper validation rules
        if random.random() < 0.3:
            kwargs['sort'] = random.choice(['ASC', 'DESC'])
        
        # Count and any must be handled together (any requires count)
        if random.random() < 0.4:
            kwargs['count'] = random.randint(1, 20)
            # Only add 'any' if count is present
            if random.random() < 0.3:
                kwargs['any'] = True
        
        if random.random() < 0.3:
            kwargs['withcoord'] = True
        if random.random() < 0.3:
            kwargs['withdist'] = True
        if random.random() < 0.2:
            kwargs['withhash'] = True
        
        pipe.geosearch(key, **kwargs)

    @cg_method(cmd_type="geo", can_create_key=False)
    def geosearchstore(self, pipe: redis.client.Pipeline, key: str) -> None:
        # Store geosearch results in a destination key
        redis_obj = self._pipe_to_redis(pipe)
        dest_key = f"geo_search_result_{self._rand_str(5)}"
        kwargs = {}
        
        # Search origin
        if random.random() < 0.5:
            # Search by member
            geo_key = self._scan_rand_key(redis_obj, "geo")
            if geo_key:
                existing_members = redis_obj.zrange(geo_key, 0, -1)
                if existing_members:
                    member = random.choice(existing_members).decode('utf-8') if isinstance(existing_members[0], bytes) else random.choice(existing_members)
                    key = geo_key
                    kwargs['member'] = member
                else:
                    kwargs['member'] = self._get_geo_member_name()
            else:
                kwargs['member'] = self._get_geo_member_name()
        else:
            kwargs['longitude'] = random.uniform(geo_long_min, geo_long_max)
            kwargs['latitude'] = random.uniform(geo_lat_min, geo_lat_max)
        
        # Search area
        kwargs['unit'] = random.choice(['m', 'km', 'mi', 'ft'])
        
        if random.random() < 0.7:
            kwargs['radius'] = random.uniform(1, 1000)
        else:
            kwargs['width'] = random.uniform(1, 1000)
            kwargs['height'] = random.uniform(1, 1000)
        
        # Optional parameters - respect validation rules
        if random.random() < 0.3:
            kwargs['sort'] = random.choice(['ASC', 'DESC'])
        
        # Count and any must be handled together (any requires count)
        if random.random() < 0.4:
            kwargs['count'] = random.randint(1, 20)
            # Only add 'any' if count is present
            if random.random() < 0.3:
                kwargs['any'] = True
        
        if random.random() < 0.2:
            kwargs['storedist'] = True
        
        pipe.geosearchstore(dest_key, key, **kwargs)

if __name__ == "__main__":
    geo_gen = parse(GeoGen)
    geo_gen.distributions = '{"geoadd": 100, "geodel": 80, "geodist": 60, "geohash": 40, "geopos": 50, "georadius": 70, "georadiusbymember": 60, "geosearch": 50, "geosearchstore": 30}'
    geo_gen._run()
