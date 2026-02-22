from crawler_service.core.config import get_settings
from shared_utils.logging import Logger, setup_logger

settings = get_settings()


logger: Logger = setup_logger(
    service_name=settings.SERVICE_NAME,
    log_level=settings.LOG_LEVEL,
    log_dir=settings.LOG_DIR,
)
