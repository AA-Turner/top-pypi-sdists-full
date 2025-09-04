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
import threading
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict
from urllib.parse import urlparse
from .pipeline import Pipeline
from typing import List, Dict, Optional
from kafka import KafkaProducer, KafkaConsumer
import torch
from PIL import Image
from transformers import AutoTokenizer, AutoModelForCausalLM
from diffusers import DiffusionPipeline
from diffusers.utils import load_image
from huggingface_hub import login
from matrice.utils import handle_response
from diffusers import AutoPipelineForImage2Image

MIN_DIM = 1.0

@dataclass
class PromptStep:
    """Represents a single prompt step"""
    prompt: str

@dataclass
class SyntheticPipelineConfig:
    """Configuration for synthetic generation pipeline"""
    total_new_images: int
    prompt_pool: List[str]
    generation_id: str
    dataset_id: str
    source_version: str = 'v1.0'
    target_version: str = 'v1.1'
    auto_generate_prompt: bool = False
    categories: List[str] = field(default_factory=list)

class PromptManager:
    """
    Manages prompt distribution for synthetic generation with global tracking
    """
    def __init__(self, config: SyntheticPipelineConfig):
        self.config = config
        self.lock = threading.RLock()
        self.total_generated = 0
        self.target_images = config.total_new_images
        self.prompt_usage = defaultdict(int)
        self.generation_history = []
        self.image_prompt_history = defaultdict(set)
        self.available_images = []
        self.image_usage_count = defaultdict(int)
        self.combination_usage = defaultdict(int)  # Track global combination usage
        self.max_attempts = self._calculate_max_attempts()
        
        if self.config.auto_generate_prompt:
            self._generate_prompts_with_model()
        
        logging.info(f"Initialized Prompt Manager for {self.target_images} images")
        logging.info(f"Available prompts: {[p.prompt for p in config.prompt_pool]}")
        logging.info(f"Calculated max attempts: {self.max_attempts}")
    
    def _calculate_max_attempts(self) -> int:
        """Calculate maximum retry attempts based on possible combinations"""
        return min(max(10, len(self.config.prompt_pool) // 10), 100)  # Cap between 10 and 100
    
    def _generate_prompts_with_model(self):
        """Generate prompts using Gemma model based on categories"""
        try:
            tokenizer = AutoTokenizer.from_pretrained("google/gemma-2-2b")
            model = AutoModelForCausalLM.from_pretrained("google/gemma-2-2b")
            if torch.cuda.is_available():
                model = model.to("cuda")
            
            meta_prompt = f"Generate {self.target_images} unique image editing prompts for synthetic data generation based on these categories: {', '.join(self.config.categories)}. Each prompt should be on a separate line."
            inputs = tokenizer(meta_prompt, return_tensors="pt").to(model.device)
            outputs = model.generate(**inputs, max_new_tokens=2000, do_sample=True, temperature=0.7)
            text = tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            generated_prompts = [line.strip() for line in text.split("\n") if line.strip() and not line.startswith("Generate")]
            
            if len(generated_prompts) < self.target_images:
                logging.warning(f"Generated {len(generated_prompts)} prompts, repeating to reach {self.target_images}")
                repeats = (self.target_images // len(generated_prompts)) + 1
                generated_prompts *= repeats
                generated_prompts = generated_prompts[:self.target_images]
            
            self.config.prompt_pool = [PromptStep(p) for p in generated_prompts]
            logging.info(f"Generated {len(self.config.prompt_pool)} prompts using Gemma model")
        except Exception as e:
            logging.error(f"Error generating prompts with model: {e}")
            raise
    
    def add_available_image(self, image_id: str):
        """Add an image ID to the pool of available images"""
        with self.lock:
            self.available_images.append(image_id)
            logging.debug(f"Added image {image_id} to available pool. Total available: {len(self.available_images)}")
    
    def select_prompt_for_image(self, image_id: str) -> Optional[List[PromptStep]]:
        """Select a prompt for the image with coverage"""
        with self.lock:
            if self.is_complete():
                logging.info(f"Selection blocked: already generated {self.total_generated}/{self.target_images} images")
                return None
            
            if not self.config.prompt_pool:
                logging.error("No prompts available in pool")
                return None
            
            num_prompts = 1
            
            logging.debug(f"Selecting {num_prompts} prompt for image {image_id}")
            
            selected_prompts = []
            available_prompts = self.config.prompt_pool.copy()
            attempt = 0
            
            if len(self.image_prompt_history[image_id]) >= self.max_attempts:
                logging.debug(f"Max attempts reached for image {image_id}, falling back to single prompt")
                num_prompts = 1
            
            while attempt < self.max_attempts:
                selected_prompts = []
                
                for _ in range(num_prompts):
                    if not available_prompts:
                        break
                    
                    selected_step = random.choice(available_prompts)
                    selected_prompts.append(selected_step)
                    available_prompts.remove(selected_step)
                
                # Check if this combination is unique
                prompt_combination = tuple(sorted([step.prompt for step in selected_prompts]))
                if prompt_combination not in self.image_prompt_history[image_id]:
                    for step in selected_prompts:
                        self.prompt_usage[step.prompt] += 1
                    
                    self.image_prompt_history[image_id].add(prompt_combination)
                    self.combination_usage[prompt_combination] += 1
                    self.generation_history.append((image_id, prompt_combination))
                    self.image_usage_count[image_id] += 1
                    
                    logging.debug(f"Selected prompt for image {image_id}: {prompt_combination}")
                    return selected_prompts
                
                attempt += 1
                logging.debug(f"Combination {prompt_combination} already used for image {image_id}, retrying ({attempt}/{self.max_attempts})")
            
            # Fallback to single prompt if no valid combination found
            if self.config.prompt_pool:
                selected_step = random.choice(self.config.prompt_pool)
                prompt_combination = (selected_step.prompt,)
                self.prompt_usage[selected_step.prompt] += 1
                self.image_prompt_history[image_id].add(prompt_combination)
                self.combination_usage[prompt_combination] += 1
                self.generation_history.append((image_id, prompt_combination))
                self.image_usage_count[image_id] += 1
                logging.debug(f"Fallback to single prompt for image {image_id}: {selected_step.prompt}")
                return [selected_step]
            
            logging.debug(f"No prompts available for image {image_id} after {self.max_attempts} attempts")
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
                'prompt_usage': dict(self.prompt_usage),
                'combination_usage': dict(self.combination_usage),
                'is_complete': self.is_complete(),
                'recent_combinations': self.generation_history[-10:],
                'image_usage_counts': dict(self.image_usage_count)
            }
    
    def get_usage_distribution(self) -> Dict[str, float]:
        """Get the distribution of prompt usage as percentages"""
        with self.lock:
            if not self.prompt_usage:
                return {}
            
            total_usage = sum(self.prompt_usage.values())
            return {
                name: (count / total_usage * 100) if total_usage > 0 else 0
                for name, count in self.prompt_usage.items()
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
        self.applied_prompt = None
    
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
    
    def create_generated_copy(self) -> 'ImageDataItem':
        """Create a new ImageDataItem for the generated version"""
        new_data = self.json_data.copy()
        new_data['filename'] = f"syn_{self.file_name}"
        new_item = ImageDataItem(new_data)
        new_item.image = self.image
        new_item.augmented_image = self.augmented_image
        new_item.upload_url = self.upload_url
        new_item.applied_prompt = self.applied_prompt
        logging.info(f"Generated copy upload url: {new_item.upload_url}")
        logging.info(f"Generated copy image shape: {new_item.augmented_image.shape if new_item.augmented_image is not None else 'None'}")
        logging.info(f"Generated copy id: {new_item.id}")
        logging.info(f"Generated copy file name: {new_item.file_name}")
        logging.info(f"Generated copy file location: {new_item.file_location}")
        logging.info(f"Generated copy dataset id: {new_item.dataset_id}")
        logging.info(f"Generated copy applied prompt: {new_item.applied_prompt}")
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
                 consumer_group: str = 'synthetic_pipeline_consumer',
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
    
    def request_page(self, page_number: int, dataset_id: str = None, generation_id: str = None, source_version: str = 'v1.0', **kwargs) -> bool:
        try:
            logging.info(f"Requesting page {page_number} for dataset {dataset_id}")
            request_data = {
                'page_number': page_number,
                'page_size': self.page_size,
                'dataset_id': dataset_id,
                'timestamp': int(time.time()),
                'synthetic_data_generation_id': generation_id,
                'version': source_version,
                **kwargs
            }
            with self.lock:
                self.pending_requests[page_number] = time.time()
            
            self.producer.send(self.request_topic, value=request_data)
            logging.info(f"Requested page {page_number}")
            return True
        except Exception as e:
            logging.error(f"Error requesting page {page_number}: {e}")
            return False
    
    def check_for_responses(self, expected_generation_id: str = None) -> List[ImageDataItem]:
        items = []
        try:
            message_batch = self.consumer.poll(timeout_ms=100000)
            logging.info(f"Polled {len(message_batch)} messages from Kafka")
            for topic_partition, messages in message_batch.items():
                for message in messages:
                    try:
                        response_data = message.value
                        logging.info(f"Checking against {response_data.get('synthetic_data_generation_id')}")
                        if expected_generation_id and response_data.get('synthetic_data_generation_id') != expected_generation_id:
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
                            
                            logging.info(f"Received page {page_number} with {len(page_data)} items")
                    except Exception as e:
                        logging.error(f"Error processing response message: {e}")
        except Exception as e:
            logging.info(f"No messages available or error polling: {e}")
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
    
    def request_upload_url(self, dataset_id: str, generation_id: str = None) -> bool:
        try:
            self.generation_id = generation_id if generation_id else ''
            request_data = {
                'dataset_id': dataset_id,
                'synthetic_data_generation_id': generation_id
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
    
    def get_upload_url(self, timeout_seconds: int = 60, expected_generation_id: str = None) -> Optional[str]:
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
                self._poll_for_responses(expected_generation_id=expected_generation_id)
                poll_attempts += 1
            except Exception as e:
                logging.warning(f"Error during polling attempt {poll_attempts}: {e}")
                time.sleep(1)
            
            time.sleep(0.5)
        
        logging.error(f"Timeout waiting for upload URL after {timeout_seconds} seconds and {poll_attempts} poll attempts")
        return None
    
    def _poll_for_responses(self, expected_generation_id: str = None):
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
                        if expected_generation_id and response_data.get('synthetic_data_generation_id') != expected_generation_id:
                            logging.debug(f"Skipping response for generation ID {response_data.get('generation_id')}")
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

def parse_synthetic_pipeline_config(config_data: Dict, source_dataset_version: str = 'v1.0', target_dataset_version: str = 'v1.1') -> SyntheticPipelineConfig:
    """Parse synthetic pipeline configuration from input data"""
    total_new_images = config_data.get('TotalNewImages', 0)
    generation_id = config_data.get('generationId', '')
    dataset_id = config_data.get('dataset_id', '')
    prompt_pool = []
    prompt_lists = config_data.get('prompts', [])  # list of lists, each with 1 prompt
    for p in prompt_lists:
        if p:
            prompt_pool.append(PromptStep(prompt=p))
    
    return SyntheticPipelineConfig(
        total_new_images=total_new_images,
        prompt_pool=prompt_pool,
        generation_id=generation_id,
        dataset_id=dataset_id,
        source_version=source_dataset_version,
        target_version=target_dataset_version,
        auto_generate_prompt=config_data.get('autoGeneratePrompt', False),
        categories=config_data.get('categories', [])
    )

def fetch_dataset_items_stage(dataset_item, pipeline_config, prompt_manager, **kwargs):
    if prompt_manager.is_complete():
        logging.info(f"Target reached ({prompt_manager.total_generated}/{prompt_manager.target_images}), skipping item {dataset_item.id}")
        return None
    
    try:
        logging.debug(f"Processing dataset item {dataset_item.id} for synthetic generation")
        selected_prompts = prompt_manager.select_prompt_for_image(dataset_item.id)
        if selected_prompts is None:
            logging.debug(f"No valid prompt for item {dataset_item.id}, skipping")
            return None
        
        dataset_item.selected_prompts = selected_prompts
        logging.debug(f"Selected prompts for item {dataset_item.id}: {[p.prompt for p in selected_prompts]}")
        return dataset_item
    except Exception as e:
        logging.error(f"Error in fetch dataset items stage: {e}")
        return None

def download_images_stage(dataset_item, upload_url_manager, pipeline_config, prompt_manager, **kwargs):
    if prompt_manager.is_complete():
        logging.debug(f"Target reached ({prompt_manager.total_generated}/{prompt_manager.target_images}), skipping item {dataset_item.id}")
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
        
        return dataset_item
    except Exception as e:
        logging.error(f"Error downloading image: {e}")
        return None

def fetch_upload_urls_stage(dataset_item, pipeline_config, upload_url_manager, prompt_manager, **kwargs):
    if prompt_manager.is_complete():
        logging.info(f"Target reached ({prompt_manager.total_generated}/{prompt_manager.target_images}), skipping item {dataset_item.id}")
        return None
    
    try:
        upload_url_manager.request_upload_url(dataset_item.dataset_id, generation_id=pipeline_config.generation_id)
        
        upload_url = upload_url_manager.get_upload_url(timeout_seconds=10000, expected_generation_id=pipeline_config.generation_id)
        if upload_url is None:
            logging.error(f"Failed to get upload URL for item {dataset_item.id}")
            return None
        
        dataset_item.upload_url = upload_url
        logging.info(f"Assigned presigned upload URL for item {dataset_item.id}: {upload_url}")
        return dataset_item
    except Exception as e:
        logging.error(f"Error fetching upload URL: {e}")
        return None

def apply_synthetic_generation_stage(dataset_item, pipeline_config, prompt_manager, pipe, **kwargs):
    try:
        if prompt_manager.is_complete():
            logging.info(f"Target reached ({prompt_manager.total_generated}/{prompt_manager.target_images}), skipping generation for item {dataset_item.id}")
            return None
        
        logging.debug(f"Applying synthetic generation for item {dataset_item.id}")
        if dataset_item.image is None:
            logging.error(f"No image found for dataset item {dataset_item.id}")
            return None
        
        selected_prompts = getattr(dataset_item, 'selected_prompts', [])
        if not selected_prompts:
            logging.error(f"No selected prompts found for item {dataset_item.id}")
            return None
        
        # Since num=1, take the first (only) prompt
        prompt = selected_prompts[0].prompt
        
        current_image = dataset_item.image.copy()
        
        # Convert NumPy array (RGB) to PIL Image
        input_image = Image.fromarray(current_image)  # Directly convert NumPy array to PIL Image
        
        # Generate new image using diffusion model
        generated_image = pipe(image=input_image, prompt=prompt, guidance_scale=10.0, strength=0.4, num_inference_steps=50).images[0]
        augmented_image_np = np.array(generated_image)  # Convert PIL Image back to NumPy array
        augmented_image_np = cv2.cvtColor(augmented_image_np, cv2.COLOR_RGB2BGR)  # Adjust if needed
        
        try:
            generated_item = dataset_item.create_generated_copy()
            generated_item.augmented_image = augmented_image_np
            generated_item.applied_prompt = prompt
            generated_item.update_dimensions(augmented_image_np.shape[0], augmented_image_np.shape[1])
            
            if not prompt_manager.increment_generated_count():
                logging.warning(f"Item {dataset_item.id} discarded: target count already reached")
                return None
            
            logging.debug(f"Successfully applied prompt '{prompt}' to item {dataset_item.id}")
            return generated_item
        except Exception as e:
            logging.error(f"Error creating generated copy for item {dataset_item.id}: {e}")
            return None
    except Exception as e:
        logging.error(f"Error in synthetic generation stage: {e}")
        return None

def upload_and_publish_stage(dataset_item, new_items_producer, new_items_topic, pipeline_config, prompt_manager, **kwargs):
    try:
        logging.debug(f"Uploading generated image for item {dataset_item.id}")
        if dataset_item.augmented_image is None:
            logging.error(f"No generated image found for dataset item {dataset_item.id}")
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
            logging.debug(f"Uploaded generated image for item {dataset_item.id}")
            full_url = dataset_item.upload_url.split('?')[0]
            s3_key = get_object_key_from_url(full_url)
            
            dataset_item.json_data['fileLocation'] = s3_key
            dataset_item.json_data['fileSize'] = file_size_mb
            dataset_item.json_data['Status'] = 'completed'
            dataset_item.json_data['_id'] = ""
            dataset_item.json_data['promptApplied'] = dataset_item.applied_prompt
            dataset_item.json_data['versionInfo'] = [
                {**i, 'version': pipeline_config.target_version} 
                for i in dataset_item.json_data['versionInfo'] 
                if i.get('version') == pipeline_config.source_version
            ]
            dataset_item.json_data["_idGeneratedFrom"] = dataset_item.id
            dataset_item.json_data['_idGeneration'] = pipeline_config.generation_id
            
            # Log new dataset item details before sending to Kafka
            logging.info(f"New dataset item details for Kafka: {json.dumps(dataset_item.get_json_data(), indent=2)}")
            
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

def completion_monitor_stage(dataset_item, prompt_manager, pipeline_config, **kwargs):
    try:
        logging.debug(f"Processed item {dataset_item.id}")
        status = prompt_manager.get_status()
        
        if status['total_generated'] % 10 == 0 or prompt_manager.is_complete():
            logging.info(f"Progress: {status['total_generated']}/{status['target_images']} "
                        f"({status['progress_percentage']:.1f}%)")
            usage_dist = prompt_manager.get_usage_distribution()
            logging.info(f"Prompt usage: {usage_dist}")
            logging.info(f"Combination coverage: {status['combination_usage']}")
        
        if prompt_manager.is_complete():
            logging.info(f"All {pipeline_config.total_new_images} generated images completed")
            final_status = prompt_manager.get_status()
            logging.info("=== Final Generation Statistics ===")
            logging.info(f"Total generated: {final_status['total_generated']}")
            logging.info(f"Prompt usage: {final_status['prompt_usage']}")
            logging.info(f"Combination usage: {final_status['combination_usage']}")
            logging.info(f"Recent combinations: {final_status['recent_combinations']}")
        
        return dataset_item
    except Exception as e:
        logging.error(f"Error in completion monitor stage: {e}")
        return dataset_item
    
def get_model_secret_keys(rpc, secret_name):
        """Get model secret keys.

        Args:
            secret_name: Name of the secret

        Returns:
            Tuple of (data, error, message) from API response
        """
        path = f"/v1/scaling/get_models_secret_keys?secret_name={secret_name}"
        resp = rpc.get(path=path)
        return handle_response(
            resp,
            "Secret keys fetched successfully",
            "Could not fetch the secret keys",
        )

def get_hugging_face_token_for_data_generation(rpc):
        """Retrieve Hugging Face token for data generation."""
        secret_name = "hugging_face"
        resp, error, message = get_model_secret_keys(rpc, secret_name)
        if error is not None:
            logging.error("Error getting Hugging Face token: %s", message)
            raise RuntimeError(f"Failed to retrieve Hugging Face token: {message}")
        else:
            hugging_face_token = resp["user_access_token"]
            return hugging_face_token

def create_synthetic_generation_pipeline(pipeline_config: SyntheticPipelineConfig, kafka_config: Dict[str, Any], rpc: callable) -> Optional[Pipeline]:
    try:
        logging.info("Setting up synthetic generation pipeline")
        prompt_manager = PromptManager(pipeline_config)
        try:
            hf_token = get_hugging_face_token_for_data_generation(rpc)
            logging.info(f"retrieved Hugging Face token: {hf_token}")
            login(token=hf_token)
            logging.info("Successfully logged in to Hugging Face with token")
        except Exception as e:
            logging.error(f"Failed to log in to Hugging Face: {e}")
            raise RuntimeError(f"Failed to authenticate with Hugging Face: {str(e)}")
        # Load diffusion model
        
        model_id = "kandinsky-community/kandinsky-2-2-decoder"
        try:
            pipe = AutoPipelineForImage2Image.from_pretrained(
                model_id, torch_dtype=torch.float16, use_safetensors=True
            )
            pipe.enable_xformers_memory_efficient_attention()
            logging.info("Stable Diffusion pipeline initialized successfully")
        except Exception as e:
            logging.error(f"Failed to initialize Stable Diffusion pipeline: {e}")
            raise
        
        if torch.cuda.is_available():
            pipe = pipe.to("cuda")
        else:
            pipe.enable_model_cpu_offload()
        
        dataset_items_queue = Queue(maxsize=1000)
        download_queue = Queue(maxsize=500)
        upload_url_queue = Queue(maxsize=500)
        generation_queue = Queue(maxsize=500)
        upload_queue = Queue(maxsize=500)
        output_queue = Queue(maxsize=1000)
        
        kafka_brokers = kafka_config.get('bootstrap_servers')
        
        data_manager = PaginatedDataManager(
            request_topic=kafka_config['dataset_request_topic'],
            response_topic=kafka_config['dataset_response_topic'],
            bootstrap_servers=kafka_brokers,
            consumer_group=f"synthetic_pipeline_{random.randint(1000, 9999)}",
            page_size=kafka_config.get('page_size', 100)
        )
        
        upload_url_manager = UploadURLManager(
            request_topic=kafka_config['upload_url_request_topic'],
            response_topic=kafka_config['upload_url_response_topic'],
            bootstrap_servers=kafka_config['bootstrap_servers'],
            consumer_group=f"synthetic_pipeline_{random.randint(1000, 9999)}",
        )
        
        new_items_producer = KafkaProducer(
            bootstrap_servers=kafka_config['bootstrap_servers'],
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )
        
        def consume_dataset_items():
            logging.info("Starting dataset items consumer for synthetic pipeline")
            logging.info(f"Target images: {pipeline_config.total_new_images}")
            
            limited_page_size = min(kafka_config.get('page_size', 100), pipeline_config.total_new_images * 2)
            data_manager.page_size = limited_page_size
            
            data_manager.request_page(page_number=data_manager.current_page, 
                                    dataset_id=pipeline_config.dataset_id,
                                    generation_id=pipeline_config.generation_id,
                                    source_version=pipeline_config.source_version)
            
            available_items = []
            queued_count = 0
            target_queue_size = pipeline_config.total_new_images * 3
            
            logging.info(f'Prompt manager status: {prompt_manager.is_complete()}')
            while not prompt_manager.is_complete():
                try:
                    logging.info(f"expected generation id: {pipeline_config.generation_id}")
                    items = data_manager.check_for_responses(
                        expected_generation_id=pipeline_config.generation_id
                    )
                    available_items.extend(items)
                    for item in items:
                        prompt_manager.add_available_image(item.id)
                    
                    while (available_items and 
                        not prompt_manager.is_complete() and 
                        queued_count < target_queue_size):
                        
                        selected_item = random.choice(available_items)
                        available_items.remove(selected_item)
                        dataset_items_queue.put(selected_item)
                        queued_count += 1
                        logging.info(f"Queued item {selected_item.id} ({queued_count}/{target_queue_size})")
                        prompt_manager.add_available_image(selected_item.id)
                    
                    if (not available_items and 
                        not prompt_manager.is_complete() and 
                        queued_count < target_queue_size):
                        
                        if data_manager.total_pages is None or data_manager.current_page >= data_manager.total_pages:
                            logging.info("Resetting to first page to fetch more items")
                            data_manager.current_page = 0
                            data_manager.received_pages.clear()
                        
                        next_page = data_manager.current_page
                        if next_page not in data_manager.pending_requests and next_page not in data_manager.received_pages:
                            data_manager.request_page(next_page, 
                                                    dataset_id=pipeline_config.dataset_id,
                                                    generation_id=pipeline_config.generation_id)
                            data_manager.current_page = next_page + 1
                    
                    time.sleep(0.1)
                except Exception as e:
                    logging.error(f"Error in dataset items consumer: {e}")
                    time.sleep(1)
            
            logging.info(f"Dataset items consumption complete. Queued {queued_count} items total.")
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
                'prompt_manager': prompt_manager
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
                'prompt_manager': prompt_manager
            },
            num_threads=10
        )
        
        pipeline.add_stage(
            stage_name="Fetch Upload URLs",
            process_fn=fetch_upload_urls_stage,
            pull_queue=upload_url_queue,
            push_queue=generation_queue,
            process_params={
                'upload_url_manager': upload_url_manager,
                'pipeline_config': pipeline_config,
                'prompt_manager': prompt_manager
            },
            num_threads=5
        )
        
        pipeline.add_stage(
            stage_name="Apply Synthetic Generation",
            process_fn=apply_synthetic_generation_stage,
            pull_queue=generation_queue,
            push_queue=upload_queue,
            process_params={
                'pipeline_config': pipeline_config,
                'prompt_manager': prompt_manager,
                'pipe': pipe
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
                'prompt_manager': prompt_manager
            },
            num_threads=10
        )
        
        pipeline.add_stage(
            stage_name="Completion Monitor",
            process_fn=completion_monitor_stage,
            pull_queue=output_queue,
            process_params={
                'prompt_manager': prompt_manager,
                'pipeline_config': pipeline_config
            },
            num_threads=1,
            is_last_stage=True
        )
        
        logging.info("Synthetic generation pipeline configuration complete")
        return pipeline
    except Exception as e:
        logging.error(f"Error setting up synthetic generation pipeline: {e}")
        traceback.print_exc()
        raise