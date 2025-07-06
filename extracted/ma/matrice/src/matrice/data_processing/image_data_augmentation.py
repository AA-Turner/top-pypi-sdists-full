import logging
import traceback
import json
import requests
import cv2
import numpy as np
import time
from queue import Queue, Empty
from typing import Any, Optional, List, Dict, Tuple
from kafka import KafkaConsumer, KafkaProducer
from abc import ABC, abstractmethod
import albumentations as A
import threading

# Assuming these are imported from your existing codebase
from pipeline import Pipeline  # Your existing Pipeline class
from .augmentation_utils.strategies import (
    CompressionArtifactsAugmentation,
    HorizontalFlipAugmentation,
    VerticalFlipAugmentation,
    RotationAugmentation,
    BrightnessContrastAugmentation,
    bit_depth_reduction
    # Add other augmentation strategy imports as needed
)

class ImageAugmentationStrategy(ABC):
    """Base class for image augmentation strategies"""
    
    @abstractmethod
    def apply(self, image, bboxes, bbox_format='coco') -> Tuple[np.ndarray, int, int, List[List[float]]]:
        pass

class DatasetItem:
    """Represents a dataset item with all necessary metadata"""
    
    def __init__(self, json_data: Dict):
        # Store the original JSON data
        self.json_data = json_data.copy()
        
        # Easy access properties
        self.id = json_data.get('id')
        self.download_url = json_data.get('download_url')
        self.upload_url = json_data.get('upload_url')
        self.augmentations = json_data.get('augmentations', [])
        
        # Image processing properties
        self.image = None
        self.augmented_image = None
    
    def update_json_fields(self, updated_fields: Dict):
        """Update specific fields in the JSON data"""
        self.json_data.update(updated_fields)
    
    def get_json_data(self) -> Dict:
        """Get the updated JSON data"""
        return self.json_data

class PaginationRequest:
    """Represents a pagination request"""
    
    def __init__(self, page_number: int, page_size: int = 100, dataset_id: str = None, **kwargs):
        self.page_number = page_number
        self.page_size = page_size
        self.dataset_id = dataset_id
        self.additional_params = kwargs
        self.timestamp = int(time.time())
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for Kafka message"""
        return {
            'page_number': self.page_number,
            'page_size': self.page_size,
            'dataset_id': self.dataset_id,
            'timestamp': self.timestamp,
            **self.additional_params
        }

class PaginatedDataManager:
    """Manages paginated data requests and responses"""
    
    def __init__(self, 
                 request_topic: str,
                 response_topic: str,
                 bootstrap_servers: List[str],
                 consumer_group: str = 'pagination_consumer',
                 page_size: int = 100,
                 max_retries: int = 3,
                 retry_delay: int = 5):
        
        self.request_topic = request_topic
        self.response_topic = response_topic
        self.bootstrap_servers = bootstrap_servers
        self.consumer_group = consumer_group
        self.page_size = page_size
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        
        # Track pagination state
        self.current_page = 1
        self.total_pages = None
        self.is_complete = False
        
        # Thread-safe data structures
        self.pending_requests = {}  # page_number -> request_time
        self.received_pages = {}    # page_number -> data
        self.lock = threading.Lock()
        
        # Kafka setup
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )
        
        self.consumer = KafkaConsumer(
            response_topic,
            bootstrap_servers=bootstrap_servers,
            group_id=consumer_group,
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            auto_offset_reset='latest',
            consumer_timeout_ms=1000  # 1 second timeout
        )
    
    def request_page(self, page_number: int, dataset_id: str = None, **kwargs) -> bool:
        """Request a specific page of data"""
        try:
            pagination_request = PaginationRequest(
                page_number=page_number,
                page_size=self.page_size,
                dataset_id=dataset_id,
                **kwargs
            )
            
            with self.lock:
                self.pending_requests[page_number] = time.time()
            
            self.producer.send(self.request_topic, value=pagination_request.to_dict())
            logging.debug(f"Requested page {page_number}")
            return True
            
        except Exception as e:
            logging.error(f"Error requesting page {page_number}: {e}")
            return False
    
    def check_for_responses(self) -> List[DatasetItem]:
        """Check for and process responses from Kafka"""
        items = []
        
        try:
            # Poll for messages with timeout
            message_batch = self.consumer.poll(timeout_ms=1000)
            
            for topic_partition, messages in message_batch.items():
                for message in messages:
                    try:
                        response_data = message.value
                        page_number = response_data.get('page_number')
                        page_data = response_data.get('data', [])
                        total_pages = response_data.get('total_pages')
                        
                        if page_number is not None:
                            with self.lock:
                                # Remove from pending requests
                                if page_number in self.pending_requests:
                                    del self.pending_requests[page_number]
                                
                                # Store received data
                                self.received_pages[page_number] = page_data
                                
                                # Update total pages if provided
                                if total_pages is not None:
                                    self.total_pages = total_pages
                            
                            # Convert to DatasetItem objects
                            for item_data in page_data:
                                items.append(DatasetItem(item_data))
                            
                            logging.debug(f"Received page {page_number} with {len(page_data)} items")
                    
                    except Exception as e:
                        logging.error(f"Error processing response message: {e}")
        
        except Exception as e:
            logging.debug(f"No messages available or error polling: {e}")
        
        return items
    
    def retry_failed_requests(self):
        """Retry requests that haven't received responses within timeout"""
        current_time = time.time()
        
        with self.lock:
            failed_pages = []
            for page_number, request_time in self.pending_requests.items():
                if current_time - request_time > self.retry_delay:
                    failed_pages.append(page_number)
            
            # Retry failed requests
            for page_number in failed_pages:
                retry_count = getattr(self, f'_retry_count_{page_number}', 0)
                if retry_count < self.max_retries:
                    logging.warning(f"Retrying request for page {page_number} (attempt {retry_count + 1})")
                    self.request_page(page_number)
                    setattr(self, f'_retry_count_{page_number}', retry_count + 1)
                else:
                    logging.error(f"Max retries exceeded for page {page_number}")
                    del self.pending_requests[page_number]
    
    def is_pagination_complete(self) -> bool:
        """Check if all pages have been received"""
        if self.total_pages is None:
            return False
        
        with self.lock:
            return (len(self.received_pages) >= self.total_pages and 
                   len(self.pending_requests) == 0)

