
from datetime import datetime
from zoneinfo import ZoneInfo

from rag import search as rag_search


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


def get_sum(a, b):
    """
    Returns the sum of two numbers.
    """
    print(f"Calculating the sum of {a} and {b}")
    return a + b


def get_square(a):
    """
    Returns the square of a number.
    """
    print(f"Calculating the square of {a}")
    return a * a

def search(query, top_k=3):
    """
    Search company policy documents and return the most relevant sections.
    """
    print(f"Searching company documents for: {query}")
    return rag_search(query, top_k)

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "ONLY use this function when the user explicitly asks for current date or time. NEVER use it for mathematical calculations.",
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
    },
    {
        "type": "function",
        "function": {
            "name": "get_square",
            "description": "Get the square of a number.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "Number to square."
                    }
                },
                "required": ["a"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search",
            "description": "Search company policy documents for leave balances, provident fund deductions, insurance, medical benefits, or ESOP information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Question or keywords to search in company documents."
                    },
                    "top_k": {
                        "type": "integer",
                        "description": "Maximum number of relevant document sections to return.",
                        "default": 3
                    }
                },
                "required": ["query"]
            }
        }
    }
]


FUNCTION_NAME_TO_FUNCTION_MAP = {
    "get_current_time": get_current_time,
    "get_sum": get_sum,
    "get_square": get_square,
    "search": search
}
