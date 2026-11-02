"""Launch a service-owned reusable worker container."""

from labqoat.compute.pool_worker.pool_worker import PoolWorker

if __name__ == "__main__":
    PoolWorker.main()
