from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from crawler_service.models.enum import ExecutionMethod, TaskStatus, TaskType


class TaskBase(BaseModel):
    """Base task fields"""

    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    task_type: TaskType
    execution_method: ExecutionMethod
    config: Dict[str, Any] = Field(default_factory=dict)
    schedule_config: Optional[Dict[str, Any]] = Field(default_factory=dict)
    priority: int = Field(default=5, ge=1, le=10)
    max_retries: int = Field(default=3, ge=0, le=10)

    @field_validator("config")
    @classmethod
    def validate_config(cls, c: Dict[str, Any], info) -> Dict[str, Any]:
        execution_method = info.data.get("execution_method")

        if execution_method == ExecutionMethod.SCRIPT:
            if "script_path" not in c:
                raise ValueError(
                    "config must include 'script_path' for SCRIPT execution method"
                )

        elif execution_method in [
            ExecutionMethod.AGENT_GRPC,
            ExecutionMethod.AGENT_HTTP,
        ]:
            if "agent_url" not in c and "agent_id" not in c:
                raise ValueError(
                    "config must include 'agent_url' or 'agent_id' for AGENT execution methods"
                )

        return c


class TaskCreate(TaskBase):
    """Fields required to create a task"""

    pass


class TaskUpdate(BaseModel):
    """Fields allowed to update in a task"""

    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    schedule_config: Optional[Dict[str, Any]] = None
    priority: Optional[int] = Field(None, ge=1, le=10)
    max_retries: Optional[int] = Field(None, ge=0, le=10)
    status: Optional[TaskStatus] = None
    model_config = ConfigDict(extra="ignore")


class TaskResponse(TaskBase):
    """Fields returned in task responses"""

    id: UUID
    user_id: UUID
    status: TaskStatus
    retry_count: int
    # result
    result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    # timing
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    # scheduling
    last_run_at: Optional[datetime] = None
    next_run_at: Optional[datetime] = None
    run_count: int
    # timestamps
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class TaskListResponse(BaseModel):
    """Response model for listing tasks"""

    tasks: list[TaskResponse]
    total: int
    page: int
    size: int
    pages: int


class TaskExecutionBase(BaseModel):
    """Base fields for task execution"""

    execution_method: Optional[ExecutionMethod] = None
    agent_id: Optional[str] = None


class TaskExecutionCreate(TaskExecutionBase):
    """Fields required to create a task execution"""

    task_id: UUID


class TaskExecutionResponse(TaskExecutionBase):
    """Fields returned in task execution responses"""

    id: UUID
    task_id: UUID
    status: TaskStatus
    # timing
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration_seconds: Optional[int] = None
    # result
    result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    # metrics
    items_processed: Optional[int] = None
    bytes_transferred: Optional[int] = None
    # timestamps
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class TaskLogBase(BaseModel):
    """Base fields for task log"""

    level: str = Field(..., pattern="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$")
    message: str
    component: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class TaskLogCreate(TaskLogBase):
    """Fields required to create a task log"""

    task_id: UUID
    execution_id: Optional[UUID] = None


class TaskLogResponse(TaskLogBase):
    """Fields returned in task log responses"""

    id: UUID
    task_id: UUID
    execution_id: Optional[UUID] = None
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)


class TaskStatsResponse(BaseModel):
    """Response model for task statistics"""

    total_tasks: int
    pending_tasks: int
    running_tasks: int
    completed_tasks: int
    failed_tasks: int
    # by type
    one_time_tasks: int
    scheduled_tasks: int
    recurring_tasks: int
    # performance
    avg_duration_seconds: Optional[float] = None
    success_rate: Optional[float] = None


class TaskExecutionRequest(BaseModel):
    """Request model for executing a task"""

    force: bool = Field(default=False)


class TaskCancelRequest(BaseModel):
    """Request model for canceling a task"""

    reason: Optional[str] = None


class TaskRetryRequest(BaseModel):
    """Request model for retrying a task"""

    reset_retry_count: bool = Field(default=False)
