#!/usr/bin/env python3
"""HTTP entry point for Temporal Awareness MCP server."""

import asyncio
import argparse
from .server import create_server


async def main():
    parser = argparse.ArgumentParser(description="Temporal Awareness MCP Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    
    args = parser.parse_args()
    
    server = create_server()
    await server.run_sse(host=args.host, port=args.port)


if __name__ == "__main__":
    asyncio.run(main())