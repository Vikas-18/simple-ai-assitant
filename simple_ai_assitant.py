from openai import OpenAI
from dotenv import load_dotenv
import os
import json

from tools import TOOLS, FUNCTION_NAME_TO_FUNCTION_MAP

load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

messages = [
    {
        "role": "system",
        "content": (
            "You are a helpful assistant. Answer in 200 words or less. "
        )
    }
]

while True:
    user_input = input("User: ")

    if user_input.lower() == "exit":
        break

    messages.append({
        "role": "user",
        "content": user_input
    })

    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=messages,
        tools=TOOLS
    )

    msg = response.choices[0].message

    if msg.tool_calls:
        messages.append(msg.model_dump(exclude_none=True))

        for tool in msg.tool_calls:
            function_name = tool.function.name
            function_args = json.loads(tool.function.arguments or "{}")

            if function_name in FUNCTION_NAME_TO_FUNCTION_MAP:
                function_to_call = FUNCTION_NAME_TO_FUNCTION_MAP[function_name]
                function_response = function_to_call(**function_args)
            else:
                function_response = f"Function {function_name} not found."

            messages.append({
                "role": "tool",
                "tool_call_id": tool.id,
                "content": str(function_response)
            })

        # Request the final answer after tool execution.
        response = client.chat.completions.create(
            model=os.getenv("MODEL"),
            messages=messages
        )

        msg = response.choices[0].message

    messages.append({
        "role": "assistant",
        "content": msg.content or ""
    })

    print("Assistant:", msg.content)
