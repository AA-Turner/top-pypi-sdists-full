import subprocess

import ray


@ray.remote(num_cpus=0)
class WarmupActor:
    """Used for preheating resources"""

    def __init__(self, image: str):
        import logging

        self.logging = logging
        self._image: str = image

    async def warmup(self):
        try:
            print(f"Start to pull image {self._image}")
            subprocess.run(["docker", "pull", self._image])
            print(f"Finish pulling image {self._image}")
        except Exception as e:
            print(f"Failed to pull image {self._image}: {e}")
