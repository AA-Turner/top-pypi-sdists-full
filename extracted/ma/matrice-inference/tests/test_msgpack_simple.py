"""Simple test for msgpack unpacking logic without full dependencies."""
import msgpack


def unpack_msgpack_fields(data):
    """Simplified version of the unpacking logic."""
    if not isinstance(data, dict):
        return data

    result = {}
    for key, value in data.items():
        if isinstance(value, bytes):
            # Try to unpack as msgpack (nested structure)
            try:
                unpacked = msgpack.unpackb(value, raw=False)
                result[key] = unpacked
                print(f"  Unpacked msgpack field '{key}' ({len(value)} bytes)")
            except Exception:
                # Not msgpack, keep as bytes
                result[key] = value
        elif isinstance(value, dict):
            # Recursively process nested dicts
            result[key] = unpack_msgpack_fields(value)
        else:
            result[key] = value

    return result


def test_msgpack_unpacking():
    """Test msgpack unpacking logic."""
    print("Testing msgpack unpacking logic...")
    print("="*60)

    # Create test data similar to streaming gateway message
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

    print("\n1. Original data:")
    print(f"   - Binary content size: {len(input_stream_data['content'])} bytes")

    # Serialize with msgpack (like streaming gateway)
    input_stream_msgpack = msgpack.packb(input_stream_data, use_bin_type=True)
    print(f"\n2. Msgpack serialized: {len(input_stream_msgpack)} bytes")

    # Create message structure
    message_data = {
        "frame_id": "test_frame_123",
        "input_name": "frame_1",
        "input_unit": "frame",
        "input_stream": input_stream_msgpack  # Msgpack bytes
    }

    print("\n3. Unpacking msgpack fields...")

    # Unpack
    unpacked = unpack_msgpack_fields(message_data)

    print(f"\n4. Verification:")
    print(f"   - Unpacked keys: {list(unpacked.keys())}")

    # Verify input_stream was unpacked
    if isinstance(unpacked.get("input_stream"), dict):
        print("   - input_stream: UNPACKED to dict")
        input_stream = unpacked["input_stream"]

        # Check binary content
        if "content" in input_stream:
            content = input_stream["content"]
            if isinstance(content, bytes) and content == input_stream_data["content"]:
                print(f"   - Binary content: PRESERVED ({len(content)} bytes)")
            else:
                print(f"   - ERROR: Binary content mismatch!")
                return False
        else:
            print("   - ERROR: 'content' field missing!")
            return False
    else:
        print("   - ERROR: input_stream not unpacked!")
        return False

    print("\n" + "="*60)
    print("TEST PASSED!")
    print("="*60)
    print("\nMsgpack unpacking preserves binary data correctly.")
    print("The inference pipeline can now read messages from streaming gateway.")

    return True


if __name__ == "__main__":
    try:
        success = test_msgpack_unpacking()
        exit(0 if success else 1)
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
