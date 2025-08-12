import json
import logging
import os
import time
import threading
from datetime import datetime
from typing import Dict, Optional, Callable
from confluent_kafka import Producer
from matrice.deploy.client.streaming_gateway.streaming_gateway_utils import (
    OutputType,
    OutputConfig,
    _RealTimeJsonEventPicker,
)
from matrice.deploy.client.client_stream_utils import ClientStreamUtils
from matrice.deploy.utils.post_processing import PostProcessor

class StreamingResultsHandler:
    def __init__(
        self, 
        client_stream_utils: ClientStreamUtils, 
        output_config: OutputConfig,
        json_event_picker: _RealTimeJsonEventPicker,
        service_id: str = None,
        strip_input_from_result: bool = True,
        result_callback: Optional[Callable] = None
    ):
        self.client_stream_utils = client_stream_utils
        self.output_config = output_config
        self.json_event_picker = json_event_picker
        self.service_id = service_id
        self.strip_input_from_result = strip_input_from_result
        self.result_callback = result_callback
        
        # Initialize state management
        self._state_lock = threading.RLock()
        self._stop_streaming = threading.Event()
        self._file_counter = 0
        self.kafka_producer = None
        
        # Initialize statistics
        self.stats = {
            "start_time": None,
            "results_received": 0,
            "results_post_processed": 0,
            "post_processing_errors": 0,
            "errors": 0,
            "last_error": None,
            "last_error_time": None,
        }
        
        # Initialize post-processor only if post_processing_config exists
        self.post_processor = None
        if (self.output_config and 
            self.output_config.post_processing_config and 
            self.output_config.apply_post_processing):
            try:
                self.post_processor = PostProcessor(
                    config=self.output_config.post_processing_config,
                    index_to_category=self.output_config.post_processing_config.index_to_category,
                    map_index_to_category=self.output_config.post_processing_config.map_index_to_category,
                )
            except Exception as exc:
                logging.error(f"Failed to initialize post-processor: {exc}")
                self.post_processor = None

    def _setup_output(self):
        """Setup output configurations."""
        if not self.output_config:
            return

        try:
            # Setup file output
            if self.output_config.type in [OutputType.FILE, OutputType.BOTH]:
                if self.output_config.file_config:
                    os.makedirs(self.output_config.file_config.directory, exist_ok=True)

            # Setup Kafka output
            if self.output_config.type in [OutputType.KAFKA, OutputType.BOTH]:
                if self.output_config.kafka_config:
                    self._setup_kafka_producer()
        except Exception as exc:
            logging.error(f"Error setting up output: {exc}")
            raise

    def _setup_kafka_producer(self):
        """Setup Kafka producer for custom output."""
        try:
            kafka_config = self.output_config.kafka_config
            producer_config = {
                "bootstrap.servers": kafka_config.bootstrap_servers,
                "acks": "all",
                "retries": 3,
                "batch.size": 16384,
                "linger.ms": 1,
                "buffer.memory": 33554432,
            }

            # Add custom producer config if provided
            if kafka_config.producer_config:
                producer_config.update(kafka_config.producer_config)

            self.kafka_producer = Producer(producer_config)
            logging.info("Kafka producer initialized successfully")
        except Exception as exc:
            logging.error(f"Failed to setup Kafka producer: {exc}")
            raise

    def _setup_post_processing(self):
        """Setup post-processing capabilities."""
        if not self.output_config.post_processing_config:
            raise ValueError(
                "Post-processing configuration is required when apply_post_processing is True"
            )

        try:
            # Initialize PostProcessor with the configuration
            self.post_processor = PostProcessor(
                config=self.output_config.post_processing_config,
                index_to_category=self.output_config.post_processing_config.index_to_category,
                map_index_to_category=self.output_config.post_processing_config.map_index_to_category,
            )
            logging.info("Post-processing initialized successfully")
        except Exception as exc:
            logging.error(f"Failed to setup post-processing: {exc}")
            raise

    def _apply_post_processing(self, result: Dict) -> Dict:
        """Apply post-processing to a result.

        Args:
            result: Raw result from the model

        Returns:
            Dict containing both original and processed results
        """
        if not self.post_processor:
            return result

        try:
            # Extract the model output from the result
            model_output = result.get("result", result)

            # Apply post-processing
            processed_result = self.post_processor.process(model_output)

            # Update statistics
            with self._state_lock:
                self.stats["results_post_processed"] += 1

            # Create enhanced result
            enhanced_result = result.copy()
            enhanced_result["post_processing_applied"] = True
            enhanced_result["post_processing_result"] = processed_result

            # Optionally keep original result
            if self.output_config.save_original_results:
                enhanced_result["original_result"] = result.get("result", result)
            else:
                # Replace the result with processed data
                enhanced_result["result"] = processed_result.get(
                    "processed_data", model_output
                )

            return enhanced_result

        except Exception as exc:
            logging.error(f"Post-processing failed: {exc}")
            with self._state_lock:
                self.stats["post_processing_errors"] += 1
                self.stats["last_error"] = f"Post-processing error: {str(exc)}"
                self.stats["last_error_time"] = time.time()

            # Return original result with error information
            error_result = result.copy()
            error_result["post_processing_applied"] = False
            error_result["post_processing_error"] = str(exc)
            return error_result
        
    def _consume_results(self, send_to_api: bool = False):
        """Consume and process results from the deployment."""
        logging.info("Starting result consumption thread")

        while not self._stop_streaming.is_set():
            try:
                result = self.client_stream_utils.consume_result(timeout=5)

                if not result:
                    continue

                # Remove input field if configured to do so
                if self.strip_input_from_result and "input" in result["value"]:
                    del result["value"]["input"]

                with self._state_lock:
                    self.stats["results_received"] += 1

                # Apply post-processing if configured
                processed_result = result
                if self.output_config and self.output_config.apply_post_processing:
                    processed_result = self._apply_post_processing(result)

                # Process result based on output configuration
                if self.output_config:
                    try:
                        if self.output_config.type in [
                            OutputType.FILE,
                            OutputType.BOTH,
                        ]:
                            self._save_result_to_file(processed_result,send_to_api=send_to_api)

                        if self.output_config.type in [
                            OutputType.KAFKA,
                            OutputType.BOTH,
                        ]:
                            self._send_result_to_kafka(processed_result)

                    except Exception as output_exc:
                        logging.error(f"Error processing output: {output_exc}")
                        with self._state_lock:
                            self.stats["errors"] += 1
                            self.stats["last_error"] = str(output_exc)
                            self.stats["last_error_time"] = time.time()

                # Call custom callback if provided (use processed result)
                if self.result_callback:
                    try:
                        self.result_callback(processed_result)
                    except Exception as callback_exc:
                        logging.error(f"Error in result callback: {callback_exc}")
                        with self._state_lock:
                            self.stats["errors"] += 1
                            self.stats["last_error"] = str(callback_exc)
                            self.stats["last_error_time"] = time.time()

            except Exception as e:
                logging.error(f"Error in result consumption: {e}")
                with self._state_lock:
                    self.stats["errors"] += 1
                    self.stats["last_error"] = str(e)
                    self.stats["last_error_time"] = time.time()

                # Add a small delay to prevent tight error loops
                time.sleep(0.1)

        logging.info("Result consumption thread stopped")

    def _save_result_to_file(self, result: Dict, send_to_api: bool = False):
        """Save result to file."""
        if not self.output_config.file_config:
            return

        try:
            value = result["value"]
            stream_key = (
                value.get("stream_info", {}).get("stream_key") or
                value.get("stream_key") or
                value.get("camera_id") or
                value.get("stream_id") or
                value.get("source_id") or
                value.get("key") or
                result.get("key")
            )
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]

            filename = self.output_config.file_config.filename_pattern.format(
                frame_number=result.get("frame_number", self._file_counter),
                stream_key=stream_key,
                timestamp=timestamp,
            )

            filepath = os.path.join(self.output_config.file_config.directory, filename)

            # Add metadata
            result_with_metadata = {
                "timestamp": timestamp,
                "service_id": self.service_id,
                "stream_key": stream_key,
                "result": result,
            }

            if send_to_api:
                self._send_file_to_api_(result_with_metadata) #demo function to send highlight json to api. 

            # Write atomically by using a temporary file
            temp_filepath = filepath + ".tmp"
            try:
                with open(temp_filepath, "w") as f:
                    json.dump(
                        result_with_metadata, f, indent=2, default=str
                    )  # Use default=str for non-serializable objects
            except (TypeError, ValueError) as json_err:
                logging.error(f"JSON serialization error: {json_err}")
                # Try to save a simplified version
                simplified_result = {
                    "timestamp": timestamp,
                    "service_id": str(self.service_id),
                    "stream_key": str(stream_key),
                    "result": str(result),  # Convert to string as fallback
                    "json_error": str(json_err),
                }
                with open(temp_filepath, "w") as f:
                    json.dump(simplified_result, f, indent=2)

            os.rename(temp_filepath, filepath)
            self._file_counter += 1

            # Cleanup old files if needed
            if (
                self.output_config.file_config.max_files
                and self._file_counter % 10 == 0
            ):
                self._cleanup_old_files()

        except Exception as e:
            logging.error(f"Failed to save result to file: {e}")
            logging.exception("File save error details:")
            raise
    def _send_file_to_api_(self, frame_json):
        """Send file to API."""
        # frame_id = list(frame_json.get("result").get("value").get("agg_summary").keys())[0]
        frame_id = list(frame_json.get("result").get("value").get("agg_apps")[0].get("agg_summary").keys())[0]
        return self.json_event_picker.process(int(frame_id), frame_json)
    def _cleanup_old_files(self):
        """Remove old result files if exceeding max_files limit."""
        try:
            directory = self.output_config.file_config.directory
            max_files = self.output_config.file_config.max_files

            files = []
            for filename in os.listdir(directory):
                if filename.endswith(".json") and not filename.endswith(".tmp"):
                    filepath = os.path.join(directory, filename)
                    if os.path.isfile(filepath):
                        files.append((filepath, os.path.getctime(filepath)))

            # Sort by creation time (oldest first)
            files.sort(key=lambda x: x[1])

            # Remove oldest files if exceeding limit
            while len(files) >= max_files:
                filepath, _ = files.pop(0)
                try:
                    os.remove(filepath)
                    logging.debug(f"Removed old result file: {filepath}")
                except Exception as e:
                    logging.warning(f"Failed to remove old file {filepath}: {e}")
        except Exception as e:
            logging.warning(f"Error during file cleanup: {e}")

    def _send_result_to_kafka(self, result: Dict):
        """Send result to custom Kafka topic."""
        if not self.kafka_producer or not self.output_config.kafka_config:
            return

        try:
            message = {
                "timestamp": datetime.now().isoformat(),
                "service_id": self.service_id,
                "result": result,
            }

            key = result.get(self.output_config.kafka_config.key_field or "key")

            try:
                # Attempt JSON serialization
                message_json = json.dumps(
                    message, default=str
                )  # Use default=str for non-serializable objects
            except (TypeError, ValueError) as json_err:
                logging.error(f"JSON serialization error for Kafka: {json_err}")
                # Create a simplified message
                simplified_message = {
                    "timestamp": datetime.now().isoformat(),
                    "service_id": str(self.service_id),
                    "result": str(result),  # Convert to string as fallback
                    "json_error": str(json_err),
                }
                message_json = json.dumps(simplified_message)

            self.kafka_producer.produce(
                topic=self.output_config.kafka_config.topic,
                key=str(key) if key else None,
                value=message_json.encode("utf-8"),
            )
            self.kafka_producer.poll(0)  # Non-blocking poll

        except Exception as e:
            logging.error(f"Failed to send result to Kafka: {e}")
            logging.exception("Kafka send error details:")
            raise