# Claude Desktop Integration Guide

## Overview

[Claude Desktop](https://claude.ai/desktop) is Anthropic's desktop application that allows you to interact with Claude AI models. It supports the Model Context Protocol (MCP), enabling Claude to access external tools and resources through MCP-compliant servers like Claude Connect.

This guide explains how to configure Claude Desktop to use your Claude Connect server.

## Prerequisites

- Claude Desktop installed on your computer
- Claude Connect server set up and working correctly (see [Setup Guide](SETUP.md))

## Configuration Steps

### 1. Locate the Configuration File

The Claude Desktop configuration file is located at:

- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
  - Typically: `C:\Users\<username>\AppData\Roaming\Claude\claude_desktop_config.json`

### 2. Edit the Configuration File

1. Open the configuration file in a text editor (you may need administrator privileges)

2. Add or modify the `mcpServers` section in the JSON file:

```json
{
  "mcpServers": {
    "claude-connect": {
      "command": "C:\\path\\to\\your\\claude-connect\\venv\\Scripts\\python.exe",
      "args": [
        "C:\\path\\to\\your\\claude-connect\\main.py"
      ],
      "env": {
         "BING_API_KEY": "your_bing_api_key_here"
      }
    }
  }
}
```

**Important Notes:**
- Replace the paths with the correct absolute paths on your system
- Always use double backslashes (`\\`) in Windows paths within JSON
- Use the Python executable from your virtual environment
- You can specify environment variables directly in the config if needed, or rely on the `.env` file in your project directory

### 3. Restart Claude Desktop

Completely close and restart Claude Desktop after saving the configuration.

## Testing the Integration

In a Claude conversation, try commands like:

- "Search the web for recent AI research papers"
- "Create a file called notes.txt in your sandbox with a brief summary of MCP"
- "List all files in your sandbox"

Claude should be able to execute these commands using your Claude Connect server.

## Troubleshooting

### Common Issues

1. **Claude can't find the server**
   - Verify the paths in the configuration file are correct
   - Ensure you're using double backslashes in paths
   - Check that the Python executable path is correct

2. **Search functionality not working**
   - Verify your Bing API key is correct in the environment variables
   - Check that the search API is enabled in `search_config.json`

3. **File operations not working**
   - Ensure the sandbox directory exists and has appropriate permissions

### Checking Logs

Claude Desktop logs can help diagnose issues:

- **Windows**: `%APPDATA%\Claude\logs\`

The MCP server logs are output to the console by default. You can modify the logging configuration in `main.py` to write to a file for easier troubleshooting.

## Advanced Configuration

For more advanced configuration options, see the [Configuration Guide](CONFIGURATION.md).

## Security Considerations

- The MCP server runs with the same permissions as Claude Desktop
- File operations are restricted to the sandbox directory
- API keys should be kept secure and not shared

## Limitations

- Claude Desktop can only use one MCP server at a time
- Some capabilities may be restricted by Claude's permissions
- Network operations require appropriate firewall permissions
