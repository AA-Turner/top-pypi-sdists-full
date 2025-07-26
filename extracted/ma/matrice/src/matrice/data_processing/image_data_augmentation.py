import logging
import traceback
import json
import requests
import cv2
import numpy as np
import time
import random
import math
from queue import Queue, Empty
from typing import Any, Optional, List, Dict, Tuple
from kafka import KafkaConsumer, KafkaProducer, TopicPartition
from abc import ABC, abstractmethod
import albumentations as A
import threading
from dataclasses import dataclass
from datetime import datetime
from collections import defaultdict
from urllib.parse import urlparse
from .pipeline import Pipeline
from .augmentation_utils.strategies import *
from typing import List, Dict, Optional
from kafka import KafkaProducer, KafkaConsumer
from scipy.special import softmax
from math import comb

MIN_DIM = 1.0

@dataclass
class AugmentationStep:
    """Represents a single augmentation step"""
    name: str
    params: Dict[str, Any]
    dynamic_prob: float = 0.5
    is_random_params: bool = False  # Indicates if augmentation uses random parameters

class ImageAugmentationStrategy(ABC):
    """Base class for image augmentation strategies"""
    @abstractmethod
    def apply(self, image, bboxes, bbox_format='coco') -> Tuple[np.ndarray, int, int, List[List[float]]]:
        pass

@dataclass
class DynamicPipelineConfig:
    """Configuration for dynamic augmentation pipeline"""
    total_new_images: int
    augmentation_pool: List[AugmentationStep]
    augmentation_id: str
    dataset_id: str
    min_augmentations_per_image: int = 1
    max_augmentations_per_image: int = 3
    source_version: str = 'v1.0'
    target_version: str = 'v1.1'
    prob_adjust_step: float = 0.05  # Configurable step size for probability updates
    prob_min: float = 0.1  # Minimum probability bound
    prob_max: float = 0.9  # Maximum probability bound

