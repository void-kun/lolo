from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, Optional
from uuid import UUID

from crawler_service.models.base import Base
from crawler_service.models.enum import ExecutionMethod, TaskStatus, TaskType
from sqlalchemy import UUID as PG_UUID
from sqlalchemy import DateTime, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import ENUM, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .task_execution import TaskExecution
    from .task_log import TaskLog


class Task(Base):
    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, index=True)
    user_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False, index=True)
    # Task details
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    # Task configuration
    task_type: Mapped[TaskType] = mapped_column(ENUM(TaskType, name="task_type"), nullable=False, index=True)
    execution_method: Mapped[ExecutionMethod] = mapped_column(
        ENUM(ExecutionMethod, name="execution_method"), nullable=False
    )
    # Configuration (JSON)
    config: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)
    schedule_config: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True, default=dict)
    # Status
    status: Mapped[TaskStatus] = mapped_column(
        ENUM(TaskStatus, name="task_status"),
        nullable=False,
        index=True,
        default=TaskStatus.PENDING,
    )
    priority: Mapped[int] = mapped_column(Integer, default=0, index=True)
    # Retry configuration
    retry_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    max_retries: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    retry_delay: Mapped[int] = mapped_column(Integer, default=30, nullable=False)  # in seconds
    # Result and error information
    result: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    error_trace: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    # Timing
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    duration_seconds: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # in seconds
    # Scheduling
    last_run_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    next_run_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    run_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    # Relationships
    executions: Mapped[list["TaskExecution"]] = relationship(
        "TaskExecution",
        back_populates="task",
        cascade="all, delete-orphan",
    )
    logs: Mapped[list["TaskLog"]] = relationship(
        "TaskLog",
        back_populates="task",
        cascade="all, delete-orphan",
    )
    # Indexes
    __table_args__ = (
        Index("idx_task_user_status", "user_id", "status"),
        Index(
            "idx_task_next_run",
            "next_run_at",
            postgresql_where=(task_type != TaskType.ONE_TIME),
        ),
    )
