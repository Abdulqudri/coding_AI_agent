from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
def main():

    working_directory = "functions"
    root_contents = get_files_info(working_directory)
    print(root_contents)
    bin_contents = get_files_info(working_directory, "__pycache__")
    print(bin_contents)
    bin_contents = get_files_info(working_directory, "/bin")
    print(bin_contents)
    all_contents = get_files_info(working_directory, "../")
    print(all_contents)

    function = get_file_content(working_directory, "get_file_content.py")
    print(function)
    function = get_file_content(working_directory, "index.py")
    print(function)

main()
