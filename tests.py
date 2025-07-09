# from subdirectory.filename import function_name
from functions.get_files_info import get_files_info

print("\n---\n")
print(get_files_info("calculator", "."))
print("\n---\n")
print(get_files_info("calculator", "pkg"))
print("\n---\n")
print(get_files_info("calculator", "/bin"))
print("\n---\n")
print(get_files_info("calculator", "../"))
