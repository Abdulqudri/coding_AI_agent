"""For getting file content"""
import os
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):
    """read the file content in a directory"""
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_directory):
        return f"Error: {file_path} is not in the working directory"

    if not os.path.isfile(abs_file_path):
        return f"Errpr: {file_path} is not a file"

    file_content = ""
    try:
        with open(abs_file_path, "r") as f:
            file_content = f.read(MAX_CHARS)
            if len(file_content) >= MAX_CHARS:
                file_content += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )
            return file_content
    except Exception as e:
        return f"Exception reading file: {e}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get the content of the given file as a string, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the file, from the working directory."
            ),
        },
    ),
)