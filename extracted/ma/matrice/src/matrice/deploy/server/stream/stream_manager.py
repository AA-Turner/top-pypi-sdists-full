"""Simple stream manager with priority queues and integrated debug logging."""

import asyncio
import logging
import uuid
import threading
import time
from typing import Dict, Optional, Any, Callable


from matrice.deploy.server.inference.inference_interface import InferenceInterface
from matrice.deploy.server.stream.kafka_consumer_worker import KafkaConsumerWorker
from matrice.deploy.server.stream.inference_worker import InferenceWorker
from matrice.deploy.server.stream.post_processing_worker import PostProcessingWorker
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
        num_post_processing_workers: int = 1,
        num_producers: int = 1,
        app_name: str = "",
        app_version: str = "",
        inference_pipeline_id: str = "",
        debug_logging_enabled: bool = False,
        debug_log_interval: float = 30.0,
        input_queue_maxsize: int = 0,
        post_processing_queue_maxsize: int = 0,
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
            num_post_processing_workers: Number of post-processing workers
            num_producers: Number of producer workers
            app_name: Application name for result formatting
            app_version: Application version for result formatting
            inference_pipeline_id: ID of the inference pipeline
            debug_logging_enabled: Whether to enable debug logging
            debug_log_interval: Interval for debug logging in seconds
            input_queue_maxsize: Maximum size for input queue (0 = unlimited)
            post_processing_queue_maxsize: Maximum size for post-processing queue (0 = unlimited)
            output_queue_maxsize: Maximum size for output queue (0 = unlimited)
        """
        self.session = session
        self.deployment_id = deployment_id
        self.deployment_instance_id = deployment_instance_id
        self.inference_interface = inference_interface
        self.num_consumers = num_consumers
        self.num_inference_workers = num_inference_workers
        self.num_post_processing_workers = num_post_processing_workers
        self.num_producers = num_producers
        self.app_name = app_name
        self.app_version = app_version
        self.inference_pipeline_id = inference_pipeline_id
        # Asyncio queues
        self.input_queue = asyncio.PriorityQueue(maxsize=input_queue_maxsize)
        self.post_processing_queue = asyncio.PriorityQueue(maxsize=post_processing_queue_maxsize)
        self.output_queue = asyncio.PriorityQueue(maxsize=output_queue_maxsize)
        
        # Worker storage
        self.consumer_workers: Dict[str, KafkaConsumerWorker] = {}
        self.inference_workers: Dict[str, InferenceWorker] = {}
        self.post_processing_workers: Dict[str, PostProcessingWorker] = {}
        self.producer_workers: Dict[str, KafkaProducerWorker] = {}
        
        # Thread storage for workers
        self.consumer_threads: Dict[str, threading.Thread] = {}
        self.inference_threads: Dict[str, threading.Thread] = {}
        self.post_processing_threads: Dict[str, threading.Thread] = {}
        self.producer_threads: Dict[str, threading.Thread] = {}
        
        # Manager state
        self.is_running = False
        self._debug_task: Optional[asyncio.Task] = None
        self._shutdown_event = asyncio.Event()
        
        # Debug logging component
        self.debug_logger = StreamDebugLogger(
            enabled=debug_logging_enabled,
            log_interval=debug_log_interval
        )
        
        self.logger = logging.getLogger(__name__)
        self.logger.info(
            f"Initialized StreamManager for deployment {deployment_id} "
            f"with {num_consumers} consumers, {num_inference_workers} inference workers, "
            f"{num_post_processing_workers} post-processing workers, {num_producers} producers | "
            f"Debug logging: {'ON' if debug_logging_enabled else 'OFF'} | "
            f"Queue sizes: IN:{input_queue_maxsize} PP:{post_processing_queue_maxsize} OUT:{output_queue_maxsize}"
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
            # Start all workers in separate threads
            self.logger.info("Starting all workers in separate threads...")
            
            # Start consumer workers
            self.logger.info(f"Starting {self.num_consumers} consumer workers...")
            for i in range(self.num_consumers):
                try:
                    self._start_consumer_worker(i)
                except Exception as exc:
                    error_msg = f"Failed to start consumer worker {i}: {str(exc)}"
                    self.logger.error(error_msg)
                    startup_errors.append(error_msg)
            
            # Start inference workers  
            self.logger.info(f"Starting {self.num_inference_workers} inference workers...")
            for i in range(self.num_inference_workers):
                try:
                    self._start_inference_worker(i)
                except Exception as exc:
                    error_msg = f"Failed to start inference worker {i}: {str(exc)}"
                    self.logger.error(error_msg)
                    startup_errors.append(error_msg)
            
            # Start post-processing workers
            self.logger.info(f"Starting {self.num_post_processing_workers} post-processing workers...")
            for i in range(self.num_post_processing_workers):
                try:
                    self._start_post_processing_worker(i)
                except Exception as exc:
                    error_msg = f"Failed to start post-processing worker {i}: {str(exc)}"
                    self.logger.error(error_msg)
                    startup_errors.append(error_msg)
            
            # Start producer workers with better error handling
            self.logger.info(f"Starting {self.num_producers} producer workers...")
            for i in range(self.num_producers):
                try:
                    self._start_producer_worker(i)
                except Exception as exc:
                    error_msg = f"Failed to start producer worker {i}: {str(exc)}"
                    self.logger.error(error_msg)
                    startup_errors.append(error_msg)
                    # Continue trying to start other workers even if one fails
            
            # Give threads a moment to start
            time.sleep(0.5)
            
            # Check if we have enough worker threads running
            running_consumer_threads = len([t for t in self.consumer_threads.values() if t.is_alive()])
            running_inference_threads = len([t for t in self.inference_threads.values() if t.is_alive()])
            running_post_processing_threads = len([t for t in self.post_processing_threads.values() if t.is_alive()])
            running_producer_threads = len([t for t in self.producer_threads.values() if t.is_alive()])
            
            self.logger.info(
                f"Started StreamManager with "
                f"{running_consumer_threads}/{self.num_consumers} consumer threads, "
                f"{running_inference_threads}/{self.num_inference_workers} inference threads, "
                f"{running_post_processing_threads}/{self.num_post_processing_workers} post-processing threads, "
                f"{running_producer_threads}/{self.num_producers} producer threads"
            )
            
            if startup_errors:
                self.logger.warning(f"Stream manager started with {len(startup_errors)} errors: {startup_errors}")
            
            # Ensure we have at least one worker thread of each type
            if running_consumer_threads == 0:
                raise RuntimeError("No consumer worker threads started successfully")
            if running_inference_threads == 0:
                raise RuntimeError("No inference worker threads started successfully")
            if running_post_processing_threads == 0:
                raise RuntimeError("No post-processing worker threads started successfully")
            if running_producer_threads == 0:
                raise RuntimeError("No producer worker threads started successfully")
            
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
        
        # Signal shutdown to all worker threads
        self._shutdown_event.set()
        
        # Collect all threads for shutdown
        all_threads = []
        all_threads.extend(self.consumer_threads.values())
        all_threads.extend(self.inference_threads.values())
        all_threads.extend(self.post_processing_threads.values())
        all_threads.extend(self.producer_threads.values())
        
        # Wait for all threads to stop
        if all_threads:
            try:
                shutdown_errors = []
                for thread in all_threads:
                    if thread.is_alive():
                        self.logger.debug(f"Waiting for thread {thread.name} to stop...")
                        thread.join(timeout=30.0)
                        
                        if thread.is_alive():
                            shutdown_errors.append(f"Thread {thread.name} did not stop within timeout")
                            self.logger.warning(f"Thread {thread.name} did not stop within timeout")
                        else:
                            self.logger.debug(f"Thread {thread.name} stopped successfully")
                
                if shutdown_errors:
                    self.logger.warning(f"Encountered {len(shutdown_errors)} errors during thread shutdown: {shutdown_errors}")
                    
            except Exception as exc:
                self.logger.error(f"Error during thread shutdown: {str(exc)}")
        
        # Clear worker and thread dictionaries
        self.consumer_workers.clear()
        self.inference_workers.clear()
        self.post_processing_workers.clear()
        self.producer_workers.clear()
        
        self.consumer_threads.clear()
        self.inference_threads.clear()
        self.post_processing_threads.clear()
        self.producer_threads.clear()
        
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
    
    def _run_worker_in_thread(self, worker, worker_type: str, worker_id: str) -> None:
        """Run a worker in its own thread with an asyncio event loop."""
        try:
            # Create new event loop for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            async def worker_main():
                try:
                    self.logger.info(f"Starting {worker_type} worker thread: {worker_id}")
                    await worker.start()
                    
                    # Keep the worker running until shutdown
                    while self.is_running and not self._shutdown_event.is_set():
                        await asyncio.sleep(0.1)
                        
                except asyncio.CancelledError:
                    self.logger.info(f"{worker_type} worker {worker_id} cancelled")
                except Exception as exc:
                    self.logger.error(f"Error in {worker_type} worker {worker_id}: {str(exc)}", exc_info=True)
                finally:
                    try:
                        await worker.stop()
                        self.logger.info(f"Stopped {worker_type} worker: {worker_id}")
                    except Exception as exc:
                        self.logger.error(f"Error stopping {worker_type} worker {worker_id}: {str(exc)}")
            
            # Run the worker
            loop.run_until_complete(worker_main())
            
        except Exception as exc:
            self.logger.error(f"Fatal error in {worker_type} worker thread {worker_id}: {str(exc)}", exc_info=True)
        finally:
            try:
                loop.close()
            except Exception:
                pass
    
    def _start_consumer_worker(self, worker_index: int) -> None:
        """Start a consumer worker in a separate thread."""
        worker_id = f"consumer_{worker_index}"
        
        worker = KafkaConsumerWorker(
            worker_id=worker_id,
            session=self.session,
            deployment_id=self.deployment_id,
            deployment_instance_id=self.deployment_instance_id,
            input_queue=self.input_queue,  # Direct asyncio.Queue
            inference_pipeline_id=self.inference_pipeline_id,
            app_name=self.app_name
        )
        
        try:
            # Create and start thread for this worker
            thread = threading.Thread(
                target=self._run_worker_in_thread,
                args=(worker, "consumer", worker_id),
                name=f"Consumer-{worker_id}",
                daemon=False
            )
            
            self.consumer_workers[worker_id] = worker
            self.consumer_threads[worker_id] = thread
            thread.start()
            self.logger.info(f"Started consumer worker thread: {worker_id}")
        except Exception as exc:
            self.logger.error(f"Failed to start consumer worker {worker_id}: {str(exc)}", exc_info=True)
            raise
    
    def _start_inference_worker(self, worker_index: int) -> None:
        """Start an inference worker in a separate thread."""
        worker_id = f"inference_{worker_index}"
        
        worker = InferenceWorker(
            worker_id=worker_id,
            inference_interface=self.inference_interface,
            input_queue=self.input_queue,   # Direct asyncio.Queue
            output_queue=self.post_processing_queue, # Output to post-processing queue
            enable_video_buffering=True,
            ssim_threshold=0.95,
            cache_size=100
        )
        
        try:
            # Create and start thread for this worker
            thread = threading.Thread(
                target=self._run_worker_in_thread,
                args=(worker, "inference", worker_id),
                name=f"Inference-{worker_id}",
                daemon=False
            )
            
            self.inference_workers[worker_id] = worker
            self.inference_threads[worker_id] = thread
            thread.start()
            self.logger.info(f"Started inference worker thread: {worker_id}")
        except Exception as exc:
            self.logger.error(f"Failed to start inference worker {worker_id}: {str(exc)}", exc_info=True)
            raise
    
    def _start_post_processing_worker(self, worker_index: int) -> None:
        """Start a post-processing worker in a separate thread."""
        worker_id = f"post_processing_{worker_index}"
        
        worker = PostProcessingWorker(
            worker_id=worker_id,
            inference_interface=self.inference_interface,
            input_queue=self.post_processing_queue,  # Input from post-processing queue
            output_queue=self.output_queue,  # Output to final output queue
            max_concurrent_tasks=20  # Allow up to 5 concurrent post-processing tasks
        )
        
        try:
            # Create and start thread for this worker
            thread = threading.Thread(
                target=self._run_worker_in_thread,
                args=(worker, "post_processing", worker_id),
                name=f"PostProcessing-{worker_id}",
                daemon=False
            )
            
            self.post_processing_workers[worker_id] = worker
            self.post_processing_threads[worker_id] = thread
            thread.start()
            self.logger.info(f"Started post-processing worker thread: {worker_id}")
        except Exception as exc:
            self.logger.error(f"Failed to start post-processing worker {worker_id}: {str(exc)}", exc_info=True)
            raise

    def _start_producer_worker(self, worker_index: int) -> None:
        """Start a producer worker in a separate thread."""
        worker_id = f"producer_{worker_index}"
        
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
            # Create and start thread for this worker
            thread = threading.Thread(
                target=self._run_worker_in_thread,
                args=(worker, "producer", worker_id),
                name=f"Producer-{worker_id}",
                daemon=False
            )
            
            self.producer_workers[worker_id] = worker
            self.producer_threads[worker_id] = thread
            thread.start()
            self.logger.info(f"Started producer worker thread: {worker_id}")
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
        
        post_processing_metrics = {}
        for worker_id, worker in self.post_processing_workers.items():
            post_processing_metrics[worker_id] = worker.get_metrics()
        
        producer_metrics = {}
        for worker_id, worker in self.producer_workers.items():
            producer_metrics[worker_id] = worker.get_metrics()
        
        # Queue status for asyncio.PriorityQueue
        queue_status = {
            "input_queue": {
                "size": self.input_queue.qsize(),
                "maxsize": self.input_queue.maxsize if self.input_queue.maxsize > 0 else "unlimited",
                "full": self.input_queue.full(),
                "empty": self.input_queue.empty(),
            },
            "post_processing_queue": {
                "size": self.post_processing_queue.qsize(),
                "maxsize": self.post_processing_queue.maxsize if self.post_processing_queue.maxsize > 0 else "unlimited",
                "full": self.post_processing_queue.full(),
                "empty": self.post_processing_queue.empty(),
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
                "post_processing_workers": len(self.post_processing_workers),
                "producers": len(self.producer_workers),
            },
            "queue_sizes": {
                "input_queue": self.input_queue.qsize(),
                "post_processing_queue": self.post_processing_queue.qsize(),
                "output_queue": self.output_queue.qsize(),
            },
            "queue_status": queue_status,
            "worker_metrics": {
                "consumers": consumer_metrics,
                "inference": inference_metrics,
                "post_processing": post_processing_metrics,
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




