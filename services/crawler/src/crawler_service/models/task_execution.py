from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

from crawler_service.models.base import Base
from crawler_service.models.enum import ExecutionMethod, TaskStatus
from sqlalchemy import UUID as PG_UUID
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import ENUM, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .task import Task
    from .task_log import TaskLog


class TaskExecution(Base):
    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uuid4,
    )
    # Foreign keys
    task_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("task.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    # Execution details
    execution_method: Mapped[ExecutionMethod] = mapped_column(
        ENUM(ExecutionMethod, name="execution_method"), nullable=False
    )
    agent_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    # Status
    status: Mapped[TaskStatus] = mapped_column(
        ENUM(TaskStatus, name="task_status"),
        nullable=False,
        default=TaskStatus.PENDING,
    )
    # Timing
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    duration_seconds: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # in seconds
    # Result
    result: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    # Logs
    stdout: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    stderr: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    # Metrics
    items_processed: Mapped[int] = mapped_column(Integer, default=0)
    bytes_transferred: Mapped[int] = mapped_column(Integer, default=0)
    # Relationships
    task: Mapped["Task"] = relationship("Task", back_populates="executions")
    logs: Mapped[list["TaskLog"]] = relationship("TaskLog", back_populates="execution", cascade="all, delete-orphan")
