
import json
from pathlib import Path

from schemas import resumeData

from PyPDF2 import PdfReader
from llm import get_llm


model, client = get_llm()

BASE_DIR = Path(__file__).resolve().parent
resumePath = BASE_DIR / "resume" / "sample.pdf"
outputPath = BASE_DIR / "resume_data.json"


def extract_text_from_resume(pdf_path: Path) -> str:
    """Extract text from all pages of a PDF resume."""

    reader = PdfReader(str(pdf_path))

    extracted_text = ""

    for page in reader.pages:
        text = page.extract_text()
        if text:
            extracted_text += text + "\n"

    return extracted_text.strip()


def parse_data(resume_text: str) -> resumeData:

    """Extract structured resume information using the LLM and validate it."""

    schema=resumeData.model_json_schema()

    prompt = f"""
    You are an expert resume information extraction system.

    Extract all relevant information from the resume below.

    Follow the provided resume schema strictly.
    Do not invent any data yourself.
    Do not fabricate or assume information.
    For missing required string fields, use an empty string.
    For missing required list fields, use an empty list.
    For missing optional fields, use null.

    RESUME:
    {resume_text}
    """

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": f"Extract resume information and return valid JSON only. Format : {schema}"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        response_format={"type": "json_object"},
        temperature=0
    )

    response_content = response.choices[0].message.content

    return response_content


def extract_text_resume():
    """Complete resume extraction and JSON storage pipeline."""

    if not resumePath.exists():
        raise FileNotFoundError(f"Resume not found: {resumePath}")

    # Step 1: Extract PDF text
    resume_text = extract_text_from_resume(resumePath)

    if not resume_text:
        raise ValueError("No text could be extracted from the PDF.")

    # Step 2: Parse extracted text using LLM + Pydantic
    parsed_data = parse_data(resume_text)

    # Step 3: Convert Pydantic model into JSON
    json_data = parsed_data.model_dump_json(indent=4)

    # Step 4: Save JSON file
    outputPath.write_text(json_data, encoding="utf-8")

    # Step 5: Return parsed Pydantic object
    return parsed_data


