from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from crawler_service.models.base import Base
from crawler_service.models.enum import AgentConnectionType, AgentStatus
from sqlalchemy import UUID as PG_UUID
from sqlalchemy import DateTime, Integer, String
from sqlalchemy.dialects.postgresql import ENUM, JSONB
from sqlalchemy.orm import Mapped, mapped_column


class Agent(Base):
    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uuid4,
    )
    # Basic information
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    # Connection
    endpoint: Mapped[str] = mapped_column(String(255), nullable=False)
    api_key: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    connection_type: Mapped[AgentConnectionType] = mapped_column(
        ENUM(AgentConnectionType, name="agent_connection_type"),
        default=AgentConnectionType.HTTP,
        nullable=False,
    )
    # Status
    status: Mapped[AgentStatus] = mapped_column(
        ENUM(AgentStatus, name="agent_status"),
        nullable=False,
        index=True,
        default=AgentStatus.OFFLINE,
    )
    # Capabilities
    capabilities: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
        default=dict,
    )
    # Health
    last_heartbeat: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), index=True, nullable=True)
    current_tasks: Mapped[int] = mapped_column(Integer, default=0)
    max_concurrent_tasks: Mapped[int] = mapped_column(Integer, default=1)
    # Stats
    total_tasks_completed: Mapped[int] = mapped_column(Integer, default=0)
    total_tasks_failed: Mapped[int] = mapped_column(Integer, default=0)
    avg_response_time_ms: Mapped[int] = mapped_column(Integer, default=0)
