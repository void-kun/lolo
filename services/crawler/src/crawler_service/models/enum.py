from enum import StrEnum


class TaskType(StrEnum):
    ONE_TIME = "one_time"
    RECURRING = "recurring"
    SCHEDULED = "scheduled"


class TaskStatus(StrEnum):
    PENDING = "pending"
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELED = "canceled"
    RETRYING = "retrying"


class ExecutionMethod(StrEnum):
    SCRIPT = "script"
    AGENT_GRPC = "agent_grpc"
    AGENT_HTTP = "agent_http"
    DIRECT = "direct"


class AgentStatus(StrEnum):
    ONLINE = "online"
    OFFLINE = "offline"
    BUSY = "busy"
    ERROR = "error"


class AgentConnectionType(StrEnum):
    GRPC = "grpc"
    HTTP = "http"
