import os
from groq import Groq
from dotenv import load_dotenv
from pathlib import Path
import time

load_dotenv()
api_key=os.getenv("GROQ_API_KEY")
model = "openai/gpt-oss-120b"

client=Groq(api_key=api_key)

job_description ="""

AI Engineer
Location: Hybrid / Remote

Employment Type: Full-Time

About the Role
We are looking for an AI Engineer to design, build, and deploy production machine learning systems, large language model (LLM) pipelines, and low-latency inference services. You will bridge research prototypes and scalable software engineering, owning models from data preparation and training through evaluation, serving, and monitoring.

Key Responsibilities
Model & Pipeline Engineering: Build, fine-tune, and evaluate neural networks, transformer architectures, and retrieval or agentic workflows using PyTorch and modern orchestration frameworks.

Production Inference & Serving: Optimize model execution, quantization, batching, and serving throughput (for example, with vLLM or custom inference runtimes) to meet strict latency and cost targets.

Data & Evaluation Systems: Construct reproducible data pipelines, synthetic evaluation suites, and automated regression checks to measure accuracy, grounding, and system reliability in production.

Distributed Systems & MLOps: Integrate AI services with backend APIs, vector or relational data stores, experiment tracking, and observability tooling while handling rate limits, retries, and fault tolerance.

Cross-Functional Execution: Partner with product engineers, data engineers, and applied researchers to turn ambiguous problem statements into maintainable production systems.

Required Qualifications
Strong software engineering fundamentals in Python and at least one systems or typed language (such as C++, Go, Java, or TypeScript), with solid grasp of data structures, algorithms, concurrency, and memory management.

Hands-on experience training, fine-tuning, or deploying deep learning / LLM systems in PyTorch, including custom training loops, loss functions, or model modules.

Practical understanding of transformer mechanics, embeddings, retrieval-augmented generation (RAG), tool/agent orchestration, or evaluation methodologies.

Experience building and debugging production services, REST/gRPC APIs, SQL/NoSQL databases, and Linux/containerized environments.

Clear technical communication and disciplined debugging habits across model weights, data drift, and infrastructure bottlenecks.

Preferred Qualifications
Experience optimizing GPU utilization, KV-cache memory, speculative decoding, or distributed training/inference.

Familiarity with workflow orchestration, experiment tracking, or evaluation platforms (such as MLflow, ZenML, LangGraph, or similar tooling).

Prior work shipping user-facing AI features, real-time pipelines, or high-throughput data systems from scratch.

What We Offer
Competitive compensation aligned with scope and impact (specify band, equity, or bonus structure).

Ownership over high-impact technical architecture and modern compute/tooling infrastructure.

Flexible work arrangement, health benefits, and learning/conference support.

"""

resume="""

Alex Rivera
AI Engineer

San Francisco, CA (Open to Hybrid/Remote) | alex.rivera@email.com | github.com/alexrivera-ai | linkedin.com/in/alexrivera-ai

Summary
AI Engineer with 4+ years of experience building, fine-tuning, and deploying production machine learning systems, large language model (LLM) pipelines, and low-latency inference services. Skilled in bridging research prototypes and scalable software engineering across PyTorch, vLLM, and distributed backend infrastructure.

Technical Skills
Languages: Python, C++, SQL, TypeScript

ML & AI Frameworks: PyTorch, Hugging Face Transformers, LangGraph, vLLM, TensorRT-LLM, Scikit-Learn

Infrastructure & MLOps: Docker, Kubernetes, AWS (EC2, S3, SageMaker), MLflow, FastAPI, gRPC, PostgreSQL, Redis, Qdrant

Core Competencies: LLM Fine-Tuning (LoRA/QLoRA), Retrieval-Augmented Generation (RAG), Agentic Workflows, Quantization (AWQ/GPTQ), Evaluation Pipelines, Distributed Inference

Experience
AI Engineer | Nimbus AI Systems

June 2024 – Present

Architected and deployed a multi-step agentic workflow and hybrid RAG pipeline serving 150K+ daily queries with 99.9% uptime.

Reduced P95 inference latency by 42% and GPU compute costs by 30% by migrating serving workloads to vLLM with AWQ quantization and dynamic batching.

Built an automated evaluation suite combining LLM-as-a-judge metrics and deterministic regression checks to catch prompt and retrieval drift prior to production releases.

Engineered fault-tolerant FastAPI and gRPC microservices with structured output validation, rate-limiting, and fallback routing across model providers.

Machine Learning Engineer | DataPulse Technologies

July 2022 – May 2024

Fine-tuned domain-specific encoder and decoder transformer models in PyTorch using custom training loops and LoRA, improving downstream classification and extraction F1 scores by 14%.

Designed reproducible data ingestion, deduplication, and synthetic dataset generation pipelines processing 10M+ documents per week.

Integrated MLflow experiment tracking and automated model registry promotion gates into CI/CD pipelines, cutting deployment turnaround from days to hours.

Collaborated with backend and product teams to ship real-time semantic search backed by PostgreSQL (pgvector) and Redis caching.

Software Engineer – Data & ML Platform | CloudScale Inc.

June 2021 – June 2022

Developed high-throughput ETL pipelines and REST APIs in Python and C++ to support feature engineering for real-time recommendation models.

Containerized model training and batch inference jobs on Kubernetes, reducing pipeline failure rates by 35% through automated retries and observability dashboards.

Projects
OpenServe-LLM (Low-Latency Inference Engine Wrapper)

Built a lightweight C++ and Python serving wrapper supporting continuous batching, KV-cache memory profiling, and Prometheus telemetry for open-weight 7B–70B models.

EvalGuard (Automated RAG & Agent Benchmark Framework)

Developed an open-source evaluation harness measuring faithfulness, context recall, and tool-calling accuracy across multi-turn agent trajectories.

Education
B.S. in Computer Science

University of California, Davis | Graduated: May 2021

"""

def ask_llm(system_prompt,user_prompt):

    sys_msg={
        "role":"system",
        "content":system_prompt
    }
    user_msg={
        "role":"user",
        "content":user_prompt
    }

    messages=[sys_msg,user_msg]

    response=client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.2,
    )

    answer=response.choices[0].message.content
    return answer

def resume_extract():
    system_prompt=""""

    You are a professional HR assistant. Extract the skills from the candidate resume provided .
    Only return the skills , no other information . Do not invent any info yourself.

    """
    user_prompt=f"""

    Extract the skills from the resume
    {resume}

    """

    answer= ask_llm(system_prompt=system_prompt,user_prompt=user_prompt)
    print("resume skills :\n",answer)
    return answer

def JD_extract():
    system_prompt=""""

    You are a professional HR assistant. Extract the skills from the job description provided .
    Only return the skills , no other information . Do not invent any info yourself.

    """
    user_prompt=f"""

    Extract the skills from the job description
    {job_description}

    """

    answer= ask_llm(system_prompt=system_prompt,user_prompt=user_prompt)
    print("job required skills :\n",answer)
    return answer

def match_skills(candidate,jd):

    system_prompt="""

    You are a professional HR assitant , compare the skills of the candidate and the skills required in the job description
    and produce a final score based on the criteria . The score must be from 0-100.
    Also produce a short verdict for the explnation

    """
    user_prompt=f"""

    Compare and match the skills. 
    Candidate resume : {candidate}
    JOB description :   {jd}

    """

    return ask_llm(system_prompt=system_prompt,user_prompt=user_prompt)

candidate=resume_extract()
time.sleep(5)

jd=JD_extract()
time.sleep(5)

score=match_skills(candidate=candidate,jd=jd)
time.sleep(5)

print(score)