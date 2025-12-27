import os, json
appdata = os.environ.get('APPDATA')
if not appdata:
    raise SystemExit('APPDATA environment variable not found')
path = os.path.join(appdata, 'Claude', 'claude_desktop_config.json')
backup = os.path.join(appdata, 'Claude', 'claude_desktop_config_backup_day9.json')
print('Config path:', path)
if not os.path.exists(backup):
    print('Backup not found at', backup)
    raise SystemExit(1)
# Try to read backup with utf-8-sig to handle BOM
with open(backup, 'r', encoding='utf-8-sig') as f:
    try:
        obj = json.load(f)
        print('Loaded backup JSON successfully')
    except Exception as e:
        print('Failed to parse backup JSON:', e)
        raise
if 'mcpServers' not in obj or not isinstance(obj['mcpServers'], dict):
    obj['mcpServers'] = {}
# Ensure database entry set
obj['mcpServers']['database'] = {
    'command': r"C:\Users\nyala\OneDrive\RAG\week2-mcp\day9-database-mcp\venv\Scripts\python.exe",
    'args': [r"C:\Users\nyala\OneDrive\RAG\week2-mcp\day9-database-mcp\database_mcp_server.py"]
}
# Write merged config
os.makedirs(os.path.dirname(path), exist_ok=True)
with open(path, 'w', encoding='utf-8') as f:
    json.dump(obj, f, indent=2)
print('Merged config written to:', path)
print('\n--- mcpServers section ---')
print(json.dumps(obj.get('mcpServers', {}), indent=2))
