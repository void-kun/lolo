from sqlalchemy import UUID, Column, DateTime, Enum, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from crawler_service.models.base import Base
from crawler_service.models.enum import ExecutionMethod, TaskStatus, TaskType


class Task(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    # Task details
    name = Column(String(200), nullable=False)
    description = Column(Text)
    # Task configuration
    task_type = Column(Enum(TaskType), nullable=False, index=True)
    execution_method = Column(Enum(ExecutionMethod), nullable=False)
    # Configuration (JSON)
    config = Column(JSONB, nullable=False, default=dict)
    schedule_config = Column(JSONB, default=dict)
    # Status
    status = Column(
        Enum(TaskStatus),
        nullable=False,
        index=True,
        default=TaskStatus.PENDING,
    )
    priority = Column(Integer, default=0, index=True)
    # Retry configuration
    retry_count = Column(Integer, default=0, nullable=False)
    max_retries = Column(Integer, default=3, nullable=False)
    retry_delay = Column(Integer, default=60, nullable=False)  # in seconds
    # Result and error information
    result = Column(JSONB)
    error_message = Column(Text)
    error_trace = Column(Text)
    # Timing
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    duration_seconds = Column(Integer)  # in seconds
    # Scheduling
    last_run_at = Column(DateTime(timezone=True))
    next_run_at = Column(DateTime(timezone=True))
    run_count = Column(Integer, default=0)
    # Relationships
    executions = relationship(
        "TaskExecution",
        back_populates="task",
        cascade="all, delete-orphan",
    )
    logs = relationship(
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