class AugmentationStrategyFactory:
    """Factory class to create augmentation strategy instances"""
    
    STRATEGIES = {
        'compression_artifacts': CompressionArtifactsAugmentation,
        'horizontal_flip': HorizontalFlipAugmentation,
        'vertical_flip': VerticalFlipAugmentation,
        'rotation': RotationAugmentation,
        'brightness_contrast': BrightnessContrastAugmentation,
        # Add more strategies as needed
    }
    
    @classmethod
    def create_strategy(cls, aug_config: Dict) -> ImageAugmentationStrategy:
        """Create augmentation strategy from configuration"""
        aug_name = aug_config.get('aug_name')
        if aug_name not in cls.STRATEGIES:
            raise ValueError(f"Unknown augmentation strategy: {aug_name}")
        
        # Remove aug_name from config and pass rest as kwargs
        strategy_params = {k: v for k, v in aug_config.items() if k != 'aug_name'}
        return cls.STRATEGIES[aug_name](**strategy_params)

def paginated_kafka_consumer_producer(
    request_topic: str,
    response_topic: str,
    producer_topic: str,
    bootstrap_servers: List[str],
    dataset_items_queue: Queue,
    output_queue: Queue,
    consumer_group: str = 'augmentation_pipeline',
    dataset_id: str = None,
    page_size: int = 100,
    **kwargs
):
    """
    Paginated Kafka consumer to populate input queue and producer to publish output
    """
    
    # Setup paginated data manager
    data_manager = PaginatedDataManager(
        request_topic=request_topic,
        response_topic=response_topic,
        bootstrap_servers=bootstrap_servers,
        consumer_group=consumer_group,
        page_size=page_size
    )
    
    # Producer setup for output
    producer = KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )
    
    def consume_messages():
        """Consume messages from Kafka using pagination"""
        logging.info("Starting paginated Kafka consumer")
        
        # Request first page
        data_manager.request_page(1, dataset_id=dataset_id, **kwargs)
        
        while not data_manager.is_pagination_complete():
            try:
                # Check for responses
                items = data_manager.check_for_responses()
                
                # Add items to queue
                for item in items:
                    dataset_items_queue.put(item)
                    logging.debug(f"Added dataset item {item.id} to queue")
                
                # Retry failed requests
                data_manager.retry_failed_requests()
                
                # Request next page if we have total_pages info
                if (data_manager.total_pages is not None and 
                    data_manager.current_page < data_manager.total_pages):
                    
                    next_page = data_manager.current_page + 1
                    if next_page not in data_manager.pending_requests and next_page not in data_manager.received_pages:
                        data_manager.request_page(next_page, dataset_id=dataset_id, **kwargs)
                        data_manager.current_page = next_page
                
                # Small delay to prevent busy waiting
                time.sleep(0.1)
                
            except Exception as e:
                logging.error(f"Error in paginated consumer: {e}")
                time.sleep(1)
        
        logging.info("Pagination complete, all data consumed")
        # Signal end of data
        dataset_items_queue.put(None)
    
    def produce_messages():
        """Consume from output queue and publish to Kafka"""
        logging.info(f"Starting Kafka producer for topic: {producer_topic}")
        while True:
            try:
                result_item = output_queue.get()
                if result_item is None:  # Poison pill to stop
                    break
                
                # Get the updated JSON data
                result_data = result_item.get_json_data()
                
                producer.send(producer_topic, value=result_data)
                logging.debug(f"Published result for dataset item {result_item.id}")
                output_queue.task_done()
            except Exception as e:
                logging.error(f"Error publishing to Kafka: {e}")
    
    return consume_messages, produce_messages

