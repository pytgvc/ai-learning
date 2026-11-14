from google import genai
from google.genai import types
import os
import datetime


# 1. SETUP GEMINI

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found!")

client = genai.Client(api_key=api_key)


# 2. TOOL 1: ADD NUMBERS

def add_numbers(a, b):
    return a + b


# 3. TOOL 2: GET TODAY'S DATE

def get_today_date():
    return str(datetime.date.today())


# 4. TOOL DESCRIPTIONS FOR GEMINI

add_tool = types.FunctionDeclaration(
    name="add_numbers",
    description="Add two numbers and return their sum.",
    parameters={
        "type": "object",
        "properties": {
            "a": {
                "type": "number",
                "description": "First number"
            },
            "b": {
                "type": "number",
                "description": "Second number"
            }
        },
        "required": ["a", "b"]
    }
)


date_tool = types.FunctionDeclaration(
    name="get_today_date",
    description="Return today's date.",
    parameters={
        "type": "object",
        "properties": {}
    }
)


tools = types.Tool(
    function_declarations=[add_tool, date_tool]
)


# 5. AVAILABLE PYTHON FUNCTIONS

available_tools = {
    "add_numbers": add_numbers,
    "get_today_date": get_today_date
}


# 6. USER QUESTION

prompt = input("Ask something: ")

history = [
    types.Content(
        role="user",
        parts=[types.Part.from_text(text=prompt)]
    )
]


# 7. AGENT LOOP

step_count = 0
max_steps = 5

while step_count < max_steps:

    step_count += 1

    print(f"\n----- STEP {step_count} -----")

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=history,
        config=types.GenerateContentConfig(
            tools=[tools]
        )
    )

    # Print raw response
    print("Gemini is thinking")

    # Get model response
    model_content = response.candidates[0].content

    # Save model response in history
    history.append(model_content)

    # Check function calls
    function_calls = response.function_calls

    if not function_calls:

        print("\nFinal Answer:")
        print(response.text)
        break

    # Execute requested functions
    tool_parts = []

    for call in function_calls:

        tool_name = call.name
        tool_args = dict(call.args)

        print("\nTool requested:", tool_name)
        print("Tool inputs:", tool_args)

        if tool_name in available_tools:

            try:
                result = available_tools[tool_name](**tool_args)

                print("Tool result:", result)

                tool_result = {"result": result}

            except Exception as error:

                tool_result = {"error": str(error)}

        else:

            tool_result = {"error": "Unknown tool"}

        # Prepare tool response
        tool_parts.append(
            types.Part.from_function_response(
                name=tool_name,
                response=tool_result,
              
            )
        )

    # Send all tool results back to Gemini
    history.append(
        types.Content(
            role="user",
            parts=tool_parts
        )
    )

else:

    print("\nMaximum steps reached. Agent stopped.")

