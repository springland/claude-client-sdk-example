
from util.claude_client import get_claude_client_and_default_model

client , llm = get_claude_client_and_default_model()

# llm = 'claude-opus-5-5'

#
# very interesting
# deepseek does not force output format , still in text but gives top five officers
# claude-haiku-4-5-20251001 says {"name": "Trump 2020 Administration Officers", "date_of_birth": "2020-01-20"} , totally bullshit
# opus-5-5 only gives 1 record {"name":"Donald J. Trump","gender":"male","date_of_birth":"1946-06-14"}
message = client.messages.create(
    model = llm,
    max_tokens= 12800,
    messages = [
        {
            'role' : 'user',
            'content' : [

                {
                    'type' : 'text',
                    'text' : 'List top 5 major officers in Trump 2020 administration',
                }
            ]
        }
    ],
    output_config={
        "format": {
            "type": "json_schema",
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "gender": {"type": "string"},
                    "date_of_birth": {"type": "string"},
                },
                "required": ["name", "date_of_birth"],
                "additionalProperties": False,
            },
        }
    },

)
print( message.model_dump_json(indent=4) )

print(next(block.text for block in message.content if block.type == "text"))