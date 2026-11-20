import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
api_key=os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("error while finding api key")

def get_llm():
    try:
        model="openai/gpt-oss-120b"
        return model , Groq(api_key=api_key)
    except:
        return ValueError("error while creating llm client")