import json
import os
import pytest
import sys
from pathlib import Path

# Add parent directory to path so we can import main
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import functions from main.py
from main import (
    capabilities_list_handler,
    tool_file_list_handler,
    tool_file_write_handler,
    tool_file_read_handler,
    tool_file_delete_handler,
    prompt_list_handler,
)

@pytest.fixture(autouse=True)
def setup_and_teardown():
    """Setup before each test and cleanup after."""
    # Create sandbox directory if it doesn't exist
    Path("sandbox").mkdir(exist_ok=True)
    
    # Clean up any existing test files
    test_file = Path("sandbox/test_file.txt")
    if test_file.exists():
        test_file.unlink()
    
    yield
    
    # Clean up after tests
    if test_file.exists():
        test_file.unlink()

@pytest.mark.asyncio
async def test_capabilities_list():
    """Test the capabilities/list handler."""
    result = await capabilities_list_handler()
    assert "result" in result
    assert "resources" in result["result"]
    assert "tools" in result["result"]
    assert "prompts" in result["result"]
    
    # Check for specific capabilities
    tools = result["result"]["tools"]
    assert "tool://web-search" in tools
    assert "tool://file-read" in tools
    assert "tool://file-write" in tools
    assert "tool://file-list" in tools
    assert "tool://file-delete" in tools

@pytest.mark.asyncio
async def test_file_operations():
    """Test file operations (write, read, list, delete)."""
    # Test file_list (initially empty or without our test file)
    list_result = await tool_file_list_handler()
    initial_files = list_result["result"]["files"]
    assert "test_file.txt" not in initial_files
    
    # Test file_write
    write_result = await tool_file_write_handler(filename="test_file.txt", content="Hello, world!")
    assert "result" in write_result
    assert "message" in write_result["result"]
    assert "test_file.txt" in write_result["result"]["message"]
    
    # Test file_read
    read_result = await tool_file_read_handler(filename="test_file.txt")
    assert "result" in read_result
    assert "content" in read_result["result"]
    assert read_result["result"]["content"] == "Hello, world!"
    
    # Test file_list again (should now include our test file)
    list_result = await tool_file_list_handler()
    updated_files = list_result["result"]["files"]
    assert "test_file.txt" in updated_files
    
    # Test file_delete
    delete_result = await tool_file_delete_handler(filename="test_file.txt")
    assert "result" in delete_result
    assert "message" in delete_result["result"]
    assert "test_file.txt" in delete_result["result"]["message"]
    
    # Test file_list one more time (should no longer include our test file)
    list_result = await tool_file_list_handler()
    final_files = list_result["result"]["files"]
    assert "test_file.txt" not in final_files

@pytest.mark.asyncio
async def test_prompt_list():
    """Test the prompt/list handler."""
    result = await prompt_list_handler()
    assert "result" in result
    assert "prompts" in result["result"]
    
    # Check for specific prompts from prompts.json
    prompts = result["result"]["prompts"]
    assert len(prompts) > 0  # Should have at least one prompt
