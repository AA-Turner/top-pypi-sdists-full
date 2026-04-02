from typing import Any, Dict, List

from app.src.domain.repositories.task_repository import TaskRepository


class TaskService:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    async def create_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        return await self.task_repository.create_task(task_data)

    async def get_tasks(
        self,
        page: int,
        per_page: int,
    ) -> List[Dict[str, Any]]:
        return await self.task_repository.get_tasks(page, per_page)

    async def update_task(
        self, task_id: int, task_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        return await self.task_repository.update_task(task_id, task_data)

    async def get_task(self, task_id: int) -> Dict[str, Any]:
        return await self.task_repository.get_task(task_id)

    async def delete_task(self, task_id: int) -> Dict[str, Any]:
        return await self.task_repository.delete_task(task_id)

    async def assign_task(self, task_id: int, user_id: int) -> Dict[str, Any]:
        return await self.task_repository.assign_task(task_id, user_id)

    async def start_task(self, task_id: int) -> Dict[str, Any]:
        return await self.task_repository.start_task(task_id)

    async def finalize_task(self, task_id: int) -> Dict[str, Any]:
        return await self.task_repository.finalize_task(task_id)

    async def approve_task(self, task_id: int) -> Dict[str, Any]:
        return await self.task_repository.approve_task(task_id)

    async def reject_task(self, task_id: int) -> Dict[str, Any]:
        return await self.task_repository.reject_task(task_id)
