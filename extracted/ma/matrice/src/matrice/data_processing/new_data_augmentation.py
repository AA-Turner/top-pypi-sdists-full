import logging
import traceback
import json
import requests
import cv2
import numpy as np
import time
from queue import Queue
from typing import Any, Optional, List, Dict, Tuple
from kafka import KafkaConsumer, KafkaProducer
from abc import ABC, abstractmethod
import albumentations as A

# Fix imports to use existing codebase infrastructure
from .pipeline import Pipeline  # Fix relative import
from .augmentation_utils.base import ImageAugmentationStrategy  # Use existing base class
from .augmentation_utils.strategies import (
    BlurAugmentation,
    BrightnessContrastAugmentation,
    HorizontalFlipAugmentation,
    RandomAffineAugmentation,
    ColorJitterAugmentation,
    HueSaturationValueAugmentation,
    # Add other augmentation strategy imports as needed
)

class DatasetItem:
    """Represents a dataset item with all necessary metadata"""
    
    def __init__(self, json_data: Dict):
        # Store the original JSON data
        self.json_data = json_data.copy()
        
        # Easy access properties
        self.id = json_data.get('_id') or json_data.get('id')
        self.download_url = json_data.get('fileLocation') or json_data.get('download_url')
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

class AugmentationStrategyFactory:
    """Factory class to create augmentation strategy instances"""
    
    STRATEGIES = {
        'blur': BlurAugmentation,
        'brightness_contrast': BrightnessContrastAugmentation,
        'horizontal_flip': HorizontalFlipAugmentation,
        'vertical_flip': HorizontalFlipAugmentation,  # Use horizontal flip for now
        'rotation': RandomAffineAugmentation,
        'random_affine': RandomAffineAugmentation,
        'color_jitter': ColorJitterAugmentation,
        'flip': HorizontalFlipAugmentation,
        'hsv': HueSaturationValueAugmentation,
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

def kafka_consumer_producer(
    consumer_topic: str,
    producer_topic: str,
    bootstrap_servers: List[str],
    dataset_items_queue: Queue,
    output_queue: Queue,
    consumer_group: str = 'augmentation_pipeline'
):
    """
    Kafka consumer to populate input queue and producer to publish output
    """
    # Consumer setup
    consumer = KafkaConsumer(
        consumer_topic,
        bootstrap_servers=bootstrap_servers,
        group_id=consumer_group,
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        auto_offset_reset='latest'
    )
    
    # Producer setup
    producer = KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )
    
    def consume_messages():
        """Consume messages from Kafka and add to input queue"""
        logging.info("Starting Kafka consumer for topic: %s", consumer_topic)
        for message in consumer:
            try:
                dataset_item_data = message.value
                dataset_item = DatasetItem(dataset_item_data)
                dataset_items_queue.put(dataset_item)
                logging.debug("Added dataset item %s to queue", dataset_item.id)
            except Exception as e:
                logging.error("Error processing Kafka message: %s", e)
    
    def produce_messages():
        """Consume from output queue and publish to Kafka"""
        logging.info("Starting Kafka producer for topic: %s", producer_topic)
        while True:
            try:
                result_item = output_queue.get()
                if result_item is None:  # Poison pill to stop
                    break
                
                # Get the updated JSON data
                result_data = result_item.get_json_data()
                
                producer.send(producer_topic, value=result_data)
                logging.debug("Published result for dataset item %s", result_item.id)
                output_queue.task_done()
            except Exception as e:
                logging.error("Error publishing to Kafka: %s", e)
    
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
            
            logging.debug("Processing dataset item: %s", dataset_item.id)
            download_queue.put(dataset_item)
            dataset_items_queue.task_done()
            
        except Exception as e:
            logging.error("Error in fetch dataset items stage: %s", e)

