import os, json, time, subprocess, sys
from pathlib import Path

appdata = os.environ.get('APPDATA')
if not appdata:
    print('ERROR: APPDATA not set')
    sys.exit(1)
cfg = Path(appdata) / 'Claude' / 'claude_desktop_config.json'
print('Config path:', cfg)
if cfg.exists():
    try:
        with open(cfg, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print('\n--- mcpServers (from config) ---')
        print(json.dumps(data.get('mcpServers', {}), indent=2)[:4000])
    except Exception as e:
        print('Failed to load JSON (trying utf-8-sig):', e)
        try:
            with open(cfg, 'r', encoding='utf-8-sig') as f:
                data = json.load(f)
            print('\n--- mcpServers (from config, utf-8-sig) ---')
            print(json.dumps(data.get('mcpServers', {}), indent=2)[:4000])
        except Exception as e2:
            print('Failed to parse config:', e2)
else:
    print('Config file does not exist')

py = Path('C:/Users/nyala/OneDrive/RAG/week2-mcp/day9-database-mcp/venv/Scripts/python.exe')
scr = Path('C:/Users/nyala/OneDrive/RAG/week2-mcp/day9-database-mcp/database_mcp_server.py')
print('\nCheck Python exists:', py.exists(), str(py))
print('Check server script exists:', scr.exists(), str(scr))

if not py.exists() or not scr.exists():
    print('\nOne or more paths missing; aborting start attempt')
    sys.exit(0)

print('\nStarting server subprocess (capturing first 5 seconds of output)...')
proc = subprocess.Popen([str(py), str(scr)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
start = time.time()
lines = []
try:
    while True:
        if proc.stdout is None:
            break
        line = proc.stdout.readline()
        if line:
            print('OUT:', line.strip())
            lines.append(line)
        if time.time() - start > 5:
            break
    # after capturing, terminate
    proc.terminate()
    try:
        proc.wait(timeout=2)
    except subprocess.TimeoutExpired:
        proc.kill()
except Exception as e:
    print('Error while running subprocess:', e)
finally:
    if proc.poll() is None:
        try:
            proc.kill()
        except Exception:
            pass

print('\nCaptured output lines:', len(lines))
for l in lines[-20:]:
    print(l.rstrip())

print('\nDone.')
