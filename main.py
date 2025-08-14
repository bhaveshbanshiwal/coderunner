from flask import Flask, request, jsonify, render_template
import subprocess # For running external commands
import os # ---- To clean up created files ----

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

# API endpoint to run Python code
@app.route('/api/run', methods=['POST'])
def run_code():
    data = request.get_json()
    code = data.get('code', '')
    
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
    except Exception as e:
        output = str(e)
    finally:
        # ---- Clean up the temporary file ----
        if os.path.exists("temp_script.py"):
            os.remove("temp_script.py")
            
    return jsonify({'output': output})

# API for installing Python packages
@app.route('/api/install', methods=['POST'])
def install_package():
    data = request.get_json()
    package_name = data.get('package', '')

    if not package_name or not package_name.isalnum():
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


# ---- START OF CHANGES ----
# ---- API endpoint for C++ code execution ----
@app.route('/api/run_cpp', methods=['POST'])
def run_cpp_code():
    data = request.get_json()
    code = data.get('code', '')

    cpp_filename = "temp_script.cpp"
    executable_filename = "temp_executable"
    output = ""

    try:
        # ---- Write the C++ code to a .cpp file ----
        with open(cpp_filename, "w") as f:
            f.write(code)
        
        # ---- Compile the .cpp file using g++ ----
        compile_result = subprocess.run(
            ['g++', cpp_filename, '-o', executable_filename],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        # ---- If there was a compilation error, return the error message ----
        if compile_result.returncode != 0:
            output = compile_result.stderr
        else:
            # ---- If compilation was successful, run the executable ----
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
        # ---- Clean up the created .cpp and executable files ----
        if os.path.exists(cpp_filename):
            os.remove(cpp_filename)
        if os.path.exists(executable_filename):
            os.remove(executable_filename)
            
    return jsonify({'output': output})
# ---- END OF CHANGES ----

if __name__ == '__main__':
    app.run(debug=True)
