"""
Tests for the core calculation tools by calling the functions directly.
"""
import pytest
from datetime import datetime
from zoneinfo import ZoneInfo

from temporal_awareness_mcp.models import (
    GetCurrentTimeInput,
    CalculateDifferenceInput,
    AdjustTimestampInput,
)
from temporal_awareness_mcp.tools.core import (
    get_current_time,
    calculate_difference,
    adjust_timestamp,
)

def test_get_current_time_direct_utc():
    """
    Tests the get_current_time tool function directly with UTC.
    """
    test_input = GetCurrentTimeInput(timezone="UTC")
    result = get_current_time(test_input)
    assert result.timezone == "UTC"
    now_utc = datetime.now(ZoneInfo("UTC"))
    response_dt = datetime.fromisoformat(result.iso_timestamp)
    time_difference = abs((now_utc - response_dt).total_seconds())
    assert time_difference < 5


def test_get_current_time_direct_specific_timezone():
    """
    Tests the get_current_time tool function directly with a specific timezone.
    """
    timezone_str = "America/New_York"
    test_input = GetCurrentTimeInput(timezone=timezone_str)
    result = get_current_time(test_input)
    assert result.timezone == timezone_str
    now_tz = datetime.now(ZoneInfo(timezone_str))
    response_dt = datetime.fromisoformat(result.iso_timestamp)
    time_difference = abs((now_tz - response_dt).total_seconds())
    assert time_difference < 5


def test_calculate_difference_simple():
    """Tests a simple time difference calculation."""
    test_input = CalculateDifferenceInput(
        start_timestamp="2024-01-01 10:00:00",
        end_timestamp="2024-01-01 12:30:15",
    )
    result = calculate_difference(test_input)
    assert result.total_seconds == 9015
    assert result.is_negative is False
    assert result.formatted_duration == "2 hours, 30 minutes, 15 seconds"


def test_calculate_difference_negative():
    """Tests a negative (reversed) time difference calculation."""
    test_input = CalculateDifferenceInput(
        start_timestamp="2024-01-01 12:30:15",
        end_timestamp="2024-01-01 10:00:00",
    )
    result = calculate_difference(test_input)
    assert result.total_seconds == -9015
    assert result.is_negative is True
    assert result.formatted_duration == "2 hours, 30 minutes, 15 seconds"


def test_calculate_difference_spanning_days():
    """Tests a time difference that spans multiple days."""
    test_input = CalculateDifferenceInput(
        start_timestamp="2024-03-10 20:00:00",
        end_timestamp="2024-03-12 10:00:00",
    )
    result = calculate_difference(test_input)
    assert result.total_seconds == 136800
    assert result.is_negative is False
    assert result.formatted_duration == "1 day, 14 hours"



def test_adjust_timestamp_add_days():
    """Tests adding days to a timestamp."""
    test_input = AdjustTimestampInput(
        start_timestamp="2024-07-20 12:00:00",
        delta_value=5,
        delta_unit="days",
    )
    result = adjust_timestamp(test_input)
    assert result.adjusted_timestamp_iso == "2024-07-25T12:00:00+00:00"

def test_adjust_timestamp_subtract_hours():
    """Tests subtracting hours from a timestamp."""
    test_input = AdjustTimestampInput(
        start_timestamp="2024-07-20 10:00:00",
        delta_value=-3.5,
        delta_unit="hours",
    )
    result = adjust_timestamp(test_input)
    assert result.adjusted_timestamp_iso == "2024-07-20T06:30:00+00:00"

def test_adjust_timestamp_add_weeks_and_change_timezone():
    """Tests adding weeks in a specific timezone."""
    test_input = AdjustTimestampInput(
        start_timestamp="2025-01-01 00:00:00",
        delta_value=2,
        delta_unit="weeks",
        timezone="America/Los_Angeles"
    )
    result = adjust_timestamp(test_input)
    assert result.adjusted_timestamp_iso == "2025-01-15T00:00:00-08:00"