
import os
import subprocess

from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes the python file in the specified path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to be executed, relative to the working directory.",
            ),
        },
    ),
)

def run_python_file(working_directory, file_path):
    try:
        path = os.path.join(working_directory, file_path)

        abs_target_path = os.path.abspath(path)
        abs_working_path = os.path.abspath(working_directory)
        if not abs_target_path.startswith(abs_working_path):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(path):
            return f'Error: File "{file_path}" not found.'

        file_extension = file_path.split(".")[-1]
        if not file_extension == "py":
            return f'Error: "{file_path}" is not a Python file.'

        raw_output = subprocess.run(["python", file_path] , timeout=30, capture_output=True, cwd=abs_working_path)
        stderr = raw_output.stderr
        stdout = raw_output.stdout
        return_code = raw_output.returncode

        if stderr == "" and stdout == "" and return_code == 0:
            return "No output produced."
        else:
            response = []
            response.append(f"STDOUT:{str(stdout)}")
            response.append(f"STDERR:{str(stderr)}")
            if not return_code == 0:
                response.append(f"Process exited with code {return_code}")
            return "\n".join(response)

        

    except Exception as e:
        return f"Error: executing Python file: {e}"