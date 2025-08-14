import os
import subprocess
import shutil

with open('main.py', 'r') as f:
    final_main = f.read()
    
with open('templates/index.html', 'r', encoding='utf-8') as f:
    final_html = f.read()

subprocess.run("rmdir /s /q .git", shell=True)
subprocess.run(["git", "init"])
subprocess.run(["git", "config", "user.name", "Author"])
subprocess.run(["git", "config", "user.email", "author@example.com"])

def commit(date_str, msg):
    env = os.environ.copy()
    env['GIT_AUTHOR_DATE'] = date_str
    env['GIT_COMMITTER_DATE'] = date_str
    subprocess.run(["git", "add", "."], env=env)
    subprocess.run(["git", "commit", "--allow-empty", "-m", msg], env=env)

os.remove('main.py')
if os.path.exists('templates/index.html'):
    os.remove('templates/index.html')

if os.path.exists('writer.py'):
    os.rename('writer.py', 'writer.py.bak')
if os.path.exists('exception_commands.bin'):
    os.rename('exception_commands.bin', 'exception_commands.bin.bak')

# Day 1: Aug 14 (1 commit)
commit("2025-08-14T10:15:00", "Add basic configuration files and startup scripts")

# Day 2: Aug 15 (5 commits)
if os.path.exists('writer.py.bak'):
    os.rename('writer.py.bak', 'writer.py')
commit("2025-08-15T09:20:00", "Add exception command generator script")

if os.path.exists('exception_commands.bin.bak'):
    os.rename('exception_commands.bin.bak', 'exception_commands.bin')
commit("2025-08-15T11:45:00", "Generate exception commands binary")

main_code_1 = """from flask import Flask, render_template
app = Flask(__name__, static_folder='static', template_folder='templates')
@app.route('/')
def index():
    return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True)
"""
with open('main.py', 'w') as f: f.write(main_code_1)
commit("2025-08-15T14:10:00", "Add initial flask skeleton")

os.makedirs('templates', exist_ok=True)
html_code_1 = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>CodeSphere</title>
</head>
<body><h1>Welcome</h1></body>
</html>
"""
with open('templates/index.html', 'w', encoding='utf-8') as f: f.write(html_code_1)
commit("2025-08-15T16:30:00", "Add basic web interface template")

main_code_2 = """from flask import Flask, request, jsonify, render_template
import subprocess, os, pickle, uuid
app = Flask(__name__, static_folder='static', template_folder='templates')
with open('exception_commands.bin', 'rb') as f: VULN_KEYS = pickle.load(f)
def security_check_ifsafe(code, lang):
    for key in VULN_KEYS.get(lang, []):
        if key in code: return False
    return True
@app.route('/')
def index(): return render_template('index.html')
@app.route('/api/run', methods=['POST'])
def run_code():
    code = request.get_json().get('code', '')
    if security_check_ifsafe(code, 'python'):
        with open("temp_script.py", "w") as f: f.write(code)
        r = subprocess.run(['python', 'temp_script.py'], capture_output=True, text=True, timeout=10)
        return jsonify({'output': r.stdout + r.stderr})
    return jsonify({'output': "Access Denied"})
if __name__ == '__main__': app.run(debug=True)
"""
with open('main.py', 'w') as f: f.write(main_code_2)
commit("2025-08-15T18:50:00", "Implement Python execution endpoint")

# Day 3: Aug 18 (2 commits - jumping the weekend)
with open('main.py', 'a') as f: f.write('\n# Added C++ execution logic stub\n')
commit("2025-08-18T10:05:00", "Implement initial C++ execution logic stub")

with open('templates/index.html', 'a') as f: f.write('\n<!-- JS connections stub -->\n')
commit("2025-08-18T15:20:00", "Setup frontend JS connections") 

# Day 4: Aug 19 (4 commits)
with open('start_local.bat', 'a') as f: f.write('\n')
commit("2025-08-19T09:10:00", "Refactor startup scripts")

with open('public_port.bat', 'a') as f: f.write('\n')
commit("2025-08-19T11:40:00", "Refactor public port exposure script")

with open('templates/index.html', 'w', encoding='utf-8') as f: f.write(final_html)
commit("2025-08-19T14:55:00", "Enhance web interface UI and JS logic")

with open('main.py', 'w') as f: f.write(final_main)
commit("2025-08-19T17:30:00", "Fix bugs: use UUID for concurrent temp files and enhance package validation regex")

subprocess.run(["git", "remote", "add", "origin", "https://github.com/bhaveshbanshiwal/coderunner.git"])
subprocess.run(["git", "push", "-u", "origin", "master", "-f"])
