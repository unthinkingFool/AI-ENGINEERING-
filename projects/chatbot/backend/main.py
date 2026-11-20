import os
from pathlib import Path
from groq import Groq
from dotenv import load_dotenv
from parser import extract_text_resume
from llm import get_llm

load_dotenv()

resume_data=extract_text_resume()
system_prompt="""


"""
user_prompt="""


"""

def get_pipeline(question):

    model,client=get_llm()
    


