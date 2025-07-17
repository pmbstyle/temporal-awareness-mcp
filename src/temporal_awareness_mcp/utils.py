"""Utility functions for temporal parsing."""

from datetime import datetime
from dateutil import parser
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


def robust_parse_datetime(timestamp_str: str, tz_str: str = "UTC") -> datetime:
    try:
        dt_naive = parser.parse(timestamp_str, ignoretz=True)
        
        tz = ZoneInfo(tz_str)
        
        return dt_naive.replace(tzinfo=tz)

    except parser.ParserError as e:
        raise ValueError(f"Could not parse the timestamp string: '{timestamp_str}'") from e
    except ZoneInfoNotFoundError as e:
        raise ValueError(f"The specified timezone '{tz_str}' is not a valid IANA timezone.") from e