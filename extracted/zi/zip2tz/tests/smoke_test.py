import zip2tz
import sys

def test_lookup():
    # Test known zipcodes from our placeholder data
    assert zip2tz.timezone("90210") == "America/Los_Angeles", "Failed 90210"
    assert zip2tz.timezone("10001") == "America/New_York", "Failed 10001"
    assert zip2tz.timezone("60601") == "America/Chicago", "Failed 60601"
    
    # Test unknown
    assert zip2tz.timezone("00000") is None, "Failed unknown"
    
    print("Smoke test passed!")

if __name__ == "__main__":
    try:
        test_lookup()
    except Exception as e:
        print(f"Test failed: {e}")
        sys.exit(1)
