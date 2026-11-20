import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)
model = "openai/gpt-oss-120b"

stream = client.chat.completions.create(

    messages=[
        {
            "role": "system",
            "content": "You are a helpful research assistant"
        },
        # Set a user message for the assistant to respond to.
        {
            "role": "user",
            "content": "explain how neural networks are made broadly",
        }
    ],

    model=model,

    temperature=2,

    max_completion_tokens=1024,

    top_p=1,

    stop=None,

    # streaming
    stream=True,
)

# print like streaming
for chunk in stream:
    content=chunk.choices[0].delta.content
    if content:
        print(content,end="",flush=True)

