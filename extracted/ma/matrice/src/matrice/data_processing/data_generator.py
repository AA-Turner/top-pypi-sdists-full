import logging
import json
import sys
from typing import Dict, Any

# Import your pipeline modules
from .data_generation import (
    create_synthetic_generation_pipeline,
    parse_synthetic_pipeline_config,
    SyntheticPipelineConfig,
    PromptStep,
)

def create_sample_pipeline_config() -> Dict[str, Any]:
    """Create a sample pipeline configuration for testing"""
    config_data = {
        "TotalNewImages": 15,
        "generationId": "gen_123",
        "dataset_id": "6800f1ab79ee9ad0a1bc8749",
        "prompts": [
            ["A futuristic cityscape at sunset"],
            ["A serene beach with palm trees"],
            ["A medieval castle under moonlight"],
            ["A dense forest with glowing fireflies"],
            ["A vibrant marketplace in an ancient town"],
            ["A snowy mountain peak at dawn"],
            ["A desert oasis with a clear blue spring"],
            ["A bustling urban street with neon lights"],
            ["A tranquil lake surrounded by mountains"],
            ["A gothic cathedral in the rain"],
            ["A tropical jungle with colorful birds"],
            ["A quiet countryside with rolling hills"],
            ["A futuristic robot in a high-tech lab"],
            ["A vintage car on a coastal road"],
            ["A starry night sky over a desert"]
        ],
        "autoGeneratePrompt": False,
        "categories": ["nature", "urban", "historical", "futuristic"]
    }
    return config_data

def create_kafka_config() -> Dict[str, Any]:
    """Create Kafka configuration with hardcoded values"""
    return {
        # Kafka broker configuration
        "bootstrap_servers": ["35.238.188.103:9092"],
        "Kafka_ip": "",
        "Kafka_port": "",
        # Topics for dataset pagination
        "dataset_request_topic": "synthetic_dataset_item_request",
        "dataset_response_topic": "synthetic_dataset_item_response",
        # Topics for upload URL management
        "upload_url_request_topic": "synthetic_PreSignedURL_request",
        "upload_url_response_topic": "synthetic_PreSignedURL_response",
        # Topic for publishing new generated dataset items
        "new_items_topic": "update_synthetic_dataset_items",
        # Consumer groups
        "consumer_group": "synthetic_pipeline_consumer",
        "upload_url_consumer_group": "upload_url_consumer",
        # Pagination settings - conservative to prevent over-consumption
        "page_size": 5  # Small page size to prevent over-queuing
    }

def create_completion_api_config() -> str:
    """Create completion API URL configuration"""
    import os
    return os.getenv('COMPLETION_API_URL', None)  # Returns None if not set, which will skip API calls

