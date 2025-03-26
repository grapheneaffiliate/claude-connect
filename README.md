# Claude Connect

An MCP-compliant external connector server enabling Claude and other LLMs to interact with web APIs, filesystem, and custom resources. v1.1 (March 2025)

## Overview

Claude Connect is a server that implements Anthropic's Model Context Protocol (MCP), allowing Large Language Models like Claude to interact with external tools and resources in a standardized way. This server enables LLMs to access web search results, read and write files in a sandboxed environment, and utilize custom resources.

### Key Features

- **Web Search Integration**: Connect to Bing Search API (required) and Google Search API (optional)
- **File Operations**: Read, write, list, and delete files within a secure sandbox
- **Custom Resources**: Define and access custom resource types
- **Prompt Templates**: Store and retrieve custom prompt templates
- **Multiple Transport Options**: Primary STDIO transport for Claude Desktop integration, optional HTTP transport with JWT authentication
- **Extensible Architecture**: Easy to add new capabilities and resources
- **Cross-Platform**: Tested on Windows 10, but designed to work on any platform supporting Python 3.10+

## Quick Start

This MCP server enables Large Language Models like Claude to access external tools and resources. It takes about 15 minutes to set up and requires Python 3.10+ and API keys for search functionality. Follow these steps to get started:

1. Install [Python 3.10+](https://www.python.org/downloads/), create a virtual environment, and activate it (e.g., using `python -m venv venv` and `..\venv\Scripts\activate` on Windows).
2. Install dependencies: `..\venv\Scripts\pip.exe install -r requirements.txt` (using full path helps bypass potential PowerShell execution policy issues).
3. Rename `.env.example` to `.env` and add your API keys ([Bing Search API](https://portal.azure.com/#create/microsoft.bingsearch) required, [Google Search API](https://console.cloud.google.com/apis/library/customsearch.googleapis.com) optional).
4. Run server in STDIO mode: `..\venv\Scripts\python.exe main.py` or HTTP mode: `..\venv\Scripts\python.exe main.py --http`.
5. Test with `..\venv\Scripts\pytest.exe`.

**Note**: Some commands, especially activation or installation, might require running PowerShell/CMD as Administrator on Windows depending on your system configuration.

For detailed setup instructions, see the [Setup Guide](docs/SETUP.md). For Claude Desktop integration, see the [Claude Desktop Integration Guide](docs/CLAUDE_DESKTOP.md).

## Documentation

- [Setup Guide](docs/SETUP.md)
- [Configuration Guide](docs/CONFIGURATION.md)
- [Claude Desktop Integration](docs/CLAUDE_DESKTOP.md)
- [API Reference](docs/API_REFERENCE.md)
- [Advanced Usage](docs/ADVANCED_USAGE.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)

## Advanced Usage

For advanced usage scenarios, including:

- Manual JSON-RPC interaction
- Extending the server with new capabilities
- Using PostgreSQL instead of SQLite
- Enabling Redis caching
- Internationalization
- Performance tuning

See the [Advanced Usage Guide](docs/ADVANCED_USAGE.md).

## Code Explanation & Design Rationale

The Claude Connect server is designed with the following principles in mind:

- **Modularity**: Each capability is implemented as a separate handler function.
- **Security**: File operations are restricted to a sandbox directory, and path traversal attempts are prevented.
- **Extensibility**: New capabilities can be added by implementing new handler functions and updating the capabilities list.
- **Configurability**: Most aspects of the server can be configured through environment variables and configuration files.

The server supports two transport modes:

- **STDIO**: For integration with Claude Desktop and other MCP clients that support STDIO transport.
- **HTTP**: For development, testing, and integration with web applications.

For more details on the code structure and design decisions, see the [API Reference](docs/API_REFERENCE.md).

## Containerization & Deployment

You can containerize Claude Connect using Docker:

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN mkdir -p sandbox

EXPOSE 8000

CMD ["python", "main.py", "--http"]
```

Build and run the Docker container:

```bash
docker build -t claude-connect .
docker run -p 8000:8000 --env-file=.env claude-connect
```

For more deployment options, including Windows services and systemd, see the [Advanced Usage Guide](docs/ADVANCED_USAGE.md).

## Future Enhancements

Planned enhancements for future versions include:

- **WebSocket Transport**: For real-time communication with web applications.
- **More Search Providers**: Integration with additional search APIs.
- **Enhanced Authentication**: More authentication options for HTTP mode.
- **Admin Dashboard**: A web interface for managing the server.
- **Plugin System**: A plugin system for extending the server with custom capabilities.

## Troubleshooting

If you encounter issues, check the [Troubleshooting Guide](docs/TROUBLESHOOTING.md) for common problems and solutions.

For more detailed logging, set the log level to DEBUG in main.py:

```python
logging.basicConfig(
    level=logging.DEBUG,  # Change from INFO to DEBUG
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
```

## Contributing

Contributions are welcome! Please check out our [Contributing Guidelines](CONTRIBUTING.md) and [Code of Conduct](CODE_OF_CONDUCT.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Community

- GitHub Issues: For bug reports and feature requests
- [Discord Server](https://discord.gg/mcp-community): For discussions and community support (Coming Soon)
