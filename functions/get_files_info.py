
import os

from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory=None):
    try:
        path = os.path.join(working_directory, directory)
        abs_target_path = os.path.abspath(path)
        abs_working_path = os.path.abspath(working_directory)

        if not abs_target_path.startswith(abs_working_path):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if not os.path.isdir(path):
            f'Error: "{directory}" is not a directory'

        dir_file_list = os.listdir(path)

        output = ""

        for file in dir_file_list:
            file_name = file
            filepath = os.path.join(path, file)
            file_size = os.path.getsize(filepath)
            is_dir = not os.path.isfile(filepath)
            line = f"- {file_name}: file_size={file_size} bytes, is_dir={is_dir}"
            output = "\n".join([output, line])

        return output

    except Exception as e:
        return f"Error: {e}"