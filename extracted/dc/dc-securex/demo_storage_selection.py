"""
Demo showing how storage backend selection works in SecureX SDK
"""

import asyncio
from securex.storage import create_storage_backend

async def demo():
    print("=" * 60)
    print("SecureX Storage Backend Selection Demo")
    print("=" * 60 + "\n")
    
    # Example 1: Single SDK instance with JSON
    print("Example 1: SDK Instance with JSON Storage")
    print("-" * 60)
    json_storage = create_storage_backend("json", backup_dir="./data/json_storage")
    print(f"✅ Created JSON storage backend")
    print(f"   Type: {type(json_storage).__name__}")
    print(f"   Data directory: ./data/json_storage\n")
    
    # Example 2: Single SDK instance with PostgreSQL
    print("Example 2: SDK Instance with PostgreSQL Storage")
    print("-" * 60)
    try:
        pg_storage = create_storage_backend(
            "postgres",
            url="postgresql://postgres:postgres@localhost:5432/securex_test"
        )
        await pg_storage.initialize()
        print(f"✅ Created PostgreSQL storage backend")
        print(f"   Type: {type(pg_storage).__name__}") 
        print(f"   Pool size: {pg_storage.pool.get_size()}")
        print(f"   Idle connections: {pg_storage.pool.get_idle_size()}\n")
        await pg_storage.close()
    except Exception as e:
        print(f"⚠️  PostgreSQL not available: {e}\n")
    
    # Example 3: Can you use both at once? NO!
    print("Example 3: Can One SDK Instance Use Both? NO!")
    print("-" * 60)
    print("❌ An SDK instance uses EITHER JSON OR PostgreSQL")
    print("❌ You cannot use both storage backends simultaneously")
    print("   in the same SDK instance.\n")
    
    # Example 4: Multiple SDK instances (if needed)
    print("Example 4: Multiple SDK Instances (Advanced Use Case)")
    print("-" * 60)
    print("✅ You CAN have multiple SDK instances with different backends:")
    print("""
    # Bot 1 uses JSON
    sdk1 = SecureX(bot=bot1, storage_backend="json")
    
    # Bot 2 uses PostgreSQL 
    sdk2 = SecureX(bot=bot2, storage_backend="postgres", 
                   postgres_url="postgresql://...")
    """)
    
    # Example 5: Typical Usage
    print("\nExample 5: Typical Production Usage")
    print("-" * 60)
    print("""
    Most users choose ONE backend based on their needs:
    
    • Small/Medium bots (< 1000 servers):
      → Use JSON (default, no setup needed)
    
    • Large bots (1000+ servers):
      → Use PostgreSQL (better performance, scalability)
    
    • Multi-server deployments:
      → Use PostgreSQL (shared database)
    """)
    
    print("\n" + "=" * 60)
    print("Key Takeaway:")
    print("=" * 60)
    print("ONE SDK instance = ONE storage backend choice")
    print("Choose based on your scale and deployment needs!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(demo())
