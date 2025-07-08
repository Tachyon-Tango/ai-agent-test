import os
import sys
from dotenv import load_dotenv
from google import genai

# Grab the API Key and pass to Google GenAi

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Get and Parse system arguments

num_args = len(sys.argv)

if num_args != 2:
    os._exit(1)

user_prompt = sys.argv[1]


# Actual Generation of the prompt

response = client.models.generate_content(
    model='gemini-2.0-flash-001', 
    contents=user_prompt
)

print(response.text)

print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
print(f"Response tokens: {response.usage_metadata.candidates_token_count}")