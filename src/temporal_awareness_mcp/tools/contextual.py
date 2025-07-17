"""
This file contains tools that provide human context about time.
e.g., get_timestamp_context, parse_natural_language_time
"""
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from .. import models, utils


def get_timestamp_context(
    input_data: models.GetTimestampContextInput,
) -> models.GetTimestampContextOutput:
    """
    Provides human-readable context about a specific timestamp.
    """
    try:
        dt = utils.robust_parse_datetime(input_data.timestamp, input_data.timezone)

        # Day of week and weekend check
        # dt.weekday() -> Monday is 0 and Sunday is 6
        day_of_week = dt.strftime("%A")
        is_weekend = dt.weekday() >= 5  # Saturday or Sunday

        # Business hours check
        is_business_hours = (
            not is_weekend and
            input_data.business_hours_start <= dt.hour < input_data.business_hours_end
        )

        # Time of day check
        hour = dt.hour
        if 5 <= hour < 12:
            time_of_day = "morning"
        elif 12 <= hour < 17:
            time_of_day = "afternoon"
        elif 17 <= hour < 21:
            time_of_day = "evening"
        else:
            time_of_day = "night"

        return models.GetTimestampContextOutput(
            day_of_week=day_of_week,
            is_weekend=is_weekend,
            is_business_hours=is_business_hours,
            time_of_day=time_of_day,
        )

    except (ValueError, ZoneInfoNotFoundError) as e:
        raise e