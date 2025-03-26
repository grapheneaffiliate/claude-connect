# Claude Connect

An MCP-compliant external connector server enabling Claude and other LLMs to interact with web APIs, filesystem, and custom resources.

![Claude Connect](https://raw.githubusercontent.com/grapheneaffiliate/claude-connect/master/docs/images/claude-connect-logo.png)

## Overview

Claude Connect is a server that implements Anthropic's Model Context Protocol (MCP), allowing Large Language Models like Claude to interact with external tools and resources in a standardized way. This server enables LLMs to access web search results, read and write files in a sandboxed environment, and utilize custom resources.

### Key Features

- **Web Search Integration**: Connect to Bing Search API (required) and Google Search API (optional)
- **File Operations**: Read, write, list, and delete files within a secure sandbox
- **Custom Resources**: Define and access custom resource types
- **Prompt Templates**: Store and retrieve custom prompt templates
- **Multiple Transport Options**: Primary STDIO transport for Claude Desktop integration, optional HTTP transport with JWT authentication
- **Extensible Architecture**: Easy to add new capabilities and resources

## Quick Start

This MCP server enables Large Language Models like Claude to access external tools and resources. It takes about 15 minutes to set up and requires Python 3.10+ and API keys for search functionality. Follow these steps to get started:

1. Install [Python 3.10+](https://www.python.org/downloads/), create a virtual environment, and activate it.
2. Install dependencies: `pip install -r requirements.txt`.
3. Rename `.env.example` to `.env` and add your API keys ([Bing Search API](https://portal.azure.com/#create/microsoft.bingsearch) required, [Google Search API](https://console.cloud.google.com/apis/library/customsearch.googleapis.com) optional).
4. Run server in STDIO mode: `python main.py` or HTTP mode: `python main.py --http`.
5. Test with `pytest`.

For detailed setup instructions, see the [Setup Guide](docs/SETUP.md). For Claude Desktop integration, see the [Claude Desktop Integration Guide](docs/CLAUDE_DESKTOP.md).

## Documentation

- [Setup Guide](docs/SETUP.md)
- [Configuration Guide](docs/CONFIGURATION.md)
- [Claude Desktop Integration](docs/CLAUDE_DESKTOP.md)
- [API Reference](docs/API_REFERENCE.md)
- [Advanced Usage](docs/ADVANCED_USAGE.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)

## Contributing

Contributions are welcome! Please check out our [Contributing Guidelines](CONTRIBUTING.md) and [Code of Conduct](CODE_OF_CONDUCT.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Community

- GitHub Issues: For bug reports and feature requests
- [Discord Server](https://discord.gg/mcp-community): For discussions and community support (Coming Soon)
