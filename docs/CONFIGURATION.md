# Configuration Guide

This guide covers the advanced configuration options for Claude Connect.

## Environment Variables

The `.env` file contains environment variables that control the server's behavior. Here's a detailed explanation of each variable:

### Core Settings

```
# Secret key for authorizing MCP clients via the initialize method
SECRET_KEY=my-very-secure-mcp-secret
```

- **SECRET_KEY**: Optional secret key that clients must provide in the `initialize` method. Set this for additional security.

### Search API Keys

```
# Required: Bing Search API v7 key
BING_API_KEY=YOUR_BING_API_KEY

# Optional: Google Custom Search API Key
GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY

# Optional: Google Custom Search Engine ID (CX)
GOOGLE_CX=YOUR_GOOGLE_CX
```

- **BING_API_KEY**: Required for the default search functionality. Obtain from [Microsoft Azure Portal](https://portal.azure.com/#create/microsoft.bingsearch).
- **GOOGLE_API_KEY** and **GOOGLE_CX**: Optional for Google search functionality. Obtain from [Google Cloud Console](https://console.cloud.google.com/apis/library/customsearch.googleapis.com) and [Programmable Search Engine](https://programmablesearchengine.google.com/).

### HTTP Authentication

```
# Required if using HTTP mode with JWT
JWT_SECRET_KEY=a-different-very-secure-jwt-secret
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
```

- **JWT_SECRET_KEY**: Secret key for JWT token generation and validation.
- **JWT_ALGORITHM**: Algorithm used for JWT encoding/decoding (default: HS256).
- **JWT_ACCESS_TOKEN_EXPIRE_MINUTES**: Token expiration time in minutes (default: 30).

### Database Settings

```
# Example for PostgreSQL
# DATABASE_URL=postgresql+asyncpg://user:password@host:port/dbname
DATABASE_URL=sqlite:///model_context.db
```

- **DATABASE_URL**: Database connection string. Defaults to SQLite, but can be configured for PostgreSQL.

### Caching

```
# Example for Redis
# REDIS_URL=redis://localhost:6379/0
```

- **REDIS_URL**: Optional Redis connection string for caching.

### Internationalization

```
# Default language code (e.g., en, es, fr)
LANGUAGE=en
```

- **LANGUAGE**: Default language code for internationalization.

## Configuration Files

### search_config.json

This file configures the web search functionality:

```json
{
  "default": "bing",
  "apis": {
    "bing": {
      "enabled": true,
      "handler": "bing_search_handler"
    },
    "google": {
      "enabled": false,
      "handler": "google_search_handler"
    }
  }
}
```

- **default**: The default search API to use when not specified.
- **apis**: Configuration for each supported API:
  - **enabled**: Whether the API is enabled.
  - **handler**: The handler function to use for this API.

### resources.json

This file defines custom resource types:

```json
{
  "user-profile": {
    "handler": "user_profile_handler",
    "schema": {"user_id": "string"},
    "description": "Retrieves user profile information."
  },
  "weather": {
    "handler": "weather_handler",
    "schema": {"location": "string"},
    "description": "Retrieves weather information for a location."
  }
}
```

For each resource type:
- **handler**: The function that handles requests for this resource type.
- **schema**: The expected parameters for this resource type.
- **description**: A description of the resource type.

### prompts.json

This file defines custom prompt templates:

```json
{
  "email-reply": {
    "template": "Draft a polite reply to the following email:\n\n{email_content}",
    "description": "Template for drafting email replies."
  },
  "summarize-data": {
    "template": "Summarize the following data in a clear, concise way:\n\n{data}",
    "description": "Template for summarizing complex data."
  }
}
```

For each prompt template:
- **template**: The prompt template text with placeholders in curly braces.
- **description**: A description of the prompt template.

## Advanced Configuration

### Customizing Handlers

You can customize the behavior of resource and tool handlers by modifying the corresponding functions in `main.py`. For example, to customize the web search functionality, modify the `bing_search_handler` and `google_search_handler` functions.

### Adding New Capabilities

To add a new capability:

1. Implement the handler function in `main.py`.
2. Add the capability to the `capabilities_list_handler` function.
3. Update the relevant configuration file if necessary.

### Logging Configuration

You can customize logging by modifying the logging configuration in `main.py`:

```python
logging.basicConfig(
    level=logging.INFO,  # Change to logging.DEBUG for more detailed logs
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    # Add filename parameter to log to a file instead of console
    # filename="mcp_server.log",
)
```

### Security Considerations

- Keep your API keys and secrets secure.
- Use HTTPS if exposing the HTTP endpoint publicly.
- Regularly update dependencies to address security vulnerabilities.
- Limit file operations to the sandbox directory.
