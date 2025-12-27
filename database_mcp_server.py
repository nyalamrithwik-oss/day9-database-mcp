"""
Database MCP Server
Day 9: Claude Desktop Integration & Database Operations

Purpose: Create an MCP server that provides database operations to Claude.
This allows Claude to store and retrieve data persistently.

Author: Rithwik Nyalam
Date: December 27, 2024
Part of: 30-Day RAG Learning Journey - Week 2
"""

import asyncio
import logging
import aiosqlite
from typing import Any, List
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("database-mcp")

# Initialize MCP server
app = Server("database-mcp-server")

# Database configuration
DB_PATH = "data.db"


async def init_database():
    """
    Initialize SQLite database with a simple notes table.
    
    This creates a table to store notes with:
    - id: Auto-incrementing primary key
    - title: Note title
    - content: Note content
    - created_at: Timestamp
    """
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()
    logger.info("Database initialized successfully")


@app.list_tools()
async def list_tools() -> List[Tool]:
    """
    Register available database tools with MCP host.
    
    These tools allow Claude to:
    1. Create notes (INSERT)
    2. Read notes (SELECT)
    3. Update notes (UPDATE)
    4. Delete notes (DELETE)
    5. Search notes (LIKE query)
    
    Returns:
        List[Tool]: Available database operations
    """
    return [
        Tool(
            name="create_note",
            description="Create a new note in the database",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Title of the note"
                    },
                    "content": {
                        "type": "string",
                        "description": "Content/body of the note"
                    }
                },
                "required": ["title", "content"]
            }
        ),
        Tool(
            name="get_all_notes",
            description="Retrieve all notes from the database",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_note_by_id",
            description="Get a specific note by its ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "description": "ID of the note to retrieve"
                    }
                },
                "required": ["id"]
            }
        ),
        Tool(
            name="update_note",
            description="Update an existing note",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "description": "ID of the note to update"
                    },
                    "title": {
                        "type": "string",
                        "description": "New title (optional)"
                    },
                    "content": {
                        "type": "string",
                        "description": "New content (optional)"
                    }
                },
                "required": ["id"]
            }
        ),
        Tool(
            name="delete_note",
            description="Delete a note by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "description": "ID of the note to delete"
                    }
                },
                "required": ["id"]
            }
        ),
        Tool(
            name="search_notes",
            description="Search notes by keyword in title or content",
            inputSchema={
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "Keyword to search for"
                    }
                },
                "required": ["keyword"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """
    Execute database operations based on tool name.
    
    This is the core function that handles all database interactions.
    Each tool corresponds to a specific SQL operation.
    
    Args:
        name: Tool name (create_note, get_all_notes, etc.)
        arguments: Tool-specific parameters
        
    Returns:
        list[TextContent]: Operation result message
    """
    
    try:
        if name == "create_note":
            # INSERT operation
            title = arguments.get("title")
            content = arguments.get("content")
            
            async with aiosqlite.connect(DB_PATH) as db:
                cursor = await db.execute(
                    "INSERT INTO notes (title, content) VALUES (?, ?)",
                    (title, content)
                )
                await db.commit()
                note_id = cursor.lastrowid
            
            return [TextContent(
                type="text",
                text=f"Note created successfully! ID: {note_id}\nTitle: {title}"
            )]
        
        elif name == "get_all_notes":
            # SELECT ALL operation
            async with aiosqlite.connect(DB_PATH) as db:
                async with db.execute("SELECT * FROM notes ORDER BY created_at DESC") as cursor:
                    rows = await cursor.fetchall()
            
            if not rows:
                return [TextContent(
                    type="text",
                    text="No notes found in database."
                )]
            
            # Format notes for display
            result = "All Notes:\n\n"
            for row in rows:
                result += f"ID: {row[0]}\n"
                result += f"Title: {row[1]}\n"
                result += f"Content: {row[2]}\n"
                result += f"Created: {row[3]}\n"
                result += "-" * 50 + "\n"
            
            return [TextContent(type="text", text=result)]
        
        elif name == "get_note_by_id":
            # SELECT BY ID operation
            note_id = arguments.get("id")
            
            async with aiosqlite.connect(DB_PATH) as db:
                async with db.execute(
                    "SELECT * FROM notes WHERE id = ?", 
                    (note_id,)
                ) as cursor:
                    row = await cursor.fetchone()
            
            if not row:
                return [TextContent(
                    type="text",
                    text=f"Note with ID {note_id} not found."
                )]
            
            result = f"Note Details:\n\n"
            result += f"ID: {row[0]}\n"
            result += f"Title: {row[1]}\n"
            result += f"Content: {row[2]}\n"
            result += f"Created: {row[3]}\n"
            
            return [TextContent(type="text", text=result)]
        
        elif name == "update_note":
            # UPDATE operation
            note_id = arguments.get("id")
            title = arguments.get("title")
            content = arguments.get("content")
            
            # Build dynamic UPDATE query
            updates = []
            params = []
            
            if title:
                updates.append("title = ?")
                params.append(title)
            if content:
                updates.append("content = ?")
                params.append(content)
            
            if not updates:
                return [TextContent(
                    type="text",
                    text="No fields to update. Provide title or content."
                )]
            
            params.append(note_id)
            query = f"UPDATE notes SET {', '.join(updates)} WHERE id = ?"
            
            async with aiosqlite.connect(DB_PATH) as db:
                cursor = await db.execute(query, params)
                await db.commit()
                
                if cursor.rowcount == 0:
                    return [TextContent(
                        type="text",
                        text=f"Note with ID {note_id} not found."
                    )]
            
            return [TextContent(
                type="text",
                text=f"Note {note_id} updated successfully!"
            )]
        
        elif name == "delete_note":
            # DELETE operation
            note_id = arguments.get("id")
            
            async with aiosqlite.connect(DB_PATH) as db:
                cursor = await db.execute(
                    "DELETE FROM notes WHERE id = ?",
                    (note_id,)
                )
                await db.commit()
                
                if cursor.rowcount == 0:
                    return [TextContent(
                        type="text",
                        text=f"Note with ID {note_id} not found."
                    )]
            
            return [TextContent(
                type="text",
                text=f"Note {note_id} deleted successfully!"
            )]
        
        elif name == "search_notes":
            # SEARCH operation (LIKE query)
            keyword = arguments.get("keyword")
            
            async with aiosqlite.connect(DB_PATH) as db:
                async with db.execute(
                    "SELECT * FROM notes WHERE title LIKE ? OR content LIKE ?",
                    (f"%{keyword}%", f"%{keyword}%")
                ) as cursor:
                    rows = await cursor.fetchall()
            
            if not rows:
                return [TextContent(
                    type="text",
                    text=f"No notes found matching '{keyword}'."
                )]
            
            result = f"Search Results for '{keyword}':\n\n"
            for row in rows:
                result += f"ID: {row[0]}\n"
                result += f"Title: {row[1]}\n"
                result += f"Content: {row[2][:100]}...\n"  # Preview
                result += f"Created: {row[3]}\n"
                result += "-" * 50 + "\n"
            
            return [TextContent(type="text", text=result)]
        
        else:
            return [TextContent(
                type="text",
                text=f"Unknown tool: {name}"
            )]
    
    except Exception as e:
        logger.error(f"Error in {name}: {str(e)}")
        return [TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]


async def main():
    """
    Main entry point for the database MCP server.
    
    Initializes database and starts MCP server on stdio.
    """
    logger.info("Starting Database MCP Server...")
    
    # Initialize database
    await init_database()
    
    logger.info("Available operations: create, read, update, delete, search")
    logger.info("Listening on stdio for MCP connections...")
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    """
    Entry point for the database MCP server.
    
    Usage:
        python database_mcp_server.py
    
    For testing:
        python test_db_server.py
    
    For Claude Desktop:
        Add to claude_desktop_config.json
    """
    asyncio.run(main())
