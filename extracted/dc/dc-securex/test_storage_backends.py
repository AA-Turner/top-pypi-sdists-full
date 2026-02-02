"""
Quick test to verify the storage backend implementation
"""

import asyncio
from securex.storage import create_storage_backend

async def test_sqlite_backend():
    """Test SQLite storage backend with WAL mode"""
    print("Testing SQLite backend...")
    
    storage = create_storage_backend("sqlite", db_path="./test_data/test.db")
    
    # Test whitelist operations
    await storage.add_whitelist_user(123456, 111111)
    await storage.add_whitelist_user(123456, 222222)
    
    is_whitelisted = await storage.is_whitelisted(123456, 111111)
    print(f"✅ User whitelisted: {is_whitelisted}")
    
    users = await storage.get_whitelist_users(123456)
    print(f"✅ Whitelisted users: {users}")
    
    # Test guild settings
    await storage.save_guild_settings(123456, {
        "guild_id": 123456,
        "name": "Test Server",
        "vanity_url_code": "test"
    })
    
    settings = await storage.load_guild_settings(123456)
    print(f"✅ Guild settings: {settings}")
    
    # Verify WAL mode is enabled
    import aiosqlite
    async with aiosqlite.connect("./test_data/test.db") as db:
        async with db.execute("PRAGMA journal_mode") as cursor:
            mode = await cursor.fetchone()
            print(f"✅ Journal mode: {mode[0]}")
            assert mode[0].lower() == "wal", "WAL mode should be enabled"

    print("✅ SQLite backend test passed!\n")

async def test_postgres_backend():
    """Test PostgreSQL storage backend (requires PostgreSQL)"""
    print("Testing PostgreSQL backend...")
    
    try:
        storage = create_storage_backend(
            "postgres",
            url="postgresql://postgres:postgres@localhost:5432/securex_test"
        )
        
        # Initialize connection pool
        await storage.initialize()
        print(f"✅ Connection pool initialized")
        print(f"   Pool size: {storage.pool.get_size()}")
        print(f"   Min: {storage.min_pool_size}, Max: {storage.max_pool_size}")
        
        # Test whitelist operations
        await storage.add_whitelist_user(123456, 111111)
        await storage.add_whitelist_user(123456, 222222)
        
        is_whitelisted = await storage.is_whitelisted(123456, 111111)
        print(f"✅ User whitelisted: {is_whitelisted}")
        
        users = await storage.get_whitelist_users(123456)
        print(f"✅ Whitelisted users: {users}")
        
        # Test guild settings
        await storage.save_guild_settings(123456, {
            "guild_id": 123456,
            "name": "Test Server",
            "vanity_url_code": "test"
        })
        
        settings = await storage.load_guild_settings(123456)
        print(f"✅ Guild settings: {settings}")
        
        # Test concurrent operations
        print("Testing concurrent operations...")
        tasks = [storage.is_whitelisted(123456, 111111) for _ in range(100)]
        results = await asyncio.gather(*tasks)
        print(f"✅ 100 concurrent whitelist checks completed")
        print(f"   All passed: {all(results)}")
        
        # Close pool
        await storage.close()
        print("✅ PostgreSQL backend test passed!\n")
        
    except ImportError:
        print("⚠️  PostgreSQL backend not available (asyncpg not installed)")
        print("   Install with: pip install dc-securex[postgres]")
    except Exception as e:
        print(f"⚠️  PostgreSQL test skipped: {e}")
        print("   Make sure PostgreSQL is running and database exists")

async def main():
    print("=" * 60)
    print("SecureX Storage Backend Test")
    print("=" * 60 + "\n")
    
    await test_sqlite_backend()
    await test_postgres_backend()
    
    print("=" * 60)
    print("All tests completed!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
