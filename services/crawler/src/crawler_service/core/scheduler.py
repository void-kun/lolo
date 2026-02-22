from crawler_service.core.task_manager import TaskManager


class Scheduler:
    def __init__(self, task_manager: TaskManager):
        self.task_manager = task_manager

    async def start(self):
        """Start the scheduler loop"""

        pass

    async def stop(self):
        """Stop the scheduler loop"""

        pass

    async def schedule_tasks(self):
        """Internal method to find and schedule pending tasks"""
        pass

    async def unschedule_task(self):
        """Internal method to unschedule a task (e.g. when cancelled)"""

        pass

    async def _load_scheduled_tasks(self):
        """Internal method to load scheduled tasks from the database on startup"""

        pass
