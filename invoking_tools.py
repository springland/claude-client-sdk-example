import anthropic
import os

client = anthropic.Client()
llm_model = os.getenv('LLM_MODEL')

tools = [
    {
        'name' : 'get_weather',
        'description' : 'Get current weather of a city',
        'input_schema': {
            'city' : 'string'
        }
    }

]

client.messages.create(
    model = llm_model ,
    max_tokens= 1024 ,

)

