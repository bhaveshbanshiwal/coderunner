from flask import Flask, request, jsonify, render_template
import subprocess
import os
import pickle

app = Flask(__name__, static_folder='static', template_folder='templates')

f = open('exception_commands.bin', 'rb')
VULN_KEYS = pickle.load(f)
f.close()

def security_check_ifsafe(code, lang):
    for key in VULN_KEYS[lang]:
        if key in code:
            return  False
    return True


@app.route('/')
def index():
    return render_template('index.html')


# API for running python
@app.route('/api/run', methods=['POST'])
def run_code():
    data = request.get_json()
    code = data.get('code', '')
    output = ""
    if security_check_ifsafe(code, 'python'):
        # ---- SECURITY WARNING: In a real app, run this in a secure sandbox (Docker container). ----
        try:
            with open("temp_script.py", "w") as f:
                f.write(code)
            
            result = subprocess.run(
                ['python', 'temp_script.py'],
                capture_output=True,
                text=True,
                timeout=10
            )
            output = result.stdout + result.stderr
        # if an error occurs then it produces the error in the frontend terminal
        except Exception as e:
            output = str(e)
        finally:
            # Deleting temp files
            if os.path.exists("temp_script.py"):
                os.remove("temp_script.py")
    else:
        output = "Access Denied"
            
    return jsonify({'output': output})

# API for installing Python packages
@app.route('/api/install', methods=['POST'])
def install_package():
    data = request.get_json()
    package_name = data.get('package', '')

    if not package_name or not package_name.isalnum():
        return jsonify({'log': 'Invalid package name.', 'success': False})
    # Running cmd commands
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

# API for cpp execution
@app.route('/api/run_cpp', methods=['POST'])
def run_cpp_code():
    data = request.get_json()
    code = data.get('code', '')
    output = ""
    if security_check_ifsafe(code, 'cpp'):
        cpp_filename = "temp_script.cpp"
        executable_filename = "temp_executable"


        try:
            # code in file with gcc extension
            with open(cpp_filename, "w") as f:
                f.write(code)
            
        
            compile_result = subprocess.run(
                ['g++', cpp_filename, '-o', executable_filename],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            # checking if gcc compiler produced an error on complilation
            if compile_result.returncode != 0:
                output = compile_result.stderr
            else:
                # if no error
                run_result = subprocess.run(
                    [f'./{executable_filename}'],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                output = run_result.stdout + run_result.stderr

        except Exception as e:
            output = str(e)
        finally:
            # Deleting compiled and base code after getting output
            if os.path.exists(cpp_filename):
                os.remove(cpp_filename)
            if os.path.exists(executable_filename):
                os.remove(executable_filename)
    else:
        output = "Access Denied"

    return jsonify({'output': output})










if __name__ == '__main__':
    app.run(debug=True)
