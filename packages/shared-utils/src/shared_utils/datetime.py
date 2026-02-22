from datetime import datetime, timezone


def now(utc: bool = True) -> datetime:
    """Returns the current date and time.

    Args:
        utc (bool, optional): If True, returns the current date and time in UTC. Defaults to False.

    Returns:
        datetime: The current date and time.
    """

    if utc:
        return datetime.now(timezone.utc)
    return datetime.now()
