import anthropic
import os
client = anthropic.Anthropic();
llm_model = os.getenv('LLM_MODEL_NAME')

weather_tool = {
    "name": "get_weather",
    "description": "Get the current weather in a given location",
    "input_schema": {
        "type": "object",
        "properties": {
            "location": {"type": "string", "description": "City and state"},
        },
        "required": ["location"],
    },
}
def execute_tool(name, tool_input):
    """Execute a tool and return the result."""
    print(f"Executing tool: {name} , input: {tool_input}")
    return f"Weather in {tool_input.get('location', 'unknown')}: 72°F"


messages = [
{"role": "user", "content": "What is the weather in San Francisco?"}
]

message = client.messages.create(
    model=llm_model,
    max_tokens=1024,
    tools=[weather_tool],
    messages=messages,

)

while message.stop_reason != 'end_turn':

    print(message.model_dump_json(indent=4))

    if message.stop_reason == "tool_use":
        messages.append({
            "role": "assistant",
            "content": [
                block.model_dump(mode="json")
                for block in message.content
            ],
        })
        tool_results = []
        # Extract and execute the tool
        for block in message.content:
            if block.type == "tool_use":
                result = execute_tool(block.name, block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result,
                })

        messages.append({
            "role": "user",
            "content": tool_results,
        })
    else:
        raise RuntimeError(
            f"Unexpected stop reason: {message.stop_reason}"
        )
    message = client.messages.create(
        model=llm_model,
        max_tokens=1024,
        tools=[weather_tool],
        messages=messages,

)
print('done')
print(message.model_dump_json(indent=4))
