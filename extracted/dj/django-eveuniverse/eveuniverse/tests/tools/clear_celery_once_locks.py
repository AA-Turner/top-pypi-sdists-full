"""Tool for removing all locks by celery once on tasks.

This tool can be helpful when running tests locally,
where it sometimes can happen that a lock on a task is not removed
and then the next test run will fail.

This tool assumes that celery once is using the Django backend
and that Redis is configured inj Django for caching on DB 1.
"""

import redis

REDIS_URL = "redis://localhost:6379/1"


r = redis.from_url(REDIS_URL)
deleted_count = 0
if keys := r.keys(":?:qo_eveuniverse.*"):
    print(f"We found {len(keys)} locks for eveuniverse tasks.")
    response = input("Delete (y/N)?")
    if response.lower() == "y":
        deleted_count += r.delete(*keys)
        print(f"Deleted {deleted_count} celery once keys.")
else:
    print("No locks found.")
