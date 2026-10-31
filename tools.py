from datetime import datetime
from zoneinfo import ZoneInfo


def get_current_time(timezone: str = "UTC"):
    """
    Returns the current time in the specified timezone.
    Example: Europe/London, Asia/Kolkata
    """
    
    try:
        print(f"Getting current time for timezone: {timezone}")
        current_time = datetime.now(ZoneInfo(timezone))
        return current_time.strftime("%Y-%m-%d %H:%M:%S %Z")
    except Exception:
        return f"Invalid timezone: {timezone}"

def get_sum(a,b):
    """
    Returns the sum of two numbers.
    """
    print(f"Calculating the sum of {a} and {b}")
    return a + b

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get the current date and time in a specified IANA timezone, such as Europe/London or Asia/Kolkata.",
            "parameters": {
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "IANA timezone, for example Europe/London or Asia/Kolkata."
                    }
                },
                "required": ["timezone"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_sum",
            "description": "Get the sum of two numbers.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "First number."
                    },
                    "b": {
                        "type": "number",
                        "description": "Second number."
                    }
                },
                "required": ["a", "b"]
            }
            }
    }
]

FUNCTION_NAME_TO_FUNCTION_MAP = {
    "get_current_time": get_current_time,
    "get_sum": get_sum
}
