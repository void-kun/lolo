from sqlalchemy import UUID, Column, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from crawler_service.models.base import Base
from crawler_service.models.enum import TaskStatus


class TaskExecution(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    # Foreign keys
    task_id = Column(
        UUID(as_uuid=True),
        ForeignKey("task.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    # Execution details
    execution_method = Column(Enum(TaskStatus))
    agent_id = Column(String(100))
    # Status
    status = Column(
        Enum(TaskStatus),
        nullable=False,
        default=TaskStatus.PENDING,
    )
    # Timing
    started_at = Column(DateTime(timezone=True), nullable=False)
    completed_at = Column(DateTime(timezone=True))
    duration_seconds = Column(Integer)  # in seconds
    # Result
    result = Column(JSONB)
    error_message = Column(Text)
    # Logs
    stdout = Column(Text)
    stderr = Column(Text)
    # Metrics
    items_processed = Column(Integer, default=0)
    bytes_transferred = Column(Integer, default=0)
    # Relationships
    task = relationship("Task", back_populates="executions")
    logs = relationship(
        "TaskLog", back_populates="execution", cascade="all, delete-orphan"
    )
