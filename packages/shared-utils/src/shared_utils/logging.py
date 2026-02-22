import sys
from pathlib import Path

from loguru import Logger, logger


def setup_logger(
    service_name: str, log_level: str = "INFO", log_dir: str = "logs"
) -> Logger:
    """
    Sets up a logger for a given service.
    Args:
        service_name (str): Name of the service (e.g., "crawler", "api").
        log_level (str): Logging level (e.g., "DEBUG", "INFO", "ERROR").
        log_dir (str): Directory where log files will be stored.
    Returns:
        loguru.Logger: Configured logger instance.
    """
    # Remove default logger
    logger.remove()
    Path(log_dir).mkdir(parents=True, exist_ok=True)

    # Add console logger
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{extra[service]}</cyan> | <level>{message}</level>",
        level=log_level,
        colorize=True,
        filter=lambda record: record["extra"].get("service") == service_name,
    )

    # Add file logger (all logs)
    logger.add(
        f"{log_dir}/{service_name}_{{time:YYYY-MM-DD}}.json",
        format="{time} {level} {message}",
        level=log_level,
        rotation="00:00",
        retention="30 days",
        compression="zip",
        serialize=True,
        enqueue=True,
        backtrace=True,
        diagnose=True,
    )

    # Add file logger for errors only
    logger.add(
        f"{log_dir}/{service_name}_errors_{{time:YYYY-MM-DD}}.json",
        format="{time} {level} {message}",
        level="ERROR",
        rotation="00:00",
        retention="90 days",
        compression="zip",
        serialize=True,
        enqueue=True,
        backtrace=True,
        diagnose=True,
    )

    return logger.bind(service=service_name)
