"""the main intry point of the project"""
import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import get_files_info

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

    messages = [
        types.Content(role="user",
                      parts=types.Part(text=user_input)),
    ]

    client = genai.Client(api_key=GEMINI_API_KEY)

    response = client.models.generate_content(model="gemini-2.5-flash",
                                              contents=messages)
    if VERBOSE_FLAG:
        print(f"User prompt: {response.text}")
        print(f"Prompt Tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Completion Tokens: {response.usage_metadata.candidates_token_count}")


print(get_files_info("functions"))