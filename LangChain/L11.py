from openai import OpenAI
import os
import json

from dotenv import load_dotenv, find_dotenv
load_dotenv()

client = OpenAI(
    api_key = os.environ['OPENAI_API_KEY']
)

def find_sum (a, b):
    """Find the sum of the two values passed as parameters"""
    
    ans = {
        "sum": a+b
    }

    return json.dumps(ans)

# https://platform.openai.com/docs/api-reference/chat/create

functions = [
    {
        "name": "find_sum",
        "description": "Find the sum of the two values passed as parameters",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {
                    "type": "integer",
                    "description": "first of the numbers to be summed together",
                },
                "b": {
                    "type": "integer",
                    "description": "second of the numbers to be summed together",
                }
            },
            "required": ["a", "b"]
        }
    }
]

messages = [
    {
        "role": "user",
        "content": "What's the sum of 12.5 and?"
    }
]

response = client.chat.completions.create(
    messages = messages,
    model = "gpt-3.5-turbo",
    functions = functions
)

# print(args)
print(response.choices[0].message)
args = json.loads(response.choices[0].message.function_call.arguments)
print(args)

print(find_sum(args['a'], args['b']))
