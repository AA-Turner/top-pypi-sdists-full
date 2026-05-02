from redis import Redis

redis_client: Redis | None = None


def generate_redis_key(task_name: str, user_name: str = "inklov3"):
    return f"{task_name}:{user_name}"


def init_redis(host: str, port: int, password: str | None = None, db: int = 0):
    global redis_client
    redis_client = Redis(host=host, port=port, password=password, db=db)
    return redis_client


def get_redis_client():
    if redis_client is None:
        raise ValueError("Redis client not initialized")
    return redis_client
