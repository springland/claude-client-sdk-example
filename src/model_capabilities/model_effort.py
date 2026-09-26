import anthropic
import os

from anthropic.types import output_config_param

client = anthropic.Client()
#  set effort
# https://platform.claude.com/docs/en/build-with-claude/effort

llm_model = os.getenv("LLM_MODEL")

# When 1024 is used stop_reason = max_tokens returned
#max_tokens = 1024
max_tokens = 4096
message = client.messages.create(
    model = llm_model,
    max_tokens= max_tokens ,
    messages = [
        {
            'role' : 'user',
            'content':
            [
                {
                'type' : 'text',
                'text' :     'Analyze the trade-offs between microservices and monolithic architectures'
                }
            ]

        }

    ],
    output_config= {
        'effort': 'medium'
    }
)

print( message.model_dump_json(indent=4) )
