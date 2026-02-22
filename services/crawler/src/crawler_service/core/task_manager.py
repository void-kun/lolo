from uuid import UUID

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from crawler_service.models.enum import TaskStatus
from crawler_service.models.task import Task
from crawler_service.schemas.task import TaskCreate, TaskUpdate


class TaskManager:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_task(self, task_data: TaskCreate, user_id: UUID) -> Task:
        """Create a new task"""

        task = Task(
            user_id=user_id,
            name=task_data.name,
            description=task_data.description,
            task_type=task_data.task_type,
            execution_method=task_data.execution_method,
            config=task_data.config,
            schedule_config=task_data.schedule_config,
            priority=task_data.priority,
            max_retries=task_data.max_retries,
        )

        self.db_session.add(task)
        await self.db_session.commit()
        await self.db_session.refresh(task)

        logger.info(f"Task created: {task.id} by user {user_id}")
        return task

    async def get_task(self, task_id: UUID):
        """Get a task by ID"""

        pass

    async def list_tasks(self, user_id: UUID, status: TaskStatus):
        """List tasks for a user with optional status filter"""

        pass

    async def update_task(self, task_id: UUID, task_data: TaskUpdate):
        """Update a task's details"""

        pass

    async def cancel_task(self, task_id: UUID):
        """Cancel a task"""

        pass

    async def _dispatch_task(self, task: Task):
        """Internal method to dispatch a task for execution"""

        pass
