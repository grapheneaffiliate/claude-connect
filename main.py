#!/usr/bin/env python

import argparse
import asyncio
import json
import logging
import os
import pathlib
import sys
from typing import Any, Dict, List, Optional, Union

# Third-party imports
from dotenv import load_dotenv
from jsonrpcserver import Result, Success, async_dispatch, method
import uvicorn  # Added import for HTTP mode
from sqlmodel import Field, Session, SQLModel, create_engine, select
from pydantic import BaseModel  # Keep for potential future use
import requests

# Optional imports (will be imported conditionally)
try:
    import uvicorn
    from fastapi import Depends, FastAPI, HTTPException, Request, status
    from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
    from jose import JWTError, jwt
    from passlib.context import CryptContext
    from starlette.responses import JSONResponse
    HTTP_AVAILABLE = True
except ImportError:
    HTTP_AVAILABLE = False

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("mcp-server")

# Create sandbox directory if it doesn't exist
pathlib.Path("sandbox").mkdir(exist_ok=True)

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///model_context.db")
engine = create_engine(DATABASE_URL)

# Define database models
class ModelContextDB(SQLModel, table=True):
    """Model for storing model context in the database."""
    id: Optional[int] = Field(default=None, primary_key=True)
    model_id: str = Field(index=True)
    version: str
    status: str
    parameters: str  # JSON string
    metrics: Optional[str] = None  # JSON string

# Create database tables
SQLModel.metadata.create_all(engine)

# Load configuration files
def load_config(filename: str) -> Dict[str, Any]:
    """Load a JSON configuration file."""
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.warning(f"Could not load {filename}: {e}")
        return {}

search_config = load_config("search_config.json")
resources_config = load_config("resources.json")
prompts_config = load_config("prompts.json")

# MCP method handlers
@method
async def initialize_handler(secret_key: Optional[str] = None) -> Result:
    """Handle the initialize method for MCP."""
    expected_key = os.getenv("SECRET_KEY")
    if expected_key and secret_key != expected_key:
        return Error(code=-32001, message="Unauthorized: Invalid secret key")
    return Success({"status": "initialized"})

@method
async def capabilities_list_handler() -> Result:
    """Handle the capabilities/list method for MCP."""
    capabilities = {
        "resources": [
            "resource://model-context/{model_id}",
        ],
        "tools": [
            "tool://web-search",
            "tool://file-read",
            "tool://file-write",
            "tool://file-list",
            "tool://file-delete",
        ],
        "prompts": [
            "prompt://list",
            "prompt://{prompt_name}",
        ]
    }
    
    # Add custom resources from resources_config
    for resource_type in resources_config:
        capabilities["resources"].append(f"resource://{resource_type}/{{resource_id}}")
    
    return Success(capabilities)

@method
async def resource_model_context_handler(model_id: str) -> Result:
    """Handle the resource/model-context method for MCP."""
    with Session(engine) as session:
        statement = select(ModelContextDB).where(ModelContextDB.model_id == model_id)
        model_context = session.exec(statement).first()
        
        if not model_context:
            return Error(code=-32004, message=f"Resource not found: Model ID '{model_id}' not found.")
        
        return Success({
            "version": model_context.version,
            "status": model_context.status,
            "parameters": json.loads(model_context.parameters),
            "metrics": json.loads(model_context.metrics) if model_context.metrics else None
        })

@method
async def tool_web_search_handler(query: str, api: Optional[str] = None) -> Result:
    """Handle the tool/web-search method for MCP."""
    # Use the specified API or the default from config
    api_to_use = api or search_config.get("default", "bing")
    
    # Check if the API is enabled
    api_config = search_config.get("apis", {}).get(api_to_use, {})
    if not api_config.get("enabled", False):
        return Error(
            code=-32001, 
            message=f"Configuration error: '{api_to_use}' API not enabled or misconfigured."
        )
    
    # Implement the search logic based on the API
    if api_to_use == "bing":
        return await bing_search_handler(query)
    elif api_to_use == "google":
        return await google_search_handler(query)
    else:
        return Error(code=-32001, message=f"Unsupported search API: {api_to_use}")

