"""Preload platform code and fork before receiving any authored assignment."""

from labqoat.compute.fork_worker.fork_worker import ForkWorker

if __name__ == "__main__":
    ForkWorker.main()
