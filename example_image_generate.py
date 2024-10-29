import os
from openai import OpenAI

openai_api_key = os.environ.get("OPENAI_API_KEY")

client = OpenAI(api_key=openai_api_key)


response = client.images.generate(
    prompt="A cute baby sea otter",
    n=2,
    size="1024x1024"
)

print(response.data[0].url)
