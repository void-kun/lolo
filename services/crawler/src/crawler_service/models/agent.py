from sqlalchemy import UUID, Column, DateTime, Enum, Integer, String
from sqlalchemy.dialects.postgresql import JSONB

from crawler_service.models.base import Base
from crawler_service.models.enum import AgentConnectionType, AgentStatus


class Agent(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    # Basic information
    name = Column(String(100), nullable=False, unique=True)
    # Connection
    endpoint = Column(String(255), nullable=False)
    api_key = Column(String(255))
    connection_type = Column(
        Enum(AgentConnectionType),
        default=AgentConnectionType.HTTP,
        nullable=False,
    )
    # Status
    status = Column(
        Enum(AgentStatus),
        default=AgentStatus.OFFLINE,
        nullable=False,
        index=True,
    )
    # Capabilities
    capabilities = Column(JSONB, default=dict)
    # Health
    last_heartbeat = Column(DateTime(timezone=True), index=True)
    current_tasks = Column(Integer, default=0)
    max_concurrent_tasks = Column(Integer, default=1)
    # Stats
    total_tasks_completed = Column(Integer, default=0)
    total_tasks_failed = Column(Integer, default=0)
    avg_response_time_ms = Column(Integer, default=0)
