from flask import Flask, request, jsonify, render_template
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
