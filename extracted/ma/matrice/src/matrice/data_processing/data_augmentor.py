#!/usr/bin/env python3

import logging
import json
import sys
from typing import Dict, Any

# Import your pipeline modules
from .image_data_augmentation import (
    create_probability_based_augmentation_pipeline,
    parse_dynamic_pipeline_config,
    DynamicPipelineConfig,
    AugmentationStep,
)

def create_sample_pipeline_config() -> Dict[str, Any]:
    """Create a sample pipeline configuration for testing"""
    # return {
    #     "TotalNewImages": 6,
    #     "augmentationId": "test_aug_001",
    #     "dataset_id": "684916d765b796606a22fc89",
    #     "augChains": [
    #         # Chain 1: Blur + Brightness/Contrast (40 images)
    #         [
    #             [
    #                 {"blur": {"blur_limit": 7, "prob": 1.0}},
    #                 {"brightness_contrast": {"brightness_limit": 0.2, "contrast_limit": 0.2, "prob": 1.0}}
    #             ],
    #             1
    #         ],
    #         # Chain 2: Rotation + Color Jitter (30 images)
    #         [
    #             [
    #                 {"random_affine": {"shift_limit":0.0625, "scale_limit":0.1, "rotate_limit":15, "prob": 1.0}},
    #                 {"color_jitter": {"brightness": 0.2, "contrast": 0.2, "saturation": 0.2, "hue": 0.1, "prob": 1.0}}
    #             ],
    #             1
    #         ],
    #         # Chain 3: Flip + HSV (20 images)
    #         [
    #             [
    #                 {"flip": {"prob": 1.0}},
    #                 {"hsv": {"hue_shift_limit": 20, "sat_shift_limit": 30, "val_shift_limit": 20, "prob": 1.0}}
    #             ],
    #             1
    #         ],
    #         # Chain 4: Noise + Compression (10 images)
    #         [
    #             [
    #                 {"iso_noise": {"color_shift":(0.02, 0.03), "intensity": (0.2, 0.3), "prob": 1.0}},
    #             ],
    #             1
    #         ]
    #     ]
    # }
    
    config_data = [
        
        {
        "TotalNewImages": 15,
        "augmentationId": "aug_123",
        "dataset_id": "6800f1ab79ee9ad0a1bc8749",
        "minAugmentationsPerImage": 2,
        "maxAugmentationsPerImage": 6,
        "augmentationPool": [
            
                    {"blur": {"blur_limit": 7}},
                    {"brightness_contrast": {"brightness_limit": 0.2, "contrast_limit": 0.2}},
                    {"random_affine": {"shift_limit": 0.0625, "scale_limit": 0.1, "rotate_limit": 15}},
                    {"color_jitter": {"brightness": 0.2, "contrast": 0.2, "saturation": 0.2, "hue": 0.1}},
                    {"flip": {}},  # No parameters needed for flip
                    {"hsv": {"hue_shift_limit": 20, "sat_shift_limit": 30, "val_shift_limit": 20}}
            ]
        
    },
                   ]
    return config_data

def create_kafka_config() -> Dict[str, Any]:
    """Create Kafka configuration with hardcoded values"""
    return {
        # Kafka broker configuration
        "bootstrap_servers": ["35.238.188.103:9092"],
        
        "Kafka_ip": "",
        "Kafka_port": "",
        # Topics for dataset pagination
        "dataset_request_topic": "augmentation_dataset_item_request",
        "dataset_response_topic": "augmentation_dataset_item_response",
        
        # Topics for upload URL management
        "upload_url_request_topic": "augmentation_PreSignedURL_request",
        "upload_url_response_topic": "augmentation_PreSignedURL_response",
        
        # Topic for publishing new augmented dataset items
        "new_items_topic": "update_augmented_dataset_items",
        
        # Consumer groups
        "consumer_group": "augmentation_pipeline_consumer",
        "upload_url_consumer_group": "upload_url_consumer",
        
        # Pagination settings - conservative to prevent over-consumption
        "page_size": 5  # Small page size to prevent over-queuing
    }

def create_completion_api_config() -> str:
    """Create completion API URL configuration"""
    # Use environment variable if available, otherwise default to None to skip API calls
    import os
    return os.getenv('COMPLETION_API_URL', None)  # Returns None if not set, which will skip API calls
    
    

