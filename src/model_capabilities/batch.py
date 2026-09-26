import time
import os
import anthropic
from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.messages.batch_create_params import Request
from util.claude_client import get_claude_client_and_default_model

client , llm = get_claude_client_and_default_model()

message_batch = client.messages.batches.create(

    requests= [
        Request(
            custom_id="springland-89e99a40-66d4-4b47-90f8-b83b0b70a9fa",
            params = MessageCreateParamsNonStreaming(
                model  = llm ,
                max_tokens = 1024 ,
                messages = [
                    {
                        'role' : 'user',
                        'content' : [
                            {
                                'type': 'text',
                                'text': "What is the capital of France?"
                            }
                        ]
                    }

                ]
            )
        ) ,

        Request(
            custom_id="springland-368c51f9-27d1-4ed4-ad93-893f22325f4a",
            params=MessageCreateParamsNonStreaming(
                model=llm,
                max_tokens=1024,
                messages=[
                    {
                        'role': 'user',
                        'content': [
                            {
                                'type': 'text',
                                'text': "What is the capital of China"
                            }
                        ]
                    }

                ]
            )
        )
    ]
)

print( message_batch.model_dump_json(indent=4) )


batch_id = message_batch.id

while True:
    message_batch = client.messages.batches.retrieve(batch_id)

    if message_batch.processing_status == 'ended':
        break
    print( message_batch.model_dump_json(indent=4) )

    time.sleep(60)

print(' complete received \n\n')


print(message_batch.model_dump_json(indent=4))

print(" batch result \n\n")
for entry in client.messages.batches.results(batch_id):
    print(f"\nRequest: {entry.custom_id}")

    if entry.result.type == "succeeded":
        for block in entry.result.message.content:
            if block.type == "text":
                print(block.text)
    else:
        print(entry.result)