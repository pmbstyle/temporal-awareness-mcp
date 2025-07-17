# Temporal Awareness MCP Server

A Model Context Protocol (MCP) server that provides AI agents with comprehensive temporal awareness and time calculation capabilities.

## Features

- **Current Time**: Get current date and time in any timezone
- **Time Calculations**: Calculate differences between timestamps
- **Time Adjustments**: Add or subtract durations from timestamps  
- **Contextual Analysis**: Get human-readable context about timestamps
- **Multiple Transports**: Support for both stdio (local) and HTTP (remote) connections
- **Docker Support**: Ready for cloud deployment

## Quick Start

### For Local Development (Claude Desktop, Cursor)

1. **Install dependencies**:
   ```bash
   git clone https://github.com/pmbstyle/temporal-awareness-mcp.git
   cd temporal-awareness-mcp
   poetry install
   ```

2. **Run with stdio transport**:
   ```bash
   poetry run python -m temporal_awareness_mcp.stdio_main
   ```

### For Cloud Deployment

1. **Run with Docker**:
   ```bash
   docker-compose up -d --build
   ```

2. **Or run directly with HTTP transport**:
   ```bash
   poetry run python -m temporal_awareness_mcp.http_main --host 0.0.0.0 --port 8000
   ```

## Integration Guide

### Claude Desktop

Add to your Claude Desktop configuration file:

**For Windows:**
```json
{
  "mcpServers": {
    "temporal-awareness": {
      "command": "cmd",
      "args": ["/c", "cd /d \"C:\\path\\to\\temporal-awareness-mcp\" && poetry run python -m temporal_awareness_mcp.stdio_main"],
      "env": {}
    }
  }
}
```

**For macOS/Linux:**
```json
{
  "mcpServers": {
    "temporal-awareness": {
      "command": "sh",
      "args": ["-c", "cd '/path/to/temporal-awareness-mcp' && poetry run python -m temporal_awareness_mcp.stdio_main"],
      "env": {}
    }
  }
}
```

> **Important**: Replace `/path/to/temporal-awareness-mcp` with your actual project directory.

**Alternative: Using Python with PYTHONPATH**

If you prefer not to use Poetry:

```json
{
  "mcpServers": {
    "temporal-awareness": {
      "command": "python",
      "args": ["-m", "temporal_awareness_mcp.stdio_main"],
      "env": {
        "PYTHONPATH": "/path/to/temporal-awareness-mcp/src"
      }
    }
  }
}
```

### Cursor IDE

Configure in Cursor Settings > Extensions > MCP:

```json
{
  "servers": {
    "temporal-awareness": {
      "command": "poetry",
      "args": ["run", "python", "-m", "temporal_awareness_mcp.stdio_main"],
      "cwd": "/path/to/temporal-awareness-mcp"
    }
  }
}
```

### OpenAI and Cloud Clients

For cloud-based AI services, deploy the server and use HTTP transport:

1. **Deploy with ngrok (development)**:
   ```bash
   # Terminal 1: Start the server
   docker-compose up -d --build
   
   # Terminal 2: Expose with ngrok
   ngrok http 8000
   ```

2. **Use the public URL in your MCP client**:
   ```json
   {
     "type": "mcp",
     "server_label": "temporal-awareness",
     "server_url": "https://your-ngrok-url.ngrok.app/sse",
     "require_approval": "never"
   }
   ```

3. **Production deployment**: Deploy to Railway, Heroku, Google Cloud Run, etc.

## Available Tools

### `get_current_time`
Get the current date and time in a specified timezone.

**Parameters:**
- `timezone` (string, optional): Timezone name (default: "UTC")
- `format` (string, optional): Output format - "iso", "human", or "timestamp" (default: "iso")

**Example:**
```
What time is it in Tokyo?
```

### `calculate_difference`
Calculate the duration between two timestamps.

**Parameters:**
- `start_time` (string): Start timestamp (ISO format or human readable)
- `end_time` (string): End timestamp (ISO format or human readable)
- `unit` (string, optional): Result unit - "seconds", "minutes", "hours", or "days" (default: "seconds")

**Example:**
```
How long is it from 9:00 AM to 5:30 PM?
```

### `get_timestamp_context`
Provide human-readable context about a timestamp.

**Parameters:**
- `timestamp` (string): Timestamp to analyze
- `timezone` (string, optional): Timezone for context (default: "UTC")

**Example:**
```
Is March 15, 2024 2:30 PM a business day?
```

### `adjust_timestamp`
Add or subtract a duration from a timestamp.

**Parameters:**
- `timestamp` (string): Base timestamp
- `adjustment` (string): Adjustment to apply (e.g., "+1 day", "-2 hours")
- `timezone` (string, optional): Timezone for calculation (default: "UTC")

**Example:**
```
What date is 30 days after March 1, 2024?
```

## Testing the Server

Try these example prompts with your AI agent:

### Basic Operations
- "What time is it right now?"
- "What's the current time in Tokyo?"
- "Convert 3:30 PM EST to Pacific Time"

### Date Calculations
- "How many days until Christmas?"
- "What day of the week was January 1st, 2000?"
- "Add 45 days to March 15, 2024"

### Complex Scenarios
- "I have a flight departing Los Angeles at 11:30 PM on Friday. If the flight is 14 hours long, what time will I arrive in Tokyo local time?"
- "Calculate work hours in February 2024, assuming 8-hour workdays Monday through Friday"

## Development

### Prerequisites

- Python 3.12+
- Poetry for dependency management
- Docker (optional, for containerized deployment)

### Setup

```bash
# Clone and install
git clone <repository-url>
cd temporal-awareness-mcp
poetry install

# Run tests
poetry run pytest
```

## Deployment

### Docker

```bash
# Build and run
docker-compose up -d --build

# Check logs
docker-compose logs temporal-awareness-mcp-server

# Stop
docker-compose down
```

### Environment Variables

For production deployment, you can configure:

- `HOST`: Server host (default: "0.0.0.0")
- `PORT`: Server port (default: 8000)

## License

MIT License
