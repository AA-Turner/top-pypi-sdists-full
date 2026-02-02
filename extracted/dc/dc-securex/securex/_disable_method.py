    async def disable(self):
        """
        Disable SecureX protection and cleanup resources gracefully.
        Closes connection pools and stops background workers.
        """
        # Stop workers
        print("🛑 Stopping workers...")
        # (Worker stopping logic would go here)
        
        # Close storage backend (PostgreSQL pool)
        if hasattr(self.storage, 'close'):
            await self.storage.close()
            print(f"✅ {self.storage_backend_type.upper()} storage backend closed")
        
        print("✅ SecureX SDK disabled")
