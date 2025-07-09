
import os
from .config import *

def get_file_content(working_directory, file_path):
    try:
        path = os.path.join(working_directory, file_path)
        abs_target_path = os.path.abspath(path)
        abs_working_path = os.path.abspath(working_directory)
        if not abs_target_path.startswith(abs_working_path):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        file_content_string = ""
        with open(path, "r") as f:
            file_content_string = f.read(FILE_CHAR_LIMIT)
            if len(file_content_string) == FILE_CHAR_LIMIT:
                file_content_string = file_content_string + f'[...File "{file_path}" truncated at {str(FILE_CHAR_LIMIT)} characters]'
        return file_content_string

    except Exception as e:
        return f"Error: {e}"