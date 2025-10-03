import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import available_functions, call_function
from prompts import system_prompt


def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    for _ in range(20):
        try:
            done = generate_content(client, messages, verbose)
            if done:
                print(done)
                break
        except Exception as e:
            return f"Error: calling model: {e}"


def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    for candidate in response.candidates:
        messages.append(candidate.content)

    if not response.function_calls:
        return response.text

    for function_call_part in response.function_calls:
        function_call_result = call_function(
            function_call_part=function_call_part, verbose=verbose
        )
        call_response = function_call_result.parts[0].function_response.response
        if not call_response:
            raise Exception("No response was gotten from the function call")
        if verbose:
            print(call_response)
        tool_msg = types.Content(
            role="user",
            parts=[
                types.Part(
                    function_response=types.FunctionResponse(
                        name=function_call_part.name,
                        response=call_response,
                    )
                )
            ],
        )
        messages.append(tool_msg)


if __name__ == "__main__":
    main()
