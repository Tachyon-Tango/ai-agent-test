import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Grab the API Key and pass to Google GenAi

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Get and Parse system arguments

num_args = len(sys.argv)

if num_args == 1:
    os._exit(1)

verbose_arg = False
if num_args == 3:
    if sys.argv[2] == "--verbose":
        verbose_arg = True

user_prompt = sys.argv[1]



# Keep track of user prompts

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]


system_prompt = ""

# Actual Generation of the prompt

response = client.models.generate_content(
    model='gemini-2.0-flash-001', 
    contents=messages,
    config=types.GenerateContentConfig(system_instruction=system_prompt),
)

print(response.text)


# Handle Verbose Flag

if(verbose_arg):
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")