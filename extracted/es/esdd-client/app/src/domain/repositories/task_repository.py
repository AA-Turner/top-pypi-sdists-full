from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class TaskRepository(ABC):
    @abstractmethod
    async def create_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new task"""
        pass

    @abstractmethod
    async def get_tasks(
        self,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        assignee_id: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """Get list of tasks with optional filtering"""
        pass

    @abstractmethod
    async def update_task(
        self, task_id: int, task_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update an existing task"""
        pass

    @abstractmethod
    async def get_task(self, task_id: int) -> Dict[str, Any]:
        """Get detailed information about a specific task"""
        pass

    @abstractmethod
    async def delete_task(self, task_id: int) -> Dict[str, Any]:
        """Delete a task"""
        pass

    @abstractmethod
    async def assign_task(self, task_id: int, user_id: int) -> Dict[str, Any]:
        """Assign a task to a user"""
        pass

    @abstractmethod
    async def start_task(self, task_id: int) -> Dict[str, Any]:
        """Mark task as started"""
        pass

    @abstractmethod
    async def finalize_task(self, task_id: int) -> Dict[str, Any]:
        """Mark task as finalized/completed"""
        pass

    @abstractmethod
    async def approve_task(self, task_id: int) -> Dict[str, Any]:
        """Approve a completed task"""
        pass

    @abstractmethod
    async def reject_task(self, task_id: int) -> Dict[str, Any]:
        """Reject a completed task"""
        pass
