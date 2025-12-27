import os, json, shutil
appdata = os.environ.get('APPDATA')
if not appdata:
    raise SystemExit('APPDATA environment variable not found')
path = os.path.join(appdata, 'Claude', 'claude_desktop_config.json')
backup = os.path.join(appdata, 'Claude', 'claude_desktop_config_backup_day9.json')
print('Config path:', path)
if os.path.exists(path):
    shutil.copy(path, backup)
    print('Backed up existing config to:', backup)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            obj = json.load(f)
    except Exception as e:
        print('Failed to parse existing JSON:', e)
        obj = {}
else:
    print('No existing config found; creating new one at:', path)
    obj = {}
if 'mcpServers' not in obj or not isinstance(obj['mcpServers'], dict):
    obj['mcpServers'] = {}
# Add database entry
obj['mcpServers']['database'] = {
    'command': r"C:\Users\nyala\OneDrive\RAG\week2-mcp\day9-database-mcp\venv\Scripts\python.exe",
    'args': [r"C:\Users\nyala\OneDrive\RAG\week2-mcp\day9-database-mcp\database_mcp_server.py"]
}
# Ensure directory exists
os.makedirs(os.path.dirname(path), exist_ok=True)
with open(path, 'w', encoding='utf-8') as f:
    json.dump(obj, f, indent=2)
print('Updated config written to:', path)
print('\n--- mcpServers section ---')
print(json.dumps(obj['mcpServers'], indent=2))
