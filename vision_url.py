import anthropic
import os

from anthropic.resources.messages import messages

llm_model = os.getenv('LLM_MODEL')
client = anthropic.Anthropic()
message = client.messages.create(

    model = llm_model,
    max_tokens= 1024,
    messages= [
                    {
                        'role' : 'user',
                        'content' : [
                            {
                                'type' : 'image',
                                'source': {
                                    'type' : 'url',
                                    'url' : 'https://ctfassets.ksldigital.com/0wjmk6wgfops/5mwfCli3JzV5p4MgDaQXVe/d98553028e45bada76029157488d22cd/AdobeStock_63156360.jpeg?w=2140&h=501&fit=fill&f=center&q=70',
                                }
                            },
                            {
                                'type': 'text',
                                "text": "What is in the above image?"
                            }
                        ]
                    }
        ]
)

print(message.model_dump_json(indent=4))

