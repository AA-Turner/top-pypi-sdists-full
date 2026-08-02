import time

from uuid_extension import uuid7

# Example usage
print(f"UUIDv7: {repr(uuid7())}")
print(f"UUIDv7 string: {uuid7()}")

# Generate a few UUIDs to show time ordering

print("\nMultiple UUIDs (should be time-ordered):")
for _ in range(5):
    u = uuid7()
    print(u, "->", u.to_datetime(), "->", u.to_timestamp())
    time.sleep(0.1)  # Small delay to see time difference
