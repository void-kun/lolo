from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from crawler_service.models.enum import AgentConnectionType, AgentStatus


class AgentBase(BaseModel):
    """Base agent fields"""

    name: str = Field(..., min_length=1, max_length=100)
    endpoint: str = Field(..., min_length=1, max_length=255)
    connection_type: AgentConnectionType
    capabilities: Dict[str, Any] = Field(default_factory=dict)
    max_concurrent_tasks: int = Field(default=1, ge=1, le=10)

    @field_validator("endpoint")
    @classmethod
    def validate_endpoint(cls, v: str) -> str:
        if not v:
            raise ValueError("endpoint must be a non-empty string")

        if "://" in v:
            if not (
                v.startswith("http://") or v.startswith("https://")
            ) or v.startswith("grpc://"):
                raise ValueError(
                    "endpoint should start with http:// or https:// or grpc:// if it contains a scheme"
                )

        return v

    @field_validator("capabilities")
    @classmethod
    def validate_capabilities(cls, v: Dict[str, Any]) -> Dict[str, Any]:
        if "max_concurrent_tasks" in v and not isinstance(
            v["max_concurrent_tasks"], int
        ):
            raise ValueError("capabilities.max_concurrent_tasks must be an integer")
        return v


class AgentCreate(AgentBase):
    """Fields required to create an agent"""

    api_key: Optional[str] = Field(None)


class AgentUpdate(BaseModel):
    """Fields allowed to update in an agent"""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    endpoint: Optional[str] = Field(None, min_length=1, max_length=255)
    connection_type: Optional[AgentConnectionType] = None
    capabilities: Optional[Dict[str, Any]] = None
    max_concurrent_tasks: Optional[int] = Field(None, ge=1, le=10)
    api_key: Optional[str] = Field(None)
    status: Optional[AgentStatus] = None
    model_config = ConfigDict(extra="ignore")


class AgentResponse(AgentBase):
    """Schema for agent response"""

    id: UUID
    status: AgentStatus
    # Health
    last_heartbeat: Optional[datetime] = None
    current_tasks: int
    # Stats
    total_tasks_completed: int
    total_tasks_failed: int
    avg_response_time_ms: Optional[float] = None
    # Timestamps
    created_at: datetime
    updated_at: datetime
    api_key: Optional[str] = Field(None, exclude=True)
    model_config = ConfigDict(from_attributes=True)


class AgentListResponse(BaseModel):
    """Response model for listing agents"""

    agents: list[AgentResponse]
    total: int
    page: int
    size: int
    pages: int


class AgentHeartbeatRequest(BaseModel):
    """Schema for agent heartbeat request"""

    current_tasks: Optional[int] = Field(None, ge=0)
    status: Optional[AgentStatus] = None
    metrics: Optional[Dict[str, Any]] = Field(None)


class AgentHeartbeatResponse(BaseModel):
    """Schema for agent heartbeat response"""

    success: bool
    message: Optional[str] = None
    next_heartbeat_in_seconds: int = Field(default=30)


class AgentStatsResponse(BaseModel):
    """Schema for agent stats response"""

    total_agents: int
    online_agents: int
    offline_agents: int
    busy_agents: int
    # Performance metrics
    total_tasks_processed: int
    avg_response_time_ms: Optional[float] = None
    grpc_agents: int
    http_agents: int


class AgentCapabilitiesUpdate(BaseModel):
    """Schema for updating agent capabilities"""

    capabilities: Dict[str, Any] = Field(default_factory=dict)


class AgentTaskAssignment(BaseModel):
    """Schema for assigning a task to an agent"""

    task_id: UUID
    agent_id: Optional[UUID] = None
    model_config = ConfigDict(from_attributes=True)


class AgentHealthCheckRequest(BaseModel):
    """Schema for agent health check request"""

    timeout_seconds: int = Field(default=5, ge=1, le=30)


class AgentHealthCheckResponse(BaseModel):
    """Schema for agent health check response"""

    agent_id: UUID
    healthy: bool
    response_time_ms: Optional[int] = None
    error: Optional[str] = None
    checked_at: datetime
