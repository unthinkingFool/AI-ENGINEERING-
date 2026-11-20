
from pydantic import BaseModel, Field
from typing import Optional


class personalData(BaseModel):
    name: str = Field(..., description="Full name of the candidate.")
    phone_number: str = Field(..., description="Candidate's contact phone number.")
    email: str = Field(..., description="Candidate's professional email address.")
    github: str = Field(..., description="GitHub profile URL.")
    linkedin: str = Field(..., description="LinkedIn profile URL.")


class educationData(BaseModel):
    institutionName: str = Field(..., description="Name of the university, college, or educational institution.")
    degreeName: str = Field(..., description="Degree or qualification obtained or currently pursuing.")
    department: str = Field(..., description="Department, major, or field of study.")
    duration: str = Field(..., description="Start and end dates or duration of the education.")
    cgpa: Optional[str] = Field(None, description="CGPA, GPA, or academic result. Optional if not mentioned.")


class projectData(BaseModel):
    projectName: str = Field(..., description="Name or title of the project.")
    techStack: list[str] = Field(..., description="Programming languages, frameworks, libraries, and tools used.")
    description: str = Field(..., description="Detailed explanation of the project's purpose, functionality, and implementation.")
    impact: str = Field(..., description="Measurable outcomes, achievements, results, or value delivered by the project.")
    gitRepo: str = Field(..., description="GitHub or other source code repository URL.")


class experienceData(BaseModel):
    companyName: str = Field(..., description="Name of the company or organization where the candidate worked.")
    duration: str = Field(..., description="Employment start and end dates or total duration.")
    role: str = Field(..., description="Job title or professional position held.")
    impact: str = Field(..., description="Key responsibilities, achievements, contributions, and measurable results.")
    techStack: list[str] = Field(..., description="Technologies, programming languages, frameworks, and tools used.")


class researchData(BaseModel):
    title: str = Field(..., description="Title of the research project, publication, or paper.")
    fieldName: str = Field(..., description="Research domain, discipline, or area of study.")
    organizationName: str = Field(..., description="University, research lab, institution, or organization associated with the research.")
    impact: str = Field(..., description="Research contributions, findings, outcomes, or significance.")
    paper_link: str = Field(..., description="URL of the published paper, preprint, or research documentation.")


class resumeData(BaseModel):
    personal_data: personalData = Field(..., description="Candidate's personal and contact information.")
    education: educationData = Field(..., description="Candidate's educational background and qualifications.")
    current_role: str = Field(..., description="Candidate's current professional role, job title, or career position.")
    skills: list[str] = Field(..., description="List of the candidate's technical, professional, and relevant soft skills.")
    projects: list[projectData] = Field(..., description="List of projects completed or currently being developed by the candidate.")
    experience: Optional[list[experienceData]] = Field(None, description="List of professional work experiences. Optional if no experience is mentioned.")
    research: Optional[list[researchData]] = Field(None, description="List of research projects, publications, or academic research experiences. Optional if not mentioned.")
