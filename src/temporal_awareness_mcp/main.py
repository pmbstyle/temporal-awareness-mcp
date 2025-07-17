"""
This file contains the main server application.
It will initialize the FastMCP instance and register the tools.
"""
from fastmcp import FastMCP

from .tools import core, contextual
from . import models

mcp = FastMCP(
    name="Temporal Awareness MCP",
    instructions="You have access to a suite of powerful and reliable tools for understanding "
                 "and calculating time. Use them to provide accurate, context-aware "
                 "responses to any time-related queries.",
)


@mcp.tool
def get_current_time(
    input_data: models.GetCurrentTimeInput,
) -> models.GetCurrentTimeOutput:
    """Returns the current date and time in a specified timezone."""
    return core.get_current_time(input_data)


@mcp.tool
def calculate_difference(
    input_data: models.CalculateDifferenceInput,
) -> models.CalculateDifferenceOutput:
    """Calculates the duration between two timestamps."""
    return core.calculate_difference(input_data)


@mcp.tool
def get_timestamp_context(
    input_data: models.GetTimestampContextInput,
) -> models.GetTimestampContextOutput:
    """Provides human-readable context about a specific timestamp."""
    return contextual.get_timestamp_context(input_data)

@mcp.tool
def get_timestamp_context(
    input_data: models.GetTimestampContextInput,
) -> models.GetTimestampContextOutput:
    """Provides human-readable context about a specific timestamp."""
    return contextual.get_timestamp_context(input_data)


@mcp.tool
def adjust_timestamp(
    input_data: models.AdjustTimestampInput,
) -> models.AdjustTimestampOutput:
    """Adds or subtracts a duration from a given timestamp."""
    return core.adjust_timestamp(input_data)
