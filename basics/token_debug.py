import os
from pathlib import Path
from pyexpat import model
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
model = "openai/gpt-oss-120b"

llm = Groq(api_key=GROQ_API_KEY)

prompt1="hello"
prompt2="10 names for food restaurants"
prompt3="Explain the importance of small language models"

prompts=[
    prompt1,

]
print("\n\n\n")

for prompt in prompts:
    response = llm.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=50,
    )
    usage = response.usage
    print(f"Prompt: {prompt} \n Total Tokens: {usage.total_tokens} \n Prompt Tokens: {usage.prompt_tokens} \n Completion Tokens: {usage.completion_tokens}")
    print(usage)
    print(response.choices[0].message.content)
    print("\n\n\n")

