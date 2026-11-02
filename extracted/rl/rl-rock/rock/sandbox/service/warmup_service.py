import asyncio
import logging

from ray.util.scheduling_strategies import NodeAffinitySchedulingStrategy

from rock.admin.proto.request import WarmupRequest
from rock.config import WarmupConfig
from rock.sandbox.job.warmup_actor import WarmupActor
from rock.utils import RayUtil


class WarmupService:
    def __init__(self, config: WarmupConfig | None = None):
        self._config = config

    async def init(self):
        asyncio.create_task(self._warmup_background())
        logging.info("WarmupService started")

    async def _warmup_background(self):
        """Execute warmup task"""
        if self._config is None or self._config.images is None:
            logging.info("WarmupService not started, no images to warmup")
            return
        for image in self._config.images:
            await self._warmup_image(image)

    async def warmup(self, request: WarmupRequest):
        await self._warmup_image(request.image)

    async def _warmup_image(self, image: str):
        """Coroutine to periodically execute warmup tasks"""
        try:
            logging.info(f"Starting warmup {image} on all Ray nodes")

            alive_worker_nodes = await RayUtil.get_alive_worker_nodes()

            logging.info(f"Found {len(alive_worker_nodes)} alive Ray worker nodes: {alive_worker_nodes}")

            # Create WarmupActor on each node and execute warmup
            warmup_futures = []
            for node in alive_worker_nodes:
                node_id = node["NodeID"]
                logging.info(f"Creating Warmup Job for {image} on node {node_id}")
                warmup_actor = WarmupActor.options(
                    scheduling_strategy=NodeAffinitySchedulingStrategy(node_id=node_id, soft=False)
                ).remote(image)
                warmup_futures.append(warmup_actor.warmup.remote())  # type: ignore

            if warmup_futures:
                # ray.get(warmup_futures)
                await RayUtil.async_ray_get(warmup_futures)
                logging.info(f"Warmup task {image} completed on all {len(alive_worker_nodes)} nodes")
            else:
                logging.warning(f"No alive nodes found for warmup {image}")

        except Exception as e:
            logging.exception(f"Warmup task {image} failed: {e}")