class DynamicProbabilityDistributionManager:
    """
    Manages dynamic probability distribution for augmentations with global combination tracking
    """
    NON_REPEATING_AUGS = {'flip', 'bit_depth_reduction', 'random_affine', 'color_jitter'}  # Augmentations that generate new effects on reapplication
    
    def __init__(self, config: DynamicPipelineConfig):
        self.config = config
        self.lock = threading.RLock()
        self.total_generated = 0
        self.target_images = config.total_new_images
        self.augmentation_usage = defaultdict(int)
        self.augmentation_history = []
        self.image_augmentation_history = defaultdict(set)
        self.available_images = []
        self.image_usage_count = defaultdict(int)
        self.combination_usage = defaultdict(int)  # Track global combination usage
        self._initialize_probabilities()
        self.max_attempts = self._calculate_max_attempts()
        
        logging.info(f"Initialized Dynamic Probability Manager for {self.target_images} images")
        logging.info(f"Available augmentations: {[aug.name for aug in config.augmentation_pool]}")
        logging.info(f"Calculated max attempts: {self.max_attempts}")
    
    def _calculate_max_attempts(self) -> int:
        """Calculate maximum retry attempts based on possible combinations"""
        max_combinations = sum(
            comb(len(self.config.augmentation_pool), k)
            for k in range(self.config.min_augmentations_per_image, 
                         self.config.max_augmentations_per_image + 1)
        )
        return min(max(10, max_combinations // 10), 100)  # Cap between 10 and 100
    
    def _initialize_probabilities(self):
        """Initialize dynamic probabilities using softmax"""
        base_prob = 1.0 / len(self.config.augmentation_pool)
        for aug in self.config.augmentation_pool:
            aug.dynamic_prob = base_prob
            aug.is_random_params = aug.name in self.NON_REPEATING_AUGS
            if 'prob' in aug.params:
                del aug.params['prob']
        
        self._apply_softmax_probabilities()
        logging.debug(f"Initialized {len(self.config.augmentation_pool)} augmentations with base probability {base_prob}")
    
    def _apply_softmax_probabilities(self):
        """Apply softmax to normalize probabilities"""
        raw_scores = [aug.dynamic_prob for aug in self.config.augmentation_pool]
        normalized_probs = softmax(raw_scores)
        for aug, prob in zip(self.config.augmentation_pool, normalized_probs):
            aug.dynamic_prob = max(self.config.prob_min, min(self.config.prob_max, prob))
        
        logging.debug(f"Softmax probabilities: {[(aug.name, aug.dynamic_prob) for aug in self.config.augmentation_pool]}")
    
    def _update_probabilities(self):
        """Update probabilities based on usage and combination coverage"""
        if not self.augmentation_usage:
            return
        
        total_usage = sum(self.augmentation_usage.values())
        avg_usage = total_usage / len(self.config.augmentation_pool) if total_usage > 0 else 1
        
        # Calculate combination coverage factor
        total_combinations = sum(self.combination_usage.values())
        avg_combination_usage = total_combinations / len(self.combination_usage) if total_combinations > 0 else 1
        
        for aug in self.config.augmentation_pool:
            current_usage = self.augmentation_usage.get(aug.name, 0)
            usage_ratio = current_usage / max(avg_usage, 1)
            
            # Adjust probability based on usage and combination coverage
            adjustment = self.config.prob_adjust_step * (1 - usage_ratio)
            aug.dynamic_prob += adjustment
            
            # Boost probability for augmentations in less-used combinations
            aug_combinations = [c for c, count in self.combination_usage.items() 
                              if aug.name in c and count < avg_combination_usage]
            if aug_combinations:
                aug.dynamic_prob += self.config.prob_adjust_step * 0.5
        
        self._apply_softmax_probabilities()
        logging.debug(f"Updated probabilities: {[(aug.name, aug.dynamic_prob) for aug in self.config.augmentation_pool]}")
    
    def add_available_image(self, image_id: str):
        """Add an image ID to the pool of available images"""
        with self.lock:
            self.available_images.append(image_id)
            logging.debug(f"Added image {image_id} to available pool. Total available: {len(self.available_images)}")
    
    def select_augmentations_for_image(self, image_id: str) -> Optional[List[AugmentationStep]]:
        """Select a random combination of augmentations with combination coverage"""
        with self.lock:
            if self.is_complete():
                logging.info(f"Selection blocked: already generated {self.total_generated}/{self.target_images} images")
                return None
            
            if not self.config.augmentation_pool:
                logging.error("No augmentations available in pool")
                return None
            
            self._update_probabilities()
            
            max_possible = min(self.config.max_augmentations_per_image, len(self.config.augmentation_pool))
            min_required = min(self.config.min_augmentations_per_image, max_possible)
            
            if min_required > max_possible:
                logging.warning(f"min_augmentations_per_image ({self.config.min_augmentations_per_image}) > max possible ({max_possible}), adjusting")
                min_required = max_possible
            
            num_augmentations = min_required if min_required == max_possible else random.randint(min_required, max_possible)
            
            logging.debug(f"Selecting {num_augmentations} augmentations for image {image_id}")
            
            selected_augmentations = []
            available_augmentations = self.config.augmentation_pool.copy()
            attempt = 0
            
            # Fallback mechanism
            if len(self.image_augmentation_history[image_id]) >= self.max_attempts:
                logging.debug(f"Max attempts reached for image {image_id}, falling back to single augmentation")
                num_augmentations = 1
            
            while attempt < self.max_attempts:
                selected_augmentations = []
                available_augmentations = self.config.augmentation_pool.copy()
                
                for _ in range(num_augmentations):
                    if not available_augmentations:
                        break
                    
                    weights = [aug.dynamic_prob for aug in available_augmentations]
                    if all(w == 0 for w in weights):
                        logging.warning("All augmentation weights are zero, using uniform distribution")
                        weights = [1.0] * len(available_augmentations)
                    
                    selected_aug = random.choices(available_augmentations, weights=weights)[0]
                    selected_augmentations.append(selected_aug)
                    available_augmentations.remove(selected_aug)
                
                # Check if this combination is unique (ignore for random parameter augmentations)
                aug_combination = tuple(sorted([aug.name for aug in selected_augmentations]))
                if any(aug.is_random_params for aug in selected_augmentations) or \
                   aug_combination not in self.image_augmentation_history[image_id]:
                    for aug in selected_augmentations:
                        self.augmentation_usage[aug.name] += 1
                    
                    self.image_augmentation_history[image_id].add(aug_combination)
                    self.combination_usage[aug_combination] += 1
                    self.augmentation_history.append((image_id, aug_combination))
                    self.image_usage_count[image_id] += 1
                    
                    logging.debug(f"Selected augmentations for image {image_id}: {aug_combination}")
                    return selected_augmentations
                
                attempt += 1
                logging.debug(f"Combination {aug_combination} already used for image {image_id}, retrying ({attempt}/{self.max_attempts})")
            
            # Fallback to single augmentation if no valid combination found
            if available_augmentations:
                selected_aug = random.choice(available_augmentations)
                aug_combination = (selected_aug.name,)
                self.augmentation_usage[selected_aug.name] += 1
                self.image_augmentation_history[image_id].add(aug_combination)
                self.combination_usage[aug_combination] += 1
                self.augmentation_history.append((image_id, aug_combination))
                self.image_usage_count[image_id] += 1
                logging.debug(f"Fallback to single augmentation for image {image_id}: {selected_aug.name}")
                return [selected_aug]
            
            logging.debug(f"No augmentations available for image {image_id} after {self.max_attempts} attempts")
            return None
    
    def increment_generated_count(self):
        """Increment the count of generated images"""
        with self.lock:
            self.total_generated += 1
            logging.info(f"Generated images: {self.total_generated}/{self.target_images}")
            
            if self.total_generated > self.target_images:
                logging.warning(f"Generated count exceeded target: {self.total_generated}/{self.target_images}. Reverting increment.")
                self.total_generated -= 1
                return False
            
            if self.total_generated == self.target_images:
                logging.info(f"TARGET REACHED! Generated {self.total_generated} out of {self.target_images} images")
            
            return True
    
    def is_complete(self) -> bool:
        """Check if target number of images has been generated"""
        with self.lock:
            return self.total_generated >= self.target_images
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status and statistics"""
        with self.lock:
            return {
                'total_generated': self.total_generated,
                'target_images': self.target_images,
                'progress_percentage': (self.total_generated / self.target_images * 100) if self.target_images > 0 else 0,
                'augmentation_usage': dict(self.augmentation_usage),
                'combination_usage': dict(self.combination_usage),
                'current_probabilities': {aug.name: aug.dynamic_prob for aug in self.config.augmentation_pool},
                'is_complete': self.is_complete(),
                'recent_combinations': self.augmentation_history[-10:],
                'image_usage_counts': dict(self.image_usage_count)
            }
    
    def get_usage_distribution(self) -> Dict[str, float]:
        """Get the distribution of augmentation usage as percentages"""
        with self.lock:
            if not self.augmentation_usage:
                return {}
            
            total_usage = sum(self.augmentation_usage.values())
            return {
                name: (count / total_usage * 100) if total_usage > 0 else 0
                for name, count in self.augmentation_usage.items()
            }

class ImageDataItem:
    """Represents an image dataset item with all necessary metadata"""
    def __init__(self, json_data: Dict):
        self.json_data = json_data.copy()
        self.id = json_data.get('ID') or json_data.get('_id')
        self.dataset_id = json_data.get('DatasetID') or json_data.get('_idDataset')
        self.file_location = json_data.get('FileLocation') or json_data.get('fileLocation')
        self.file_name = json_data.get('FileName') or json_data.get('filename')
        self.height = json_data.get('Height') or json_data.get('height')
        self.width = json_data.get('Width') or json_data.get('width')
        self.area = json_data.get('Area') or json_data.get('area')
        self.version_info = json_data.get('versionInfo') or json_data.get('version_info', [])
        self.image = None
        self.augmented_image = None
        self.upload_url = None
        self.applied_chain_index = None
        self.applied_augmentations = []
    
    def get_bboxes(self, source_version) -> List[List[float]]:
        """Extract bounding boxes from version info"""
        bboxes = []
        for version in self.version_info:
            if version.get('version') == source_version:
                if version.get('annotation'):
                    for annotation in version['annotation']:
                        if annotation.get('bbox'):
                            bboxes.append(annotation['bbox'])
        
        bboxes = [[x, y, max(w, MIN_DIM), max(h, MIN_DIM)] 
                 for (x, y, w, h) in bboxes 
                 if w > 0 and h > 0]
        
        logging.debug(f'Extracted bounding boxes: {bboxes}')
        return bboxes
    
    def update_bboxes(self, new_bboxes: List[List[float]], source_version: str):
        """Update bounding boxes in version info"""
        bbox_index = 0
        for version in self.version_info:
            if version.get('version') == source_version:
                if version.get('annotation'):
                    for annotation in version['annotation']:
                        if annotation.get('bbox') and bbox_index < len(new_bboxes):
                            annotation['bbox'] = new_bboxes[bbox_index]
                            logging.debug(f"Updated bbox for version {version.get('version', 'unknown')}: {annotation['bbox']}")
                            bbox_index += 1
    
    def update_dimensions(self, new_height: int, new_width: int):
        """Update image dimensions"""
        self.json_data['height'] = new_height
        self.json_data['width'] = new_width
        self.json_data['area'] = float(new_height * new_width)
        self.height = new_height
        self.width = new_width
        self.area = float(new_height * new_width)
    
    def create_augmented_copy(self) -> 'ImageDataItem':
        """Create a new ImageDataItem for the augmented version"""
        new_data = self.json_data.copy()
        new_data['filename'] = f"aug_{self.file_name}"
        new_item = ImageDataItem(new_data)
        new_item.image = self.image
        new_item.augmented_image = self.augmented_image
        new_item.upload_url = self.upload_url
        new_item.applied_chain_index = self.applied_chain_index
        new_item.applied_augmentations = self.applied_augmentations
        logging.debug(f"augmented copy upload url: {new_item.upload_url}")
        logging.debug(f"augmented copy image shape: {new_item.augmented_image.shape if new_item.augmented_image is not None else 'None'}")
        logging.debug(f"augmented copy id: {new_item.id}")
        logging.debug(f"augmented copy file name: {new_item.file_name}")
        logging.debug(f"augmented copy file location: {new_item.file_location}")
        logging.debug(f"augmented copy dataset id: {new_item.dataset_id}")
        logging.debug(f"augmented copy applied chain index: {new_item.applied_chain_index}")
        logging.debug(f"augmented copy applied augmentations: {new_item.applied_augmentations}")
        return new_item
    
    def get_json_data(self) -> Dict:
        """Get the updated JSON data"""
        return self.json_data

def get_kafka_brokers():
    try:
        kafka_ip = "35.238.188.103"
        kafka_port = 9092
        kafka_brokers = f"{kafka_ip}:{kafka_port}"
        return kafka_brokers
    except Exception as e:
        logging.error(f"Error retrieving Kafka broker details: {e}")
        raise

def get_object_key_from_url(source_url: str) -> str:
    parsed_url = urlparse(source_url)
    if "amazonaws.com" in parsed_url.netloc:
        path_segments = parsed_url.path.strip('/').split('/')
        if len(path_segments) >= 3:
            return '/'.join(path_segments[1:])
        else:
            raise ValueError("Invalid AWS URL format")
    elif "storage.googleapis.com" in parsed_url.netloc:
        path_segments = parsed_url.path.strip('/').split('/')
        if len(path_segments) >= 1:
            return '/'.join(path_segments)
        else:
            raise ValueError("Invalid GCP URL format")
    else:
        raise ValueError(f"Unsupported URL format: {source_url}")

class PaginatedDataManager:
    """Manages paginated data requests and responses"""
    def __init__(self, 
                 request_topic: str,
                 response_topic: str,
                 bootstrap_servers: str,
                 consumer_group: str = 'augmentation_pipeline_consumer',
                 page_size: int = 100,
                 max_retries: int = 3,
                 retry_delay: int = 5):
        self.request_topic = request_topic
        self.response_topic = response_topic
        self.broker = bootstrap_servers
        self.consumer_group = consumer_group
        self.page_size = page_size
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.current_page = 0
        self.total_pages = None
        self.is_complete = False
        self.pending_requests = {}
        self.received_pages = {}
        self.lock = threading.Lock()
        
        self.producer = KafkaProducer(
            bootstrap_servers=[self.broker],
            value_serializer=lambda x: json.dumps(x).encode('utf-8'),
            max_block_ms=5000,
            retries=3
        )
    
        self.consumer = KafkaConsumer(
            bootstrap_servers=[self.broker],
            enable_auto_commit=True,
            auto_commit_interval_ms=1000,
            group_id=self.consumer_group,
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            consumer_timeout_ms=5000,
            session_timeout_ms=3000000,
            heartbeat_interval_ms=10000,
            max_poll_interval_ms=30000000,
            auto_offset_reset='latest',
            fetch_max_wait_ms=1000,
            request_timeout_ms=310000000,
            connections_max_idle_ms=320000000,
        )
        self.new_response_topic = TopicPartition(self.response_topic, partition=0)
        self.consumer.assign([self.new_response_topic])
    
    def request_page(self, page_number: int, dataset_id: str = None, augmentation_id: str = None, source_version: str = 'v1.0', **kwargs) -> bool:
        try:
            logging.debug(f"Requesting page {page_number} for dataset {dataset_id}")
            request_data = {
                'page_number': page_number,
                'page_size': self.page_size,
                'dataset_id': dataset_id,
                'timestamp': int(time.time()),
                'augmentation_id': augmentation_id,
                'version': source_version,
                **kwargs
            }
            with self.lock:
                self.pending_requests[page_number] = time.time()
            
            self.producer.send(self.request_topic, value=request_data)
            logging.debug(f"Requested page {page_number}")
            return True
        except Exception as e:
            logging.error(f"Error requesting page {page_number}: {e}")
            return False
    
    def check_for_responses(self, expected_augmentation_id: str = None) -> List[ImageDataItem]:
        items = []
        try:
            message_batch = self.consumer.poll(timeout_ms=100000)
            logging.debug(f"Polled {len(message_batch)} messages from Kafka")
            for topic_partition, messages in message_batch.items():
                for message in messages:
                    try:
                        response_data = message.value
                        if expected_augmentation_id and response_data.get('augmentation_id') != expected_augmentation_id:
                            continue
                        page_number = response_data.get('page')
                        page_data = response_data.get('items', [])
                        total_items = response_data.get('total')
                        total_pages = total_items // self.page_size
                        
                        if page_number is not None:
                            with self.lock:
                                if page_number in self.pending_requests:
                                    del self.pending_requests[page_number]
                                self.received_pages[page_number] = page_data
                                if total_pages is not None:
                                    self.total_pages = total_pages
                            
                            for item_data in page_data:
                                items.append(ImageDataItem(item_data))
                            
                            logging.debug(f"Received page {page_number} with {len(page_data)} items")
                    except Exception as e:
                        logging.error(f"Error processing response message: {e}")
        except Exception as e:
            logging.debug(f"No messages available or error polling: {e}")
        return items
    
    def is_pagination_complete(self) -> bool:
        with self.lock:
            return (len(self.received_pages) >= self.total_pages and 
                   len(self.pending_requests) == 0)

class UploadURLManager:
    """Manages upload URL requests and responses"""
    def __init__(self, 
                 request_topic: str,
                 response_topic: str,
                 bootstrap_servers: str,
                 consumer_group: str = 'upload_url_consumer'):
        self.request_topic = request_topic
        self.response_topic = response_topic
        self.consumer_group = consumer_group
        self.pending_requests = 0
        self.available_urls = []
        self.lock = threading.Lock()
        
        self.producer = KafkaProducer(
            bootstrap_servers=[bootstrap_servers],
            value_serializer=lambda x: json.dumps(x).encode('utf-8'),
            max_block_ms=5000,
            retries=3
        )
        
        self.consumer = KafkaConsumer(
            bootstrap_servers=[bootstrap_servers],
            enable_auto_commit=True,
            auto_commit_interval_ms=1000,
            group_id=self.consumer_group,
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            consumer_timeout_ms=5000,
            session_timeout_ms=3000000,
            heartbeat_interval_ms=10000,
            max_poll_interval_ms=30000000,
            auto_offset_reset='latest',
            fetch_max_wait_ms=1000,
            request_timeout_ms=310000000,
            connections_max_idle_ms=320000000,
        )
        self.new_response_topic = TopicPartition(self.response_topic, partition=0)
        self.consumer.assign([self.new_response_topic])
    
    def request_upload_url(self, dataset_id: str, augmentation_id: str = None) -> bool:
        try:
            self.augmentation_id = augmentation_id if augmentation_id else ''
            request_data = {
                'dataset_id': dataset_id,
                'augmentation_id': augmentation_id
            }
            with self.lock:
                self.pending_requests += 1
                
            future = self.producer.send(self.request_topic, value=request_data)
            future.get(timeout=10)
            logging.debug(f"Requested upload URL for dataset {dataset_id}")
            return True
        except Exception as e:
            logging.error(f"Error requesting upload URL for dataset {dataset_id}: {e}")
            with self.lock:
                self.pending_requests = max(0, self.pending_requests - 1)
            return False
    
    def get_upload_url(self, timeout_seconds: int = 60, expected_augmentation_id: str = None) -> Optional[str]:
        start_time = time.time()
        poll_attempts = 0
        max_poll_attempts = timeout_seconds // 5
        
        while time.time() - start_time < timeout_seconds and poll_attempts < max_poll_attempts:
            with self.lock:
                if self.available_urls:
                    url = self.available_urls.pop(0)
                    logging.debug(f"Retrieved upload URL from cache")
                    return url
            
            try:
                self._poll_for_responses(expected_augmentation_id=expected_augmentation_id)
                poll_attempts += 1
            except Exception as e:
                logging.warning(f"Error during polling attempt {poll_attempts}: {e}")
                time.sleep(1)
            
            time.sleep(0.5)
        
        logging.error(f"Timeout waiting for upload URL after {timeout_seconds} seconds and {poll_attempts} poll attempts")
        return None
    
    def _poll_for_responses(self, expected_augmentation_id: str = None):
        try:
            message_batch = self.consumer.poll(timeout_ms=100000)
            if not message_batch:
                logging.debug("No upload URL messages received in this poll")
                return
                
            messages_processed = 0
            for topic_partition, messages in message_batch.items():
                for message in messages:
                    try:
                        response_data = message.value
                        messages_processed += 1
                        if expected_augmentation_id and response_data.get('augmentation_id') != expected_augmentation_id:
                            logging.debug(f"Skipping response for augmentation ID {response_data.get('augmentation_id')}")
                            continue
                            
                        upload_url = response_data.get('uploadPath')
                        if upload_url:
                            with self.lock:
                                self.available_urls.append(upload_url)
                                self.pending_requests = max(0, self.pending_requests - 1)
                            logging.debug(f"Received and cached upload URL")
                        else:
                            logging.warning(f"Response missing uploadPath: {response_data}")
                    except Exception as e:
                        logging.error(f"Error processing upload URL response: {e}")
            if messages_processed > 0:
                logging.debug(f"Processed {messages_processed} upload URL messages")
        except Exception as e:
            if "timeout" not in str(e).lower():
                logging.warning(f"Error polling for upload URL responses: {e}")
    
    def has_pending_requests(self) -> bool:
        with self.lock:
            return self.pending_requests > 0
    
    def close(self):
        try:
            if hasattr(self, 'consumer'):
                self.consumer.close()
            if hasattr(self, 'producer'):
                self.producer.close()
        except Exception as e:
            logging.error(f"Error closing UploadURLManager: {e}")

class AugmentationStrategyFactory:
    """Factory class to create augmentation strategy instances"""
    STRATEGIES = {
        'blur': BlurAugmentation,
        'bit_depth_reduction': BitDepthReductionAugmentation,
        'brightness_contrast': BrightnessContrastAugmentation,
        'color_jitter': ColorJitterAugmentation,
        'compression_artifacts': CompressionArtifactsAugmentation,
        'downscale_upscale': DownscaleUpscaleAugmentation,
        'film_grain': FilmGrainAugmentation,
        'flip': HorizontalFlipAugmentation,
        'fog': FogAugmentation,
        'hsv': HueSaturationValueAugmentation,
        'iso_noise': ISONoiseAugmentation,
        'low_light': LowLightSimulationAugmentation,
        'posterize': PosterizeAugmentation,
        'rain': RainAugmentation,
        'random_affine': RandomAffineAugmentation,
        'salt_pepper': SaltAndPepperNoiseAugmentation,
        'shadows': ShadowAugmentation,
        'snow': SnowAugmentation,
        'speckle': SpeckleNoiseAugmentation,
        'sunflare': SunFlareAugmentation
    }
    
    @classmethod
    def create_strategy(cls, aug_step: AugmentationStep) -> ImageAugmentationStrategy:
        if aug_step.name not in cls.STRATEGIES:
            raise ValueError(f"Unknown augmentation strategy: {aug_step.name}")
        return cls.STRATEGIES[aug_step.name](**aug_step.params)

def parse_dynamic_pipeline_config(config_data: Dict, source_dataset_version: str = 'v1.0', target_dataset_version: str = 'v1.1') -> DynamicPipelineConfig:
    """Parse dynamic pipeline configuration from input data"""
    total_new_images = config_data.get('TotalNewImages', 0)
    augmentation_id = config_data.get('augmentationId', '')
    dataset_id = config_data.get('dataset_id', '')
    augmentation_pool = []
    aug_list = config_data.get('augmentationPool', [])
    
    for aug_data in aug_list:
        aug_name = list(aug_data.keys())[0]
        params = aug_data[aug_name].copy()
        if 'prob' in params:
            del params['prob']
        augmentation_pool.append(AugmentationStep(name=aug_name, params=params))
    
    return DynamicPipelineConfig(
        total_new_images=total_new_images,
        augmentation_pool=augmentation_pool,
        augmentation_id=augmentation_id,
        dataset_id=dataset_id,
        min_augmentations_per_image=config_data.get('minAugmentationsPerImage', 1),
        max_augmentations_per_image=config_data.get('maxAugmentationsPerImage', 3),
        source_version=source_dataset_version,
        target_version=target_dataset_version,
        prob_adjust_step=config_data.get('probAdjustStep', 0.05),
        prob_min=config_data.get('probMin', 0.1),
        prob_max=config_data.get('probMax', 0.9)
    )

def fetch_dataset_items_stage(dataset_item, pipeline_config, probability_manager, **kwargs):
    if probability_manager.is_complete():
        logging.info(f"Target reached ({probability_manager.total_generated}/{probability_manager.target_images}), skipping item {dataset_item.id}")
        return None
    
    try:
        logging.debug(f"Processing dataset item {dataset_item.id} for dynamic augmentation")
        selected_augmentations = probability_manager.select_augmentations_for_image(dataset_item.id)
        if selected_augmentations is None:
            logging.debug(f"No valid augmentations for item {dataset_item.id}, skipping")
            return None
        
        dataset_item.selected_augmentations = selected_augmentations
        logging.debug(f"Selected augmentations for item {dataset_item.id}: {[aug.name for aug in selected_augmentations]}")
        return dataset_item
    except Exception as e:
        logging.error(f"Error in fetch dataset items stage: {e}")
        return None

def download_images_stage(dataset_item, upload_url_manager, pipeline_config, probability_manager, **kwargs):
    if probability_manager.is_complete():
        logging.debug(f"Target reached ({probability_manager.total_generated}/{probability_manager.target_images}), skipping item {dataset_item.id}")
        return None
    
    try:
        logging.debug(f"Downloading image for item {dataset_item.id} from {dataset_item.file_location}")
        response = requests.get(dataset_item.file_location, timeout=30)
        response.raise_for_status()
        
        image_array = np.frombuffer(response.content, np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        
        if image is None:
            logging.error(f"Failed to decode image for item {dataset_item.id}")
            return None
        
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        dataset_item.image = image
        logging.debug(f"Downloaded image for item {dataset_item.id} with shape {image.shape}")
        upload_url_manager.request_upload_url(dataset_item.dataset_id, augmentation_id=pipeline_config.augmentation_id)
        return dataset_item
    except Exception as e:
        logging.error(f"Error downloading image: {e}")
        return None

def fetch_upload_urls_stage(dataset_item, pipeline_config, upload_url_manager, probability_manager, **kwargs):
    if probability_manager.is_complete():
        logging.info(f"Target reached ({probability_manager.total_generated}/{probability_manager.target_images}), skipping item {dataset_item.id}")
        return None
    
    try:
        upload_url = upload_url_manager.get_upload_url(timeout_seconds=10000, expected_augmentation_id=pipeline_config.augmentation_id)
        if upload_url is None:
            logging.error(f"Failed to get upload URL for item {dataset_item.id}")
            return None
        
        dataset_item.upload_url = upload_url
        logging.debug(f"Assigned upload URL to item {dataset_item.id}: {upload_url}")
        return dataset_item
    except Exception as e:
        logging.error(f"Error fetching upload URL: {e}")
        return None

def apply_augmentations_stage(dataset_item, pipeline_config, probability_manager, **kwargs):
    try:
        if probability_manager.is_complete():
            logging.info(f"Target reached ({probability_manager.total_generated}/{probability_manager.target_images}), skipping augmentation for item {dataset_item.id}")
            return None
        
        logging.debug(f"Applying dynamic augmentations for item {dataset_item.id}")
        if dataset_item.image is None:
            logging.error(f"No image found for dataset item {dataset_item.id}")
            return None
        
        selected_augmentations = getattr(dataset_item, 'selected_augmentations', [])
        if not selected_augmentations:
            logging.error(f"No selected augmentations found for item {dataset_item.id}")
            return None
        
        current_image = dataset_item.image.copy()
        current_bboxes = dataset_item.get_bboxes(pipeline_config.source_version)
        applied_augmentations = []
        
        for aug_step in selected_augmentations:
            try:
                strategy = AugmentationStrategyFactory.create_strategy(aug_step)
                augmented_image, new_height, new_width, new_bboxes = strategy.apply(
                    current_image, current_bboxes, bbox_format='coco'
                )
                logging.debug(f"Applied {aug_step.name} to item {dataset_item.id}")
                current_image = augmented_image
                current_bboxes = new_bboxes
                applied_augmentations.append(aug_step.name)
            except Exception as e:
                logging.error(f"Error applying augmentation {aug_step.name} to item {dataset_item.id}: {e}")
                continue
        
        try:
            augmented_item = dataset_item.create_augmented_copy()
            augmented_item.augmented_image = current_image
            augmented_item.applied_augmentations = applied_augmentations
            augmented_item.update_dimensions(current_image.shape[0], current_image.shape[1])
            augmented_item.update_bboxes(current_bboxes, pipeline_config.source_version)
            
            if not probability_manager.increment_generated_count():
                logging.warning(f"Item {dataset_item.id} discarded: target count already reached")
                return None
            
            logging.debug(f"Successfully applied {len(applied_augmentations)} augmentations to item {dataset_item.id}")
            return augmented_item
        except Exception as e:
            logging.error(f"Error creating augmented copy for item {dataset_item.id}: {e}")
            return None
    except Exception as e:
        logging.error(f"Error in dynamic augmentation stage: {e}")
        return None

def upload_and_publish_stage(dataset_item, new_items_producer, new_items_topic, pipeline_config, probability_manager, **kwargs):
    try:
        logging.debug(f"Uploading augmented image for item {dataset_item.id}")
        if dataset_item.augmented_image is None:
            logging.error(f"No augmented image found for dataset item {dataset_item.id}")
            return None
        
        image_bgr = cv2.cvtColor(dataset_item.augmented_image, cv2.COLOR_RGB2BGR)
        _, img_encoded = cv2.imencode('.jpg', image_bgr)
        img_bytes = img_encoded.tobytes()
        file_size_mb = len(img_bytes) / (1024 * 1024)
        
        upload_response = requests.put(
            dataset_item.upload_url,
            data=img_bytes,
            headers={'Content-Type': 'image/jpeg'},
            timeout=30
        )
        
        if upload_response.status_code in [200, 201, 204]:
            logging.debug(f"Uploaded augmented image for item {dataset_item.id}")
            full_url = dataset_item.upload_url.split('?')[0]
            s3_key = get_object_key_from_url(full_url)
            
            dataset_item.json_data['fileLocation'] = s3_key
            dataset_item.json_data['fileSize'] = file_size_mb
            dataset_item.json_data['Status'] = 'completed'
            dataset_item.json_data['_id'] = ""
            dataset_item.json_data['augmentationApplied'] = dataset_item.applied_augmentations
            dataset_item.json_data['versionInfo'] = [
                {**i, 'version': pipeline_config.target_version} 
                for i in dataset_item.json_data['versionInfo'] 
                if i.get('version') == pipeline_config.source_version
            ]
            dataset_item.json_data["_idAugmentedFrom"] = dataset_item.id
            dataset_item.json_data['_idAugmentation'] = pipeline_config.augmentation_id
            
            new_items_producer.send(new_items_topic, value=dataset_item.get_json_data())
            logging.debug(f"Published new dataset item to topic {new_items_topic}")
            return dataset_item
        else:
            logging.error(f"Failed to upload image for item {dataset_item.id}. Status: {upload_response.status_code}")
            dataset_item.json_data['Status'] = 'failed'
            dataset_item.json_data['UploadError'] = f'HTTP {upload_response.status_code}'
            return dataset_item
    except Exception as e:
        logging.error(f"Error in upload and publish stage: {e}")
        if dataset_item:
            dataset_item.json_data['Status'] = 'failed'
            dataset_item.json_data['UploadError'] = str(e)
            return dataset_item
        return None

def completion_monitor_stage(dataset_item, probability_manager, pipeline_config, **kwargs):
    try:
        logging.debug(f"Processed item {dataset_item.id}")
        status = probability_manager.get_status()
        
        if status['total_generated'] % 10 == 0 or probability_manager.is_complete():
            logging.info(f"Progress: {status['total_generated']}/{status['target_images']} "
                        f"({status['progress_percentage']:.1f}%)")
            usage_dist = probability_manager.get_usage_distribution()
            logging.info(f"Augmentation usage: {usage_dist}")
            logging.info(f"Combination coverage: {status['combination_usage']}")
        
        if probability_manager.is_complete():
            logging.info(f"All {pipeline_config.total_new_images} augmented images completed")
            final_status = probability_manager.get_status()
            logging.info("=== Final Augmentation Statistics ===")
            logging.info(f"Total generated: {final_status['total_generated']}")
            logging.info(f"Augmentation usage: {final_status['augmentation_usage']}")
            logging.info(f"Combination usage: {final_status['combination_usage']}")
            logging.info(f"Final probabilities: {final_status['current_probabilities']}")
            logging.info(f"Recent combinations: {final_status['recent_combinations']}")
        
        return dataset_item
    except Exception as e:
        logging.error(f"Error in completion monitor stage: {e}")
        return dataset_item

def create_probability_based_augmentation_pipeline(pipeline_config: DynamicPipelineConfig, kafka_config: Dict[str, Any]) -> Optional[Pipeline]:
    try:
        logging.info("Setting up dynamic augmentation pipeline")
        probability_manager = DynamicProbabilityDistributionManager(pipeline_config)
        
        dataset_items_queue = Queue(maxsize=1000)
        download_queue = Queue(maxsize=500)
        upload_url_queue = Queue(maxsize=500)
        augmentation_queue = Queue(maxsize=500)
        upload_queue = Queue(maxsize=500)
        output_queue = Queue(maxsize=1000)
        
        kafka_brokers = kafka_config.get('bootstrap_servers')
        
        data_manager = PaginatedDataManager(
            request_topic=kafka_config['dataset_request_topic'],
            response_topic=kafka_config['dataset_response_topic'],
            bootstrap_servers=kafka_brokers,
            consumer_group=f"augmentation_pipeline_{random.randint(1000, 9999)}",
            page_size=kafka_config.get('page_size', 100)
        )
        
        upload_url_manager = UploadURLManager(
            request_topic=kafka_config['upload_url_request_topic'],
            response_topic=kafka_config['upload_url_response_topic'],
            bootstrap_servers=kafka_config['bootstrap_servers'],
            consumer_group=f"augmentation2_pipeline_{random.randint(1000, 9999)}",
        )
        
        new_items_producer = KafkaProducer(
            bootstrap_servers=kafka_config['bootstrap_servers'],
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )
        
        def consume_dataset_items():
            logging.info("Starting dataset items consumer for dynamic pipeline")
            logging.info(f"Target images: {pipeline_config.total_new_images}")
            
            limited_page_size = min(kafka_config.get('page_size', 100), pipeline_config.total_new_images * 2)
            data_manager.page_size = limited_page_size
            
            data_manager.request_page(data_manager.current_page, 
                                    dataset_id=pipeline_config.dataset_id,
                                    augmentation_id=pipeline_config.augmentation_id,
                                    source_version=pipeline_config.source_version)
            
            available_items = []
            
            while not probability_manager.is_complete():
                try:
                    items = data_manager.check_for_responses(
                        expected_augmentation_id=pipeline_config.augmentation_id
                    )
                    available_items.extend(items)
                    for item in items:
                        probability_manager.add_available_image(item.id)
                    
                    while available_items and not probability_manager.is_complete():
                        selected_item = random.choice(available_items)
                        dataset_items_queue.put(selected_item)
                        logging.debug(f"Queued item {selected_item.id}")
                        probability_manager.add_available_image(selected_item.id)
                    
                    if not available_items and not probability_manager.is_complete():
                        if data_manager.total_pages is None or data_manager.current_page >= data_manager.total_pages:
                            logging.debug("Resetting to first page to fetch more items")
                            data_manager.current_page = 0
                            data_manager.received_pages.clear()
                        
                        next_page = data_manager.current_page
                        if next_page not in data_manager.pending_requests and next_page not in data_manager.received_pages:
                            data_manager.request_page(next_page, 
                                                    dataset_id=pipeline_config.dataset_id,
                                                    augmentation_id=pipeline_config.augmentation_id)
                            data_manager.current_page = next_page + 1
                    
                    time.sleep(0.1)
                except Exception as e:
                    logging.error(f"Error in dataset items consumer: {e}")
                    time.sleep(1)
            
            logging.info("Dataset items consumption complete. Signaling pipeline termination.")
            dataset_items_queue.put(None)
        
        pipeline = Pipeline()
        
        pipeline.add_producer(
            process_fn=consume_dataset_items,
            process_params={},
            partition_num=0
        )
        
        pipeline.add_stage(
            stage_name="Fetch Dataset Items",
            process_fn=fetch_dataset_items_stage,
            pull_queue=dataset_items_queue,
            push_queue=download_queue,
            process_params={
                'pipeline_config': pipeline_config,
                'probability_manager': probability_manager
            },
            num_threads=2
        )
        
        pipeline.add_stage(
            stage_name="Download Images",
            process_fn=download_images_stage,
            pull_queue=download_queue,
            push_queue=upload_url_queue,
            process_params={
                'upload_url_manager': upload_url_manager,
                'pipeline_config': pipeline_config,
                'probability_manager': probability_manager
            },
            num_threads=10
        )
        
        pipeline.add_stage(
            stage_name="Fetch Upload URLs",
            process_fn=fetch_upload_urls_stage,
            pull_queue=upload_url_queue,
            push_queue=augmentation_queue,
            process_params={
                'upload_url_manager': upload_url_manager,
                'pipeline_config': pipeline_config,
                'probability_manager': probability_manager
            },
            num_threads=5
        )
        
        pipeline.add_stage(
            stage_name="Apply Augmentations",
            process_fn=apply_augmentations_stage,
            pull_queue=augmentation_queue,
            push_queue=upload_queue,
            process_params={
                'pipeline_config': pipeline_config,
                'probability_manager': probability_manager
            },
            num_threads=8
        )
        
        pipeline.add_stage(
            stage_name="Upload and Publish",
            process_fn=upload_and_publish_stage,
            pull_queue=upload_queue,
            push_queue=output_queue,
            process_params={
                'new_items_producer': new_items_producer,
                'new_items_topic': kafka_config['new_items_topic'],
                'pipeline_config': pipeline_config,
                'probability_manager': probability_manager
            },
            num_threads=10
        )
        
        pipeline.add_stage(
            stage_name="Completion Monitor",
            process_fn=completion_monitor_stage,
            pull_queue=output_queue,
            process_params={
                'probability_manager': probability_manager,
                'pipeline_config': pipeline_config
            },
            num_threads=1,
            is_last_stage=True
        )
        
        logging.info("Dynamic augmentation pipeline configuration complete")
        return pipeline
    except Exception as e:
        logging.error(f"Error setting up dynamic augmentation pipeline: {e}")
        traceback.print_exc()
        raise