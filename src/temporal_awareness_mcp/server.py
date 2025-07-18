"""Temporal Awareness MCP Server implementation."""

from typing import Any
from mcp.server import Server
from mcp.types import Tool, ServerCapabilities, ToolsCapability

from .tools import core, contextual
from . import models


class TemporalAwarenessServer:
    """Temporal awareness MCP server."""

    def __init__(self):
        self.server = Server("temporal-awareness-mcp")
        self._setup_handlers()

    def _setup_handlers(self):
        
        @self.server.list_tools()
        async def handle_list_tools() -> list[Tool]:
            return [
                Tool(
                    name="get_current_time",
                    description="Returns the current date and time in a specified timezone",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "timezone": {
                                "type": "string",
                                "description": "Timezone name (e.g., 'UTC', 'US/Pacific', 'Europe/London')",
                                "default": "UTC"
                            },
                            "format": {
                                "type": "string", 
                                "description": "Output format ('iso', 'human', 'timestamp')",
                                "default": "iso"
                            }
                        }
                    }
                ),
                Tool(
                    name="calculate_difference",
                    description="Calculates the duration between two timestamps",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "start_timestamp": {
                                "type": "string",
                                "description": "Start timestamp (ISO format or human readable)"
                            },
                            "end_timestamp": {
                                "type": "string", 
                                "description": "End timestamp (ISO format or human readable)"
                            },
                            "timezone": {
                                "type": "string",
                                "description": "Timezone for parsing ambiguous timestamps",
                                "default": "UTC"
                            }
                        },
                        "required": ["start_timestamp", "end_timestamp"]
                    }
                ),
                Tool(
                    name="get_timestamp_context",
                    description="Provides human-readable context about a specific timestamp",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "timestamp": {
                                "type": "string",
                                "description": "Timestamp to analyze (ISO format or human readable)"
                            },
                            "timezone": {
                                "type": "string",
                                "description": "Timezone for context (e.g., 'UTC', 'US/Pacific')",
                                "default": "UTC"
                            }
                        },
                        "required": ["timestamp"]
                    }
                ),
                Tool(
                    name="adjust_timestamp",
                    description="Adds or subtracts a duration from a given timestamp",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "start_timestamp": {
                                "type": "string",
                                "description": "Base timestamp (ISO format or human readable)"
                            },
                            "delta_value": {
                                "type": "number",
                                "description": "The value of the duration to add or subtract"
                            },
                            "delta_unit": {
                                "type": "string",
                                "enum": ["weeks", "days", "hours", "minutes", "seconds"],
                                "description": "The unit of the duration"
                            },
                            "timezone": {
                                "type": "string",
                                "description": "Timezone for calculation",
                                "default": "UTC"
                            }
                        },
                        "required": ["start_timestamp", "delta_value", "delta_unit"]
                    }
                )
            ]

        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: dict[str, Any] | None) -> list[Any]:
            if arguments is None:
                arguments = {}

            try:
                if name == "get_current_time":
                    input_data = models.GetCurrentTimeInput(**arguments)
                    result = core.get_current_time(input_data)
                    if hasattr(arguments, 'format') and arguments.get('format') == 'human':
                        return [{"type": "text", "text": result.formatted_timestamp}]
                    else:
                        return [{"type": "text", "text": result.iso_timestamp}]
                
                elif name == "calculate_difference":
                    input_data = models.CalculateDifferenceInput(**arguments)
                    result = core.calculate_difference(input_data)
                    return [{"type": "text", "text": result.formatted_duration}]
                
                elif name == "get_timestamp_context":
                    input_data = models.GetTimestampContextInput(**arguments)
                    result = contextual.get_timestamp_context(input_data)
                    context_info = f"Day: {result.day_of_week}, Weekend: {result.is_weekend}, Business Hours: {result.is_business_hours}, Time of Day: {result.time_of_day}"
                    return [{"type": "text", "text": context_info}]
                
                elif name == "adjust_timestamp":
                    input_data = models.AdjustTimestampInput(**arguments)
                    result = core.adjust_timestamp(input_data)
                    return [{"type": "text", "text": f"Original: {result.original_timestamp_iso}, Adjusted: {result.adjusted_timestamp_iso}"}]
                
                else:
                    raise ValueError(f"Unknown tool: {name}")
                    
            except Exception as e:
                return [{"type": "text", "text": f"Error: {str(e)}"}]

    async def run_stdio(self):
        from mcp.server.stdio import stdio_server
        from mcp.server.models import InitializationOptions
        
        async with stdio_server(self.server) as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="temporal-awareness-mcp",
                    server_version="0.1.0",
                ),
            )

    async def run_sse(self, host: str = "localhost", port: int = 8000):
        from mcp.server.sse import SseServerTransport
        from mcp.server.models import InitializationOptions
        from starlette.applications import Starlette
        from starlette.responses import Response
        from starlette.routing import Mount, Route
        import uvicorn
        
        sse = SseServerTransport("/messages/")
        
        async def handle_sse(request):
            async with sse.connect_sse(
                request.scope, request.receive, request._send
            ) as streams:
                await self.server.run(
                    streams[0], streams[1],
                    InitializationOptions(
                        server_name="temporal-awareness-mcp",
                        server_version="0.1.0",
                        capabilities=ServerCapabilities(
                            tools=ToolsCapability()
                        ),
                    ),
                )
            return Response()
        
        app = Starlette(
            routes=[
                Route("/sse", endpoint=handle_sse, methods=["GET"]),
                Mount("/messages/", app=sse.handle_post_message),
            ],
        )
        
        config = uvicorn.Config(app, host=host, port=port)
        server = uvicorn.Server(config)
        await server.serve()


def create_server() -> TemporalAwarenessServer:
    return TemporalAwarenessServer()