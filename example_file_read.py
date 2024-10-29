import os
from openai import OpenAI

openai_api_key = os.environ.get("OPENAI_API_KEY")

client = OpenAI(api_key=openai_api_key)

file = client.files.create(
    file=open("input_text.txt", "rb"),
    purpose="assistants"
)

assistant = client.beta.assistants.create(
    instructions="Write a summary of this text.",
    model="gpt-3.5-turbo",
    tools=[{"type": "code_interpreter"}],
    tool_resources={
        "code_interpreter": {
            "file_ids": [file.id]
        }
    }
)

print("assistant--->:", assistant)

question = "What is the summary of this text?"

thread = client.beta.threads.create(
    messages=[
        {
            "role": "user",
            "content" : question,
            "attachments": [
                {
                    "file_id": file.id,
                    "tools": [{"type": "code_interpreter"}]
                }
            ]
        }
    ]
)

print(f'thread--->:{thread}')

stream = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
    stream=True
)

print(f'stream--->:{stream}')

chat_response = []

for event in stream:
    if event.__class__.__name__ == "ThreadMessageDelta":
        if event.data.delta.content[0].text.value:
            chat_response.append(event.data.delta.content[0].text.value)

add_answer_to_thread = client.beta.threads.messages.create(
    thread.id,
    role="assistant",
    content=("").join(chat_response),
)
print(add_answer_to_thread)
print(add_answer_to_thread.content[0].text.value)