async def bing_search_handler(query: str) -> Result:
    """Handle Bing search requests."""
    # This is a placeholder. In a real implementation, you would use the Bing Search API.
    api_key = os.getenv("BING_API_KEY")
    if not api_key:
        return Error(code=-32001, message="Bing API key not configured.")
    
    try:
        # Make the API request to Bing Search API
        headers = {"Ocp-Apim-Subscription-Key": api_key}
        params = {"q": query, "count": 10, "offset": 0, "mkt": "en-US"}
        response = requests.get(
            "https://api.bing.microsoft.com/v7.0/search",
            headers=headers,
            params=params
        )
        response.raise_for_status()
        search_results = response.json()
        
        # Process the response to extract relevant information
        processed_results = []
        if "webPages" in search_results and "value" in search_results["webPages"]:
            for result in search_results["webPages"]["value"]:
                processed_results.append({
                    "title": result.get("name", ""),
                    "url": result.get("url", ""),
                    "snippet": result.get("snippet", "")
                })
        
        return Success({"results": processed_results})
    except requests.RequestException as e:
        return Error(code=-32002, message=f"Error making Bing search request: {str(e)}")

async def google_search_handler(query: str) -> Result:
    """Handle Google search requests."""
    # This is a placeholder. In a real implementation, you would use the Google Custom Search API.
    api_key = os.getenv("GOOGLE_API_KEY")
    cx = os.getenv("GOOGLE_CX")
    if not api_key or not cx:
        return Error(code=-32001, message="Google API key or CX not configured.")
    
    try:
        # Make the API request to Google Custom Search API
        params = {"key": api_key, "cx": cx, "q": query}
        response = requests.get(
            "https://www.googleapis.com/customsearch/v1",
            params=params
        )
        response.raise_for_status()
        search_results = response.json()
        
        # Process the response to extract relevant information
        processed_results = []
        if "items" in search_results:
            for result in search_results["items"]:
                processed_results.append({
                    "title": result.get("title", ""),
                    "url": result.get("link", ""),
                    "snippet": result.get("snippet", "")
                })
        
        return Success({"results": processed_results})
    except requests.RequestException as e:
        return Error(code=-32002, message=f"Error making Google search request: {str(e)}")

@method
async def tool_file_read_handler(filename: str) -> Result:
    """Handle the tool/file-read method for MCP."""
    # Ensure the file is within the sandbox
    file_path = pathlib.Path("sandbox") / filename
    try:
        # Prevent path traversal attacks
        if not file_path.resolve().is_relative_to(pathlib.Path("sandbox").resolve()):
            return Error(code=-32003, message="Operation denied: Path traversal attempt detected.")
        
        if not file_path.exists():
            return Error(code=-32004, message=f"File '{filename}' not found in sandbox.")
        
        with open(file_path, "r") as f:
            content = f.read()
        
        return Success({"content": content})
    except Exception as e:
        return Error(code=-32002, message=f"Error reading file: {str(e)}")

@method
async def tool_file_write_handler(filename: str, content: str, append: bool = False) -> Result:
    """Handle the tool/file-write method for MCP.
    
    Args:
        filename: The name of the file to write to in the sandbox.
        content: The content to write to the file.
        append: Whether to append to the file (True) or overwrite it (False).
    """
    # Ensure the file is within the sandbox
    file_path = pathlib.Path("sandbox") / filename
    try:
        # Prevent path traversal attacks
        if not file_path.resolve().is_relative_to(pathlib.Path("sandbox").resolve()):
            return Error(code=-32003, message="Operation denied: Path traversal attempt detected.")
        
        mode = "a" if append else "w"
        with open(file_path, mode) as f:
            f.write(content)
        
        return Success({"message": f"Successfully {'appended to' if append else 'wrote'} '{filename}' in sandbox."})
    except Exception as e:
        return Error(code=-32002, message=f"Error writing file: {str(e)}")

@method
async def tool_file_list_handler() -> Result:
    """Handle the tool/file-list method for MCP."""
    try:
        files = [f.name for f in pathlib.Path("sandbox").iterdir() if f.is_file()]
        return Success({"files": files})
    except Exception as e:
        return Error(code=-32002, message=f"Error listing files: {str(e)}")