def fetch_dataset_items_stage(dataset_items_queue: Queue, download_queue: Queue, **kwargs):
    """
    Stage 1: Fetch dataset items from input queue
    This is essentially a pass-through stage that can add any preprocessing if needed
    """
    while True:
        try:
            dataset_item = dataset_items_queue.get()
            if dataset_item is None:
                download_queue.put(None)
                break
            
            logging.debug(f"Processing dataset item: {dataset_item.id}")
            download_queue.put(dataset_item)
            dataset_items_queue.task_done()
            
        except Exception as e:
            logging.error(f"Error in fetch dataset items stage: {e}")

def download_images_stage(download_queue: Queue, augmentation_queue: Queue, **kwargs):
    """
    Stage 2: Download images from S3 URLs
    """
    while True:
        try:
            dataset_item = download_queue.get()
            if dataset_item is None:
                augmentation_queue.put(None)
                break
            
            response = requests.get(dataset_item.download_url, timeout=30)
            response.raise_for_status()
            
            # Convert to numpy array
            image_array = np.frombuffer(response.content, np.uint8)
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            
            if image is None:
                logging.error(f"Failed to decode image for item {dataset_item.id}")
                download_queue.task_done()
                continue
            
            # Convert BGR to RGB (OpenCV uses BGR by default)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            dataset_item.image = image
            
            # Update JSON with original image dimensions
            height, width = image.shape[:2]
            
            logging.debug(f"Downloaded image for item {dataset_item.id}, size: {width}x{height}")
            
            augmentation_queue.put(dataset_item)
            download_queue.task_done()
           
        except Exception as e:
            logging.error(f"Error downloading image: {e}")
            if 'dataset_item' in locals():
                download_queue.task_done()

def apply_augmentations_stage(augmentation_queue: Queue, update_queue: Queue, **kwargs):
    """
    Stage 3: Apply augmentations to images
    """
    while True:
        try:
            dataset_item = augmentation_queue.get()
            if dataset_item is None: 
                update_queue.put(None)
                break
            
            if dataset_item.image is None:
                logging.error(f"No image found for dataset item {dataset_item.id}")
                augmentation_queue.task_done()
                continue
            
            current_image = dataset_item.image.copy()
            current_bboxes = dataset_item.json_data.get('bboxes', []).copy()
            augmentations_applied = []
            
            for aug_config in dataset_item.augmentations:
                try:
                    strategy = AugmentationStrategyFactory.create_strategy(aug_config)
                    
                    # Apply augmentation
                    augmented_image, new_height, new_width, new_bboxes = strategy.apply(
                        current_image, current_bboxes, bbox_format='coco'
                    )
                    
                    # Update current state
                    current_image = augmented_image
                    current_bboxes = new_bboxes
                    
                    augmentations_applied.append(aug_config['aug_name'])
                    logging.debug(f"Applied {aug_config['aug_name']} to item {dataset_item.id}")
                    
                except Exception as e:
                    logging.error(f"Error applying augmentation {aug_config.get('aug_name')} to item {dataset_item.id}: {e}")
            
            # Update dataset item with final results
            dataset_item.augmented_image = current_image
            
            # Update JSON fields with new values
            dataset_item.update_json_fields({
                'bboxes': current_bboxes,
                'image_height': current_image.shape[0],
                'image_width': current_image.shape[1],
                'height': current_image.shape[0],  
                'width': current_image.shape[1],   
                'augmentations_applied': augmentations_applied
            })
            
            logging.debug(f"Completed augmentations for item {dataset_item.id}")
            update_queue.put(dataset_item)
            augmentation_queue.task_done()
            
        except Exception as e:
            logging.error(f"Error in augmentation stage: {e}")
            if 'dataset_item' in locals():
                augmentation_queue.task_done()

