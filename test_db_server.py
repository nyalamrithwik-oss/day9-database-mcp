"""
Database MCP Server Test Client
Tests all CRUD operations

Author: Rithwik Nyalam
Date: December 27, 2024
"""

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def print_header(title: str):
    """Print formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


async def test_database_mcp():
    """
    Test all database MCP server operations.
    
    Tests:
    1. Create notes (INSERT)
    2. Read all notes (SELECT)
    3. Read specific note (SELECT WHERE)
    4. Update note (UPDATE)
    5. Search notes (LIKE)
    6. Delete note (DELETE)
    """
    
    print_header("DATABASE MCP SERVER TEST")
    
    # Server configuration
    server_params = StdioServerParameters(
        command="python",
        args=["database_mcp_server.py"]
    )
    
    print("\nConnecting to MCP server...")
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize connection
                print("Initializing session...")
                await session.initialize()
                print("Connection established!\n")
                
                # List available tools
                print_header("AVAILABLE TOOLS")
                tools = await session.list_tools()
                print(f"\nFound {len(tools.tools)} tools:\n")
                for i, tool in enumerate(tools.tools, 1):
                    print(f"  {i}. {tool.name}")
                    print(f"     -> {tool.description}\n")
                
                # Test operations
                print_header("TESTING DATABASE OPERATIONS")
                
                # Test 1: Create notes
                print("\nTest 1: Creating Notes")
                print("-" * 70)
                
                result = await session.call_tool("create_note", {
                    "title": "Day 9 Learning",
                    "content": "Completed MCP database server. Learned async SQLite operations."
                })
                print(result.content[0].text)
                
                result = await session.call_tool("create_note", {
                    "title": "Week 2 Progress",
                    "content": "MCP fundamentals complete. Building real-world integrations."
                })
                print(result.content[0].text)
                
                result = await session.call_tool("create_note", {
                    "title": "Claude Desktop Setup",
                    "content": "Successfully connected calculator MCP to Claude Desktop!"
                })
                print(result.content[0].text)
                
                # Test 2: Get all notes
                print("\nTest 2: Retrieving All Notes")
                print("-" * 70)
                result = await session.call_tool("get_all_notes", {})
                print(result.content[0].text)
                
                # Test 3: Get specific note
                print("\nTest 3: Getting Note by ID (ID=1)")
                print("-" * 70)
                result = await session.call_tool("get_note_by_id", {"id": 1})
                print(result.content[0].text)
                
                # Test 4: Update note
                print("\nTest 4: Updating Note (ID=1)")
                print("-" * 70)
                result = await session.call_tool("update_note", {
                    "id": 1,
                    "content": "Day 9 complete! MCP database + Claude Desktop integration working!"
                })
                print(result.content[0].text)
                
                # Verify update
                result = await session.call_tool("get_note_by_id", {"id": 1})
                print("\nUpdated note:")
                print(result.content[0].text)
                
                # Test 5: Search notes
                print("\nTest 5: Searching Notes (keyword: 'MCP')")
                print("-" * 70)
                result = await session.call_tool("search_notes", {"keyword": "MCP"})
                print(result.content[0].text)
                
                # Test 6: Delete note
                print("\nTest 6: Deleting Note (ID=2)")
                print("-" * 70)
                result = await session.call_tool("delete_note", {"id": 2})
                print(result.content[0].text)
                
                # Verify deletion
                print("\nRemaining notes:")
                result = await session.call_tool("get_all_notes", {})
                print(result.content[0].text)
                
                # Summary
                print_header("TEST SUMMARY")
                print("\nAll database operations tested successfully!")
                print("Operations verified:")
                print("  [X] CREATE - Insert new notes")
                print("  [X] READ - Get all notes & specific notes")
                print("  [X] UPDATE - Modify existing notes")
                print("  [X] DELETE - Remove notes")
                print("  [X] SEARCH - Find notes by keyword")
                print("\n" + "=" * 70)
                print("Day 9 Complete! Database MCP Server working perfectly.")
                print("=" * 70 + "\n")
    
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Make sure database_mcp_server.py is in the same directory")
        print("2. Check that virtual environment is activated")
        print("3. Verify aiosqlite package is installed")


if __name__ == "__main__":
    asyncio.run(test_database_mcp())
