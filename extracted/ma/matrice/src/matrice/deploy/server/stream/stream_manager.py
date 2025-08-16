"""Simple stream manager with fixed worker counts and standard Python queues."""

import asyncio
import logging
import uuid
import queue
import threading
from typing import Dict, Optional, Any


from matrice.deploy.server.inference.inference_interface import InferenceInterface
from matrice.deploy.server.stream.kafka_consumer_worker import KafkaConsumerWorker
from matrice.deploy.server.stream.inference_worker import InferenceWorker
from matrice.deploy.server.stream.kafka_producer_worker import KafkaProducerWorker


class StreamManager:
    """Simple stream manager with fixed worker counts."""
    
    def __init__(
        self,
        session,
        deployment_id: str,
        deployment_instance_id: str,
        inference_interface: InferenceInterface,
        num_consumers: int = 1,
        num_inference_workers: int = 1,  
        num_producers: int = 1,
        app_name: str = "",
        app_version: str = "",
    ):
        """Initialize simple stream manager.
        
        Args:
            session: Session object for authentication and RPC
            deployment_id: ID of the deployment
            deployment_instance_id: ID of the deployment instance
            inference_interface: Inference interface to use for inference
            config: Stream configuration
            app_name: Application name for result formatting
            app_version: Application version for result formatting
        """
        self.session = session
        self.deployment_id = deployment_id
        self.deployment_instance_id = deployment_instance_id
        self.inference_interface = inference_interface
        self.num_consumers = num_consumers
        self.num_inference_workers = num_inference_workers
        self.num_producers = num_producers
        self.app_name = app_name
        self.app_version = app_version
        
        # Simple standard Python queues
        self.input_queue = queue.Queue()
        self.output_queue = queue.Queue()
        
        # Worker storage
        self.consumer_workers: Dict[str, KafkaConsumerWorker] = {}
        self.inference_workers: Dict[str, InferenceWorker] = {}
        self.producer_workers: Dict[str, KafkaProducerWorker] = {}
        
        # Manager state
        self.is_running = False
        
        self.logger = logging.getLogger(__name__)
        self.logger.info(
            f"Initialized SimpleStreamManager for deployment {deployment_id} "
            f"with {num_consumers} consumers, {num_inference_workers} inference workers, "
            f"{num_producers} producers"
        )
    
    async def start(self) -> None:
        """Start the stream manager and all workers."""
        if self.is_running:
            self.logger.warning("SimpleStreamManager is already running")
            return
        
        self.is_running = True
        self.logger.info("Starting SimpleStreamManager...")
        
        startup_errors = []
        
        try:
            # Start consumer workers
            self.logger.info(f"Starting {self.num_consumers} consumer workers...")
            for i in range(self.num_consumers):
                try:
                    await self._start_consumer_worker(i)
                except Exception as exc:
                    error_msg = f"Failed to start consumer worker {i}: {str(exc)}"
                    self.logger.error(error_msg)
                    startup_errors.append(error_msg)
            
            # Start inference workers  
            self.logger.info(f"Starting {self.num_inference_workers} inference workers...")
            for i in range(self.num_inference_workers):
                try:
                    await self._start_inference_worker(i)
                except Exception as exc:
                    error_msg = f"Failed to start inference worker {i}: {str(exc)}"
                    self.logger.error(error_msg)
                    startup_errors.append(error_msg)
            
            # Start producer workers
            self.logger.info(f"Starting {self.num_producers} producer workers...")
            for i in range(self.num_producers):
                try:
                    await self._start_producer_worker(i)
                except Exception as exc:
                    error_msg = f"Failed to start producer worker {i}: {str(exc)}"
                    self.logger.error(error_msg)
                    startup_errors.append(error_msg)
            
            # Check if we have enough workers running
            running_consumers = len([w for w in self.consumer_workers.values() if w.is_running])
            running_inference = len([w for w in self.inference_workers.values() if w.is_running])
            running_producers = len([w for w in self.producer_workers.values() if w.is_running])
            
            self.logger.info(
                f"Started SimpleStreamManager with "
                f"{running_consumers}/{self.num_consumers} consumers, "
                f"{running_inference}/{self.num_inference_workers} inference workers, "
                f"{running_producers}/{self.num_producers} producers"
            )
            
            if startup_errors:
                self.logger.warning(f"Stream manager started with {len(startup_errors)} errors: {startup_errors}")
            
            # Ensure we have at least one worker of each type
            if running_consumers == 0:
                raise RuntimeError("No consumer workers started successfully")
            if running_inference == 0:
                raise RuntimeError("No inference workers started successfully")
            if running_producers == 0:
                raise RuntimeError("No producer workers started successfully")
            
        except Exception as exc:
            self.logger.error(f"Failed to start SimpleStreamManager: {str(exc)}")
            await self.stop()
            raise
    
    async def stop(self) -> None:
        """Stop the stream manager and all workers."""
        if not self.is_running:
            return
        
        self.logger.info("Stopping SimpleStreamManager...")
        self.is_running = False
        
        # Stop all workers
        all_stop_tasks = []
        
        # Stop consumers
        for worker in self.consumer_workers.values():
            all_stop_tasks.append(asyncio.create_task(worker.stop()))
        
        # Stop inference workers
        for worker in self.inference_workers.values():
            all_stop_tasks.append(asyncio.create_task(worker.stop()))
        
        # Stop producers
        for worker in self.producer_workers.values():
            all_stop_tasks.append(asyncio.create_task(worker.stop()))
        
        # Wait for all to stop
        if all_stop_tasks:
            try:
                results = await asyncio.wait_for(
                    asyncio.gather(*all_stop_tasks, return_exceptions=True),
                    timeout=30.0
                )
                
                # Check for any exceptions during shutdown
                shutdown_errors = []
                for i, result in enumerate(results):
                    if isinstance(result, Exception):
                        shutdown_errors.append(f"Worker {i} shutdown error: {str(result)}")
                
                if shutdown_errors:
                    self.logger.warning(f"Encountered {len(shutdown_errors)} errors during shutdown: {shutdown_errors}")
                    
            except asyncio.TimeoutError:
                self.logger.warning("Some workers did not stop within timeout")
                # Force cancellation of remaining tasks
                for task in all_stop_tasks:
                    if not task.done():
                        task.cancel()
        
        # Clear worker dictionaries
        self.consumer_workers.clear()
        self.inference_workers.clear()
        self.producer_workers.clear()
        
        self.logger.info("Stopped SimpleStreamManager")
    
    async def _start_consumer_worker(self, worker_index: int) -> None:
        """Start a consumer worker."""
        worker_id = f"consumer_{worker_index}_{uuid.uuid4().hex[:8]}"
        
        # Create simple queue wrapper for consumer worker
        queue_wrapper = SimpleQueueWrapper(self.input_queue)
        
        worker = KafkaConsumerWorker(
            worker_id=worker_id,
            session=self.session,
            deployment_id=self.deployment_id,
            deployment_instance_id=self.deployment_instance_id,
            input_queue=queue_wrapper
        )
        
        await worker.start()
        self.consumer_workers[worker_id] = worker
        self.logger.info(f"Started consumer worker: {worker_id}")
    
    async def _start_inference_worker(self, worker_index: int) -> None:
        """Start an inference worker."""
        worker_id = f"inference_{worker_index}_{uuid.uuid4().hex[:8]}"
        
        # Create simple queue wrappers
        input_wrapper = SimpleQueueWrapper(self.input_queue)
        output_wrapper = SimpleQueueWrapper(self.output_queue)
        
        worker = InferenceWorker(
            worker_id=worker_id,
            inference_interface=self.inference_interface,
            input_queue=input_wrapper,
            output_queue=output_wrapper,
            enable_video_buffering=True,
            ssim_threshold=0.95,
            cache_size=100
        )
        
        await worker.start()
        self.inference_workers[worker_id] = worker
        self.logger.info(f"Started inference worker: {worker_id}")
    
    async def _start_producer_worker(self, worker_index: int) -> None:
        """Start a producer worker."""
        worker_id = f"producer_{worker_index}_{uuid.uuid4().hex[:8]}"
        
        # Create simple queue wrapper
        queue_wrapper = SimpleQueueWrapper(self.output_queue)
        
        worker = KafkaProducerWorker(
            worker_id=worker_id,
            session=self.session,
            deployment_id=self.deployment_id,
            deployment_instance_id=self.deployment_instance_id,
            output_queue=queue_wrapper,
            app_name=self.app_name,
            app_version=self.app_version,
        )
        
        await worker.start()
        self.producer_workers[worker_id] = worker
        self.logger.info(f"Started producer worker: {worker_id}")
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get simple metrics."""
        consumer_metrics = {}
        for worker_id, worker in self.consumer_workers.items():
            consumer_metrics[worker_id] = worker.get_metrics()
        
        inference_metrics = {}
        for worker_id, worker in self.inference_workers.items():
            inference_metrics[worker_id] = worker.get_metrics()
        
        producer_metrics = {}
        for worker_id, worker in self.producer_workers.items():
            producer_metrics[worker_id] = worker.get_metrics()
        
        return {
            "is_running": self.is_running,
            "worker_counts": {
                "consumers": len(self.consumer_workers),
                "inference_workers": len(self.inference_workers), 
                "producers": len(self.producer_workers),
            },
            "queue_sizes": {
                "input_queue": self.input_queue.qsize(),
                "output_queue": self.output_queue.qsize(),
            },
            "worker_metrics": {
                "consumers": consumer_metrics,
                "inference": inference_metrics,
                "producers": producer_metrics,
            },
        }


class SimpleQueueWrapper:
    """Simple wrapper to make standard queue.Queue compatible with async worker interfaces."""
    
    def __init__(self, std_queue: queue.Queue):
        self.queue = std_queue
    
    async def put(self, item: Any, timeout: Optional[float] = None) -> bool:
        """Put item in queue (non-blocking for async compatibility)."""
        try:
            # Use put_nowait for non-blocking operation in async context
            self.queue.put_nowait(item)
            return True
        except queue.Full:
            return False
    
    async def get(self, timeout: Optional[float] = None) -> Optional[Any]:
        """Get item from queue."""
        try:
            # Use get with timeout in a thread executor to avoid blocking the event loop
            loop = asyncio.get_event_loop()
            if timeout:
                item = await loop.run_in_executor(
                    None, lambda: self.queue.get(timeout=timeout)
                )
            else:
                item = await loop.run_in_executor(
                    None, lambda: self.queue.get(timeout=1.0)  # 1 second default to avoid indefinite blocking
                )
            return item
        except queue.Empty:
            return None
        except Exception:
            return None
    
    def qsize(self) -> int:
        """Get queue size."""
        return self.queue.qsize()
    
    def is_under_backpressure(self) -> bool:
        """Simple check for queue fullness."""
        return self.queue.full()