def update_and_upload_stage(update_queue: Queue, output_queue: Queue, **kwargs):
    """
    Stage 4: Update dataset item metadata and upload augmented image to S3
    """
    while True:
        try:
            dataset_item = update_queue.get()
            if dataset_item is None:  # Poison pill
                output_queue.put(None)
                break
            
            if dataset_item.augmented_image is None:
                logging.error(f"No augmented image found for dataset item {dataset_item.id}")
                update_queue.task_done()
                continue
            
            # Convert image back to BGR for encoding
            image_bgr = cv2.cvtColor(dataset_item.augmented_image, cv2.COLOR_RGB2BGR)
            
            # Encode image
            _, img_encoded = cv2.imencode('.jpg', image_bgr)
            img_bytes = img_encoded.tobytes()
            
            # Upload using the pre-signed URL (assuming it's a pre-signed upload URL)
            upload_response = requests.put(
                dataset_item.upload_url,
                data=img_bytes,
                headers={'Content-Type': 'image/jpeg'},
                timeout=30
            )
            
            if upload_response.status_code in [200, 201, 204]:
                logging.debug(f"Uploaded augmented image for item {dataset_item.id}")
                
                # Update JSON with upload confirmation
                dataset_item.update_json_fields({
                    'upload_status': 'completed',
                    'upload_timestamp': str(int(time.time()))
                })
            else:
                logging.error(f"Failed to upload image for item {dataset_item.id}. Status: {upload_response.status_code}")
                dataset_item.update_json_fields({
                    'upload_status': 'failed',
                    'upload_error': f'HTTP {upload_response.status_code}'
                })
            
            # Add to output queue
            output_queue.put(dataset_item)
            update_queue.task_done()
            
        except Exception as e:
            logging.error(f"Error in update and upload stage: {e}")
            # Still add to output queue even if upload failed
            if 'dataset_item' in locals():
                dataset_item.update_json_fields({
                    'upload_status': 'failed',
                    'upload_error': str(e)
                })
                output_queue.put(dataset_item)
                update_queue.task_done()

def create_paginated_data_augmentation_pipeline(
    kafka_config: Dict[str, Any]
) -> Optional[Pipeline]:
    """
    Create and configure the paginated data augmentation pipeline
    
    Args:
        kafka_config: Configuration for Kafka consumer/producer with pagination
        Expected keys:
        - request_topic: Topic to send pagination requests
        - response_topic: Topic to receive paginated data
        - producer_topic: Topic to publish results
        - bootstrap_servers: Kafka bootstrap servers
        - dataset_id: Optional dataset ID for filtering
        - page_size: Number of items per page (default: 100)
        
    Returns:
        Configured Pipeline instance
    """
    try:
        logging.info("Setting up paginated data augmentation pipeline")
        
        # Create queues for pipeline stages
        dataset_items_queue = Queue(maxsize=1000)
        download_queue = Queue(maxsize=500)
        augmentation_queue = Queue(maxsize=500)
        update_queue = Queue(maxsize=500)
        output_queue = Queue(maxsize=1000)
        
        # Setup paginated Kafka consumer and producer
        consume_fn, produce_fn = paginated_kafka_consumer_producer(
            request_topic=kafka_config['request_topic'],
            response_topic=kafka_config['response_topic'],
            producer_topic=kafka_config['producer_topic'],
            bootstrap_servers=kafka_config['bootstrap_servers'],
            dataset_items_queue=dataset_items_queue,
            output_queue=output_queue,
            consumer_group=kafka_config.get('consumer_group', 'augmentation_pipeline'),
            dataset_id=kafka_config.get('dataset_id'),
            page_size=kafka_config.get('page_size', 100)
        )
        
        # Create pipeline
        pipeline = Pipeline()
        
        # Add Kafka consumer as producer (entry point)
        pipeline.add_producer(
            process_fn=consume_fn,
            process_params={},
            partition_num=0
        )
        
        # Stage 1: Fetch Dataset Items
        pipeline.add_stage(
            stage_name="Fetch Dataset Items",
            process_fn=fetch_dataset_items_stage,
            pull_queue=dataset_items_queue,
            push_queue=download_queue,
            process_params={},
            num_threads=2
        )
        
        # Stage 2: Download Images
        pipeline.add_stage(
            stage_name="Download Images",
            process_fn=download_images_stage,
            pull_queue=download_queue,
            push_queue=augmentation_queue,
            process_params={},
            num_threads=10
        )
        
        # Stage 3: Apply Augmentations
        pipeline.add_stage(
            stage_name="Apply Augmentations",
            process_fn=apply_augmentations_stage,
            pull_queue=augmentation_queue,
            push_queue=update_queue,
            process_params={},
            num_threads=8
        )
        
        # Stage 4: Update Metadata and Upload
        pipeline.add_stage(
            stage_name="Update and Upload",
            process_fn=update_and_upload_stage,
            pull_queue=update_queue,
            push_queue=output_queue,
            process_params={},
            num_threads=10
        )
        
        # Add Kafka producer as final stage
        pipeline.add_stage(
            stage_name="Publish Results",
            process_fn=produce_fn,
            pull_queue=output_queue,
            process_params={},
            num_threads=2,
            is_last_stage=True
        )
        
        logging.info("Paginated data augmentation pipeline configuration complete")
        return pipeline
        
    except Exception as e:
        logging.error(f"Error setting up paginated data augmentation pipeline: {e}")
        traceback.print_exc()
        raise