# utils/improvement_suggester.py
import os
from groq import Groq
from dotenv import load_dotenv
from google.cloud import secretmanager

load_dotenv()

def get_api_key():
    # Try local .env
    api_key = os.getenv("GROQ_API_KEY")
    if api_key:
        return api_key

    # Try GCP secret manager (when deployed)
    try:
        client = secretmanager.SecretManagerServiceClient()
        project_id = os.getenv("GCP_PROJECT")
        name = f"projects/{project_id}/secrets/GROQ_API_KEY/versions/latest"
        response = client.access_secret_version(name=name)
        return response.payload.data.decode("utf-8")
    except Exception as e:
        raise RuntimeError(f"Could not load GROQ_API_KEY: {e}")

client = Groq(api_key=get_api_key())

def suggest_improvements(resume_text, jd_text):
    prompt = f"""
You are an expert resume consultant. Given the resume and the job description below, suggest improvements to better match the resume to the job.

Resume:
{resume_text}

Job Description:
{jd_text}

List clear bullet points on what the candidate should add or improve in the resume to align with the job.
"""
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="mixtral-8x7b-32768"
    )
    return chat_completion.choices[0].message.content
