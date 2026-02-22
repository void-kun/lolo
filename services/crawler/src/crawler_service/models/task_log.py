from sqlalchemy import (
    UUID,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from crawler_service.models.base import Base


class TaskLog(Base):
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    # Foreign keys
    task_id = Column(
        UUID(as_uuid=True),
        ForeignKey("task.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    execution_id = Column(
        UUID(as_uuid=True),
        ForeignKey("task_execution.id", ondelete="CASCADE"),
        index=True,
    )
    # Log details
    level = Column(String(20), nullable=False)
    message = Column(Text, nullable=False)
    # Context
    component = Column(String(50))
    metadata_val = Column(JSONB)
    timestamp = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True,
    )
    # Relationships
    task = relationship("Task", back_populates="logs")
    execution = relationship("TaskExecution", back_populates="logs")
    # Indexes
    __table_args__ = (
        Index("idx_log_task_time", "task_id", "timestamp"),
        Index("idx_log_level_time", "level", "timestamp"),
    )
