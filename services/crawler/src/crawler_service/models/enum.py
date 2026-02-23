from enum import StrEnum


class TaskType(StrEnum):
    ONE_TIME = "ONE_TIME"
    RECURRING = "RECURRING"
    SCHEDULED = "SCHEDULED"


class TaskStatus(StrEnum):
    PENDING = "PENDING"
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELED = "CANCELED"
    RETRYING = "RETRYING"


class ExecutionMethod(StrEnum):
    SCRIPT = "SCRIPT"
    AGENT_GRPC = "AGENT_GRPC"
    AGENT_HTTP = "AGENT_HTTP"
    DIRECT = "DIRECT"


class AgentStatus(StrEnum):
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"
    BUSY = "BUSY"
    ERROR = "ERROR"


class AgentConnectionType(StrEnum):
    GRPC = "GRPC"
    HTTP = "HTTP"
