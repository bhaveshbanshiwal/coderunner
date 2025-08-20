from flask import Flask, request, jsonify, render_template
import subprocess
import os
import pickle
import uuid
import re
from flask_cors import CORS

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

from security import security_check_ifsafe

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/status')
def status():
    return jsonify({'status': 'running', 'service': 'coderunner API'})

@app.route('/api/run', methods=['POST'])
def run_code():
    data = request.get_json()
    code = data.get('code', '')
    output = ""
    if security_check_ifsafe(code, 'python'):
        unique_id = uuid.uuid4().hex
        filename = f"temp_{unique_id}.py"
        try:
            with open(filename, "w") as f:
                f.write(code)
            
            result = subprocess.run(
                ['python', filename],
                capture_output=True,
                text=True,
                timeout=10
            )
            output = result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            output = "Error: Execution timed out after 10 seconds."
        except Exception as e:
            output = f"Error: {str(e)}"
        finally:
            if os.path.exists(filename):
                os.remove(filename)
    else:
        output = "Access Denied"
            
    return jsonify({'output': output})

@app.route('/api/install', methods=['POST'])
def install_package():
    data = request.get_json()
    package_name = data.get('package', '')

    if not package_name or not re.match(r'^[a-zA-Z0-9_\-]+$', package_name):
        return jsonify({'log': 'Invalid package name.', 'success': False})
    try:
        result = subprocess.run(
            ['pip', 'install', package_name],
            capture_output=True,
            text=True,
            timeout=60
        )
        log = result.stdout + result.stderr
        success = result.returncode == 0
        return jsonify({'log': log, 'success': success})
    except Exception as e:
        return jsonify({'log': str(e), 'success': False})

@app.route('/api/run_cpp', methods=['POST'])
def run_cpp_code():
    data = request.get_json()
    code = data.get('code', '')
    output = ""
    if security_check_ifsafe(code, 'cpp'):
        unique_id = uuid.uuid4().hex
        cpp_filename = f"temp_{unique_id}.cpp"
        executable_filename = f"temp_exe_{unique_id}"

        try:
            with open(cpp_filename, "w") as f:
                f.write(code)
            
            compile_result = subprocess.run(
                ['g++', cpp_filename, '-o', executable_filename],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if compile_result.returncode != 0:
                output = compile_result.stderr
            else:
                exe_to_run = f"{executable_filename}.exe" if os.name == 'nt' else f"./{executable_filename}"
                run_result = subprocess.run(
                    [exe_to_run],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                output = run_result.stdout + run_result.stderr

        except Exception as e:
            output = str(e)
        finally:
            if os.path.exists(cpp_filename):
                os.remove(cpp_filename)
            if os.path.exists(executable_filename):
                os.remove(executable_filename)
            if os.path.exists(f"{executable_filename}.exe"):
                os.remove(f"{executable_filename}.exe")
    else:
        output = "Access Denied"

    return jsonify({'output': output})

@app.route('/api/run_js', methods=['POST'])
def run_js_code():
    data = request.get_json()
    code = data.get('code', '')
    output = ""
    if security_check_ifsafe(code, 'javascript'):
        unique_id = uuid.uuid4().hex
        js_filename = f"temp_{unique_id}.js"

        try:
            with open(js_filename, "w") as f:
                f.write(code)
            
            run_result = subprocess.run(
                ['node', js_filename],
                capture_output=True,
                text=True,
                timeout=10
            )
            output = run_result.stdout + run_result.stderr

        except Exception as e:
            output = str(e)
        finally:
            if os.path.exists(js_filename):
                os.remove(js_filename)
    else:
        output = "Access Denied"

    return jsonify({'output': output})

if __name__ == '__main__':
    app.run(debug=True)