def download_images_stage(download_queue: Queue, augmentation_queue: Queue, **kwargs):
    """
    Stage 2: Download images from S3 URLs
    """
    while True:
        try:
            dataset_item = download_queue.get()
            if dataset_item is None:
                augmentation_queue.put(None)
                download_queue.task_done()
                break
                
            response = requests.get(dataset_item.download_url, timeout=30)
            response.raise_for_status()
            
            # Convert to numpy array
            image_array = np.frombuffer(response.content, np.uint8)
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            
            if image is None:
                logging.error("Failed to decode image for item %s", dataset_item.id)
                download_queue.task_done()
                continue
            
            # Convert BGR to RGB (OpenCV uses BGR by default)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            dataset_item.image = image
            
            # Update JSON with original image dimensions
            height, width = image.shape[:2]
            # dataset_item.update_json_fields({
            #     'original_image_height': height,
            #     'original_image_width': width,
            #     'image_height': height,
            #     'image_width': width,
            #     'height': height,  # Alternative field name
            #     'width': width     # Alternative field name
            # })
            
            logging.debug("Downloaded image for item %s, size: %dx%d", 
                         dataset_item.id, width, height)
            
            augmentation_queue.put(dataset_item)
            download_queue.task_done()
           
        except Exception as e:
            logging.error("Error downloading image: %s", e)
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
                augmentation_queue.task_done()
                break
            
            if dataset_item.image is None:
                logging.error("No image found for dataset item %s", dataset_item.id)
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
                    logging.debug("Applied %s to item %s", aug_config['aug_name'], dataset_item.id)
                    
                except Exception as e:
                    logging.error("Error applying augmentation %s to item %s: %s", 
                                aug_config.get('aug_name'), dataset_item.id, e)
            
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
            
            logging.debug("Completed augmentations for item %s", dataset_item.id)
            update_queue.put(dataset_item)
            augmentation_queue.task_done()
            
        except Exception as e:
            logging.error("Error in augmentation stage: %s", e)
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
                update_queue.task_done()
                break
            
            if dataset_item.augmented_image is None:
                logging.error("No augmented image found for dataset item %s", dataset_item.id)
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
                logging.debug("Uploaded augmented image for item %s to %s", 
                             dataset_item.id, dataset_item.upload_url)
                
                # Update JSON with upload confirmation
                dataset_item.update_json_fields({
                    'upload_status': 'completed',
                    'upload_timestamp': str(int(time.time()))
                })
            else:
                logging.error("Failed to upload image for item %s. Status: %s", 
                             dataset_item.id, upload_response.status_code)
                dataset_item.update_json_fields({
                    'upload_status': 'failed',
                    'upload_error': f'HTTP {upload_response.status_code}'
                })
            
            # Add to output queue
            output_queue.put(dataset_item)
            update_queue.task_done()
            
        except Exception as e:
            logging.error("Error in update and upload stage: %s", e)
            # Still add to output queue even if upload failed
            if 'dataset_item' in locals():
                dataset_item.update_json_fields({
                    'upload_status': 'failed',
                    'upload_error': str(e)
                })
                output_queue.put(dataset_item)
            update_queue.task_done()

def create_data_augmentation_pipeline(
    kafka_config: Dict[str, Any]
) -> Optional[Pipeline]:
    """
    Create and configure the data augmentation pipeline
    
    Args:
        kafka_config: Configuration for Kafka consumer/producer
        
    Returns:
        Configured Pipeline instance
    """
    try:
        logging.info("Setting up data augmentation pipeline")
        
        # Create queues for pipeline stages
        dataset_items_queue = Queue(maxsize=1000)
        download_queue = Queue(maxsize=500)
        augmentation_queue = Queue(maxsize=500)
        update_queue = Queue(maxsize=500)
        output_queue = Queue(maxsize=1000)
        
        # Setup Kafka consumer and producer
        consume_fn, produce_fn = kafka_consumer_producer(
            consumer_topic=kafka_config['consumer_topic'],
            producer_topic=kafka_config['producer_topic'],
            bootstrap_servers=kafka_config['bootstrap_servers'],
            dataset_items_queue=dataset_items_queue,
            output_queue=output_queue,
            consumer_group=kafka_config.get('consumer_group', 'augmentation_pipeline')
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
        
        logging.info("Data augmentation pipeline configuration complete")
        return pipeline
        
    except Exception as e:
        logging.error("Error setting up data augmentation pipeline: %s", e)
        traceback.print_exc()
        raise