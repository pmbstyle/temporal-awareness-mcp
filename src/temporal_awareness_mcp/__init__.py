"""Temporal Awareness MCP Server

A robust MCP server that provides temporal awareness and time calculation abilities.
Built with the official Python MCP SDK following 2025 best practices.
"""

__version__ = "0.1.0"

from .server import create_server

__all__ = ["create_server", "__version__"]