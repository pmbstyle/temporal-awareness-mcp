"""
This file contains shared utility functions,
such as the robust timestamp parser, that can be used
across different parts of the application.
"""
from datetime import datetime
from dateutil import parser
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


def robust_parse_datetime(timestamp_str: str, tz_str: str = "UTC") -> datetime:
    """
    Parses a wide variety of timestamp strings into a timezone-aware datetime object.

    This function is designed to be the single source of truth for parsing time-related
    strings throughout the application.

    Args:
        timestamp_str: The string representation of the timestamp (e.g., "2024-07-20 10:00:00",
                       "next Tuesday at 5pm").
        tz_str: The IANA timezone name (e.g., "UTC", "America/New_York") to apply to the
                parsed timestamp.

    Returns:
        A timezone-aware datetime object.

    Raises:
        ValueError: If the timestamp string cannot be parsed or if the timezone is unknown.
    """
    try:
        dt_naive = parser.parse(timestamp_str, ignoretz=True)
        
        tz = ZoneInfo(tz_str)
        
        return dt_naive.replace(tzinfo=tz)

    except parser.ParserError as e:
        raise ValueError(f"Could not parse the timestamp string: '{timestamp_str}'") from e
    except ZoneInfoNotFoundError as e:
        raise ValueError(f"The specified timezone '{tz_str}' is not a valid IANA timezone.") from e