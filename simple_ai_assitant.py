
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
            "For mathematical operations, always use the available tools. "
            "For questions about company leave, provident fund, insurance, medical benefits, or ESOP policies, use the search tool "
            "and answer only from the returned company documents. "
            "When operations are dependent, execute them sequentially. "
            "Always pass the actual result of the previous tool call "
            "as the argument to the next tool call."
        )
    }
]

while True:
    user_input = input("\nUser: ")

    if user_input.lower() == "exit":
        break

    messages.append({
        "role": "user",
        "content": user_input
    })

    while True:

        stream = client.chat.completions.create(
            model=os.getenv("MODEL"),
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            stream=True
        )

        content = ""
        tool_calls = {}

        print("Assistant: ", end="", flush=True)

        for chunk in stream:

            delta = chunk.choices[0].delta

            # Stream normal text
            if delta.content:
                content += delta.content
                print(delta.content, end="", flush=True)

            # Collect tool calls
            if delta.tool_calls:
                for tool in delta.tool_calls:

                    index = tool.index

                    if index not in tool_calls:
                        tool_calls[index] = {
                            "id": "",
                            "type": "function",
                            "function": {
                                "name": "",
                                "arguments": ""
                            }
                        }

                    if tool.id:
                        tool_calls[index]["id"] = tool.id

                    if tool.function.name:
                        tool_calls[index]["function"]["name"] += (
                            tool.function.name
                        )

                    if tool.function.arguments:
                        tool_calls[index]["function"]["arguments"] += (
                            tool.function.arguments
                        )

        print()

        # No tool calls: final response
        if not tool_calls:
            messages.append({
                "role": "assistant",
                "content": content
            })
            break

        # Append assistant tool-call message
        assistant_tool_message = {
            "role": "assistant",
            "content": content or None,
            "tool_calls": list(tool_calls.values())
        }

        messages.append(assistant_tool_message)

        # Execute tools
        for tool in tool_calls.values():

            function_name = tool["function"]["name"]

            function_args = json.loads(
                tool["function"]["arguments"] or "{}"
            )

            print(f"\n[Calling tool: {function_name}]")
            print("Arguments:", function_args)

            if function_name in FUNCTION_NAME_TO_FUNCTION_MAP:

                function_to_call = FUNCTION_NAME_TO_FUNCTION_MAP[
                    function_name
                ]

                function_response = function_to_call(**function_args)

            else:
                function_response = (
                    f"Function {function_name} not found."
                )

            print("Tool result:", function_response)

            messages.append({
                "role": "tool",
                "tool_call_id": tool["id"],
                "content": str(function_response)
            })
