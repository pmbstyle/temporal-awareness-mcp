# Temporal Awareness MCP

A robust, modern, and well-tested MCP server that gives language models temporal awareness and time calculation abilities.

This project provides a suite of reliable tools for an LLM to understand and reason about time, from simple date calculations to human-centric contextual analysis. It is built with modern Python (3.12+), Poetry for dependency management, and a strong emphasis on automated testing with pytest.

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- [Poetry](https://python-poetry.org/) (1.2+ recommended) for dependency management.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/temporal-awareness-mcp.git
    cd temporal-awareness-mcp
    ```

2.  **Install dependencies:**
    Poetry will create a dedicated virtual environment and install all necessary packages from the `poetry.lock` file, ensuring a consistent and reliable setup.
    ```bash
    poetry install
    ```

## 🏃‍♀️ Running the Server

To run the development server, use the following command. The `--reload` flag enables hot-reloading, which means the server will automatically restart whenever you save a change to the code.

```bash
poetry run python -m uvicorn temporal_awareness_mcp.main:mcp --reload
```