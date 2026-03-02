"""Test msgpack unpacking in inference pipeline consumer worker.

NOTE: This test is outdated. ConsumerWorker has been replaced by AsyncConsumerManager.
TODO: Update this test to test AsyncConsumerManager or remove if no longer needed.
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# NOTE: ConsumerWorker has been removed - this test needs updating
# from matrice_inference.server.stream.consumer_worker import ConsumerWorker
import msgpack


def test_msgpack_unpacking():
    """Test that consumer worker can unpack msgpack-serialized data."""
    print("Testing msgpack unpacking in consumer worker...")
    print("="*60)

    # Create a mock consumer worker (we'll just test the helper method)
    class MockCameraConfig:
        enabled = True

    # Mock minimal required params
    worker = ConsumerWorker(
        camera_id="test_camera",
        worker_id=0,
        stream_config={"stream_type": "redis"},
        input_topic="test_topic",
        inference_queue=None,  # Not needed for this test
        message_timeout=1.0,
        camera_config=MockCameraConfig(),
        frame_cache=None,
        use_shared_metrics=False
    )

    print("\n1. Test msgpack-serialized nested structure:")

    # Simulate streaming gateway message structure
    # The top-level message is a dict, but input_stream is msgpack-serialized
    input_stream_data = {
        "ip_key_name": "test_service",
        "stream_info": {
            "broker": "redis://localhost:6379",
            "topic": "test_topic"
        },
        "video_codec": "h264",
        "content": b"fake_jpeg_data_12345",  # Binary content
        "input_hash": "abc123"
    }

    # Serialize input_stream with msgpack (like streaming gateway does)
    input_stream_msgpack = msgpack.packb(input_stream_data, use_bin_type=True)

    # Create message data structure
    message_data = {
        "frame_id": "test_frame_123",
        "input_name": "frame_1",
        "input_unit": "frame",
        "input_stream": input_stream_msgpack  # Msgpack-serialized bytes
    }

    print(f"   - input_stream is msgpack bytes: {len(input_stream_msgpack)} bytes")
    print(f"   - Original binary content size: {len(input_stream_data['content'])} bytes")

    print("\n2. Unpack msgpack fields:")

    # Use the worker's _unpack_msgpack_fields method
    unpacked = worker._unpack_msgpack_fields(message_data)

    print(f"   - Unpacked keys: {list(unpacked.keys())}")

    # Check if input_stream was unpacked
    if isinstance(unpacked.get("input_stream"), dict):
        print("   - input_stream successfully unpacked to dict!")
        input_stream_unpacked = unpacked["input_stream"]
        print(f"   - Unpacked input_stream keys: {list(input_stream_unpacked.keys())}")

        # Check if binary content was preserved
        if "content" in input_stream_unpacked:
            content = input_stream_unpacked["content"]
            if isinstance(content, bytes):
                print(f"   - Binary content preserved: {len(content)} bytes")
                if content == input_stream_data["content"]:
                    print("   - Binary content matches original!")
                else:
                    print("   - ERROR: Binary content doesn't match!")
                    return False
            else:
                print(f"   - ERROR: Content is not bytes: {type(content)}")
                return False
        else:
            print("   - ERROR: 'content' field not found in unpacked input_stream!")
            return False
    else:
        print(f"   - ERROR: input_stream was not unpacked! Type: {type(unpacked.get('input_stream'))}")
        return False

    print("\n3. Test _parse_message_data with msgpack:")

    # Simulate Redis message format with msgpack-serialized value
    redis_message = {
        "key": "test_key",
        "value": message_data  # Dict with msgpack-serialized nested field
    }

    parsed = worker._parse_message_data(redis_message)

    print(f"   - Parsed keys: {list(parsed.keys())}")

    if isinstance(parsed.get("input_stream"), dict):
        print("   - input_stream successfully parsed and unpacked!")
        print(f"   - input_stream has {len(parsed['input_stream'])} fields")
    else:
        print(f"   - ERROR: input_stream not properly unpacked! Type: {type(parsed.get('input_stream'))}")
        return False

    print("\n" + "="*60)
    print("TEST PASSED: Msgpack unpacking works correctly!")
    print("="*60)
    print("\nInference pipeline can now read msgpack-serialized messages")
    print("from streaming gateway with binary content preserved.")

    return True


if __name__ == "__main__":
    try:
        success = test_msgpack_unpacking()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\nERROR: Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