def initialize_and_run_pipeline():
    """Initialize and run the synthetic generation pipeline"""
    try:
        logging.info("=== Starting Synthetic Generation Pipeline ===")
        
        # Create sample configuration
        config_data = create_sample_pipeline_config()
        logging.info(f"Created pipeline configuration: {json.dumps(config_data, indent=2)}")
        
        # Parse pipeline configuration
        pipeline_config = parse_synthetic_pipeline_config(config_data)
        logging.info(f"Parsed pipeline config - Total images: {pipeline_config.total_new_images}")
        logging.info(f"Generation ID: {pipeline_config.generation_id}")
        logging.info(f"Dataset ID: {pipeline_config.dataset_id}")
        
        # Log prompt details
        logging.info(f"Number of prompts: {len(pipeline_config.prompt_pool)}")
        for i, prompt in enumerate(pipeline_config.prompt_pool):
            logging.info(f"  Prompt {i}: {prompt.prompt}")
        
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
        logging.info("Creating synthetic generation pipeline...")
        pipeline = create_synthetic_generation_pipeline(
            pipeline_config=pipeline_config,
            kafka_config=kafka_config,
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
        pipeline_config = parse_synthetic_pipeline_config(config_data)
        kafka_config = create_kafka_config()
        completion_api_url = create_completion_api_config()
        
        if completion_api_url:
            logging.info(f"Using completion API URL: {completion_api_url}")
        else:
            logging.info("No completion API URL configured - will skip API calls")
        
        # Create and start pipeline
        pipeline = create_synthetic_generation_pipeline(
            pipeline_config=pipeline_config,
            kafka_config=kafka_config
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

def transform_synthetic_data(input_dict):
    """
    Transform input synthetic dictionary into the expected configuration format
    """

    result = {
        "TotalNewImages": input_dict.get("TotalNewImages", 0),
        "generationId": input_dict.get("_idDataGeneration", "unknown"),
        "dataset_id": input_dict.get("dataset_id", ""),
        "prompts": input_dict.get("prompts", []),
        "autoGeneratePrompt": input_dict.get("autoGeneratePrompt", False),
        "categories": input_dict.get("categories", []),
        "project_type": input_dict.get("project_type", "detection"),  # Default to 'detection' if not provided
        "project_id": input_dict.get("project_id", "")
    }
    return result

class DataGeneration:
    """Class to handle dataset preparation for synthetic generation."""

    def __init__(self, session: Any, action_record_id: str):
        """Initialize DataGeneration.

        Args:
            session: Session object with RPC client
            action_record_id: ID of action record
        """
        self.session = session
        self.rpc = session.rpc
        self.action_record_id = action_record_id

        # Fetch action details
        url = f"/v1/project/action/{self.action_record_id}/details"
        response = self.rpc.get(url)
        self.action_doc = response["data"]

        # Extract fields
        self.action_type = self.action_doc.get("action")
        self.job_params = self.action_doc.get("jobParams", {})
        self.action_details = self.action_doc.get("actionDetails", {})

        logging.info(f"Job parameters: {self.job_params}")

        # Extract nested fields
        self.dataset_id = self.action_details.get("_idDataset")
        self.source_dataset_version = self.job_params.get("source_version", "")
        self.target_dataset_version = self.job_params.get("target_version", "")
        self.generation_params = self.job_params.get("generationConfig", {})

        # Transform using updated function
        self.formatted_generation = transform_synthetic_data(self.generation_params)

        self.kafka_config = self.job_params.get("kafka_config", {})

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
        """Start dataset synthetic generation processing."""
        self.update_status(
            "DCKR_PROC",
            "OK",
            "Dataset started synthetic generation",
        )

        try:
            logging.info(f"Processing synthetic generation config: {json.dumps(self.formatted_generation, indent=2)}")
            
            self.pipeline_config = parse_synthetic_pipeline_config(
                self.formatted_generation, 
                self.source_dataset_version, 
                self.target_dataset_version
            )
            logging.debug(f"Parsed pipeline config: {self.pipeline_config}")
            for attr, value in vars(self.pipeline_config).items():
                logging.info(f"Pipeline Config Attribute - {attr}: {value}")
            
            self.pipeline = create_synthetic_generation_pipeline(
                pipeline_config=self.pipeline_config,
                kafka_config=self.kafka_config,
                rpc=self.rpc,
                project_type=self.pipeline_config.project_type,
                session=self.session
            )
            self.pipeline.start()
            self.pipeline.wait_to_finish_processing_and_stop()
            new_dataset_items = self.pipeline.get_all_items_from_last_stage()

            try:
                completion_url = f"/v1/dataset_item/complete_bulk_data_generation/{self.pipeline_config.generation_id}"
                logging.debug(f"Calling completion API at {completion_url}")
                response = self.rpc.post(path=completion_url, payload={})

                if response and response.get("success"):
                    logging.info("Completion API called successfully")
                else:
                    logging.warning(f"Completion API call returned status {response}")
            except Exception as e:
                logging.error(f"Error calling completion API: {e}")

            self.update_status(
                "SUCCESS",
                "SUCCESS",
                "Dataset Synthetic Generation completed",
            )
        except Exception as e:
            logging.error(f"Error processing synthetic generation: {e}")
            self.update_status(
                "FAILED",
                "FAILED",
                f"Dataset Synthetic Generation failed: {str(e)}",
            )
            raise
