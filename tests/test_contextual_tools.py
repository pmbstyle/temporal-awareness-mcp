"""
Tests for the contextual time tools.
"""
from temporal_awareness_mcp.models import GetTimestampContextInput
from temporal_awareness_mcp.tools.contextual import get_timestamp_context


def test_context_weekday_business_hours():
    """Tests a weekday during business hours."""
    # Monday, March 11, 2024 @ 10:30 AM
    test_input = GetTimestampContextInput(timestamp="2024-03-11 10:30:00")
    result = get_timestamp_context(test_input)

    assert result.day_of_week == "Monday"
    assert result.is_weekend is False
    assert result.is_business_hours is True
    assert result.time_of_day == "morning"

def test_context_weekday_evening():
    """Tests a weekday during the evening, outside business hours."""
    # Wednesday, March 13, 2024 @ 8:00 PM
    test_input = GetTimestampContextInput(timestamp="2024-03-13 20:00:00")
    result = get_timestamp_context(test_input)

    assert result.day_of_week == "Wednesday"
    assert result.is_weekend is False
    assert result.is_business_hours is False
    assert result.time_of_day == "evening"

def test_context_weekend():
    """Tests a weekend timestamp."""
    # Saturday, March 16, 2024 @ 2:00 PM
    test_input = GetTimestampContextInput(timestamp="2024-03-16 14:00:00")
    result = get_timestamp_context(test_input)

    assert result.day_of_week == "Saturday"
    assert result.is_weekend is True
    assert result.is_business_hours is False
    assert result.time_of_day == "afternoon"

def test_context_night():
    """Tests a timestamp that falls at night."""
    # Friday, March 15, 2024 @ 11:30 PM
    test_input = GetTimestampContextInput(timestamp="2024-03-15 23:30:00")
    result = get_timestamp_context(test_input)

    assert result.day_of_week == "Friday"
    assert result.is_weekend is False
    assert result.is_business_hours is False
    assert result.time_of_day == "night"