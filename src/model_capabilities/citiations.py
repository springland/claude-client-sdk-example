import os
import anthropic
import base64
from util.claude_client import get_claude_client_and_default_model
client , llm_model = get_claude_client_and_default_model()


with open('cdc_84800_DS1.pdf', 'rb') as f:
    pdf_base64 = base64.b64encode(f.read()).decode("utf-8")



message = client.messages.create(
    model = llm_model,
    max_tokens= 4096,
    messages= [
        {
            'role' : 'user',
            'content': [
                {
                  'type' :'document',
                    "source": {
                        "type": "base64",
                        "media_type": "application/pdf",
                        "data": pdf_base64,
                    },
                    "citations": {"enabled": True},
                    "title": "cdc_84800_DS1.pdf",
                },
                {
                    'type' :'text',
                    'text' : 'What is CDC requirement on reporting travelers from China with specific symptoms during COVID-19? ',
                }


            ]
        }
    ]
)

print( message.model_dump_json(indent=4) )