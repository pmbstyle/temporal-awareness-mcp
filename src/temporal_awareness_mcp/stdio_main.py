#!/usr/bin/env python3
"""Stdio entry point for Temporal Awareness MCP server."""

import asyncio
import mcp.server.stdio
from mcp.server.models import InitializationOptions
from mcp.types import ServerCapabilities, ToolsCapability

from .server import create_server


async def main():
    temporal_server = create_server()
    
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await temporal_server.server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="temporal-awareness-mcp",
                server_version="0.1.0",
                capabilities=ServerCapabilities(
                    tools=ToolsCapability()
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())