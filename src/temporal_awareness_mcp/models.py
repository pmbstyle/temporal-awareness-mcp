"""Pydantic models for temporal awareness tools."""

from pydantic import BaseModel, Field
from typing import Literal


class GetCurrentTimeInput(BaseModel):
    timezone: str = Field(
        default="UTC",
        description="The IANA timezone name for which to get the current time. e.g., 'America/New_York', 'Europe/London'."
    )


class GetCurrentTimeOutput(BaseModel):
    iso_timestamp: str = Field(description="The full timestamp in ISO 8601 format.")
    formatted_timestamp: str = Field(description="A human-friendly formatted timestamp, e.g., 'July 20, 2024 at 10:30 AM'.")
    timezone: str = Field(description="The timezone used for the calculation.")
    day_of_week: str = Field(description="The full name of the day of the week, e.g., 'Saturday'.")


class CalculateDifferenceInput(BaseModel):
    start_timestamp: str = Field(description="The earlier timestamp in any common format.")
    end_timestamp: str = Field(description="The later timestamp in any common format.")
    timezone: str = Field(
        default="UTC",
        description="The IANA timezone to use for parsing if the timestamps are ambiguous."
    )


class CalculateDifferenceOutput(BaseModel):
    total_seconds: float = Field(description="The total difference in seconds. Can be negative.")
    is_negative: bool = Field(description="True if the start_timestamp is after the end_timestamp.")
    formatted_duration: str = Field(description="A human-friendly string representing the duration, e.g., '2 days, 3 hours, 45 minutes'.")

class GetTimestampContextInput(BaseModel):
    timestamp: str = Field(description="The timestamp to analyze, in any common format.")
    timezone: str = Field(
        default="UTC",
        description="The IANA timezone to use for context (e.g., 'America/New_York')."
    )
    business_hours_start: int = Field(
        default=9,
        description="The start hour (0-23) for business hours.",
        ge=0, le=23
    )
    business_hours_end: int = Field(
        default=17,
        description="The end hour (0-23) for business hours.",
        ge=0, le=23
    )


class GetTimestampContextOutput(BaseModel):
    day_of_week: str = Field(description="The full name of the day of the week.")
    is_weekend: bool = Field(description="True if the day is a Saturday or Sunday.")
    is_business_hours: bool = Field(description="True if the time falls within defined business hours on a weekday.")
    time_of_day: str = Field(description="A label for the time of day, e.g., 'morning', 'afternoon', 'evening', 'night'.")

class AdjustTimestampInput(BaseModel):
    start_timestamp: str = Field(description="The starting timestamp in any common format.")
    delta_value: float = Field(description="The value of the duration to add or subtract.")
    delta_unit: Literal["weeks", "days", "hours", "minutes", "seconds"] = Field(
        description="The unit of the duration."
    )
    timezone: str = Field(
        default="UTC",
        description="The IANA timezone to use for parsing if the timestamp is ambiguous."
    )


class AdjustTimestampOutput(BaseModel):
    original_timestamp_iso: str = Field(description="The original timestamp in ISO 8601 format.")
    adjusted_timestamp_iso: str = Field(description="The resulting new timestamp in ISO 8601 format.")