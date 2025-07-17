"""
This file contains the core time calculation tools.
e.g., get_current_time, calculate_difference, adjust_timestamp
"""
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from .. import models, utils


def get_current_time(
    input_data: models.GetCurrentTimeInput,
) -> models.GetCurrentTimeOutput:
    """
    Returns the current date and time in a specified timezone.
    This is a foundational tool for establishing temporal awareness.
    """
    try:
        target_timezone = ZoneInfo(input_data.timezone)
        now = datetime.now(target_timezone)
        formatted_string = now.strftime("%A, %B %d, %Y at %I:%M %p")

        return models.GetCurrentTimeOutput(
            iso_timestamp=now.isoformat(),
            formatted_timestamp=formatted_string,
            timezone=str(target_timezone),
            day_of_week=now.strftime("%A"),
        )
    except ZoneInfoNotFoundError as e:
        raise ValueError(f"The specified timezone '{input_data.timezone}' is not valid.") from e


def _format_timedelta(duration: timedelta) -> str:
    """A helper to format a timedelta into a human-readable string."""
    seconds = abs(duration.total_seconds())
    days, remainder = divmod(seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    parts = []
    if days > 0:
        parts.append(f"{int(days)} day{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{int(hours)} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{int(minutes)} minute{'s' if minutes != 1 else ''}")
    if seconds > 0 or not parts:
        parts.append(f"{int(seconds)} second{'s' if seconds != 1 else ''}")

    return ", ".join(parts)


def calculate_difference(
    input_data: models.CalculateDifferenceInput,
) -> models.CalculateDifferenceOutput:
    """
    Calculates the duration between two timestamps.
    """
    try:
        start_dt = utils.robust_parse_datetime(
            input_data.start_timestamp, input_data.timezone
        )
        end_dt = utils.robust_parse_datetime(
            input_data.end_timestamp, input_data.timezone
        )

        difference = end_dt - start_dt
        total_seconds = difference.total_seconds()

        return models.CalculateDifferenceOutput(
            total_seconds=total_seconds,
            is_negative=total_seconds < 0,
            formatted_duration=_format_timedelta(difference),
        )
    except (ValueError, ZoneInfoNotFoundError) as e:
        raise e

def adjust_timestamp(
    input_data: models.AdjustTimestampInput,
) -> models.AdjustTimestampOutput:
    """
    Adds or subtracts a duration from a given timestamp.
    """
    try:
        start_dt = utils.robust_parse_datetime(
            input_data.start_timestamp, input_data.timezone
        )

        duration_args = {input_data.delta_unit: input_data.delta_value}
        duration = timedelta(**duration_args)

        adjusted_dt = start_dt + duration

        return models.AdjustTimestampOutput(
            original_timestamp_iso=start_dt.isoformat(),
            adjusted_timestamp_iso=adjusted_dt.isoformat(),
        )
    except (ValueError, ZoneInfoNotFoundError) as e:
        raise e