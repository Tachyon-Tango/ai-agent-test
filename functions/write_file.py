
import os

from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the specified contents into a file in the specified path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to write contents to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The contents to be written into the file.",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    try:
        path = os.path.join(working_directory, file_path)

        abs_target_path = os.path.abspath(path)
        abs_working_path = os.path.abspath(working_directory)
        if not abs_target_path.startswith(abs_working_path):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        path_dir = os.path.dirname(path)
        if not os.path.exists(path_dir):
            os.makedirs(path_dir)

        with open(path, "w") as f:
            f.write(content)
    
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"