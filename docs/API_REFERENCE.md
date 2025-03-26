# API Reference

This document provides a comprehensive reference for all the capabilities exposed by the Claude Connect server.

## JSON-RPC 2.0 Protocol

Claude Connect implements the JSON-RPC 2.0 protocol as specified by the Model Context Protocol (MCP). All requests and responses follow this format.

### Request Format

```json
{
  "jsonrpc": "2.0",
  "method": "method/name",
  "params": { /* method parameters */ },
  "id": 1
}
```

### Response Format

**Success:**
```json
{
  "jsonrpc": "2.0",
  "result": { /* result object */ },
  "id": 1
}
```

**Error:**
```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32000,
    "message": "Error message"
  },
  "id": 1
}
```

## Core Methods

### initialize

Initializes the connection with the server. This method should be called first.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "initialize",
  "params": {
    "secret_key": "your-secret-key"
  },
  "id": 1
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "status": "initialized"
  },
  "id": 1
}
```

### capabilities/list

Lists all available capabilities of the server.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "capabilities/list",
  "params": {},
  "id": 2
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "resources": [
      "resource://model-context/{model_id}",
      "resource://user-profile/{user_id}",
      "resource://weather/{location}",
      "resource://news/{topic}"
    ],
    "tools": [
      "tool://web-search",
      "tool://file-read",
      "tool://file-write",
      "tool://file-list",
      "tool://file-delete"
    ],
    "prompts": [
      "prompt://list",
      "prompt://{prompt_name}"
    ]
  },
  "id": 2
}
```

## Resource Methods

### resource/model-context

Retrieves metadata about a model.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "resource/model-context",
  "params": {
    "model_id": "model_abc"
  },
  "id": 3
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "version": "1.2.0",
    "status": "active",
    "parameters": {
      "lr": 0.01,
      "epochs": 100
    },
    "metrics": {
      "accuracy": 0.95,
      "loss": 0.05
    }
  },
  "id": 3
}
```

### resource/user-profile

Retrieves user profile information.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "resource/user-profile",
  "params": {
    "user_id": "123"
  },
  "id": 4
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "preferences": {
      "theme": "dark",
      "language": "en"
    }
  },
  "id": 4
}
```

### resource/weather

Retrieves weather information for a location.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "resource/weather",
  "params": {
    "location": "New York"
  },
  "id": 5
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "temperature": 22,
    "conditions": "Partly Cloudy",
    "humidity": 65,
    "wind_speed": 10
  },
  "id": 5
}
```

## Tool Methods

### tool/web-search

Executes a web search using the configured search API.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "tool/web-search",
  "params": {
    "query": "latest AI research",
    "api": "bing"  // Optional, defaults to the configured default
  },
  "id": 6
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "results": [
      {
        "title": "Latest AI Research Breakthroughs",
        "url": "https://example.com/ai-research",
        "snippet": "Recent breakthroughs in AI research include..."
      },
      {
        "title": "AI Research Trends 2025",
        "url": "https://example.com/ai-trends",
        "snippet": "The top AI research trends for 2025 are..."
      }
    ]
  },
  "id": 6
}
```

### tool/file-read

Reads the content of a file from the sandbox.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "tool/file-read",
  "params": {
    "filename": "notes.txt"
  },
  "id": 7
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "content": "This is the content of the notes.txt file."
  },
  "id": 7
}
```

### tool/file-write

Writes content to a file in the sandbox.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "tool/file-write",
  "params": {
    "filename": "new_file.txt",
    "content": "This is the content to write to the file.",
    "append": false  // Optional, defaults to false
  },
  "id": 8
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "message": "Successfully wrote to 'new_file.txt' in sandbox."
  },
  "id": 8
}
```

### tool/file-list

Lists all files in the sandbox.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "tool/file-list",
  "params": {},
  "id": 9
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "files": ["notes.txt", "new_file.txt", "data.json"]
  },
  "id": 9
}
```

### tool/file-delete

Deletes a file from the sandbox.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "tool/file-delete",
  "params": {
    "filename": "new_file.txt"
  },
  "id": 10
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "message": "Successfully deleted 'new_file.txt' from sandbox."
  },
  "id": 10
}
```

## Prompt Methods

### prompt/list

Lists all available prompt templates.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "prompt/list",
  "params": {},
  "id": 11
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "prompts": ["email-reply", "summarize-data", "explain-code", "translate", "meeting-agenda"]
  },
  "id": 11
}
```

### prompt/{prompt_name}

Retrieves a specific prompt template.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "prompt/email-reply",
  "params": {},
  "id": 12
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "template": "Draft a polite reply to the following email:\n\n{email_content}",
    "description": "Template for drafting email replies."
  },
  "id": 12
}
```

## Error Codes

| Code | Message | Description |
|------|---------|-------------|
| -32700 | Parse error | Invalid JSON was received |
| -32600 | Invalid Request | The JSON sent is not a valid Request object |
| -32601 | Method not found | The method does not exist / is not available |
| -32602 | Invalid params | Invalid method parameter(s) |
| -32603 | Internal error | Internal JSON-RPC error |
| -32000 | Server error | Generic server error |
| -32001 | Configuration error | Error in server configuration |
| -32002 | I/O error | Error in input/output operations |
| -32003 | Operation denied | Operation not permitted |
| -32004 | Resource not found | Requested resource not found |