@method
async def tool_file_delete_handler(filename: str) -> Result:
    """Handle the tool/file-delete method for MCP."""
    # Ensure the file is within the sandbox
    file_path = pathlib.Path("sandbox") / filename
    try:
        # Prevent path traversal attacks
        if not file_path.resolve().is_relative_to(pathlib.Path("sandbox").resolve()):
            return Error(code=-32003, message="Operation denied: Path traversal attempt detected.")
        
        if not file_path.exists():
            return Error(code=-32004, message=f"File '{filename}' not found in sandbox.")
        
        file_path.unlink()
        return Success({"message": f"Successfully deleted '{filename}' from sandbox."})
    except Exception as e:
        return Error(code=-32002, message=f"Error deleting file: {str(e)}")

@method
async def prompt_list_handler() -> Result:
    """Handle the prompt/list method for MCP."""
    # Get prompts from the configuration file
    prompts = list(prompts_config.keys())
    return Success({"prompts": prompts})

@method
async def prompt_handler(prompt_name: str) -> Result:
    """Handle the prompt/{prompt_name} method for MCP."""
    prompt = prompts_config.get(prompt_name)
    if not prompt:
        return Error(code=-32004, message=f"Prompt '{prompt_name}' not found.")
    
    return Success({
        "template": prompt.get("template", ""),
        "description": prompt.get("description", "")
    })

# Error class for JSON-RPC errors
class Error(Exception):
    """JSON-RPC error class."""
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(message)

# HTTP server setup (if FastAPI is available)
if HTTP_AVAILABLE:
    app = FastAPI(title="MCP Server", description="Model Context Protocol Server")
    
    # JWT Authentication
    SECRET_KEY = os.getenv("JWT_SECRET_KEY", "")
    ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Password hashing
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
    
    # User database (simplified for demo)
    fake_users_db = {
        "testuser": {
            "username": "testuser",
            "hashed_password": pwd_context.hash("testpassword"),
        }
    }
    
    # JWT token functions
    def create_access_token(data: dict):
        to_encode = data.copy()
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    def verify_token(token: str = Depends(oauth2_scheme)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        return username
    
    # Token endpoint
    @app.post("/token")
    async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
        user = fake_users_db.get(form_data.username)
        if not user or not pwd_context.verify(form_data.password, user["hashed_password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = create_access_token(data={"sub": user["username"]})
        return {"access_token": access_token, "token_type": "bearer"}
    
    # MCP endpoint
    @app.post("/mcp")
    async def mcp_endpoint(request: Request, username: str = Depends(verify_token)):
        request_json = await request.json()
        # Use dispatch directly with the request, relying on the @method decorators
        response = await async_dispatch(request_json)
        return JSONResponse(response)

# Main function
async def main_stdio():
    """Run the MCP server using STDIO transport."""
    logger.info("Starting MCP server (STDIO mode)")
    while True:
        request = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
        if not request:
            break
        try:
            request_json = json.loads(request)
            response = await async_dispatch(request_json)
            print(json.dumps(response))
            sys.stdout.flush()
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON: {request}")
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32700, "message": "Parse error"}, "id": None}))
            sys.stdout.flush()

def main_http():
    """Run the MCP server using HTTP transport."""
    if not HTTP_AVAILABLE:
        logger.error("HTTP mode requires FastAPI and Uvicorn. Please install them with 'pip install fastapi uvicorn'.")
        sys.exit(1)
    
    logger.info("Starting MCP server (HTTP mode)")
    uvicorn.run(app, host="127.0.0.1", port=8000)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MCP Server")
    parser.add_argument("--http", action="store_true", help="Run in HTTP mode instead of STDIO mode")
    parser.add_argument("--version", action="store_true", help="Show version and exit")
    args = parser.parse_args()
    
    if args.version:
        print("MCP Server v1.1")
        sys.exit(0)
    
    if args.http:
        main_http()
    else:
        asyncio.run(main_stdio())
