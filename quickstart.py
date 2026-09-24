import anthropic
import os
import json
client = anthropic.Anthropic()
llm_model = os.getenv("LLM_MODEL")
message = client.messages.create(
    model=llm_model ,
    max_tokens=1000,
    system="You are a helpful assistant.",

    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Hi, how are you?"
                }
            ]
        }
    ]
)
#print(message.content)


for block in message.content:
    print(block.type , block , '\n')

print( message.model_dump_json(indent=4) )