# Advanced Usage

This guide covers advanced usage scenarios for Claude Connect.

## Manual JSON-RPC Interaction

While Claude Connect is primarily designed to be used with Claude Desktop, you can also interact with it directly using JSON-RPC requests.

### STDIO Mode

In STDIO mode, you can send JSON-RPC requests directly to the server's standard input and receive responses from standard output.

**Example (PowerShell):**

```powershell
$request = '{"jsonrpc": "2.0", "method": "capabilities/list", "params": {}, "id": 1}'
$request | & "C:\path\to\venv\Scripts\python.exe" "C:\path\to\claude-connect\main.py"
```

### HTTP Mode

In HTTP mode, you can send JSON-RPC requests to the server's HTTP endpoint.

**Example (PowerShell):**

```powershell
# First, obtain a JWT token
$tokenResponse = Invoke-RestMethod -Uri http://127.0.0.1:8000/token `
  -Method Post `
  -ContentType 'application/x-www-form-urlencoded' `
  -Body "username=testuser&password=testpassword"
$token = $tokenResponse.access_token

# Then, send a JSON-RPC request
$jsonRequest = '{"jsonrpc": "2.0", "method": "capabilities/list", "params": {}, "id": 1}'
$headers = @{
  "Authorization" = "Bearer $token"
  "Content-Type"  = "application/json"
}
Invoke-RestMethod -Uri http://127.0.0.1:8000/mcp -Method Post -Headers $headers -Body $jsonRequest
```

## Extending the Server

### Adding a New Resource Type

1. Define the resource type in `resources.json`:

```json
{
  "custom-resource": {
    "handler": "custom_resource_handler",
    "schema": {"resource_id": "string"},
    "description": "A custom resource type."
  }
}
```

2. Implement the handler function in `main.py`:

```python
@method
async def custom_resource_handler(resource_id: str) -> Result:
    """Handle the resource/custom-resource method for MCP."""
    # Implement your custom logic here
    return Success({
        "id": resource_id,
        "data": "Custom resource data"
    })
```

### Adding a New Tool

1. Implement the tool handler function in `main.py`:

```python
@method
async def tool_custom_tool_handler(param1: str, param2: Optional[int] = None) -> Result:
    """Handle the tool/custom-tool method for MCP."""
    # Implement your custom logic here
    return Success({
        "result": f"Processed {param1} with {param2 if param2 is not None else 'default'}"
    })
```

2. Add the tool to the capabilities list in the `capabilities_list_handler` function:

```python
capabilities = {
    "resources": [...],
    "tools": [
        "tool://web-search",
        "tool://file-read",
        "tool://file-write",
        "tool://file-list",
        "tool://file-delete",
        "tool://custom-tool"  # Add your new tool here
    ],
    "prompts": [...]
}
```

### Adding a New Prompt Template

Add the prompt template to `prompts.json`:

```json
{
  "custom-prompt": {
    "template": "This is a custom prompt template with {placeholder}.",
    "description": "A custom prompt template."
  }
}
```

## Advanced Configuration

### Using PostgreSQL Instead of SQLite

1. Install the required dependencies:

```bash
pip install asyncpg
```

2. Update the `DATABASE_URL` in your `.env` file:

```
DATABASE_URL=postgresql+asyncpg://user:password@host:port/dbname
```

### Enabling Redis Caching

1. Install the required dependencies:

```bash
pip install redis aioredis
```

2. Update the `REDIS_URL` in your `.env` file:

```
REDIS_URL=redis://localhost:6379/0
```

3. Modify the caching logic in `main.py` to use Redis.

### Internationalization

1. Install the required dependencies:

```bash
pip install Babel
```

2. Extract translatable strings:

```bash
pybabel extract -o locale/messages.pot main.py
```

3. Initialize language catalogs:

```bash
pybabel init -i locale/messages.pot -d locale -l es  # For Spanish
```

4. Translate the strings in `locale/es/LC_MESSAGES/messages.po`.

5. Compile the translations:

```bash
pybabel compile -d locale
```

6. Set the `LANGUAGE` environment variable in your `.env` file:

```
LANGUAGE=es
```

## Performance Tuning

### Asynchronous Operations

Claude Connect uses `asyncio` for asynchronous operations. To improve performance:

- Use asynchronous libraries for I/O-bound operations (e.g., `aiohttp` for HTTP requests, `asyncpg` for database operations).
- Avoid blocking operations in handler functions.
- Use `asyncio.gather` for concurrent operations.

### Caching

Implement caching for frequently accessed data:

```python
# Example: Caching search results
async def tool_web_search_handler(query: str, api: Optional[str] = None) -> Result:
    cache_key = f"search:{api or 'default'}:{query}"
    
    # Check cache
    cached_result = await cache.get(cache_key)
    if cached_result:
        return Success(json.loads(cached_result))
    
    # Perform search
    result = await perform_search(query, api)
    
    # Cache result
    await cache.set(cache_key, json.dumps(result), expire=3600)  # Cache for 1 hour
    
    return Success(result)
```

## Security Considerations

### JWT Authentication

For HTTP mode, Claude Connect uses JWT authentication. To enhance security:

- Use a strong, unique `JWT_SECRET_KEY`.
- Rotate the secret key periodically.
- Set an appropriate expiration time for tokens.

### File Operations

File operations are restricted to the sandbox directory to prevent unauthorized access to the file system. To further enhance security:

- Implement file type validation.
- Set size limits for file operations.
- Regularly clean up the sandbox directory.

### API Keys

Protect your API keys:

- Store them securely in the `.env` file.
- Do not commit the `.env` file to version control.
- Use different API keys for development and production.
- Implement rate limiting to prevent abuse.

## Deployment

### Docker

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

### Systemd Service

You can create a systemd service to run Claude Connect as a background service on Linux:

```ini
[Unit]
Description=Claude Connect MCP Server
After=network.target

[Service]
User=your_user
WorkingDirectory=/path/to/claude-connect
ExecStart=/path/to/claude-connect/venv/bin/python main.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Save this as `/etc/systemd/system/claude-connect.service` and enable it:

```bash
sudo systemctl enable claude-connect
sudo systemctl start claude-connect
```

### Windows Service

You can use NSSM (Non-Sucking Service Manager) to run Claude Connect as a Windows service:

```bash
nssm install ClaudeConnect "C:\path\to\claude-connect\venv\Scripts\python.exe" "C:\path\to\claude-connect\main.py"
nssm set ClaudeConnect AppDirectory "C:\path\to\claude-connect"
nssm start ClaudeConnect
```
