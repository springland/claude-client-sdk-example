
import anthropic
import json
import os
import base64
import httpx2

client = anthropic.Anthropic()
llm_model = os.getenv("LLM_MODEL")
#image_url = "https://platform.claude.com/docs/images/vision-example.jpg"
image_url = 'https://en.wikipedia.org/wiki/The_Wave_%28Arizona%29#/media/File:TheWave_1600pixels.jpg'
image_url = (
    "https://upload.wikimedia.org/wikipedia/commons/"
    "b/b2/TheWave_1600pixels.jpg"
)
image_url = 'https://ctfassets.ksldigital.com/0wjmk6wgfops/5mwfCli3JzV5p4MgDaQXVe/d98553028e45bada76029157488d22cd/AdobeStock_63156360.jpeg?w=2140&h=501&fit=fill&f=center&q=70'
response = httpx2.get(image_url, follow_redirects=True)
response.raise_for_status()

image_media_type = response.headers.get("content-type", "").split(";")[0]
print("Content type:", image_media_type)
print("First bytes:", response.content[:20])

if image_media_type not in {
    "image/jpeg", "image/png", "image/webp", "image/gif"
}:
    raise ValueError(f"Expected an image, received {image_media_type}")

image_data = base64.standard_b64encode(response.content).decode("utf-8")

message = client.messages.create(
    model = llm_model,
    max_tokens=1000,
    messages = [
        {
            'role' : 'user',
            'content' : [
                {
                    'type': 'image',
                    'source': {
                        'media_type': image_media_type,
                        'data': image_data,
                        "type": "base64",
                    }
                },
                {"type": "text", "text": "What is in the above image?"}
            ]
        }
    ]
)

print( message.model_dump_json(indent=4) )