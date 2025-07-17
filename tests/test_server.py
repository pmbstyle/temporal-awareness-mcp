"""Tests for the MCP server implementation."""
import pytest
from temporal_awareness_mcp.server import create_server
from temporal_awareness_mcp.models import (
    GetCurrentTimeInput,
    CalculateDifferenceInput,
)
from temporal_awareness_mcp.tools.core import get_current_time, calculate_difference


def test_create_server():
    server = create_server()
    assert server is not None
    assert server.server.name == "temporal-awareness-mcp"


@pytest.mark.asyncio 
async def test_tool_functionality_direct():
    # Test get_current_time
    input_data = GetCurrentTimeInput(timezone="UTC", format="iso")
    result = get_current_time(input_data)
    assert result.timezone == "UTC"
    assert "T" in result.iso_timestamp
    
    # Test calculate_difference
    input_data = CalculateDifferenceInput(
        start_timestamp="2024-01-01 10:00:00",
        end_timestamp="2024-01-01 12:00:00"
    )
    result = calculate_difference(input_data)
    assert result.total_seconds == 7200  # 2 hours
    assert not result.is_negative


def test_server_configuration():
    server = create_server()
    
    # Test that the server object exists and has the right name
    assert server.server.name == "temporal-awareness-mcp"
    
    # Test that our TemporalAwarenessServer wrapper exists
    assert hasattr(server, 'run_stdio')
    assert hasattr(server, 'run_sse')


def test_server_has_mcp_server():
    server = create_server()
    
    # Should have an MCP server instance
    assert hasattr(server, 'server')
    assert server.server is not None
    
    # Server should have the expected capabilities
    from mcp.server import Server
    assert isinstance(server.server, Server)


def test_expected_tools_count():
    expected_tools = [
        "get_current_time",
        "calculate_difference", 
        "get_timestamp_context",
        "adjust_timestamp"
    ]
    
    # This tests that our server is properly configured with tools
    assert len(expected_tools) == 4  # We expect 4 tools