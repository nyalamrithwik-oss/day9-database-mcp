# Database MCP Server

> **Production-ready Model Context Protocol server with SQLite database integration for Claude Desktop**

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![MCP](https://img.shields.io/badge/MCP-1.0+-green.svg)
![Status](https://img.shields.io/badge/status-production-brightgreen.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

**Part of:** [30-Day RAG & MCP Learning Journey](https://github.com/nyalamrithwik-oss/30-day-rag-learning) | **Day 9 of 30**

---

## 🎯 Overview

This MCP server enables Claude Desktop to create, read, update, delete, and search notes in a persistent SQLite database. It demonstrates full CRUD operations with async database handling, professional error management, and real-world Claude Desktop integration.

**🔥 Live Demo:** Works directly in Claude Desktop with persistent data storage!

---

## ✨ Features

### 6 Database Tools for Claude
- **create_note** - Insert new notes with auto-incrementing IDs
- **get_all_notes** - Retrieve all notes with timestamps
- **get_note_by_id** - Fetch specific note by ID
- **update_note** - Modify existing note (title and/or content)
- **delete_note** - Remove notes from database
- **search_notes** - Find notes by keyword (LIKE query)

### Technical Highlights
- ✅ **Async Operations** - Non-blocking I/O with aiosqlite
- ✅ **SQL Injection Prevention** - Parameterized queries throughout
- ✅ **Error Handling** - Comprehensive try/except blocks
- ✅ **Type Safety** - Full type hints
- ✅ **Professional Logging** - Debug and info level logging
- ✅ **Production Ready** - Tested and verified in Claude Desktop

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- pip package manager
- Claude Desktop (for integration testing)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/nyalamrithwik-oss/day9-database-mcp.git
cd day9-database-mcp

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. Install dependencies
pip install -r day9_requirements.txt
```

### Dependencies
```
mcp>=1.0.0                    # Model Context Protocol SDK
aiosqlite>=0.19.0             # Async SQLite support
pydantic>=2.5.0               # Data validation
python-dotenv>=1.0.0          # Environment variables
```

---

## 💻 Usage

### Option 1: Local Testing

Test all database operations without Claude Desktop:

```bash
python test_db_server.py
```

**Expected Output:**
```
======================================================================
  DATABASE MCP SERVER TEST
======================================================================

✅ Connection established
✅ Found 6 tools: create_note, get_all_notes, get_note_by_id, 
   update_note, delete_note, search_notes

TESTING DATABASE OPERATIONS
----------------------------------------------------------------------
Test 1: Creating Notes ✅
Test 2: Retrieving All Notes ✅
Test 3: Getting Note by ID ✅
Test 4: Updating Note ✅
Test 5: Searching Notes ✅
Test 6: Deleting Note ✅

======================================================================
All database operations tested successfully!
======================================================================
```

---

### Option 2: Claude Desktop Integration

#### Step 1: Configure Claude Desktop

Edit your Claude Desktop config file:
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **Mac:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux:** `~/.config/Claude/claude_desktop_config.json`

Add this configuration:

```json
{
  "mcpServers": {
    "database": {
      "command": "/absolute/path/to/venv/Scripts/python.exe",
      "args": [
        "/absolute/path/to/database_mcp_server.py"
      ]
    }
  }
}
```

**Windows Example:**
```json
{
  "mcpServers": {
    "database": {
      "command": "C:\\Users\\YourName\\day9-database-mcp\\venv\\Scripts\\python.exe",
      "args": [
        "C:\\Users\\YourName\\day9-database-mcp\\database_mcp_server.py"
      ]
    }
  }
}
```

**Mac/Linux Example:**
```json
{
  "mcpServers": {
    "database": {
      "command": "/Users/YourName/day9-database-mcp/venv/bin/python",
      "args": [
        "/Users/YourName/day9-database-mcp/database_mcp_server.py"
      ]
    }
  }
}
```

#### Step 2: Restart Claude Desktop

Close and reopen Claude Desktop completely.

#### Step 3: Verify Integration

In Claude Desktop, ask:
```
"What tools do you have access to?"
```

You should see **"Database notes"** in the Utilities section.

#### Step 4: Test Operations

Try these commands in Claude Desktop:

**Create a note:**
```
"Create a note titled 'Meeting Notes' with content 'Discussed Q4 goals'"
```

**Show all notes:**
```
"Show me all my notes"
```

**Search notes:**
```
"Search for notes about meetings"
```

**Update a note:**
```
"Update note 1 with new content: 'Updated goals for Q4'"
```

**Delete a note:**
```
"Delete note 1"
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────┐
│      Claude Desktop             │
│      (MCP Client)                │
└────────────┬────────────────────┘
             │
             │ stdio (JSON-RPC)
             │
             ▼
┌─────────────────────────────────┐
│   Database MCP Server           │
│                                  │
│   ┌──────────────────────┐      │
│   │  Tool Registry       │      │
│   │  - create_note       │      │
│   │  - get_all_notes     │      │
│   │  - get_note_by_id    │      │
│   │  - update_note       │      │
│   │  - delete_note       │      │
│   │  - search_notes      │      │
│   └──────────────────────┘      │
│                                  │
│   ┌──────────────────────┐      │
│   │  Request Handler     │      │
│   │  - Async execution   │      │
│   │  - Error handling    │      │
│   │  - Response format   │      │
│   └──────────────────────┘      │
└────────────┬────────────────────┘
             │
             │ aiosqlite
             │
             ▼
┌─────────────────────────────────┐
│      SQLite Database            │
│      (data.db)                  │
│                                  │
│   Table: notes                  │
│   - id (INTEGER PRIMARY KEY)    │
│   - title (TEXT NOT NULL)       │
│   - content (TEXT NOT NULL)     │
│   - created_at (DATETIME)       │
└─────────────────────────────────┘
```

---

## 💾 Database Schema

```sql
CREATE TABLE notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**Fields:**
- `id` - Auto-incrementing primary key
- `title` - Note title (required)
- `content` - Note content (required)
- `created_at` - Timestamp of creation (auto-generated)

---

## 📚 API Reference

### create_note

Create a new note in the database.

**Parameters:**
```json
{
  "title": "string (required)",
  "content": "string (required)"
}
```

**Example:**
```json
{
  "title": "Meeting Notes",
  "content": "Discussed Q4 goals and timelines"
}
```

**Response:**
```
Note created successfully! ID: 1
Title: Meeting Notes
```

---

### get_all_notes

Retrieve all notes from the database, ordered by creation date (newest first).

**Parameters:** None

**Response:**
```
All Notes:

ID: 3
Title: Project Update
Content: Completed Phase 1
Created: 2025-12-27 14:30:00
--------------------------------------------------
ID: 2
Title: Todo List
Content: Review code, Update docs
Created: 2025-12-27 12:15:00
--------------------------------------------------
```

---

### get_note_by_id

Get a specific note by its ID.

**Parameters:**
```json
{
  "id": "integer (required)"
}
```

**Example:**
```json
{
  "id": 1
}
```

**Response:**
```
Note Details:

ID: 1
Title: Meeting Notes
Content: Discussed Q4 goals and timelines
Created: 2025-12-27 11:30:00
```

---

### update_note

Update an existing note's title and/or content.

**Parameters:**
```json
{
  "id": "integer (required)",
  "title": "string (optional)",
  "content": "string (optional)"
}
```

**Example:**
```json
{
  "id": 1,
  "content": "Updated Q4 goals - added performance metrics"
}
```

**Response:**
```
Note 1 updated successfully!
```

---

### delete_note

Delete a note by ID.

**Parameters:**
```json
{
  "id": "integer (required)"
}
```

**Example:**
```json
{
  "id": 1
}
```

**Response:**
```
Note 1 deleted successfully!
```

---

### search_notes

Search notes by keyword in title or content.

**Parameters:**
```json
{
  "keyword": "string (required)"
}
```

**Example:**
```json
{
  "keyword": "meeting"
}
```

**Response:**
```
Search Results for 'meeting':

ID: 1
Title: Meeting Notes
Content: Discussed Q4 goals and timelines
Created: 2025-12-27 11:30:00
--------------------------------------------------
```

---

## 📁 Project Structure

```
day9-database-mcp/
├── database_mcp_server.py         # Main MCP server (~391 lines)
├── test_db_server.py               # Test client (~151 lines)
├── day9_requirements.txt           # Python dependencies
├── README.md                       # This file
├── DAY9_NOTES.md                   # Detailed learning notes
├── .gitignore                      # Git exclusions
│
├── Helper Scripts (Optional):
│   ├── update_claude_config.py     # Config automation
│   ├── merge_claude_config_from_backup.py  # Config recovery
│   └── run_server_check.py         # Diagnostic tool
│
└── data.db                         # SQLite database (auto-created)
```

---

## 🧪 Testing

### Running Tests

```bash
# Activate virtual environment
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Run comprehensive test suite
python test_db_server.py
```

### Test Coverage

| Operation | Status | Description |
|-----------|--------|-------------|
| **CREATE** | ✅ Passing | Inserts 3 test notes |
| **READ (All)** | ✅ Passing | Retrieves all notes |
| **READ (By ID)** | ✅ Passing | Gets note ID=1 |
| **UPDATE** | ✅ Passing | Modifies note ID=1 |
| **SEARCH** | ✅ Passing | Finds notes by keyword |
| **DELETE** | ✅ Passing | Removes note ID=2 |

**Overall Coverage:** 100% (6/6 operations)

---

## 🔧 Troubleshooting

### Issue: MCP server shows warning in Claude Desktop

**Symptoms:**
- Warning triangle next to "database" in MCP settings
- Tools not appearing in Claude

**Solution:**
1. Verify Python path exists:
   ```bash
   # Windows PowerShell
   Test-Path "C:\path\to\venv\Scripts\python.exe"
   ```
2. Check config syntax (commas, backslashes)
3. Use absolute paths, not relative
4. Restart Claude Desktop after config changes

---

### Issue: "Module 'mcp' not found"

**Solution:**
```bash
# Make sure venv is activated
.\venv\Scripts\activate

# Reinstall dependencies
pip install -r day9_requirements.txt
```

---

### Issue: Database locked

**Symptoms:**
```
sqlite3.OperationalError: database is locked
```

**Solution:**
- Close any other connections to data.db
- Restart the MCP server
- Delete data.db (loses data) and let it recreate

---

### Issue: Permission denied on data.db

**Solution:**
- Check file permissions
- Run terminal/PowerShell as administrator
- Move project to user directory (avoid C:\Program Files)

---

## 📊 Performance

### Benchmarks (Local Testing)

- **Connection:** ~50ms
- **Tool registration:** ~10ms
- **Create operation:** ~5ms
- **Read operation:** ~3ms
- **Update operation:** ~5ms
- **Delete operation:** ~4ms
- **Search operation:** ~8ms

**Total test suite:** ~2 seconds (including initialization)

---

## 🔒 Security Considerations

### Implemented Protections

✅ **SQL Injection Prevention**
```python
# Using parameterized queries
await db.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
```

✅ **Input Validation**
- Pydantic schemas for type checking
- Required field enforcement
- Type safety throughout

✅ **Error Handling**
- No sensitive data in error messages
- Graceful degradation
- Comprehensive logging

### Known Limitations

⚠️ **No Authentication** - Anyone with Claude Desktop access can use tools  
⚠️ **No Authorization** - All operations available to all users  
⚠️ **No Encryption** - Data stored in plaintext  
⚠️ **No Audit Logging** - No record of who did what  

**For Production:** Add authentication, authorization, encryption, and audit logs.

---

## 🚀 Future Enhancements

### Planned Features
- [ ] Multi-user support with user IDs
- [ ] Note tagging and categories
- [ ] Full-text search with ranking
- [ ] Export notes to markdown/PDF
- [ ] Import notes from files
- [ ] Note sharing between users
- [ ] Backup and restore functionality
- [ ] Web interface for note management

### Possible Integrations
- [ ] Sync with cloud storage (Dropbox, Google Drive)
- [ ] Export to note-taking apps (Notion, Obsidian)
- [ ] Email integration for note delivery
- [ ] Calendar integration for time-based notes
- [ ] Webhooks for external notifications

---

## 📈 Project Statistics

```
Date Completed:  December 27, 2025
Time Investment: 5.5 hours
Code Written:    700+ lines (391 server + 151 test + helpers)
Tools Created:   6 MCP tools
Helper Scripts:  3 diagnostic tools
Test Coverage:   100% (6/6 operations)
Status:          Production Ready
```

---

## 🎓 What I Learned

### Technical Skills
- MCP protocol architecture and implementation
- Async programming patterns in Python
- SQLite database operations and best practices
- Production debugging and problem-solving
- Multi-server MCP deployment
- Professional code organization

### Challenges Overcome
- Fixed requirements file corruption
- Rebuilt virtual environment after pip corruption
- Created 3 diagnostic helper scripts
- Resolved Claude Desktop config issues
- Handled Windows UTF-8 encoding problems

**Full learning notes:** See [DAY9_NOTES.md](DAY9_NOTES.md)

---

## 📝 Documentation

- **[DAY9_NOTES.md](DAY9_NOTES.md)** - Complete learning journey with challenges, solutions, and insights
- **[GITHUB_PUSH_GUIDE.md](GITHUB_PUSH_GUIDE.md)** - Git workflow and repository setup
- **[SETUP_COMPLETE.md](SETUP_COMPLETE.md)** - Setup verification and testing guide

---

## 🤝 Contributing

This is a learning project, but feedback and suggestions are welcome!

**To contribute:**
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - feel free to use it for learning and projects!

---

## 👤 Author

**Rithwik Nyalam**

- GitHub: [@nyalamrithwik-oss](https://github.com/nyalamrithwik-oss)
- LinkedIn: [Rithwik Nyalam](https://linkedin.com/in/rithwik-nyalam)
- Email: nyalamrithwik@gmail.com
- Location: Karimnagar, Telangana, India

---

## 🔗 Related Projects

### 30-Day RAG & MCP Learning Journey

**Week 1: RAG Systems**
- [Day 1: Basic RAG with LangChain](https://github.com/nyalamrithwik-oss/day1-basic-rag)
- [Day 3: Vector Database Comparison](https://github.com/nyalamrithwik-oss/day3-vector-comparison)
- [Day 6-7: Smart Knowledge Base](https://github.com/nyalamrithwik-oss/portfolio-project-1) (Portfolio Project #1)

**Week 2: Model Context Protocol**
- [Day 8: Calculator MCP Server](https://github.com/nyalamrithwik-oss/day8-mcp-basics)
- **Day 9: Database MCP Server** ← You are here
- Day 10-12: Custom API MCP (Coming soon)

---

## 🌟 Acknowledgments

- **Anthropic** - For Claude and the MCP protocol
- **aiosqlite** - For async SQLite support
- **Python Community** - For excellent documentation and support

---

## 📊 Repository Stats

![GitHub stars](https://img.shields.io/github/stars/nyalamrithwik-oss/day9-database-mcp?style=social)
![GitHub forks](https://img.shields.io/github/forks/nyalamrithwik-oss/day9-database-mcp?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/nyalamrithwik-oss/day9-database-mcp?style=social)

---

<div align="center">

**Built with ❤️ as part of the 30-day RAG & MCP learning journey**

[⭐ Star this repo](https://github.com/nyalamrithwik-oss/day9-database-mcp) • [🐛 Report Bug](https://github.com/nyalamrithwik-oss/day9-database-mcp/issues) • [💡 Request Feature](https://github.com/nyalamrithwik-oss/day9-database-mcp/issues)

**Day 9 Complete! ✅**

*Last Updated: December 27, 2025*

</div>
