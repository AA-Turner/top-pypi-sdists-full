from abc import ABC, abstractmethod


class StorageProvider(ABC):
    @abstractmethod
    async def retrieve_user(self, search_query: dict) -> dict:
        pass

    @abstractmethod
    async def update_user(self, id: str, update_data: dict) -> tuple[int, str | None]:
        pass

    @abstractmethod
    async def insert_user(self, user_data: dict) -> int:
        pass

    @abstractmethod
    async def delete_user(self, id: int) -> tuple[int, str | None]:
        pass

    @abstractmethod
    async def merge_accounts(
        self, from_account_id: int, to_account_id: int
    ) -> tuple[int, str | None]:
        """
        Merge two accounts by transferring all related records from source to target,
        then deleting the source account.

        Args:
            from_account_id: Source account ID (will be deleted)
            to_account_id: Target account ID (will receive all records)

        Returns:
            Tuple of (records_transferred_count, error_message)
        """
        pass
