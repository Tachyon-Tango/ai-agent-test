import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_files_info import *
from functions.get_file_content import *
from functions.write_file import *
from functions.run_python import *

### Constants
WORKING_DIRECTORY = "./calculator"
MAX_GEN_ITERS = 20


### Function Definitions

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    func_name = function_call_part.name
    func_args = function_call_part.args

    match func_name:
        case "get_files_info":
            result =  get_files_info(WORKING_DIRECTORY, **func_args)
        case "get_file_content":
            result =  get_file_content(WORKING_DIRECTORY, **func_args)
        case "write_file":
            result =  write_file(WORKING_DIRECTORY, **func_args)
        case "run_python_file":
            result =  run_python_file(WORKING_DIRECTORY, **func_args)
        case _:
            return types.Content(
                    role="tool",
                    parts=[
                        types.Part.from_function_response(
                            name=func_name,
                            response={"error": f"Unknown function: {func_name}"},
                        )
                    ],
                )

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=func_name,
                response={"result": result},
            )
        ],
    )


### Run Main Algorithm

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

#Define available functions

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file
    ]
)

# Define system prompt

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

Execute this plan with the tool before giving any text response back to the user.

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""




for generation_iteration in range(MAX_GEN_ITERS):
    try:
        # Actual Generation of the prompt
        response = client.models.generate_content(
            model='gemini-2.0-flash-001', 
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt),
        )

        # Add the model candidates to the messages
        for candidate in response.candidates:
            messages.append(candidate.content)

        # Process the generation resuls
        if response.function_calls != None: #len(response.function_calls) > 0:
            for function_call_part in response.function_calls:
                function_call_result = call_function(function_call_part, verbose_arg)
                if function_call_result.parts[0].function_response.response == None:
                    raise Exception("Function Call Response was None.")
                if verbose_arg: 
                    print(f"-> {function_call_result.parts[0].function_response.response}")
                messages.append(function_call_result)
        else:
            print(response.text)
            break


    except Exception as e:
        raise Exception(e)



# Handle Verbose Flag

if(verbose_arg):
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")