# Troubleshooting Guide

This guide helps you diagnose and resolve common issues with Claude Connect.

## Installation Issues

### Python Version

**Issue:** Error message about incompatible Python version.

**Solution:** Ensure you have Python 3.10 or higher installed:

```bash
python --version
```

If you have multiple Python versions installed, make sure you're using the correct one:

```bash
py -3.10 --version  # On Windows
```

### Virtual Environment

**Issue:** Unable to create or activate the virtual environment.

**Solution:**

1. Ensure `virtualenv` is installed:

```bash
pip install virtualenv
```

2. If activation fails on Windows, check your PowerShell execution policy:

```powershell
Get-ExecutionPolicy
```

If it's set to `Restricted`, change it to `RemoteSigned` for the current user:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

3. If you still have issues, use the full path to the Python executable:

```bash
& "C:\path\to\venv\Scripts\python.exe" main.py
```

### Dependencies

**Issue:** Error installing dependencies.

**Solution:**

1. Ensure pip is up to date:

```bash
python -m pip install --upgrade pip
```

2. Install dependencies one by one to identify the problematic package:

```bash
pip install python-dotenv
pip install jsonrpcserver
# Continue with other packages
```

3. Check for conflicting dependencies and version requirements.

## Configuration Issues

### Environment Variables

**Issue:** Server can't find environment variables.

**Solution:**

1. Ensure you've copied `.env.example` to `.env`:

```bash
copy .env.example .env  # On Windows
```

2. Verify the `.env` file is in the same directory as `main.py`.

3. Check that the `.env` file contains all required variables.

4. If using Claude Desktop, ensure environment variables are correctly set in the configuration file.

### API Keys

**Issue:** "API key not configured" or similar errors.

**Solution:**

1. Ensure you've added your API keys to the `.env` file:

```
BING_API_KEY=your_bing_api_key_here
```

2. Verify the API keys are valid and active.

3. Check for whitespace or special characters in the API keys.

### Search Configuration

**Issue:** Search functionality not working.

**Solution:**

1. Check `search_config.json` to ensure the API you're trying to use is enabled:

```json
{
  "default": "bing",
  "apis": {
    "bing": {"enabled": true},
    "google": {"enabled": false}
  }
}
```

2. If using Google Search, ensure both `GOOGLE_API_KEY` and `GOOGLE_CX` are set in your `.env` file.

## Runtime Issues

### Server Won't Start

**Issue:** Error when starting the server.

**Solution:**

1. Check for syntax errors in `main.py`.

2. Ensure all required dependencies are installed.

3. Check the error message for specific issues.

### HTTP Mode Issues

**Issue:** HTTP server won't start or is not accessible.

**Solution:**

1. Ensure port 8000 is not already in use:

```bash
netstat -aon | findstr 8000  # On Windows
```

2. If the port is in use, either close the application using it or change the port in `main.py`.

3. Ensure `fastapi` and `uvicorn` are installed:

```bash
pip install fastapi uvicorn
```

### JWT Authentication

**Issue:** Unable to authenticate with JWT.

**Solution:**

1. Ensure `JWT_SECRET_KEY` is set in your `.env` file.

2. Verify you're including the token in the `Authorization` header with the `Bearer` prefix.

3. Check that the token hasn't expired.

4. If you're getting a 401 Unauthorized error, ensure you're using the correct username and password when obtaining the token.

## Claude Desktop Integration Issues

### Connection Issues

**Issue:** Claude Desktop can't connect to the server.

**Solution:**

1. Ensure the paths in `claude_desktop_config.json` are correct and use double backslashes:

```json
{
  "mcpServers": {
    "claude-connect": {
      "command": "C:\\path\\to\\venv\\Scripts\\python.exe",
      "args": [
        "C:\\path\\to\\claude-connect\\main.py"
      ]
    }
  }
}
```

2. Verify the Python executable path exists and is correct.

3. Ensure Claude Desktop has been restarted after changing the configuration.

### Functionality Issues

**Issue:** Some capabilities don't work in Claude Desktop.

**Solution:**

1. Check the Claude Desktop logs for errors:
   - Windows: `%APPDATA%\Claude\logs\`

2. Ensure the required environment variables are set in the Claude Desktop configuration.

3. Verify the capabilities are correctly implemented in `main.py`.

## File Operation Issues

### Permission Denied

**Issue:** Permission denied when reading or writing files.

**Solution:**

1. Ensure the sandbox directory exists and has appropriate permissions.

2. Run the server with appropriate permissions.

3. Check for file locks from other processes.

### Path Traversal

**Issue:** "Path traversal attempt detected" error.

**Solution:**

1. Ensure file paths are relative to the sandbox directory and don't contain `..` or other path traversal attempts.

2. Use only valid filenames without special characters.

## Database Issues

### SQLite Issues

**Issue:** SQLite database errors.

**Solution:**

1. Ensure the directory where the database file is created has write permissions.

2. Check for database file corruption. You may need to delete the database file and let it be recreated.

### PostgreSQL Issues

**Issue:** Unable to connect to PostgreSQL.

**Solution:**

1. Ensure PostgreSQL is running and accessible.

2. Verify the connection string in `DATABASE_URL` is correct.

3. Check that the database user has appropriate permissions.

4. Ensure `asyncpg` is installed:

```bash
pip install asyncpg
```

## Logging and Debugging

### Enabling Debug Logs

To get more detailed logs, modify the logging configuration in `main.py`:

```python
logging.basicConfig(
    level=logging.DEBUG,  # Change from INFO to DEBUG
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
```

### Logging to a File

To save logs to a file for easier troubleshooting:

```python
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="claude_connect.log",  # Add this line
    filemode="a"  # Append to the log file
)
```

### Debugging JSON-RPC

To debug JSON-RPC requests and responses, you can add print statements or logging:

```python
async def main_stdio():
    while True:
        request = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
        if not request:
            break
        try:
            request_json = json.loads(request)
            logger.debug(f"Received request: {request_json}")  # Add this line
            response = await async_dispatch(request_json)
            logger.debug(f"Sending response: {response}")  # Add this line
            print(json.dumps(response))
            sys.stdout.flush()
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON: {request}")
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32700, "message": "Parse error"}, "id": None}))
            sys.stdout.flush()
```

## Getting Help

If you're still experiencing issues after trying the solutions in this guide, you can:

1. Check the [GitHub Issues](https://github.com/grapheneaffiliate/claude-connect/issues) for similar problems and solutions.

2. Create a new issue with detailed information about your problem, including:
   - Error messages
   - Steps to reproduce
   - Your environment (OS, Python version, etc.)
   - Relevant configuration files (with sensitive information redacted)

3. Join the [Discord Server](https://discord.gg/mcp-community) (coming soon) for community support.
