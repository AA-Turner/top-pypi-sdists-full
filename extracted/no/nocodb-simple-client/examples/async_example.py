"""
Async client examples for NocoDB Simple Client.

This example demonstrates how to use the async client for high-performance
concurrent operations with NocoDB.

INSTALLATION:
    pip install "nocodb-simple-client[async]"

This installs the required dependencies:
    - aiohttp: Async HTTP client
    - aiofiles: Async file operations
"""

import asyncio
import importlib.util
import sys

# =============================================================================
# DEPENDENCY CHECK
# =============================================================================
# Check if async dependencies are available before importing

ASYNC_AVAILABLE = (
    importlib.util.find_spec("aiohttp") is not None
    and importlib.util.find_spec("aiofiles") is not None
)

if not ASYNC_AVAILABLE:
    print("=" * 60)
    print("ERROR: Async dependencies not installed!")
    print("=" * 60)
    print()
    print("To use the async client, install the [async] extra:")
    print()
    print('    pip install "nocodb-simple-client[async]"')
    print()
    print("This will install: aiohttp, aiofiles")
    print("=" * 60)
    sys.exit(1)

# Now we can safely import the async client
from nocodb_simple_client import NocoDBConfig  # noqa: E402
from nocodb_simple_client.async_client import (  # noqa: E402
    AsyncNocoDBClient,
    AsyncNocoDBTable,
)
from nocodb_simple_client.exceptions import (  # noqa: E402
    AuthenticationException,
    NocoDBException,
    RateLimitException,
    RecordNotFoundException,
)

# =============================================================================
# CONFIGURATION
# =============================================================================
NOCODB_BASE_URL = "https://your-nocodb-instance.com"
API_TOKEN = "your-api-token-here"
TABLE_ID = "your-table-id-here"


# =============================================================================
# EXAMPLE 1: Basic Async Operations
# =============================================================================
async def example_basic_operations():
    """Demonstrate basic async CRUD operations."""
    print("\n" + "=" * 60)
    print("Example 1: Basic Async Operations")
    print("=" * 60)

    config = NocoDBConfig(
        base_url=NOCODB_BASE_URL,
        api_token=API_TOKEN,
        timeout=30.0,
    )

    # Use async context manager for automatic session management
    async with AsyncNocoDBClient(config) as client:
        table = AsyncNocoDBTable(client, TABLE_ID)

        # Insert a record
        record_id = await table.insert_record(
            {
                "Name": "Async User",
                "Email": "async@example.com",
            }
        )
        print(f"Inserted record: {record_id}")

        # Get the record
        record = await table.get_record(record_id)
        print(f"Retrieved record: {record}")

        # Update the record
        await table.update_record({"Id": record_id, "Name": "Updated Async User"})
        print(f"Updated record: {record_id}")

        # Delete the record
        await table.delete_record(record_id)
        print(f"Deleted record: {record_id}")

    print("Basic async operations completed!")


# =============================================================================
# EXAMPLE 2: Parallel Bulk Operations
# =============================================================================
async def example_bulk_operations():
    """Demonstrate high-performance bulk operations with concurrency control."""
    print("\n" + "=" * 60)
    print("Example 2: Parallel Bulk Operations")
    print("=" * 60)

    config = NocoDBConfig(
        base_url=NOCODB_BASE_URL,
        api_token=API_TOKEN,
        pool_connections=20,  # Increase for bulk operations
        pool_maxsize=50,
    )

    async with AsyncNocoDBClient(config) as client:
        table = AsyncNocoDBTable(client, TABLE_ID)

        # Prepare records for bulk insert
        records = [{"Name": f"User {i}", "Email": f"user{i}@example.com"} for i in range(100)]

        # Bulk insert with automatic concurrency limiting (10 concurrent requests)
        print(f"Inserting {len(records)} records in parallel...")
        inserted_ids = await table.bulk_insert_records(records)
        print(f"Inserted {len(inserted_ids)} records")

        # Bulk update
        updates = [{"Id": id, "Name": f"Updated User {i}"} for i, id in enumerate(inserted_ids)]
        print(f"Updating {len(updates)} records in parallel...")
        await table.bulk_update_records(updates)
        print("Bulk update completed")

    print("Bulk operations completed!")


