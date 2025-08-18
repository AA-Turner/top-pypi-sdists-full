"""Simple stream manager with asyncio queues and integrated debug logging."""

import asyncio
import logging
import uuid
from typing import Dict, Optional, Any


from matrice.deploy.server.inference.inference_interface import InferenceInterface
from matrice.deploy.server.stream.kafka_consumer_worker import KafkaConsumerWorker
from matrice.deploy.server.stream.inference_worker import InferenceWorker
from matrice.deploy.server.stream.kafka_producer_worker import KafkaProducerWorker
from matrice.deploy.server.stream.stream_debug_logger import StreamDebugLogger

class StreamManager:
    """Stream manager with asyncio queues and integrated debug logging."""
    
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
        inference_pipeline_id: str = "",
        debug_logging_enabled: bool = False,
        debug_log_interval: float = 30.0,
        input_queue_maxsize: int = 0,
        output_queue_maxsize: int = 0
    ):
        """Initialize stream manager.
        
        Args:
            session: Session object for authentication and RPC
            deployment_id: ID of the deployment
            deployment_instance_id: ID of the deployment instance
            inference_interface: Inference interface to use for inference
            num_consumers: Number of consumer workers
            num_inference_workers: Number of inference workers
            num_producers: Number of producer workers
            app_name: Application name for result formatting
            app_version: Application version for result formatting
            inference_pipeline_id: ID of the inference pipeline
            debug_logging_enabled: Whether to enable debug logging
            debug_log_interval: Interval for debug logging in seconds
            input_queue_maxsize: Maximum size for input queue (0 = unlimited)
            output_queue_maxsize: Maximum size for output queue (0 = unlimited)
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
        self.inference_pipeline_id = inference_pipeline_id
        
        # Asyncio queues
        self.input_queue = asyncio.Queue(maxsize=input_queue_maxsize)
        self.output_queue = asyncio.Queue(maxsize=output_queue_maxsize)
        
        # Worker storage
        self.consumer_workers: Dict[str, KafkaConsumerWorker] = {}
        self.inference_workers: Dict[str, InferenceWorker] = {}
        self.producer_workers: Dict[str, KafkaProducerWorker] = {}
        
        # Manager state
        self.is_running = False
        self._debug_task: Optional[asyncio.Task] = None
        
        # Debug logging component
        self.debug_logger = StreamDebugLogger(
            enabled=debug_logging_enabled,
            log_interval=debug_log_interval
        )
        
        self.logger = logging.getLogger(__name__)
        self.logger.info(
            f"Initialized StreamManager for deployment {deployment_id} "
            f"with {num_consumers} consumers, {num_inference_workers} inference workers, "
            f"{num_producers} producers | Debug logging: {'ON' if debug_logging_enabled else 'OFF'} "
            f"| Queue sizes: IN:{input_queue_maxsize} OUT:{output_queue_maxsize}"
        )
    
    async def start(self) -> None:
        """Start the stream manager and all workers."""
        if self.is_running:
            self.logger.warning("StreamManager is already running")
            return
        
        self.is_running = True
        self.logger.info("Starting StreamManager...")
        
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
            
            # Start producer workers with better error handling
            self.logger.info(f"Starting {self.num_producers} producer workers...")
            for i in range(self.num_producers):
                try:
                    await self._start_producer_worker(i)
                except Exception as exc:
                    error_msg = f"Failed to start producer worker {i}: {str(exc)}"
                    self.logger.error(error_msg)
                    startup_errors.append(error_msg)
                    # Continue trying to start other workers even if one fails
            
            # Check if we have enough workers running
            running_consumers = len([w for w in self.consumer_workers.values() if w.is_running])
            running_inference = len([w for w in self.inference_workers.values() if w.is_running])
            running_producers = len([w for w in self.producer_workers.values() if w.is_running])
            
            self.logger.info(
                f"Started StreamManager with "
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
            
            # Start debug logging task if enabled
            if self.debug_logger.enabled:
                self._debug_task = asyncio.create_task(self._debug_logging_loop())
                self.logger.info("Started debug logging task")
            
        except Exception as exc:
            self.logger.error(f"Failed to start StreamManager: {str(exc)}")
            await self.stop()
            raise
    
    async def stop(self) -> None:
        """Stop the stream manager and all workers."""
        if not self.is_running:
            return
        
        self.logger.info("Stopping StreamManager...")
        self.is_running = False
        
        # Stop debug logging task
        if self._debug_task and not self._debug_task.done():
            self._debug_task.cancel()
            try:
                await asyncio.wait_for(self._debug_task, timeout=5.0)
            except (asyncio.CancelledError, asyncio.TimeoutError):
                pass
            except Exception as exc:
                self.logger.error(f"Error stopping debug task: {str(exc)}")
        
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
        
        self.logger.info("Stopped StreamManager")
    
    async def _debug_logging_loop(self) -> None:
        """Background debug logging loop."""
        try:
            while self.is_running:
                self.debug_logger.log_pipeline_status(self)
                await asyncio.sleep(1.0)  # Check every second
        except asyncio.CancelledError:
            self.logger.debug("Debug logging loop cancelled")
        except Exception as exc:
            self.logger.error(f"Error in debug logging loop: {str(exc)}")
    
    async def _start_consumer_worker(self, worker_index: int) -> None:
        """Start a consumer worker."""
        worker_id = f"consumer_{worker_index}_{uuid.uuid4().hex[:8]}"
        
        worker = KafkaConsumerWorker(
            worker_id=worker_id,
            session=self.session,
            deployment_id=self.deployment_id,
            deployment_instance_id=self.deployment_instance_id,
            input_queue=self.input_queue,  # Direct asyncio.Queue
            inference_pipeline_id=self.inference_pipeline_id
        )
        
        try:
            await worker.start()
            self.consumer_workers[worker_id] = worker
            self.logger.info(f"Started consumer worker: {worker_id}")
        except Exception as exc:
            self.logger.error(f"Failed to start consumer worker {worker_id}: {str(exc)}", exc_info=True)
            raise
    
    async def _start_inference_worker(self, worker_index: int) -> None:
        """Start an inference worker."""
        worker_id = f"inference_{worker_index}_{uuid.uuid4().hex[:8]}"
        
        worker = InferenceWorker(
            worker_id=worker_id,
            inference_interface=self.inference_interface,
            input_queue=self.input_queue,   # Direct asyncio.Queue
            output_queue=self.output_queue, # Direct asyncio.Queue
            enable_video_buffering=True,
            ssim_threshold=0.95,
            cache_size=100
        )
        
        try:
            await worker.start()
            self.inference_workers[worker_id] = worker
            self.logger.info(f"Started inference worker: {worker_id}")
        except Exception as exc:
            self.logger.error(f"Failed to start inference worker {worker_id}: {str(exc)}", exc_info=True)
            raise
    
    async def _start_producer_worker(self, worker_index: int) -> None:
        """Start a producer worker."""
        worker_id = f"producer_{worker_index}_{uuid.uuid4().hex[:8]}"
        
        worker = KafkaProducerWorker(
            worker_id=worker_id,
            session=self.session,
            deployment_id=self.deployment_id,
            deployment_instance_id=self.deployment_instance_id,
            output_queue=self.output_queue,  # Direct asyncio.Queue
            app_name=self.app_name,
            app_version=self.app_version,
            inference_pipeline_id=self.inference_pipeline_id
        )
        
        try:
            await worker.start()
            self.producer_workers[worker_id] = worker
            self.logger.info(f"Started producer worker: {worker_id}")
        except Exception as exc:
            self.logger.error(f"Failed to start producer worker {worker_id}: {str(exc)}", exc_info=True)
            raise
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get comprehensive metrics."""
        consumer_metrics = {}
        for worker_id, worker in self.consumer_workers.items():
            consumer_metrics[worker_id] = worker.get_metrics()
        
        inference_metrics = {}
        for worker_id, worker in self.inference_workers.items():
            inference_metrics[worker_id] = worker.get_metrics()
        
        producer_metrics = {}
        for worker_id, worker in self.producer_workers.items():
            producer_metrics[worker_id] = worker.get_metrics()
        
        # Queue status for asyncio.Queue
        queue_status = {
            "input_queue": {
                "size": self.input_queue.qsize(),
                "maxsize": self.input_queue.maxsize if self.input_queue.maxsize > 0 else "unlimited",
                "full": self.input_queue.full(),
                "empty": self.input_queue.empty(),
            },
            "output_queue": {
                "size": self.output_queue.qsize(),
                "maxsize": self.output_queue.maxsize if self.output_queue.maxsize > 0 else "unlimited", 
                "full": self.output_queue.full(),
                "empty": self.output_queue.empty(),
            }
        }
        
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
            "queue_status": queue_status,
            "worker_metrics": {
                "consumers": consumer_metrics,
                "inference": inference_metrics,
                "producers": producer_metrics,
            },
            "debug_logger": self.debug_logger.get_debug_summary(),
        }
    
    def enable_debug_logging(self, log_interval: Optional[float] = None):
        """Enable debug logging."""
        if log_interval is not None:
            self.debug_logger.log_interval = log_interval
        self.debug_logger.enable()
        
        # Start debug task if not running and manager is running
        if self.is_running and (not self._debug_task or self._debug_task.done()):
            self._debug_task = asyncio.create_task(self._debug_logging_loop())
            self.logger.info("Started debug logging task")
    
    def disable_debug_logging(self):
        """Disable debug logging."""
        self.debug_logger.disable()
        
        # Stop debug task if running
        if self._debug_task and not self._debug_task.done():
            self._debug_task.cancel()
            self.logger.info("Stopped debug logging task")
    
    def get_debug_summary(self) -> Dict[str, Any]:
        """Get debug logging summary."""
        return self.debug_logger.get_debug_summary()




