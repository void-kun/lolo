from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from crawler_service.models.base import Base
from sqlalchemy import UUID as PG_UUID
from sqlalchemy import (
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .task import Task
    from .task_execution import TaskExecution


class TaskLog(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    # Foreign keys
    task_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("task.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    execution_id: Mapped[Optional[UUID]] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("task_execution.id", ondelete="CASCADE"),
        index=True,
    )
    # Log details
    level: Mapped[str] = mapped_column(String(20), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    # Context
    component: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    metadata_val: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True,
    )
    # Relationships
    task: Mapped["Task"] = relationship("Task", back_populates="logs")
    execution: Mapped["TaskExecution"] = relationship("TaskExecution", back_populates="logs")
    # Indexes
    __table_args__ = (
        Index("idx_log_task_time", "task_id", "timestamp"),
        Index("idx_log_level_time", "level", "timestamp"),
    )
