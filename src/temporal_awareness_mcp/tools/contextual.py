"""Contextual time analysis tools."""

from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from .. import models, utils


def get_timestamp_context(input_data: models.GetTimestampContextInput) -> models.GetTimestampContextOutput:
    try:
        dt = utils.robust_parse_datetime(input_data.timestamp, input_data.timezone)

        day_of_week = dt.strftime("%A")
        is_weekend = dt.weekday() >= 5
        is_business_hours = (
            not is_weekend and
            input_data.business_hours_start <= dt.hour < input_data.business_hours_end
        )

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