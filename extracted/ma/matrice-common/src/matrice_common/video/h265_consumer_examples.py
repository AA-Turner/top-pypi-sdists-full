"""Example H.265 consumer classes for both frame-wise and stream-wise decoding."""
import redis
import logging
import threading
import queue
import numpy as np
import cv2
from typing import Optional, Callable, Generator
from .h265_video_processor import H265FrameDecoder, H265StreamDecoder, decode_frame_h265

logger = logging.getLogger(__name__)


class H265FrameConsumer:
    """Consumer for frame-wise H.265 encoded messages (compatible with existing downstream)."""
    
    def __init__(
        self, 
        redis_host: str = "localhost", 
        redis_port: int = 6379, 
        redis_db: int = 0,
        use_hardware: bool = False
    ):
        """Initialize frame-wise H.265 consumer.
        
        Args:
            redis_host: Redis server host
            redis_port: Redis server port  
            redis_db: Redis database number
            use_hardware: Use hardware decoding if available
        """
        self.redis_client = redis.Redis(host=redis_host, port=redis_port, db=redis_db)
        self.use_hardware = use_hardware
        self.decoder = H265FrameDecoder(use_hardware=use_hardware)
        
    def consume_frames(
        self, 
        channel: str, 
        frame_callback: Callable[[np.ndarray, dict], None],
        width: int,
        height: int
    ):
        """Consume H.265 frames from Redis channel.
        
        Args:
            channel: Redis channel name
            frame_callback: Callback function(frame, metadata)
            width: Expected frame width
            height: Expected frame height
        """
        pubsub = self.redis_client.pubsub()
        pubsub.subscribe(channel)
        
        logger.info(f"Started consuming H.265 frames from channel: {channel}")
        
        try:
            for message in pubsub.listen():
                if message["type"] != "message":
                    continue
                    
                try:
                    # Decode H.265 frame data
                    h265_data = message["data"]
                    frame = decode_frame_h265(
                        h265_data, 
                        width=width, 
                        height=height, 
                        use_hardware=self.use_hardware
                    )
                    
                    if frame is not None:
                        # Create metadata
                        metadata = {
                            "channel": channel,
                            "encoding": "h265",
                            "size": len(h265_data),
                            "shape": frame.shape
                        }
                        
                        # Call user callback
                        frame_callback(frame, metadata)
                    else:
                        logger.warning("Failed to decode H.265 frame")
                        
                except Exception as e:
                    logger.error(f"Error processing H.265 frame: {e}")
                    
        except KeyboardInterrupt:
            logger.info("Stopping H.265 frame consumer")
        finally:
            pubsub.close()


class H265StreamConsumer:
    """Consumer for continuous H.265 stream chunks (optimal compression)."""
    
    def __init__(
        self, 
        redis_host: str = "localhost", 
        redis_port: int = 6379, 
        redis_db: int = 0,
        width: int = 640,
        height: int = 480,
        use_hardware: bool = False
    ):
        """Initialize stream-wise H.265 consumer.
        
        Args:
            redis_host: Redis server host
            redis_port: Redis server port
            redis_db: Redis database number
            width: Expected frame width
            height: Expected frame height
            use_hardware: Use hardware decoding if available
        """
        self.redis_client = redis.Redis(host=redis_host, port=redis_port, db=redis_db)
        self.width = width
        self.height = height
        self.use_hardware = use_hardware
        
        # Stream decoder
        self.decoder = H265StreamDecoder(width, height, use_hardware)
        
        # Frame output queue
        self.frame_queue: queue.Queue[np.ndarray] = queue.Queue(maxsize=50)
        self._stop_consuming = False
        
    def start_consuming(self, channel: str) -> bool:
        """Start consuming H.265 stream chunks from Redis channel.
        
        Args:
            channel: Redis channel name
            
        Returns:
            True if started successfully
        """
        try:
            # Start decoder
            if not self.decoder.start():
                logger.error("Failed to start H.265 stream decoder")
                return False
                
            # Start Redis consumer thread
            self._stop_consuming = False
            self.consumer_thread = threading.Thread(
                target=self._consume_chunks, 
                args=(channel,), 
                daemon=True
            )
            self.consumer_thread.start()
            
            logger.info(f"Started consuming H.265 stream from channel: {channel}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start H.265 stream consumer: {e}")
            return False
            
    def stop_consuming(self):
        """Stop consuming H.265 stream chunks."""
        self._stop_consuming = True
        
        if hasattr(self, 'consumer_thread'):
            self.consumer_thread.join(timeout=2)
            
        self.decoder.stop()
        logger.info("Stopped H.265 stream consumer")
        
    def get_frame(self, timeout: float = 0.1) -> Optional[np.ndarray]:
        """Get next decoded frame.
        
        Args:
            timeout: Timeout in seconds
            
        Returns:
            OpenCV frame (BGR format) or None
        """
        try:
            return self.frame_queue.get(timeout=timeout)
        except queue.Empty:
            return None
            
    def get_frames(self) -> Generator[np.ndarray, None, None]:
        """Generator that yields decoded frames."""
        while not self._stop_consuming:
            frame = self.get_frame(timeout=0.1)
            if frame is not None:
                yield frame
                
    def _consume_chunks(self, channel: str):
        """Background thread to consume H.265 chunks from Redis."""
        pubsub = self.redis_client.pubsub()
        pubsub.subscribe(channel)
        
        try:
            for message in pubsub.listen():
                if self._stop_consuming:
                    break
                    
                if message["type"] != "message":
                    continue
                    
                try:
                    # Feed H.265 chunk to decoder
                    h265_chunk = message["data"]
                    if self.decoder.decode_chunk(h265_chunk):
                        # Get any decoded frames
                        while True:
                            frame = self.decoder.get_frame(timeout=0.001)
                            if frame is not None:
                                if not self.frame_queue.full():
                                    self.frame_queue.put(frame)
                                else:
                                    logger.warning("Frame queue full, dropping frame")
                            else:
                                break
                    else:
                        logger.warning("Failed to decode H.265 chunk")
                        
                except Exception as e:
                    logger.error(f"Error processing H.265 chunk: {e}")
                    
        except Exception as e:
            logger.error(f"Error in H.265 chunk consumer: {e}")
        finally:
            pubsub.close()


# Example usage functions
def example_frame_consumer():
    """Example of consuming frame-wise H.265."""
    def on_frame(frame, metadata):
        print(f"Received H.265 frame: {frame.shape}, size: {metadata['size']} bytes")
        cv2.imshow("H.265 Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return
            
    consumer = H265FrameConsumer()
    consumer.consume_frames(
        channel="camera_frames",
        frame_callback=on_frame,
        width=640,
        height=480
    )
    cv2.destroyAllWindows()


def example_stream_consumer():
    """Example of consuming continuous H.265 stream."""
    consumer = H265StreamConsumer(width=640, height=480)
    
    if consumer.start_consuming("camera_stream"):
        try:
            for frame in consumer.get_frames():
                cv2.imshow("H.265 Stream", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        except KeyboardInterrupt:
            pass
        finally:
            consumer.stop_consuming()
            cv2.destroyAllWindows()


if __name__ == "__main__":
    # Run frame consumer example
    print("Starting H.265 frame consumer example...")
    example_frame_consumer()
    
    # Run stream consumer example  
    print("Starting H.265 stream consumer example...")
    example_stream_consumer()