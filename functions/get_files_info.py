
import os

def get_files_info(working_directory, directory=None):
    try:
        path = os.path.join(working_directory, directory)
    except Exception:
        return f"Error: os.path.join() returned an exception from the given relative path."

    try:
        abs_target_path = os.path.abspath(path)
        abs_working_path = os.path.abspath(working_directory)
    except Exception:
        return f"Error: os.path.abspath() returned an exception from the given relative path."

    if not abs_target_path.startswith(abs_working_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'


    try:
        if not os.path.isdir(path):
            f'Error: "{directory}" is not a directory'
    except Exception:
        return f"Error: os.path.isdir() returned an exception from the given relative path."

    try:
        dir_file_list = os.listdir(path)
    except Exception:
        return f"Error: os.listdir() returned an exception from the given relative path."

    output = ""

    for file in dir_file_list:
        #print(file)
        file_name = file
        filepath = os.path.join(path, file)
        #print(filepath)

        try:
            file_size = os.path.getsize(filepath)
        except Exception:
            return f"Error: os.path.getsize() returned an exception from a file in the given relative path."

        try:
            is_dir = not os.path.isfile(filepath)
        except Exception:
            return f"Error: os.path.isfile() returned an exception from a file in the given relative path."

        line = f"- {file_name}: file_size={file_size} bytes, is_dir={is_dir}"
        output = "\n".join([output, line])

    
    return output