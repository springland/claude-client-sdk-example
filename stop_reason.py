
import anthropic
import os
client = anthropic.Anthropic();
llm_model = os.getenv('LLM_MODEL')

# Max token
message = client.messages.create(
    model = llm_model,
    max_tokens= 10,
    messages = [
        {
            'role': 'user',
            'stop_sequences': ["END", "STOP"],
            'content' : [
                {
                    'type' : 'text',
                    'text' :"Generate text until you say END"
                }
            ]
        }
    ]
)
print( message.model_dump_json(indent=4) )


# stop sequence
message = client.messages.create(
    model = llm_model,
    max_tokens= 1024,
    messages = [
        {
            'role': 'user',
            'stop_sequences': ["END", "STOP"],
            'content' : [
                {
                    'type' : 'text',
                    'text' :"Generate text until you say END"
                }
            ]
        }
    ]
)
print( message.model_dump_json(indent=4) )