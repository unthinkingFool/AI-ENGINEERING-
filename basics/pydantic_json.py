import os
from pathlib import Path
from pyexpat import model
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel, Field

load_dotenv()

# ------------------------------
# Defining a Pydantic model for structured output
# ------------------------------


class UserData(BaseModel):
    name : str = Field(..., description="The user's name") # required field
    age : int = Field(..., description="The user's age") # required field
    email : str = Field(..., description="The user's email address") # required field
    address: str | None = Field(None, description="The user's address") # optional field

testPerson_1 = UserData(
    name="John Doe",
    age=30,
    email="johndoe@example.com",
    address="123 Main St, Anytown, USA"
)

print(testPerson_1)


# --------------------------------
#### Integrating with llm
# -------------------------------

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)
model = "openai/gpt-oss-120b"

class CodeSnippet(BaseModel):
    title: str = Field(..., description="The title of the code snippet")
    code_language: str = Field(..., description="The programming language of the code snippet")
    code: str = Field(..., description="The actual code snippet")

# creating the JSON schema for the CodeSnippet model
schema = CodeSnippet.model_json_schema()

prompt = f"""
Write a code snippet in Python that defines a function to calculate the factorial of a number.
The function should take an integer as input and return the factorial of that number. 
"""

user_message={
    "role": "user",
    "content": prompt
}
system_message={
    "role": "system",
    "content": f"You are a helpful assistant that provides code snippets in JSON format: {schema}"
}

messages = [system_message, user_message]

response = client.chat.completions.create(
    model=model,
    messages=messages,
    max_completion_tokens=2000,
)

print(response.choices[0].message.content)


# --------------------------------
# extracting required info from text
# -------------------------------
Text= """
 hi customer care , this is swapnil das . I have bought 
 a iphpone 13 from your store on 12th jan 2025.
 currently iam facing some issue with the display 
 of the phone.It is not responsing properly and sometimes the phone also 
 become very hot .
 hahahaha
 i am going home.
 i want for a servicing facility.
 contact me on email : abc@gmail.com
 mobile : 12345678901
 address : hello,dhaka-100
"""

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)
model = "openai/gpt-oss-120b"

class CustomerServiceRequest(BaseModel):
    name: str = Field(..., description="The customer's name")
    product: str = Field(..., description="The product purchased by the customer")
    purchase_date: str = Field(..., description="The date of purchase")
    issue: str = Field(..., description="The issue faced by the customer")
    contact_email: str = Field(..., description="The customer's email address")
    contact_mobile: str = Field(..., description="The customer's mobile number")
    address: str = Field(..., description="The customer's address")


schema = CustomerServiceRequest.model_json_schema()

user_message={
    "role": "user",
    "content": f"Extract information from the text: {Text}."
}
system_message={
    "role": "system",
    "content": f"""
            You are a helpful assistant that extracts information from text 
            and provides it in JSON format according to the following schema: {schema}
    """
}

messages = [system_message, user_message]

response = client.chat.completions.create(
    model=model,
    messages=messages,
    max_completion_tokens=2000,
    temperature=0.0,
)

answer = response.choices[0].message.content
print(answer)

# accessing the extracted information from the response
import json

raw_json = answer
data_file=json.loads(raw_json)
customer_request = CustomerServiceRequest(**data_file)

print(f"Name: {customer_request.name}")
print(f"Product: {customer_request.product}")
print(f"Purchase Date: {customer_request.purchase_date}")
print(f"Issue: {customer_request.issue}")
print(f"Contact Email: {customer_request.contact_email}")
print(f"Contact Mobile: {customer_request.contact_mobile}")
print(f"Address: {customer_request.address}")
