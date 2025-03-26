# Setup Guide

This guide provides detailed instructions for setting up the Claude Connect server on Windows 10.

## Prerequisites

Before you begin, ensure you have the following:

- **Python 3.10+**: Download and install from [python.org](https://www.python.org/downloads/)
- **API Keys**:
  - **Bing Search API Key** (Required): Obtain from [Microsoft Azure Portal](https://portal.azure.com/#create/microsoft.bingsearch)
  - **Google Custom Search API Key & CX ID** (Optional): Obtain from [Google Cloud Console](https://console.cloud.google.com/apis/library/customsearch.googleapis.com) and [Programmable Search Engine](https://programmablesearchengine.google.com/)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/grapheneaffiliate/claude-connect.git
cd claude-connect
```

### 2. Create a Virtual Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
.\venv\Scripts\activate
```

If you encounter permission issues, you may need to adjust your PowerShell execution policy:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

For optional features, uncomment and run the relevant installation commands in `requirements.txt`.

### 4. Configure Environment Variables

1. Copy the example environment file:
   ```bash
   copy .env.example .env
   ```

2. Edit the `.env` file with your API keys and other settings:
   ```
   # Required: Bing Search API v7 key
   BING_API_KEY=YOUR_BING_API_KEY

   # Optional: Google Custom Search API Key
   GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY

   # Optional: Google Custom Search Engine ID (CX)
   GOOGLE_CX=YOUR_GOOGLE_CX
   ```

### 5. Configure Search APIs

Edit `search_config.json` to enable or disable specific search APIs:

```json
{
  "default": "bing",
  "apis": {
    "bing": {"enabled": true},
    "google": {"enabled": false}
  }
}
```

Set `"enabled": true` for the APIs you want to use.

## Running the Server

### STDIO Mode (for Claude Desktop)

This is the primary mode for integration with Claude Desktop:

```bash
python main.py
```

### HTTP Mode (for Testing/Development)

This mode starts an HTTP server for testing and development:

```bash
python main.py --http
```

The server will start on `http://127.0.0.1:8000`.

## Verifying Installation

Run the tests to verify that everything is working correctly:

```bash
pytest
```

All tests should pass if the setup is correct.

## Next Steps

- [Configure Claude Desktop](CLAUDE_DESKTOP.md) to use your MCP server
- Learn about [advanced configuration options](CONFIGURATION.md)
- Explore [API reference](API_REFERENCE.md) for all available capabilities

## Troubleshooting

If you encounter issues during setup, check the [Troubleshooting Guide](TROUBLESHOOTING.md) for common problems and solutions.