# =============================================================================
# EXAMPLE 3: Custom Concurrency Control
# =============================================================================
async def example_custom_concurrency():
    """Demonstrate custom concurrency control with semaphores."""
    print("\n" + "=" * 60)
    print("Example 3: Custom Concurrency Control")
    print("=" * 60)

    config = NocoDBConfig(
        base_url=NOCODB_BASE_URL,
        api_token=API_TOKEN,
    )

    async with AsyncNocoDBClient(config) as client:
        table = AsyncNocoDBTable(client, TABLE_ID)

        # Custom concurrency limit
        max_concurrent = 5
        semaphore = asyncio.Semaphore(max_concurrent)

        async def process_with_limit(record_data: dict) -> int | str:
            """Insert a record with concurrency limiting."""
            async with semaphore:
                return await table.insert_record(record_data)

        # Create tasks
        records = [{"Name": f"Concurrent {i}"} for i in range(20)]
        tasks = [process_with_limit(record) for record in records]

        # Execute with controlled concurrency
        print(f"Processing {len(records)} records with max {max_concurrent} concurrent...")
        results = await asyncio.gather(*tasks)
        print(f"Processed {len(results)} records")

    print("Custom concurrency example completed!")


# =============================================================================
# EXAMPLE 4: Error Handling in Async Context
# =============================================================================
async def example_error_handling():
    """Demonstrate proper error handling in async operations."""
    print("\n" + "=" * 60)
    print("Example 4: Async Error Handling")
    print("=" * 60)

    config = NocoDBConfig(
        base_url=NOCODB_BASE_URL,
        api_token=API_TOKEN,
    )

    async with AsyncNocoDBClient(config) as client:
        table = AsyncNocoDBTable(client, TABLE_ID)

        try:
            # Try to get a non-existent record
            _record = await table.get_record(999999)  # noqa: F841
        except RecordNotFoundException:
            print("Record not found (expected)")
        except AuthenticationException:
            print("Authentication failed - check your API token")
        except RateLimitException as e:
            print(f"Rate limited - retry after {e.retry_after} seconds")
        except NocoDBException as e:
            print(f"NocoDB error: {e.message}")

    print("Error handling example completed!")


# =============================================================================
# EXAMPLE 5: Parallel Queries
# =============================================================================
async def example_parallel_queries():
    """Demonstrate running multiple queries in parallel."""
    print("\n" + "=" * 60)
    print("Example 5: Parallel Queries")
    print("=" * 60)

    config = NocoDBConfig(
        base_url=NOCODB_BASE_URL,
        api_token=API_TOKEN,
    )

    async with AsyncNocoDBClient(config) as client:
        table = AsyncNocoDBTable(client, TABLE_ID)

        # Run multiple queries in parallel
        results = await asyncio.gather(
            table.get_records(limit=10, sort="Name"),
            table.get_records(limit=10, sort="-CreatedAt"),
            table.count_records(),
            table.count_records(where="(Status,eq,Active)"),
        )

        sorted_by_name, recent_records, total_count, active_count = results

        print(f"Records sorted by name: {len(sorted_by_name)}")
        print(f"Recent records: {len(recent_records)}")
        print(f"Total count: {total_count}")
        print(f"Active count: {active_count}")

    print("Parallel queries completed!")


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================
async def main():
    """Run all async examples."""
    print("\n" + "=" * 60)
    print("NOCODB SIMPLE CLIENT - ASYNC EXAMPLES")
    print("=" * 60)
    print()
    print("These examples demonstrate the [async] optional dependency group.")
    print()
    print("Installation: pip install 'nocodb-simple-client[async]'")
    print()

    # Uncomment the examples you want to run:
    # await example_basic_operations()
    # await example_bulk_operations()
    # await example_custom_concurrency()
    # await example_error_handling()
    # await example_parallel_queries()

    print("\n" + "=" * 60)
    print("Uncomment the examples in main() to run them.")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
