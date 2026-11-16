import os
from pathlib import Path
from pydantic import BaseModel,Field
from groq import Groq
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import json
import csv



load_dotenv()

## ---------------------
# pipeline:
#   1. Extract text from file
#   2. Parse text with Groq
#   3: candidate matching against job description
#   4. Store in a local list to later store in a csv
#   5. return the data

class CandidateData(BaseModel):
    name: str = Field(..., description="Candidate's full name")
    email: str = Field(..., description="Candidate's email address")
    phone: str = Field(..., description="Candidate's phone number")
    skills: list[str] = Field(..., description="List of candidate's skills")
    experience: str = Field(..., description="Candidate's work experience")
    education: str = Field(..., description="Candidate's educational background")
    projects: list[str] = Field(..., description="List of candidate's projects")

MODEL_NAME="openai/gpt-oss-120b"

def get_model():

    try:
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables.")

        client = Groq(api_key=api_key)
        return client

    except Exception as e:
        print(f"Error initializing Groq client: {e}")
        return None

def extract_text_from_pdf(file_path: Path) -> str | None:
    try:
        # one file at a time
        reader = PdfReader(str(file_path))
        text = ""
        for page in reader.pages:
            text += (page.extract_text() or "") + "\n"
        return text
    
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None

def parse_text(text: str)-> dict:

    llm= get_model()
    schema=CandidateData.model_json_schema()

    user_message = {
                "role":"user",
                "content":f"""
                        You are an expert resume parser. 
                        Text to parse:
                        {text}
                        """
            }
    system_message ={
                "role":"system",
                "content":f"""
                        You will parse the text and return a JSON object with the following fields:
                        {schema}
                If information is missing, use empty strings or empty lists.
                Never invent candidate information.
                        """
            } 

    messages=[system_message,user_message]

    response = llm.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        max_tokens=1000,
        temperature=0.2,
    )

    answer = response.choices[0].message.content
    candidate_dict=CandidateData.model_validate_json(answer).model_dump()

    return candidate_dict

def store_data(data: list[dict]):

    if not data :
        print("No data to store.")
        return

    csv_file_path = Path("candidate_data.csv")

    fields_name=list(CandidateData.model_fields.keys()) + ["score","explanation"]

    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
        
        writer = csv.DictWriter(csvfile, fieldnames=fields_name)
        writer.writeheader()

        for candidate in data:

            candidate=candidate.copy()

            candidate['skills']=', '.join(candidate['skills'])
            candidate['projects']=', '.join(candidate['projects'])

            writer.writerow(candidate)

    print(f"Data stored in {csv_file_path}")

def return_data(data: list[dict]):

    for candidate in data:
        print(json.dumps(candidate, indent=4))

def match_candidate_to_job(candidate_data: dict, job_description: str):

    llm= get_model()
    user_message = {
                "role":"user",
                "content":f"""
                        You are an expert job matcher. 
                        Candidate data:
                        {json.dumps(candidate_data)}
                        Job description:
                        {job_description}
                        """
            }
    system_message = {
        "role": "system",
        "content": """
        You are an expert job matcher.

        Evaluate the candidate only against job-related criteria.

        Return a JSON object containing:
        - score: integer between 0 and 100
        - explanation: short explanation of the score

        Do not consider protected personal characteristics.
        """
    }

    response = llm.chat.completions.create(
        model=MODEL_NAME,
        messages=[system_message,user_message],
        max_tokens=1000,
        temperature=0.1,
    )

    answer = response.choices[0].message.content
    return json.loads(answer)


def main():
    
    data_dir = Path("./data")
    pdf_files = list(data_dir.glob("*.pdf"))

    if not pdf_files:
        print("No PDF files found in the data directory.")
        return

    print(f"Found {len(pdf_files)} PDF files. Processing...")

    job_description = """
        We are looking for a ai engineer with experience in Python, machine learning, and data analysis, llm , producion agentic ai system.
        The ideal candidate should have a strong background in algorithms and data structures, as well as experience with 
        cloud platforms like AWS or Azure alongside deeper expertise in AI systems. 
        Excellent communication skills and the ability to work in a team are also essential.
        """
    
    all_candidate_data = []

    for index ,pdf_path in enumerate(pdf_files,start=1):

        print(f"Processing file {index}/{len(pdf_files)}: {pdf_path.name}")
        # step 1 : extract data from pdf
        text = extract_text_from_pdf(pdf_path)

        if not text:
            print(f"Skipping {pdf_path.name} due to extraction error.")
            continue

        try:
            #step 2: parse data with llm
            candidate_data = parse_text(text)
            print(f"Successfully parsed data for {pdf_path.name}: {json.dumps(candidate_data, indent=4)}")
        
            #step 3: candidate matching against job description
            match_result=match_candidate_to_job(
                candidate_data=candidate_data,
                job_description=job_description
            )
            candidate_data["score"]=match_result["score"]
            candidate_data["explanation"]=match_result["explanation"]

            # step 4: store data in local list
            all_candidate_data.append(candidate_data)

        except Exception as e:
            print(f"Error parsing text from {pdf_path.name}: {e}")
            continue

    # step 5: store in the csv file
    store_data(all_candidate_data)
    return_data(all_candidate_data)

    print("Matching candidates to job description...")


    

if __name__ == "__main__":
    main()
