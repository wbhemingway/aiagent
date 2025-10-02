import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

if len(sys.argv) < 2:
    sys.exit(1)
user_prompt = sys.argv[1]

load_dotenv()

messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
)
print(response.text)

if "--verbose" in sys.argv[2:]:
    meta_data = response.usage_metadata
    prompt_tokens = meta_data.prompt_token_count
    response_tokens = meta_data.candidates_token_count
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {response_tokens}")

