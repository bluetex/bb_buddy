import sys
import platform
from flask import Flask, render_template, request, redirect, url_for
import os
import mido
import subprocess
import webbrowser
from params import port_name, outport, homedir_path as default_homedir_path

app = Flask(__name__)

mido.set_backend('mido.backends.rtmidi')

webbrowser.open('http://localhost:8000/')

def validate_params():
    input_names = mido.get_input_names()
    output_names = mido.get_output_names()

    if port_name not in input_names or outport not in output_names:
        return False

    if not os.path.isdir(default_homedir_path):
        return False

    return True

def write_params(selected_input, selected_output, custom_homedir_path):
    params_code = f"import mido\nport_name = '{selected_input}'\noutport = '{selected_output}'\nhomedir_path = r'{custom_homedir_path}'"
    with open('params.py', 'w') as file:
        file.write(params_code)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        selected_input = request.form.get('input')
        selected_output = request.form.get('output')
        custom_homedir_path = request.form.get('homedir_path')
        write_params(selected_input, selected_output, custom_homedir_path)
        # Modify the redirect below to the desired endpoint or route
        
        subprocess.Popen(['python', 'app.py'])
        return redirect('http://localhost:5000/')

    if not validate_params():
        return render_template('setup.html', inputs=inz, outputs=outz, homepath=default_homedir_path)
    
    subprocess.Popen(['python', 'app.py'])
    return redirect('http://localhost:5000/')        

if __name__ == '__main__':
    mido.set_backend('mido.backends.rtmidi')
    outz = mido.get_output_names()
    inz = mido.get_input_names()
    app.run(host="0.0.0.0", port=8000)