def initialize_and_run_pipeline():
    """Initialize and run the probability-based augmentation pipeline"""
    
    try:
        logging.info("=== Starting Probability-Based Augmentation Pipeline ===")
        
        # Create sample configuration
        config_data = create_sample_pipeline_config()
        logging.info(f"Created pipeline configuration: {json.dumps(config_data, indent=2)}")
        
        # Parse pipeline configuration
        pipeline_config = parse_dynamic_pipeline_config(config_data)
        logging.info(f"Parsed pipeline config - Total images: {pipeline_config.total_new_images}")
        logging.info(f"Augmentation ID: {pipeline_config.augmentation_id}")
        logging.info(f"Dataset ID: {pipeline_config.dataset_id}")
        # logging.info(f"Number of augmentation chains: {len(pipeline_config.augmentation_chains)}")
        
        # Log chain details
        # for i, chain in enumerate(pipeline_config.augmentation_chains):
        #     logging.info(f"Chain {i}: {len(chain.steps)} steps, target: {chain.target_count} images")
        #     for j, step in enumerate(chain.steps):
        #         logging.info(f"  Step {j}: {step.name} with params {step.params}")
        
        # Create Kafka configuration
        kafka_config = create_kafka_config()
        logging.info(f"Kafka configuration: {json.dumps(kafka_config, indent=2)}")
        
        # Completion API URL (configurable)
        completion_api_url = create_completion_api_config()
        if completion_api_url:
            logging.info(f"Using completion API URL: {completion_api_url}")
        else:
            logging.info("No completion API URL configured - will skip API calls")
        
        # Create the pipeline
        logging.info("Creating probability-based augmentation pipeline...")
        pipeline = create_probability_based_augmentation_pipeline(
            pipeline_config=pipeline_config,
            kafka_config=kafka_config,
            completion_api_url=completion_api_url
        )
        
        if pipeline is None:
            logging.error("Failed to create pipeline")
            return False
        
        logging.info("Pipeline created successfully!")
        logging.info("Pipeline stages:")
        for i, stage in enumerate(pipeline.stages):
            logging.info(f"  Stage {i}: {stage}")
        
        # Start the pipeline
        logging.info("Starting pipeline execution...")
        pipeline.start()
        
        logging.info("=== Pipeline execution completed successfully ===")
        return True
        
    except KeyboardInterrupt:
        logging.info("Pipeline execution interrupted by user")
        return False
    except Exception as e:
        logging.error(f"Error during pipeline execution: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_with_custom_config(config_file_path: str = None):
    """Run pipeline with custom configuration from file"""
    
    try:
        if config_file_path:
            logging.info(f"Loading configuration from: {config_file_path}")
            with open(config_file_path, 'r') as f:
                config_data = json.load(f)
        else:
            logging.info("Using default sample configuration")
            config_data = create_sample_pipeline_config()
        
        # Parse and run
        pipeline_config = parse_dynamic_pipeline_config(config_data)
        kafka_config = create_kafka_config()
        completion_api_url = create_completion_api_config()
        
        if completion_api_url:
            logging.info(f"Using completion API URL: {completion_api_url}")
        else:
            logging.info("No completion API URL configured - will skip API calls")
        
        # Create and start pipeline
        pipeline = create_probability_based_augmentation_pipeline(
            pipeline_config=pipeline_config,
            kafka_config=kafka_config,
            completion_api_url=completion_api_url
        )
        
        if pipeline:
            logging.info("Starting pipeline execution...")
            pipeline.start()
            logging.info("Pipeline execution completed successfully")
            return True
        else:
            logging.error("Failed to create pipeline")
            return False
            
    except Exception as e:
        logging.error(f"Error running pipeline with custom config: {e}")
        import traceback
        traceback.print_exc()
        return False

def transform_augmentation_data(input_dict):
    """
    Transform input augmentation dictionary into a list of output dictionaries,
    one for each augmentation chain.
    """
    def map_operation_to_pool_format(operation):
        """Convert operation format to augmentationPool format"""
        name = operation["Name"]
        params = operation.get("Params", {})
        return {name: params}

    def clean_augmentation_id(aug_id):
        """Clean ObjectID string to extract just the ID"""
        if isinstance(aug_id, str) and aug_id.startswith('ObjectID("') and aug_id.endswith('")'):
            return aug_id[10:-2]
        return aug_id

    result = []

    for chain in input_dict.get("augChains", []):
        augmentation_pool = [map_operation_to_pool_format(op) for op in chain.get("Operations", [])]

        result.append({
            "TotalNewImages": chain.get("NumImagesToGenerate", 0),
            "augmentationId": clean_augmentation_id(input_dict.get("augmentationID", "unknown")),
            "dataset_id": input_dict.get("dataset_id", ""),
            "minAugmentationsPerImage": 1,
            "maxAugmentationsPerImage": len(augmentation_pool),
            "augmentationPool": augmentation_pool
        })

    return result

        
class DataAugmentation:
    """Class to handle dataset preparation."""

    def __init__(self, session: Any, action_record_id: str):
        """Initialize DataAugmentation.

        Args:
            session: Session object with RPC client
            action_record_id: ID of action record
        """
        self.session = session
        self.rpc = session.rpc
        self.action_record_id = action_record_id

        # Updated to correctly parse nested "data"
        url = f"/v1/project/action/{self.action_record_id}/details"
        response = self.rpc.get(url)
        self.action_doc = response["data"]

        # Extract the appropriate fields from the nested structure
        self.action_type = self.action_doc.get("action")
        self.job_params = self.action_doc.get("jobParams", {})
        self.action_details = self.action_doc.get("actionDetails", {})

        logging.info(f"Job parameters: {self.job_params}")

        # Now extract nested fields correctly
        self.dataset_id = self.action_details.get("_idDataset")
        self.source_dataset_version = self.job_params.get("source_version", "")
        self.target_dataset_version = self.job_params.get("target_version", "")
        self.augmentations = self.job_params.get("augmentation_dict", {})

        # Transform using updated function
        self.formatted_augmentations = transform_augmentation_data(self.augmentations)

        self.kafka_config = self.job_params.get("kafka_config", {})
        # self.completion_api_url = self.job_params.get("completion_api_url", "")


    def update_status(
        self,
        stepCode: str,
        status: str,
        status_description: str,
    ) -> None:
        """Update status of data preparation.

        Args:
            stepCode: Code indicating current step
            status: Status of step
            status_description: Description of status
        """
        try:
            logging.info(status_description)
            url = "/v1/actions"
            payload = {
                "_id": self.action_record_id,
                "action": self.action_type,
                "serviceName": self.action_doc["serviceName"],
                "stepCode": stepCode,
                "status": status,
                "statusDescription": status_description,
            }
            self.rpc.put(path=url, payload=payload)
        except Exception as e:
            logging.error(
                "Exception in update_status: %s",
                str(e),
            )
            raise

    def start_processing(self) -> None:
        """Start dataset augmentation processing."""
        self.update_status(
            "DCKR_PROC",
            "OK",
            "Dataset started augmentation",
        )

        for chain in self.formatted_augmentations:
            try:
                logging.info(f"Processing augmentation chain: {json.dumps(chain, indent=2)}")
                
                self.pipeline_config = parse_dynamic_pipeline_config(
                    chain, self.source_dataset_version, self.target_dataset_version
                )
                logging.debug(f"Parsed pipeline config: {self.pipeline_config}")
                for attr, value in vars(self.pipeline_config).items():
                    logging.info(f"Pipeline Config Attribute - {attr}: {value}")
                
                self.pipeline = create_probability_based_augmentation_pipeline(
                    pipeline_config=self.pipeline_config,
                    kafka_config=self.kafka_config,
                )
                self.pipeline.start()
                self.pipeline.wait_to_finish_processing_and_stop()
                new_dataset_items = self.pipeline.get_all_items_from_last_stage()

                # Optional: Uncomment these if you want to preserve partition updates
                # update_partitions_numbers(
                #     self.rpc,
                #     self.dataset_id,
                #     new_dataset_items,
                #     partition_key="partitionNumber",
                # )

                # create_partition_stats(
                #     rpc=self.rpc,
                #     dataset_id=self.dataset_id,
                #     source_version=self.dataset_version,
                #     target_version=self.dataset_version,
                #     partition_stats=calculate_partition_stats(new_dataset_items),
                # )

                # batch_insert_dataset_items(
                #     new_dataset_items,
                #     self.dataset_id,
                #     self.rpc,
            except Exception as e:
                logging.error(f"Error processing augmentation chain: {e}")
                continue    # )

        try:
            completion_url = f"/v1/dataset_item/complete/{self.pipeline_config.augmentation_id}"
            logging.debug(f"Calling completion API at {completion_url}")
            response = self.rpc.post(path=completion_url, payload={})

            if response and response.get("success"):
                logging.info("Completion API called successfully")
            else:
                logging.warning(f"Completion API call returned status {response}")
        except Exception as e:
            logging.error(f"Error calling completion API: {e}")

              # Continue to next chain even if this one fails

        self.update_status(
            "SUCCESS",
            "SUCCESS",
            "Dataset Augmentation completed",
        )
