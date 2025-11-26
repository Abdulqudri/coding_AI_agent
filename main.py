"""the main intry point of the project"""
import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from call_function import call_function

load_dotenv()

def main():
    """the main function of the program"""

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not set in environment variables.")

    if len(sys.argv) < 2:
        print("Usage: python main.py <your_input>")
        sys.exit(1)

    VERBOSE_FLAG = False
    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        VERBOSE_FLAG = True
    user_input = sys.argv[1]
    system_prompt = """
    You are a helpful AI coding agent.
    when a user asks a question or make a request, make a function call plan. You can perform the following operations:
    -List files and directories
    -Read the content of a file
    -Write to a file(create or update)
    -Run a python file with optional arguments

    when the user asks about the code project - they are referring to the working directory.
    So, you should typically start by looking at the project's files, and figuring out how to run the project
    and how to run its tests, you'll always want to test the tests and the actual project to verify that the behavior is working.
    All paths you provide should be relative to the working directory. 
    You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_input)]),
    ]

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
        ]
    )

    config = types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt
    )
    client = genai.Client(api_key=GEMINI_API_KEY)

    max_iters = 20
    for i in range(0, max_iters):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=config,
        )
        if response is None or response.usage_metadata is None:
            print("response is malformed")
            return
        if VERBOSE_FLAG:
            print(f"User prompt: {user_input}")
            print(f"Prompt Tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Completion Tokens: {response.usage_metadata.candidates_token_count}")

        if response.candidates:
            for candidate in response.candidates:
                if candidate is None or candidate.content is None:
                    continue
                messages.append(candidate.content)

        if response.function_calls:
            for function_call_part in response.function_calls:
                result = call_function(function_call_part, VERBOSE_FLAG)
                messages.append(result)
                print(result)
        else:
            print(f"AI Response: {response.text}")
            return


main()
